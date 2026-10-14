"""Tests of guiTex (CTest: guiTex.<scenario>): a GUI atlas built from a folder of icons (TGAs written here, of several
sizes, transparent parts and an animation stripe, and a PNG icon of the CDK), its coordinates BLK and texture read
back here and compared with the icons; the DDSx atlas and bundle the games load, and unpacking an atlas again.

python guiTex_tests.py <scenario> <guiTex> <plugin>...
"""
import os
import re
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'ddsx2dds', 'tests'))
import texfiles as tf  # noqa: E402

ICON = os.path.join(HERE, '..', '..', '..', 'toolsData', 'dagor_cdk', 'commonData', 'icons', 'play.png')
CONFIG = '''Input{
  dir:t="icons"
}
Output{
  width:r=256
  height:r=256
  outdir:t="out"
  texture:t="atlas"
}
'''


def icon(w, h, seed, round_=False):
  """BGRA of an icon; round ones are transparent outside a circle."""
  pix = bytearray()
  for y in range(h):
    for x in range(w):
      inside = not round_ or (2 * x + 1 - w) ** 2 + (2 * y + 1 - h) ** 2 <= w * h
      pix += bytes(((x * 9 + seed * 40) & 0xFF, (y * 11 + seed * 70) & 0xFF, (seed * 50 + x + y) & 0xFF,
                    255 if inside else 0))
  return bytes(pix)


# name: (w, h, BGRA); anim@@4 is a stripe of 4 frames
ICONS = {'square': (24, 24, icon(24, 24, 1)), 'wide': (40, 12, icon(40, 12, 2)), 'tall': (10, 36, icon(10, 36, 3)),
         'round': (20, 20, icon(20, 20, 4, True)), 'small': (6, 6, icon(6, 6, 5)), 'anim@@4': (64, 16, icon(64, 16, 6))}


def make_icons(out):
  os.makedirs(os.path.join(out, 'icons'))
  for name, (w, h, pix) in ICONS.items():
    tf.write_tga(os.path.join(out, 'icons', name + '.tga'), w, h, pix)
  shutil.copyfile(ICON, os.path.join(out, 'icons', 'play.png'))
  with open(os.path.join(out, 'atlas.blk'), 'w') as f:
    f.write(CONFIG)
  return os.path.join(out, 'atlas.blk')


def source_icons():
  """name: (w, h, BGRA) of all the icons"""
  return dict(ICONS, play=tf.read_png(ICON))


def parse_blk(path):
  """The blocks of a text BLK as nested (name, {param: value}, [blocks]) (enough for the coordinates BLKs)."""
  root = ('', {}, [])
  stack = [root]
  with open(path) as f:
    for line in f:
      line = line.strip()
      if line.endswith('{'):
        blk = (line[:-1].strip(), {}, [])
        stack[-1][2].append(blk)
        stack.append(blk)
      elif line == '}':
        stack.pop()
      elif line:
        m = re.match(r'(\w+):(\w+)\s*=\s*"?([^"]*)"?$', line)
        tf.check(m, '{}: cannot read "{}"'.format(path, line))
        stack[-1][1][m.group(1)] = m.group(3) if m.group(2) == 't' else float(m.group(3))
  return root


def check_atlas(blk_path, atlas_w, atlas_h, pixels, icons):
  """The coordinates against the icons and the atlas (BGRA rows of atlas_w): every icon once, of its size, inside the
  texture, and there each of its pixels (transparent where the icon is)."""
  tf.check(os.path.exists(blk_path), '{} was not written'.format(blk_path))
  texs = parse_blk(blk_path)[2]
  tf.check(len(texs) == 1 and texs[0][0] == 'tex', '{}: expected one tex{{}} block'.format(blk_path))
  tex = texs[0]
  tf.check((tex[1].get('wd'), tex[1].get('ht')) == (atlas_w, atlas_h), '{}: atlas {}x{}, the texture is {}x{}'.format(
    blk_path, tex[1].get('wd'), tex[1].get('ht'), atlas_w, atlas_h))
  placed = {}
  for kind, params, _ in tex[2]:
    if kind == 'pic':
      name, frames = params['name'], 1
    else:
      tf.check(kind == 'stripe', '{}: unknown block {}'.format(blk_path, kind))
      name, frames = '{}@@{}'.format(params['prefix'], int(params['count'])), int(params['count'])
    tf.check(name in icons and name not in placed, '{}: unexpected or repeated {} {}'.format(blk_path, kind, name))
    x, y, w, h = (int(params[k]) for k in ('left', 'top', 'wd', 'ht'))
    iw, ih, src = icons[name]
    tf.check((w * frames, h) == (iw, ih), '{}: {} is {}x{} ({} frames), the icon {}x{}'.format(
      blk_path, name, w, h, frames, iw, ih))
    tf.check(0 <= x and x + iw <= atlas_w and 0 <= y and y + ih <= atlas_h, '{}: {} is out of the atlas'.format(
      blk_path, name))
    for row in range(ih):
      for col in range(iw):
        s = src[(row * iw + col) * 4:(row * iw + col + 1) * 4]
        a = pixels[((y + row) * atlas_w + x + col) * 4:((y + row) * atlas_w + x + col + 1) * 4]
        tf.check(a == s if s[3] else a[3] == 0, 'the atlas differs from {} at its pixel {},{}: {} for {}'.format(
          name, col, row, a.hex(), s.hex()))
    placed[name] = (x, y)
  tf.check(sorted(placed) == sorted(icons), '{}: missing {}'.format(blk_path, ', '.join(set(icons) - set(placed))))


