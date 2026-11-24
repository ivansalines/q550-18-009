#!/usr/bin/env python3
"""Strict source genealogy checksum verification."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
m=json.loads((ROOT/'SOURCE_MANIFEST.json').read_text())
assert m['root']==ROOT.name and m['version']=='v18.51i'
for filename,digest in m['files'].items():
 assert hashlib.sha256((ROOT/filename).read_bytes()).hexdigest()==digest,filename
print('SOURCE IDENTITY VERIFIED',len(m['files']))
