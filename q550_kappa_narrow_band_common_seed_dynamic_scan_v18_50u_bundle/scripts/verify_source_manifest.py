#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
m=json.loads((root/'SOURCE_MANIFEST.json').read_text())
if m['root']!=root.name:raise RuntimeError('Root mismatch')
for rel,expected in m['files'].items():
    p=root/rel
    if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=expected:raise RuntimeError('Source drift: '+rel)
print('v18.50u source manifest PASS',len(m['files']))
