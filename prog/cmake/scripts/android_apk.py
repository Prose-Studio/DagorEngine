"""android_apk.py <config>: the APK of a NativeActivity app (dagor_android_apk), with the Android SDK's build tools.

<config> has one key=value per line (a key given again adds to its list): apk (the APK to write), work (a dir for the
intermediate files), manifest, label, lib (the app's shared library), strip (the NDK's llvm-strip), abi, java (the
Java sources of the app and of its libraries), asset (<path in the APK's assets>|<file>), icon (a PNG), min_api,
android_jar, build_tools, java_home.

The resources (the label, the icon) go through aapt2, the Java sources through javac and d8 (classes.dex), the library
goes in without its debug information (the symbols stay in the build's copy). The APK is aligned and signed with apksigner: by the keystore that DAGOR_ANDROID_KEYSTORE names (its password in
DAGOR_ANDROID_KEYSTORE_PASS, the key's alias and password in DAGOR_ANDROID_KEY_ALIAS and DAGOR_ANDROID_KEY_PASS),
otherwise by the Android debug keystore (~/.android/debug.keystore, made like the SDK's tools make it). Nothing is
done while the inputs are those of the APK there.
"""
import hashlib
import os
import shutil
import subprocess
import sys
import zipfile
from xml.sax.saxutils import escape


def read_config(path):
  cfg = {}
  with open(path, encoding='utf-8') as f:
    for line in f:
      key, _, value = line.rstrip('\n').partition('=')
      if key and value:
        cfg.setdefault(key, []).append(value)
  return cfg


def run(*cmd, env=None):
  proc = subprocess.run([str(a) for a in cmd], capture_output=True, text=True, env=env)
  if proc.returncode:
    sys.exit(f'android_apk: {" ".join(map(str, cmd))} failed:\n{proc.stdout}{proc.stderr}')


def tool(build_tools, name):
  """A build tool: a program, or on Windows a .bat (d8, apksigner)."""
  for ext in ('.exe', '.bat', '') if os.name == 'nt' else ('',):
    path = os.path.join(build_tools, name + ext)
    if os.path.exists(path):
      return path
  sys.exit(f'android_apk: {build_tools} has no {name}')


def stamp_of(config_path, cfg):
  """What the APK is made of: the config and the size and time of each input file."""
  digest = hashlib.sha256(open(config_path, 'rb').read())
  files = [__file__] + cfg.get('manifest', []) + cfg.get('lib', []) + cfg.get('java', []) + cfg.get('icon', [])
  files += [a.split('|', 1)[1] for a in cfg.get('asset', [])]
  for path in files:
    st = os.stat(path)
    digest.update(f'{path}|{st.st_size}|{st.st_mtime_ns}\n'.encode())
  return digest.hexdigest()


def signing(java_env, keytool):
  """apksigner's arguments for the keystore to sign with."""
  keystore = os.environ.get('DAGOR_ANDROID_KEYSTORE')
  if keystore:
    store_pass = os.environ.get('DAGOR_ANDROID_KEYSTORE_PASS', '')
    args = ['--ks', keystore, '--ks-pass', 'env:DAGOR_ANDROID_KEYSTORE_PASS']
    if os.environ.get('DAGOR_ANDROID_KEY_ALIAS'):
      args += ['--ks-key-alias', os.environ['DAGOR_ANDROID_KEY_ALIAS']]
    if os.environ.get('DAGOR_ANDROID_KEY_PASS'):
      args += ['--key-pass', 'env:DAGOR_ANDROID_KEY_PASS']
    if not store_pass:
      sys.exit('android_apk: DAGOR_ANDROID_KEYSTORE needs DAGOR_ANDROID_KEYSTORE_PASS')
    return args
  keystore = os.path.join(os.path.expanduser('~'), '.android', 'debug.keystore')
  if not os.path.exists(keystore):
    os.makedirs(os.path.dirname(keystore), exist_ok=True)
    run(keytool, '-genkeypair', '-keystore', keystore, '-storepass', 'android', '-keypass', 'android',
        '-alias', 'androiddebugkey', '-keyalg', 'RSA', '-keysize', '2048', '-validity', '10000',
        '-dname', 'CN=Android Debug,O=Android,C=US', env=java_env)
  return ['--ks', keystore, '--ks-pass', 'pass:android', '--key-pass', 'pass:android']


