"""Tests of fontgen2 (CTest: fontgen2.<scenario>): dargbox's fonts (prog/tools/toolsData/dargbox/fonts) built again,
fully dynamic, into the fonts.dynFont.blk dargbox loads; a classic baked atlas of two of its fonts, read back here as
the engine loads it (DagorFontBinDump, engine/guiBase/font.cpp): its fonts, glyphs and textures against the reference
images fontgen2 writes; and broken rules.

python fontgen2_tests.py <scenario> <fontgen2>
"""
import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'converters', 'ddsx2dds', 'tests'))
import texfiles as tf  # noqa: E402

FONTS = os.path.join(HERE, '..', '..', 'toolsData', 'dargbox', 'fonts')
BAKED = '''prefix:t="out/"
atlas:t="baked"
font{
  name:t="lato"
  file:t="lato-regular.ttf"
  size_pixels:r=16
  include{ range:ip2=32,126; includeCp:b=no; }
}
font{
  name:t="mono"
  file:t="jetbrains-mono-nl-regular.ttf"
  size_pixels:r=12
  include{ range:ip2=32,126; includeCp:b=no; }
}
'''


def dynamic(out, fontgen2):
  # the rules and the fonts in a dir of their own: fontgen2 reads the fonts from its working dir and writes there
  for name in os.listdir(FONTS):
    if name == 'fontgen.blk' or name.endswith(('.ttf', '.otf')):
      shutil.copyfile(os.path.join(FONTS, name), os.path.join(out, name))
  tf.run([fontgen2, 'fontgen.blk', '-fullDynamic', '-quiet'], out)
  built, committed = (os.path.join(d, 'fonts.dynFont.blk') for d in (out, FONTS))
  with open(built, 'rb') as f, open(committed, 'rb') as ref:
    tf.check(f.read() == ref.read(), '{} differs from {} (dargbox\'s, built from its fontgen.blk)'.format(
      built, committed))


def read_font(block, what):
  """(name, fontHt, ascent, glyphs, ASCII glyph indices, texture count) of a font of a DFz7 font file: its dump (the
  data DagorFontBinDump maps) packed with 7zip's LZMA, the size first."""
  data = tf.unpack_lzma(block)
  size = struct.unpack_from('<i', data)[0]
  tf.check(len(data) == size + 4, '{}: a font dump of {} bytes, its size says {}'.format(what, len(data) - 4, size))
  dump = data[4:]
  # PatchableTab<GlyphData> glyph, uTable, tex (offset, count, 8 bytes reserved); fontHt, ascent, descent, lineSpacing,
  # xBase, yBase; uint16_t asciiGlyphIdx[256]; PatchablePtr<const char> name; selfData; uint32_t classicFont
  glyph_ofs, glyph_count = struct.unpack_from('<ii', dump, 0)
  tex_count = struct.unpack_from('<i', dump, 36)[0]
  font_ht, ascent = struct.unpack_from('<2i', dump, 48)
  ascii_idx = struct.unpack_from('<256H', dump, 72)
  name_ofs, classic = struct.unpack_from('<i', dump, 584)[0], struct.unpack_from('<I', dump, 600)[0]
  name = dump[name_ofs:dump.index(b'\0', name_ofs)].decode()
  tf.check(classic == 0xFF, '{}: font {} is not a classic one ({:#x})'.format(what, name, classic))
  # GlyphData: float u0, v0, u1, v1; uint8_t x0, y0, x1, y1; int16_t dx; int8_t texIdx; uint8_t dynGrp
  glyphs = [struct.unpack_from('<4f4BhbB', dump, glyph_ofs + 24 * i) for i in range(glyph_count)]
  return name, font_ht, ascent, glyphs, ascii_idx, tex_count


def read_blocks(d, pos, count, what):
  """count blocks (the size with 2 bits of flags, then the data) from pos: ([data], the position after them)"""
  blocks = []
  for _ in range(count):
    tf.check(pos + 4 <= len(d), '{}: truncated'.format(what))
    size = struct.unpack_from('<i', d, pos)[0] & 0x3FFFFFFF
    blocks.append(d[pos + 4:pos + 4 + size])
    pos += 4 + size
  return blocks, pos


