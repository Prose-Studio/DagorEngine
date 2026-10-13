# Regenerates the C++ of the IPC messages (*_generated.h, kept in the repo) from the schemas here with the engine's
# flatc: FLATC, or the one of the engine's cdk tree (cd prog && cmake --build --preset <host>-cdk --target flatc).
import glob
import os
import subprocess
import sys

_here = os.path.dirname(os.path.abspath(__file__))
_engine = os.path.normpath(os.path.join(_here, '..', '..', '..', '..', '..', '..'))
_host = {'win32': 'windows', 'darwin': 'macos'}.get(sys.platform, 'linux')
_exe = '.exe' if _host == 'windows' else ''
flatc = os.environ.get('FLATC') or os.path.join(_engine, 'build', _host + '-cdk', 'bin', 'flatc' + _exe)

cmd = [flatc, '--cpp', '--scoped-enums', '-o', _here] + sorted(glob.glob(os.path.join(_here, '*.fbs')))
print(' '.join(cmd))
sys.exit(subprocess.call(cmd))
