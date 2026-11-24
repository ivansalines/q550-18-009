#!/usr/bin/env python3
"""Check byte identity of all input/source files recorded for this version."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
m=json.loads((ROOT/'SOURCE_MANIFEST.json').read_text(encoding='utf-8'))
assert m['root']==ROOT.name and m['version']=='v18.51h'
for file,h in m['files'].items():
    p=ROOT/file
    assert p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest()==h,file
print('SOURCE IDENTITY VERIFIED',len(m['files']))
