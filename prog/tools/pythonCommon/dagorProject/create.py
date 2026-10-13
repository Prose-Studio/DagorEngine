"""Creating a game project from a template in <engine>/templates (dng.py new in the engine root), and relinking one to
this engine (dng.py relink).

A template is a dir with a template.blk: its description, whether the game is multiplayer (a client and a dedicated
server) and the layers (dirs starting with _) the project is made of, in order; each layer's files replace those of the
layers before it, the template dir's own files come last. The template.blk files of the layers give the name tokens
(tokens{}) that are replaced in file names and text files. Only files git tracks (or would track) are copied. The new
project's application.blk (engineRoot) and prog/CMakePresets.json name this engine.
"""
import argparse
import fnmatch
import os
import re
import shutil
import subprocess
import sys
from typing import Dict, List, Tuple

from . import engine, presets
from .engine import ProjectError

TEMPLATE_BLK = 'template.blk'
TOKEN_KEYS = ('bundleId', 'title', 'name', 'codename')

EPILOG = '''examples:
  python dng.py new --name MyGame --dest ../MyGame
  python dng.py new --template sp-2d --name MyGame --dest ../MyGame
  python dng.py new --name MyGame --title "My Game" --company com.example --dest D:/Games/MyGame
  python dng.py new --list'''


