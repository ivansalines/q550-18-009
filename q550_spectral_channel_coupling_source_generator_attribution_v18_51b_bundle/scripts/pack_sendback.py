#!/usr/bin/env python3
"""Sendback: manifest sources and regenerated scientific results, no runtime/cache."""
from pathlib import Path
import hashlib,json,zipfile
root=Path(__file__).resolve().parents[1]
s=json.loads((root/'SOURCE_MANIFEST.json').read_text());o=json.loads((root/'SHA256SUMS_OUTPUT.json').read_text())
if s['root']!=root.name or o['root']!=root.name:raise RuntimeError('Manifest root mismatch')
files={**s['files'],**o['file_sha256']}
for rel,digest in files.items():
    p=root/rel
    if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=digest:raise RuntimeError('Source/output drift: '+rel)
names=sorted(set(files)|{'SOURCE_MANIFEST.json','SHA256SUMS_OUTPUT.json'})
if any('__pycache__' in name or name.endswith('.pyc') or '/runtime/' in name for name in names):
    raise RuntimeError('Transient files incorrectly packed')
dest=root.parent/(root.name+'_server_sendback.zip')
with zipfile.ZipFile(dest,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6,allowZip64=True) as z:
    for name in names:z.write(root/name,root.name+'/'+name)
with zipfile.ZipFile(dest) as z:
    if z.testzip() is not None:raise RuntimeError('Sendback ZIP CRC mismatch')
print('SENDBACK PACKED',dest,'members',len(names),'bytes',dest.stat().st_size)
