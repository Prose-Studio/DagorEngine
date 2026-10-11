"""The CMake build of the engine and of game projects, as dng.py and project.py run it.

A build tree is one variant of the engine (tests, cdk, editor, maxplug, dargbox, all) or of a game (client, dedicated)
for one target: the platform, architecture and compiler, and optionally a sanitizer, coverage or LTO. Its top-level
CMakeLists.txt is the prog/ of the engine or of the project; the tree is build/<name> of that root, named after what
differs from the host's defaults: windows-tests, windows-msvc-maxplug, linux-asan-tests, macos-universal-cdk, ...
The cache variables of each choice are set here (the CMake modules are in prog/cmake).
"""
import argparse
import os
import platform
import shutil
import subprocess
import sys

ENGINE_ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..'))

CONFIGS = ('Dev', 'Rel', 'IRel', 'Dbg')

# the engine's variants and the cache variables they set beside DAGOR_VARIANT
ENGINE_VARIANTS = {
  'tests': {'DAGOR_CHECKED_CONTAINERS_CONFIGS': 'Dev;Dbg', 'DAGOR_EXCEPTIONS_CONFIGS': 'Dev;Rel;IRel;Dbg',
            'DAGOR_FORCE_LOGS': 'ON'},
  'cdk': {},
  'editor': {'DAGOR_KERNEL_LINKAGE': 'dynamic'},
  'maxplug': {'DAGOR_EXCEPTIONS_CONFIGS': 'Dev;Rel;IRel;Dbg', 'DAGOR_RTTI': 'ON'},
  'dargbox': {},
  'all': {},
}
# the variants whose programs go into tools/dagor_cdk/<platform>-<arch> (the install components)
INSTALLED = {'cdk': ('cdk', 'cdk-data'), 'editor': ('cdk',)}
# (with the tests registered: trees made before they were on by default keep their cached value otherwise)
GAME_VARIANTS = {'client': {'DAGOR_DEDICATED': 'OFF', 'DAGOR_BUILD_TESTS': 'ON'},
                 'dedicated': {'DAGOR_DEDICATED': 'ON', 'DAGOR_BUILD_TESTS': 'ON'}}

PLATFORMS = ('windows', 'linux', 'macOS', 'android', 'iOS', 'tvOS')
COMPILERS = ('clang', 'msvc', 'gcc', 'lcc')
SANITIZERS = ('address', 'undefined', 'thread')
SANITIZER_TAGS = {'address': 'asan', 'undefined': 'ubsan', 'thread': 'tsan'}
# test labels of what hosted CI runners cannot run
CI_EXCLUDED_LABELS = 'requires-gpu|requires-display'


def _host():
  if sys.platform.startswith('win'):
    cpu = os.environ.get('PROCESSOR_IDENTIFIER', '')
    arm = os.environ.get('PROCESSOR_ARCHITECTURE', '') == 'ARM64' or ('ARMv' in cpu and '64-bit' in cpu)
    return 'windows', 'arm64' if arm else 'x86_64'
  if sys.platform.startswith('darwin'):
    return 'macOS', 'arm64' if platform.machine() == 'arm64' else 'x86_64'
  if sys.platform.startswith('linux'):
    machine = platform.machine()
    return 'linux', {'aarch64': 'arm64', 'amd64': 'x86_64'}.get(machine, machine)
  sys.exit('unsupported host platform {}'.format(sys.platform))


HOST, HOST_ARCH = _host()


