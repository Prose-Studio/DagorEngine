#!/usr/bin/env python3
# DagorEngine's script:
#   dagor.py devtools DEVTOOLS_DEST_DIR
#       downloads and sets up the build tools of this host (compilers, SDKs, jam) in DEVTOOLS_DEST_DIR and writes
#       prog/platform.jam
#   dagor.py build [project:<name>...] [code] [shaders] [assets] [vromfs] [gui] [arch:<arch>] [--dry-run]
#       builds the engine tools and projects (dagorTools, dargbox, physTest: all when none is named), the components
#       named (all when none is), after check-hosts
#   dagor.py new --name <Name> [--template <template>] [--dest <dir>] ... (--help, --list)
#       creates a game project from a template of templates/, anywhere on the engine's drive
#   dagor.py relink <project dir>
#       points a game project at this engine (after either moved)
#   dagor.py check-hosts
#       fails on Gaijin hosts, app IDs or release downloads in the engine (see check_hosts)
# A project's build.py imports it for the build helpers: run, run_per_platform, the tools' paths, the components and
# arch of the project's own command line, setup_project.
import sys

if not (sys.version_info.major >= 3 and sys.version_info.minor >= 7):
  print("\nERROR: Python 3.7 or a higher version is required to run this script.")
  exit(1)

import subprocess
import pathlib
import os
import platform
import multiprocessing
import re
import urllib
import ssl
import ctypes
import zipfile
import tarfile
import shutil
import glob
import filecmp
from urllib import request

COMMANDS = ['devtools', 'build', 'check-hosts', 'new', 'relink']

# the build's command line: that of the project's build.py, or that of dagor.py after the command
ARGS = sys.argv[1:]
if __name__ == '__main__' and ARGS[:1] and ARGS[0] in COMMANDS:
  ARGS = ARGS[1:]

DAGOR_ROOT_FOLDER = os.path.dirname(os.path.realpath(__file__))
DAGOR_HOST_ARCH = 'x86_64'

if sys.platform.startswith('win'):
  DAGOR_HOST = 'windows'
  if (os.environ.get('PROCESSOR_ARCHITECTURE', '') == 'ARM64' or
     ('ARMv' in os.environ.get('PROCESSOR_IDENTIFIER', '') and '64-bit' in os.environ.get('PROCESSOR_IDENTIFIER', ''))):
    DAGOR_HOST_ARCH = 'arm64'
  DAGOR_TOOLS_FOLDER = os.path.realpath('{0}/tools/dagor_cdk/windows-{1}'.format(DAGOR_ROOT_FOLDER, DAGOR_HOST_ARCH))
elif sys.platform.startswith('darwin'):
  DAGOR_HOST = 'macOS'
  DAGOR_TOOLS_FOLDER = os.path.realpath('{0}/tools/dagor_cdk/macOS-{1}'.format(DAGOR_ROOT_FOLDER, DAGOR_HOST_ARCH))
elif sys.platform.startswith('linux'):
  DAGOR_HOST = 'linux'
  DAGOR_HOST_ARCH = platform.uname().machine
  DAGOR_TOOLS_FOLDER = os.path.realpath('{0}/tools/dagor_cdk/linux-{1}'.format(DAGOR_ROOT_FOLDER, DAGOR_HOST_ARCH))
else:
  print('\nERROR: unsupported platform {0}\n'.format(sys.platform))
  exit(1)
VROMFS_PACKER_EXE = os.path.realpath('{0}/vromfsPacker-dev{1}'.format(DAGOR_TOOLS_FOLDER, '.exe' if DAGOR_HOST == 'windows' else ''))
DABUILD_EXE = os.path.realpath('{0}/daBuild-dev{1}'.format(DAGOR_TOOLS_FOLDER, '.exe' if DAGOR_HOST == 'windows' else ''))
DABUILD_CMD = [DABUILD_EXE, '-jobs:{}'.format(multiprocessing.cpu_count()), '-q']
FONTGEN_EXE = os.path.realpath('{0}/fontgen2-dev{1}'.format(DAGOR_TOOLS_FOLDER, '.exe' if DAGOR_HOST == 'windows' else ''))

# detect dry run
DRY_RUN = False

def is_s_dry_run(s):
  if s == '--dry-run' or s == '-dry-run':
    return True

for s in ARGS:
  if is_s_dry_run(s):
    DRY_RUN = True
    break

# gather build components from commandline (to allow partial builds)
BUILD_COMPONENTS = []
for s in ARGS:
  if not s.startswith('project:') and not s.startswith('arch:') and not is_s_dry_run(s):
    BUILD_COMPONENTS += [s]
# when no components specified we build all of them
if len(BUILD_COMPONENTS) == 0:
  BUILD_COMPONENTS = ['code', 'shaders', 'assets', 'vromfs', 'gui']

# get target architecture from commandline if any (and using default when none specified)
BUILD_TARGET_ARCH = ""
JAM_BUILD_TARGET_ARCH_OPTIONS = []
for s in ARGS:
  if s.startswith('arch:'):
    BUILD_TARGET_ARCH = s[5:]
    JAM_BUILD_TARGET_ARCH_OPTIONS = ['-sPlatformArch='+BUILD_TARGET_ARCH]
    break

def run(cmd, cwd='.'):
  if DRY_RUN:
    print(f"DRY_RUN: {cwd} > {cmd}")
    return True
  try:
    print('--- Running: {0}  in  {1}'.format(cmd, cwd)); sys.stdout.flush()
    subprocess.run(cmd, shell = True if type(cmd)==str else False, check = True, cwd = cwd)
    return True
  except subprocess.CalledProcessError as e:
    print('subprocess.run failed with a non-zero exit code. Error: {0}'.format(e))
    return False
  except OSError as e:
    print('An OSError occurred, subprocess.run command may have failed. Error: {0}'.format(e))
    return True

def run_per_platform(cmds_windows=[], cmds_macOS=[], cmds_linux=[], cwd='.'):
  for c in cmds_windows if DAGOR_HOST == 'windows' else cmds_macOS if DAGOR_HOST == 'macOS' else cmds_linux if DAGOR_HOST == 'linux' else []:
    if not run(c, cwd=cwd):
      return False
  return True



# --- devtools --------------------------------------------------------------------------------------------------------

# jam and the macOS build of DXC come from this repository's releases (copies of those of jam-G8 and DXC-prebuilt, with the
# same tags and file names); the other tools and SDKs come from their vendors
DEVTOOLS_RELEASES_URL = 'https://github.com/Prose-Studio/DagorEngine/releases/download'
JAM_RELEASE_URL = DEVTOOLS_RELEASES_URL + '/2.5-G8-1.3-2024%2F04%2F01'

def error(s):
  print("\nERROR: {0}\n".format(s))
  exit(1)

def ask(s):
  while True:
    answer = input("\n{0} [Y/n]: ".format(s)).strip().lower()
    if answer == "y" or answer == "y" or answer == "":
      return True
    if answer == "n" or answer == "no":
      return False

def contains_spaces(s):
  return ' ' in s

def contains_non_ascii(s):
  try:
    s.encode('ascii')
  except UnicodeEncodeError:
    return True
  return False

def make_directory_symlink(src, dest):
  try:
    if DAGOR_HOST == 'windows':
      subprocess.run(['cmd', '/C', 'mklink', '/J', os.path.normpath(dest), os.path.normpath(src)], shell = True, check = True)
    else:
      subprocess.run('ln -s {0} {1}'.format(os.path.normpath(src), os.path.normpath(dest)), shell = True, check = True)
  except subprocess.CalledProcessError as e:
    error("Symlink command failed with a non-zero exit code. Error: {0}, Source = '{1}', Destination = '{2}'".format(e, src, dest))
  except OSError as e:
    print("An OSError occurred. Symlink command may have failed. Error: {0}, Source = '{1}', Destination = '{2}'".format(e, src, dest))

def make_file_link(src, dest):
  os.link(src, dest)

def download_url2(url, file, dest_dir):
  file = "{0}/.packages/{1}".format(dest_dir, file)
  if not pathlib.Path(file).exists():
    print("Downloading '{0}' to '{1}' ...".format(url, file));
    response = request.urlretrieve(url, file)
  else:
    print("Package '{0}' already exists".format(file));

def download_url(url, dest_dir):
  path, file = os.path.split(os.path.normpath(url))
  download_url2(url, file, dest_dir)

def devtools(dest_dir):
  dest_dir = dest_dir.replace('\\', '/').rstrip('/')

  if contains_spaces(dest_dir):
    error("The destination directory contains spaces, which are not allowed in a file path.")

  if contains_non_ascii(dest_dir):
    error("The destination directory contains non-ASCII characters.")

  if not os.path.isabs(dest_dir):
    error("The destination directory must be an absolute path.")

  ssl._create_default_https_context = ssl._create_unverified_context

  pathlib.Path(dest_dir).mkdir(parents=True, exist_ok=True)
  pathlib.Path(dest_dir+'/.packages').mkdir(parents=True, exist_ok=True)

  {'windows': devtools_windows, 'linux': devtools_linux, 'macOS': devtools_macOS}[DAGOR_HOST](dest_dir)


