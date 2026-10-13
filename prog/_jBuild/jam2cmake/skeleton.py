#!/usr/bin/env python3
"""A first CMakeLists.txt for a jamfile, for the port to CMake (deleted together with jam).

It translates the common subset of jamfiles: the target variables (Target, TargetType, Sources, AddIncludes,
UseProgLibs, CPPopt, AddLibs, ...), 'opt on <file>', Autoscan source dirs, and 'if' on Platform, PlatformArch,
KernelLinkage, PlatformSpec, SSEVersion and Sanitize. Branches only consoles take are dropped. What it cannot translate
is kept as '# TODO(jam): <statement>' at its place, to be ported by hand (the CI lint fails on TODO(jam) in ported dirs).

A game module (build_module.jam) becomes dagor_add_dng_module(); a library's _lib.jam and _aot.jam (what it adds to the
game and to its AOT compiler) become _lib.cmake and _aot.cmake with dagor_game_lib() calls.

python skeleton.py <jamfile>... [--write] [--force]   -- prints the CMakeLists.txt, or writes it next to the jamfile
"""
import argparse
import os
import re
import sys

ENGINE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))

CONSOLES = {'ps4', 'ps5', 'xboxOne', 'scarlett', 'nswitch'}
PLATFORMS = {'windows', 'linux', 'macOS', 'iOS', 'tvOS', 'android'}
ARCHS = {'x86_64': 'x86_64', 'arm64': 'arm64', 'arm64-v8a': 'arm64', 'e2k': 'e2k'}
# jam switches whose value is fixed in CMake builds: the vendored OpenSSL and libcurl, NEON on Android arm64, no APEX
CONSTANT_VARS = {'UseSystemOpenSSL': 'no', 'UseSystemLibcurl': 'no', 'AndroidHasNeon': 'yes',
                 'UseApex': 'no'}  # the fork has no APEX
# jam yes/no switches that are CMake tree options
BOOL_VARS = {'NeedDasAotCompile': 'DAGOR_DAS_AOT', 'NeedDasLLVMAotCompile': 'DAGOR_DAS_LLVM_AOT',
             'Dedicated': 'DAGOR_DEDICATED', 'ForceLogs': 'DAGOR_FORCE_LOGS', 'BreakpadEnabled': 'DAGOR_BREAKPAD',
             'SqVarTrace': 'DAGOR_SQ_VAR_TRACE', 'BuildingTools': 'DAGOR_BUILDING_TOOLS',
             # the game's switches (DagorGame.cmake; those jam turned off in Rel are generator expressions, not here)
             'HaveRenderer': 'DAGOR_GAME_RENDERER', 'HaveFx': 'DAGOR_GAME_FX', 'HaveSound': 'DAGOR_GAME_SOUND',
             'HaveSoundNet': 'DAGOR_GAME_SOUND_NET', 'HaveOverlayUI': 'DAGOR_GAME_OVERLAY_UI',
             'HaveDngInput': 'DAGOR_GAME_DNG_INPUT', 'HaveEmbeddedBrowser': 'DAGOR_GAME_EMBEDDED_BROWSER',
             'HaveAssetManager': 'DAGOR_GAME_ASSET_MANAGER', 'BVHSupport': 'DAGOR_GAME_BVH'}
CONDITION_VARS = {'Platform': 'DAGOR_PLATFORM', 'PlatformArch': 'DAGOR_ARCH', 'KernelLinkage': 'DAGOR_KERNEL_LINKAGE',
                  'SSEVersion': 'DAGOR_SSE', 'Sanitize': 'DAGOR_SANITIZE', 'PlatformSpec': 'DAGOR_CC'}
LIST_VARS = {'Sources': 'sources', 'AddIncludes': 'includes', 'UseProgLibs': 'deps', 'CPPopt': 'cpp_opt',
             'Copt': 'c_opt', 'AddLibs': 'libs', 'LINKopt': 'link_options', 'ExplicitLicenseUsed': 'license_files'}
IGNORED_VARS = {'TargetLib', 'LibPath',  # jam bookkeeping without a CMake counterpart
                'ProjectAllowsOodle',  # Oodle is in every program of a tree given DAGOR_SDK_OODLE_DIR
                'PlatformSpec_windows', 'PlatformArch_windows',  # the trees choose the compiler and architecture
                'ForcePdb', 'ReproducibleExeBuild', 'UseLLDLink'}  # always so in CMake builds
SCALAR_VARS = {'Location', 'Target', 'TargetType', 'StrictCompile', 'ConsoleExe', 'OutDir', 'Exceptions', 'Rtti', 'UseQuirrel',
               'Config',
               'Root'}
KNOWN_INCLUDES = {'defaults.jam', 'build.jam', 'unitTest.jam'}
# jam variables that only ever had their defaults.jam value; CMake builds have just that version
FIXED_VERSIONS = {'UseZlibVer': 'ng', 'ZstdVer': '1.4.5', 'OpenSSLVer': '3.x', 'DefOpenSSLVer': '3.x', 'BulletSdkVer': '3',
                  'DefBulletSdkVer': '3', 'FreeTypeVer': '2.8', 'DefFreeTypeVer': '2.8', 'OpenXrVer': '1.1.54',
                  'CPPStd': '20'}


