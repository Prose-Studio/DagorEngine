"""Tests of ddsConverter (CTest: ddsConverter.<scenario>): images (a PNG icon of the CDK, TGAs written here) converted
to DDS in each format, the pixels read back here (decoding the DXT blocks here, the ASTC ones with the astcenc
ddsConverter runs) and compared with the source's.

python ddsConverter_tests.py <scenario> <ddsConverter>
"""
import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'ddsx2dds', 'tests'))
import texfiles as tf  # noqa: E402

ICON = os.path.join(HERE, '..', '..', '..', 'toolsData', 'dagor_cdk', 'commonData', 'icons', 'play.png')


def test_image(w, h, alpha):
  """BGRA of a TGA with smooth, unlike channels (so swapped or misplaced ones are found)."""
  return b''.join(bytes((255 - 4 * (x + y), y * 255 // (h - 1), x * 255 // (w - 1), (x + y) * 255 // (w + h - 2)
                         if alpha else 255)) for y in range(h) for x in range(w))


def rgb565(c):
  return ((c >> 11) * 255 // 31, (c >> 5 & 63) * 255 // 63, (c & 31) * 255 // 31)


def decode_dxt(fmt, w, h, data):
  """BGRA of the first surface of a DXT1 or DXT5 texture."""
  out = bytearray(w * h * 4)
  size = 8 if fmt == 'dxt1' else 16
  for i in range((w // 4) * (h // 4)):
    blk = data[i * size:(i + 1) * size]
    alpha = [255] * 16
    if fmt == 'dxt5':
      a0, a1, bits = blk[0], blk[1], int.from_bytes(blk[2:8], 'little')
      pal = [a0, a1] + ([((6 - k) * a0 + (k + 1) * a1) // 7 for k in range(6)] if a0 > a1 else
                        [((4 - k) * a0 + (k + 1) * a1) // 5 for k in range(4)] + [0, 255])
      alpha = [pal[bits >> (3 * k) & 7] for k in range(16)]
      blk = blk[8:]
    c0, c1, bits = struct.unpack('<HHI', blk)
    p0, p1 = rgb565(c0), rgb565(c1)
    if c0 > c1 or fmt == 'dxt5':
      pal = [p0, p1, tuple((2 * a + b) // 3 for a, b in zip(p0, p1)), tuple((a + 2 * b) // 3 for a, b in zip(p0, p1))]
    else:
      pal = [p0, p1, tuple((a + b) // 2 for a, b in zip(p0, p1)), (0, 0, 0)]
    bx, by = i % (w // 4) * 4, i // (w // 4) * 4
    for k in range(16):
      r, g, b = pal[bits >> (2 * k) & 3]
      a = alpha[k] if fmt == 'dxt5' else (0 if c0 <= c1 and bits >> (2 * k) & 3 == 3 else 255)
      o = ((by + k // 4) * w + bx + k % 4) * 4
      out[o:o + 4] = bytes((b, g, r, a))
  return bytes(out)


def convert(tool, out, src, *opts):
  """Converts a copy of src in out (ddsConverter writes next to its source) and reads the DDS back."""
  name = os.path.splitext(os.path.basename(src))[0]
  copy = os.path.join(out, os.path.basename(src))
  if not os.path.exists(copy):
    shutil.copyfile(src, copy)
  suffix = '-'.join(o.split(':')[1] for o in opts) or 'default'
  tf.run([tool, copy, '-suffix:' + suffix] + list(opts), out)
  return tf.read_dds(os.path.join(out, '{}@{}.dds'.format(name, suffix)))


def check_layout(dds, fmt, w, h, mips):
  tf.check((tf.dds_format(dds), dds.w, dds.h, dds.mips) == (fmt, w, h, mips), '{} {}x{} with {} mips, expected {} '
           '{}x{} with {}'.format(tf.dds_format(dds), dds.w, dds.h, dds.mips, fmt, w, h, mips))
  tf.check(len(dds.data) == sum(tf.mip_sizes(fmt, w, h, mips)), '{} bytes of data for {} {}x{} with {} mips'.format(
    len(dds.data), fmt, w, h, mips))


def argb(out, tool):
  w, h, src = tf.read_png(ICON)
  dds = convert(tool, out, ICON, '-format:fmtARGB', '-mipmapType:mipmapNone')
  check_layout(dds, 'argb', w, h, 1)
  tf.check(dds.data == src, 'the pixels differ from the PNG')
  # the mips down to 1x1, the top one the image as it is
  dds = convert(tool, out, ICON, '-format:fmtARGB', '-mipmapType:mipmapGenerate')
  check_layout(dds, 'argb', w, h, w.bit_length())
  tf.check(dds.data[:len(src)] == src, 'the top mip differs from the PNG')


def dxt(out, tool):
  w, h = 32, 32
  for alpha in (False, True):
    src = test_image(w, h, alpha)
    tga = os.path.join(out, 'alpha.tga' if alpha else 'opaque.tga')
    tf.write_tga(tga, w, h, src)
    # a TGA with alpha is DXT5 by default, mips are generated for DXT; the encoder's choices differ with the compiler
    # (MSVC's at most 17 off, GCC's 25 here): a swapped channel or a misplaced block is far more
    fmt, opts = ('dxt5', ['-format:fmtDXT5']) if alpha else ('dxt1', ['-format:fmtDXT1'])
    for dds in (convert(tool, out, tga, *opts), convert(tool, out, tga) if alpha else None):
      if dds:
        check_layout(dds, fmt, w, h, 6)
        tf.check_close(fmt, decode_dxt(fmt, w, h, dds.data), src, 48, 8)


def astc(out, tool):
  # the mobile formats, encoded by the astcenc ddsConverter runs from its dir, decoded here by it again
  w, h = 32, 32
  src = test_image(w, h, True)
  tga = os.path.join(out, 'image.tga')
  tf.write_tga(tga, w, h, src)
  # (measured: 4x4 at most 10 off, 2.2 on average; 8x8, 2 bits per texel, 19 and 4.2)
  for opt, fmt, max_err, mean_err in (('fmtASTC4', 'astc4', 24, 4), ('fmtASTC8', 'astc8', 40, 8)):
    dds = convert(tool, out, tga, '-format:' + opt)
    check_layout(dds, fmt, w, h, 1)
    tf.check_close(fmt, tf.decode_astc(tf.astcenc(tool), out, fmt, fmt, w, h, dds.data), src, max_err, mean_err)


def formats(out, tool):
  w, h = 16, 8
  src = test_image(w, h, True)
  tga = os.path.join(out, 'image.tga')
  tf.write_tga(tga, w, h, src)
  pixels = [src[i:i + 4] for i in range(0, len(src), 4)]  # BGRA
  # the channels of each format (bits, shift) as BGRA; each value within a step of the source's
  layouts = {'fmt4444': ('rgba4444', ((4, 4), (4, 8), (4, 12), (4, 0))),
             'fmt5551': ('rgba5551', ((5, 1), (5, 6), (5, 11), (1, 0))),
             'fmt565': ('rgb565', ((5, 0), (6, 5), (5, 11), None))}
  for opt, (fmt, channels) in layouts.items():
    dds = convert(tool, out, tga, '-format:' + opt)
    check_layout(dds, fmt, w, h, 1)
    for i, (v, ) in enumerate(struct.iter_unpack('<H', dds.data)):
      for c, ch in enumerate(channels):
        if ch:
          bits, shift = ch
          top = (1 << bits) - 1
          got = (v >> shift & top) * 255 // top
          tf.check(abs(got - pixels[i][c]) <= (255 // top + 1 if bits > 1 else 128), '{}: pixel {} channel {} is {}, '
                   'in the source {}'.format(opt, i, 'BGRA'[c], got, pixels[i][c]))
  # the 8-bit formats keep the red (luminance) channel and alpha as they are: R8 one byte, A8R8 two (R low, A high)
  dds = convert(tool, out, tga, '-format:fmtR8')
  check_layout(dds, 'r8', w, h, 1)
  tf.check(dds.data == bytes(p[2] for p in pixels), 'fmtR8: the pixels differ from the source\'s red')
  dds = convert(tool, out, tga, '-format:fmtA8R8')
  tf.check((dds.bits, dds.masks) == (16, (0xff, 0, 0, 0xff00)), 'fmtA8R8: {} bits with masks (R, G, B, A) {}, '
           'expected 16 with R 0xff and A 0xff00 (the DDSx plugins read that as D3DFMT_A8L8)'.format(
             dds.bits, ', '.join(hex(m) for m in dds.masks)))
  tf.check(dds.data == bytes(c for p in pixels for c in (p[2], p[3])), 'fmtA8R8: the pixels differ from the source')


def errors(out, tool):
  tga = os.path.join(out, 'image.tga')
  tf.write_tga(tga, 4, 4, bytes(64))
  not_image = os.path.join(out, 'not_an_image.png')
  with open(not_image, 'w') as f:
    f.write('not an image\n')
  for args in ([os.path.join(out, 'missing.tga')], [not_image], [tga, 'notAnOption'], [tga, '-format:fmtNone'],
               [tga, '-type:typeVolume']):  # (a volume needs -depth:)
    tf.run([tool] + args, out, code=1)


if __name__ == '__main__':
  sys.exit(tf.main({'argb': argb, 'dxt': dxt, 'astc': astc, 'formats': formats, 'errors': errors}))
