"""binBlk -j: all_types.blk exported to JSON must be valid JSON (any strict parser reads it) holding every value.

usage: blk_json.py <binBlk> (in DAGOR_TEST_OUT)
"""
import json
import math
import os
import shutil
import subprocess
import sys

EXPECTED = {
  'str': 'plain',
  'str_quoted': 'with "quotes", a ~tilde and a\ttab',
  'str_ticks': 'single "quoted"',
  'str_unicode': '\u00fcn\u00efc\u00f6d\u00e9 \u2713 \u65e5\u672c\u8a9e',
  'str_empty': '',
  'str_multiline': 'line one\nline two',
  'int': 42,
  'int_min': -2147483648,
  'int_max': 2147483647,
  'int64_min': -9223372036854775807,
  'int64_max': 9223372036854775807,
  'real': 3.14159,
  'real_small': -1.5e-20,
  'real_big': 3.4e38,
  'bool_yes': True,
  'bool_no': False,
  'color': [255, 128, 0, 64],
  'point2': [1.5, -2.25],
  'point3': [0.1, 0.2, 0.3],
  'point4': [1, 2, 3, 4],
  'ipoint2': [-7, 8],
  'ipoint3': [1, -2, 3],
  'ipoint4': [10, 20, 30, -40],
  'matrix': [1, 0, 0, 0, 0.5, 0, 0, 0, 2, 10, -20, 30.5],
  'repeated': [1, 2],  # repeated names become arrays
  'nested': [{'repeated': ['a', 'b'], 'deeper': {'name with spaces': 'x', 'empty': {}}}, {'second': True}],
}


def same(expected, actual, path, errors):
  if isinstance(expected, dict):
    if not isinstance(actual, dict) or list(expected) != list(actual):
      keys = list(actual) if isinstance(actual, dict) else actual
      errors.append('%s: keys %s, expected %s' % (path, keys, list(expected)))
      return
    for k in expected:
      same(expected[k], actual[k], '%s/%s' % (path, k), errors)
  elif isinstance(expected, list):
    if not isinstance(actual, list) or len(expected) != len(actual):
      errors.append('%s: %r, expected %r' % (path, actual, expected))
      return
    for i, (e, a) in enumerate(zip(expected, actual)):
      same(e, a, '%s[%d]' % (path, i), errors)
  elif isinstance(expected, (bool, str)):
    if type(expected) is not type(actual) or expected != actual:
      errors.append('%s: %r, expected %r' % (path, actual, expected))
  elif isinstance(actual, bool) or not isinstance(actual, (int, float)):
    errors.append('%s: %r, expected %r' % (path, actual, expected))
  elif isinstance(expected, float):
    # the export writes reals as %g of the float the BLK holds
    if not math.isclose(expected, actual, rel_tol=1e-6):
      errors.append('%s: %r, expected %r' % (path, actual, expected))
  elif expected != actual:
    errors.append('%s: %r, expected %r' % (path, actual, expected))


def main():
  binblk = os.path.abspath(sys.argv[1])
  out = os.environ.get('DAGOR_TEST_OUT')
  if not out:
    sys.exit('DAGOR_TEST_OUT is not set (the tests run through CTest)')
  shutil.rmtree(out, ignore_errors=True)
  os.makedirs(out)
  blk = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'all_types.blk')
  dest = os.path.join(out, 'all_types.json')
  result = subprocess.run([binblk, blk, dest, '-j', '-h'], cwd=out)
  if result.returncode != 0:
    sys.exit('binBlk -j exited with %d' % result.returncode)
  with open(dest, 'rb') as f:
    text = f.read().decode('utf-8')
  try:
    data = json.loads(text)
  except json.JSONDecodeError as e:
    line = text.splitlines()[e.lineno - 1] if e.lineno <= len(text.splitlines()) else ''
    sys.exit('%s is not valid JSON: %s\n  line %d: %r' % (dest, e, e.lineno, line))
  errors = []
  same(EXPECTED, data, '', errors)
  if errors:
    sys.exit('%s does not hold the values of %s:\n  %s' % (dest, blk, '\n  '.join(errors)))
  print('%s: %d values exported' % (dest, len(EXPECTED)))


if __name__ == '__main__':
  main()