# --- lexer -----------------------------------------------------------------------------------------------------------
def tokens(text):
  """(token, line) of a jamfile: whitespace-separated, '#' comments, "quoted" parts kept with their quotes."""
  out = []
  i, n, line = 0, len(text), 1
  while i < n:
    c = text[i]
    if c == '\n':
      line += 1
      i += 1
    elif c.isspace():
      i += 1
    elif c == '#':
      while i < n and text[i] != '\n':
        i += 1
    else:
      start, start_line, quoted = i, line, False
      while i < n and (quoted or not text[i].isspace()):
        if text[i] == '\\' and i + 1 < n:
          i += 2
          continue
        if text[i] == '"':
          quoted = not quoted
        if text[i] == '\n':
          line += 1
        i += 1
      word = text[start:i]
      if word == '{}':  # an empty block written without a space
        out += [('{', start_line), ('}', start_line)]
      else:
        out.append((word, start_line))
  return out


# --- parser ----------------------------------------------------------------------------------------------------------
class Parser:
  """Statements as tuples: ('assign', var, op, values, src), ('on', var, target, op, values, src),
  ('include', path, src), ('if', [(cond, block)...], else_block, src), ('other', src)."""

  def __init__(self, toks):
    self.toks = toks
    self.i = 0

  def peek(self, k=0):
    return self.toks[self.i + k][0] if self.i + k < len(self.toks) else None

  def next(self):
    t = self.toks[self.i][0]
    self.i += 1
    return t

  def until_semicolon(self):
    words = []
    while self.peek() not in (';', None):
      words.append(self.next())
    if self.peek() == ';':
      self.next()
    return words

  def block(self):
    stmts = []
    while self.peek() not in ('}', None):
      stmts.append(self.statement())
    if self.peek() == '}':
      self.next()
    return stmts

  def skip_braced(self):
    """The text of a { ... } construct the converter does not translate."""
    words, depth = [], 0
    while self.peek() is not None:
      t = self.next()
      words.append(t)
      if t == '{':
        depth += 1
      elif t == '}':
        depth -= 1
        if depth == 0:
          break
    return words

  def statement(self):
    t = self.peek()
    if t == 'if':
      self.next()
      branches, else_block = [], None
      cond = []
      while self.peek() != '{':
        cond.append(self.next())
      self.next()
      branches.append((cond, self.block()))
      while self.peek() == 'else':
        self.next()
        if self.peek() == 'if':
          self.next()
          cond = []
          while self.peek() != '{':
            cond.append(self.next())
          self.next()
          branches.append((cond, self.block()))
        else:
          self.next()  # {
          else_block = self.block()
          break
      return ('if', branches, else_block)
    if t == 'include':
      self.next()
      words = self.until_semicolon()
      return ('include', ' '.join(words), 'include ' + ' '.join(words) + ' ;')
    if t in ('for', 'switch', 'rule', 'while', 'actions'):
      return ('other', ' '.join(self.skip_braced()))
    if t == 'local':
      if self.peek(2) in ('=', '+='):
        self.next()
        var, op = self.next(), self.next()
        return ('assign', var, op, self.until_semicolon())
      words = self.until_semicolon()
      return ('other', ' '.join(words) + ' ;')
    if t == '{':
      self.next()
      return ('if', [(['1'], self.block())], None)
    # assignment, 'on' assignment or a rule call
    if self.peek(1) in ('=', '+=', '?=', '-='):
      var, op = self.next(), self.next()
      return ('assign', var, op, self.until_semicolon())
    if self.peek(1) == 'on' and self.peek(3) in ('=', '+='):
      var = self.next()
      self.next()
      target, op = self.next(), self.next()
      return ('on', var, target, op, self.until_semicolon())
    words = self.until_semicolon()
    return ('other', ' '.join(words) + ' ;')

  def parse(self):
    stmts = []
    while self.peek() is not None:
      if self.peek() == '}':
        self.next()
        continue
      stmts.append(self.statement())
    return stmts


# --- translation -----------------------------------------------------------------------------------------------------
class Untranslatable(Exception):
  pass


