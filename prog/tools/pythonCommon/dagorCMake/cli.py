"""dng.py build and dng.py test on the CMake build (the jam build with --jam, until jam is deleted)."""
import argparse
import os
import subprocess
import sys

from . import (CONFIGS, ENGINE_ROOT, ENGINE_VARIANTS, INSTALLED, Target, add_target_arguments, engine_tree, game_tree,
               target_from_args)

# the projects of the engine checkout dng.py build builds: their project.py does
PROJECTS = {'dngEmpty': 'templates/dng-empty'}
DEFAULT = ['cdk', 'editor']

BUILD_EPILOG = '''examples:
  python dng.py build                          the engine tools (cdk, editor) into tools/dagor_cdk/<platform>-<arch>
  python dng.py build tests --config Rel       the unit tests tree, in Rel
  python dng.py build cdk --compiler msvc      with MSVC instead of clang-cl
  python dng.py build tests --sanitize address
  python dng.py build dngEmpty                 the project template (its project.py build)
  python dng.py build --jam [...]              the jam build (python dng.py build --jam -h)'''


def build_parser():
  p = argparse.ArgumentParser(prog='dng.py build', epilog=BUILD_EPILOG, formatter_class=argparse.RawDescriptionHelpFormatter,
                              description='Configures and builds trees of the engine (CMake) in build/<name>, and the '
                                          'engine\'s projects.')
  p.add_argument('items', nargs='*', metavar='TREE',
                 help='{} (engine variants) or {} (default: {})'.format(', '.join(ENGINE_VARIANTS), ', '.join(PROJECTS),
                                                                       ' '.join(DEFAULT)))
  add_target_arguments(p)
  p.add_argument('--target', action='append', default=[], metavar='TARGET', help='build only these targets (repeatable)')
  p.add_argument('-j', '--jobs', type=int, help='parallel build jobs (default: the build tool\'s)')
  p.add_argument('--configure-only', action='store_true', help='configure the trees without building them')
  p.add_argument('--dry-run', action='store_true', help='print the commands instead of running them')
  return p


def build(argv):
  args = build_parser().parse_args(argv)
  items = args.items or DEFAULT
  for item in items:
    if item not in ENGINE_VARIANTS and item not in PROJECTS:
      build_parser().error('unknown tree "{}": expected {} or {}'.format(item, ', '.join(ENGINE_VARIANTS), ', '.join(PROJECTS)))
  target = target_from_args(args)
  configs = args.config or ['Dev']
  for item in items:
    if item in PROJECTS:
      cmd = [sys.executable, 'project.py', 'build'] + (['--dry-run'] if args.dry_run else [])
      print('--- {} (in {})'.format(' '.join(cmd), PROJECTS[item]), flush=True)
      if subprocess.call(cmd, cwd=os.path.join(ENGINE_ROOT, PROJECTS[item])) != 0:
        print('ERROR: building {} failed'.format(item), flush=True)
        return 1
      continue
    tree = engine_tree(item, target, args.dry_run)
    if not tree.configure():
      print('ERROR: configuring {} failed'.format(tree.dir), flush=True)
      return 1
    if args.configure_only:
      continue
    if not tree.build(configs, args.target, args.jobs):
      print('ERROR: building {} failed'.format(tree.dir), flush=True)
      return 1
    if item in INSTALLED and not args.target:
      for config in configs:
        if not tree.install(config, INSTALLED[item]):
          print('ERROR: installing {} failed'.format(tree.dir), flush=True)
          return 1
  return 0


TEST_EPILOG = '''Arguments after the options go to ctest, e.g. -R datablock or -L cpp.

examples:
  python dng.py test                           builds the unit tests tree and runs every test
  python dng.py test --ci                      without the tests that need a GPU or a display
  python dng.py test --sanitize address -R kernel
  python dng.py test --jam [...]               the jam-built tests (python dng.py test --jam -h)'''


