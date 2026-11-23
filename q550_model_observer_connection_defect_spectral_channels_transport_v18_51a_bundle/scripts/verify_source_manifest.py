#!/usr/bin/env python3
"""Check immutable source/input SHA-256 entries only."""
import hashlib,json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
m=json.loads((root/'SOURCE_MANIFEST.json').read_text())
if m['root']!=root.name or m['version']!='v18.51a':raise RuntimeError('Wrong source root/version')
for rel,expected in m['files'].items():
    p=root/rel
    if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=expected:
        raise RuntimeError('Source drift: '+rel)
print('SOURCE IDENTITY VERIFIED',len(m['files']))
