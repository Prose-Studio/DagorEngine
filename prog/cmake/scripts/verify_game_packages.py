#!/usr/bin/env python3
"""Inspect project.py's client/server packages and run the packaged server's ECS tests (CI)."""
import json
import os
from pathlib import Path
import signal
import shutil
import subprocess
import sys
import tarfile
import tempfile
import zipfile


def run(command, cwd):
  process = subprocess.Popen(command, cwd=cwd, start_new_session=os.name != 'nt')
  try:
    code = process.wait(timeout=300)
  except subprocess.TimeoutExpired:
    if os.name == 'nt':
      subprocess.run(['taskkill', '/PID', str(process.pid), '/T', '/F'], check=False)
    else:
      os.killpg(process.pid, signal.SIGKILL)
    process.wait()
    raise
  if code:
    raise subprocess.CalledProcessError(code, command)


def main(argv):
  project = Path(argv[0]).resolve()
  packages = project / 'build' / 'packages'
  archives = sorted(list(packages.glob('*.zip')) + list(packages.glob('*.tar.gz')))
  if len(archives) != 2 or sum('-dedicated-' in p.name for p in archives) != 1:
    raise RuntimeError('expected client and dedicated archives in {}'.format(packages))
  wrapper = Path(__file__).with_name('run_game_test.py').resolve()
  for archive in archives:
    dedicated = '-dedicated-' in archive.name
    with tempfile.TemporaryDirectory(prefix='package verification ', dir=project / 'build') as tmp:
      extracted = Path(tmp).resolve()
      extracted.relative_to(project / 'build')
      if archive.suffix == '.zip':
        with zipfile.ZipFile(archive) as package:
          package.extractall(extracted)
      else:
        with tarfile.open(archive) as package:
          package.extractall(extracted, **({'filter': 'data'} if sys.version_info >= (3, 12) else {}))
      root, = extracted.iterdir()
      if not (root / 'content').is_dir() or not any(root.glob('*.vromfs.bin')):
        raise RuntimeError('package data missing: {}'.format(archive))
      if not dedicated and not any((root / 'compiledShaders').glob('*.shdump.bin')):
        raise RuntimeError('client shader dumps missing: {}'.format(archive))
      suffix = '.cmd' if os.name == 'nt' else '.sh'
      launcher, = root.glob('*' + suffix)
      if os.name != 'nt':
        subprocess.run(['sh', '-n', str(launcher)], check=True)
        if not os.access(launcher, os.X_OK):
          raise RuntimeError('launcher is not executable: {}'.format(launcher))
      if sys.platform == 'darwin' and not dedicated:
        bundle, = root.glob('*.app')
        subprocess.run(['codesign', '--verify', '--deep', '--strict', str(bundle)], check=True)
      if dedicated:
        # Test support is intentionally absent from production archives. Supply only
        # these helpers; the game's scripts, standard library and data stay packed.
        engine = Path(__file__).resolve().parents[3]
        shutil.copytree(engine / 'prog' / '1stPartyLibs' / 'daScript' / 'dastest', root / 'dastest')
        shutil.copytree(engine / 'prog' / 'daNetGameLibs' / 'test_harness', root / 'danetlibs' / 'test_harness')
        out = project / 'build' / 'package-checks' / 'ecs'
        command = ['cmd.exe', '/d', '/c', launcher.name] if os.name == 'nt' else [str(launcher)]
        command += ['-stdout', '-quiet', '-nolisten', '-nostatsd', '-nonetenc', '-nopeerauth',
                    '-config:debug/useAddonVromSrc:b=no', '-config:debug/daScriptHotReload:b=no',
                    '-das_test:' + str(project / 'prog' / 'tests' / 'ecs'), '-test_timeout:120',
                    '-test_out:' + str(out)]
        run([sys.executable, str(wrapper), str(out)] + command, cwd=root)
        with (out / 'dastest.json').open(encoding='utf-8') as report:
          tests = json.load(report).get('tests', [])
        if not tests or any(not t.get('passed') or t.get('skipped') for t in tests):
          raise RuntimeError('packaged dedicated server did not pass its ECS tests')
      print('verified {}'.format(archive.name), flush=True)
  return 0


if __name__ == '__main__':
  sys.exit(main(sys.argv[1:]))
