"""Tests of ddsxCvt (CTest: ddsxCvt.<scenario>): DDS textures of the formats the CDK writes, converted to the DDSx of
each platform by its plugin (plugins/ddsx next to ddsxCvt), read back here and compared with their source.

python ddsxCvt_tests.py <scenario> <ddsxCvt> <plugin>...
"""
import os
import struct
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'ddsx2dds', 'tests'))
import texfiles as tf  # noqa: E402

# (name, format, width, height, mips)
CASES = [('argb', 'argb', 16, 8, 5), ('argb4444', 'argb4444', 8, 8, 1), ('rgba4444', 'rgba4444', 8, 8, 1),
         ('rgba5551', 'rgba5551', 8, 4, 1), ('rgb565', 'rgb565', 8, 4, 2), ('r8', 'r8', 16, 4, 1),
         ('dxt1', 'dxt1', 16, 16, 5), ('dxt5', 'dxt5', 16, 16, 3), ('astc4', 'astc4', 16, 16, 5),
         ('astc8', 'astc8', 32, 32, 6)]
# the block formats' dxtShift (ASTC: the mobile block size codes)
DXT_SHIFT = {'dxt1': 3, 'dxt5': 4, 'astc4': 5, 'astc8': 6}


def write_cases(out):
  for name, fmt, w, h, mips in CASES:
    data = tf.pattern(sum(tf.mip_sizes(fmt, w, h, mips)), len(name))
    tf.write_dds(os.path.join(out, name + '.dds'), fmt, w, h, mips, data)


def swizzle16(data, fn):
  return b''.join(struct.pack('<H', fn(v)) for v, in struct.iter_unpack('<H', data))


# what each platform's plugin stores for a source format: (D3DFMT, the conversion of a surface's data)
PC = {'argb': ('argb', None), 'argb4444': ('argb4444', None),
      'rgba4444': ('argb4444', lambda d: swizzle16(d, lambda v: (v & 0xF) << 12 | v >> 4)),
      'rgba5551': ('a1r5g5b5', lambda d: swizzle16(d, lambda v: (v & 1) << 15 | v >> 1)), 'rgb565': ('rgb565', None),
      'r8': ('l8', None), 'dxt1': ('dxt1', None), 'dxt5': ('dxt5', None), 'astc4': ('astc4', None),
      'astc8': ('astc8', None)}
# the mobile GPUs read 16-bit formats with the alpha in the low bits: RGBA4444 and RGBA5551 are kept, ARGB4444 swizzled
MOBILE = dict(PC, rgba4444=('argb4444', None), rgba5551=('a1r5g5b5', None),
              argb4444=('r4g4b4a4', lambda d: swizzle16(d, lambda v: v >> 12 | (v & 0xFFF) << 4)))


def check_ddsx(ddsx, src, fmt, w, h, mips, expected):
  """A DDSx against its source DDS data: the header, and its surfaces converted, the smallest mip first (as the
  plugins store them by default, for partial reading)."""
  d3d, convert = expected[fmt]
  tf.check((ddsx.d3d_format, ddsx.w, ddsx.h, ddsx.levels) == (tf.D3DFMT[d3d], w, h, mips),
           'format {:#x} {}x{} with {} mips, expected {} ({:#x}) {}x{} with {}'.format(
             ddsx.d3d_format, ddsx.w, ddsx.h, ddsx.levels, d3d, tf.D3DFMT[d3d], w, h, mips))
  if fmt in DXT_SHIFT:
    tf.check(ddsx.dxt_shift == DXT_SHIFT[fmt], 'dxtShift {} for {}'.format(ddsx.dxt_shift, fmt))
  else:
    tf.check(ddsx.bpp == tf.FORMATS[fmt][0], '{} bits per pixel for {}'.format(ddsx.bpp, fmt))
  tf.check(bool(ddsx.flags & tf.FLG_REV_MIP_ORDER) == (mips > 1), 'flags {:08X}: REV_MIP_ORDER expected only with mips'
           .format(ddsx.flags))
  tf.check(bool(ddsx.flags & tf.FLG_MOBILE_TEXFMT) == fmt.startswith('astc'),
           'flags {:08X}: MOBILE_TEXFMT expected only for ASTC'.format(ddsx.flags))
  surfaces = list(tf.chunks(src, tf.mip_sizes(fmt, w, h, mips)))
  if mips > 1:
    surfaces.reverse()
  expected_data = b''.join(convert(s) if convert else s for s in surfaces)
  tf.check(ddsx.data == expected_data, 'the DDSx data differs from its source' + (' converted' if convert else ''))


def check_plugins(ddsxcvt, plugins):
  # ddsxCvt loads the plugins from plugins/ddsx next to it
  plugin_dir = os.path.join(os.path.dirname(ddsxcvt), 'plugins', 'ddsx')
  for p in plugins:
    tf.check(os.path.normcase(os.path.dirname(p)) == os.path.normcase(plugin_dir),
             '{} is not in {}'.format(p, plugin_dir))


