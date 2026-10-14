"""Tests of ddsx2dds (CTest: ddsx2dds.<scenario>): DDSx textures made by ddsxCvt (PC) in each compression, converted
back to DDS and compared with their source; the header dump, the compression check, the GUI atlas bundles
(<name>.ta.bin), ASTC decoding and broken input.

python ddsx2dds_tests.py <scenario> <ddsxCvt> <ddsx2dds> <plugin>...
"""
import os
import struct
import sys

import texfiles as tf

# (name, format, width, height, mips): the PC formats whose DDSx keeps the source's data as it is, large enough to be
# packed (over 512 bytes)
CASES = [('argb', 'argb', 16, 8, 5), ('argb4444', 'argb4444', 32, 16, 1), ('rgb565', 'rgb565', 32, 16, 2),
         ('r8', 'r8', 32, 32, 1), ('dxt1', 'dxt1', 64, 64, 5), ('dxt5', 'dxt5', 32, 32, 3)]
PACKING = {'none': ['-pack-'], 'zlib': ['-pack:zlib'], 'zstd': ['-pack:zstd'], '7zip': ['-pack:7zip', '-packThres:0']}


def make_ddsx(out, ddsxcvt, name, fmt, w, h, mips, packing='none', opts=()):
  src = os.path.join(out, name + '.dds')
  tf.write_dds(src, fmt, w, h, mips, tf.pattern(sum(tf.mip_sizes(fmt, w, h, mips)), len(name)))
  ddsx = os.path.join(out, '{}.{}.ddsx'.format(name, packing))
  tf.run([ddsxcvt, '-q'] + PACKING[packing] + list(opts) + ['PC', src, ddsx], out)
  tf.check(tf.read_ddsx(ddsx).flags & tf.FLG_COMPR_MASK or packing == 'none', '{} was not packed'.format(ddsx))
  return src, ddsx


def check_dds(path, src):
  """A DDS converted back against its source DDS: the same texture, format and data."""
  dds, ref = tf.read_dds(path), tf.read_dds(src)
  tf.check((dds.w, dds.h, dds.mips, tf.dds_format(dds)) == (ref.w, ref.h, ref.mips, tf.dds_format(ref)),
           '{}: {} {}x{} with {} mips, expected {} {}x{} with {}'.format(
             path, tf.dds_format(dds), dds.w, dds.h, dds.mips, tf.dds_format(ref), ref.w, ref.h, ref.mips))
  tf.check(dds.data == ref.data, '{}: the data differs from the source texture'.format(path))


def roundtrip(out, ddsxcvt, ddsx2dds, *plugins):
  for packing in PACKING:
    for name, fmt, w, h, mips in CASES:
      src, ddsx = make_ddsx(out, ddsxcvt, name, fmt, w, h, mips, packing)
      dds = ddsx[:-1]  # <name>.<packing>.dds
      tf.run([ddsx2dds, ddsx, dds], out)
      check_dds(dds, src)


def dump(out, ddsxcvt, ddsx2dds, *plugins):
  _, ddsx = make_ddsx(out, ddsxcvt, 'dxt5', 'dxt5', 32, 32, 3, 'zlib', ['-addru:clamp', '-addrv:mirror'])
  log = tf.run([ddsx2dds, ddsx, '-dump'], out)
  for line in ('D3D fmt 0x35545844 (DXT5)  bpp=8 code=4', 'mem sz  1344,', 'tex2D   32x32', 'mips    3',
               'addr    clamp, mirror', 'flags   REV_MIP_ORDER', 'compr   ZLIB',
               'mip  2:    8x8        32 (pitch) *    2 (lines) =       64',
               'mip  0:   32x32      128 (pitch) *    8 (lines) =     1024'):
    tf.check(line in log, 'the dump has no "{}"'.format(line))