def baked(out, fontgen2):
  for name in ('lato-regular.ttf', 'jetbrains-mono-nl-regular.ttf'):
    shutil.copyfile(os.path.join(FONTS, name), os.path.join(out, name))
  with open(os.path.join(out, 'fontgen.blk'), 'w') as f:
    f.write(BAKED)
  tf.run([fontgen2, 'fontgen.blk', '-tga', '-quiet'], out)
  path = os.path.join(out, 'out', 'baked.bin')
  with open(path, 'rb') as f:
    d = f.read()
  # 'DFz\7', the fonts and the dynamic glyph groups (none: everything is in the atlas), the fonts, the textures' block
  tf.check(d[:4] == b'DFz\x07', '{} is not a DFz7 font file'.format(path))
  font_count, dyn_groups = struct.unpack_from('<ii', d, 4)
  tf.check((font_count, dyn_groups) == (2, 0), '{}: {} fonts with {} dynamic groups, expected 2 and 0'.format(
    path, font_count, dyn_groups))
  font_blocks, pos = read_blocks(d, 12, font_count, path)
  (tex_block, ), pos = read_blocks(d, pos, 1, path)
  tf.check(pos == len(d), '{}: {} bytes after the textures'.format(path, len(d) - pos))
  fonts = [read_font(b, path) for b in font_blocks]
  textures = []
  for i, block in enumerate(read_blocks(tex_block, 0, fonts[0][5], path)[0]):
    tex = tf.parse_ddsx(block, '{} texture {}'.format(path, i))
    tf.check((tex.d3d_format, tex.levels) == (tf.D3DFMT['l8'], 1), '{} texture {}: format {:#x} with {} mips, expected '
             'L8 without mips'.format(path, i, tex.d3d_format, tex.levels))
    # the reference image (-tga) of each texture: the glyphs in its alpha
    w, h, ref = tf.read_tga(os.path.join(out, 'out', 'baked.0_{}.tga'.format(i)))
    tf.check((w, h) == (tex.w, tex.h) and tex.data == ref[3::4], '{} texture {} differs from baked.0_{}.tga'.format(
      path, i, i))
    textures.append(tex)
  for (name, font_ht, ascent, glyphs, ascii_idx, tex_count), expected in zip(fonts, (('lato', 16), ('mono', 12))):
    tf.check((name, font_ht, tex_count) == expected + (len(textures), ), 'font {} of height {} with {} textures, '
             'expected {} of {} with {}'.format(name, font_ht, tex_count, *expected, len(textures)))
    tf.check(0 < ascent <= font_ht + 4, '{}: ascent {}'.format(name, ascent))
    space = glyphs[ascii_idx[32]]
    tf.check(space[9] == -1 and space[8] > 0, '{}: the space has an image or no advance'.format(name))
    # each printable character: its image in a texture, as large as its box, not empty
    for c in range(33, 127):
      u0, v0, u1, v1, x0, y0, x1, y1, dx, tex_idx, _ = glyphs[ascii_idx[c]]
      what = '{} {!r}'.format(name, chr(c))
      tf.check(0 <= tex_idx < len(textures) and dx > 0, '{}: texture {}, advance {}'.format(what, tex_idx, dx))
      tex = textures[tex_idx]
      l, t, r, b = (round(v * s) for v, s in ((u0, tex.w), (v0, tex.h), (u1, tex.w), (v1, tex.h)))
      tf.check(0 <= l < r <= tex.w and 0 <= t < b <= tex.h and (r - l, b - t) == (x1 - x0, y1 - y0),
               '{}: image {},{}-{},{} of {}x{} for a box of {}x{}'.format(what, l, t, r, b, tex.w, tex.h, x1 - x0,
                                                                         y1 - y0))
      tf.check(any(tex.data[y * tex.w + x] for y in range(t, b) for x in range(l, r)), what + ': empty image')
  # built again only when its sources change
  log = tf.run([fontgen2, 'fontgen.blk', '-tga', '-quiet'], out)
  with open(path, 'rb') as f:
    tf.check('up-to-date' in log and f.read() == d, 'the atlas was built again')


def errors(out, fontgen2):
  shutil.copyfile(os.path.join(FONTS, 'lato-regular.ttf'), os.path.join(out, 'lato-regular.ttf'))
  with open(os.path.join(out, 'missing.blk'), 'w') as f:
    f.write(BAKED.replace('jetbrains-mono-nl-regular.ttf', 'missing.ttf'))
  tf.run([fontgen2, 'missing.blk', '-quiet'], out, code=None)
  tf.check(not os.path.exists(os.path.join(out, 'out', 'baked.bin')), 'baked.bin was written without one of its fonts')
  # a fully dynamic font loads its file at runtime: one that does not exist (and is not optional) is an error too
  tf.run([fontgen2, 'missing.blk', '-fullDynamic', '-quiet'], out, code=None)
  tf.run([fontgen2, 'fontgen.txt'], out, code=None)
  tf.run([fontgen2, 'missing.blk', '-unknownOption'], out, code=None)


if __name__ == '__main__':
  sys.exit(tf.main({'dynamic': dynamic, 'baked': baked, 'errors': errors}))
