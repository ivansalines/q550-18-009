#!/usr/bin/env python3
"""Pack only source/output manifests and listed members (never runtime/logs)."""
from pathlib import Path
import json,hashlib,zipfile
root=Path(__file__).resolve().parents[1]
sm=json.loads((root/'SOURCE_MANIFEST.json').read_text());om=json.loads((root/'SHA256SUMS_OUTPUT.json').read_text())
if sm['root']!=root.name or om['root']!=root.name:raise RuntimeError('Wrong root in manifest')
for rel,digest in {**sm['files'],**om['file_sha256']}.items():
    f=root/rel
    if not f.is_file() or hashlib.sha256(f.read_bytes()).hexdigest()!=digest:
        raise RuntimeError('Source or output drift: '+rel)
members=sorted(set([*sm['files'],*om['file_sha256'],'SOURCE_MANIFEST.json','SHA256SUMS_OUTPUT.json']))
dest=root.parent/(root.name+'_server_sendback.zip')
with zipfile.ZipFile(dest,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6,allowZip64=True) as z:
    for rel in members:z.write(root/rel,root.name+'/'+rel)
with zipfile.ZipFile(dest) as z:
    if z.testzip() is not None:raise RuntimeError('Packed ZIP CRC error')
print('SENDBACK PACKED',dest,'members',len(members),'bytes',dest.stat().st_size)
