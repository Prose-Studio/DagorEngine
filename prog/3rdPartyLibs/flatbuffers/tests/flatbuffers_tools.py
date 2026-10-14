"""flatc and flathash, the FlatBuffers schema compiler and name hasher of the CDK.

json: monster.json (every kind of field of monster.fbs) compiled to a binary and back to JSON gives the values back
  (the defaults filled in, the hashed ids as flathash computes them), that JSON compiles to the same binary, and JSON
  or a binary that breaks the schema is rejected.
cpp: the C++ the engine keeps generated from its schemas (the web browser's IPC messages, made by its generate.py) is
  what flatc generates from them now.
hash: flathash gives the FNV-1 and FNV-1a hashes: the published FNV test values for 32 bits, FlatBuffers' own for 64
  (its offset basis is 0xcbf29ce484222645, not FNV's 0xcbf29ce484222325, and flatc stores those).

usage: flatbuffers_tools.py json|cpp|hash <flatc> <flathash> (in DAGOR_TEST_OUT)
"""
import json
import math
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROG = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
IPC_SCHEMAS = os.path.join(PROG, '1stPartyLibs', 'webbrowser', 'lib', 'ipc', 'msg')
HASHES = {  # of 'a' and 'foobar'
  'fnv1_32': (0x050c5d7e, 0x31f0b262),
  'fnv1a_32': (0xe40c292c, 0xbf9cf968),
  'fnv1_64': (0xaf66dd4c8607075e, 0xdfa2f343546bbae2),
  'fnv1a_64': (0xaf66bc4c8606cf2c, 0x09d3072cda4f5808),
}


