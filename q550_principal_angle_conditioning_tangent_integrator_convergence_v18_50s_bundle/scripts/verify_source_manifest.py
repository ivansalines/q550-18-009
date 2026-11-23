#!/usr/bin/env python3
"""Verify immutable source manifest without rejecting regenerated results/logs."""
import hashlib,json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
m=json.loads((root/'SOURCE_MANIFEST.json').read_text())
if m['root']!=root.name:raise RuntimeError('Unexpected source manifest root')
for rel,h in m['files'].items():
 p=root/rel
 if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=h:raise RuntimeError('Source drift: '+rel)
print('v18.50s SOURCE IDENTITY VERIFIED',len(m['files']))
