#!/usr/bin/env python3
"""Compare a built tree's engine ES codegen with the committed jam output (deleted with jam).

python codegen_parity.py <build dir>...
Only engine sources are compared: a newly scaffolded game's source location differs from the template's.
Line endings are normalized because Git checks out CRLF on Windows; all generated C++ text must match.
"""
import argparse
import difflib
from pathlib import Path
import re
import sys

ENGINE = Path(__file__).resolve().parents[3]


def main(argv):
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument('build_dirs', nargs='+', type=Path)
  args = parser.parse_args(argv)
  compared = failed = 0
  for tree in args.build_dirs:
    count = 0
    for generated in sorted(tree.rglob('*.gen.es.cpp')):
      if generated.parent.name != 'es':
        continue
      stem = generated.name[:-len('.gen.es.cpp')]
      forwarders = [p for p in generated.parent.glob(stem + '.*')
                    if not p.name.endswith('.gen.es.cpp')]
      match = next((m for p in forwarders
                    for m in [re.fullmatch(r'#include "([^"]+)"\s*', p.read_text(encoding='utf-8'))] if m), None)
      if not match:
        print('missing or invalid source forwarding file for: {}'.format(generated))
        failed += 1
        continue
      source = Path(match[1]).resolve()
      try:
        source.relative_to(ENGINE / 'prog')
      except ValueError:
        continue
      committed = source.with_suffix('.gen.es.cpp')
      count += 1
      if not committed.is_file():
        print('missing committed output: {}'.format(committed))
        failed += 1
        continue
      expected = committed.read_text(encoding='utf-8')
      actual = generated.read_text(encoding='utf-8')
      if actual != expected:
        failed += 1
        print(''.join(difflib.unified_diff(expected.splitlines(keepends=True), actual.splitlines(keepends=True),
                                         fromfile=str(committed), tofile=str(generated))))
    print('{}: {} engine ES outputs compared'.format(tree, count))
    if not count:
      print('no generated engine ES outputs found: build the game first')
      failed += 1
    compared += count
  print('{} engine ES outputs, {} differences or errors'.format(compared, failed))
  return 1 if failed else 0


if __name__ == '__main__':
  sys.exit(main(sys.argv[1:]))
