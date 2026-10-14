"""csvUtil2 on localization CSVs and texts.

localization: a task BLK (groups of CSVs found by path, wildcard and exclude regexp or listed, a language pack, a key
  pack filtering keys) writes the CSV of the task's languages and the dump of their values; the CSV it writes reads
  back the same, and a task BLK that cannot be read is rejected.
all-tasks: the same task BLK run as plainly as the usage allows (csvUtil2 <task.blk>: no task names, no -q) runs all
  its tasks.
word-breaks: -word_breaks:jp|zh inserts breaks (tab, or U+200B with -use:U+200B) where Japanese and Chinese text may
  wrap, by the tool's rules (no break before closing punctuation or after opening, Japanese breaks between scripts).

usage: csv_util.py localization|all-tasks|word-breaks <csvUtil2> (in DAGOR_TEST_OUT)
"""
import os
import shutil
import subprocess
import sys

BOM = b'\xef\xbb\xbf'
# the CSVs: "" is a quote, \n a line break; the first line names the columns; both line ends and a BOM are read
CSVS = {
  'lang/menu.csv': BOM + '''"<ID|readonly|noverify>";"<English>";"<Russian>";"<German>";"<comment>"\r
"menu/start";"Start";"Старт";"Start";""\r
"menu/quote";"Say ""hi""";"Скажи ""привет""";"Sag ""hallo""";"a comment"\r
"menu/lines";"one\\ntwo";"раз\\nдва";"eins\\nzwei";""\r
"debug/fps";"FPS";"ФПС";"FPS";"not for release"\r
'''.encode('utf-8'),
  'lang/menu_PC.csv': '''"<ID|readonly|noverify>";"<English>";"<Russian>";"<German>";"<comment>"
"menu/pc_only";"excluded";"исключён";"ausgeschlossen";""
'''.encode('utf-8'),
  'hud/hud.csv': '''"<ID|readonly|noverify>";"<English>";"<Russian>";"<German>";"<comment>"
"hud/hp";"HP: %d";"ОЗ: %d";"LP: %d";""
'''.encode('utf-8'),
}
TASKS = '''rootFolder:t="%(root)s"
group{
  name:t="common"
  find{
    path:t="lang"
    wildcard:t="*.csv"
    exclude:t="_PC\\.csv$"
  }
}
group{
  name:t="hud"
  csv:t="hud/hud.csv"
}
group{
  name:t="release"
  group:t="common"
  group:t="hud"
}
langpack{
  name:t="euro"
  lang:t="English"
  lang:t="Russian"
}
keypack{
  name:t="release"
  includeKey:t=".*"
  excludeKey:t="^debug/"
}
task{
  name:t="dump"
  group:t="release"
  langpack:t="euro"
  keypack:t="release"
  writeCsv:t="dump/release.csv"
  writeValDump:t="dump/release.txt"
}
'''
READ_BACK = '''rootFolder:t="%(root)s"
group{
  name:t="written"
  csv:t="dump/release.csv"
}
langpack{
  name:t="euro"
  lang:t="English"
  lang:t="Russian"
}
task{
  name:t="again"
  group:t="written"
  langpack:t="euro"
  writeCsv:t="again/release.csv"
  writeValDump:t="again/release.txt"
}
'''
# the keys of the group's files in order, debug/ and the excluded file's left out; each row ends with "; "
EXPECTED_CSV = '''"<ID|readonly|noverify>";"English";"Russian";"comment"\r
"menu/start";"Start";"Старт"; \r
"menu/quote";"Say ""hi""";"Скажи ""привет"""; \r
"menu/lines";"one
two";"раз
два"; \r
"hud/hp";"HP: %d";"ОЗ: %d"; \r
'''.encode('utf-8')
# each language's values, a line each, an empty line after each language
EXPECTED_DUMP = '''Start\r
Say "hi"\r
one
two\r
HP: %d\r
\r
Старт\r
Скажи "привет"\r
раз
два\r
ОЗ: %d\r
\r
'''.encode('utf-8')
# hand-derived from the rules: katakana|kanji, kanji|latin, digit|kana and after an ideographic full stop break; latin
# and digits stay together, no break before 。 and 」 or after 「
WORD_BREAKS = [
  ('jp', 'カタカナ漢字ABC123です。次「引用」', 'カタカナ|漢字|ABC123|です。|次「引用」'),
  ('zh', '中文，测试。OK', '中|文，|测|试。|OK'),
]