def convert_cases(out, ddsxcvt, plugins, target, expected, rejected=()):
  check_plugins(ddsxcvt, plugins)
  write_cases(out)
  for name, fmt, w, h, mips in CASES:
    src = os.path.join(out, name + '.dds')
    dst = os.path.join(out, '{}.{}.ddsx'.format(name, target))
    if fmt in rejected:
      log = tf.run([ddsxcvt, '-pack-', target, src, dst], out, code=1)
      tf.check('Cannot transcode' in log, '{} for {}: no reason given'.format(fmt, target))
      tf.check(not os.path.exists(dst), '{} was written for a rejected texture'.format(dst))
      continue
    tf.run([ddsxcvt, '-q', '-pack-', target, src, dst], out)
    check_ddsx(tf.read_ddsx(dst), tf.read_dds(src).data, fmt, w, h, mips, expected)


def pc(out, ddsxcvt, *plugins):
  convert_cases(out, ddsxcvt, plugins, 'PC', PC)
  # without an output name it is written next to the source; -ddsSuffix takes the addressing and the quality mips from
  # the name's suffix (ddsConverter -suffix:) and drops it: @Acm_Q012 is clamp U, mirror V, medium quality from mip 1,
  # low from mip 2
  src = os.path.join(out, 'suffixed@Acm_Q012.dds')
  tf.write_dds(src, 'argb', 16, 16, 5, tf.pattern(sum(tf.mip_sizes('argb', 16, 16, 5)), 1))
  tf.run([ddsxcvt, '-q', '-pack-', '-ddsSuffix', 'PC', src], out)
  ddsx = tf.read_ddsx(os.path.join(out, 'suffixed.ddsx'))
  tf.check(ddsx.flags & 0xFF == 0x23, 'addressing {:02X}, expected 23 (U clamp, V mirror)'.format(ddsx.flags & 0xFF))
  tf.check((ddsx.mq_mip, ddsx.lq_mip) == (1, 2), 'quality mips (medium {}, low {}), expected (1, 2)'.format(
    ddsx.mq_mip, ddsx.lq_mip))


def mobile(out, ddsxcvt, *plugins):
  # iOS has no DXT (BC) formats: those textures must be ASTC
  convert_cases(out, ddsxcvt, plugins, 'iOS', MOBILE, rejected=('dxt1', 'dxt5'))
  convert_cases(out, ddsxcvt, plugins, 'and', MOBILE)


def packing(out, ddsxcvt, *plugins):
  w = h = 64
  sizes = tf.mip_sizes('argb', w, h, 7)
  data = tf.pattern(sum(sizes), 3)
  src = os.path.join(out, 'packed.dds')
  tf.write_dds(src, 'argb', w, h, 7, data)

  def convert(name, opts, compression):
    dst = os.path.join(out, name + '.ddsx')
    tf.run([ddsxcvt, '-q'] + opts + ['PC', src, dst], out)
    ddsx = tf.read_ddsx(dst)
    tf.check(ddsx.flags & tf.FLG_COMPR_MASK == compression, '{}: compression flags {:08X}, expected {:08X}'.format(
      ' '.join(opts) or 'default', ddsx.flags & tf.FLG_COMPR_MASK, compression))
    if compression:
      tf.check(0 < ddsx.packed_sz < ddsx.mem_sz, '{}: packed {} of {} bytes'.format(name, ddsx.packed_sz, ddsx.mem_sz))
    if ddsx.data is not None:  # (zstd is read back by ddsx2dds.roundtrip)
      check_ddsx(ddsx, data, 'argb', w, h, 7, PC)

  convert('default', [], tf.FLG_ZLIB)
  convert('none', ['-pack-'], 0)
  convert('7zip', ['-pack:7zip', '-packThres:0'], tf.FLG_7ZIP)
  convert('zstd', ['-pack:zstd'], tf.FLG_ZSTD)
  # 7zip only for DDSx larger than the threshold (256K by default)
  convert('7zip_below_threshold', ['-pack:7zip'], tf.FLG_ZLIB)
  convert('7zip_below_given_threshold', ['-pack:7zip', '-packThres:{}'.format(1 << 20)], tf.FLG_ZLIB)
  convert('7zip_above_given_threshold', ['-pack:7zip', '-packThres:1024'], tf.FLG_7ZIP)


def errors(out, ddsxcvt, *plugins):
  src = os.path.join(out, 'good.dds')
  tf.write_dds(src, 'argb', 4, 4, 1, bytes(64))
  not_dds = os.path.join(out, 'not_a.dds')
  with open(not_dds, 'w') as f:
    f.write('not a DDS file\n')
  for args in (['PC', os.path.join(out, 'missing.dds')], ['PC', not_dds], ['XYZ', src], ['-unknownOption', 'PC', src]):
    dst = os.path.join(out, 'failed.ddsx')
    tf.run([ddsxcvt] + args + [dst], out, code=1)
    tf.check(not os.path.exists(dst), '{} was left behind by a failed conversion'.format(dst))


if __name__ == '__main__':
  sys.exit(tf.main({'pc': pc, 'mobile': mobile, 'packing': packing, 'errors': errors}))