def main(config_path):
  cfg = read_config(config_path)
  one = {key: values[0] for key, values in cfg.items()}
  apk, work = one['apk'], one['work']
  stamp_file = os.path.join(work, 'stamp')
  stamp = stamp_of(config_path, cfg)
  if os.path.exists(apk) and os.path.exists(stamp_file) and open(stamp_file).read() == stamp:
    return
  shutil.rmtree(work, ignore_errors=True)
  os.makedirs(work)
  build_tools, android_jar = one['build_tools'], one['android_jar']
  java_env = dict(os.environ, JAVA_HOME=one['java_home'])
  java_bin = os.path.join(one['java_home'], 'bin')
  java_env['PATH'] = java_bin + os.pathsep + java_env.get('PATH', '')
  exe = '.exe' if os.name == 'nt' else ''

  # resources: the label and the icon
  res = os.path.join(work, 'res')
  os.makedirs(os.path.join(res, 'values'))
  with open(os.path.join(res, 'values', 'strings.xml'), 'w', encoding='utf-8') as f:
    f.write(f'<?xml version="1.0" encoding="utf-8"?>\n<resources>\n'
            f'  <string name="app_name">{escape(one["label"])}</string>\n</resources>\n')
  if 'icon' in one:
    os.makedirs(os.path.join(res, 'mipmap'))
    shutil.copy(one['icon'], os.path.join(res, 'mipmap', 'icon.png'))
  aapt2 = tool(build_tools, 'aapt2')
  run(aapt2, 'compile', '--dir', res, '-o', os.path.join(work, 'res.zip'))
  base = os.path.join(work, 'base.apk')
  run(aapt2, 'link', '-o', base, '-I', android_jar, '--manifest', one['manifest'], os.path.join(work, 'res.zip'))

  # the code: classes.dex of the Java sources
  dex = None
  java = sorted(set(cfg.get('java', [])))
  if java:
    classes = os.path.join(work, 'classes')
    run(os.path.join(java_bin, 'javac' + exe), '-nowarn', '-Xlint:-options', '--release', '11',
        '-classpath', android_jar, '-d', classes, *java, env=java_env)
    class_files = [os.path.join(d, f) for d, _, fs in os.walk(classes) for f in fs if f.endswith('.class')]
    dex_dir = os.path.join(work, 'dex')
    os.makedirs(dex_dir)
    run(tool(build_tools, 'd8'), '--release', '--min-api', one['min_api'], '--lib', android_jar, '--output', dex_dir,
        *class_files, env=java_env)
    dex = os.path.join(dex_dir, 'classes.dex')

  # the APK: the linked resources and manifest, the code, the app's library and the assets
  lib = os.path.join(work, os.path.basename(one['lib']))
  run(one['strip'], '--strip-debug', '-o', lib, one['lib'])
  unaligned = os.path.join(work, 'unaligned.apk')
  with zipfile.ZipFile(base) as src, zipfile.ZipFile(unaligned, 'w', zipfile.ZIP_DEFLATED) as out:
    for item in src.infolist():
      out.writestr(item, src.read(item.filename))
    if dex:
      out.write(dex, 'classes.dex')
    out.write(lib, f'lib/{one["abi"]}/{os.path.basename(lib)}')
    for asset in sorted(cfg.get('asset', [])):
      dest, path = asset.split('|', 1)
      out.write(path, f'assets/{dest}')
  aligned = os.path.join(work, 'aligned.apk')
  run(tool(build_tools, 'zipalign'), '-p', '-f', '4', unaligned, aligned)
  signed = os.path.join(work, 'signed.apk')
  run(tool(build_tools, 'apksigner'), 'sign', *signing(java_env, os.path.join(java_bin, 'keytool' + exe)),
      '--out', signed, aligned, env=java_env)
  os.makedirs(os.path.dirname(apk), exist_ok=True)
  os.replace(signed, apk)
  with open(stamp_file, 'w') as f:
    f.write(stamp)
  print(f'android_apk: {apk}')


if __name__ == '__main__':
  if len(sys.argv) != 2:
    sys.exit(__doc__)
  main(sys.argv[1])