def value(word, kind):
  """A jam word as a CMake list item; Untranslatable for variables it does not know."""
  w = word
  if w == '$(Root)/$(Location)':
    return '${CMAKE_CURRENT_SOURCE_DIR}'
  w = re.sub(r'^\$\(Root\)/\$\(Location\)/', '', w)
  w = w.replace('$(Root)/prog/', '${DAGOR_PROG_DIR}/').replace('$(Root)/', '${DAGOR_ENGINE_ROOT}/')
  w = re.sub(r'^\$\(Location\)/', '', w)
  w = w.replace('$(Platform)', '${DAGOR_PLATFORM}').replace('$(PlatformArch)', '${DAGOR_ARCH}')
  if kind == 'deps' and re.fullmatch(r'(\$\(Root\)/prog/)?engine/phys/phys\$\(PhysName\)', word):
    return 'Dagor::Phys'  # the tree's physics engine
  for var, fixed in FIXED_VERSIONS.items():
    w = w.replace('$({})'.format(var), fixed)
  if '$(' in w or '[' in w:
    raise Untranslatable(word)
  if kind == 'deps':  # a library dir under prog/ is the target named after it
    if w.startswith('${DAGOR_PROG_DIR}/'):
      w = w[len('${DAGOR_PROG_DIR}/'):]
    w = w.replace('/', '.') if '::' not in w else w
  if kind == 'libs':  # Ws2_32.lib and -lX11 are the system libraries System::ws2_32 and System::X11
    m = re.fullmatch(r'"?-framework\s+(\w+)"?', w)
    if m:
      return '"$<LINK_LIBRARY:FRAMEWORK,{}>"'.format(m.group(1))
    if '/' not in w and re.search(r'(?i)\.lib$', w):
      return 'System::' + re.sub(r'(?i)\.lib$', '', w).lower()
    if w.startswith('-l'):
      return 'System::' + w[2:]
  return w


def split_cpp_opt(words):
  """(defines, options) of CPPopt words."""
  defines, options = [], []
  for w in words:
    if w.startswith('-D'):
      d = w[2:].replace('\\\\\\"', '"').replace('\\"', '"')
      defines.append(d if not re.search(r'[\s;"]', d) else '"' + d.replace('"', '\\"') + '"')
    else:
      options.append(w)
  return defines, options


def cmake_values(values, depth=0, head=''):
  """the values on the line, or one per line when they do not fit"""
  line = ' '.join(values)
  if len(head) + len(line) + 2 * depth <= 110:
    return line
  return '\n' + '\n'.join('  ' * (depth + 1) + v for v in values) + '\n' + '  ' * depth


def condition(words):
  """A jam condition as a CMake if() expression, or 'FALSE'/'TRUE' when it only depends on consoles."""
  expr, i = [], 0

  def operand(w):
    m = re.fullmatch(r'\$\((\w+)\)', w)
    if m and m.group(1) in CONSTANT_VARS:
      return ('lit', CONSTANT_VARS[m.group(1)])
    if m:
      var = m.group(1)
      if var not in CONDITION_VARS and var not in BOOL_VARS:
        raise Untranslatable(w)
      return ('var', var)
    if '$(' in w:
      if re.fullmatch(r'\$\(Platform\)-\$\(PlatformArch\)', w):
        return ('var', 'Platform-PlatformArch')
      raise Untranslatable(w)
    return ('lit', w.strip('"'))

  def cvar(var):
    if var == 'Platform-PlatformArch':
      return '"${DAGOR_PLATFORM}-${DAGOR_ARCH}"'
    return CONDITION_VARS.get(var) or BOOL_VARS[var]

  def norm(var, lit):
    """the CMake value of a jam value, None when no supported target has it"""
    if var == 'Platform':
      return lit if lit in PLATFORMS else None
    if var == 'PlatformArch':
      return ARCHS.get(lit)
    if var == 'Platform-PlatformArch':
      p, _, a = lit.partition('-')
      return '{}-{}'.format(p, ARCHS[a]) if p in PLATFORMS and a in ARCHS else None
    if var == 'Sanitize':
      return 'none' if lit == 'disabled' else lit
    if var == 'PlatformSpec':
      return {'clang': 'clang', 'gcc': 'gcc', 'vc17': 'msvc', 'vc16': 'msvc', 'msvc': 'msvc'}.get(lit)
    return lit

  def term(a, op, rest):
    kind, var = a
    if kind != 'var':
      raise Untranslatable(a[1])
    if var in BOOL_VARS and len(rest) == 1 and rest[0] in ('yes', 'no'):
      return BOOL_VARS[var] if (op in ('=', 'in')) == (rest[0] == 'yes') else 'NOT ' + BOOL_VARS[var]
    lits = [norm(var, lit) for lit in rest]
    if var == 'PlatformSpec' and 'clang' in lits:
      lits += ['clang-cl']
    lits = sorted({l for l in lits if l is not None})
    if op in ('=', 'in'):
      if not lits:
        return 'FALSE'
      if len(lits) == 1:
        return '{} STREQUAL "{}"'.format(cvar(var), lits[0])
      return '{} MATCHES "^({})$"'.format(cvar(var), '|'.join(re.escape(l) for l in lits))
    if op == '!=':
      if not lits:
        return 'TRUE'
      if len(lits) == 1:
        return 'NOT {} STREQUAL "{}"'.format(cvar(var), lits[0])
      return 'NOT {} MATCHES "^({})$"'.format(cvar(var), '|'.join(re.escape(l) for l in lits))
    raise Untranslatable(op)

  while i < len(words):
    w = words[i]
    if w == '[' and words[i + 1:i + 2] == ['GLOB'] and words[i + 3:i + 6] == [':', '*', ']']:
      expr.append('IS_DIRECTORY "{}"'.format(value(words[i + 2], 'dirs')))  # [ GLOB <dir> : * ]: the dir exists
      i += 6
    elif w in ('&&', '||'):
      expr.append('AND' if w == '&&' else 'OR')
      i += 1
    elif w == '!':
      expr.append('NOT')
      i += 1
    elif w in ('(', ')'):
      expr.append(w)
      i += 1
    else:
      a = operand(w)
      op = words[i + 1] if i + 1 < len(words) else None
      if op in ('=', '!=') and a[0] == 'lit':
        equal = a[1] == operand(words[i + 2])[1]
        expr.append('TRUE' if equal == (op == '=') else 'FALSE')
        i += 3
      elif op in ('=', '!='):
        expr.append(term(a, op, [words[i + 2]]))
        i += 3
      elif op == 'in':
        j = i + 2
        lits = []
        while j < len(words) and words[j] not in ('&&', '||', ')'):
          lits.append(operand(words[j])[1])
          j += 1
        expr.append(term(a, 'in', lits))
        i = j
      else:
        if a[0] == 'lit' and a[1] == '1':
          expr.append('TRUE')
        elif a[0] == 'var':
          expr.append(cvar(a[1]))
        else:
          raise Untranslatable(w)
        i += 1
  text = ' '.join(expr)
  # conditions that only depended on consoles fold to constants
  if re.fullmatch(r'(TRUE|FALSE|NOT|AND|OR|\(|\)|\s)+', text):
    py = text.replace('TRUE', 'True').replace('FALSE', 'False').replace('NOT', 'not').replace('AND', 'and')
    return 'TRUE' if eval(py.replace('OR', 'or')) else 'FALSE'
  return text


