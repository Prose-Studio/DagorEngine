"""vromfsPacker: a directory packed by a build BLK (as games pack theirs) and unpacked again.

The pack holds exactly the files the BLK selects (wildcards, the exclude regexp), byte for byte except what the BLK
processes: BLKs preprocessed for the target (#if_target, #if_def with -D:) and packed to binary BLK (which binBlk reads
back), scripts preprocessed with their lines kept. Packing is deterministic (the same pack twice), the target selects
the preprocessing, -writeVersion stamps the version -dumpver reads, -dump lists the files with their sizes and rejects
a file that is no pack. A file of a long path (LONG_PATH characters: its directory search once cut such paths and left
the file out silently) is packed; a path past the longest the engine handles (DAGOR_MAX_PATH: 260 characters on
Windows, 516 elsewhere) fails the pack loudly instead.

usage: vromfs_pack.py <vromfsPacker> <binBlk> (in DAGOR_TEST_OUT)
"""
import os
import re
import shutil
import subprocess
import sys

BLOB = bytes(range(256)) * 64
SOURCES = {
  'settings.blk': b'''// settings: preprocessed for the target and packed as binary BLK
name:t="test"
#if_target(PC)
platform:t="pc"
#else
platform:t="other"
#endif
#if_def(EXTRA)
extra:b=yes
#endif
value:i=42
block{
  pos:p3=1, 2, 3
}
''',
  'scripts/main.nut': b'''// a script: preprocessed with its lines kept
let x = 1
#if_target(PC)
let y = "pc"
#endif
return x
''',
  'scripts/sub/notes.txt': b'copied as is\r\nwith both line ends\n#if_target(PC) is not a directive here\n',
  'data/blob.bin': BLOB,
  'data/empty.bin': b'',
  'data/_private.blk': b'secret:b=yes\n',  # excluded by the regexp
  'readme.md': b'# matches no wildcard\n',
}
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
  wildcard:t="*.nut"
  wildcard:t="*.txt"
  wildcard:t="*.bin"
}
exclude{
  exclude:t="(^|/)_[^/]*\\.blk$"
}
preprocess{
  ext:t="blk"
  ext:t="nut"
  keepLines{
    include:t=".*\\.nut$"
  }
}
packBlk{
  include:t=".*\\.blk$"
}
'''
PACKED = ['data/blob.bin', 'data/empty.bin', 'scripts/main.nut', 'scripts/sub/notes.txt', 'settings.blk']
LONG_PATH = 240  # past the 211 characters the search once kept, within Windows' 259 (as unpacked too)
TOO_LONG_PATH = 1100  # past DAGOR_MAX_PATH everywhere
# per target (and defines): the script with the directives' lines blank, the settings BLK as binBlk writes it
EXPECTED = {
  'PC': (b'\nlet x = 1\n\nlet y = "pc"\n\nreturn x\n',
         'name:t="test"\nplatform:t="pc"\nextra:b=yes\nvalue:i=42\n\nblock{\n  pos:p3=1, 2, 3\n}\n'),
  'and': (b'\nlet x = 1\n\n\n\nreturn x\n',
          'name:t="test"\nplatform:t="other"\nvalue:i=42\n\nblock{\n  pos:p3=1, 2, 3\n}\n'),
}


def outcome(args, cwd):
  result = subprocess.run(args, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  return result.returncode, result.stdout.decode('utf-8', 'replace').replace('\r\n', '\n')


def run(args, cwd):
  code, output = outcome(args, cwd)
  if code != 0:
    sys.exit('%s\nexited with %d:\n%s' % (' '.join(args), code, output))
  return output


def read(path):
  with open(path, 'rb') as f:
    return f.read()


def check(cond, message, errors):
  if not cond:
    errors.append(message)


def slashes(path):
  return path.replace('\\', '/')


def write_tree(src, files):
  for name, data in files.items():
    path = os.path.join(src, name)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'wb') as f:
      f.write(data)


def write_build_blk(path, src, pack):
  with open(path, 'w') as f:
    f.write(BUILD_BLK % {'src': slashes(src), 'pack': slashes(pack)})


def main():
  packer, binblk = [os.path.abspath(p) for p in sys.argv[1:3]]
  out = os.environ.get('DAGOR_TEST_OUT')
  if not out:
    sys.exit('DAGOR_TEST_OUT is not set (the tests run through CTest)')
  shutil.rmtree(out, ignore_errors=True)
  out = os.path.abspath(out)
  src = os.path.join(out, 'src')
  sources = dict(SOURCES)
  pad = LONG_PATH - len(os.path.join(src, 'long', '', 'deep.txt'))
  if pad > 0:
    sources['long/%s/deep.txt' % ('p' * pad)] = b'deep'
  else:
    print('%s leaves no room for a path of %d characters: not checked' % (src, LONG_PATH))
  packed = sorted(PACKED + [name for name in sources if name.startswith('long/')])
  write_tree(src, sources)
  pack = os.path.join(out, 'test.vromfs.bin')
  write_build_blk(os.path.join(out, 'build.blk'), src, pack)
  errors = []

  for target, defines in (('PC', ['-D:EXTRA']), ('and', [])):
    build = ['build.blk', '-platform:' + target, '-quiet'] + defines
    run([packer] + build, out)
    first = read(pack)
    run([packer] + build, out)
    check(read(pack) == first, '%s: packing the same sources twice made different packs' % target, errors)
    check(first[:4] == b'VRFs', '%s: the pack does not start with VRFs: %r' % (target, first[:4]), errors)

    listing = run([packer, '-dump', pack], out)
    listed = dict(re.findall(r'^  (\S+), sz=(\d+)$', listing, re.M))
    check(sorted(listed) == packed, '%s: -dump lists %s, expected %s' % (target, sorted(listed), packed), errors)

    unpacked = os.path.join(out, 'unpacked-' + target)
    run([packer, '-u', pack, unpacked], out)
    files = sorted(slashes(os.path.relpath(os.path.join(d, f), unpacked)) for d, _, names in os.walk(unpacked)
                   for f in names)
    check(files == packed, '%s: unpacked %s, expected %s' % (target, files, packed), errors)
    for name in files:
      data = read(os.path.join(unpacked, name))
      check(name not in listed or int(listed[name]) == len(data),
            '%s: -dump says %s has %s bytes, it unpacks to %d' % (target, name, listed.get(name), len(data)), errors)
      if name in sources and not name.endswith(('.blk', '.nut')):
        check(data == sources[name], '%s: %s is not the source' % (target, name), errors)
    script, settings = EXPECTED[target]
    actual = read(os.path.join(unpacked, 'scripts/main.nut'))
    check(actual == script, '%s: scripts/main.nut is %r, expected %r' % (target, actual, script), errors)
    blk = os.path.join(unpacked, 'settings.blk')
    check(read(blk)[:1] == b'\x01', '%s: settings.blk is not packed to binary BLK' % target, errors)
    text = os.path.join(out, 'settings-%s.blk' % target)
    run([binblk, blk, text, '-t', '-h'], out)
    actual = read(text).decode('utf-8').replace('\r\n', '\n')  # binBlk writes the platform's line ends
    check(actual == settings, '%s: settings.blk reads as\n%s\nexpected\n%s' % (target, actual, settings), errors)

  run([packer, 'build.blk', '-platform:PC', '-quiet', '-writeVersion:1.2.3.4'], out)
  version = run([packer, '-dumpver', pack], out)
  check('VROMFS content version 1.2.3.4' in version, '-dumpver does not read the version written:\n' + version, errors)

  bogus = os.path.join(out, 'bogus.vromfs.bin')
  with open(bogus, 'wb') as f:
    f.write(SOURCES['readme.md'])
  code, output = outcome([packer, '-dump', bogus], out)
  check(code == 13 and 'VRFS label not found' in output,
        '-dump of a file that is no pack exited with %d:\n%s' % (code, output), errors)

  # a tree of 100-character dirs past the engine's limit, where the file system makes one (Windows needs long paths)
  too_long = os.path.join(out, 'too-long')
  try:
    write_tree(too_long, {'/'.join(['q' * 100] * (TOO_LONG_PATH // 101 + 1)) + '/x.txt': b'x'})
  except OSError as e:
    print('no path of %d characters here (%s): its failure is not checked' % (TOO_LONG_PATH, e))
  else:
    write_build_blk(os.path.join(out, 'too_long.blk'), too_long, os.path.join(out, 'too_long.vromfs.bin'))
    code, output = outcome([packer, 'too_long.blk', '-platform:PC', '-quiet'], out)
    check(code == 13 and 'path too long' in output,
          'the pack of a path past the limit exited with %d:\n%s' % (code, output), errors)

  if errors:
    sys.exit('\n'.join(errors))
  print('packed, listed and unpacked %d files for PC and and' % len(packed))


if __name__ == '__main__':
  main()