def engine_root() -> str:
  return engine.norm(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..'))


def templates_dir() -> str:
  return engine_root() + '/templates'


def list_templates() -> Dict[str, str]:
  """{template id: description}"""
  out = {}
  if os.path.isdir(templates_dir()):
    for d in sorted(os.listdir(templates_dir())):
      if not d.startswith('_') and os.path.isfile(os.path.join(templates_dir(), d, TEMPLATE_BLK)):
        out[d] = read_template(d).description
  return out


class Template:
  """A template: its description, multiplayer, its dirs (the layers, then its own) and the tokens they use"""

  def __init__(self, description: str, multiplayer: bool, dirs: List[str], tokens: Dict[str, str]):
    self.description, self.multiplayer, self.dirs, self.tokens = description, multiplayer, dirs, tokens


def _blk_params(text: str, name: str, kind: str = 't') -> List[str]:
  if kind == 't':
    return re.findall(r'^\s*' + name + r'\s*:\s*t\s*=\s*"([^"]*)"', text, re.MULTILINE)
  return re.findall(r'^\s*' + name + r'\s*:\s*b\s*=\s*(\w+)', text, re.MULTILINE)


def read_template(template_id: str) -> Template:
  own = os.path.join(templates_dir(), template_id)
  fn = os.path.join(own, TEMPLATE_BLK)
  if template_id.startswith('_') or not os.path.isfile(fn):
    raise ProjectError('no template "{}" in {} (python dng.py new --list)'.format(template_id, templates_dir()))
  with open(fn, 'r', encoding='utf-8') as f:
    text = f.read()
  dirs = []
  for layer in _blk_params(text, 'layer'):
    d = os.path.join(templates_dir(), layer)
    if not layer.startswith('_') or not os.path.isdir(d):
      raise ProjectError('{}: layer "{}" is not a layer dir (_<name>) in {}'.format(fn, layer, templates_dir()))
    dirs.append(d)
  dirs.append(own)
  tokens = {}
  for d in dirs:
    blk = os.path.join(d, TEMPLATE_BLK)
    if os.path.isfile(blk):
      with open(blk, 'r', encoding='utf-8') as f:
        m = re.search(r'tokens\s*\{([^}]*)\}', f.read())
      if m:
        tokens.update({k: v[0] for k in TOKEN_KEYS for v in [_blk_params(m.group(1), k)] if v})
  missing = [k for k in TOKEN_KEYS if not tokens.get(k)]
  if missing:
    raise ProjectError('{}: the layers\' tokens{{}} must have {}'.format(fn, ', '.join(k + ':t=' for k in missing)))
  multiplayer = _blk_params(text, 'multiplayer', 'b')
  return Template((_blk_params(text, 'description') or [''])[0], bool(multiplayer) and multiplayer[0] in ('yes', 'true'),
                  dirs, tokens)


# ---- names

def split_words(name: str) -> List[str]:
  """PascalCase words, digits stay with theirs: MyGame -> My Game, E2eGame -> E2e Game, HTTPServer2 -> HTTP Server2"""
  return re.findall(r'[A-Z]?[a-z0-9]+|[A-Z0-9]+(?![a-z])', name)


def default_codename(name: str) -> str:
  return '_'.join(w.lower() for w in split_words(name))


def default_title(name: str) -> str:
  return ' '.join(split_words(name))


def validate(name, codename, title, company, dest):
  if not re.match(r'^[A-Z][A-Za-z0-9]*$', name):
    raise ProjectError('--name must be PascalCase ASCII letters and digits (like MyGame), not "{}"'.format(name))
  if not re.match(r'^[a-z][a-z0-9_]*$', codename):
    raise ProjectError('--codename must be lowercase letters, digits and _ (like my_game), not "{}"'.format(codename))
  if not title.strip() or '"' in title or '\\' in title:
    raise ProjectError('--title must be non-empty, without " or \\')
  if not re.match(r'^[A-Za-z][A-Za-z0-9-]*(\.[A-Za-z][A-Za-z0-9-]*)+$', company):
    raise ProjectError('--company must be a reverse domain name (like com.example), not "{}"'.format(company))
  if not re.match(r'^[\x21-\x7e]+$', dest):
    raise ProjectError('the destination must be an ASCII path without spaces (the build tools need it), not "{}"'.format(dest))


# ---- template files

def _git_files(template: str) -> List[str]:
  """Files git tracks or would track (not ignored) in the template, relative to it; None without git."""
  try:
    out = subprocess.run(['git', 'ls-files', '-z', '--cached', '--others', '--exclude-standard', '--', '.'], cwd=template,
                         capture_output=True, check=True).stdout
  except (OSError, subprocess.CalledProcessError):
    return None
  files = [f for f in out.decode('utf-8').split('\0') if f]
  return [f for f in files if os.path.isfile(os.path.join(template, f))]  # skips deleted, not yet committed files


def _gitignore_files(template: str) -> List[str]:
  """Without git (an engine from an archive): every file except those the template's .gitignore matches."""
  patterns = []
  try:
    with open(os.path.join(template, '.gitignore'), 'r', encoding='utf-8') as f:
      patterns = [l.strip() for l in f if l.strip() and not l.startswith('#')]
  except OSError:
    pass

  def ignored(rel):
    result = False
    for p in patterns:
      neg = p.startswith('!')
      p = p[1:] if neg else p
      anchored = p.startswith('/')
      p = p.strip('/')
      parts = rel.split('/')
      candidates = ['/'.join(parts[:i]) for i in range(1, len(parts) + 1)]
      if not anchored:
        candidates += parts
      if any(fnmatch.fnmatch(c, p) for c in candidates):
        result = not neg
    return result

  files = []
  for dirpath, dirnames, filenames in os.walk(template):
    for fn in filenames:
      rel = os.path.relpath(os.path.join(dirpath, fn), template).replace('\\', '/')
      if not ignored(rel):
        files.append(rel)
  return files


def dir_files(d: str) -> List[str]:
  files = _git_files(d)
  if files is None:
    files = _gitignore_files(d)
  return sorted(f for f in files if f != TEMPLATE_BLK)


def template_files(template: Template) -> Dict[str, str]:
  """{project-relative path: source file}: the dirs' files, later dirs replacing earlier ones"""
  out = {}
  for d in template.dirs:
    out.update({rel: os.path.join(d, rel) for rel in dir_files(d)})
  return dict(sorted(out.items()))


def is_text(data: bytes) -> bool:
  return b'\0' not in data


def substitute(text: str, tokens: List[Tuple[str, str]]) -> str:
  """One pass, longest token first: a replacement is never replaced again"""
  pattern = re.compile('|'.join(re.escape(old) for old, _ in tokens))
  mapping = dict(tokens)
  return pattern.sub(lambda m: mapping[m.group(0)], text)


def tokens_left(text: str, tokens: List[Tuple[str, str]]) -> bool:
  return any(old in text for old, new in tokens if old not in new)  # a new name may contain a token on purpose


# ---- creation

def create(template_id: str, name: str, dest: str, codename=None, title=None, company='com.example', absolute_engine_path=False,
           git_init=True, force=False, dry_run=False, log=print):
  codename = codename or default_codename(name)
  title = title or default_title(name)
  validate(name, codename, title, company, dest)
  template = read_template(template_id)
  values = {'bundleId': company + '.' + name, 'title': title, 'name': name, 'codename': codename}
  tokens = sorted(((template.tokens[k], values[k]) for k in TOKEN_KEYS), key=lambda t: -len(t[0]))  # longest first

  dest = engine.norm(dest)
  if (dest + '/').startswith(engine.norm(templates_dir()) + '/'):
    raise ProjectError('the destination is inside the templates dir')
  if os.path.exists(dest) and (not os.path.isdir(dest) or os.listdir(dest)) and not force:
    raise ProjectError('{} exists and is not empty (--force writes into it anyway)'.format(dest))

  files = template_files(template)
  if not files:
    raise ProjectError('the template {} has no files'.format(template_id))
  log('{} "{}" ({}) from template {} into {}'.format('would create' if dry_run else 'creating', title, codename, template_id, dest))
  for rel, src in files.items():
    out_rel = substitute(rel, tokens)
    with open(src, 'rb') as f:
      data = f.read()
    if is_text(data):
      data = substitute(data.decode('utf-8'), tokens).encode('utf-8')
    if dry_run:
      log('  ' + out_rel)
      continue
    out = os.path.join(dest, out_rel)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, 'wb') as f:
      f.write(data)
    shutil.copymode(src, out)  # keeps scripts executable

  if dry_run:
    return dest
  leftovers = []
  for rel in files:
    out_rel = substitute(rel, tokens)
    with open(os.path.join(dest, out_rel), 'rb') as f:
      data = f.read()
    if tokens_left(out_rel, tokens) or (is_text(data) and tokens_left(data.decode('utf-8'), tokens)):
      leftovers.append(rel)
  if leftovers:
    raise ProjectError('template tokens are left in: {}'.format(', '.join(leftovers)))

  relink(dest, absolute=absolute_engine_path, multiplayer=template.multiplayer)
  if git_init and shutil.which('git') and not os.path.isdir(os.path.join(dest, '.git')):
    subprocess.run(['git', 'init', '-q'], cwd=dest, check=True)
    log('initialized a git repository (nothing committed)')
  return dest


