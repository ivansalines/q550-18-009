#!/usr/bin/env python3
"""Verify immutable source inputs and Python ancestry by SHA-256."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
m=json.loads((ROOT/'SOURCE_MANIFEST.json').read_text())
assert m['root']==ROOT.name and m['version']=='v18.51g'
for name,h in m['files'].items():
    p=ROOT/name
    assert p.is_file(),name
    assert hashlib.sha256(p.read_bytes()).hexdigest()==h, name
print('SOURCE IDENTITY VERIFIED',len(m['files']))
