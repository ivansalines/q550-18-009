#!/usr/bin/env python3
"""Pack only manifest-listed source/results; never package a runtime tree."""
from pathlib import Path
import hashlib,json,zipfile
root=Path(__file__).resolve().parents[1]
a=json.loads((root/'SOURCE_MANIFEST.json').read_text());b=json.loads((root/'SHA256SUMS_OUTPUT.json').read_text())
if a['root']!=root.name or b['root']!=root.name:raise RuntimeError('Manifest root mismatch')
entries={**a['files'],**b['file_sha256']}
for rel,digest in entries.items():
    p=root/rel
    if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=digest:
        raise RuntimeError('Source/output drift: '+rel)
members=sorted(set(entries)|{'SOURCE_MANIFEST.json','SHA256SUMS_OUTPUT.json'})
dest=root.parent/(root.name+'_server_sendback.zip')
with zipfile.ZipFile(dest,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6,allowZip64=True) as z:
    for rel in members:z.write(root/rel,root.name+'/'+rel)
with zipfile.ZipFile(dest) as z:
    if z.testzip() is not None:raise RuntimeError('Sendback ZIP CRC failure')
print('SENDBACK PACKED',dest,'members',len(members),'bytes',dest.stat().st_size)