def test_parser():
  p = argparse.ArgumentParser(prog='dng.py test', epilog=TEST_EPILOG, formatter_class=argparse.RawDescriptionHelpFormatter,
                              description='Builds the engine\'s tests tree (CMake) and runs its tests with CTest.')
  add_target_arguments(p)
  p.add_argument('--ci', action='store_true', help='skip the tests labeled requires-gpu or requires-display')
  p.add_argument('-j', '--jobs', type=int, help='parallel build jobs and tests')
  p.add_argument('--no-build', action='store_true', help='run the tests that are already built')
  p.add_argument('--dry-run', action='store_true', help='print the commands instead of running them')
  return p


def test(argv):
  args, ctest_args = test_parser().parse_known_args(argv)
  target = target_from_args(args)
  configs = args.config or ['Dev']
  tree = engine_tree('tests', target, args.dry_run)
  if not args.no_build and not (tree.configure() and tree.build(configs, jobs=args.jobs)):
    print('ERROR: building {} failed'.format(tree.dir), flush=True)
    return 1
  ok = all([tree.test(config, args.ci, args.jobs or (4 if args.ci else None), ctest_args) for config in configs])
  return 0 if ok else 1


PROJECT_TEST_EPILOG = '''Arguments after the options go to ctest, e.g. -L ecs, -R dng_empty.das or --output-junit <file>.

The cpp, das and ecs tests are in the dedicated server's tree, the scenario tests (they render: GPU, display and the
game's shaders) in the client's. DAGOR_TEST_UPDATE_REFERENCES=1 in the environment makes scenario tests replace their
reference images.

examples:
  python project.py test                       builds the game and its tests, runs them all
  python project.py test --ci                  without the tests that need a GPU or a display (the dedicated tree)
  python project.py test -L ecs                only the ECS tests
  python project.py test --jam [...]           the jam-built tests (python project.py test --jam -h)'''


def project_test_parser():
  p = argparse.ArgumentParser(prog='project.py test', epilog=PROJECT_TEST_EPILOG,
                              formatter_class=argparse.RawDescriptionHelpFormatter,
                              description='Builds the game (project.py build code) and its tests (CMake), and runs '
                                          'them with CTest.')
  p.add_argument('--arch', help='the architecture of the build (default: the host\'s)')
  p.add_argument('--config', action='append', choices=CONFIGS, help='configurations to test (repeatable; default Dev)')
  p.add_argument('--game', choices=('dedicated', 'client', 'both'), default='both',
                 help='the trees whose tests run (default: both; the dedicated server\'s only with --ci)')
  p.add_argument('--ci', action='store_true', help='skip the tests labeled requires-gpu or requires-display')
  p.add_argument('-j', '--jobs', type=int, help='parallel build jobs and tests')
  p.add_argument('--no-build', action='store_true', help='run the tests that are already built')
  p.add_argument('--dry-run', action='store_true', help='print the commands instead of running them')
  return p


def project_test(project_root, argv):
  """project.py test: the game's code (the project's build.py, which knows its options) and the target tests of its
  trees, then CTest in each tree."""
  args, ctest_args = project_test_parser().parse_known_args(argv)
  configs = args.config or ['Dev']
  games = ['dedicated', 'client'] if args.game == 'both' else [args.game]
  if args.ci and args.game == 'both':
    games = ['dedicated']  # the client's tests all render
  target = Target(arch=args.arch)
  trees = [game_tree(project_root, g, target, args.dry_run) for g in games]
  if not args.no_build:
    cmd = [sys.executable, os.path.join(project_root, 'project.py'), 'build', 'code']
    cmd += (['arch:' + args.arch] if args.arch else []) + (['--dry-run'] if args.dry_run else [])
    print('--- ' + ' '.join(cmd), flush=True)
    if subprocess.call(cmd, cwd=project_root) != 0:
      print('ERROR: building the game failed', flush=True)
      return 1
    for tree in trees:
      if not (tree.build(configs, jobs=args.jobs) and tree.build(configs, ['tests'], args.jobs)):
        print('ERROR: building the tests of {} failed'.format(tree.dir), flush=True)
        return 1
  ok = True
  for tree in trees:
    for config in configs:
      ok = tree.test(config, args.ci, args.jobs, ctest_args, no_tests='ignore') and ok  # -L picks one tree's
  return 0 if ok else 1
