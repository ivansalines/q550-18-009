#!/usr/bin/env python3
from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parents[1]
s=json.loads((root/'SOURCE_MANIFEST.json').read_text())
assert (s['root'],s['version'])==(root.name,'v18.51d')
for rel,dig in s['files'].items():
 if any(x in rel for x in ('__pycache__','.pyc','runtime/')):raise RuntimeError('Transient source in manifest')
 p=root/rel
 if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=dig:raise RuntimeError('Source drift: '+rel)
print('SOURCE IDENTITY VERIFIED',len(s['files']))
