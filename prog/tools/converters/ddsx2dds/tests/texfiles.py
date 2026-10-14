"""The image files of the CDK's texture and font tools (DDS, DDSx, TGA, PNG) for their tests: readers and writers
written from the formats themselves (DDSURFACEDESC2, ddsx::Header of engine/sharedInclude/3d/ddsxTex.h, Truevision
TGA, PNG), and what the tests share: running a tool and failing with a message.

The tests are scripts run by CTest (python <script> <scenario> <program>...): they write into DAGOR_TEST_OUT (the test's
dir under <build>/test-artifacts, which CI keeps when a test fails) and run the tools there, since the tools write
their logs into the working dir.
"""
import collections
import lzma
import os
import shutil
import struct
import subprocess
import sys
import zlib


class Failure(Exception):
  pass


def check(cond, msg):
  if not cond:
    raise Failure(msg)


def check_close(what, got, expected, max_err, mean_err):
  """Images (or any values) alike within an error: the largest one and the mean."""
  errs = [abs(a - b) for a, b in zip(got, expected)]
  worst, mean = max(errs), sum(errs) / len(errs)
  print('{}: max error {}, mean {:.2f}'.format(what, worst, mean))
  check(worst <= max_err and mean <= mean_err, '{}: max error {} (at most {}), mean {:.2f} (at most {})'.format(
    what, worst, max_err, mean, mean_err))


def run(cmd, cwd, code=0, timeout=60):
  """Runs a tool in cwd and returns its output; fails unless it exits with code (None: with any code but 0)."""
  cmd = [str(c) for c in cmd]
  print('>', ' '.join(cmd), flush=True)
  try:
    p = subprocess.run(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=timeout)
  except subprocess.TimeoutExpired:
    raise Failure('{} did not finish in {} s'.format(os.path.basename(cmd[0]), timeout))
  out = p.stdout.decode('utf-8', 'replace')
  print(out, flush=True)
  if code is None:
    check(p.returncode != 0, '{} exited with 0 (expected a failure)'.format(os.path.basename(cmd[0])))
  else:
    check(p.returncode == code, '{} exited with {} (expected {})'.format(os.path.basename(cmd[0]), p.returncode, code))
  return out


def main(scenarios):
  """The scripts' entry point: python <script> <scenario> <program>...; runs scenarios[<scenario>](out, *programs) in
  an empty DAGOR_TEST_OUT."""
  if len(sys.argv) < 2 or sys.argv[1] not in scenarios:
    print('usage: {} {{{}}} <program>...'.format(sys.argv[0], '|'.join(scenarios)), file=sys.stderr)
    return 2
  out = os.environ.get('DAGOR_TEST_OUT')
  if not out:
    print('DAGOR_TEST_OUT is not set (the tests run through CTest)', file=sys.stderr)
    return 2
  shutil.rmtree(out, ignore_errors=True)
  os.makedirs(out)
  try:
    scenarios[sys.argv[1]](os.path.abspath(out), *[os.path.abspath(p) for p in sys.argv[2:]])
  except Failure as e:
    print('FAILED:', e, file=sys.stderr)
    return 1
  print('passed')
  return 0


# DDS: magic, DDSURFACEDESC2 (124 bytes, DDPIXELFORMAT at 72), then the surfaces (each face's mip chain, largest first)
DDSD_CAPS, DDSD_HEIGHT, DDSD_WIDTH, DDSD_PIXELFORMAT, DDSD_MIPMAPCOUNT = 0x1, 0x2, 0x4, 0x1000, 0x20000
DDPF_ALPHAPIXELS, DDPF_FOURCC, DDPF_RGB = 0x1, 0x4, 0x40
DDSCAPS_COMPLEX, DDSCAPS_TEXTURE, DDSCAPS_MIPMAP = 0x8, 0x1000, 0x400000

