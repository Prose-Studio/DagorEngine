"""Tests of dagorProject: engine.blk, the project presets and project creation from templates/dng-empty."""
import os
import re
import shutil
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, '..', '..', '..')))  # prog/tools: pythonCommon is importable
from pythonCommon.dagorProject import create, engine, presets  # noqa: E402
from pythonCommon.dagorProject.engine import ProjectError  # noqa: E402

ENGINE = create.engine_root()


class EngineBlkTest(unittest.TestCase):
  def setUp(self):
    self.dir = tempfile.mkdtemp()

  def tearDown(self):
    shutil.rmtree(self.dir, ignore_errors=True)

  def test_written_relative_and_read_back(self):
    engine.write_engine_blk(self.dir, ENGINE)
    with open(os.path.join(self.dir, 'engine.blk'), encoding='utf-8') as f:
      text = f.read()
    ref = re.search(r'engineRoot:t="([^"]*)"', text).group(1)
    if os.path.splitdrive(self.dir)[0].lower() == os.path.splitdrive(ENGINE)[0].lower():
      self.assertFalse(os.path.isabs(ref), ref)
    self.assertEqual(engine.read_engine_root(self.dir), ENGINE)

  def test_absolute_on_request(self):
    engine.write_engine_blk(self.dir, ENGINE, absolute=True)
    self.assertEqual(engine.read_engine_root(self.dir), ENGINE)
    with open(os.path.join(self.dir, 'engine.blk'), encoding='utf-8') as f:
      self.assertIn('engineRoot:t="{}"'.format(ENGINE), f.read())

  def test_the_engine_reads_only_the_engine_root_line(self):
    # prog/engine/osApiWrappers/namedMounts.cpp takes the first quoted string after "engineRoot": comments must not name it
    engine.write_engine_blk(self.dir, ENGINE)
    with open(os.path.join(self.dir, 'engine.blk'), encoding='utf-8') as f:
      lines = [l for l in f if 'engineRoot' in l]
    self.assertEqual(len(lines), 1)
    self.assertTrue(lines[0].startswith('engineRoot:t='))

  def test_blk_escapes(self):
    # ~ escapes in BLK strings (the engine reads engine.blk as a DataBlock), Windows short names have one: RUNNER~1
    with open(os.path.join(self.dir, 'engine.blk'), 'w') as f:
      f.write('engineRoot:t="C:/Users/RUNNER~~1/engine"\n')
    self.assertEqual(engine.read_engine_ref(self.dir), 'C:/Users/RUNNER~1/engine')

  def test_missing_and_wrong_engine_fail_clearly(self):
    with self.assertRaisesRegex(ProjectError, 'cannot read'):
      engine.read_engine_root(self.dir)
    with open(os.path.join(self.dir, 'engine.blk'), 'w') as f:
      f.write('engineRoot:t="no/such/dir"\n')
    with self.assertRaisesRegex(ProjectError, 'not a Dagor Engine checkout'):
      engine.read_engine_root(self.dir)
    with self.assertRaisesRegex(ProjectError, 'not a Dagor Engine checkout'):
      engine.write_engine_blk(self.dir, self.dir)

  def test_relative_or_absolute(self):
    self.assertEqual(engine.relative_or_absolute('C:/a/b/c', 'C:/a/d'), '../b/c') if os.name == 'nt' else None
    self.assertEqual(engine.relative_or_absolute(ENGINE, ENGINE + '/x', absolute=True), ENGINE)


class NamesTest(unittest.TestCase):
  def test_defaults_from_name(self):
    self.assertEqual(create.default_codename('MyGame'), 'my_game')
    self.assertEqual(create.default_title('MyGame'), 'My Game')
    self.assertEqual(create.default_codename('HTTPServer2'), 'http_server2')
    self.assertEqual(create.default_codename('E2eGame'), 'e2e_game')
    self.assertEqual(create.default_title('E2eGame'), 'E2e Game')

  def test_substitution_is_one_pass(self):
    tokens = [('Dng Empty', 'DngEmpty Ultra'), ('DngEmpty', 'MyGame')]  # longest first, as create() orders them
    self.assertEqual(create.substitute('Dng Empty / DngEmpty', tokens), 'DngEmpty Ultra / MyGame')
    self.assertFalse(create.tokens_left('DngEmpty Ultra', [('DngEmpty', 'DngEmpty Ultra')]))
    self.assertTrue(create.tokens_left('a DngEmpty', [('DngEmpty', 'MyGame')]))

  def test_validation(self):
    ok = dict(name='MyGame', codename='my_game', title='My Game', company='com.example', dest='C:/x')
    create.validate(**ok)
    for key, bad in (('name', 'my_game'), ('name', 'My Game'), ('codename', 'MyGame'), ('codename', '1x'),
                     ('title', ''), ('title', 'a"b'), ('company', 'example'), ('dest', 'C:/a b'), ('dest', 'C:/ä')):
      with self.subTest(key=key, value=bad), self.assertRaises(ProjectError):
        create.validate(**dict(ok, **{key: bad}))


