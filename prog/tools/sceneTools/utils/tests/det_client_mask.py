"""detClientMask: the lightmap masks of the clients of a distributed light computation.

From the computation's log (which client computed which range of samples, in the pass between "started pass" and
"finished pass") and the lightmap's sample binding (the LM records of the light binding data: the lightmap texels each
sample lights), it writes <client>-mask.tga for each client, $none$-mask.tga for the samples no client computed and
$white$-mask.tga for the texels no sample lights: grey (the client's index times 240 / the client count, 254 for no
client, 253 for no sample) with the texels of the mask in alpha. The inputs are written here in the formats the tool
reads (its LtBindHeader and tagged blocks).

masks: two clients (one with two ranges, a third after the pass, which must be ignored).
no-clients: a pass no client reported on: only the masks of no client and no sample.

usage: det_client_mask.py masks|no-clients <detClientMask> (in DAGOR_TEST_OUT)
"""
import os
import shutil
import struct
import subprocess
import sys

W, H = 4, 3
SAMPLES = 10
PASS = 'distributed light computation\nstarted pass 1: 0 units done/%d\n' % SAMPLES
SCENARIOS = {
  # the log after the start of the pass; what each texel ends up with: the client index of its sample, -1 for a
  # sample of no client, -2 for no sample; the masks written with the index each holds
  'masks': ('''client alpha computed [0,1]
client beta computed [4,7]
client alpha computed [2,3]
finished pass 1
client gamma computed [8,9]
''', [0, 0, 0, 0, 1, 1, -2, 1, -2, 1, -1, -1], {'alpha': 0, 'beta': 1, '$none$': -1, '$white$': -2}),
  'no-clients': ('finished pass 1\n', [-1, -1, -1, -1, -1, -1, -2, -1, -2, -1, -1, -1], {'$none$': -1, '$white$': -2}),
}
# LM records: (first texel, second texel or run length, run): samples 0-5 light texels 0-5, 6 and 7 texels 7 and 9,
# 8 and 9 texels 10 and 11; texels 6 and 8 have no sample
LM_RECORDS = [(0, 6, True), (7, 9, False), (10, 2, True)]


def tagged_block(tag, payload):
  # IGenSave::beginBlock/endBlock: the length of what follows (the tag and the data), then the tag (_MAKE4C bytes)
  return struct.pack('<i', 4 + len(payload)) + tag.rjust(4, b'\0') + payload


def bind_data():
  header = struct.pack('<4s7i', b'lbOK', SAMPLES, 0, 0, 0, len(LM_RECORDS), 0, 0)
  spt = b'\0' * (32 * SAMPLES)  # LtSamplePoint records, which the tool skips
  lm = b''
  for first, second, run in LM_RECORDS:
    lm += struct.pack('<iI', first, (1 << 31 | second) if run else second)
  return header + tagged_block(b'SPT', spt) + tagged_block(b'LM', lm)


def read_tga(path):
  with open(path, 'rb') as f:
    data = f.read()
  idlen, cmtype, kind = data[0], data[1], data[2]
  w, h, bits, desc = struct.unpack('<HHBB', data[12:18])
  if (idlen, cmtype, kind, w, h, bits) != (0, 0, 2, W, H, 32):
    sys.exit('%s: not a %dx%d 32-bit true color TGA (id %d, color map %d, type %d, %dx%d, %d bits)' %
             (path, W, H, idlen, cmtype, kind, w, h, bits))
  pixels = data[18:18 + w * h * 4]
  rows = [pixels[r * w * 4:(r + 1) * w * 4] for r in range(h)]
  if not desc & 0x20:  # the origin at the bottom: the file's first row is the image's last
    rows.reverse()
  return [tuple(row[x * 4:x * 4 + 4]) for row in rows for x in range(w)]  # BGRA


def main():
  if len(sys.argv) != 3 or sys.argv[1] not in SCENARIOS:
    sys.exit('usage: det_client_mask.py %s <detClientMask>' % '|'.join(SCENARIOS))
  log, texels, masks = SCENARIOS[sys.argv[1]]
  tool = os.path.abspath(sys.argv[2])
  out = os.environ.get('DAGOR_TEST_OUT')
  if not out:
    sys.exit('DAGOR_TEST_OUT is not set (the tests run through CTest)')
  shutil.rmtree(out, ignore_errors=True)
  os.makedirs(out)
  with open(os.path.join(out, 'compute.log'), 'w') as f:
    f.write(PASS + log)
  with open(os.path.join(out, 'lt.bind.bin'), 'wb') as f:
    f.write(bind_data())
  result = subprocess.run([tool, 'compute.log', 'lt.bind.bin', str(W), str(H)], cwd=out)
  if result.returncode != 0:
    sys.exit('detClientMask exited with %d' % result.returncode)

  written = sorted(f for f in os.listdir(out) if f.endswith('-mask.tga'))
  expected = sorted('%s-mask.tga' % name for name in masks)
  if written != expected:
    sys.exit('detClientMask wrote %s, expected %s' % (written, expected))
  scale = 240 // max(len([i for i in masks.values() if i >= 0]), 1)
  errors = []
  for name, index in sorted(masks.items()):
    pixels = read_tga(os.path.join(out, '%s-mask.tga' % name))
    for i, (b, g, r, a) in enumerate(pixels):
      want_a = 255 if texels[i] == index else 0
      want_grey = texels[i] * scale if texels[i] >= 0 else 255 + texels[i]
      if a != want_a:
        errors.append('%s-mask.tga texel %d: alpha %d, expected %d' % (name, i, a, want_a))
      if not b == g == r:
        errors.append('%s-mask.tga texel %d: (%d, %d, %d) is not grey' % (name, i, r, g, b))
      elif r != want_grey:
        errors.append('%s-mask.tga texel %d: grey %d, expected %d' % (name, i, r, want_grey))
  if errors:
    sys.exit('\n'.join(errors))
  print('%d masks of %dx%d checked' % (len(masks), W, H))


if __name__ == '__main__':
  main()
