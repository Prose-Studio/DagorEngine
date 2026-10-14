#!/usr/bin/env python3
# DagorEngine's script:
#   dagor.py devtools DEVTOOLS_DEST_DIR
#       downloads and sets up the build tools of this host (compilers, SDKs, jam) in DEVTOOLS_DEST_DIR and writes
#       prog/platform.jam
#   dagor.py build [project:<name>...] [code] [shaders] [assets] [vromfs] [gui] [arch:<arch>] [--dry-run]
#       builds the engine tools and projects (dagorTools, dargbox, physTest: all when none is named), the components
#       named (all when none is)
# A project's build.py imports it for the build helpers: run, run_per_platform, the tools' paths and the components and
# arch of the project's own command line.
import sys

if not (sys.version_info.major >= 3 and sys.version_info.minor >= 5):
  print("\nERROR: Python 3.5 or a higher version is required to run this script.")
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
from urllib import request

COMMANDS = ['devtools', 'build']

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


# --- build -----------------------------------------------------------------------------------------------------------

def build():
  # gather build projects from commandline (to allow partial builds)
  BUILD_PROJECTS = []
  for s in ARGS:
    if s.startswith('project:'):
      BUILD_PROJECTS += [s[8:]]
  # when no projects specified we build all of them
  if len(BUILD_PROJECTS) == 0:
    BUILD_PROJECTS = ['dagorTools', 'dargbox', 'physTest']

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
  else:
    print('\nUsage: dagor.py devtools DEVTOOLS_DEST_DIR\n' +
          '       dagor.py build [project:<name>...] [code] [shaders] [assets] [vromfs] [gui] [arch:<arch>] [--dry-run]\n' +
          'example: python3 dagor.py devtools {0}\n'.format('d:\\devtools' if DAGOR_HOST == 'windows' else '~/devtools'))
    exit(1)
