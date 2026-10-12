#!/usr/bin/env python3
"""Dagor Engine commands: python dng.py <command> [arguments], python dng.py <command> -h for its arguments.

  new     creates a game project from a template in templates/
  relink  points a game project at this engine (its engine.blk and prog/CMakePresets.json)

The engine and its projects are built with CMake presets: cmake --list-presets in prog/ (see README.md).
"""
import os
import sys

if sys.version_info < (3, 8):
  sys.exit('dng.py needs Python 3.8 or newer')
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'prog', 'tools'))


def new(argv):
  from pythonCommon.dagorProject import create
  return create.main(argv)


def relink(argv):
  from pythonCommon.dagorProject import create
  return create.relink_main(argv)


COMMANDS = {'new': new, 'relink': relink}

if __name__ == '__main__':
  if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
    print(__doc__.strip())
    sys.exit(0 if sys.argv[1:2] in (['-h'], ['--help']) else 2)
  sys.exit(COMMANDS[sys.argv[1]](sys.argv[2:]))