class Target:
  """What a tree builds for: platform, arch, compiler and instrumentation."""

  def __init__(self, platform=None, arch=None, compiler=None, msvc_toolset=None, sanitize=None, coverage=False,
               lto=None, generator=None, defines=()):
    self.platform = platform or HOST
    if self.platform not in PLATFORMS:
      raise ValueError('unknown platform {} (expected one of {})'.format(self.platform, ', '.join(PLATFORMS)))
    self.arch = arch or (HOST_ARCH if self.platform == HOST else 'arm64' if self.platform in ('iOS', 'tvOS', 'android')
                         else 'x86_64')
    self.sanitize = sanitize
    self.coverage = coverage
    self.lto = lto
    self.compiler = compiler or self.default_compiler()
    if self.compiler not in COMPILERS:
      raise ValueError('unknown compiler {} (expected one of {})'.format(self.compiler, ', '.join(COMPILERS)))
    self.msvc_toolset = msvc_toolset
    self.generator = generator
    self.defines = list(defines)

  def default_compiler(self):
    if self.platform == 'linux':
      if self.arch == 'e2k':
        return 'lcc'
      # the LLVM-only instrumentation
      return 'clang' if self.coverage or self.sanitize in ('undefined', 'thread') else 'gcc'
    return 'clang'

  def tag(self):
    """windows, windows-arm64, windows-msvc, windows-vc16, linux-clang, linux-e2k, macos-universal, linux-asan, ..."""
    parts = [self.platform.lower()]
    if self.arch != (HOST_ARCH if self.platform == HOST else 'x86_64') and not (self.platform == 'macOS' and
                                                                                 self.arch in ('x86_64', 'arm64')):
      parts.append(self.arch)
    if self.msvc_toolset == '14.29':
      parts.append('vc16')
    elif self.compiler != self.default_compiler():
      parts.append(self.compiler)
    if self.sanitize:
      parts.append(SANITIZER_TAGS[self.sanitize])
    if self.coverage:
      parts.append('coverage')
    if self.lto:
      parts.append('lto')
    if self.generator:
      parts.append({'Xcode': 'xcode'}.get(self.generator, 'vs' if self.generator.startswith('Visual Studio') else
                                         self.generator.split()[0].lower()))
    return '-'.join(parts)

  def cache(self):
    values = {'DAGOR_PLATFORM': self.platform, 'DAGOR_ARCH': self.arch, 'DAGOR_COMPILER': self.compiler}
    if self.msvc_toolset:
      values['DAGOR_MSVC_TOOLSET'] = self.msvc_toolset
    if self.sanitize:
      values['DAGOR_SANITIZE'] = self.sanitize
    if self.coverage:
      values['DAGOR_COVERAGE'] = 'ON'
    if self.lto:
      values['DAGOR_LTO'] = self.lto
    if self.arch == 'e2k':
      values['DAGOR_WARNINGS_AS_ERRORS'] = 'OFF'  # lcc's warnings differ from the other compilers'
    return values


def add_target_arguments(p):
  """the command-line options of a Target"""
  g = p.add_argument_group('target')
  g.add_argument('--platform', choices=PLATFORMS, help='target platform (default: the host, {})'.format(HOST))
  g.add_argument('--arch', help='target architecture: x86_64, arm64, e2k, universal (macOS) (default: the host\'s)')
  g.add_argument('--compiler', choices=COMPILERS,
                 help='compiler family (default: clang, clang-cl on Windows; gcc on Linux; lcc on e2k)')
  g.add_argument('--msvc-toolset', metavar='VERSION', help='MSVC toolset of --compiler msvc, e.g. 14.29 (vc16)')
  g.add_argument('--sanitize', choices=SANITIZERS, help='build with a sanitizer')
  g.add_argument('--coverage', action='store_true', help='clang source-based code coverage')
  g.add_argument('--lto', choices=('thin', 'full'), help='link-time optimization')
  g.add_argument('--generator', help='CMake generator (default: Ninja Multi-Config), e.g. "Visual Studio 17 2022", Xcode')
  g.add_argument('-D', dest='defines', action='append', default=[], metavar='VAR=VALUE',
                 help='another cache variable of the tree (repeatable)')
  g.add_argument('--config', action='append', choices=CONFIGS, metavar='CONFIG',
                 help='configuration to build: {} (repeatable; default: Dev)'.format(', '.join(CONFIGS)))


def target_from_args(args):
  try:
    return Target(args.platform, args.arch, args.compiler, args.msvc_toolset, args.sanitize, args.coverage, args.lto,
                  args.generator, args.defines)
  except ValueError as e:
    sys.exit(str(e))


