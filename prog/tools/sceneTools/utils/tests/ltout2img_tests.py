"""Tests of ltout2img (CTest: ltout2img.<scenario>): a lightmapper output (LTo3, the format ltout2img.cpp reads; nothing
in the engine writes it any more) written here, converted to each image format and read back by the format's own rules.

python ltout2img_tests.py <scenario> <ltout2img>
"""
import math
import os
import struct
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'converters', 'ddsx2dds',
                                'tests'))
import texfiles as tf  # noqa: E402

# 8x3 lightmap texels and 5 vertex lights (stored as one more row, padded with black); eighths are exact in float32,
# so their 8-bit values are too; above 1 is clamped in the TGA
W, H = 8, 3
TEXELS = [((x + 1) / 8, (y + 1) / 4, (x * y) / 8 + (x == 7) * 1.5) for y in range(H) for x in range(W)]
VLIGHTS = [(0.5, 0.25, 0.125), (2.0, 0.0, 1.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0), (0.375, 0.625, 0.875)]
DONE = [(x + y) % 3 != 0 for y in range(H) for x in range(W)]  # the texels the lightmapper computed
EFF_H = H + (len(VLIGHTS) + W - 1) // W
PIXELS = TEXELS + VLIGHTS + [(0.0, 0.0, 0.0)] * (W * EFF_H - W * H - len(VLIGHTS))


def write_ltoutput(path, label=b'LTo3'):
  def bits(flags):  # a Bitarray: 32-bit words
    words = [0] * ((len(flags) + 31) // 32)
    for i, f in enumerate(flags):
      words[i // 32] |= f << (i % 32)
    return struct.pack('<{}I'.format(len(words)), *words)
  # label, the lightmap's UUID, the pass it was made after, the size, the vertex lights; the colors; a tagged block
  # with the done and internal texel bits
  data = label + bytes(range(16)) + struct.pack('<4i', 3, W, H, len(VLIGHTS))
  data += b''.join(struct.pack('<3f', *c) for c in TEXELS + VLIGHTS)
  lbit = b'Lbit' + bits(DONE) + bits([False] * len(DONE))
  with open(path, 'wb') as f:
    f.write(data + struct.pack('<i', len(lbit)) + lbit)


def convert(out, ltout2img, ext):
  src = os.path.join(out, 'lightmap.LToutput.dat')
  write_ltoutput(src)
  dst = os.path.join(out, 'lightmap.' + ext)
  log = tf.run([ltout2img, src, dst], out)
  tf.check('size {}x{}'.format(W, H) in log, 'no size reported')
  return dst


def tga(out, ltout2img):
  # 32-bit: the colors clamped to 0..1, alpha 255 for the texels done and the vertex lights, the padding transparent
  w, h, pix = tf.read_tga(convert(out, ltout2img, 'tga'))
  tf.check((w, h) == (W, EFF_H), 'the TGA is {}x{}, expected {}x{}'.format(w, h, W, EFF_H))
  for i, c in enumerate(PIXELS):
    a = (255 if DONE[i] else 0) if i < W * H else 255 if i < W * H + len(VLIGHTS) else 0
    expected = bytes(int(min(max(v, 0.0), 1.0) * 255) for v in reversed(c)) + bytes((a, ))
    tf.check(pix[i * 4:i * 4 + 4] == expected, 'pixel {}: {} (BGRA), expected {}'.format(
      i, pix[i * 4:i * 4 + 4].hex(), expected.hex()))


def pfm(out, ltout2img):
  # Portable float map: "PF", the size, a negative scale for little endian, then the RGB floats, the rows bottom to top
  with open(convert(out, ltout2img, 'pfm'), 'rb') as f:
    d = f.read()
  header = 'PF\n{} {}\n-1.0\n'.format(W, EFF_H).encode()
  tf.check(d.startswith(header), 'PFM header {!r}, expected {!r}'.format(d[:len(header)], header))
  rows = [PIXELS[y * W:(y + 1) * W] for y in range(EFF_H)]
  expected = b''.join(struct.pack('<3f', *c) for row in reversed(rows) for c in row)
  tf.check(d[len(header):] == expected, 'the PFM pixels differ{}'.format(
    ' (its rows are top to bottom)' if d[len(header):] == b''.join(struct.pack('<3f', *c) for c in PIXELS) else ''))


def read_rgbe(d):
  """(w, h, [(r, g, b)] rows top to bottom) of a Radiance HDR with -Y h +X w scanlines, flat or run-length encoded."""
  header, _, rest = d.partition(b'\n\n')
  tf.check(header.startswith(b'#?') and b'FORMAT=32-bit_rle_rgbe' in header, 'not a Radiance RGBE file')
  res, _, data = rest.partition(b'\n')
  m = res.split()
  tf.check(len(m) == 4 and m[0] == b'-Y' and m[2] == b'+X', 'resolution {!r}'.format(res))
  h, w = int(m[1]), int(m[3])
  pos, rgbe = 0, []
  for _ in range(h):
    if 8 <= w < 0x8000 and data[pos:pos + 2] == b'\2\2':  # four planes, each of runs and dumps
      tf.check(data[pos + 2] << 8 | data[pos + 3] == w, 'bad scanline width')
      pos += 4
      planes = []
      for _ in range(4):
        plane = bytearray()
        while len(plane) < w:
          n = data[pos]
          if n > 128:
            plane += bytes((data[pos + 1], )) * (n - 128)
            pos += 2
          else:
            plane += data[pos + 1:pos + 1 + n]
            pos += 1 + n
        planes.append(plane)
      rgbe += zip(*planes)
    else:
      rgbe += [tuple(data[pos + i * 4:pos + i * 4 + 4]) for i in range(w)]
      pos += 4 * w
  tf.check(pos == len(data), '{} bytes after the scanlines'.format(len(data) - pos))
  return w, h, [tuple(v * math.ldexp(1, e - 136) if e else 0.0 for v in (r, g, b)) for r, g, b, e in rgbe]


def hdr(out, ltout2img):
  # Radiance RGBE: the colors as they are, to the 8-bit mantissa shared by a pixel's channels
  with open(convert(out, ltout2img, 'hdr'), 'rb') as f:
    w, h, pix = read_rgbe(f.read())
  tf.check((w, h) == (W, EFF_H), 'the HDR is {}x{}, expected {}x{}'.format(w, h, W, EFF_H))
  for i, (got, c) in enumerate(zip(pix, PIXELS)):
    tf.check(all(abs(g - v) <= max(c) / 128 for g, v in zip(got, c)), 'pixel {}: {}, expected {}'.format(i, got, c))


def errors(out, ltout2img):
  # not a lightmapper output, or none: it must fail
  src = os.path.join(out, 'other.LToutput.dat')
  write_ltoutput(src, label=b'LTo2')
  tf.run([ltout2img, src, os.path.join(out, 'other.tga')], out, code=None)
  tf.run([ltout2img, os.path.join(out, 'missing.LToutput.dat')], out, code=None)


if __name__ == '__main__':
  sys.exit(tf.main({'tga': tga, 'pfm': pfm, 'hdr': hdr, 'errors': errors}))
