#!/usr/bin/env python3
"""Pack only manifest-listed sources and results; never pack runtime caches."""
from pathlib import Path
import hashlib,json,zipfile
root=Path(__file__).resolve().parents[1]
sm=json.loads((root/'SOURCE_MANIFEST.json').read_text());om=json.loads((root/'SHA256SUMS_OUTPUT.json').read_text())
if sm['root']!=root.name or om['root']!=root.name:raise RuntimeError('Manifest root mismatch')
for name,digest in {**sm['files'],**om['file_sha256']}.items():
 p=root/name
 if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=digest:
  raise RuntimeError('Drift in manifest member: '+name)
members=sorted(set([*sm['files'],*om['file_sha256'],'SOURCE_MANIFEST.json','SHA256SUMS_OUTPUT.json']))
dest=root.parent/(root.name+'_server_sendback.zip')
with zipfile.ZipFile(dest,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6,allowZip64=True) as z:
 for rel in members:z.write(root/rel,root.name+'/'+rel)
with zipfile.ZipFile(dest) as z:
 if z.testzip() is not None:raise RuntimeError('Packed ZIP CRC failure')
print('SENDBACK PACKED',str(dest),'members',len(members),'bytes',dest.stat().st_size)
