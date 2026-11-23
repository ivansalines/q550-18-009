#!/usr/bin/env python3
"""Package only hash-validated sources and results; never temporary genealogy."""
import hashlib,json,zipfile
from pathlib import Path
root=Path(__file__).resolve().parents[1]
keep={'SOURCE_MANIFEST.json','SHA256SUMS_OUTPUT.json'}
for manifest,key in (('SOURCE_MANIFEST.json','files'),('SHA256SUMS_OUTPUT.json','file_sha256')):
 d=json.loads((root/manifest).read_text())
 if d['root']!=root.name:raise RuntimeError('Manifest root mismatch')
 for name,expected in d[key].items():
  path=root/name
  if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=expected:raise RuntimeError('Digest mismatch: '+name)
  keep.add(name)
out=root.parent/(root.name+'_server_sendback.zip')
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for name in sorted(keep):z.write(root/name,arcname=root.name+'/'+name)
with zipfile.ZipFile(out) as z:
 if z.testzip() is not None:raise RuntimeError('Sendback CRC error')
print('v18.50s SENDBACK CREATED',out,'files',len(keep),'bytes',out.stat().st_size)
