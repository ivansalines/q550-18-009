#!/usr/bin/env python3
"""Strictly verify immutable v18.50y source members and their exact bytes."""
from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parents[1]
d=json.loads((root/'SOURCE_MANIFEST.json').read_text())
assert d['root']==root.name
for name,digest in d['files'].items():
 p=root/name
 if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=digest:
  raise RuntimeError('Source drift: '+name)
print('SOURCE IDENTITY VERIFIED',len(d['files']))