def run(args, cwd):
  result = subprocess.run(args, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  return result.returncode, result.stdout.decode('utf-8', 'replace')


def run_ok(args, cwd):
  code, output = run(args, cwd)
  if code != 0:
    sys.exit('%s\nexited with %d:\n%s' % (' '.join(args), code, output))
  return output


def read(path):
  with open(path, 'rb') as f:
    return f.read()


def write(path, data):
  os.makedirs(os.path.dirname(path), exist_ok=True)
  with open(path, 'wb') as f:
    f.write(data)


def check_file(path, expected, errors):
  if not os.path.exists(path):
    errors.append('%s was not written' % path)
    return
  actual = read(path)
  if actual != expected:
    errors.append('%s is\n%r\nexpected\n%r' % (path, actual.decode('utf-8', 'replace'), expected.decode('utf-8')))


def localization(tool, out, task_names):
  for name, data in CSVS.items():
    write(os.path.join(out, name), data)
  root = out.replace('\\', '/')
  write(os.path.join(out, 'tasks.blk'), (TASKS % {'root': root}).encode('utf-8'))
  write(os.path.join(out, 'read_back.blk'), (READ_BACK % {'root': root}).encode('utf-8'))
  errors = []
  run_ok([tool] + (['-q'] if task_names else []) + ['tasks.blk'] + task_names, out)
  check_file(os.path.join(out, 'dump/release.csv'), EXPECTED_CSV, errors)
  check_file(os.path.join(out, 'dump/release.txt'), EXPECTED_DUMP, errors)
  if not task_names:
    return errors
  run_ok([tool, '-q', 'read_back.blk', 'again'], out)
  check_file(os.path.join(out, 'again/release.csv'), EXPECTED_CSV, errors)
  check_file(os.path.join(out, 'again/release.txt'), EXPECTED_DUMP, errors)
  code, output = run([tool, '-q', 'missing.blk', 'dump'], out)
  if code == 0 or 'cannot read: missing.blk' not in output:
    errors.append('a missing task BLK was not rejected (exit code %d):\n%s' % (code, output))
  return errors


def word_breaks(tool, out):
  errors = []
  for lang, text, expected in WORD_BREAKS:
    for option, sep in (([], '\t'), (['-use:U+200B'], '\u200b')):
      src = os.path.join(out, '%s.txt' % lang)
      dest = os.path.join(out, '%s%s.out.txt' % (lang, '-u200b' if option else ''))
      write(src, text.encode('utf-8'))
      run_ok([tool, '-q', src, '-word_breaks:' + lang, dest] + option, out)
      check_file(dest, expected.replace('|', sep).encode('utf-8'), errors)
  return errors


def main():
  scenario, tool = sys.argv[1], os.path.abspath(sys.argv[2])
  out = os.environ.get('DAGOR_TEST_OUT')
  if not out:
    sys.exit('DAGOR_TEST_OUT is not set (the tests run through CTest)')
  shutil.rmtree(out, ignore_errors=True)
  os.makedirs(out)
  out = os.path.abspath(out)
  if scenario == 'localization':
    errors = localization(tool, out, ['dump'])
  elif scenario == 'all-tasks':
    errors = localization(tool, out, [])
  elif scenario == 'word-breaks':
    errors = word_breaks(tool, out)
  else:
    sys.exit('unknown scenario ' + scenario)
  if errors:
    sys.exit('\n'.join(errors))
  print('%s: as expected' % scenario)


if __name__ == '__main__':
  main()
