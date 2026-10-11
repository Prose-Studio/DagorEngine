#!/usr/bin/env python3
"""Dagor Engine commands: python dng.py <command> [arguments], python dng.py <command> -h for its arguments.

  build     configures and builds the engine's CMake trees (tools, tests, ...) and its projects
  test      builds and runs the engine's tests
  new       creates a game project from a template in templates/
  devtools  downloads and sets up the toolkit of the jam build (the CMake build fetches its own)

build and test take --jam for the jam build, until it is deleted.
"""
import os
import sys

if sys.version_info < (3, 8):
  sys.exit('dng.py needs Python 3.8 or newer')
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'prog', 'tools'))


def _jam(argv):
  """the arguments without --jam, and whether it was given"""
  return [a for a in argv if a != '--jam'], '--jam' in argv


def devtools(argv):
  from pythonCommon import dagorDevtools
  return dagorDevtools.main(argv)


def build(argv):
  argv, jam = _jam(argv)
  if jam:
    from pythonCommon.dagorBuild import cli
    return cli.main(argv)
  from pythonCommon.dagorCMake import cli
  return cli.build(argv)


def new(argv):
  from pythonCommon.dagorProject import create
  return create.main(argv)


def test(argv):
  argv, jam = _jam(argv)
  if jam:
    from pythonCommon.dagorBuild import ENGINE_ROOT, HOST, HOST_ARCH, TOOLS_DIR
    from pythonCommon.dagorTest import cli
    return cli.main(argv, ENGINE_ROOT, HOST, HOST_ARCH, TOOLS_DIR)
  from pythonCommon.dagorCMake import cli
  return cli.test(argv)


COMMANDS = {'build': build, 'test': test, 'new': new, 'devtools': devtools}

if __name__ == '__main__':
  if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
    print(__doc__.strip())
    sys.exit(0 if sys.argv[1:2] in (['-h'], ['--help']) else 2)
  sys.exit(COMMANDS[sys.argv[1]](sys.argv[2:]))
