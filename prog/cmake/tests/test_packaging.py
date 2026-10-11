#!/usr/bin/env python3
"""Build a small CPack game package and run its installed shell launcher on Unix hosts."""
import os
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile


def check_package(cmake, root, apple=False, dedicated=False):
  module = (Path(__file__).resolve().parents[1] / 'DagorPackaging.cmake').as_posix()
  arch = 'arm64' if apple and os.uname().machine == 'arm64' else 'x86_64'
  source = root / 'prog'
  source.mkdir(parents=True)
  declaration = '''add_executable(game IMPORTED)
set_target_properties(game PROPERTIES IMPORTED_LOCATION "${CMAKE_CURRENT_SOURCE_DIR}/game")
'''
  if apple:
    declaration = '''add_executable(game main.c)
set(DAGOR_CMAKE_DIR "''' + Path(module).parent.as_posix() + '''")
dagor_apple_bundle(game NAME Fixture ID com.dagor.fixture DIR ../game)
file(GENERATE OUTPUT "${CMAKE_CURRENT_SOURCE_DIR}/../game/Fixture.app/Contents/Resources/LICENSE-game"
  CONTENT "fixture license\\n")
'''
    (source / 'main.c').write_text('''#include <stdio.h>
#include <unistd.h>
int main(int argc, char **argv) {
  char cwd[4096];
  if (!getcwd(cwd, sizeof(cwd))) return 1;
  FILE *out = fopen("result.txt", "w");
  if (!out) return 1;
  fprintf(out, "%s\\n", cwd);
  for (int i = 1; i < argc; ++i) fprintf(out, "%s\\n", argv[i]);
  return fclose(out) != 0;
}
''', encoding='utf-8')
  (source / 'CMakeLists.txt').write_text('''cmake_minimum_required(VERSION 4.0)
project(package_fixture LANGUAGES ''' + ('C' if apple else 'NONE') + ''')
include("''' + module + '''")
function(_dagor_abs_paths output path)
  cmake_path(ABSOLUTE_PATH path BASE_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}" NORMALIZE)
  set(${output} "${path}" PARENT_SCOPE)
endfunction()
set(DAGOR_PLATFORM ''' + ('macOS' if apple else 'linux') + ''')
set(DAGOR_ARCH ''' + arch + ''')
set(DAGOR_DEDICATED ''' + ('ON' if dedicated else 'OFF') + ''')
''' + declaration + '''
dagor_package_game(game GAME_DIR . NAME fixture DATA content data.bin ARGS -forcestart)
_dagor_package()
''', encoding='utf-8')
  (source / 'game').write_text('''#!/bin/sh
printf '%s\\n' "$PWD" "$@" > result.txt
''', encoding='utf-8')
  (source / 'LICENSE-game').write_text('fixture license\n', encoding='utf-8')
  (source / 'data.bin').write_bytes(b'game data\0')
  (source / 'content').mkdir()
  (source / 'content' / 'asset.bin').write_bytes(b'asset data\0')
  build = root / 'build' / 'fixture'
  subprocess.run([cmake, '-S', str(source), '-B', str(build)], check=True)
  # The package target uses the CPack from the same CMake installation.
  subprocess.run([cmake, '--build', str(build), '--target', 'package'], check=True)
  archive, = (root / 'build' / 'packages').glob('*.tar.gz')
  extracted = root / 'installed game with spaces'
  with tarfile.open(archive) as package:
    package.extractall(extracted, **({'filter': 'data'} if sys.version_info >= (3, 12) else {}))
  platform = 'macOS' if apple else 'linux'
  installed = extracted / ('package_fixture' + ('-dedicated' if dedicated else '') + '-' + platform + '-' + arch)
  launcher = installed / ('fixture-server.sh' if dedicated else 'fixture.sh')
  assert (installed / 'data.bin').read_bytes() == b'game data\0'
  assert (installed / 'content' / 'asset.bin').read_bytes() == b'asset data\0'
  license_dir = 'Fixture.app/Contents/Resources' if apple else 'linux-x86_64'
  assert (installed / license_dir / 'LICENSE-game').read_text() == 'fixture license\n'
  if apple:
    subprocess.run(['codesign', '--verify', '--deep', '--strict', str(installed / 'Fixture.app')], check=True)
  if os.name != 'nt':
    subprocess.run(['sh', '-n', str(launcher)], check=True)
    # Invoke from a different working directory; the launcher must locate the game and its data itself.
    subprocess.run([str(launcher), 'argument with spaces', '*', ''], cwd=root, check=True)
    result = (installed / 'result.txt').read_text().splitlines()
    assert result == [str(installed), '-forcestart', 'argument with spaces', '*', ''], result
  print('CPack game data, license and launcher verified')


def main():
  cmake = sys.argv[1]
  with tempfile.TemporaryDirectory(prefix='dagor package ') as tmp:
    root = Path(tmp)
    check_package(cmake, root / 'client')
    check_package(cmake, root / 'dedicated', dedicated=True)
    if sys.platform == 'darwin':
      check_package(cmake, root / 'apple', apple=True)
  return 0


if __name__ == '__main__':
  sys.exit(main())
