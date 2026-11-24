#!/usr/bin/env python3
from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parents[1]
m=json.loads((root/'SOURCE_MANIFEST.json').read_text())
assert (m['root'],m['version'])==(root.name,'v18.51e')
for rel,h in m['files'].items():
 f=root/rel
 if not f.is_file() or hashlib.sha256(f.read_bytes()).hexdigest()!=h:
  raise RuntimeError('Source hash mismatch: '+rel)
print('SOURCE IDENTITY VERIFIED',len(m['files']))
