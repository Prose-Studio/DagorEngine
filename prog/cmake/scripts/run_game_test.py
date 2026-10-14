#!/usr/bin/env python3
"""Runs a game in its test mode for CTest (dagor_add_game_test, DagorTesting.cmake).

python run_game_test.py [--display] <out dir> <game> <argument>...

The game writes its report (dastest.json) and events into <out dir>. The exit code is the game's: 0 passed, 1 failed,
3 a test exceeded its time limit, 77 skipped (nothing ran, or the machine cannot run the tests: no video driver
started); 2 when the game wrote no report. The results of the tests are printed after the game's output.
--display: the game opens a window, so on Linux without a display server (neither DISPLAY nor WAYLAND_DISPLAY set),
where it cannot start, the test is skipped. DAGOR_TEST_UPDATE_REFERENCES=1 in the environment makes scenario tests
replace their reference images.
"""
import json
import os
import subprocess
import sys

EXIT_FAILED = 1
EXIT_INFRA_ERROR = 2
EXIT_SKIPPED = 77


def main(argv):
  display = argv[:1] == ['--display']
  if display:
    argv = argv[1:]
  if len(argv) < 2:
    print(__doc__, file=sys.stderr)
    return EXIT_INFRA_ERROR
  out, cmd = argv[0], argv[1:]
  if display and sys.platform.startswith('linux') and not (os.environ.get('DISPLAY') or os.environ.get('WAYLAND_DISPLAY')):
    print('skipped: the game opens a window, and this machine has no display (neither DISPLAY nor WAYLAND_DISPLAY set)')
    return EXIT_SKIPPED
  os.makedirs(out, exist_ok=True)
  report = os.path.join(out, 'dastest.json')
  for stale in (report, os.path.join(out, 'events.jsonl')):
    if os.path.exists(stale):
      os.remove(stale)
  if os.environ.get('DAGOR_TEST_UPDATE_REFERENCES') == '1':
    cmd.append('-test_update_references')
  sys.stdout.flush()
  # the game's output comes through a pipe, relayed as it comes: a Windows program of the GUI subsystem only has a
  # stdout when it is given one
  game = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  for line in iter(game.stdout.readline, b''):
    sys.stdout.buffer.write(line)
    sys.stdout.flush()
  code = game.wait()

  if not os.path.isfile(report):
    if code == EXIT_SKIPPED:
      print("skipped: this machine cannot run the tests, see the game's output above")
      return EXIT_SKIPPED
    print('the game wrote no test report (exit code {}), see its output above'.format(code))
    return EXIT_INFRA_ERROR if code == 0 else code if code > 0 else EXIT_FAILED
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