# the pixel formats the tests write: (bits, R, G, B, A masks) or a FourCC
FORMATS = {
  'argb': (32, 0xff0000, 0xff00, 0xff, 0xff000000),
  'argb4444': (16, 0x0f00, 0x00f0, 0x000f, 0xf000),  # D3DFMT_A4R4G4B4
  'rgba4444': (16, 0xf000, 0x0f00, 0x00f0, 0x000f),  # ddsConverter's fmt4444
  'rgba5551': (16, 0xf800, 0x07c0, 0x003e, 0x0001),  # ddsConverter's fmt5551
  'rgb565': (16, 0xf800, 0x07e0, 0x001f, 0),
  'r8': (8, 0xff, 0, 0, 0),  # ddsConverter's fmtR8 (the plugins read it as D3DFMT_L8)
  'dxt1': b'DXT1',
  'dxt5': b'DXT5',
  'astc4': b'AST4',  # ASTC 4x4 and 8x8 blocks (ddsConverter's fmtASTC4, fmtASTC8)
  'astc8': b'AST8',
}
BLOCKS = {'dxt1': (4, 8), 'dxt5': (4, 16), 'astc4': (4, 16), 'astc8': (8, 16)}  # block size, bytes per block

Dds = collections.namedtuple('Dds', 'w h mips flags pf_flags fourcc bits masks caps data')


def surface_size(fmt, w, h):
  if fmt in BLOCKS:
    side, size = BLOCKS[fmt]
    return (w + side - 1) // side * ((h + side - 1) // side) * size
  return w * h * FORMATS[fmt][0] // 8


def mip_sizes(fmt, w, h, mips):
  return [surface_size(fmt, max(w >> i, 1), max(h >> i, 1)) for i in range(mips)]


def pattern(n, seed):
  """Texture data: no two 8-byte runs alike within 2K (so surfaces in the wrong place are found), and packable."""
  return bytes(((i >> 3) + seed * 17) & 0xFF for i in range(n))


def write_dds(path, fmt, w, h, mips, data):
  """A 2D texture of FORMATS[fmt] with its mip chain in data."""
  check(len(data) == sum(mip_sizes(fmt, w, h, mips)), 'bad data size for {} {}x{} with {} mips'.format(fmt, w, h, mips))
  flags = DDSD_CAPS | DDSD_HEIGHT | DDSD_WIDTH | DDSD_PIXELFORMAT | (DDSD_MIPMAPCOUNT if mips > 1 else 0)
  caps = DDSCAPS_TEXTURE | (DDSCAPS_COMPLEX | DDSCAPS_MIPMAP if mips > 1 else 0)
  f = FORMATS[fmt]
  if isinstance(f, bytes):
    pf = struct.pack('<II4s5I', 32, DDPF_FOURCC, f, 0, 0, 0, 0, 0)
  else:
    pf = struct.pack('<8I', 32, DDPF_RGB | (DDPF_ALPHAPIXELS if f[4] else 0), 0, *f)
  hdr = struct.pack('<7I44x', 124, flags, h, w, 0, 0, mips) + pf + struct.pack('<4I4x', caps, 0, 0, 0)
  with open(path, 'wb') as file:
    file.write(b'DDS ' + hdr + data)


def read_dds(path):
  with open(path, 'rb') as f:
    d = f.read()
  check(len(d) >= 128 and d[:4] == b'DDS ' and struct.unpack_from('<I', d, 4)[0] == 124, '{} is not a DDS'.format(path))
  size, flags, h, w, pitch, depth, mips = struct.unpack_from('<7I', d, 4)
  pf_size, pf_flags, fourcc, bits, r, g, b, a = struct.unpack_from('<II4s5I', d, 76)
  caps = struct.unpack_from('<I', d, 108)[0]
  return Dds(w, h, max(mips, 1), flags, pf_flags, fourcc if pf_flags & DDPF_FOURCC else None, bits, (r, g, b, a), caps,
             d[128:])


def dds_format(dds):
  """The FORMATS name of a DDS's pixel format (None for another one)."""
  for name, f in FORMATS.items():
    if dds.fourcc == f or (dds.fourcc is None and (dds.bits, ) + dds.masks == f):
      return name
  return None


