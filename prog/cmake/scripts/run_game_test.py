#!/usr/bin/env python3
"""Runs a game in its test mode for CTest (dagor_add_game_test, DagorTesting.cmake).

python run_game_test.py <out dir> <game> <argument>...

The game writes its report (dastest.json) and events into <out dir>. The exit code is the game's: 0 passed, 1 failed,
3 a test exceeded its time limit, 77 skipped (nothing ran); 2 when the game wrote no report. The results of the tests
are printed after the game's output. DAGOR_TEST_UPDATE_REFERENCES=1 in the environment makes scenario tests replace
their reference images.
"""
import json
import os
import subprocess
import sys

EXIT_FAILED = 1
EXIT_INFRA_ERROR = 2
EXIT_SKIPPED = 77


def main(argv):
  if len(argv) < 2:
    print(__doc__, file=sys.stderr)
    return EXIT_INFRA_ERROR
  out, cmd = argv[0], argv[1:]
  os.makedirs(out, exist_ok=True)
  report = os.path.join(out, 'dastest.json')
  for stale in (report, os.path.join(out, 'events.jsonl')):
    if os.path.exists(stale):
      os.remove(stale)
  if os.environ.get('DAGOR_TEST_UPDATE_REFERENCES') == '1':
    cmd.append('-test_update_references')
  sys.stdout.flush()
  code = subprocess.call(cmd)

  if not os.path.isfile(report):
    print('the game wrote no test report (exit code {}), see its output above'.format(code))
    return EXIT_INFRA_ERROR if code in (0, EXIT_SKIPPED) else code if code > 0 else EXIT_FAILED
  with open(report, encoding='utf-8') as f:
    tests = json.load(f).get('tests', [])
  failed = 0
  for t in tests:
    if t.get('skipped'):
      status = 'skipped'
    elif t.get('passed'):
      status = 'passed'
    else:
      status = 'FAILED'
      failed += 1
    print('{}: {}{}'.format(status, t.get('name', ''), ' ({})'.format(t['location']) if t.get('location') else ''))
    if status == 'FAILED':
      for message in t.get('messages', []):
        print('    ' + message)
  print('{} tests, {} failed; report {}'.format(len(tests), failed, report))
  if code < 0:  # killed by a signal
    return EXIT_FAILED
  return EXIT_FAILED if code == 0 and failed else code


if __name__ == '__main__':
  sys.exit(main(sys.argv[1:]))