class Converter:
  def __init__(self, jamfile):
    self.jamfile = jamfile
    # a library's _lib.jam / _aot.jam: what it adds to the game (or its AOT compiler), dagor_game_lib() calls
    self.lib_mode = os.path.basename(jamfile) in ('_lib.jam', '_aot.jam')
    self.lines = []
    self.scalars = {}
    self.used = set()
    self.after_build = False
    self.todo = 0
    self.user_vars = set()
    self.derived = 0
    self.locals = {}
    self.nonempty = set()  # the jamfile's lists that something is put into

  def refs(self, depth, values):
    """values with $(V) and $(V:D=dir) of the jamfile's own list variables as CMake ${...}"""
    out = []
    for v in values:
      m = re.fullmatch(r'\$\((\w+)(?::D=([^)]*))?\)', v)
      if m and m.group(1) in self.user_vars:
        if not m.group(2):
          out.append('${' + m.group(1) + '}')
        else:
          self.derived += 1
          name = '_{}_{}'.format(m.group(1), self.derived)
          self.emit(depth, 'set({} ${{{}}})'.format(name, m.group(1)))
          self.emit(depth, 'list(TRANSFORM {} PREPEND "{}/")'.format(name, value(m.group(2), 'dirs')))
          out.append('${' + name + '}')
      else:
        out.append(v)
    return out

  def stringify(self, depth, src):
    """StringifySourceFile <f> : <f>.inl : <user> [: --array] ; alone or in a for loop over a list; True if done"""
    m = re.fullmatch(r'for (\w+) in \$\((\w+)\) \{ StringifySourceFile \$\(\1\) : \$\(\1\)\.inl : \S+'
                     r'(?: :(?: (--array|--full-string))?)? ; \}', src.strip())
    if m and m.group(2) in self.user_vars and m.group(3) != '--full-string':
      var = 'stringify_array' if m.group(3) else 'stringify'
      self.emit(depth, 'list(APPEND {} ${{{}}})'.format(var, m.group(2)))
      self.used.add(var)
      return True
    m = re.fullmatch(r'StringifySourceFile (\S+) : \1\.inl : \S+(?: :(?: (--array))?)? ;', src.strip())
    if m and '$(' not in m.group(1):
      var = 'stringify_array' if m.group(2) else 'stringify'
      self.emit(depth, 'list(APPEND {} {})'.format(var, m.group(1)))
      self.used.add(var)
      return True
    return False

  def autoscan(self, depth, src):
    """AutoscanBuildLists <dirs> : <pattern> : Sources [: <exclude regex>] ;"""
    groups = [g.split() for g in src.rstrip(' ;').split(' : ')]
    groups[0] = groups[0][1:]
    if len(groups) < 3 or len(groups[2]) != 1:
      raise Untranslatable(src)
    out = groups[2][0]
    if out == 'Sources':
      out = 'sources'
    elif groups[1] == ['*ES.cpp.inl']:
      self.user_vars.add(out)  # the entity systems, for the ES codegen loop that follows
    else:
      raise Untranslatable(src)
    dirs = [value(d, 'dirs') for d in self.refs(depth, groups[0])]
    line = 'dagor_glob_sources({} DIRS {} GLOB {}'.format(out, ' '.join(dirs), ' '.join(groups[1]))
    if len(groups) > 3:
      line += ' EXCLUDE "{}"'.format(' '.join(groups[3]).replace('\\\\', '\\'))
    self.emit(depth, line + ')')
    if out == 'sources':
      self.used.add('sources')

  def emit(self, depth, text):
    self.lines.append('  ' * depth + text.replace(' \n', '\n'))

  def todo_line(self, depth, src):
    self.todo += 1
    for i, part in enumerate(re.findall(r'.{1,100}(?:\s|$)', src.strip()) or [src]):
      self.emit(depth, ('# TODO(jam): ' if i == 0 else '#   ') + part.strip())

  def assign(self, depth, var, op, values, src):
    if depth == 0 and op == '=':
      self.locals[var] = values  # for the Location check (Location = prog/$(LibPath) ;)
    try:
      values = self.refs(depth, values)
    except Untranslatable:
      self.todo_line(depth, src)
      return
    if self.lib_mode and var == 'R':
      return  # local R = prog/<lib> ; of the sources below
    if self.lib_mode and var == 'Sources' and op == '+=':
      # engine-relative sources ($(R)/<file>, prog/<file>) compiled into the game or its AOT compiler
      files = [re.sub(r'\$\((\w+)\)', lambda m: ' '.join(self.locals.get(m.group(1), [m.group(0)])), v) for v in values]
      if any('$(' in f or not f.startswith('prog/') for f in files):
        self.todo_line(depth, src)
        return
      head = 'dagor_game_lib(SOURCES '
      self.emit(depth, head + cmake_values(['${DAGOR_ENGINE_ROOT}/' + f for f in files], depth, head) + ')')
      return
    if self.lib_mode and var in ('UseProgLibs', 'AddIncludes') and op == '+=':
      kind = 'deps' if var == 'UseProgLibs' else 'includes'
      try:
        vals = [value(v, kind) for v in values]
      except Untranslatable:
        self.todo_line(depth, src)
        return
      head = 'dagor_game_lib({} '.format('LINK' if kind == 'deps' else 'INCLUDES')
      self.emit(depth, head + cmake_values(vals, depth, head) + ')')
      return
    if var in LIST_VARS:
      name = LIST_VARS[var]
      try:
        if name == 'cpp_opt':
          defines, options = split_cpp_opt(values)
          items = [('defines', defines), ('options', [value(o, 'options') for o in options])]
        elif name == 'c_opt':
          items = [('c_options', [value(o, 'options') for o in values])]
        else:
          items = [(name, [value(v, name) for v in values])]
      except Untranslatable:
        self.todo_line(depth, src)
        return
      for name, vals in items:
        if not vals and (op != '=' or name not in self.used):
          continue
        if op == '+=' or (op == '?=' and name in self.used):
          head = 'list(APPEND {} '.format(name)
          self.emit(depth, head + cmake_values(vals, depth, head) + ')')
        elif vals:
          head = 'set({} '.format(name)
          self.emit(depth, head + cmake_values(vals, depth, head) + ')')
        else:
          self.emit(depth, 'set({})'.format(name))
        self.used.add(name)
      return
    # game modules (build_module.jam): dagor_add_dng_module
    if var == 'Module' and depth == 0 and op == '=' and len(values) == 1:
      self.scalars['Module'] = values
      return
    if var == 'DasModule' and depth == 0:
      self.scalars['DasModule'] = values
      return
    if var == 'ModuleDependsOnVars':
      if 'PhysName' in values:  # build_module.jam includes setup-phys.jam then
        self.emit(depth, 'list(APPEND deps Dagor::Phys)')
        self.used.add('deps')
      return  # otherwise only jam's naming of the library
    if var == 'AddPullVars':
      head = 'list(APPEND pull_vars '
      self.emit(depth, head + cmake_values(values, depth, head) + ')')
      self.used.add('pull_vars')
      return
    if var == 'gamePulls' and op == '+=':
      head = 'dagor_game_lib(PULLS '
      self.emit(depth, head + cmake_values(values, depth, head) + ')')
      return
    if var in IGNORED_VARS or (var in FIXED_VERSIONS and values == [FIXED_VERSIONS[var]]):
      return
    if var == 'FullOOPEnabled' and depth == 0 and values == ['yes']:
      # jam's exceptions with SEH and RTTI for the whole build; in CMake for the program's own code
      self.scalars['Exceptions'] = ['SEH']
      self.scalars['Rtti'] = ['yes']
      return
    if var in ('Platform', 'PlatformArch') and op == '?=':
      return  # the tree's
    if var in BOOL_VARS and op == '?=':
      return  # the default of a tree option
    if var == 'Target' and depth > 0:
      return  # jam named the library after its settings; a CMake tree has one
    if var in SCALAR_VARS and depth == 0 and op in ('=', '?='):
      self.scalars[var] = values
      return
    # <list> = [ GLOB $(Root)/$(Location)[/<dir>] : <patterns> ] ; names relative to <dir>, as :D= makes them
    if len(values) >= 5 and values[0] == '[' and values[1] == 'GLOB' and values[-1] == ']' and values[3] == ':':
      d = values[2]
      sub = re.fullmatch(r'\$\(Root\)/\$\(Location\)(?:/(.*))?', d)
      if sub:
        base = '${CMAKE_CURRENT_SOURCE_DIR}' + ('/' + sub.group(1) if sub.group(1) else '')
        patterns = ' '.join('"{}/{}"'.format(base, p) for p in values[4:-1])
        self.emit(depth, 'file(GLOB {} RELATIVE "{}" CONFIGURE_DEPENDS {})'.format(var, base, patterns))
        self.user_vars.add(var)
        return
    # the jamfile's own lists of sources and dirs
    if re.search(r'(?i)(source|src|folder|dirs?|files)', var) and op in ('=', '+=', '?='):
      try:
        vals = [value(v, 'dirs') for v in values]
      except Untranslatable:
        self.todo_line(depth, src)
        return
      if vals:
        self.nonempty.add(var)
      head = ('list(APPEND {} ' if op == '+=' and var in self.user_vars else 'set({} ').format(var)
      self.emit(depth, head + cmake_values(vals, depth, head) + ')')
      self.user_vars.add(var)
      return
    self.todo_line(depth, src)

  def statements(self, stmts, depth):
    for s in stmts:
      kind = s[0]
      if kind == 'assign':
        _, var, op, values = s
        self.assign(depth, var, op, values, '{} {} {} ;'.format(var, op, ' '.join(values)))
      elif kind == 'on':
        _, var, target, op, values = s
        src = '{} on {} {} {} ;'.format(var, target, op, ' '.join(values))
        if var in ('opt', 'CPPopt') and '$(' not in target:
          self.emit(depth, 'set_property(SOURCE {} APPEND PROPERTY COMPILE_OPTIONS {})'.format(target, ' '.join(values)))
        else:
          self.todo_line(depth, src)
      elif kind == 'include':
        _, path, src = s
        base = os.path.basename(path)
        if base in KNOWN_INCLUDES:
          if base == 'unitTest.jam':
            self.scalars['unitTest'] = True
          if base == 'build.jam':
            self.after_build = True
        elif base == 'defPlatform.jam':
          pass  # the platform comes from the tree
        elif base == 'tools_setup.jam':
          pass  # the tool trees' settings (SSE2, precise floats on Windows) are DagorOptions defaults
        elif base in ('tools_setup_outdir_util.jam', 'tools_setup_outdir_bin.jam'):
          self.scalars['cdk'] = True
        elif base == 'add_quirrel.jam':
          self.scalars['quirrelHeaders'] = True
        elif path.endswith('3rdPartyLibs/phys/setup-phys.jam'):
          self.emit(depth, 'list(APPEND deps Dagor::Phys)')  # the tree's physics engine: its settings and library
          self.used.add('deps')
        elif path.endswith('prog/daNetGame/setup.jam'):
          pass  # the game's switches are the tree's (DagorGame.cmake)
        elif base == 'build_module.jam':
          self.scalars['module'] = True
        elif base == 'add_null_include.jam':
          self.emit(depth, 'list(APPEND force_includes supp/dag_null.h)')
          self.used.add('force_includes')
        else:
          self.todo_line(depth, src)
      elif kind == 'if':
        _, branches, else_block = s
        emitted = False
        start = len(self.lines)
        try:
          conds = [condition(c) for c, _ in branches]
        except Untranslatable:
          self.todo_line(depth, self.source_of(s))
          continue
        for (cond_words, block), cond in zip(branches, conds):
          if cond == 'FALSE':
            continue
          if cond == 'TRUE' and not emitted:
            self.statements(block, depth)
            else_block = None
            emitted = None
            break
          self.emit(depth, ('elseif({})' if emitted else 'if({})').format(cond))
          self.statements(block, depth + 1)
          emitted = True
        if emitted is None:
          continue
        if else_block:
          if emitted:
            self.emit(depth, 'else()')
            self.statements(else_block, depth + 1)
          else:
            self.statements(else_block, depth)
        if emitted:
          self.emit(depth, 'endif()')
          # an if whose branches all came out empty (jam bookkeeping only) is dropped
          construct = self.lines[start:]
          if all(re.fullmatch(r'\s*(if|elseif|else|endif)\(.*\)', l) for l in construct):
            del self.lines[start:]
      elif s[1].startswith('AutoscanBuildLists '):
        try:
          self.autoscan(depth, s[1])
        except Untranslatable:
          self.todo_line(depth, s[1])
      elif self.stringify(depth, s[1]):
        pass
      elif re.fullmatch(r'for (\w+) in \$\((\w+)\) \{ GenESSourceFile \$\(\1\) ; \}', s[1]):
        # the ES codegen of a list of <name>ES.cpp.inl (ES_SOURCES of dagor_add_*)
        var = re.fullmatch(r'for (\w+) in \$\((\w+)\).*', s[1]).group(2)
        self.emit(depth, 'list(APPEND es_sources ${{{}}})'.format(var))
        self.used.add('es_sources')
      elif re.fullmatch(r'GenESSourceFile [\w./]+ ;', s[1]):
        self.emit(depth, 'list(APPEND es_sources {})'.format(s[1].split()[1]))
        self.used.add('es_sources')
      else:
        self.todo_line(depth, s[1])

  def source_of(self, s):
    def text(stmts):
      out = []
      for st in stmts:
        if st[0] == 'assign':
          out.append('{} {} {} ;'.format(st[1], st[2], ' '.join(st[3])))
        elif st[0] == 'on':
          out.append('{} on {} {} {} ;'.format(st[1], st[2], st[3], ' '.join(st[4])))
        elif st[0] == 'if':
          out.append(self.source_of(st))
        else:
          out.append(st[-1])
      return ' '.join(out)
    _, branches, else_block = s
    parts = []
    for n, (cond, block) in enumerate(branches):
      parts.append('{}if {} {{ {} }}'.format('else ' if n else '', ' '.join(cond), text(block)))
    if else_block:
      parts.append('else {{ {} }}'.format(text(else_block)))
    return ' '.join(parts)

  def test_manifest(self, exe):
    """the dagor_add_catch2_test options of the test.blk target of <exe>"""
    path = os.path.join(os.path.dirname(self.jamfile), 'test.blk')
    if not os.path.exists(path):
      return []
    text = open(path, encoding='utf-8', errors='replace').read()
    for block in re.findall(r'target\s*\{(.*?)\}', text, re.S):
      values = re.findall(r'(\w+):[a-z]+=("[^"]*"|\S+)', block)
      get = lambda key: [v.strip('"') for k, v in values if k == key]
      if get('exe') != [exe]:
        continue
      out = []
      for key, kw in (('tag', 'TAGS'), ('requires', 'REQUIRES'), ('platform', 'PLATFORMS')):
        if get(key):
          out.append('{} {}'.format(kw, ' '.join(get(key))))
      for key, kw in (('timeout', 'TIMEOUT'), ('caseTimeout', 'CASE_TIMEOUT'), ('dataDir', 'DATA_DIR')):
        if get(key):
          out.append('{} {}'.format(kw, get(key)[0]))
      if get('serial') and get('serial')[0] in ('yes', 'true', '1'):
        out.append('SERIAL')
      if get('args'):
        out.append('ARGS ' + get('args')[0])
      return out
    return []

  def call(self):
    """the target: dagor_add_library/executable or dagor_add_catch2_test with target_* calls, which the declaration
    converter turns into dagor_add_target() with the sources in a _files.cmake"""
    s = self.scalars
    type_ = (s.get('TargetType') or ['lib'])[0]
    rel = os.path.relpath(os.path.dirname(self.jamfile), os.path.join(ENGINE, 'prog')).replace(os.sep, '/')
    target = (s.get('Target') or [''])[0]
    exe_name = os.path.splitext(os.path.basename(re.sub(r'\$\([^)]*\)', '', target)))[0].rstrip('-~')
    name = rel.replace('/', '.') if type_ == 'lib' or type_ == 'dll' and not exe_name else exe_name
    if s.get('module'):
      # build_module.jam: the .cpp of AllSrcFolder_CPP, the entity systems of AllSrcFolder_ES, the daScript of
      # AllSrcFolder_DAS (the module's pull: DAS_PULL module, which dng_module() makes dagor_add_dng_module's DAS)
      name = rel.replace('/', '.')
      for var, out, glob in (('AllSrcFolder_CPP', 'sources', '*.cpp'), ('AllSrcFolder_ES', 'es_sources', '*ES.cpp.inl'),
                             ('AllSrcFolder_DAS', 'das', '*.das')):
        if var in self.nonempty:
          self.emit(0, 'dagor_glob_sources({} DIRS ${{{}}} GLOB {})'.format(out, var, glob))
          self.used.add(out)
      s['StrictCompile'] = ['yes']
      s.pop('UseQuirrel', None)  # dagor_add_dng_module links Quirrel
    head = []
    if s.get('unitTest'):
      head = ['dagor_add_catch2_test(' + exe_name] + self.test_manifest(exe_name)
    elif type_ == 'exe':
      head = ['dagor_add_executable(' + name] + ([] if s.get('ConsoleExe') == ['yes'] else ['WIN32'])
    else:
      head = ['dagor_add_library(' + name] + (['SHARED'] if type_ == 'dll' else [])
    if s.get('StrictCompile') != ['yes']:
      head.append('LAX')
    if s.get('Config') == ['rel']:
      head.append('NO_CONFIG_POSTFIX')  # jam built it in rel only, so without a config suffix (prog/cmake/DESIGN.md)
    if 'OutDir' in s:
      try:
        head += ['OUTPUT_DIRECTORY', value(s['OutDir'][0], 'dirs')]
      except Untranslatable:
        self.todo_line(0, 'OutDir = {} ;'.format(' '.join(s['OutDir'])))
    if 'sources' in self.used:
      head.append('${sources}')
    self.emit(0, ' '.join(head) + ')')
    deps = (['${deps}'] if 'deps' in self.used else [])
    if s.get('UseQuirrel') == ['yes']:
      deps.append('Dagor::Quirrel')
    elif s.get('quirrelHeaders'):
      deps.append('Dagor::QuirrelHeaders')
    calls = [('target_include_directories', 'includes', 'PRIVATE ${includes}'),
             ('target_compile_definitions', 'defines', 'PRIVATE ${defines}'),
             ('target_compile_options', 'options', 'PRIVATE ${options}'),
             ('target_compile_options', 'c_options', 'PRIVATE "$<$<COMPILE_LANGUAGE:C>:${c_options}>"'),
             ('target_link_options', 'link_options', 'PRIVATE ${link_options}'),
             ('dagor_target_force_include', 'force_includes', '${force_includes}'),
             ('dagor_target_licenses', 'license_files', '${license_files}'),
             ('dagor_target_stringify', 'stringify', '${stringify}'),
             ('dagor_target_stringify', 'stringify_array', 'ARRAY ${stringify_array}'),
             ('dagor_target_es_sources', 'es_sources', '${es_sources}'),
             ('dagor_target_das_aot', 'das', 'PULL module ${das}')]
    if s.get('module') and s.get('DasModule') and 'das' not in self.used:
      self.emit(0, 'dagor_target_das_aot({} PULL module)'.format(name))
    for cmd, var, args in calls:
      if var in self.used:
        self.emit(0, '{}({} {})'.format(cmd, name, args))
    if s.get('module') and 'pull_vars' in self.used:
      self.emit(0, 'set_target_properties({} PROPERTIES PULL_VARS ${{pull_vars}})'.format(name))
    if deps or 'libs' in self.used:
      self.emit(0, 'target_link_libraries({} PRIVATE {})'.format(name, ' '.join(deps + (['${libs}'] if 'libs' in self.used else []))))
    props = []
    for var, prop in (('Exceptions', 'DAGOR_EXCEPTIONS'), ('Rtti', 'DAGOR_RTTI')):
      if s.get(var) in (['yes'], ['no']):
        props += [prop, 'ON' if s[var] == ['yes'] else 'OFF']
      elif s.get(var) == ['SEH']:
        props += [prop, 'SEH']
    if props:
      self.emit(0, 'set_target_properties({} PROPERTIES {})'.format(name, ' '.join(props)))
    if s.get('cdk'):
      self.emit(0, 'dagor_install_cdk({})'.format(name))

  def convert(self, text):
    stmts = Parser(tokens(text)).parse()
    body_start = len(self.lines)
    self.statements(stmts, 0)
    rel = os.path.relpath(self.jamfile, ENGINE).replace(os.sep, '/')
    # the sources are relative to Location, which some jamfiles set to another dir than theirs
    location = ' '.join(self.scalars.get('Location') or [])
    location = re.sub(r'\$\((\w+)\)', lambda m: ' '.join(self.locals.get(m.group(1), [m.group(0)])), location)
    if location and not self.lib_mode and os.path.normpath(location) != os.path.dirname(os.path.normpath(rel)):
      self.todo_line(0, 'Location = {} ; (not the jamfile\'s dir: the paths are relative to it)'.format(location))
    if not self.lib_mode:
      self.lines.append('')
      self.call()
    return '\n'.join(self.lines[body_start:]).replace('\n\n\n', '\n\n').lstrip('\n') + '\n'


def main(argv):
  parser = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
  parser.add_argument('jamfiles', nargs='+')
  parser.add_argument('--write', action='store_true', help='write CMakeLists.txt next to the jamfile')
  parser.add_argument('--force', action='store_true', help='overwrite an existing CMakeLists.txt')
  args = parser.parse_args(argv)
  status = 0
  for jamfile in args.jamfiles:
    with open(jamfile, encoding='utf-8', errors='replace') as f:
      out = Converter(os.path.abspath(jamfile)).convert(f.read())
    if not args.write:
      sys.stdout.write(out)
      continue
    base = os.path.basename(jamfile)
    dest = os.path.join(os.path.dirname(jamfile),
                        base.replace('.jam', '.cmake') if base in ('_lib.jam', '_aot.jam') else 'CMakeLists.txt')
    if os.path.exists(dest) and not args.force:
      print('{} exists, skipped (--force overwrites)'.format(dest), file=sys.stderr)
      status = 1
      continue
    with open(dest, 'w', newline='\n') as f:
      f.write(out)
    print(dest)
  return status


if __name__ == '__main__':
  sys.exit(main(sys.argv[1:]))