def relink(project_dir: str, absolute=False, multiplayer=None):
  """points the project's application.blk (engineRoot) and prog/CMakePresets.json at this engine (multiplayer: whether the game has a
  dedicated server, by default as its presets say)"""
  engine.write_engine_root(project_dir, engine_root(), absolute=absolute)
  presets.write(project_dir, engine_root(), multiplayer)


def make_parser():
  p = argparse.ArgumentParser(prog='dng.py new', description='Creates a game project from a template in templates/. '
                              'The project can be anywhere: it finds this engine through its application.blk and '
                              'CMakePresets.json.',
                              epilog=EPILOG, formatter_class=argparse.RawDescriptionHelpFormatter)
  p.add_argument('--template', default='mp-3d', help='template id (default: mp-3d; --list shows them)')
  p.add_argument('--name', help='PascalCase name, e.g. MyGame')
  p.add_argument('--dest', help='project dir to create (default: ../<name> next to the engine)')
  p.add_argument('--codename', help='lowercase name of executables and dirs (default: from --name, my_game)')
  p.add_argument('--title', help='human readable name (default: from --name, "My Game")')
  p.add_argument('--company', default='com.example', help='reverse domain name for bundle ids (default: com.example)')
  p.add_argument('--absolute-engine-path', action='store_true', help='store the engine path in application.blk as absolute '
                 '(default: relative, absolute only across drives)')
  p.add_argument('--no-git', action='store_true', help='do not run git init in the new project')
  p.add_argument('--force', action='store_true', help='write into an existing non-empty dir')
  p.add_argument('--dry-run', action='store_true', help='print the files it would create')
  p.add_argument('--list', action='store_true', help='list the templates')
  return p


def main(argv):
  args = make_parser().parse_args(argv)
  try:
    if args.list:
      for tid, desc in list_templates().items():
        print('{:16} {}'.format(tid, desc))
      return 0
    if not args.name:
      make_parser().error('--name is required')
    dest = args.dest or os.path.join(engine_root(), '..', args.name)
    dest = create(args.template, args.name, dest, codename=args.codename, title=args.title, company=args.company,
                  absolute_engine_path=args.absolute_engine_path, git_init=not args.no_git, force=args.force,
                  dry_run=args.dry_run)
  except ProjectError as e:
    print('ERROR: {}'.format(e), file=sys.stderr)
    return 2
  if not args.dry_run:
    host = {'win32': 'windows', 'darwin': 'macos'}.get(sys.platform, 'linux')
    print('''
Next steps, in {0}/prog (cmake --list-presets lists the trees):
  cmake --workflow --preset {2}         everything: the game{3}, its content, the engine tools it needs
  cmake --workflow --preset {2}-test    the tests that need no GPU
  ../game/client{1}                      run the game
  ../develop/daEditor{1}                 open the editor
See README.md there.'''.format(dest, '.cmd' if sys.platform.startswith('win') else '.sh', host,
                                 ', its dedicated server' if read_template(args.template).multiplayer else ''))
  return 0


def relink_main(argv):
  p = argparse.ArgumentParser(prog='dng.py relink', description="Points a game project's application.blk and "
                              'prog/CMakePresets.json at this engine (after either moved).')
  p.add_argument('project', help='the project dir')
  p.add_argument('--absolute-engine-path', action='store_true', help='store the engine path as absolute')
  args = p.parse_args(argv)
  try:
    relink(args.project, absolute=args.absolute_engine_path)
  except ProjectError as e:
    print('ERROR: {}'.format(e), file=sys.stderr)
    return 2
  return 0