def check(out, ddsxcvt, ddsx2dds, *plugins):
  # -check:<compression> prints the name and exits with 0 when the DDSx is packed so (scripts find textures to repack)
  ddsx = {p: make_ddsx(out, ddsxcvt, 'argb', 'argb', 16, 8, 5, p)[1] for p in ('none', 'zlib', 'zstd')}
  for packing, path in ddsx.items():
    for method in ('NONE', 'ZLIB', 'ZSTD', '7ZIP'):
      log = tf.run([ddsx2dds, path, '-check:' + method], out, code=0 if method.lower() == packing else None)
      printed = path.replace('\\', '/') in log.replace('\\', '/')
      tf.check(printed == (method.lower() == packing), '-check:{} of a {} DDSx printed "{}"'.format(
        method, packing, log.strip()))
  tf.run([ddsx2dds, ddsx['none'], '-check:FOO'], out, code=None)


def bundle(out, ddsxcvt, ddsx2dds, *plugins):
  # a GUI atlas bundle (guiTex -mkbundle) is its coordinates BLK in a 'TA.' block followed by the atlas DDSx; without
  # an output name the DDS is <name>.dds next to it
  src, ddsx = make_ddsx(out, ddsxcvt, 'argb', 'argb', 16, 8, 5, 'zlib')
  with open(ddsx, 'rb') as f:
    data = f.read()
  coords = b'(the atlas coordinates)'.ljust(32, b'\0')
  with open(os.path.join(out, 'atlas.ta.bin'), 'wb') as f:
    f.write(b'\0TA.' + struct.pack('<i', len(coords)) + coords + data)
  tf.run([ddsx2dds, os.path.join(out, 'atlas.ta.bin')], out)
  check_dds(os.path.join(out, 'atlas.dds'), src)


def astc(out, ddsxcvt, ddsx2dds, *plugins):
  # -decodeASTC writes each mip of an ASTC DDSx (the iOS textures) as a TGA, decoded by the astcenc next to ddsx2dds;
  # the mips are encoded by that astcenc too, as ddsConverter does
  astcenc = tf.astcenc(ddsx2dds)
  mips, blocks = [], b''
  for level, side in enumerate((32, 16)):
    pix = b''.join(bytes((x * 255 // (side - 1), y * 255 // (side - 1), 128, 255)) for y in range(side)
                   for x in range(side))
    tga, packed = (os.path.join(out, 'mip{}.{}'.format(level, ext)) for ext in ('tga', 'astc'))
    tf.write_tga(tga, side, side, pix)
    tf.run([astcenc, '-cl', tga, packed, '4x4', '-medium'], out)
    with open(packed, 'rb') as f:
      blocks += f.read()[16:]  # (after the header of the .astc file)
    mips.append((side, pix))
  src, ddsx = (os.path.join(out, 'astc.' + ext) for ext in ('dds', 'ddsx'))
  tf.write_dds(src, 'astc4', 32, 32, 2, blocks)
  tf.run([ddsxcvt, '-q', 'iOS', src, ddsx], out)
  tf.run([ddsx2dds, ddsx, '-decodeASTC'], out)
  for level, (side, pix) in enumerate(mips):
    tga = '{}_mip{}.tga'.format(ddsx, level)
    tf.check(os.path.exists(tga), '{} was not written'.format(tga))
    w, h, decoded = tf.read_tga(tga)
    tf.check((w, h) == (side, side), '{} is {}x{}, expected {}x{}'.format(tga, w, h, side, side))
    tf.check_close('mip {}'.format(level), decoded, pix, 8, 2)


def invalid(out, ddsxcvt, ddsx2dds, *plugins):
  # it must fail, and in time, on whatever it is given
  broken = {'missing': None, 'not_ddsx': b'DDS not a DDSx file'}
  for packing in ('none', 'zlib', '7zip'):
    with open(make_ddsx(out, ddsxcvt, 'argb', 'argb', 64, 64, 1, packing)[1], 'rb') as f:
      data = f.read()
    broken['truncated_' + packing] = data[:32 + (len(data) - 32) // 2]  # the header and half of the data
  for name, data in broken.items():
    path = os.path.join(out, name + '.ddsx')
    if data is not None:
      with open(path, 'wb') as f:
        f.write(data)
    tf.run([ddsx2dds, path, os.path.join(out, name + '.dds')], out, code=None, timeout=20)


if __name__ == '__main__':
  sys.exit(tf.main({'roundtrip': roundtrip, 'dump': dump, 'check': check, 'bundle': bundle, 'astc': astc,
                    'invalid': invalid}))
