"""Tests of utf8ranges (CTest: utf8ranges.<scenario>): the Unicode pages (256 code points each) UTF-8 texts use, the
ranges a game's fonts must have glyphs for.

python utf8ranges_tests.py <scenario> <utf8ranges>
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'converters', 'ddsx2dds',
                                'tests'))
import texfiles as tf  # noqa: E402

# the texts (of several files) and the pages they use, in order; one beyond the BMP (U+1F600) is its own page on every
# platform, not those of its UTF-16 surrogates (U+D83D U+DE00)
TEXTS = ['Hello, world!\nПривет, мир\nΓειά σου κόσμε\n', 'Ünïcödé — “quotes” € 日本語 かな \U0001F600\n']
PAGES = ['u00xx', 'u03xx', 'u04xx', 'u20xx', 'u30xx', 'u65xx', 'u67xx', 'u8Axx', 'u1F6xx']


def ranges(out, utf8ranges):
  files = []
  for i, text in enumerate(TEXTS):
    files.append(os.path.join(out, 'text{}.utf8.txt'.format(i)))
    with open(files[-1], 'w', encoding='utf-8', newline='\n') as f:
      f.write(text)
  log = tf.run([utf8ranges] + files, out)
  pages = [line.strip() for line in log.splitlines() if line.strip().startswith('u') and line.strip().endswith('xx')]
  tf.check(pages == PAGES, 'pages {}, expected {}'.format(' '.join(pages), ' '.join(PAGES)))


def errors(out, utf8ranges):
  tf.run([utf8ranges], out, code=1)
  # a text it cannot read, or not UTF-8, leaves its pages out: that must not pass for a result
  tf.run([utf8ranges, os.path.join(out, 'missing.utf8.txt')], out, code=None)
  latin1 = os.path.join(out, 'latin1.txt')
  with open(latin1, 'wb') as f:
    f.write('Ünïcödé\n'.encode('latin-1'))
  tf.run([utf8ranges, latin1], out, code=None)


if __name__ == '__main__':
  sys.exit(tf.main({'ranges': ranges, 'errors': errors}))
