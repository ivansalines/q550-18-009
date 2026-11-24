#!/usr/bin/env python3
"""Verify exact immutable source content; ignore unrelated runtime files."""
from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parents[1]
s=json.loads((root/'SOURCE_MANIFEST.json').read_text())
if (s['root'],s['version'])!=(root.name,'v18.51c'):raise RuntimeError('Wrong root/version')
for rel,dig in s['files'].items():
    if '__pycache__' in rel or rel.endswith('.pyc') or rel.startswith('runtime/'):
        raise RuntimeError('Transient code mistakenly registered')
    p=root/rel
    if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=dig:
        raise RuntimeError('Source drift: '+rel)
print('SOURCE IDENTITY VERIFIED',len(s['files']))
