#!/usr/bin/env python3
"""Verify immutable source manifest; generated files are not sources."""
from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parents[1]
m=json.loads((root/'SOURCE_MANIFEST.json').read_text())
if m['root']!=root.name or m['version']!='v18.50z':raise RuntimeError('Wrong manifest root')
for rel,expected in m['files'].items():
    p=root/rel
    if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=expected:
        raise RuntimeError('Source drift: '+rel)
print('SOURCE IDENTITY VERIFIED',len(m['files']))
