#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
m=json.loads((root/'SOURCE_MANIFEST.json').read_text())
if (m['root'],m['version'])!=(root.name,'v18.51f'):raise RuntimeError('Unmatched source identity')
for name,hexdigest in m['files'].items():
 p=root/name
 if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=hexdigest:
  raise RuntimeError('Source SHA256 mismatch '+name)
print('SOURCE IDENTITY VERIFIED',len(m['files']))
