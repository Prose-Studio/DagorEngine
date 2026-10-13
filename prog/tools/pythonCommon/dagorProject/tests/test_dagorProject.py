"""Tests of dagorProject: the engine root in application.blk, the project presets and project creation from the templates in templates/."""
import json
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
TOKENS = {'bundleId': 'com.example.StarterGame', 'title': 'Starter Game', 'name': 'StarterGame', 'codename': 'starter_game'}


class EngineRootTest(unittest.TestCase):
  """engineRoot in a project's application.blk"""

  def setUp(self):
    self.dir = tempfile.mkdtemp()

  def tearDown(self):
    shutil.rmtree(self.dir, ignore_errors=True)

  def blk(self):
    with open(os.path.join(self.dir, 'application.blk'), encoding='utf-8') as f:
      return f.read()

  def write_blk(self, text):
    with open(os.path.join(self.dir, 'application.blk'), 'w', encoding='utf-8') as f:
      f.write(text)

  def test_written_relative_and_read_back(self):
    engine.write_engine_root(self.dir, ENGINE)
    ref = re.search(r'engineRoot:t="([^"]*)"', self.blk()).group(1)
    if os.path.splitdrive(self.dir)[0].lower() == os.path.splitdrive(ENGINE)[0].lower():
      self.assertFalse(os.path.isabs(ref), ref)
    self.assertEqual(engine.read_engine_root(self.dir), ENGINE)

  def test_absolute_on_request(self):
    engine.write_engine_root(self.dir, ENGINE, absolute=True)
    self.assertEqual(engine.read_engine_root(self.dir), ENGINE)
    self.assertIn('engineRoot:t="{}"'.format(ENGINE), self.blk())

  def test_the_rest_of_application_blk_is_kept(self):
    tools = 'collision:t="Unigine"\nshaders:t="tools/tools"\n\ngame{\n  game_folder:t="game"\n}\n'
    self.write_blk(tools)
    engine.write_engine_root(self.dir, ENGINE)  # no engineRoot yet: the first line
    self.assertTrue(self.blk().endswith(tools))
    self.write_blk('// tools\ncollision:t="Unigine"\nengineRoot:t="old/path"  // a comment\nshaders:t="x"\n')
    engine.write_engine_root(self.dir, ENGINE, absolute=True)  # in place
    self.assertEqual(self.blk(), '// tools\ncollision:t="Unigine"\nengineRoot:t="{}"  // a comment\nshaders:t="x"\n'.format(ENGINE))

  def test_the_engine_reads_only_the_engine_root_line(self):
    # prog/engine/osApiWrappers/namedMounts.cpp takes the engineRoot:t= line: comments may name it, but not as that line
    engine.write_engine_root(self.dir, ENGINE)
    lines = [l for l in self.blk().splitlines() if l.lstrip().startswith('engineRoot')]
    self.assertEqual(len(lines), 1)
    self.assertTrue(lines[0].startswith('engineRoot:t='))

  def test_blk_escapes(self):
    # ~ escapes in BLK strings, and Windows short names have a ~: RUNNER~1
    self.write_blk('engineRoot:t="C:/Users/RUNNER~~1/engine"\n')
    self.assertEqual(engine.read_engine_ref(self.dir), 'C:/Users/RUNNER~1/engine')

  def test_missing_and_wrong_engine_fail_clearly(self):
    with self.assertRaisesRegex(ProjectError, 'cannot read'):
      engine.read_engine_root(self.dir)
    self.write_blk('shaders:t="x"\n')
    with self.assertRaisesRegex(ProjectError, 'expected engineRoot'):
      engine.read_engine_root(self.dir)
    self.write_blk('engineRoot:t="no/such/dir"\n')
    with self.assertRaisesRegex(ProjectError, 'not a Dagor Engine checkout'):
      engine.read_engine_root(self.dir)
    with self.assertRaisesRegex(ProjectError, 'not a Dagor Engine checkout'):
      engine.write_engine_root(self.dir, self.dir)

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
    tokens = [('Starter Game', 'StarterGame Ultra'), ('StarterGame', 'MyGame')]  # longest first, as create() orders them
    self.assertEqual(create.substitute('Starter Game / StarterGame', tokens), 'StarterGame Ultra / MyGame')
    self.assertFalse(create.tokens_left('StarterGame Ultra', [('StarterGame', 'StarterGame Ultra')]))
    self.assertTrue(create.tokens_left('a StarterGame', [('StarterGame', 'MyGame')]))

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
      for rel in ('keep.txt', 'game/run.cmd', 'game/x/big.exe', 'prog/_libs.vromfs.blk', 'a/b/c.pyc', 'template.blk'):
        os.makedirs(os.path.dirname(os.path.join(d, rel)) or d, exist_ok=True)
        open(os.path.join(d, rel), 'w').close()
      with open(os.path.join(d, '.gitignore'), 'w') as f:
        f.write('/prog/_libs.vromfs.blk\n/game/*\n!/game/*.cmd\n*.pyc\n')
      files = sorted(create._gitignore_files(d))
      self.assertEqual(files, ['.gitignore', 'game/run.cmd', 'keep.txt', 'template.blk'])
    finally:
      shutil.rmtree(d, ignore_errors=True)

  def test_templates(self):
    self.assertEqual(sorted(create.list_templates()), ['mp-2d', 'mp-3d', 'sp-2d', 'sp-3d'])  # not the _layers
    for tid in create.list_templates():
      t = create.read_template(tid)
      self.assertEqual(t.tokens, TOKENS, tid)
      self.assertEqual(t.multiplayer, tid.startswith('mp-'), tid)
      self.assertEqual([os.path.basename(d) for d in t.dirs],
                       ['_common', '_multiplayer' if t.multiplayer else '_singleplayer', '_' + tid[3:], tid])

  def test_later_layers_replace_earlier_files(self):
    files = {rel: src.replace('\\', '/') for rel, src in create.template_files(create.read_template('sp-2d')).items()}
    self.assertTrue(files['prog/CMakeLists.txt'].endswith('/_singleplayer/prog/CMakeLists.txt'))
    self.assertIn('/_2d/', files['prog/gameBase/gamedata/scenes/main.blk'])
    self.assertIn('/_common/', files['application.blk'])
    self.assertNotIn('game/server.cmd', files)
    self.assertNotIn('template.blk', files)

  def test_unknown_template(self):
    for tid in ('no-such', '_common'):
      with self.subTest(tid), self.assertRaisesRegex(ProjectError, 'no template'):
        create.read_template(tid)


