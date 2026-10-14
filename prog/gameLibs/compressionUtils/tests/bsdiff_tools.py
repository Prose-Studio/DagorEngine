"""bsdiffutil and bsapplyutil: a patch made from two files and applied to the first gives the second, byte for byte.

plain: binary data (changed, inserted and removed ranges) with the default compression and each deprecated one
  (vromfs, zlib); the patch is a fraction of the file; patches cut short or with a broken header, an unknown
  compression and the invalid placeholder one ("") are rejected.
vromfs: two versions of a vromfs pack built by vromfsPacker (a file changed, one added, one removed), the patches the
  game's updates are made of.
zstd: both of the above with the zstd compression, the current patch format (per file for vromfs packs).

usage: bsdiff_tools.py plain|vromfs|zstd <bsdiffutil> <bsapplyutil> <vromfsPacker> (in DAGOR_TEST_OUT)
"""
import os
import random
import shutil
import subprocess
import sys

BUILD_BLK = '''rootFolder:t="%(src)s"
output:t="%(pack)s"
allowMkDir:b=yes
pack:b=yes
sign_private_key:t=""
folder{
  path:t="."
  dest_path:t="./"
  scan_subfolders:b=yes
  wildcard:t="*.blk"
  wildcard:t="*.bin"
}
packBlk{
  include:t=".*\\.blk$"
}
'''


def noise(seed, size):
  rng = random.Random(seed)
  return bytes(rng.getrandbits(8) for _ in range(size))


def run(args, cwd):
  result = subprocess.run(args, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  return result.returncode, result.stdout.decode('utf-8', 'replace')


def read(path):
  with open(path, 'rb') as f:
    return f.read()


def write(path, data):
  os.makedirs(os.path.dirname(path), exist_ok=True)
  with open(path, 'wb') as f:
    f.write(data)


def roundtrip(diff, apply, out, old, new, compression, errors):
  """makes the patch from old to new, applies it to old and checks it gives new"""
  name = 'patch-%s' % (compression or 'default')
  patch = os.path.join(out, name + '.bin')
  result = os.path.join(out, name + '.result')
  code, output = run([diff, old, new, patch] + ([compression] if compression else []), out)
  if code != 0:
    errors.append('%s: bsdiffutil exited with %s:\n%s' % (name, code, output))
    return None
  code, output = run([apply, old, result, patch], out)
  if code != 0:
    errors.append('%s: bsapplyutil exited with %s:\n%s' % (name, code, output))
  elif read(result) != read(new):
    errors.append('%s: applied to %s, it does not give %s' % (name, old, new))
  elif os.path.getsize(patch) * 10 > os.path.getsize(new):
    errors.append('%s: %d bytes, not a patch of %d bytes' % (name, os.path.getsize(patch), os.path.getsize(new)))
  return patch


def plain_files(out):
  old = noise(1, 256 * 1024)
  new = bytearray(old)
  new[1000:1016] = b'\0' * 16  # changed
  new[50000:50000] = noise(2, 3000)  # inserted
  del new[150000:152000]  # removed
  new += noise(3, 500)  # appended
  old_path, new_path = os.path.join(out, 'old.bin'), os.path.join(out, 'new.bin')
  write(old_path, old)
  write(new_path, bytes(new))
  return old_path, new_path


def vromfs_packs(packer, out):
  """two versions of a pack of an incompressible blob and BLKs: the blob changed, a BLK added, one removed"""
  blob = noise(1, 256 * 1024)
  versions = [
    ('old', {'blob.bin': blob, 'settings.blk': b'value:i=1\n', 'old.blk': b'removed:b=yes\n'}),
    ('new', {'blob.bin': blob[:100000] + b'changed' + blob[100007:], 'settings.blk': b'value:i=2\n',
             'added/new.blk': b'added:b=yes\n'}),
  ]
  packs = []
  for version, files in versions:
    src = os.path.join(out, 'src-' + version)
    for name, data in files.items():
      write(os.path.join(src, name), data)
    pack = os.path.join(out, version + '.vromfs.bin')
    blk = os.path.join(out, version + '.vromfs.blk')
    with open(blk, 'w') as f:
      f.write(BUILD_BLK % {'src': src.replace('\\', '/'), 'pack': pack.replace('\\', '/')})
    code, output = run([packer, blk, '-platform:PC', '-quiet'], out)
    if code != 0:
      sys.exit('vromfsPacker exited with %s:\n%s' % (code, output))
    packs.append(pack)
  return packs


def rejects(apply, out, old, patch, errors):
  """a patch cut short or with a broken header must not apply"""
  data = read(patch)
  for what, broken in (('cut short', data[:len(data) // 2]), ('with a broken header', b'X' + data[1:])):
    path = os.path.join(out, 'broken.bin')
    result = os.path.join(out, 'broken.result')
    write(path, broken)
    if os.path.exists(result):
      os.remove(result)
    code, output = run([apply, old, result, path], out)
    if code != 1 or os.path.exists(result):
      errors.append('a patch %s was applied (exit code %s, result %s):\n%s' %
                    (what, code, 'written' if os.path.exists(result) else 'not written', output))


def main():
  scenario = sys.argv[1]
  diff, apply, packer = [os.path.abspath(p) for p in sys.argv[2:5]]
  out = os.environ.get('DAGOR_TEST_OUT')
  if not out:
    sys.exit('DAGOR_TEST_OUT is not set (the tests run through CTest)')
  shutil.rmtree(out, ignore_errors=True)
  os.makedirs(out)
  out = os.path.abspath(out)
  errors = []
  if scenario == 'plain':
    old, new = plain_files(out)
    patch = None
    for compression in (None, 'vromfs', 'zlib'):
      patch = roundtrip(diff, apply, out, old, new, compression, errors) or patch
    if patch:
      rejects(apply, out, old, patch, errors)
    # an unknown name, and the empty one of the invalid placeholder compression (which once crashed it)
    for compression in ('bogus', ''):
      code, output = run([diff, old, new, os.path.join(out, 'bogus.bin'), compression], out)
      if code != 1:
        errors.append('the compression "%s" was not rejected (exit code %s):\n%s' % (compression, code, output))
  elif scenario == 'vromfs':
    old, new = vromfs_packs(packer, out)
    for compression in (None, 'vromfs', 'zlib'):
      roundtrip(diff, apply, out, old, new, compression, errors)
  elif scenario == 'zstd':
    plain = os.path.join(out, 'plain')
    os.makedirs(plain)
    old, new = plain_files(plain)
    roundtrip(diff, apply, plain, old, new, 'zstd', errors)
    packs = os.path.join(out, 'vromfs')
    os.makedirs(packs)
    old, new = vromfs_packs(packer, packs)
    roundtrip(diff, apply, packs, old, new, 'zstd', errors)
  else:
    sys.exit('unknown scenario ' + scenario)
  if errors:
    sys.exit('\n'.join(errors))
  print('%s: patches made and applied' % scenario)


if __name__ == '__main__':
  main()
