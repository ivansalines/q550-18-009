#!/usr/bin/env python3
"""Source-identical bundle with separately regenerated hashes. Never pack runtime."""
from pathlib import Path
import hashlib,json,zipfile
root=Path(__file__).resolve().parents[1]
s=json.loads((root/'SOURCE_MANIFEST.json').read_text())
o=json.loads((root/'SHA256SUMS_OUTPUT.json').read_text())
for m,k in ((s,'files'),(o,'file_sha256')):
 if m['root']!=root.name:raise RuntimeError('Manifest root mismatch')
 for rel,h in m[k].items():
  if hashlib.sha256((root/rel).read_bytes()).hexdigest()!=h:raise RuntimeError('Digest drift: '+rel)
items=sorted(set(s['files'])|set(o['file_sha256'])|{'SOURCE_MANIFEST.json','SHA256SUMS_OUTPUT.json'})
dest=root.parent/(root.name+'_server_sendback.zip')
with zipfile.ZipFile(dest,'w',allowZip64=True) as z:
 for rel in items:
  z.write(root/rel,root.name+'/'+rel,compress_type=zipfile.ZIP_STORED if rel.endswith('.zip') else zipfile.ZIP_DEFLATED)
with zipfile.ZipFile(dest) as z:
 if z.testzip() or len(z.namelist())!=len(items):raise RuntimeError('Incomplete sendback')
print('v18.50x SERVER SENDBACK',dest,'bytes',dest.stat().st_size,'members',len(items))