class Tree:
  """A build tree of <root>/prog: <root>/build/<target tag>-<variant>."""

  def __init__(self, root, variant, target, values, dry_run=False):
    self.root = os.path.abspath(root)
    self.source = os.path.join(self.root, 'prog')
    self.variant = variant
    self.target = target
    self.values = dict(target.cache())
    self.values.update(values)
    self.dir = os.path.join(self.root, 'build', '{}-{}'.format(target.tag(), variant))
    self.dry_run = dry_run

  def run(self, cmd, cwd=None):
    print('--- ' + ' '.join('"{}"'.format(c) if ' ' in c else c for c in cmd), flush=True)
    if self.dry_run:
      return True
    return subprocess.call(cmd, cwd=cwd or self.root) == 0

  def _configured_source(self):
    cache = os.path.join(self.dir, 'CMakeCache.txt')
    if not os.path.exists(cache):
      return None
    with open(cache, encoding='utf-8', errors='replace') as f:
      for line in f:
        if line.startswith('CMAKE_HOME_DIRECTORY:INTERNAL='):
          return os.path.normcase(os.path.normpath(line.split('=', 1)[1].strip()))
    return None

  def configure(self):
    """configures the tree (again: CMake reruns only what changed); a tree of another source dir is made anew"""
    configured = self._configured_source()
    if configured and configured != os.path.normcase(os.path.normpath(self.source)):
      print('--- {} was configured for {}: removing it'.format(self.dir, configured), flush=True)
      if not self.dry_run:
        shutil.rmtree(self.dir)
      configured = None
    cmd = [cmake(), '-S', self.source, '-B', self.dir]
    if not configured:
      cmd += ['-G', self.target.generator or 'Ninja Multi-Config']
    cmd += ['-D{}={}'.format(k, v) for k, v in self.values.items()] + ['-D' + d for d in self.target.defines]
    return self.run(cmd)

  def build(self, configs=('Dev',), targets=(), jobs=None):
    for config in configs:
      cmd = [cmake(), '--build', self.dir, '--config', config]
      if targets:
        cmd += ['--target'] + list(targets)
      if jobs:
        cmd += ['--parallel', str(jobs)]
      if not self.run(cmd):
        return False
    return True

  def install(self, config, components):
    return all(self.run([cmake(), '--install', self.dir, '--config', config, '--component', c]) for c in components)

  def package(self, config='Rel'):
    """the tree's package (CPack, see prog/cmake/DagorPackaging.cmake) of a built configuration"""
    return self.run([cpack(), '--config', os.path.join(self.dir, 'CPackConfig.cmake'), '-C', config])

  def test(self, config='Dev', ci=False, jobs=None, ctest_args=(), no_tests='error'):
    """runs the tests of the tree with CTest; no_tests: what a run without tests is (error or ignore)"""
    cmd = [ctest(), '--test-dir', self.dir, '-C', config, '--output-on-failure', '--no-tests=' + no_tests]
    if ci:
      cmd += ['-LE', CI_EXCLUDED_LABELS]
    if jobs:
      cmd += ['-j', str(jobs)]
    return self.run(cmd + list(ctest_args))


def _tool(name):
  path = shutil.which(name)
  if not path:
    sys.exit('{} not found: the build needs CMake 4.0 or newer and Ninja on the PATH '
             '(e.g. python -m pip install "cmake>=4.0,<5" ninja)'.format(name))
  return path


def cmake():
  return _tool('cmake')


def ctest():
  return _tool('ctest')


def cpack():
  return _tool('cpack')


def engine_tree(variant, target, dry_run=False):
  values = {'DAGOR_VARIANT': variant}
  values.update(ENGINE_VARIANTS[variant])
  return Tree(ENGINE_ROOT, variant, target, values, dry_run)


def game_tree(project_root, variant, target, dry_run=False):
  values = {'DAGOR_VARIANT': 'game'}
  values.update(GAME_VARIANTS[variant])
  return Tree(project_root, variant, target, values, dry_run)
