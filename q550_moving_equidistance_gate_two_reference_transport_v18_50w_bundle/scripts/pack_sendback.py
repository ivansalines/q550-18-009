#!/usr/bin/env python3
"""Immutable source checks + regenerated output checksum, never pack runtime."""
import hashlib,json,zipfile
from pathlib import Path
root=Path(__file__).resolve().parents[1]
s=json.loads((root/'SOURCE_MANIFEST.json').read_text());o=json.loads((root/'SHA256SUMS_OUTPUT.json').read_text())
for manifest,key in ((s,'files'),(o,'file_sha256')):
 if manifest['root']!=root.name:raise RuntimeError('Manifest root mismatch')
 for rel,h in manifest[key].items():
  if hashlib.sha256((root/rel).read_bytes()).hexdigest()!=h:raise RuntimeError('Digest drift '+rel)
items=sorted(set(s['files'])|set(o['file_sha256'])|{'SOURCE_MANIFEST.json','SHA256SUMS_OUTPUT.json'})
dest=root.parent/(root.name+'_server_sendback.zip')
with zipfile.ZipFile(dest,'w',allowZip64=True) as z:
 for rel in items:
  f=root/rel
  z.write(f,root.name+'/'+rel,compress_type=zipfile.ZIP_STORED if f.suffix=='.zip' else zipfile.ZIP_DEFLATED)
with zipfile.ZipFile(dest) as z:
 if z.testzip() is not None or len(z.namelist())!=len(items):raise RuntimeError('Sendback invalid')
print('v18.50w SERVER SENDBACK',dest,'members',len(items),'bytes',dest.stat().st_size)
