#!/usr/bin/env python3
"""Build CPack fixtures and verify installed game launchers, arguments and exit status."""
import os
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile
import zipfile


def check_package(cmake, root, apple=False, dedicated=False, windows=False):
  module = (Path(__file__).resolve().parents[1] / 'DagorPackaging.cmake').as_posix()
  arch = 'arm64' if apple and os.uname().machine == 'arm64' else 'x86_64'
  source = root / 'prog'
  source.mkdir(parents=True)
  declaration = '''add_executable(game IMPORTED)
set_target_properties(game PROPERTIES IMPORTED_LOCATION "${CMAKE_CURRENT_SOURCE_DIR}/game")
'''
  bootstrap = ''
  if windows:
    bootstrap = 'include("' + Path(module).with_name('DagorBootstrap.cmake').as_posix() + '")\n'
    declaration = '''add_executable(game main.c)
file(GENERATE OUTPUT "$<TARGET_FILE_DIR:game>/LICENSE-game" CONTENT "fixture license\\n")
'''
  if apple:
    declaration = '''add_executable(game main.c)
set(DAGOR_CMAKE_DIR "''' + Path(module).parent.as_posix() + '''")
dagor_apple_bundle(game NAME Fixture ID com.dagor.fixture DIR ../game)
file(GENERATE OUTPUT "${CMAKE_CURRENT_SOURCE_DIR}/../game/Fixture.app/Contents/Resources/LICENSE-game"
  CONTENT "fixture license\\n")
'''
  if apple or windows:
    (source / 'main.c').write_text('''#include <stdio.h>
#include <string.h>
#ifdef _WIN32
#include <direct.h>
#define getcwd _getcwd
#else
#include <unistd.h>
#endif
int main(int argc, char **argv) {
  char cwd[4096];
  if (!getcwd(cwd, sizeof(cwd))) return 1;
  FILE *out = fopen("result.txt", "w");
  if (!out) return 1;
  fprintf(out, "%s\\n", cwd);
  for (int i = 1; i < argc; ++i) fprintf(out, "%s\\n", argv[i]);
  if (fclose(out) != 0) return 1;
  return argc > 1 && strcmp(argv[argc - 1], "fail") == 0 ? 7 : 0;
}
''', encoding='utf-8')
  (source / 'CMakeLists.txt').write_text('''cmake_minimum_required(VERSION 4.0)
''' + bootstrap + '''project(package_fixture LANGUAGES ''' + ('C' if apple or windows else 'NONE') + ''')
include("''' + module + '''")
function(_dagor_abs_paths output path)
  cmake_path(ABSOLUTE_PATH path BASE_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}" NORMALIZE)
  set(${output} "${path}" PARENT_SCOPE)
endfunction()
set(DAGOR_PLATFORM ''' + ('macOS' if apple else 'windows' if windows else 'linux') + ''')
set(DAGOR_ARCH ''' + arch + ''')
set(DAGOR_DEDICATED ''' + ('ON' if dedicated else 'OFF') + ''')
''' + declaration + '''
dagor_package_game(game GAME_DIR . NAME fixture DATA content data.bin ARGS -forcestart)
_dagor_package()
''', encoding='utf-8')
  (source / 'game').write_text('''#!/bin/sh
printf '%s\\n' "$PWD" "$@" > result.txt
for argument do last="$argument"; done
[ "$last" = fail ] && exit 7
exit 0
''', encoding='utf-8')
  (source / 'LICENSE-game').write_text('fixture license\n', encoding='utf-8')
  (source / 'data.bin').write_bytes(b'game data\0')
  (source / 'content').mkdir()
  (source / 'content' / 'asset.bin').write_bytes(b'asset data\0')
  build = root / 'build' / 'fixture'
  configure = [cmake, '-S', str(source), '-B', str(build)]
  if windows:
    configure += ['-G', 'Ninja Multi-Config']
  subprocess.run(configure, check=True)
  # The package target uses the CPack from the same CMake installation.
  build_command = [cmake, '--build', str(build), '--target', 'package']
  if windows:
    build_command += ['--config', 'Dev']
  subprocess.run(build_command, check=True)
  archive, = (root / 'build' / 'packages').glob('*.zip' if windows else '*.tar.gz')
  extracted = root / 'installed game with spaces'
  if windows:
    with zipfile.ZipFile(archive) as package:
      package.extractall(extracted)
  else:
    with tarfile.open(archive) as package:
      package.extractall(extracted, **({'filter': 'data'} if sys.version_info >= (3, 12) else {}))
  platform = 'macOS' if apple else 'windows' if windows else 'linux'
  installed = extracted / ('package_fixture' + ('-dedicated' if dedicated else '') + '-' + platform + '-' + arch)
  launcher = installed / (('fixture-server' if dedicated else 'fixture') + ('.cmd' if windows else '.sh'))
  assert (installed / 'data.bin').read_bytes() == b'game data\0'
  assert (installed / 'content' / 'asset.bin').read_bytes() == b'asset data\0'
  license_dir = 'Fixture.app/Contents/Resources' if apple else platform + '-' + arch
  assert (installed / license_dir / 'LICENSE-game').read_text() == 'fixture license\n'
  if apple:
    subprocess.run(['codesign', '--verify', '--deep', '--strict', str(installed / 'Fixture.app')], check=True)
  if os.name != 'nt' or windows:
    command = ['cmd.exe', '/d', '/c', 'call', str(launcher)] if windows else [str(launcher)]
    if not windows:
      subprocess.run(['sh', '-n', str(launcher)], check=True)
    # Invoke from a different working directory; the launcher must locate the game and its data itself.
    subprocess.run(command + ['argument with spaces', '*', ''], cwd=root, check=True)
    result = (installed / 'result.txt').read_text().splitlines()
    # getcwd can resolve the macOS /var -> /private/var symlink while sh preserves it.
    assert Path(result[0]).samefile(installed), result
    assert result[1:] == ['-forcestart', 'argument with spaces', '*', ''], result
    assert subprocess.run(command + ['fail'], cwd=root).returncode == 7
  print('CPack game data, license and launcher verified')


def main():
  cmake = sys.argv[1]
  with tempfile.TemporaryDirectory(prefix='dagor package ') as tmp:
    root = Path(tmp)
    check_package(cmake, root / 'client')
    check_package(cmake, root / 'dedicated', dedicated=True)
    if sys.platform == 'darwin':
      check_package(cmake, root / 'apple', apple=True)
    if os.name == 'nt':
      check_package(cmake, root / 'windows', windows=True, dedicated=True)
  return 0


if __name__ == '__main__':
  sys.exit(main())
