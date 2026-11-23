#!/usr/bin/env python3
"""Immutable-source hash verifier; ignores newly generated output and temporary runtime."""
import hashlib,json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
source=json.loads((root/'SOURCE_MANIFEST.json').read_text())
if source['root']!=root.name:raise RuntimeError('Root mismatch')
for name,h in source['files'].items():
 f=root/name
 if not f.exists() or hashlib.sha256(f.read_bytes()).hexdigest()!=h:raise RuntimeError('Source drift: '+name)
print('SOURCE IDENTITY VERIFIED',len(source['files']))
