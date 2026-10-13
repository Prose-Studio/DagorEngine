"""How a game project finds the engine checkout it is built with: engineRoot in its application.blk.

<project>/application.blk (the setup of the project and its tools) holds engineRoot:t="<path>", relative to the project
root or absolute. The engine reads it too (the %engine named mount, prog/engine/osApiWrappers/namedMounts.cpp), so the
game and the tools find the engine from any dir inside the project.
"""
import os
import re

from ..datablock import escapeBlkString, unescapeBlkString

APPLICATION_BLK = 'application.blk'

_ENGINE_ROOT_RE = re.compile(r'^([ \t]*engineRoot[ \t]*:[ \t]*t[ \t]*=[ \t]*)"((?:[^"~\n]|~.)*)"', re.MULTILINE)
_ENGINE_ROOT_COMMENT = ('// the Dagor Engine checkout this project is built with: relative to this dir or absolute ("python '
                        '<engine>/dng.py relink <project dir>" changes it, and prog/CMakePresets.json with it)')


class ProjectError(Exception):
  pass


def is_engine_root(path: str) -> bool:
  return os.path.isfile(os.path.join(path, 'prog', 'cmake', 'DagorConfig.cmake'))


def norm(path: str) -> str:
  return os.path.normpath(os.path.abspath(path)).replace('\\', '/')


def read_engine_ref(project_dir: str) -> str:
  """engineRoot of <project_dir>/application.blk as written: relative to the project or absolute."""
  fn = os.path.join(project_dir, APPLICATION_BLK)
  try:
    with open(fn, 'r', encoding='utf-8') as f:
      m = _ENGINE_ROOT_RE.search(f.read())
  except OSError as e:
    raise ProjectError('cannot read {}: {}'.format(fn, e.strerror))
  if not m:
    raise ProjectError('{}: expected engineRoot:t="<path to the engine checkout>"'.format(fn))
  return unescapeBlkString(m.group(2))


def read_engine_root(project_dir: str) -> str:
  """Absolute engine root named by <project_dir>/application.blk."""
  ref = read_engine_ref(project_dir)
  root = norm(os.path.join(project_dir, ref))
  if not is_engine_root(root):
    raise ProjectError('{}: engineRoot "{}" is not a Dagor Engine checkout (no {} in it); fix it with "python <engine>/dng.py relink <project dir>"'
                       .format(os.path.join(project_dir, APPLICATION_BLK), ref, 'prog/cmake/DagorConfig.cmake'))
  return root


def relative_or_absolute(path: str, start: str, absolute=False) -> str:
  """path relative to start, or absolute when asked to or when they are on different drives."""
  path = norm(path)
  if absolute:
    return path
  try:
    return os.path.relpath(path, norm(start)).replace('\\', '/')
  except ValueError:  # different drives on Windows
    return path


def write_engine_root(project_dir: str, engine_root: str, absolute=False):
  """sets engineRoot in <project_dir>/application.blk (in place, or as its first line), keeping the rest of the file"""
  if not is_engine_root(engine_root):
    raise ProjectError('{} is not a Dagor Engine checkout (no prog/cmake/DagorConfig.cmake in it)'.format(engine_root))
  value = escapeBlkString(relative_or_absolute(engine_root, project_dir, absolute))
  fn = os.path.join(project_dir, APPLICATION_BLK)
  try:
    with open(fn, 'r', encoding='utf-8') as f:
      text = f.read()
  except FileNotFoundError:
    text = ''
  if _ENGINE_ROOT_RE.search(text):
    text = _ENGINE_ROOT_RE.sub(lambda m: '{}"{}"'.format(m.group(1), value), text, count=1)
  else:
    text = '{}\nengineRoot:t="{}"\n\n{}'.format(_ENGINE_ROOT_COMMENT, value, text)
  with open(fn, 'w', encoding='utf-8', newline='\n') as f:
    f.write(text)
