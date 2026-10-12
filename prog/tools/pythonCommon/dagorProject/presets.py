"""The CMakePresets.json of a game project (<project>/prog/CMakePresets.json): its trees on the engine's preset bases
(<engine>/prog/cmake/presets/base.json), which it includes by a path relative to it; dng.py new writes it for a new
project, and python -m pythonCommon.dagorProject.presets <project> rewrites it (after the engine moved, say)."""
import json
import os
import sys

HOSTS = ('windows', 'linux', 'macos')


def project_presets(engine_prog: str) -> dict:
  """the presets of a project whose prog dir reaches the engine's prog dir at <engine_prog> (a relative path)"""
  configure = [{
    'name': 'project', 'hidden': True,
    '$comment': 'the engine this project is built with (DAGOR_ENGINE_ROOT; dng.py new writes the path)',
    'environment': {'DAGOR_ENGINE_ROOT': '${sourceDir}/' + engine_prog + '/..'},
    'cacheVariables': {'DAGOR_VARIANT': 'game', 'DAGOR_DAS_AOT': 'ON'},
  }, {
    'name': 'dedicated', 'hidden': True, 'cacheVariables': {'DAGOR_DEDICATED': 'ON'},
  }, {
    'name': 'aot-compiler', 'hidden': True,
    '$comment': "the game's daScript AOT compiler, a host program the other trees build and run",
    'cacheVariables': {'DAGOR_DAS_AOT': 'OFF', 'DAGOR_DAS_AOT_COMPILER': 'ON'},
  }]
  build, test, package, workflow = [], [], [], []
  for host in HOSTS:
    for kind in ('client', 'dedicated', 'aot-compiler'):
      name = '{}-{}'.format(host, kind)
      # the first preset inherited wins: the kind's settings over the project's
      configure.append({'name': name, 'inherits': ([kind] if kind != 'client' else []) + ['project', host]})
      build.append({'name': name, 'configurePreset': name, 'configuration': 'Dev'})
    client, dedicated = host + '-client', host + '-dedicated'
    build.append({'name': client + '-content', 'configurePreset': client, 'configuration': 'Dev', 'targets': ['content']})
    test.append({'name': dedicated, 'configurePreset': dedicated, 'inherits': 'dagor'})
    test.append({'name': dedicated + '-ci', 'configurePreset': dedicated, 'inherits': 'dagor-ci'})
    test.append({'name': client, 'configurePreset': client, 'inherits': 'dagor'})
    workflow.append({'name': dedicated + '-test', 'steps': [
      {'type': 'configure', 'name': dedicated}, {'type': 'build', 'name': dedicated},
      {'type': 'test', 'name': dedicated + '-ci'}]})
    for name in (client, dedicated):
      build.append({'name': name + '-rel', 'configurePreset': name, 'configuration': 'Rel'})
      package.append({'name': name, 'configurePreset': name, 'configurations': ['Rel']})
      workflow.append({'name': name + '-package', 'steps': [
        {'type': 'configure', 'name': name}, {'type': 'build', 'name': name + '-rel'},
        {'type': 'package', 'name': name}]})
  return {
    'version': 10,
    'cmakeMinimumRequired': {'major': 4, 'minor': 0, 'patch': 0},
    '$comment': [
      "The game's trees (cmake --list-presets): <host>-client and <host>-dedicated build the game into ../game, the",
      "client's tree its content too (cmake --build --preset <host>-client-content). Workflows: <host>-dedicated-test",
      "(the tests that need no GPU), <host>-client-package and <host>-dedicated-package. Local presets go in",
      "CMakeUserPresets.json."
    ],
    'include': [engine_prog + '/cmake/presets/base.json'],
    'configurePresets': configure, 'buildPresets': build, 'testPresets': test, 'packagePresets': package,
    'workflowPresets': workflow,
  }


def engine_prog_path(project_dir: str, engine_root: str) -> str:
  """the engine's prog dir relative to <project_dir>/prog (absolute across drives)"""
  prog = os.path.join(project_dir, 'prog')
  try:
    return os.path.relpath(os.path.join(engine_root, 'prog'), prog).replace('\\', '/')
  except ValueError:  # another drive on Windows
    return os.path.abspath(os.path.join(engine_root, 'prog')).replace('\\', '/')


def write(project_dir: str, engine_root: str) -> str:
  """writes <project_dir>/prog/CMakePresets.json; returns its path"""
  fn = os.path.join(project_dir, 'prog', 'CMakePresets.json')
  with open(fn, 'w', encoding='utf-8', newline='\n') as f:
    f.write(json.dumps(project_presets(engine_prog_path(project_dir, engine_root)), indent=2) + '\n')
  return fn


if __name__ == '__main__':
  from .engine import read_engine_root
  project = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else '.')
  print(write(project, read_engine_root(project)))