class CreateTest(unittest.TestCase):
  """Creates a real project from templates/mp-3d (no build: CI builds and tests them, see template.yaml)."""
  TEMPLATE = 'mp-3d'

  @classmethod
  def setUpClass(cls):
    cls.parent = tempfile.mkdtemp()
    cls.dest = os.path.join(cls.parent, 'MyGame')
    create.create(cls.TEMPLATE, 'MyGame', cls.dest, company='org.test', git_init=False, log=lambda *a: None)

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
        self.assertNotRegex(full, 'starter_game|StarterGame')
        with open(full, 'rb') as f:
          data = f.read()
        if b'\0' not in data:
          self.assertNotRegex(data.decode('utf-8'), 'starter_game|StarterGame|Starter Game', full)

  def test_engine_link_is_written(self):
    self.assertEqual(engine.read_engine_root(self.dest), ENGINE)
    prog = presets.engine_prog_path(self.dest, ENGINE)
    text = self.read('prog/CMakePresets.json')
    self.assertIn('"{}/cmake/presets/base.json"'.format(prog), text)
    root = prog if os.path.isabs(prog) else '${sourceDir}/' + prog  # absolute when the project is on another drive
    self.assertIn('"DAGOR_ENGINE_ROOT": "{}/.."'.format(root), text)
    self.assertTrue(os.path.isfile(os.path.normpath(os.path.join(self.dest, 'prog', prog, 'cmake', 'presets', 'base.json'))))

  def test_engine_on_another_drive_is_absolute(self):
    prog = os.path.abspath(os.path.join(ENGINE, 'prog')).replace('\\', '/')
    data = presets.project_presets(prog, multiplayer=False)
    self.assertEqual(data['include'], [prog + '/cmake/presets/base.json'])
    self.assertEqual(data['configurePresets'][0]['environment']['DAGOR_ENGINE_ROOT'], prog + '/..')

  def test_generated_and_build_files_are_not_copied(self):
    for rel in ('game/windows-x86_64', 'game/compiledShaders', 'tools', 'develop/.cache'):
      self.assertFalse(os.path.exists(self.path(rel)), rel)
    self.assertTrue(os.path.isfile(self.path('game/client.cmd')))

  def test_refuses_a_non_empty_destination(self):
    with self.assertRaisesRegex(ProjectError, 'not empty'):
      create.create(self.TEMPLATE, 'MyGame', self.dest, git_init=False, log=lambda *a: None)

  def configure_presets(self):
    return [p['name'] for p in json.loads(self.read('prog/CMakePresets.json'))['configurePresets']]

  def test_the_game_kind(self):
    self.assertIn('windows-dedicated', self.configure_presets())
    data = json.loads(self.read('prog/CMakePresets.json'))
    client = [p for p in data['configurePresets'] if p['name'] == 'linux-client'][0]
    self.assertEqual(client['inherits'], ['project', 'toolchain-linux'])
    self.assertEqual(client['cacheVariables'], {'DAGOR_DEDICATED_PRESET': 'linux-dedicated'})
    everything = [p for p in data['buildPresets'] if p['name'] == 'linux'][0]  # cmake --workflow --preset linux
    self.assertEqual(everything['targets'], ['all', 'content', 'dedicated'])
    self.assertIn('linux', [w['name'] for w in data['workflowPresets']])
    self.assertTrue(os.path.isfile(self.path('game/server.cmd')))
    self.assertIn('DEDICATED_AUTH', self.read('prog/CMakeLists.txt'))
    self.assertIn('static_cam', self.read('prog/gameBase/gamedata/scenes/main.blk'))
    presets.write(self.dest, ENGINE)  # relink keeps the trees
    self.assertIn('windows-dedicated', self.configure_presets())