class TemplateFilesTest(unittest.TestCase):
  def test_gitignore_fallback(self):
    d = tempfile.mkdtemp()
    try:
      for rel in ('keep.txt', 'game/run.cmd', 'game/x/big.exe', 'prog/_engine.jam', 'a/b/c.pyc', 'template.blk'):
        os.makedirs(os.path.dirname(os.path.join(d, rel)) or d, exist_ok=True)
        open(os.path.join(d, rel), 'w').close()
      with open(os.path.join(d, '.gitignore'), 'w') as f:
        f.write('/prog/_engine.jam\n/game/*\n!/game/*.cmd\n*.pyc\n')
      files = sorted(create._gitignore_files(d))
      self.assertEqual(files, ['.gitignore', 'game/run.cmd', 'keep.txt', 'template.blk'])
    finally:
      shutil.rmtree(d, ignore_errors=True)

  def test_dng_empty_tokens(self):
    _, tokens = create.read_template_blk(os.path.join(create.templates_dir(), 'dng-empty', create.TEMPLATE_BLK))
    self.assertEqual(tokens, {'bundleId': 'com.dagor.DngEmpty', 'title': 'Dng Empty', 'name': 'DngEmpty', 'codename': 'dng_empty'})


class CreateTest(unittest.TestCase):
  """Creates a real project from templates/dng-empty (no build: CI builds and tests one, see template.yaml)."""

  @classmethod
  def setUpClass(cls):
    cls.parent = tempfile.mkdtemp()
    cls.dest = os.path.join(cls.parent, 'MyGame')
    create.create('dng-empty', 'MyGame', cls.dest, company='org.test', git_init=False, log=lambda *a: None)

  @classmethod
  def tearDownClass(cls):
    shutil.rmtree(cls.parent, ignore_errors=True)

  def path(self, rel):
    return os.path.join(self.dest, rel)

  def read(self, rel):
    with open(self.path(rel), encoding='utf-8') as f:
      return f.read()

  def test_names_are_replaced(self):
    self.assertIn('windowTitle:t="My Game"', self.read('prog/gameBase/config/settings.blk'))
    self.assertIn('dagor_add_dng_game(NAME my_game GAME my_game', self.read('prog/CMakeLists.txt'))
    self.assertIn('FILES_CMAKE my_game_files.cmake', self.read('prog/CMakeLists.txt'))
    self.assertTrue(os.path.isfile(self.path('prog/my_game_files.cmake')))
    self.assertIn('ID org.test.MyGame', self.read('prog/CMakeLists.txt'))
    self.assertTrue(os.path.isfile(self.path('prog/scripts/my_game/my_game.das')))
    self.assertTrue(os.path.isfile(self.path('prog/platform/windows/my_game.rc')))
    self.assertFalse(os.path.exists(self.path('template.blk')))

  def test_no_token_is_left(self):
    for dirpath, _, filenames in os.walk(self.dest):
      for fn in filenames:
        full = os.path.join(dirpath, fn)
        self.assertNotRegex(full, 'dng_empty|DngEmpty')
        with open(full, 'rb') as f:
          data = f.read()
        if b'\0' not in data:
          self.assertNotRegex(data.decode('utf-8'), 'dng_empty|DngEmpty|Dng Empty|com\\.dagor\\.', full)

  def test_engine_link_is_written(self):
    self.assertEqual(engine.read_engine_root(self.dest), ENGINE)
    prog = presets.engine_prog_path(self.dest, ENGINE)
    text = self.read('prog/CMakePresets.json')
    self.assertIn('"{}/cmake/presets/base.json"'.format(prog), text)
    self.assertIn('"DAGOR_ENGINE_ROOT": "${{sourceDir}}/{}/.."'.format(prog), text)
    self.assertTrue(os.path.isfile(os.path.normpath(os.path.join(self.dest, 'prog', prog, 'cmake', 'presets', 'base.json'))))

  def test_generated_and_build_files_are_not_copied(self):
    for rel in ('game/windows-x86_64', 'game/compiledShaders', 'tools', 'develop/.cache'):
      self.assertFalse(os.path.exists(self.path(rel)), rel)
    self.assertTrue(os.path.isfile(self.path('game/client.cmd')))

  def test_refuses_a_non_empty_destination(self):
    with self.assertRaisesRegex(ProjectError, 'not empty'):
      create.create('dng-empty', 'MyGame', self.dest, git_init=False, log=lambda *a: None)


if __name__ == '__main__':
  unittest.main()