def run(args, cwd):
  result = subprocess.run(args, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  return result.returncode, result.stdout.decode('utf-8', 'replace').replace('\r\n', '\n')


def run_ok(args, cwd):
  code, output = run(args, cwd)
  if code != 0:
    sys.exit('%s\nexited with %d:\n%s' % (' '.join(args), code, output))
  return output


def read(path):
  with open(path, 'rb') as f:
    return f.read()


def same(expected, actual, path, errors):
  if isinstance(expected, dict) and isinstance(actual, dict):
    for k in sorted(set(expected) | set(actual)):
      if k not in actual or k not in expected:
        errors.append('%s/%s: %s' % (path, k, 'missing' if k not in actual else 'not expected'))
      else:
        same(expected[k], actual[k], '%s/%s' % (path, k), errors)
  elif isinstance(expected, list) and isinstance(actual, list) and len(expected) == len(actual):
    for i, (e, a) in enumerate(zip(expected, actual)):
      same(e, a, '%s[%d]' % (path, i), errors)
  elif isinstance(expected, float) and isinstance(actual, (int, float)) and not isinstance(actual, bool):
    if not math.isclose(expected, actual, rel_tol=1e-7):
      errors.append('%s: %r, expected %r' % (path, actual, expected))
  elif type(expected) is not type(actual) or expected != actual:
    errors.append('%s: %r, expected %r' % (path, actual, expected))


def flathash(tool, algorithm, strings, out):
  return [int(line) for line in run_ok([tool, algorithm, '-d', '--'] + strings, out).split()]


def check_json(flatc, hasher, out, errors):
  schema, source = os.path.join(HERE, 'monster.fbs'), os.path.join(HERE, 'monster.json')
  binary = os.path.join(out, 'bin', 'monster.dtst')
  run_ok([flatc, '-b', '-o', os.path.dirname(binary), schema, source], out)
  if read(binary)[4:8] != b'DTST':
    errors.append('%s has not the file identifier DTST' % binary)
  exported = os.path.join(out, 'json', 'monster.json')
  run_ok([flatc, '--json', '--strict-json', '--defaults-json', '-o', os.path.dirname(exported), schema, '--', binary],
         out)
  with open(exported, encoding='utf-8') as f:
    actual = json.load(f)
  with open(source, encoding='utf-8') as f:
    expected = json.load(f)
  expected['mana'] = 150  # the defaults
  expected['weapons'][1]['damage'] = 10
  expected['id32'] = flathash(hasher, 'fnv1a_32', ['foobar'], out)[0]  # the hashed ids
  expected['id64'] = flathash(hasher, 'fnv1a_64', ['foobar'], out)[0]
  same(expected, actual, '', errors)
  again = os.path.join(out, 'again', 'monster.dtst')
  run_ok([flatc, '-b', '-o', os.path.dirname(again), schema, exported], out)
  if read(again) != read(binary):
    errors.append('the exported JSON compiles to another binary than the source JSON')

  rejected = [
    ('{"hp": 1}', 'required field is missing: name'),
    ('{"name": "x", "hp": 40000}', 'constant does not fit'),
    ('{"name": "x", "color": "Purple"}', 'Purple'),
  ]
  for i, (text, message) in enumerate(rejected):
    path = os.path.join(out, 'bad%d.json' % i)
    with open(path, 'w') as f:
      f.write(text)
    code, output = run([flatc, '-b', '-o', os.path.join(out, 'bad'), schema, path], out)
    if code != 1 or message not in output:
      errors.append('%s was not rejected with "%s" (exit code %d):\n%s' % (text, message, code, output))
  foreign = os.path.join(out, 'foreign.dtst')
  with open(foreign, 'wb') as f:
    f.write(b'\x0c\0\0\0XXXX' + b'\0' * 16)
  code, output = run([flatc, '--json', '-o', os.path.join(out, 'bad'), schema, '--', foreign], out)
  if code != 1 or 'does not have expected file_identifier' not in output:
    errors.append('a binary of another file identifier was not rejected (exit code %d):\n%s' % (code, output))


def check_cpp(flatc, out, errors):
  schemas = sorted(f for f in os.listdir(IPC_SCHEMAS) if f.endswith('.fbs'))
  run_ok([flatc, '--cpp', '--scoped-enums', '-o', out] + [os.path.join(IPC_SCHEMAS, f) for f in schemas], out)
  for schema in schemas:
    header = os.path.splitext(schema)[0] + '_generated.h'
    kept = read(os.path.join(IPC_SCHEMAS, header)).replace(b'\r\n', b'\n').split(b'\n')
    generated = read(os.path.join(out, header)).replace(b'\r\n', b'\n').split(b'\n')
    for line, (k, g) in enumerate(zip(kept + [b'<end of file>'], generated + [b'<end of file>'])):
      if k != g:
        errors.append('%s differs from what flatc generates at line %d:\n  kept:      %s\n  generated: %s' %
                      (os.path.join(IPC_SCHEMAS, header), line + 1, k.decode('utf-8', 'replace'),
                       g.decode('utf-8', 'replace')))
        break


def check_hash(hasher, out, errors):
  for algorithm, expected in sorted(HASHES.items()):
    actual = flathash(hasher, algorithm, ['a', 'foobar'], out)
    if actual != list(expected):
      errors.append('%s: %s, expected %s' % (algorithm, [hex(h) for h in actual], [hex(h) for h in expected]))
  output = run_ok([hasher, 'fnv1a_32', '-0x', 'a'], out).strip()
  if output != '0xe40c292c':
    errors.append('fnv1a_32 -0x a: %s, expected 0xe40c292c' % output)


def main():
  scenario = sys.argv[1]
  flatc, hasher = [os.path.abspath(p) for p in sys.argv[2:4]]
  out = os.environ.get('DAGOR_TEST_OUT')
  if not out:
    sys.exit('DAGOR_TEST_OUT is not set (the tests run through CTest)')
  shutil.rmtree(out, ignore_errors=True)
  os.makedirs(out)
  out = os.path.abspath(out)
  errors = []
  if scenario == 'json':
    check_json(flatc, hasher, out, errors)
  elif scenario == 'cpp':
    check_cpp(flatc, out, errors)
  elif scenario == 'hash':
    check_hash(hasher, out, errors)
  else:
    sys.exit('unknown scenario ' + scenario)
  if errors:
    sys.exit('\n'.join(errors))
  print('%s: as expected' % scenario)


if __name__ == '__main__':
  main()