# DDSx: ddsx::Header (32 bytes) and the surfaces (packed after it as a whole when a compression flag is set)
FLG_REV_MIP_ORDER, FLG_MOBILE_TEXFMT = 0x40000, 0x100000
FLG_COMPR_MASK, FLG_7ZIP, FLG_ZLIB, FLG_ZSTD = 0xE0000000, 0x40000000, 0x80000000, 0x20000000
D3DFMT = {'argb': 21, 'argb4444': 26, 'rgb565': 23, 'a1r5g5b5': 25, 'l8': 50, 'r4g4b4a4': 26 + 0x80,
          'dxt1': struct.unpack('<I', b'DXT1')[0], 'dxt5': struct.unpack('<I', b'DXT5')[0],
          'astc4': struct.unpack('<I', b'AST4')[0], 'astc8': struct.unpack('<I', b'AST8')[0]}

Ddsx = collections.namedtuple('Ddsx',
                              'd3d_format flags w h levels depth bpp mq_mip lq_mip dxt_shift mem_sz packed_sz data')


def unpack_lzma(packed, size=-1):
  """Data packed by lzma_compress_data (engine/ioSys/lzmaEnc.cpp): 5 bytes of LZMA properties and the raw stream."""
  props, dict_size = packed[0], struct.unpack_from('<I', packed, 1)[0]
  lzma1 = {'id': lzma.FILTER_LZMA1, 'dict_size': dict_size, 'lc': props % 9, 'lp': props // 9 % 5, 'pb': props // 45}
  return lzma.LZMADecompressor(lzma.FORMAT_RAW, filters=[lzma1]).decompress(packed[5:], size)


def unpack_ddsx_data(flags, packed, mem_sz):
  """The surfaces of a DDSx from its (packed) data; None for zstd, which Python's library does not read."""
  compr = flags & FLG_COMPR_MASK
  if compr == FLG_ZLIB:
    return zlib.decompressobj().decompress(packed, mem_sz)
  if compr == FLG_7ZIP:
    return unpack_lzma(packed, mem_sz)
  if compr == FLG_ZSTD:
    return None
  check(compr == 0, 'unknown DDSx compression {:08X}'.format(compr))
  return packed[:mem_sz]


def parse_ddsx(d, what):
  check(len(d) >= 32 and d[:4] == b'DDSx', '{} is not a DDSx'.format(what))
  fmt, flags, w, h, levels, hq, depth, bpp, q, shift, mem_sz, packed_sz = struct.unpack_from('<IIHHBBHHBBII', d, 4)
  data = d[32:32 + (packed_sz if flags & FLG_COMPR_MASK else mem_sz)]
  if flags & FLG_COMPR_MASK:
    check(len(data) == packed_sz, '{}: {} bytes of packed data, the header says {}'.format(what, len(data), packed_sz))
  data = unpack_ddsx_data(flags, data, mem_sz)
  if data is not None:
    check(len(data) == mem_sz, '{}: {} bytes of data, the header says {}'.format(what, len(data), mem_sz))
  return Ddsx(fmt, flags, w, h, levels, depth, bpp, q >> 4, q & 0xF, shift & 0xF, mem_sz, packed_sz, data)


def read_ddsx(path):
  with open(path, 'rb') as f:
    return parse_ddsx(f.read(), path)


def astcenc(tool):
  """ARM's astcenc next to a tool that runs it (its runtime files): the SSE2 build where there are several, as any CPU
  runs it."""
  programs = sorted(p for p in os.listdir(os.path.dirname(tool)) if p.startswith('astcenc'))
  check(programs, 'no astcenc next to {}'.format(tool))
  return os.path.join(os.path.dirname(tool), next((p for p in programs if 'sse2' in p), programs[0]))


def decode_astc(astcenc_path, out, name, fmt, w, h, blocks):
  """BGRA of an ASTC surface, decoded by astcenc (from an .astc file: the magic, block size, image size, the blocks)."""
  side = BLOCKS[fmt][0]
  header = struct.pack('<I3B', 0x5CA1AB13, side, side, 1) + b''.join(v.to_bytes(3, 'little') for v in (w, h, 1))
  src, dst = os.path.join(out, name + '.astc'), os.path.join(out, name + '.decoded.tga')
  with open(src, 'wb') as f:
    f.write(header + blocks)
  run([astcenc_path, '-dl', src, dst], out)
  dw, dh, pix = read_tga(dst)
  check((dw, dh) == (w, h), '{} decoded to {}x{}, expected {}x{}'.format(src, dw, dh, w, h))
  return pix


def chunks(data, sizes):
  ofs = 0
  for s in sizes:
    yield data[ofs:ofs + s]
    ofs += s


# TGA: uncompressed true color, 24 or 32 bits; pixels as BGRA bytes, rows top to bottom
def write_tga(path, w, h, bgra):
  check(len(bgra) == w * h * 4, 'bad TGA data size')
  with open(path, 'wb') as f:
    f.write(struct.pack('<BBBHHBHHHHBB', 0, 0, 2, 0, 0, 0, 0, 0, w, h, 32, 0x28) + bgra)


def read_tga(path):
  """(w, h, BGRA bytes with rows top to bottom)"""
  with open(path, 'rb') as f:
    d = f.read()
  check(len(d) >= 18, '{} is not a TGA'.format(path))
  id_len, cmap_type, img_type, _, _, _, _, _, w, h, bits, desc = struct.unpack_from('<BBBHHBHHHHBB', d, 0)
  check(cmap_type == 0 and img_type in (2, 10) and bits in (24, 32),
        '{}: TGA type {} with {} bits, expected true color'.format(path, img_type, bits))
  bpp, pos = bits // 8, 18 + id_len
  if img_type == 2:
    pix = d[pos:pos + w * h * bpp]
  else:  # run-length encoded packets (astcenc writes them): a byte of the count - 1, the top bit set for a run
    pix = bytearray()
    while len(pix) < w * h * bpp and pos < len(d):
      n = (d[pos] & 0x7F) + 1
      pix += d[pos + 1:pos + 1 + bpp] * n if d[pos] & 0x80 else d[pos + 1:pos + 1 + n * bpp]
      pos += 1 + (bpp if d[pos] & 0x80 else n * bpp)
    pix = bytes(pix)
  check(len(pix) == w * h * bpp, '{}: truncated TGA'.format(path))
  if bpp == 3:
    pix = b''.join(pix[i:i + 3] + b'\xff' for i in range(0, len(pix), 3))
  rows = [pix[y * w * 4:(y + 1) * w * 4] for y in range(h)]
  if not desc & 0x20:  # bottom-up
    rows.reverse()
  return w, h, b''.join(rows)


# PNG: 8-bit RGB or RGBA without interlacing (the CDK's icons), read only
def read_png(path):
  """(w, h, BGRA bytes with rows top to bottom)"""
  with open(path, 'rb') as f:
    d = f.read()
  check(d[:8] == b'\x89PNG\r\n\x1a\n', '{} is not a PNG'.format(path))
  pos, idat = 8, b''
  while pos < len(d):
    size, kind = struct.unpack_from('>I4s', d, pos)
    if kind == b'IHDR':
      w, h, depth, color, _, _, interlace = struct.unpack_from('>IIBBBBB', d, pos + 8)
      check(depth == 8 and color in (2, 6) and not interlace, '{}: unsupported PNG'.format(path))
    elif kind == b'IDAT':
      idat += d[pos + 8:pos + 8 + size]
    pos += 12 + size
  bpp = 4 if color == 6 else 3
  raw, stride, prev, rows = zlib.decompress(idat), w * bpp, bytearray(w * bpp), []
  for y in range(h):
    kind, row = raw[y * (stride + 1)], bytearray(raw[y * (stride + 1) + 1:(y + 1) * (stride + 1)])
    for i in range(stride):
      a, b, c = row[i - bpp] if i >= bpp else 0, prev[i], prev[i - bpp] if i >= bpp else 0
      p = a + b - c
      pred = (0, a, b, (a + b) // 2, a if abs(p - a) <= abs(p - b) and abs(p - a) <= abs(p - c) else
              b if abs(p - b) <= abs(p - c) else c)[kind]
      row[i] = (row[i] + pred) & 0xFF
    rows.append(row)
    prev = row
  pix = b''.join(bytes(r) for r in rows)
  if bpp == 3:
    return w, h, b''.join(bytes((pix[i + 2], pix[i + 1], pix[i], 255)) for i in range(0, len(pix), 3))
  return w, h, b''.join(bytes((pix[i + 2], pix[i + 1], pix[i], pix[i + 3])) for i in range(0, len(pix), 4))