def devtools_windows(dest_dir):
  # python3
  python_dest_folder = dest_dir+'/python3'
  python_src_folder = os.path.dirname(sys.executable)
  if not pathlib.Path(python_src_folder+'/python.exe').exists():
    python_src_folder = os.environ.get('LOCALAPPDATA', '') + '/Programs/Python'
  if pathlib.Path(python_src_folder).exists():
    if not pathlib.Path(python_src_folder+'/python.exe').exists():
      for item in pathlib.Path(python_src_folder).glob("Python3*"):
        if item.is_dir():
          if pathlib.Path(os.path.normpath(item)+'/python.exe').exists():
            python_src_folder = os.path.normpath(item)
            break
  else:
    python_src_folder = ''

  if pathlib.Path(python_dest_folder).exists():
    print('=== Python 3 symlink found at {0}, skipping setup'.format(python_dest_folder))
  else:
    if python_src_folder != '' and pathlib.Path(python_src_folder).exists():
      print('+++ Python 3 found at {0}'.format(python_src_folder))
      make_directory_symlink(python_src_folder, python_dest_folder)

      if not pathlib.Path(python_dest_folder+'/python3.exe').exists():
        make_file_link(python_dest_folder+'/python.exe', python_dest_folder+'/python3.exe')
    else:
      error("Python 3 not found")

  if 'WindowsApps' in python_src_folder:
    print('WARNING: Detected Microsoft Store Python. Skipping pip upgrade/install due to access restrictions.')
    print('Install official Python from python.org for full functionality.')
  else:
    subprocess.run([python_dest_folder+'/python.exe', '-m', 'pip', 'install', '--upgrade', 'pip'])
    subprocess.run([python_dest_folder+'/python.exe', '-m', 'pip', '--version'])
    subprocess.run([python_dest_folder+'/python.exe', '-m', 'pip', 'install', 'clang==14.0.6'])
    subprocess.run([python_dest_folder+'/python.exe', '-m', 'pip', 'install', 'cymbal'])

  microsoft_retry = []

  # vs140
  def setup_vs140(check_again_after_download):
    vc2015_dest_folder = dest_dir+'/vc2015.3'
    if pathlib.Path(vc2015_dest_folder).exists():
      print('=== VC2015 symlink found at {0}, skipping setup'.format(vc2015_dest_folder))
    else:
      vc2015_src_folder = os.environ.get('VS140COMNTOOLS', '')
      if vc2015_src_folder != '':
        vc2015_src_folder = os.path.normpath(vc2015_src_folder+'/../..')
      else:
        vc2015_src_folder = '{0}/Microsoft Visual Studio 14.0'.format(os.environ['ProgramFiles(x86)'])

      if vc2015_src_folder and pathlib.Path(vc2015_src_folder).exists():
        print('+++ VC2015 found at {0}'.format(vc2015_src_folder))
        make_directory_symlink(vc2015_src_folder+'/VC', vc2015_dest_folder)
      else:
        print('--- VC2015 not found (VS140COMNTOOLS env var is empty), install VisualStudio 2015 upd.3 and re-run setup')
        if not check_again_after_download:
          error("Visual Studio 2015 is required but not found at '{0}'".format(vc2015_src_folder))
        microsoft_retry.append(setup_vs140)

  #Visual Studio 2015 is turned off
  #setup_vs140(True)


  # vs142
  def setup_vs142(check_again_after_download):
    vs142_ver = "14.29"
    vc2019_dest_folder = dest_dir + '/vc2019_16.11.34'

    if pathlib.Path(vc2019_dest_folder).exists():
      real_path = ""
      try:
        real_path = os.path.realpath(vc2019_dest_folder)
      except OSError as e:
        pass

      if (not pathlib.Path(vc2019_dest_folder + '/bin/HostX64/x64/1033').exists() or
         (real_path.find("Microsoft") != -1 and real_path.find(vs142_ver) == -1)):
        print(vc2019_dest_folder+" contains invalid version of build tools.")
        print("...removing "+vc2019_dest_folder)
        try:
          os.remove(vc2019_dest_folder)
        except OSError as e:
          error("Cannot remove link {0}: {1}".format(vc2019_dest_folder, e))


    if pathlib.Path(vc2019_dest_folder).exists():
      print('=== VC2019 symlink found at {0}, skipping setup'.format(vc2019_dest_folder))
    else:
      ok = False
      vc2019_src_folder = '{0}/Microsoft Visual Studio'.format(os.environ['ProgramFiles(x86)'])
      if vc2019_src_folder and pathlib.Path(vc2019_src_folder).exists():
        for nm in ['/2022/BuildTools', '/2022/Community', '/2022/Enterprise', '/2022/Professional',
                   '/2019/BuildTools', '/2019/Community', '/2019/Enterprise', '/2019/Professional']:
          if pathlib.Path(vc2019_src_folder + nm + '/VC/Tools/MSVC').exists():
            versions_folder = vc2019_src_folder + nm + '/VC/Tools/MSVC'
            for item in pathlib.Path(versions_folder).glob(vs142_ver + ".*"):
              if item.is_dir():
                if pathlib.Path(os.path.normpath(item)+'/bin/HostX64/x64/1033').exists():
                  if pathlib.Path(os.path.normpath(item)+'/bin/HostX86/x86/1033').exists():
                    vc2019_src_folder = os.path.normpath(item)
                    ok = True
                    break

      if ok:
        print('+++ VC2019 found at {0}'.format(vc2019_src_folder))
        make_directory_symlink(vc2019_src_folder, vc2019_dest_folder)
      else:
        print('--- VC2019 not found, install VisualStudio 2019 16.11.34+ and re-run setup')
        if not check_again_after_download:
          error("Visual Studio 2019 is required but not found at '{0}'".format(vc2019_src_folder))
        microsoft_retry.append(setup_vs142)


  setup_vs142(True)


  def setup_vs143(check_again_after_download):
    vs143_ver = "14.44"
    vc2022_dest_folder = dest_dir + '/vc2022_17.14.4'

    if pathlib.Path(vc2022_dest_folder).exists():
      real_path = ""
      try:
        real_path = os.path.realpath(vc2022_dest_folder)
      except OSError as e:
        pass

      if (not pathlib.Path(vc2022_dest_folder + '/bin/HostX64/x64/1033').exists() or
         (real_path.find("Microsoft") != -1 and real_path.find(vs143_ver) == -1)):
        print(vc2022_dest_folder+" contains invalid version of build tools.")
        print("...removing "+vc2022_dest_folder)
        try:
          os.remove(vc2022_dest_folder)
        except OSError as e:
          error("Cannot remove link {0}: {1}".format(vc2022_dest_folder, e))


    if pathlib.Path(vc2022_dest_folder).exists():
      print('=== VC2022 symlink found at {0}, skipping setup'.format(vc2022_dest_folder))
    else:
      ok = False
      vc2022_src_folder = '{0}/Microsoft Visual Studio'.format(os.environ['ProgramFiles(x86)'])
      if vc2022_src_folder and pathlib.Path(vc2022_src_folder).exists():
        for nm in ['/2022/BuildTools', '/2022/Community', '/2022/Enterprise', '/2022/Professional']:
          if pathlib.Path(vc2022_src_folder + nm + '/VC/Tools/MSVC').exists():
            versions_folder = vc2022_src_folder + nm + '/VC/Tools/MSVC'
            for item in pathlib.Path(versions_folder).glob(vs143_ver + ".*"):
              if item.is_dir():
                if pathlib.Path(os.path.normpath(item)+'/bin/HostX64/x64/1033').exists():
                  if pathlib.Path(os.path.normpath(item)+'/bin/HostX86/x86/1033').exists():
                    vc2022_src_folder = os.path.normpath(item)
                    ok = True
                    break

      if ok:
        print('+++ VC2022 found at {0}'.format(vc2022_src_folder))
        make_directory_symlink(vc2022_src_folder, vc2022_dest_folder)
      else:
        print('--- VC2022 not found, install VisualStudio 2022 17.14.4+ and re-run setup')
        if not check_again_after_download:
          error("Visual Studio 2022 is required but not found at '{0}'".format(vc2022_src_folder))
        microsoft_retry.append(setup_vs143)


  setup_vs143(True)


  # Microsoft Windows 10 SDK
  def setup_winsdk_100(check_again_after_download):
    winsdk_dest_folder = dest_dir+'/win.sdk.100'
    if pathlib.Path(winsdk_dest_folder).exists():
      print('=== Windows 10 SDK symlink found at {0}, skipping setup'.format(winsdk_dest_folder))
    else:
      winsdk_src_folder = '{0}/Windows Kits/10'.format(os.environ['ProgramFiles(x86)'])
      if pathlib.Path(winsdk_src_folder+'/include/10.0.19041.0').exists():
        print('+++ Windows 10 SDK found at {0}'.format(winsdk_src_folder))
        make_directory_symlink(winsdk_src_folder, winsdk_dest_folder)
      else:
        print('--- Windows 10 SDK not found, install Windows SDK and re-run setup')
        if not check_again_after_download:
          error("Windows 10 SDK is required but not found at '{0}'".format(winsdk_src_folder))
        microsoft_retry.append(setup_winsdk_100)

  setup_winsdk_100(True)


  # Microsoft Windows 8.1 SDK
  def setup_winsdk_81(check_again_after_download):
    winsdk_dest_folder = dest_dir+'/win.sdk.81'
    if pathlib.Path(winsdk_dest_folder).exists():
      print('=== Windows 8.1 SDK symlink found at {0}, skipping setup'.format(winsdk_dest_folder))
    else:
      winsdk_src_folder = '{0}/Windows Kits/8.1'.format(os.environ['ProgramFiles(x86)'])
      if pathlib.Path(winsdk_src_folder+'/include').exists():
        print('+++ Windows 8.1 SDK found at {0}'.format(winsdk_src_folder))
        make_directory_symlink(winsdk_src_folder, winsdk_dest_folder)
      else:
        print('--- Windows 8.1 SDK not found, install Windows SDK and re-run setup')
        if not check_again_after_download:
          error("Windows 8.1 SDK is required but not found at '{0}'".format(winsdk_src_folder))

        pathlib.Path(dest_dir+"/.packages/vs140").mkdir(parents=True, exist_ok=True)
        download_url2("https://aka.ms/vs/15/release/vs_buildtools.exe", "vs140/vs_buildtools.exe", dest_dir)
        run(dest_dir+"/.packages/vs140/vs_buildtools.exe --wait --passive --add " +
             "Microsoft.VisualStudio.Component.Windows81SDK ")
        setup_winsdk_81(False)

  setup_winsdk_81(True)


  if len(microsoft_retry) > 0:
    download_url('https://aka.ms/vs/17/release/vs_buildtools.exe', dest_dir)
    run(dest_dir+"/.packages/vs_buildtools.exe --wait --passive update")
    run(dest_dir+"/.packages/vs_buildtools.exe --wait --passive --addProductLang en-US --add " +
      " Microsoft.VisualStudio.Component.Roslyn.Compiler" +
      " Microsoft.Component.MSBuild" +
      " Microsoft.VisualStudio.Component.CoreBuildTools" +
      " Microsoft.VisualStudio.Workload.MSBuildTools" +
      " Microsoft.VisualStudio.Component.Windows10SDK" +
      " Microsoft.VisualStudio.Component.VC.CoreBuildTools" +
      " Microsoft.VisualStudio.Component.VC.Redist.14.Latest" +
      " Microsoft.VisualStudio.Component.TestTools.BuildTools" +
      " Microsoft.Net.Component.4.7.2.TargetingPack" +
      " Microsoft.VisualStudio.Component.VC.ASAN" +
      " Microsoft.VisualStudio.Component.TextTemplating" +
      " Microsoft.VisualStudio.Component.VC.CoreIde" +
      " Microsoft.VisualStudio.ComponentGroup.NativeDesktop.Core" +
      " Microsoft.VisualStudio.Component.Windows10SDK.19041" +
      " Microsoft.VisualStudio.ComponentGroup.VC.Tools.142.x86.x64" +
      " Microsoft.Component.VC.Runtime.UCRTSDK" +
      " Microsoft.VisualStudio.Component.VC.140" +
      " Microsoft.VisualStudio.Workload.VCTools" +
      " Microsoft.VisualStudio.Component.VC.14.29.16.11.x86.x64 " +
      " Microsoft.VisualStudio.Component.VC.14.29.16.11.ARM64 " +
      " Microsoft.VisualStudio.Component.VC.14.29.16.11.ATL " +
      " Microsoft.VisualStudio.Component.VC.14.44.17.14.x86.x64 " +
      " Microsoft.VisualStudio.Component.VC.14.44.17.14.ARM64 " +
      " Microsoft.VisualStudio.Component.VC.14.44.17.14.ATL " )

    for fn in microsoft_retry:
      fn(False)



  # LLVM 21.1.8
  llvm_dest_folder = dest_dir+'/LLVM-21.1.8'
  if pathlib.Path(llvm_dest_folder).exists():
    print('=== LLVM 21.1.8 symlink found at {0}, skipping setup'.format(llvm_dest_folder))
  else:
    llvm_src_folder = '{0}/LLVM'.format(os.environ['ProgramFiles']) #(x86)
    if not pathlib.Path(llvm_src_folder+'/bin/clang.exe').exists() or not pathlib.Path(llvm_src_folder+'/lib/clang/21').exists():
      print('--- LLVM 21.1.8 not found, trying to install')
      download_url('https://github.com/llvm/llvm-project/releases/download/llvmorg-21.1.8/LLVM-21.1.8-win64.exe', dest_dir)
      run(dest_dir+'/.packages/LLVM-21.1.8-win64.exe /S')

    if pathlib.Path(llvm_src_folder+'/bin').exists():
      print('+++ LLVM 21.1.8 found at {0}'.format(llvm_src_folder))
      make_directory_symlink(llvm_src_folder, llvm_dest_folder)
    else:
      error("LLVM 21.1.8 not found")


  # nasm
  nasm_dest_folder = dest_dir+'/nasm'
  if pathlib.Path(nasm_dest_folder).exists():
    print('=== NASM symlink found at {0}, skipping setup'.format(nasm_dest_folder))
  else:
    download_url('https://www.nasm.us/pub/nasm/releasebuilds/2.16/win64/nasm-2.16-win64.zip', dest_dir)
    with zipfile.ZipFile(os.path.normpath(dest_dir+'/.packages/nasm-2.16-win64.zip'), 'r') as zip_file:
      zip_file.extractall(dest_dir)
      make_directory_symlink(dest_dir+'/nasm-2.16', nasm_dest_folder)
      shutil.copyfile(nasm_dest_folder+'/nasm.exe', nasm_dest_folder+'/nasmw.exe')
      shutil.copyfile(nasm_dest_folder+'/ndisasm.exe', nasm_dest_folder+'/ndisasmw.exe')
      print('+++ NASM 2.16 installed at {0}'.format(nasm_dest_folder))


  # ducible
  ducible_dest_file = dest_dir+'/ducible.exe'
  if pathlib.Path(ducible_dest_file).exists():
    print('=== Ducible tool found at {0}, skipping setup'.format(ducible_dest_file))
  else:
    download_url('https://github.com/jasonwhite/ducible/releases/download/v1.2.2/ducible-windows-x64-Release.zip', dest_dir)
    with zipfile.ZipFile(os.path.normpath(dest_dir+'/.packages/ducible-windows-x64-Release.zip'), 'r') as zip_file:
      zip_file.extractall(dest_dir)
      print('+++ Ducible tool installed at {0}'.format(dest_dir))


  # boost-1.62
  def install_boost_1_62():
    boost_dest_folder = dest_dir+'/boost-1.62'
    if pathlib.Path(boost_dest_folder).exists():
      print('=== boost-1.62 found at {0}, skipping setup'.format(boost_dest_folder))
    else:
      boost_src_folder = ''
      for loc in ['c:/local']:
        for item in pathlib.Path(loc).glob("boost_1_62*"):
          if item.is_dir():
            if pathlib.Path(os.path.normpath(item)+'/boost').exists():
              boost_src_folder = os.path.normpath(item)
              break

      if boost_src_folder != '':
        print('+++ boost-1.62 found at {0}'.format(boost_src_folder))
        make_directory_symlink(boost_src_folder, boost_dest_folder)
      else:
        download_url('https://sourceforge.net/projects/boost/files/boost/1.62.0/boost_1_62_0.zip', dest_dir)
        with zipfile.ZipFile(os.path.normpath(dest_dir+'/.packages/boost_1_62_0.zip'), 'r') as zip_file:
          zip_file.extractall(dest_dir)
          pathlib.Path(dest_dir+'/boost-1.62/libs').mkdir(parents=True, exist_ok=True)
          subprocess.run(['cmd', '/C', 'move',
            os.path.normpath(dest_dir+'/boost_1_62_0/boost'), os.path.normpath(dest_dir+'/boost-1.62/')])
          for d in ['date_time', 'filesystem', 'system', 'thread']:
            pathlib.Path(dest_dir+'/boost-1.62/libs/'+d).mkdir(parents=True, exist_ok=True)
            subprocess.run(['cmd', '/C', 'move',
              os.path.normpath(dest_dir+'/boost_1_62_0/libs/'+d+'/src'), os.path.normpath(dest_dir+'/boost-1.62/libs/'+d)])
          subprocess.run(['cmd', '/C', 'rmdir', '/S', '/Q', os.path.normpath(dest_dir+'/boost_1_62_0')])
          print('+++ boost-1.62 installed at {0}'.format(boost_dest_folder))

  #install_boost_1_62()


  # 3ds Max SDK
  def install_3ds_Max_SDK(ver, url):
    maxsdk_dest_folder = dest_dir+'/max'+ver+'.sdk'
    if pathlib.Path(maxsdk_dest_folder).exists():
      print('=== 3ds Max SDK {1} symlink found at {0}, skipping setup'.format(maxsdk_dest_folder, ver))
    else:
      if ask("Do you want to install 3ds Max {0} SDK?".format(ver)):
        maxsdk_src_folder = '{0}/Autodesk/3ds Max {1} SDK'.format(os.environ['ProgramFiles'], ver)
        if not pathlib.Path(maxsdk_src_folder+'/maxsdk').exists():
          print('--- 3ds Max SDK '+ver+' not found, trying to install')
          download_url(url, dest_dir)
          path, file = os.path.split(os.path.normpath(url))
          run('msiexec /i ' + os.path.normpath(dest_dir + '/.packages/' + file) + ' /qb')

        if pathlib.Path(maxsdk_src_folder+'/maxsdk').exists():
          print('+++ 3ds Max SDK {1} found at {0}'.format(maxsdk_src_folder, ver))
          make_directory_symlink(maxsdk_src_folder+'/maxsdk', maxsdk_dest_folder)
        else:
          print('--- 3ds Max SDK {1} not found at {0}, skipped setup'.format(maxsdk_src_folder, ver))

  # FMOD
  fmod_dest_folder = dest_dir+'/fmod-studio-2.xx.xx'
  if pathlib.Path(fmod_dest_folder).exists():
    print('=== FMOD symlinks found at {0}, skipping setup'.format(fmod_dest_folder))
  else:
    fmod_src_folder = '{0}/FMOD SoundSystem/FMOD Studio API Windows'.format(os.environ['ProgramFiles(x86)'])
    if pathlib.Path(fmod_src_folder).exists():
      print('+++ FMOD found at {0}'.format(fmod_src_folder))

      pathlib.Path(fmod_dest_folder+'/core/win32').mkdir(parents=True, exist_ok=True)
      make_directory_symlink(fmod_src_folder+'/api/core/inc', fmod_dest_folder+'/core/win32/inc')
      make_directory_symlink(fmod_src_folder+'/api/core/lib/x86', fmod_dest_folder+'/core/win32/lib')

      pathlib.Path(fmod_dest_folder+'/core/win64').mkdir(parents=True, exist_ok=True)
      make_directory_symlink(fmod_src_folder+'/api/core/inc', fmod_dest_folder+'/core/win64/inc')
      make_directory_symlink(fmod_src_folder+'/api/core/lib/x64', fmod_dest_folder+'/core/win64/lib')

      pathlib.Path(fmod_dest_folder+'/core/win-arm64').mkdir(parents=True, exist_ok=True)
      make_directory_symlink(fmod_src_folder+'/api/core/inc', fmod_dest_folder+'/core/win-arm64/inc')
      make_directory_symlink(fmod_src_folder+'/api/core/lib/arm64', fmod_dest_folder+'/core/win-arm64/lib')

      pathlib.Path(fmod_dest_folder+'/studio/win32').mkdir(parents=True, exist_ok=True)
      make_directory_symlink(fmod_src_folder+'/api/studio/inc', fmod_dest_folder+'/studio/win32/inc')
      make_directory_symlink(fmod_src_folder+'/api/studio/lib/x86', fmod_dest_folder+'/studio/win32/lib')

      pathlib.Path(fmod_dest_folder+'/studio/win64').mkdir(parents=True, exist_ok=True)
      make_directory_symlink(fmod_src_folder+'/api/studio/inc', fmod_dest_folder+'/studio/win64/inc')
      make_directory_symlink(fmod_src_folder+'/api/studio/lib/x64', fmod_dest_folder+'/studio/win64/lib')

      pathlib.Path(fmod_dest_folder+'/studio/win-arm64').mkdir(parents=True, exist_ok=True)
      make_directory_symlink(fmod_src_folder+'/api/studio/inc', fmod_dest_folder+'/studio/win-arm64/inc')
      make_directory_symlink(fmod_src_folder+'/api/studio/lib/arm64', fmod_dest_folder+'/studio/win-arm64/lib')

      shutil.copyfile(fmod_src_folder+'/doc/LICENSE.TXT', fmod_dest_folder+'/LICENSE.TXT')
      shutil.copyfile(fmod_src_folder+'/doc/revision.txt', fmod_dest_folder+'/revision.txt')
    else:
      print('--- FMOD not found at {0}, creating stub folders'.format(fmod_src_folder))
      print('consider downloading and installing https://www.fmod.com/download#fmodengine - Windows Download')
      pathlib.Path(fmod_dest_folder+'/core/win32/inc').mkdir(parents=True, exist_ok=True)
      pathlib.Path(fmod_dest_folder+'/core/win64/inc').mkdir(parents=True, exist_ok=True)
      pathlib.Path(fmod_dest_folder+'/core/win-arm64/inc').mkdir(parents=True, exist_ok=True)
      pathlib.Path(fmod_dest_folder+'/studio/win32/inc').mkdir(parents=True, exist_ok=True)
      pathlib.Path(fmod_dest_folder+'/studio/win64/inc').mkdir(parents=True, exist_ok=True)
      pathlib.Path(fmod_dest_folder+'/studio/win-arm64/inc').mkdir(parents=True, exist_ok=True)


  # helper code do build forwarding DLL
  def _run_tool(args):
    proc = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return (proc.returncode, proc.stdout.decode('mbcs', 'replace'), proc.stderr.decode('mbcs', 'replace'))

  def _dumpbin(msvc_bin, *args):
    code, out, err = _run_tool([str(pathlib.Path(msvc_bin) / 'dumpbin.exe'), '/nologo'] + list(args))
    if code != 0:
      raise RuntimeError("dumpbin {0} failed ({1}):\n{2}".format(args, code, out))
    return out.splitlines()

  def _dump_imports(input_dll, msvc_bin):
    """Return {module.dll: [imported symbol, ...]} for a PE image."""
    _JUNK = {
      'Import Address Table',
      'Import Name Table',
      'time date stamp',
      'Index of first forwarder reference',
    }
    _RE_MODULE = re.compile(r'^ {4}(\S+\.dll)\s*$', re.IGNORECASE)
    _RE_SYMBOL = re.compile(r'^\s+[0-9A-Fa-f]+\s+(\S.*\S)\s*$')

    imports = {}
    current = None
    for line in _dumpbin(msvc_bin, '/imports', str(input_dll)):
      if line.strip() == 'Summary':  # trailing section table, not imports
        break
      m = _RE_MODULE.match(line)
      if m:
        current = imports.setdefault(m.group(1), [])
        continue
      if current is None:
        continue
      m = _RE_SYMBOL.match(line)
      if m and m.group(1) not in _JUNK:
        current.append(m.group(1))
    return imports

  def _dump_machine(input_dll, msvc_bin):
    """Return a /MACHINE: value ('ARM64', 'X64', ...) for a PE image."""
    _RE_MACHINE = re.compile(r'^\s+([0-9A-F]+) machine \((\w+)\)')
    _MACHINES = {'AA64': 'ARM64', '8664': 'X64', '14C': 'X86', '1C4': 'ARM'}

    for line in _dumpbin(msvc_bin, '/headers', str(input_dll)):
      m = _RE_MACHINE.match(line)
      if m:
        code = m.group(1).upper()
        if code not in _MACHINES:
          raise RuntimeError("unsupported machine {0} ({1})".format(code, m.group(2)))
        return _MACHINES[code]
    raise RuntimeError("no machine field in {0}".format(input_dll))


  def _build_forwarder(input_dll, ref_dll, output_dll, msvc_bin):
    """Build `output_dll`: a stub forwarding to `ref_dll`.

    input_dll   PE image whose imports drive the export list.
    ref_dll     DLL holding the real implementations, e.g. "msvcp140.dll".
    output_dll  stub to create; its file name must equal the imported module
                name, since that is how the loader resolves it.
    msvc_bin    directory containing dumpbin.exe and link.exe.
    """
    input_dll, output_dll = pathlib.Path(input_dll), pathlib.Path(output_dll)
    msvc_bin = pathlib.Path(msvc_bin)
    # forwarder syntax uses the module name without extension
    ref = pathlib.Path(ref_dll).stem
    if ref.lower() == output_dll.stem.lower():
      raise ValueError("{0} would forward to itself".format(output_dll.name))

    imports = _dump_imports(input_dll, msvc_bin)
    symbols = None
    for module in imports:
      if module.lower() == output_dll.name.lower():
        symbols = imports[module]
        break
    if not symbols:
      raise ValueError("{0} imports nothing from {1}; it imports from: {2}".format(
        input_dll.name, output_dll.name, ', '.join(sorted(imports))))

    def_path = output_dll.with_suffix('.def')
    def_path.parent.mkdir(parents=True, exist_ok=True)
    def_lines = ['LIBRARY ' + output_dll.stem.upper(), 'EXPORTS']
    for s in sorted(symbols):
      def_lines.append('  {0}={1}.{0}'.format(s, ref))
    def_path.write_text('\n'.join(def_lines) + '\n', encoding='ascii')

    code, out, err = _run_tool([str(msvc_bin / 'link.exe'), '/nologo', '/DLL', '/NOENTRY',
      '/MACHINE:' + _dump_machine(input_dll, msvc_bin), '/DEF:' + str(def_path), '/OUT:' + str(output_dll)])
    if code != 0:
      raise RuntimeError("link failed ({0}):\n{1}\n{2}".format(code, out, err))
    for junk in (output_dll.with_suffix('.lib'), output_dll.with_suffix('.exp'), def_path):
      if junk.exists():
        junk.unlink()

    #print("{0}: {1} forwarders -> {2}.dll".format(output_dll, len(symbols), ref))
    code, out, err = _run_tool([str(ducible_dest_file), str(output_dll)])
    if code != 0:
      raise RuntimeError("ducible failed ({0}):\n{1}\n{2}".format(code, out, err))
    return output_dll

  # OpenXR 1.1.54
  openxr_dest_folder = dest_dir+'/openxr-1.1.54'
  if pathlib.Path(openxr_dest_folder).exists():
    print('=== OpenXR symlink found at {0}, skipping setup'.format(openxr_dest_folder))
  else:
    download_url('https://github.com/KhronosGroup/OpenXR-SDK-Source/releases/download/release-1.1.54/openxr_loader_windows-1.1.54.zip', dest_dir)
    with zipfile.ZipFile(os.path.normpath(dest_dir+'/.packages/openxr_loader_windows-1.1.54.zip'), 'r') as zip_file:
      zip_file.extractall(openxr_dest_folder+'/openxr_loader_windows')
      make_directory_symlink(openxr_dest_folder+'/openxr_loader_windows/include', openxr_dest_folder+'/include')
      make_directory_symlink(openxr_dest_folder+'/openxr_loader_windows/Win32', openxr_dest_folder+'/win32')
      make_directory_symlink(openxr_dest_folder+'/openxr_loader_windows/x64', openxr_dest_folder+'/win64')
      make_directory_symlink(openxr_dest_folder+'/openxr_loader_windows/ARM64_uwp', openxr_dest_folder+'/win-arm64')
      msvc_dir = dest_dir + '/vc2022_17.14.4/bin/Hostx64/x64'
      openxr_loader = openxr_dest_folder+'/win-arm64/bin/openxr_loader.dll'
      _build_forwarder(openxr_loader, 'msvcp140.dll', openxr_dest_folder+'/win-arm64/bin/msvcp140_app.dll', msvc_dir)
      _build_forwarder(openxr_loader, 'vcruntime140.dll', openxr_dest_folder+'/win-arm64/bin/vcruntime140_app.dll', msvc_dir)
      print('+++ OpenXR 1.1.54 installed at {0}'.format(openxr_dest_folder))


  # FidelityFX-FSR2 compiler
  ffxsc_dest_folder = dest_dir+'/FidelityFX_SC'
  if pathlib.Path(ffxsc_dest_folder).exists():
    print('=== FidelityFX_SC symlink found at {0}, skipping setup'.format(ffxsc_dest_folder))
  else:
    download_url2('https://github.com/GPUOpen-Effects/FidelityFX-FSR2/archive/refs/tags/v2.2.1.zip', 'FidelityFX-FSR2.zip', dest_dir)
    with zipfile.ZipFile(os.path.normpath(dest_dir+'/.packages/FidelityFX-FSR2.zip'), 'r') as zip_file:
      zip_file.extractall(dest_dir+'/.packages/')
      make_directory_symlink(dest_dir+'/.packages/FidelityFX-FSR2-2.2.1/tools/sc', ffxsc_dest_folder)
      print('+++ FidelityFX_SC 2.2.1 installed at {0}'.format(ffxsc_dest_folder))


  # DXC-1.8.2505.1
  dxc_dest_folder = dest_dir+'/DXC-1.8.2505.1'
  if pathlib.Path(dxc_dest_folder).exists():
    print('=== DXC May 2025 - Patch 1 -- 1.8.2505.1 found at {0}, skipping setup'.format(dxc_dest_folder))
  else:
    download_url('https://github.com/microsoft/DirectXShaderCompiler/releases/download/v1.8.2505.1/dxc_2025_07_14.zip', dest_dir)
    download_url('https://github.com/microsoft/DirectXShaderCompiler/archive/refs/tags/v1.8.2505.1.zip', dest_dir)
    with zipfile.ZipFile(os.path.normpath(dest_dir+'/.packages/v1.8.2505.1.zip'), 'r') as zip_file:
      zip_file.extractall(dest_dir+'/.packages/')
      with zipfile.ZipFile(os.path.normpath(dest_dir+'/.packages/dxc_2025_07_14.zip'), 'r') as zip_file:
        zip_file.extractall(dest_dir+'/.packages/DirectXShaderCompiler-1.8.2505.1/_win')

        pathlib.Path(dxc_dest_folder+'/include').mkdir(parents=True, exist_ok=True)
        pathlib.Path(dxc_dest_folder+'/lib').mkdir(parents=True, exist_ok=True)
        make_directory_symlink(dest_dir+'/.packages/DirectXShaderCompiler-1.8.2505.1/include/dxc', dxc_dest_folder+'/include/dxc')
        make_directory_symlink(dest_dir+'/.packages/DirectXShaderCompiler-1.8.2505.1/_win/bin/x64', dxc_dest_folder+'/lib/win64')
        make_directory_symlink(dest_dir+'/.packages/DirectXShaderCompiler-1.8.2505.1/_win/bin/arm64', dxc_dest_folder+'/lib/win-arm64')
        shutil.copyfile(dest_dir+'/.packages/DirectXShaderCompiler-1.8.2505.1/LICENSE.TXT', dxc_dest_folder+'/LICENSE.TXT')
        print('+++ DXC May 2025 - Patch 1 -- 1.8.2505.1 installed at {0}'.format(dxc_dest_folder))

  # Agility.SDK.1.619.3
  asdk_ver = '1.619.3'
  asdk_dest_folder = dest_dir+'/Agility.SDK.'+asdk_ver
  if pathlib.Path(asdk_dest_folder).exists():
    print('=== Agility.SDK.{1} symlink found at {0}, skipping setup'.format(asdk_dest_folder, asdk_ver))
  else:
    zip_name = 'D3D12-{0}.zip'.format(asdk_ver)
    download_url2('https://www.nuget.org/api/v2/package/Microsoft.Direct3D.D3D12/'+asdk_ver, zip_name, dest_dir)
    asdk_pkg_name = dest_dir+'/.packages/D3D12-'+asdk_ver+'.pkg'
    with zipfile.ZipFile(os.path.normpath(dest_dir+'/.packages/'+zip_name), 'r') as zip_file:
      zip_file.extractall(asdk_pkg_name)
      #make_directory_symlink(asdk_pkg_name+'/build/native', asdk_dest_folder)
      shutil.move(asdk_pkg_name+'/build/native', asdk_dest_folder)
      shutil.move(asdk_pkg_name+'/README.md', asdk_dest_folder)
      shutil.move(asdk_pkg_name+'/distributable files.txt', asdk_dest_folder)
      shutil.move(asdk_pkg_name+'/LICENSE.txt', asdk_dest_folder)
      shutil.move(asdk_pkg_name+'/LICENSE-CODE.txt', asdk_dest_folder)
      shutil.move(asdk_pkg_name+'/Microsoft.Direct3D.D3D12.nuspec', asdk_dest_folder)
      print('+++ Agility.SDK.{1} installed at {0}'.format(asdk_dest_folder, asdk_ver))

  # astcenc-4.6.1
  astcenc_dest_folder = dest_dir+'/astcenc-4.6.1'
  if pathlib.Path(astcenc_dest_folder).exists():
    print('=== ASTC encoder 4.6.1 {0}, skipping setup'.format(astcenc_dest_folder))
  else:
    download_url('https://github.com/ARM-software/astc-encoder/releases/download/4.6.1/astcenc-4.6.1-windows-x64.zip', dest_dir)
    with zipfile.ZipFile(os.path.normpath(dest_dir+'/.packages/astcenc-4.6.1-windows-x64.zip'), 'r') as zip_file:
      zip_file.extractall(dest_dir+'/astcenc-4.6.1')
      os.rename(os.path.normpath(dest_dir+'/astcenc-4.6.1/bin'), os.path.normpath(dest_dir+'/astcenc-4.6.1/win64'));
      print('+++ ASTC encoder 4.6.1 installed at {0}'.format(astcenc_dest_folder))

  # ispc-v1.23.0
  ispc_dest_folder = dest_dir+'/ispc-v1.23.0-windows'
  if pathlib.Path(ispc_dest_folder).exists():
    print('=== ISPC v1.23.0 {0}, skipping setup'.format(ispc_dest_folder))
  else:
    download_url('https://github.com/ispc/ispc/releases/download/v1.23.0/ispc-v1.23.0-windows.zip', dest_dir)
    with zipfile.ZipFile(os.path.normpath(dest_dir+'/.packages/ispc-v1.23.0-windows.zip'), 'r') as zip_file:
      zip_file.extractall(dest_dir)
      print('+++ ISPC v1.23.0 installed at {0}'.format(ispc_dest_folder))

  # FidelityFX-SDK-2.1.1
  fidelityfx_sdk_ver = '2.1.1'
  fidelityfx_sdk_dest_folder = dest_dir+'/FidelityFX-SDK-'+fidelityfx_sdk_ver
  if pathlib.Path(fidelityfx_sdk_dest_folder).exists():
    print('=== FidelityFX SDK {1} found at {0}, skipping setup'.format(fidelityfx_sdk_dest_folder, fidelityfx_sdk_ver))
  else:
    fidelityfx_sdk_zip = 'FidelityFX-SDK-'+fidelityfx_sdk_ver+'.zip'
    download_url2('https://github.com/GPUOpen-LibrariesAndSDKs/FidelityFX-SDK/archive/refs/tags/v'+fidelityfx_sdk_ver+'.zip',
                  fidelityfx_sdk_zip, dest_dir)
    with zipfile.ZipFile(os.path.normpath(dest_dir+'/.packages/'+fidelityfx_sdk_zip), 'r') as zip_file:
      zip_file.extractall(dest_dir)
    print('+++ FidelityFX SDK {1} installed at {0}'.format(fidelityfx_sdk_dest_folder, fidelityfx_sdk_ver))

  # nvapi-R610
  nvapi_dest_folder = dest_dir+'/nvapi-R610'
  if pathlib.Path(nvapi_dest_folder).exists():
    print('=== nvapi symlink found at {0}, skipping setup'.format(nvapi_dest_folder))
  else:
    download_url2('https://github.com/NVIDIA/nvapi/archive/refs/heads/main.zip', 'nvapi-R610.zip', dest_dir)
    with zipfile.ZipFile(os.path.normpath(dest_dir+'/.packages/nvapi-R610.zip'), 'r') as zip_file:
      members = [
          m for m in zip_file.namelist()
          if not (m.startswith('nvapi-main/docs/') or m.startswith('nvapi-main/Sample_Code/'))
      ]
      zip_file.extractall(dest_dir, members)
    os.rename(os.path.normpath(dest_dir+'/nvapi-main'), os.path.normpath(nvapi_dest_folder));
    print('+++ nvapi-R610 installed at {0}'.format(nvapi_dest_folder))

  # Nsight Aftermath SDK 2025.5.0.25317
  aftermath_dest_folder = dest_dir+'/aftermath-2025.5.0.25317'
  if pathlib.Path(aftermath_dest_folder).exists():
    print('=== Nsight Aftermath SDK symlink found at {0}, skipping setup'.format(aftermath_dest_folder))
  else:
    download_url2('https://developer.nvidia.com/downloads/assets/tools/secure/nsight-aftermath-sdk/2025_5_0/windows_x64/'
                  'NVIDIA_Nsight_Aftermath_SDK_2025.5.0.25317-windows_x64.zip', 'aftermath-2025.5.0.25317.zip', dest_dir)
    with zipfile.ZipFile(os.path.normpath(dest_dir+'/.packages/aftermath-2025.5.0.25317.zip'), 'r') as zip_file:
      zip_file.extractall(aftermath_dest_folder)
    print('+++ Nsight Aftermath SDK 2025.5.0.25317 installed at {0}'.format(aftermath_dest_folder))

  # AGS v6.3.0
  ags_sdk_dest_folder = dest_dir+'/AGS.SDK.6.3.0'
  if pathlib.Path(ags_sdk_dest_folder).exists():
    print('=== AGS SDK symlink found at {0}, skipping setup'.format(ags_sdk_dest_folder))
  else:
    download_url2('https://github.com/GPUOpen-LibrariesAndSDKs/AGS_SDK/archive/refs/tags/v6.3.0.zip', 'AGS.SDK.6.3.0.zip', dest_dir)
    with zipfile.ZipFile(os.path.normpath(dest_dir+'/.packages/AGS.SDK.6.3.0.zip'), 'r') as zip_file:
      prefix = 'AGS_SDK-6.3.0/ags_lib/'
      for member in zip_file.namelist():
        if member.startswith(prefix) and not member.endswith('/'):
          rel_path = os.path.relpath(member, prefix)
          if rel_path == '.':
            continue
          target_path = os.path.join(ags_sdk_dest_folder, rel_path)
          os.makedirs(os.path.dirname(target_path), exist_ok=True)
          with zip_file.open(member) as source, open(target_path, 'wb') as target:
            target.write(source.read())
            target.close()
    print('+++ AGS v6.3.0 installed at {0}'.format(ags_sdk_dest_folder))

  # Streamline SDK 2.14.1
  streamline_ver = '2.14.1'
  streamline_dest_folder = dest_dir+'/streamline-'+streamline_ver
  # x64 and aarch64 ship as separate archives that share the same include/ and unpack into one
  # folder, so each is tested on the bin/<arch> only it carries - a run that dies between the
  # two leaves the other arch missing, and the folder alone would look like a finished install
  for streamline_arch, streamline_zip in [('x64', 'streamline-sdk-v'+streamline_ver+'.zip'),
                                          ('arm64', 'streamline-sdk-v'+streamline_ver+'-aarch64.zip')]:
    if pathlib.Path(streamline_dest_folder+'/bin/'+streamline_arch).exists():
      print('=== Streamline SDK {1} {2} found at {0}, skipping setup'.format(streamline_dest_folder, streamline_ver, streamline_arch))
    else:
      download_url2('https://github.com/NVIDIA-RTX/Streamline/releases/download/v'+streamline_ver+'/'+streamline_zip,
                    streamline_zip, dest_dir)
      with zipfile.ZipFile(os.path.normpath(dest_dir+'/.packages/'+streamline_zip), 'r') as zip_file:
        members = [m for m in zip_file.namelist() if m.startswith(('include/', 'bin/', 'lib/'))]
        zip_file.extractall(streamline_dest_folder, members)
      print('+++ Streamline SDK {1} {2} installed at {0}'.format(streamline_dest_folder, streamline_ver, streamline_arch))

  # install 3ds Max SDKs
  install_3ds_Max_SDK('2026',
    'https://autodesk-adn-transfer.s3.us-west-2.amazonaws.com/ADN+Extranet/M%26E/Max/Autodesk+3ds+Max+2026/SDK_3dsMax2026.msi')
  install_3ds_Max_SDK('2025',
    'https://autodesk-adn-transfer.s3.us-west-2.amazonaws.com/ADN+Extranet/M%26E/Max/Autodesk+3ds+Max+2025/SDK_3dsMax2025.msi')
  install_3ds_Max_SDK('2024',
    'https://autodesk-adn-transfer.s3.us-west-2.amazonaws.com/ADN+Extranet/M%26E/Max/Autodesk+3ds+Max+2024/SDK_3dsMax2024.msi')
  #install_3ds_Max_SDK('2023',
  #  'https://autodesk-adn-transfer.s3.us-west-2.amazonaws.com/ADN+Extranet/M%26E/Max/Autodesk+3ds+Max+2023/SDK_3dsMax2023.msi')
  #install_3ds_Max_SDK('2019',
  #  'https://autodesk-adn-transfer.s3.us-west-2.amazonaws.com/ADN%20Extranet/M%26E/Max/Autodesk%203ds%20Max%202019/SDK_3dsMax2019.msi')


  # re-write platform.jam
  if pathlib.Path("prog").exists():
    with open('prog/platform.jam', 'w') as fd:
      fd.write('_DEVTOOL = {0} ;\n'.format(dest_dir))
      if pathlib.Path(fmod_dest_folder+'/LICENSE.TXT').exists():
        fd.write('FmodStudio = 2.xx.xx ;\n')
      else:
        fd.write('FmodStudio = none ;\n')
      fd.close()


  nomalized_dest = os.path.normpath(dest_dir)
  env_updated = False

  if os.environ.get('GDEVTOOL', '') == '':
    if ask("Environment variable 'GDEVTOOL' not found. Do you want to set it?"):
      subprocess.run(["setx", "GDEVTOOL", nomalized_dest], shell=True, text=True)
      os.environ["GDEVTOOL"] = nomalized_dest
      env_updated = True
  elif os.environ.get('GDEVTOOL', '') != nomalized_dest:
    if ask("Environment variable 'GDEVTOOL' points to another directory. Do you want to update it?"):
      subprocess.run(["setx", "GDEVTOOL", nomalized_dest], shell=True, text=True)
      os.environ["GDEVTOOL"] = nomalized_dest
      env_updated = True

  if nomalized_dest not in os.environ.get('PATH', '').split(os.pathsep):
    if ask("'{0}' is not found in 'PATH' variable. Do you want to add it?".format(nomalized_dest)):
      print("adding {0} to 'PATH', it may take a while...".format(nomalized_dest))
      add_path_command = ('[System.Environment]::SetEnvironmentVariable("PATH", ' +
                          '"{0};" + [System.Environment]::GetEnvironmentVariable("PATH", [System.EnvironmentVariableTarget]::User), '.format(nomalized_dest) +
                          '[System.EnvironmentVariableTarget]::User)')
      subprocess.run(["powershell", "-Command", add_path_command], shell=True, text=True)
      env_updated = True

  try:
    subprocess.run(["jam", "-v"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
  except FileNotFoundError:
    print("jam.exe not found, installing jam...")
    jam_zip = 'jam-windows-x86_64.zip'
    if (os.environ.get('PROCESSOR_ARCHITECTURE', '') == 'ARM64' or
       ('ARMv' in os.environ.get('PROCESSOR_IDENTIFIER', '') and '64-bit' in os.environ.get('PROCESSOR_IDENTIFIER', ''))):
      jam_zip = 'jam-windows-arm64.zip'
    download_url(JAM_RELEASE_URL+'/'+jam_zip, dest_dir)
    with zipfile.ZipFile(os.path.normpath(dest_dir+'/.packages/'+jam_zip), 'r') as zip_file:
      zip_file.extractall(dest_dir)

  if env_updated:
    print("\nDone. Please restart your command-line environment to apply the environment variables.")
  else:
    print("\nDone.")


def devtools_linux(dest_dir):
  linux_release_name = ''
  linux_release_id = ''
  linux_release_ver = ''
  linux_arch_type = platform.uname().machine

  with open('/etc/os-release', 'r') as file:
    for val_pair in re.findall(r'(\w+)=(.+)\n', file.read()):
      if val_pair[0] == 'NAME':
        linux_release_name = val_pair[1]
      elif val_pair[0] == 'ID':
        linux_release_id = val_pair[1]
      elif val_pair[0] == 'VERSION':
        linux_release_ver = val_pair[1]
    file.close()

  is_rosa_linux = (linux_release_id == 'rosa')
  is_astra_linux = "Astra Linux" in linux_release_name
  is_ubuntu = ("Ubuntu" in linux_release_name)
  is_centos = ('centos' in linux_release_id)
  is_altlinux = (linux_release_id == 'altlinux')
  is_elbrus_linux = ('elbrus' in linux_release_id)
  print('Detected linux: {0} {1}  ({2}) arch={3}'.format(linux_release_name, linux_release_ver, linux_release_id, linux_arch_type))

  pkg_to_install = ['nasm']
  pkg_install_cmd = ''
  if is_rosa_linux:
    pkg_install_cmd = 'dnf install'
    pkg_to_install += ['python3-pip', 'gcc', 'gcc-c++', 'clang', 'lib64ubsan-devel']
    pkg_to_install += ['lib64x11-devel', 'lib64xrandr-devel', 'lib64xi-devel', 'lib64fltk-devel', 'lib64xkbfile-devel', 'lib64udev-devel', 'lib64pulseaudio-devel', 'lib64alsa-oss-devel']
  elif is_altlinux:
    pkg_install_cmd = 'apt-get install'
    pkg_to_install += ['python3-module-pip', 'clang21.1', 'libclang21', 'libasan-devel-static']
    pkg_to_install += ['libX11-devel', 'libXrandr-devel', 'libXi-devel', 'libXcursor-devel', 'libfltk-devel', 'libxkbfile-devel', 'libxkbcommon-devel',
                       'libudev-devel', 'libpulseaudio-devel', 'libalsa-devel', 'libuuid-devel', 'libdbus-devel']
  elif is_elbrus_linux:
    pkg_install_cmd = 'apt install'
    pkg_to_install  = ['python3-pip']
    pkg_to_install += ['libx11', 'libxrandr', 'libxi', 'fltk', 'libxkbfile', 'pulseaudio', 'alsa-lib', 'uuid']
  elif is_ubuntu:
    pkg_install_cmd = 'apt install'
    pkg_to_install += ['python3-pip', 'gcc', 'clang']
    pkg_to_install += ['libx11-dev', 'libxrandr-dev', 'libxi-dev', 'libfltk1.3-dev', 'libxkbfile-dev', 'libudev-dev', 'libpulse-dev', 'uuid-dev']
  elif is_astra_linux:
    pkg_install_cmd = 'apt install'
    pkg_to_install += ['python3-pip', 'gcc-mozilla', 'clang-10']
    pkg_to_install += ['libx11-dev', 'libxrandr-dev', 'libxi-dev', 'libfltk1.3-dev', 'libxkbfile-dev', 'libudev-dev', 'libpulse-dev', 'uuid-dev']
  elif is_centos:
    pkg_install_cmd = 'yum install'
    pkg_to_install += ['python3-pip', 'devtoolset-11', 'llvm-toolset-7.0']
    pkg_to_install += ['libX11-devel', 'libXrandr-devel', 'libXi-devel', 'libfltk-devel', 'libxkbfile-devel', 'libgudev1-devel', 'pulseaudio-libs-devel', 'alsa-lib-devel']
  else:
    pkg_to_install += ['python3-pip', 'gcc', 'gcc-c++', 'clang']
    pkg_to_install += ['libx11-dev', 'libxrandr-dev', 'libxi-dev', 'libfltk1.3-dev', 'libxkbfile-dev', 'libudev-dev', 'libpulse-dev', 'libalsa-devel']

  if pkg_install_cmd != '':
    print('--- will try to install required packages:\n  '+' '.join(pkg_to_install))
    run('sudo {0} {1}'.format(pkg_install_cmd, ' '.join(pkg_to_install)))
  else:
    print('NOTE: you have to install these (or similar) packages manually:\n  ' + ' '.join(pkg_to_install) + '\n\n')

  if is_rosa_linux:
    if not pathlib.Path('/usr/lib64/libclang.so').exists() and pathlib.Path('/usr/lib64/libclang.so.12').exists():
      run('sudo ln -s libclang.so.12 /usr/lib64/libclang.so')

  # python3
  python_dest_folder = dest_dir+'/python3'
  if pathlib.Path(python_dest_folder).exists():
    print('=== Python 3 symlink found at {0}, skipping setup'.format(python_dest_folder))
  else:
    python_src_folder = os.path.dirname(sys.executable)
    print('+++ Python 3 found at {0}'.format(python_src_folder))
    make_directory_symlink(python_src_folder, python_dest_folder)

    subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'])
    subprocess.run([sys.executable, '-m', 'pip', '--version'])
    subprocess.run([sys.executable, '-m', 'pip', 'install', 'clang==14.0.6'])
    subprocess.run([sys.executable, '-m', 'pip', 'install', 'cymbal'])


  # FMOD
  fmod_dest_folder = dest_dir+'/fmod-studio-2.xx.xx'
  if pathlib.Path(fmod_dest_folder).exists():
    print('=== FMOD symlinks found at {0}, skipping setup'.format(fmod_dest_folder))
  else:
    for fmod_src_folder in glob.glob('{0}/fmodstudioapi2*linux'.format(os.environ['HOME'])):
      if pathlib.Path(fmod_src_folder+'/api').exists():
        print('+++ FMOD found at {0}'.format(fmod_src_folder))

        pathlib.Path(fmod_dest_folder+'/core/linux64').mkdir(parents=True, exist_ok=True)
        make_directory_symlink('"{0}/api/core/inc"'.format(fmod_src_folder), fmod_dest_folder+'/core/linux64/inc')
        make_directory_symlink('"{0}/api/core/lib"'.format(fmod_src_folder), fmod_dest_folder+'/core/linux64/lib')

        pathlib.Path(fmod_dest_folder+'/studio/linux64').mkdir(parents=True, exist_ok=True)
        make_directory_symlink('"{0}/api/studio/inc"'.format(fmod_src_folder), fmod_dest_folder+'/studio/linux64/inc')
        make_directory_symlink('"{0}/api/studio/lib"'.format(fmod_src_folder), fmod_dest_folder+'/studio/linux64/lib')
        run('cp "{0}/doc/LICENSE.TXT" {1}'.format(fmod_src_folder, fmod_dest_folder))
        run('cp "{0}/doc/revision.txt" {1}'.format(fmod_src_folder, fmod_dest_folder))
        break
    if not pathlib.Path(fmod_dest_folder).exists():
      print('--- FMOD not found, creating stub folders')
      print('consider downloading and installing https://www.fmod.com/download#fmodengine - Linux Download')
      pathlib.Path(fmod_dest_folder+'/core/linux64/inc').mkdir(parents=True, exist_ok=True)
      pathlib.Path(fmod_dest_folder+'/studio/linux64/inc').mkdir(parents=True, exist_ok=True)


  # DXC-1.8.2505.1
  dxc_dest_folder = dest_dir+'/DXC-1.8.2505.1'
  if pathlib.Path(dxc_dest_folder).exists():
    print('=== DXC May 2025 - Patch 1 -- 1.8.2505.1 found at {0}, skipping setup'.format(dxc_dest_folder))
  else:
    download_url('https://github.com/microsoft/DirectXShaderCompiler/releases/download/v1.8.2505.1/linux_dxc_2025_07_14.x86_64.tar.gz', dest_dir)
    with tarfile.open(os.path.normpath(dest_dir+'/.packages/linux_dxc_2025_07_14.x86_64.tar.gz'), 'r:gz') as tar_file:
      tar_file.extractall(dxc_dest_folder)
      tar_file.close()
      pathlib.Path(dxc_dest_folder+'/lib/linux64').mkdir(parents=True, exist_ok=True);
      make_directory_symlink(dxc_dest_folder+'/lib/libdxcompiler.so', dxc_dest_folder+'/lib/linux64/libdxcompiler.so')
      print('+++ DXC May 2025 - Patch 1 -- 1.8.2505.1 installed at {0}'.format(dxc_dest_folder))
      if linux_arch_type == 'e2k':
        print('!!! arch={0} differs from x86_64, you should rebuild {1} for\n'
              '    your arch and place result binary to {2}/lib/linux64/libdxcompiler.so\n\n'
              .format(linux_arch_type, 'https://github.com/microsoft/DirectXShaderCompiler', dxc_dest_folder))

  # astcenc-4.6.1
  astcenc_dest_folder = dest_dir+'/astcenc-4.6.1'
  if pathlib.Path(astcenc_dest_folder).exists():
    print('=== ASTC encoder 4.6.1 {0}, skipping setup'.format(astcenc_dest_folder))
  elif linux_arch_type == 'e2k':
    pathlib.Path(astcenc_dest_folder+'/linux64').mkdir(parents=True, exist_ok=True)
    print('+++ ASTC encoder 4.6.1 folder created at {0}'.format(astcenc_dest_folder))
    print('!!! arch={0} differs from x86_64, you should rebuild {1}\n'
          '    for your arch and place result binary to {2}/linux64/astcenc-native\n\n'
          .format(linux_arch_type, 'https://github.com/ARM-software/astc-encoder', astcenc_dest_folder))
  else:
    download_url('https://github.com/ARM-software/astc-encoder/releases/download/4.6.1/astcenc-4.6.1-linux-x64.zip', dest_dir)
    with zipfile.ZipFile(os.path.normpath(dest_dir+'/.packages/astcenc-4.6.1-linux-x64.zip'), 'r') as zip_file:
      zip_file.extractall(dest_dir+'/astcenc-4.6.1')
      os.rename(os.path.normpath(dest_dir+'/astcenc-4.6.1/bin'), os.path.normpath(dest_dir+'/astcenc-4.6.1/linux64'));
      run('chmod 755 '+dest_dir+'/astcenc-4.6.1/linux64/astcenc*')
      print('+++ ASTC encoder 4.6.1 installed at {0}'.format(astcenc_dest_folder))

  # ispc-v1.23.0
  ispc_dest_folder = dest_dir+'/ispc-v1.23.0-linux'
  if pathlib.Path(ispc_dest_folder).exists():
    print('=== ISPC v1.23.0 {0}, skipping setup'.format(ispc_dest_folder))
  elif linux_arch_type == 'e2k':
    pathlib.Path(ispc_dest_folder).mkdir(parents=True, exist_ok=True)
    print('+++ ISPC v1.23.0 skipped (stub created at {0})'.format(ispc_dest_folder))
    print('!!! arch={0} differs from x86_64, you should rebuild {1}\n'
          '    for your arch and place result binary to {2}/bin/ispc\n\n'
          .format(linux_arch_type, 'https://github.com/ispc/ispc', ispc_dest_folder))
  else:
    download_url('https://github.com/ispc/ispc/releases/download/v1.23.0/ispc-v1.23.0-linux-oneapi.tar.gz', dest_dir)
    with tarfile.open(os.path.normpath(dest_dir+'/.packages/ispc-v1.23.0-linux-oneapi.tar.gz'), 'r:gz') as tar_file:
      tar_file.extractall(dest_dir)
      tar_file.close()
      print('+++ ISPC v1.23.0 installed at {0}'.format(ispc_dest_folder))


  try:
    subprocess.run(['jam', '-v'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  except FileNotFoundError:
    print("jam not found, installing jam...")
    jam_zip = 'jam-centOS-7-x86_64.tar.gz'
    if linux_arch_type == 'e2k':
      if is_altlinux:
        jam_zip = 'jam-AltLinux-10-e2k-v3.tar.gz'
      elif is_elbrus_linux:
        jam_zip = 'jam-ElbrusLinux-8-e2k-v3.tar.gz'

    download_url(JAM_RELEASE_URL+'/'+jam_zip, dest_dir)
    with tarfile.open(os.path.normpath(dest_dir+'/.packages/'+jam_zip), 'r:gz') as tar_file:
      tar_file.extractall(dest_dir)
      print('--- will copy jam to /usr/local/bin using sudo:')
      run('sudo cp '+dest_dir+'/jam /usr/local/bin/jam')

  # re-write platform.jam
  if pathlib.Path("prog").exists():
    with open('prog/platform.jam', 'w') as fd:
      fd.write('_DEVTOOL = {0} ;\n'.format(dest_dir))
      if pathlib.Path(fmod_dest_folder+'/LICENSE.TXT').exists():
        fd.write('FmodStudio = 2.xx.xx ;\n')
      else:
        fd.write('FmodStudio = none ;\n')
      if linux_arch_type == 'e2k':
        fd.write('PlatformArch = e2k ;\n')
        fd.write('PlatformSpec ?= clang ;\n')
        fd.write('WError = no ;\n')
        fd.write('RemoveCompilerSwitches_linux/gcc = -mno-recip -minline-all-stringops -fconserve-space ;\n')
      if is_astra_linux:
        fd.write('PlatformSpec = clang ;\n')
      if is_astra_linux or is_rosa_linux:
        fd.write('MArch = -default- ; #remove it to build for haswell\n') # to avoid building daNetGame for haswell arch
      fd.close()


def devtools_macOS(dest_dir):
  mac_proc_arm = (platform.processor() == 'arm')

  # python3
  python_dest_folder = dest_dir+'/python3'
  if pathlib.Path(python_dest_folder).exists():
    print('=== Python 3 symlink found at {0}, skipping setup'.format(python_dest_folder))
  else:
    python_src_folder = os.path.dirname(sys.executable)
    print('+++ Python 3 found at {0}'.format(python_src_folder))
    make_directory_symlink(python_src_folder, python_dest_folder)

    subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'])
    subprocess.run([sys.executable, '-m', 'pip', '--version'])
    subprocess.run([sys.executable, '-m', 'pip', 'install', 'clang==14.0.6'])
    subprocess.run([sys.executable, '-m', 'pip', 'install', 'cymbal'])


  # nasm
  nasm_dest_folder = dest_dir+'/nasm'
  if pathlib.Path(nasm_dest_folder).exists():
    print('=== NASM symlink found at {0}, skipping setup'.format(nasm_dest_folder))
  else:
    download_url('https://www.nasm.us/pub/nasm/releasebuilds/2.16/macosx/nasm-2.16-macosx.zip', dest_dir)
    with zipfile.ZipFile(os.path.normpath(dest_dir+'/.packages/nasm-2.16-macosx.zip'), 'r') as zip_file:
      zip_file.extractall(dest_dir)
      run('chmod 755 '+dest_dir+'/nasm-2.16/nasm')
      run('chmod 755 '+dest_dir+'/nasm-2.16/ndisasm')
      print('--- will copy nasm to /usr/local/bin using sudo:')
      run('sudo cp '+dest_dir+'/nasm-2.16/nasm /usr/local/bin/nasm')
      print('+++ NASM 2.16 installed at {0}'.format(nasm_dest_folder))


  # FMOD
  fmod_dest_folder = dest_dir+'/fmod-studio-2.xx.xx'
  if pathlib.Path(fmod_dest_folder).exists():
    print('=== FMOD symlinks found at {0}, skipping setup'.format(fmod_dest_folder))
  else:
    fmod_src_folder = '{0}/FMOD Programmers API'.format(os.environ['HOME'])
    if pathlib.Path(fmod_src_folder).exists():
      print('+++ FMOD found at {0}'.format(fmod_src_folder))

      pathlib.Path(fmod_dest_folder+'/core/macosx').mkdir(parents=True, exist_ok=True)
      make_directory_symlink('"{0}/api/core/inc"'.format(fmod_src_folder), fmod_dest_folder+'/core/macosx/inc')
      make_directory_symlink('"{0}/api/core/lib"'.format(fmod_src_folder), fmod_dest_folder+'/core/macosx/lib')

      pathlib.Path(fmod_dest_folder+'/studio/macosx').mkdir(parents=True, exist_ok=True)
      make_directory_symlink('"{0}/api/studio/inc"'.format(fmod_src_folder), fmod_dest_folder+'/studio/macosx/inc')
      make_directory_symlink('"{0}/api/studio/lib"'.format(fmod_src_folder), fmod_dest_folder+'/studio/macosx/lib')
      run('cp "{0}/doc/LICENSE.TXT" {1}'.format(fmod_src_folder, fmod_dest_folder))
      run('cp "{0}/doc/revision.txt" {1}'.format(fmod_src_folder, fmod_dest_folder))
    else:
      print('--- FMOD not found at {0}, creating stub folders'.format(fmod_src_folder))
      print('consider downloading and installing https://www.fmod.com/download#fmodengine - Mac Download')
      pathlib.Path(fmod_dest_folder+'/core/macosx/inc').mkdir(parents=True, exist_ok=True)
      pathlib.Path(fmod_dest_folder+'/studio/macosx/inc').mkdir(parents=True, exist_ok=True)


  # DXC-1.8.2505.1
  dxc_dest_folder = dest_dir+'/DXC-1.8.2505.1'
  if pathlib.Path(dxc_dest_folder).exists():
    print('=== DXC May 2025 - Patch 1 -- 1.8.2505.1 found at {0}, skipping setup'.format(dxc_dest_folder))
  else:
    download_url(DEVTOOLS_RELEASES_URL+'/dxc-1.8.2505.1/DXC-1.8.2505.1.tar.gz', dest_dir)
    with tarfile.open(os.path.normpath(dest_dir+'/.packages/DXC-1.8.2505.1.tar.gz'), 'r:gz') as tar_file:
      tar_file.extractall(dest_dir)
      tar_file.close()
      shutil.rmtree(dxc_dest_folder+'/lib/linux64')
      shutil.rmtree(dxc_dest_folder+'/lib/win64')
      shutil.rmtree(dxc_dest_folder+'/lib/win-arm64')
      print('+++ DXC May 2025 - Patch 1 -- 1.8.2505.1 installed at {0}'.format(dxc_dest_folder))

  # astcenc-4.6.1
  astcenc_dest_folder = dest_dir+'/astcenc-4.6.1'
  if pathlib.Path(astcenc_dest_folder).exists():
    print('=== ASTC encoder 4.6.1 {0}, skipping setup'.format(astcenc_dest_folder))
  else:
    download_url('https://github.com/ARM-software/astc-encoder/releases/download/4.6.1/astcenc-4.6.1-macos-universal.zip', dest_dir)
    with zipfile.ZipFile(os.path.normpath(dest_dir+'/.packages/astcenc-4.6.1-macos-universal.zip'), 'r') as zip_file:
      zip_file.extractall(dest_dir+'/astcenc-4.6.1')
      os.rename(os.path.normpath(dest_dir+'/astcenc-4.6.1/bin'), os.path.normpath(dest_dir+'/astcenc-4.6.1/macosx'));
      run('chmod 755 '+dest_dir+'/astcenc-4.6.1/macosx/astcenc*')
      print('+++ ASTC encoder 4.6.1 installed at {0}'.format(astcenc_dest_folder))

  # ispc-v1.23.0
  ispc_dest_folder = dest_dir+'/ispc-v1.23.0-macOS.x86_64'
  if pathlib.Path(ispc_dest_folder).exists():
    print('=== ISPC v1.23.0 {0}, skipping setup'.format(ispc_dest_folder))
  else:
    download_url('https://github.com/ispc/ispc/releases/download/v1.23.0/ispc-v1.23.0-macOS.universal.tar.gz', dest_dir)
    with tarfile.open(os.path.normpath(dest_dir+'/.packages/ispc-v1.23.0-macOS.universal.tar.gz'), 'r:gz') as tar_file:
      tar_file.extractall(dest_dir)
      tar_file.close()
      print('+++ ISPC v1.23.0 installed at {0}'.format(ispc_dest_folder))


  try:
    subprocess.run(["jam", "-v"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
  except FileNotFoundError:
    print("jam not found, installing jam...")
    jam_zip = 'jam-macOS-11.0-arm64.tar.gz' if mac_proc_arm else 'jam-macOS-10.9-x64_86.tar.gz'
    download_url(JAM_RELEASE_URL+'/'+jam_zip, dest_dir)
    with tarfile.open(os.path.normpath(dest_dir+'/.packages/'+jam_zip), 'r:gz') as tar_file:
      tar_file.extractall(dest_dir)
      run('chmod 755 '+dest_dir+'/jam')
      print('--- will copy jam to /usr/local/bin using sudo:')
      run('sudo cp '+dest_dir+'/jam /usr/local/bin/jam')

  # re-write platform.jam
  if pathlib.Path("prog").exists():
    with open('prog/platform.jam', 'w') as fd:
      fd.write('_DEVTOOL = {0} ;\n'.format(dest_dir))
      if pathlib.Path(fmod_dest_folder+'/LICENSE.TXT').exists():
        fd.write('FmodStudio = 2.xx.xx ;\n')
      else:
        fd.write('FmodStudio = none ;\n')
      fd.close()
    print('--- will prepare {0}/mac folder using jamfile:'.format(dest_dir))
    run('sudo jam -sRoot=. -f prog/engine/kernel/jamfile mkdevtools');


# --- projects --------------------------------------------------------------------------------------------------------

# A game project is made from a template of templates/ (dagor.py new) and can be anywhere: its application.blk names
# the engine it is built with (engineRoot:t="<engine root, relative to the project dir or absolute>"), which the game
# and the tools read too (the %engine named mount). setup_project() writes the project's files that depend on the
# engine's path and on the project's lib lists (prog/danetgamelibs.txt, prog/gamelibs.txt): they start with _ and are
# not committed. The project's build.py runs it before each build; dagor.py relink after pointing engineRoot here.
TEMPLATES_DIR = os.path.join(DAGOR_ROOT_FOLDER, 'templates')
TEMPLATE_BLK = 'template.blk'
TEMPLATE_TOKENS = ('bundleId', 'title', 'name', 'codename')
ENGINE_ROOT_RE = re.compile(r'^([ \t]*engineRoot[ \t]*:[ \t]*t[ \t]*=[ \t]*)"((?:[^"~\n]|~.)*)"', re.MULTILINE)
GENERATED_NOTE = 'written by dagor.py from application.blk (engineRoot) and prog/*libs.txt: not committed, do not edit'

def norm_path(path):
  return os.path.normpath(os.path.abspath(path)).replace('\\', '/')

def is_engine_root(path):
  return os.path.isfile(os.path.join(path, 'prog', '_jBuild', 'defaults.jam'))

def blk_escape(s):
  return s.replace('~', '~~').replace('"', '~"')

def blk_unescape(s):
  return re.sub(r'~(.)', lambda m: {'n': '\n', 't': '\t', 'r': '\r'}.get(m.group(1), m.group(1)), s)

def read_text(path):
  with open(path, 'rb') as f:
    raw = f.read().decode('utf-8')
  return raw.replace('\r\n', '\n'), '\r\n' if '\r\n' in raw else '\n'

def write_text(path, text, newline='\n'):
  data = text.replace('\n', newline).encode('utf-8')
  if os.path.isfile(path):
    with open(path, 'rb') as f:
      if f.read() == data:
        return # unchanged: jam and the tools see no new file
  os.makedirs(os.path.dirname(path), exist_ok=True)
  with open(path, 'wb') as f:
    f.write(data)

def project_engine_root(project_dir):
  fn = os.path.join(project_dir, 'application.blk')
  if not os.path.isfile(fn):
    error('{0} is not a game project: it has no application.blk'.format(project_dir))
  m = ENGINE_ROOT_RE.search(read_text(fn)[0])
  if not m or not m.group(2):
    error('{0}: expected engineRoot:t="<path to the engine>"'.format(fn))
  root = norm_path(os.path.join(project_dir, blk_unescape(m.group(2))))
  if not is_engine_root(root):
    error('{0}: engineRoot "{1}" is not a Dagor Engine (no prog/_jBuild/defaults.jam in it); point it at one with '
          'python <engine>/dagor.py relink {2}'.format(fn, m.group(2), project_dir))
  return root

def set_project_engine_root(project_dir, engine_root, absolute=False):
  try:
    value = engine_root if absolute else os.path.relpath(engine_root, project_dir)
  except ValueError: # another drive
    value = engine_root
  fn = os.path.join(project_dir, 'application.blk')
  text, newline = read_text(fn)
  if not ENGINE_ROOT_RE.search(text):
    error('{0} has no engineRoot:t="" line'.format(fn))
  value = blk_escape(value.replace('\\', '/'))
  write_text(fn, ENGINE_ROOT_RE.sub(lambda m: '{0}"{1}"'.format(m.group(1), value), text, count=1), newline)

def setup_project(project_dir):
  project_dir = norm_path(project_dir)
  engine = project_engine_root(project_dir)
  prog = project_dir + '/prog'
  try:
    engine_from_prog = os.path.relpath(engine, prog).replace('\\', '/')
    prog_from_engine = os.path.relpath(prog, engine).replace('\\', '/')
  except ValueError:
    error('{0} is on another drive than its engine {1}: jam builds it only from the same drive'.format(project_dir, engine))
  cdk = '{0}/{1}'.format(engine, os.path.relpath(DAGOR_TOOLS_FOLDER, DAGOR_ROOT_FOLDER).replace('\\', '/'))

  # the engine for jam (prog/jamfile, prog/jamfile-aot) and for the scripts of the project (develop/, game/)
  write_text(prog + '/_engine.jam',
    '# {0}\nEngineRoot = {1} ; # relative to prog/, where jam runs\nProjectLocation = {2} ; # prog/, relative to the engine\n'
    .format(GENERATED_NOTE, engine_from_prog, prog_from_engine))
  write_text(project_dir + '/_engine.cmd',
    '@rem {0}\n@set "DAGOR_ENGINE_ROOT={1}"\n@set "DAGOR_CDK_DIR={2}"\n'.format(GENERATED_NOTE, engine, cdk), '\r\n')
  write_text(project_dir + '/_engine.sh',
    '# {0}\n# source it: . _engine.sh\nexport DAGOR_ENGINE_ROOT="{1}"\nexport DAGOR_CDK_DIR="{2}"\n'.format(GENERATED_NOTE, engine, cdk))

  # the libs: their code (jam), daScript (loaded by load_libs()), entity templates, shaders and vromfs content
  m = re.search(r'^[ \t]*output[ \t]*:[ \t]*t[ \t]*=[ \t]*"([^"]+)"', read_text(prog + '/prog.vromfs.blk')[0], re.MULTILINE)
  if not m:
    error('{0}/prog.vromfs.blk names no output:t=""'.format(prog))
  vromfs_name = m.group(1)
  jam = aot_jam = vromfs = templates = shaders = requires = loads = ''
  for list_name, libs_dir, mount in (('danetgamelibs.txt', 'daNetGameLibs', 'danetlibs'), ('gamelibs.txt', 'gameLibs', 'gameLibs')):
    list_path = os.path.join(prog, list_name)
    if not os.path.isfile(list_path):
      continue
    for line in read_text(list_path)[0].split('\n'):
      lib = line.split('#', 1)[0].strip()
      if not lib:
        continue
      lib_rel = 'prog/{0}/{1}'.format(libs_dir, lib)
      lib_dir = os.path.join(engine, lib_rel)
      if not os.path.isdir(lib_dir):
        error('{0}: there is no {1} in the engine ({2})'.format(list_path, lib, engine))
      name = lib.split('/')[-1]
      if os.path.isfile(os.path.join(lib_dir, name + '_init.das')):
        requires += 'require {0}.{1}.{2}_init\n'.format(mount, lib.replace('/', '.'), name)
        loads += '  ok = load_{0}("%{1}/{2}") && ok\n'.format(name, mount, lib)
      if os.path.isfile(os.path.join(lib_dir, '_lib.jam')):
        jam += 'include $(Root)/{0}/_lib.jam ;\n'.format(lib_rel)
      if os.path.isfile(os.path.join(lib_dir, '_aot.jam')):
        aot_jam += 'include $(Root)/{0}/_aot.jam ;\n'.format(lib_rel)
      if os.path.isfile(os.path.join(lib_dir, '_shaders.blk')):
        shaders += 'include "%engine/{0}/_shaders.blk"\n'.format(lib_rel)
      if os.path.isdir(os.path.join(lib_dir, 'templates')):
        for template in sorted(os.listdir(os.path.join(lib_dir, 'templates'))):
          templates += 'import:t="%{0}/{1}/templates/{2}"\n'.format(mount, lib, template)
      if os.path.isdir(os.path.join(lib_dir, 'sq_stubs')):
        copy_tree(os.path.join(lib_dir, 'sq_stubs'), project_dir + '/stubs')
      wildcards = ''
      for ext in ('.blk', '.das', '.das_project'):
        if any(os.path.basename(f) != '_shaders.blk' for f in glob.glob(lib_dir + '/**/*' + ext, recursive=True)):
          wildcards += '  wildcard:t="*{0}"\n'.format(ext)
      if wildcards:
        vromfs += ('\nfolder {{\n  output:t="{0}"\n  path:t="%engine/{1}/"\n  dest_path:t="{2}/{3}/"\n  scan_folder:b=true\n'
                   '  scan_subfolders:b=true\n{4}}}\n').format(vromfs_name, lib_rel, mount, lib, wildcards)
  das_init = ('options gen2\n\n// {0}\n\noptions no_aot = true\n{1}\ndef load_libs() : bool {{\n  {2} ok = true\n{3}  return ok\n}}\n\n'
              '[export]\ndef test_all {{\n  let ok = load_libs()\n  assert(ok)\n}}\n').format(GENERATED_NOTE, requires,
              'var' if loads else 'let', loads)
  write_text(prog + '/_libs.jam', '# {0}\n{1}'.format(GENERATED_NOTE, jam))
  write_text(prog + '/_aot_libs.jam', '# {0}\n{1}'.format(GENERATED_NOTE, aot_jam))
  write_text(prog + '/_libs.vromfs.blk', '// {0}\n{1}'.format(GENERATED_NOTE, vromfs))
  write_text(prog + '/gameBase/gamedata/templates/_libs.entities.blk', '// {0}\n{1}'.format(GENERATED_NOTE, templates))
  write_text(prog + '/shaders/_libs_shaders.blk', '// {0}\n{1}'.format(GENERATED_NOTE, shaders))
  write_text(prog + '/scripts/_libs_init.das', das_init)
  write_text(prog + '/tools/_libs_init.das', das_init)

# the templates (dirs with a template.blk, not starting with _): {id: description}
def list_templates():
  out = {}
  if os.path.isdir(TEMPLATES_DIR):
    for d in sorted(os.listdir(TEMPLATES_DIR)):
      if not d.startswith('_') and os.path.isfile(os.path.join(TEMPLATES_DIR, d, TEMPLATE_BLK)):
        out[d] = read_template(d)['description']
  return out

def blk_params(text, name, kind='t'):
  value = r'"([^"]*)"' if kind == 't' else r'(\w+)'
  return re.findall(r'^\s*' + name + r'\s*:\s*' + kind + r'\s*=\s*' + value, text, re.MULTILINE)

# a template: its description, its dirs (the layers it names, then its own; each one's files replace those of the dirs
# before it) and the name tokens of the layers (tokens{} of their template.blk), replaced in file names and text
def read_template(template_id):
  own = os.path.join(TEMPLATES_DIR, template_id)
  fn = os.path.join(own, TEMPLATE_BLK)
  if template_id.startswith('_') or not os.path.isfile(fn):
    error('no template "{0}" in {1} (dagor.py new --list)'.format(template_id, TEMPLATES_DIR))
  text = read_text(fn)[0]
  dirs = []
  for layer in blk_params(text, 'layer'):
    d = os.path.join(TEMPLATES_DIR, layer)
    if not layer.startswith('_') or not os.path.isdir(d):
      error('{0}: layer "{1}" is not a layer dir (_<name>) of {2}'.format(fn, layer, TEMPLATES_DIR))
    dirs.append(d)
  dirs.append(own)
  tokens = {}
  for d in dirs:
    if os.path.isfile(os.path.join(d, TEMPLATE_BLK)):
      m = re.search(r'tokens\s*\{([^}]*)\}', read_text(os.path.join(d, TEMPLATE_BLK))[0])
      if m:
        tokens.update({k: v[0] for k in TEMPLATE_TOKENS for v in [blk_params(m.group(1), k)] if v})
  missing = [k + ':t=' for k in TEMPLATE_TOKENS if not tokens.get(k)]
  if missing:
    error('{0}: the tokens{{}} of its layers miss {1}'.format(fn, ', '.join(missing)))
  return {'description': (blk_params(text, 'description') or [''])[0], 'dirs': dirs, 'tokens': tokens}

# the files of a template dir that git tracks or would track (without git: all but its template.blk)
def template_dir_files(d):
  try:
    out = subprocess.run(['git', 'ls-files', '-z', '--cached', '--others', '--exclude-standard', '--', '.'], cwd=d,
                         capture_output=True, check=True).stdout.decode('utf-8')
    files = [f for f in out.split('\0') if f and os.path.isfile(os.path.join(d, f))]
  except (OSError, subprocess.CalledProcessError):
    files = [os.path.relpath(os.path.join(dp, f), d).replace('\\', '/') for dp, _, fs in os.walk(d) for f in fs]
  return sorted(f for f in files if f != TEMPLATE_BLK)

def substitute(text, tokens): # one pass, the longest token first: a replacement is never replaced again
  mapping = dict(tokens)
  return re.sub('|'.join(re.escape(old) for old, _ in tokens), lambda m: mapping[m.group(0)], text)

def split_words(name): # PascalCase words: MyGame -> My Game, HTTPServer2 -> HTTP Server2
  return re.findall(r'[A-Z]?[a-z0-9]+|[A-Z0-9]+(?![a-z])', name)

def new_project(argv):
  import argparse
  p = argparse.ArgumentParser(prog='dagor.py new', description='Creates a game project from a template of templates/. '
    'The project can be anywhere on the engine\'s drive: its application.blk names this engine.')
  p.add_argument('--template', default='mp-3d', help='the template (default: mp-3d; --list shows them)')
  p.add_argument('--name', help='PascalCase name, e.g. MyGame')
  p.add_argument('--dest', help='the project dir to create (default: ../<name> next to the engine)')
  p.add_argument('--codename', help='lowercase name of the executables and dirs (default: from --name, my_game)')
  p.add_argument('--title', help='human readable name (default: from --name, "My Game")')
  p.add_argument('--company', default='com.example', help='reverse domain name of the bundle ids (default: com.example)')
  p.add_argument('--absolute-engine-path', action='store_true', help='names the engine by its absolute path')
  p.add_argument('--no-git', action='store_true', help='does not run git init in the new project')
  p.add_argument('--force', action='store_true', help='writes into an existing non-empty dir')
  p.add_argument('--list', action='store_true', help='lists the templates')
  args = p.parse_args(argv)
  if args.list:
    for template_id, description in list_templates().items():
      print('{0:8} {1}'.format(template_id, description))
    return
  if not args.name:
    p.error('--name is required')
  name, company = args.name, args.company
  codename = args.codename or '_'.join(w.lower() for w in split_words(name))
  title = args.title or ' '.join(split_words(name))
  dest = norm_path(args.dest or os.path.join(DAGOR_ROOT_FOLDER, '..', name))
  if not re.match(r'^[A-Z][A-Za-z0-9]*$', name):
    error('--name must be PascalCase ASCII letters and digits (like MyGame), not "{0}"'.format(name))
  if not re.match(r'^[a-z][a-z0-9_]*$', codename):
    error('--codename must be lowercase letters, digits and _ (like my_game), not "{0}"'.format(codename))
  if not title.strip() or '"' in title or '\\' in title:
    error('--title must be non-empty, without " or \\')
  if not re.match(r'^[A-Za-z][A-Za-z0-9-]*(\.[A-Za-z][A-Za-z0-9-]*)+$', company):
    error('--company must be a reverse domain name (like com.example), not "{0}"'.format(company))
  if contains_spaces(dest) or contains_non_ascii(dest):
    error('the project dir must be an ASCII path without spaces (the build tools need it), not "{0}"'.format(dest))
  if (dest + '/').startswith(norm_path(TEMPLATES_DIR) + '/'):
    error('the project dir is inside the templates')
  if os.path.exists(dest) and (not os.path.isdir(dest) or os.listdir(dest)) and not args.force:
    error('{0} exists and is not empty (--force writes into it anyway)'.format(dest))

  template = read_template(args.template)
  values = {'bundleId': company + '.' + name, 'title': title, 'name': name, 'codename': codename}
  tokens = sorted(((template['tokens'][k], values[k]) for k in TEMPLATE_TOKENS), key=lambda t: -len(t[0]))
  files = {}
  for d in template['dirs']:
    files.update({rel: os.path.join(d, rel) for rel in template_dir_files(d)})
  print('creating "{0}" ({1}) from the {2} template in {3}'.format(title, codename, args.template, dest))
  for rel, src in sorted(files.items()):
    out = os.path.join(dest, substitute(rel, tokens))
    with open(src, 'rb') as f:
      data = f.read()
    if b'\0' not in data:
      data = substitute(data.decode('utf-8'), tokens).encode('utf-8')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, 'wb') as f:
      f.write(data)
    shutil.copymode(src, out) # keeps scripts executable
  set_project_engine_root(dest, norm_path(DAGOR_ROOT_FOLDER), args.absolute_engine_path)
  setup_project(dest)
  if not args.no_git and shutil.which('git') and not os.path.isdir(os.path.join(dest, '.git')):
    subprocess.run(['git', 'init', '-q'], cwd=dest, check=True)
    print('initialized a git repository in it (nothing committed)')
  script = '.cmd' if DAGOR_HOST == 'windows' else '.sh'
  print('\nNext, in {0}:\n  python3 prog/build.py      the game and its content (the engine tools must be built: dagor.py build)\n'
        '  game/client{1}            runs the game\n  develop/daEditor{1}       opens the editor\nSee its README.md.'
        .format(dest, script))

def relink_project(argv):
  import argparse
  p = argparse.ArgumentParser(prog='dagor.py relink', description='Points a game project at this engine (after either '
    'moved): its application.blk names it, and its generated files (_*) are written again.')
  p.add_argument('project', help='the project dir')
  p.add_argument('--absolute-engine-path', action='store_true', help='names the engine by its absolute path')
  args = p.parse_args(argv)
  set_project_engine_root(norm_path(args.project), norm_path(DAGOR_ROOT_FOLDER), args.absolute_engine_path)
  setup_project(args.project)
  print('{0} is built with {1} now'.format(norm_path(args.project), norm_path(DAGOR_ROOT_FOLDER)))


# --- check-hosts -----------------------------------------------------------------------------------------------------

# The engine contacts and downloads nothing of Gaijin's: no Gaijin hosts or app IDs, no downloads from the releases of
# Gaijin's GitHub repositories (upstream syncs bring them back). Comments, the docs and the vendored daScript and Quirrel
# (projects with their own repositories) are not checked.
GAIJIN_REFS_GIT_PATTERN = (r'(gaijin|gaijinent|gaijingames|warthunder|enlisted|crossout)\.(net|com|ru|team|lan|ops|io)'
                           r'|com[./_]gaijin|github\.com/GaijinEntertainment/[^/ ]+/releases')
GAIJIN_REFS_RE = re.compile(r'\b(?:gaijin|gaijinent|gaijingames|warthunder|enlisted|crossout)\.(?:net|com|ru|team|lan|ops|io)\b'
                            r'|\bcom[./_]gaijin|github\.com/GaijinEntertainment/[^/ ]+/releases')
GAIJIN_REFS_EXCLUDE = ['_docs', '*.md', 'prog/1stPartyLibs/daScript', 'prog/1stPartyLibs/quirrel']
COMMENT_START_RE = re.compile(r'(?<!:)//|/\*|#|<!--|^\s*(?:\*|;|--|rem\s)', re.IGNORECASE)

def check_hosts():
  try:
    grep = subprocess.run(['git', 'grep', '-n', '-I', '-E', GAIJIN_REFS_GIT_PATTERN, '--', '.'] +
                          [':(exclude){0}'.format(p) for p in GAIJIN_REFS_EXCLUDE],
                          cwd=DAGOR_ROOT_FOLDER, capture_output=True, encoding='utf-8', errors='replace')
  except OSError:
    print('--- check-hosts skipped: git not found')
    return True
  if grep.returncode > 1:
    print('--- check-hosts skipped: {0}'.format(grep.stderr.strip()))
    return True
  found = []
  for line in grep.stdout.splitlines():
    path, num, text = line.split(':', 2)
    m = GAIJIN_REFS_RE.search(text)
    if m and not COMMENT_START_RE.search(text[:m.start()]):
      found.append('{0}:{1}: {2}'.format(path, num, text.strip()))
  if found:
    print('\nERROR: Gaijin hosts, app IDs or release downloads (use the fork\'s own, see check_hosts in dagor.py):\n  ' +
          '\n  '.join(found) + '\n')
  return not found


# --- build -----------------------------------------------------------------------------------------------------------

# copies the files of src_root into dest_root that are missing or differ there (deletes nothing)
def copy_tree(src_root, dest_root, skip=()):
  copied = 0
  for src_dir, _, files in os.walk(src_root):
    dest_dir = os.path.join(dest_root, os.path.relpath(src_dir, src_root))
    for name in files:
      src, dest = os.path.join(src_dir, name), os.path.join(dest_dir, name)
      if os.path.relpath(src, src_root).replace('\\', '/') in skip:
        continue
      if not os.path.isfile(dest) or not filecmp.cmp(src, dest, shallow=False):
        os.makedirs(dest_dir, exist_ok=True)
        shutil.copyfile(src, dest)
        copied += 1
  return copied

# copies prog/tools/toolsData (the tools' data that is not built: editor commonData, Scintilla, dargbox's fonts and UI)
# into tools/, the files that differ
def copy_tools_data():
  src_root = os.path.join(DAGOR_ROOT_FOLDER, 'prog', 'tools', 'toolsData')
  dest_root = os.path.join(DAGOR_ROOT_FOLDER, 'tools')
  if DRY_RUN:
    print('DRY_RUN: copy {0} > {1}'.format(src_root, dest_root))
    return
  copied = copy_tree(src_root, dest_root, skip=('README.md',))
  print('--- tools data: {0} files copied into {1}'.format(copied, dest_root))

def build():
  # gather build projects from commandline (to allow partial builds)
  BUILD_PROJECTS = []
  for s in ARGS:
    if s.startswith('project:'):
      BUILD_PROJECTS += [s[8:]]
  # when no projects specified we build all of them
  if len(BUILD_PROJECTS) == 0:
    BUILD_PROJECTS = ['dagorTools', 'dargbox', 'physTest']

  if not check_hosts():
    exit(1)

  # the tools' data (no download)
  if 'dagorTools' in BUILD_PROJECTS or 'dargbox' in BUILD_PROJECTS:
    copy_tools_data()

  # build command line to run other build scripts
  PY_ADD_CMDLINE = BUILD_COMPONENTS
  if BUILD_TARGET_ARCH != '':
    PY_ADD_CMDLINE += ['arch:'+BUILD_TARGET_ARCH]

  # core CDK (tools and dargbox)
  if 'dagorTools' in BUILD_PROJECTS and 'code' in BUILD_COMPONENTS:
    proj_dir = 'prog/tools'
    if DAGOR_HOST == 'windows':
      BUILD_TOOLS_CMD = 'build_dagor_cdk_mini.cmd'
      if BUILD_TARGET_ARCH != '':
        BUILD_TOOLS_CMD += ' ' + BUILD_TARGET_ARCH
      if not run(BUILD_TOOLS_CMD, cwd=proj_dir):
        print('"{}" failed, trying once more...'.format(BUILD_TOOLS_CMD))
        if not run(BUILD_TOOLS_CMD, cwd=proj_dir):
          print('echo failed to build CDK, stop!')
          exit(1)
    elif DAGOR_HOST == 'macOS':
      BUILD_TOOLS_CMD = './build_dagor_cdk_mini_macOS.sh'
      if BUILD_TARGET_ARCH != '':
        BUILD_TOOLS_CMD += ' ' + BUILD_TARGET_ARCH
      run(BUILD_TOOLS_CMD, cwd=proj_dir)
    elif DAGOR_HOST == 'linux':
      run('./build_dagor_cdk_mini_linux.sh', cwd=proj_dir)

  # dargbox tool
  if 'dargbox' in BUILD_PROJECTS:
    run([sys.executable, './build.py'] + PY_ADD_CMDLINE, cwd='prog/tools/dargbox')

  # physTest sample
  if 'physTest' in BUILD_PROJECTS:
    run([sys.executable, './build.py'] + PY_ADD_CMDLINE, cwd='prog/samples/physTest')


if __name__ == '__main__':
  command = sys.argv[1] if len(sys.argv) > 1 else ''
  if command == 'devtools' and len(sys.argv) == 3:
    devtools(sys.argv[2])
  elif command == 'build':
    build()
  elif command == 'check-hosts':
    exit(0 if check_hosts() else 1)
  elif command == 'new':
    new_project(sys.argv[2:])
  elif command == 'relink':
    relink_project(sys.argv[2:])
  else:
    print('\nUsage: dagor.py devtools DEVTOOLS_DEST_DIR\n' +
          '       dagor.py build [project:<name>...] [code] [shaders] [assets] [vromfs] [gui] [arch:<arch>] [--dry-run]\n' +
          '       dagor.py new --name <Name> [--template <template>] [--dest <dir>] ... (see dagor.py new --help)\n' +
          '       dagor.py relink <project dir>\n' +
          '       dagor.py check-hosts\n' +
          'example: python3 dagor.py devtools {0}\n'.format('d:\\devtools' if DAGOR_HOST == 'windows' else '~/devtools'))
    exit(1)
