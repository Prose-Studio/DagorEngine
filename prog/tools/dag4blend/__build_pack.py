"""__build_pack.py <zip>: packs the dag4blend add-on (this dir, as dag4blend/..., with the pyparsing and datablock modules
of pythonCommon) into <zip>, the archive Blender installs. The CDK tree builds it (target dag4blend) and installs it into
tools/dagor_cdk/universal."""
import os
import sys
import zipfile

ADDON = os.path.dirname(os.path.abspath(__file__))
COMMON = os.path.join(os.path.dirname(ADDON), 'pythonCommon')
EXCLUDE_FILES = {'__build_pack.py', 'CMakeLists.txt'}  # in the add-on's dir
EXCLUDE_DIRS = {'additional', 'tests'}  # in the add-on's dir
EXCLUDE_EXTENSIONS = ('.bak', '.blend1', '.zip', '.pyc')  # backups of WinMerge and Blender, archives, bytecode


def addon_files():
  """(path, name in the archive) of the add-on's files"""
  for root, dirs, files in os.walk(ADDON):
    top = root == ADDON
    dirs[:] = sorted(d for d in dirs if d != '__pycache__' and not (top and d in EXCLUDE_DIRS))
    for fn in sorted(files):
      if fn.endswith(EXCLUDE_EXTENSIONS) or (top and fn in EXCLUDE_FILES):
        continue
      path = os.path.join(root, fn)
      yield path, 'dag4blend/' + os.path.relpath(path, ADDON).replace('\\', '/')
  for fn in ('pyparsing.py', 'datablock.py'):
    yield os.path.join(COMMON, fn), 'dag4blend/' + fn


def main(argv):
  if len(argv) != 2:
    print('usage: {} <zip>'.format(argv[0]))
    return 1
  dest = os.path.abspath(argv[1])
  os.makedirs(os.path.dirname(dest), exist_ok=True)
  files = list(addon_files())
  with zipfile.ZipFile(dest, 'w', compression=zipfile.ZIP_LZMA) as zf:
    for path, name in files:
      zf.write(path, name)
  print('packed {} files into {}'.format(len(files), dest))
  return 0


if __name__ == '__main__':
  sys.exit(main(sys.argv))