class CreateSinglePlayer2dTest(CreateTest):
  """A project from templates/sp-2d: no dedicated server, the orthographic scene"""
  TEMPLATE = 'sp-2d'

  def test_the_game_kind(self):
    self.assertIn('windows-client', self.configure_presets())
    data = json.loads(self.read('prog/CMakePresets.json'))
    everything = [p for p in data['buildPresets'] if p['name'] == 'windows'][0]
    self.assertEqual(everything['targets'], ['all', 'content'])
    self.assertFalse([n for n in self.configure_presets() if 'dedicated' in n])
    workflows = json.loads(self.read('prog/CMakePresets.json'))['workflowPresets']
    test = [s for w in workflows if w['name'] == 'linux-test' for s in w['steps'] if s['type'] == 'test']
    self.assertEqual(test, [{'type': 'test', 'name': 'linux-client'}])
    build = [s for w in workflows if w['name'] == 'linux-test' for s in w['steps'] if s['type'] == 'build']
    self.assertEqual(build, [{'type': 'build', 'name': 'linux'}])  # the client's tests run on its content
    self.assertFalse(os.path.exists(self.path('game/server.cmd')))
    self.assertNotIn('DEDICATED_AUTH', self.read('prog/CMakeLists.txt'))
    self.assertIn('ortho_cam', self.read('prog/gameBase/gamedata/scenes/main.blk'))
    presets.write(self.dest, ENGINE)  # relink keeps the trees
    self.assertFalse([n for n in self.configure_presets() if 'dedicated' in n])


if __name__ == '__main__':
  unittest.main()