def atlas(out, guitex, *plugins):
  config = make_icons(out)
  tf.run([guitex, config], out)
  dds = tf.read_dds(os.path.join(out, 'out', 'atlas.dds'))
  tf.check(tf.dds_format(dds) == 'argb' and dds.mips == 1, 'the atlas is {} with {} mips, expected ARGB without mips'
           .format(tf.dds_format(dds), dds.mips))
  # cropped to the rows used, a multiple of 4
  tf.check(dds.w == 256 and dds.h % 4 == 0 and dds.h < 256, 'the atlas is {}x{}'.format(dds.w, dds.h))
  check_atlas(os.path.join(out, 'out', 'atlas.blk'), dds.w, dds.h, dds.data, source_icons())


def read_bundle(path):
  """(coordinates BLK block, DDSx) of an atlas bundle (-mkbundle): a 'TA.' block with the BLK, then the DDSx."""
  with open(path, 'rb') as f:
    d = f.read()
  tf.check(d[:4] == b'\0TA.', '{} is not an atlas bundle'.format(path))
  size = struct.unpack_from('<i', d, 4)[0] & 0x3FFFFFFF
  return d[8:8 + size], tf.parse_ddsx(d[8 + size:], path)


def ddsx(out, guitex, *plugins):
  # the DDSx atlas holds the DDS one's pixels; built with the output dir given as a build script would
  config = make_icons(out)
  tf.run([guitex, config], out)
  dds = tf.read_dds(os.path.join(out, 'out', 'atlas.dds'))
  odir = os.path.join(out, 'pc')
  tf.run([guitex, config, '-ddsx:PC', '-odir:' + odir], out)
  tex = tf.read_ddsx(os.path.join(odir, 'atlas.ddsx'))
  tf.check((tex.d3d_format, tex.w, tex.h, tex.levels, tex.data) == (tf.D3DFMT['argb'], dds.w, dds.h, 1, dds.data),
           'the DDSx atlas differs from the DDS one')
  check_atlas(os.path.join(odir, 'atlas.blk'), dds.w, dds.h, tex.data, source_icons())
  # the bundle (BLK and DDSx in one file) the games load; built again only when its sources change
  bundle = os.path.join(out, 'bundle', 'atlas.ta.bin')
  tf.run([guitex, config, '-ddsx:PC', '-mkbundle', '-odir:' + os.path.dirname(bundle)], out)
  coords, tex = read_bundle(bundle)
  tf.check(tex.data == dds.data, 'the bundle\'s DDSx differs from the DDS atlas')
  for name in ('square', 'wide', 'tall', 'round', 'small', 'play', 'anim'):
    tf.check(name.encode() in coords, 'the bundle\'s coordinates have no {}'.format(name))
  mtime = os.path.getmtime(bundle)
  log = tf.run([guitex, config, '-ddsx:PC', '-mkbundle', '-odir:' + os.path.dirname(bundle)], out)
  tf.check('up-to-date' in log and os.path.getmtime(bundle) == mtime, 'the bundle was built again')


def unpack(out, guitex, *plugins):
  # an atlas unpacked is its icons again (stripes as one image, as they were)
  config = make_icons(out)
  tf.run([guitex, config], out)
  dest = os.path.join(out, 'unpacked')
  tf.run([guitex, os.path.join(out, 'out', 'atlas.blk'), '-unpack:' + dest], os.path.join(out, 'out'))
  for name, (w, h, src) in source_icons().items():
    path = os.path.join(dest, (name + '@@0' if '@@' in name else name) + '.tga')
    tf.check(os.path.exists(path), '{} was not unpacked'.format(path))
    uw, uh, pix = tf.read_tga(path)
    tf.check((uw, uh) == (w, h), '{} is {}x{}, the icon {}x{}'.format(path, uw, uh, w, h))
    for i in range(w * h):
      s, u = src[i * 4:i * 4 + 4], pix[i * 4:i * 4 + 4]
      tf.check(u == s if s[3] else u[3] == 0, '{} differs from its icon at pixel {}'.format(path, i))


if __name__ == '__main__':
  sys.exit(tf.main({'atlas': atlas, 'ddsx': ddsx, 'unpack': unpack}))
