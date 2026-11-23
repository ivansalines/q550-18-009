#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
m=json.loads((root/'SOURCE_MANIFEST.json').read_text())
assert m['root']==root.name and m['version']=='v18.50w'
for f,h in m['files'].items():
    p=root/f
    if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=h:raise RuntimeError('Source drift: '+f)
print('v18.50w SOURCE IDENTITY VERIFIED',len(m['files']))
