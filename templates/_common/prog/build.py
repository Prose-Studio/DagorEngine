#!/usr/bin/env python3
# Builds the game with the engine that ../application.blk names (engineRoot:t=), whose tools must be built
# (python <engine>/dagor.py build project:dagorTools code):
#   python build.py [code] [shaders] [gui] [vromfs] [assets] [arch:<arch>] [--dry-run]     (all when none is named)
# code     the game (and its dedicated server, when dedicated.jam exists) into ../game/<platform>-<arch>
# shaders  the game's shaders into ../game/compiledShaders, those of the tools into ../tools
# gui      the UI fonts (gameBase/ui/fontgen.blk)
# vromfs   the game's scripts and data into ../game/starter_game.vromfs.bin, and the editor's snapshot of them (../tools)
# assets   develop/assets into the game's packs (../game/content)
# It writes the project's _* files first (dagor.py setup_project): the engine's path and the libs of *libs.txt.
import os
import re
import sys
import glob

PROG_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = os.path.dirname(PROG_DIR)

with open(os.path.join(PROJECT_DIR, 'application.blk'), encoding='utf-8') as f:
  engine_root = re.search(r'^[ \t]*engineRoot[ \t]*:[ \t]*t[ \t]*=[ \t]*"([^"]*)"', f.read(), re.MULTILINE)
if not engine_root or not engine_root.group(1):
  print('\nERROR: ../application.blk names no engine: python <engine>/dagor.py relink {0}\n'.format(PROJECT_DIR))
  exit(1)
ENGINE_DIR = os.path.normpath(os.path.join(PROJECT_DIR, engine_root.group(1).replace('~~', '~')))
sys.path.append(ENGINE_DIR)
from dagor import run, run_per_platform, setup_project, BUILD_COMPONENTS, JAM_BUILD_TARGET_ARCH_OPTIONS, DAGOR_HOST, \
  DAGOR_TOOLS_FOLDER, VROMFS_PACKER_EXE, DABUILD_CMD, FONTGEN_EXE, DRY_RUN
sys.path.pop()

setup_project(PROJECT_DIR)
MULTIPLAYER = os.path.isfile(os.path.join(PROG_DIR, 'dedicated.jam'))
BUILD_DIR = os.path.join(PROJECT_DIR, 'build')


def cdk_tool(name):
  return os.path.join(DAGOR_TOOLS_FOLDER, name + '-dev' + ('.exe' if DAGOR_HOST == 'windows' else ''))


def step(ok):
  if not ok:
    exit(1)


if 'code' in BUILD_COMPONENTS:
  step(run(['jam', '-f', 'jamfile-aot'], cwd=PROG_DIR))
  step(run(['jam', '-sNeedDasAotCompile=yes'] + JAM_BUILD_TARGET_ARCH_OPTIONS, cwd=PROG_DIR))
  if MULTIPLAYER:
    step(run(['jam', '-sDedicated=yes', '-sNeedDasAotCompile=yes'] + JAM_BUILD_TARGET_ARCH_OPTIONS, cwd=PROG_DIR))

if 'shaders' in BUILD_COMPONENTS:
  # each: name, shader compiler, its shader list (in shaders/), its arguments; game_common.blk explains the paths
  dsc = ['-q', '-shaderOn', '-nodisassembly', '-commentPP', '-codeDumpErr', '-maxVSF', '4096']
  exp = ['-q', '-shaderOn', '-no_sha1_cache', '-clearBlkHashInDump'] # dabuild only needs the shader descriptions
  if DAGOR_HOST == 'windows':
    shaders = [('game-dx11', 'dsc2-hlsl11', 'shaders_dx11.blk', dsc), ('game-dx12', 'dsc2-dx12', 'shaders_dx12.blk', dsc + ['-wx']),
               ('tools-dx11', 'dsc2-hlsl11', 'shaders_tools11.blk', dsc),
               ('impostorbaker-dx12', 'dsc2-dx12', 'shaders_impostorbaker.blk', dsc)]
  elif DAGOR_HOST == 'macOS':
    shaders = [('game-metal', 'dsc2-metal', 'shaders_metal.blk', dsc),
               ('tools-metal', 'dsc2-metal', 'shaders_tools11.blk', dsc + ['-out', '../../tools/toolsMTL']),
               ('impostorbaker-metal', 'dsc2-metal', 'shaders_impostorbaker.blk', dsc + ['-out', '../../tools/tools.impostorbakerMTL'])]
  else:
    shaders = [('game-spirv', 'dsc2-spirv', 'shaders_spirv.blk', dsc),
               ('tools-spirv', 'dsc2-spirv', 'shaders_tools11.blk', dsc + ['-out', '../../tools/toolsSpirV']),
               ('impostorbaker-spirv', 'dsc2-spirv', 'shaders_impostorbaker.blk', dsc + ['-out', '../../tools/tools.impostorbakerSpirV'])]
  shaders.append(('tools-exp', 'dsc2-stub', 'shaders_tools_exp.blk', exp))
  for name, compiler, blk, args in shaders:
    work = os.path.join(BUILD_DIR, 'shaders', name)
    step(run([cdk_tool(compiler), blk] + args + ['-o', work, '-logdir', os.path.join(work, 'log')],
             cwd=os.path.join(PROG_DIR, 'shaders')))

if 'gui' in BUILD_COMPONENTS:
  step(run([FONTGEN_EXE, 'fontgen.blk', '-fullDynamic', '-dbgfile:' + os.path.join(BUILD_DIR, 'fonts.log')],
           cwd=os.path.join(PROG_DIR, 'gameBase', 'ui')))

if 'vromfs' in BUILD_COMPONENTS:
  step(run([VROMFS_PACKER_EXE, 'prog.vromfs.blk', '-platform:PC', '-quiet', '-addpath:.'], cwd=PROG_DIR))
  # daEditor renders the game's levels with the game's shaders, vromfs and tools/ scripts, from ../tools/snapshot
  if DRY_RUN:
    print('DRY_RUN: the daEditor snapshot of {0}'.format(PROJECT_DIR))
  else:
    sys.path.append(os.path.join(ENGINE_DIR, 'prog', 'tools'))
    from update_dng_snapshots import update_dng_snapshot
    cwd = os.getcwd()
    update_dng_snapshot(PROJECT_DIR, 'game', glob.glob(os.path.join(PROJECT_DIR, 'game', '*.vromfs.bin')), skip_cvs_update=True)
    os.chdir(cwd)

if 'assets' in BUILD_COMPONENTS:
  step(run(DABUILD_CMD + ['../application.blk'], cwd=os.path.join(PROJECT_DIR, 'develop')))
