"""resCleanUtil: the GRP/DxP files of a game root that its pack list (resPacks.blk in grp_hdr.vromfs.bin) does not
reference, listed and, with -clean, removed; -validate checks the listed ones against the list's MD5s.

The pack list and its vromfs are built here with vromfsPacker, as the asset build ships them. The tool never reads the
packs themselves (it lists, hashes and deletes files), so they are files of a few bytes.

usage: res_clean.py <resCleanUtil> <vromfsPacker> (in DAGOR_TEST_OUT)
"""
import hashlib
import os
import shutil
import subprocess
import sys

PACKS = {  # path in the game root: content
  'a.grp': b'pack a',
  'sub/c.grp': b'pack c',
  't.dxp.bin': b'texture pack',
  'stale.grp': b'stale pack',
  'sub/stale.dxp.bin': b'stale texture pack',
  'x.tmp': b'unused, by its extension',
  'other.txt': b'not a pack',
}
LISTED = ['a.grp', 'sub/c.grp', 't.dxp.bin']
UNREFERENCED = ['stale.grp', 'sub/stale.dxp.bin', 'x.tmp']
PACK_LIST = '''gameResPacks{
  pack:t="a.grp"
  pack:t="sub/c.grp"
}
ddsxTexPacks{
  pack:t="t.dxp.bin"
}
unused:t=".tmp"
hash_md5{
  "a.grp":t="%(a.grp)s"
  "t.dxp.bin":t="%(t.dxp.bin)s"
}
'''
BUILD_BLK = '''rootFolder:t="%(src)s"
output:t="%(pack)s"
pack:b=yes
sign_private_key:t=""
folder{
  path:t="."
  dest_path:t="./"
  wildcard:t="*.blk"
}
packBlk{
  include:t=".*\\.blk$"
}
'''


def run(args, cwd):
  result = subprocess.run(args, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  return result.returncode, result.stdout.decode('utf-8', 'replace').replace('\r\n', '\n')


def write(path, data):
  os.makedirs(os.path.dirname(path), exist_ok=True)
  with open(path, 'wb') as f:
    f.write(data)


def norm(path):
  return os.path.normcase(os.path.normpath(path))


def build_list(packer, out, name, blk_name, md5s):
  """a vromfs <name> holding the pack list <blk_name>"""
  src = os.path.join(out, 'list-' + name)
  write(os.path.join(src, blk_name), (PACK_LIST % md5s).encode('utf-8'))
  blk = os.path.join(out, name + '.blk')
  pack = os.path.join(out, 'root', name)
  with open(blk, 'w') as f:
    f.write(BUILD_BLK % {'src': src.replace('\\', '/'), 'pack': pack.replace('\\', '/')})
  code, output = run([packer, blk, '-platform:PC', '-quiet'], out)
  if code != 0:
    sys.exit('vromfsPacker exited with %d:\n%s' % (code, output))


def main():
  tool, packer = [os.path.abspath(p) for p in sys.argv[1:3]]
  out = os.environ.get('DAGOR_TEST_OUT')
  if not out:
    sys.exit('DAGOR_TEST_OUT is not set (the tests run through CTest)')
  shutil.rmtree(out, ignore_errors=True)
  out = os.path.abspath(out)
  root = os.path.join(out, 'root')
  for name, data in PACKS.items():
    write(os.path.join(root, name), data)
  md5s = {name: hashlib.md5(PACKS[name]).hexdigest() for name in ('a.grp', 't.dxp.bin')}
  build_list(packer, out, 'grp_hdr.vromfs.bin', 'resPacks.blk', md5s)
  build_list(packer, out, 'bad_hdr.vromfs.bin', 'badPacks.blk', dict(md5s, **{'t.dxp.bin': '0' * 32}))
  root_arg = root.replace('\\', '/')
  errors = []

  def expect(args, code, what):
    actual, output = run([tool] + args + [root_arg], out)
    if actual != code:
      errors.append('%s: exited with %d, expected %d:\n%s' % (what, actual, code, output))
    return output

  def listed(output):
    return sorted(norm(line) for line in output.split('\n') if norm(line).startswith(norm(root) + os.sep))

  unreferenced = sorted(norm(os.path.join(root, name)) for name in UNREFERENCED)
  output = expect([], 0, 'listing')
  if listed(output) != unreferenced:
    errors.append('listed as unreferenced:\n  %s\nexpected\n  %s' % ('\n  '.join(listed(output)),
                                                                  '\n  '.join(unreferenced)))
  expect(['-validate'], 0, 'validating the right MD5s')
  output = expect(['-validate', '-vfs:bad_hdr.vromfs.bin', '-resBlk:badPacks.blk'], 13, 'validating a wrong MD5')
  if 'validation failed' not in output or 't.dxp.bin' not in output:
    errors.append('the wrong MD5 of t.dxp.bin was not reported:\n' + output)
  expect(['-vfs:missing.vromfs.bin'], 13, 'a missing pack list vromfs')
  expect(['-clean'], 0, 'cleaning')
  left = sorted(os.path.relpath(os.path.join(d, f), root).replace('\\', '/') for d, _, files in os.walk(root)
                for f in files)
  kept = sorted(LISTED + ['other.txt', 'grp_hdr.vromfs.bin', 'bad_hdr.vromfs.bin'])
  if left != kept:
    errors.append('-clean left %s, expected %s' % (left, kept))
  if errors:
    sys.exit('\n'.join(errors))
  print('%d unreferenced of %d files found and removed' % (len(UNREFERENCED), len(PACKS)))


if __name__ == '__main__':
  main()
