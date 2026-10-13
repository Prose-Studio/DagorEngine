"""The CMakePresets.json of a game project (<project>/prog/CMakePresets.json): its trees on the engine's preset bases
(<engine>/prog/cmake/presets/base.json), which it includes by a path relative to it; dng.py new writes it for a new
project, and python -m pythonCommon.dagorProject.presets <project> rewrites it (after the engine moved, say)."""
import json
import os
import sys

from .engine import ProjectError

HOSTS = ('windows', 'linux', 'macos')


def project_presets(engine_prog: str, multiplayer: bool) -> dict:
  """the presets of a project whose prog dir reaches the engine's prog dir at <engine_prog> (relative to it, or
  absolute on another drive); a multiplayer game has a dedicated server's tree besides the client's"""
  engine_root = (engine_prog if os.path.isabs(engine_prog) else '${sourceDir}/' + engine_prog) + '/..'
  configure = [{
    'name': 'project', 'hidden': True,
    '$comment': 'the engine this project is built with (DAGOR_ENGINE_ROOT; dng.py new writes the path)',
    'environment': {'DAGOR_ENGINE_ROOT': engine_root},
    'cacheVariables': {'DAGOR_VARIANT': 'game', 'DAGOR_DAS_AOT': 'ON'},
  }, {
    'name': 'aot-compiler', 'hidden': True,
    '$comment': "the game's daScript AOT compiler, a host program the other trees build and run",
    'cacheVariables': {'DAGOR_DAS_AOT': 'OFF', 'DAGOR_DAS_AOT_COMPILER': 'ON'},
  }]
  kinds = ['client', 'aot-compiler']
  if multiplayer:
    configure.insert(1, {'name': 'dedicated', 'hidden': True, 'cacheVariables': {'DAGOR_DEDICATED': 'ON'}})
    kinds.insert(1, 'dedicated')
  shipped = [k for k in kinds if k != 'aot-compiler']
  tested = 'dedicated' if multiplayer else 'client'  # where the tests that need no GPU run
  build, test, package, workflow = [], [], [], []
  for host in HOSTS:
    for kind in kinds:
      name = '{}-{}'.format(host, kind)
      # the first preset inherited wins: the kind's settings over the project's
      preset = {'name': name, 'inherits': ([kind] if kind != 'client' else []) + ['project', 'toolchain-' + host]}
      if kind == 'client' and multiplayer:  # its target dedicated builds the dedicated server's tree
        preset['cacheVariables'] = {'DAGOR_DEDICATED_PRESET': host + '-dedicated'}
      configure.append(preset)
      build.append({'name': name, 'configurePreset': name, 'configuration': 'Dev'})
    client = host + '-client'
    build.append({'name': client + '-content', 'configurePreset': client, 'configuration': 'Dev', 'targets': ['content']})
    # everything: the game, its content and the dedicated server (cmake --workflow --preset <host>)
    build.append({'name': host, 'configurePreset': client, 'configuration': 'Dev',
                  'targets': ['all', 'content'] + (['dedicated'] if multiplayer else [])})
    workflow.append({'name': host, 'steps': [{'type': 'configure', 'name': client}, {'type': 'build', 'name': host}]})
    for kind in shipped:
      name = '{}-{}'.format(host, kind)
      test.append({'name': name, 'configurePreset': name, 'inherits': 'dagor'})
      if kind == tested:
        test.append({'name': name + '-ci', 'configurePreset': name, 'inherits': 'dagor-ci'})
      build.append({'name': name + '-rel', 'configurePreset': name, 'configuration': 'Rel'})
      package.append({'name': name, 'configurePreset': name, 'configurations': ['Rel']})
      workflow.append({'name': name + '-package', 'steps': [
        {'type': 'configure', 'name': name}, {'type': 'build', 'name': name + '-rel'},
        {'type': 'package', 'name': name}]})
    name = '{}-{}'.format(host, tested)
    # a client runs its tests on its content: the build of everything; a dedicated server on its sources
    workflow.append({'name': host + '-test', 'steps': [
      {'type': 'configure', 'name': name}, {'type': 'build', 'name': host if tested == 'client' else name},
      {'type': 'test', 'name': name + '-ci'}]})
  trees = ('<host>-client and <host>-dedicated build the game and its dedicated server' if multiplayer else
           '<host>-client builds the game')
  return {
    'version': 10,
    'cmakeMinimumRequired': {'major': 4, 'minor': 0, 'patch': 0},
    '$comment': [
      "cmake --workflow --preset <host> (windows, linux, macos) builds everything: the game{}, its".format(
        ', its dedicated server' if multiplayer else ''),
      "content and the engine tools it needs. The trees (cmake --list-presets): {} into ../game,".format(trees),
      "the client's tree its content too (cmake --build --preset <host>-client-content). Workflows: <host>-test (the",
      "build and the tests that need no GPU), <host>-<tree>-package. Written by dng.py new and relink; local presets go",
      "in CMakeUserPresets.json."
    ],
    'include': [engine_prog + '/cmake/presets/base.json'],
    'configurePresets': configure, 'buildPresets': build, 'testPresets': test, 'packagePresets': package,
    'workflowPresets': workflow,
  }


def is_multiplayer(project_dir: str) -> bool:
  """whether the project's presets have a dedicated server's tree"""
  fn = os.path.join(project_dir, 'prog', 'CMakePresets.json')
  try:
    with open(fn, 'r', encoding='utf-8') as f:
      return any(p.get('name') == 'dedicated' for p in json.load(f).get('configurePresets', []))
  except (OSError, ValueError) as e:
    raise ProjectError('cannot read {}: {}'.format(fn, e))


def engine_prog_path(project_dir: str, engine_root: str) -> str:
  """the engine's prog dir relative to <project_dir>/prog (absolute across drives)"""
  prog = os.path.join(project_dir, 'prog')
  try:
    return os.path.relpath(os.path.join(engine_root, 'prog'), prog).replace('\\', '/')
  except ValueError:  # another drive on Windows
    return os.path.abspath(os.path.join(engine_root, 'prog')).replace('\\', '/')


def write(project_dir: str, engine_root: str, multiplayer=None) -> str:
  """writes <project_dir>/prog/CMakePresets.json (multiplayer: with a dedicated server's tree, by default as the
  presets there have); returns its path"""
  if multiplayer is None:
    multiplayer = is_multiplayer(project_dir)
  fn = os.path.join(project_dir, 'prog', 'CMakePresets.json')
  with open(fn, 'w', encoding='utf-8', newline='\n') as f:
    f.write(json.dumps(project_presets(engine_prog_path(project_dir, engine_root), multiplayer), indent=2) + '\n')
  return fn


if __name__ == '__main__':
  from .engine import read_engine_root
  project = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else '.')
  print(write(project, read_engine_root(project)))
