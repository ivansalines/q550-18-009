#!/usr/bin/env python3
import hashlib,json,zipfile
from pathlib import Path
root=Path(__file__).resolve().parents[1]
a=json.loads((root/'SOURCE_MANIFEST.json').read_text())
b=json.loads((root/'SHA256SUMS_OUTPUT.json').read_text())
if a['root']!=root.name or b['root']!=root.name:raise RuntimeError('Root mismatch')
for m,k in ((a,'files'),(b,'file_sha256')):
    for rel,h in m[k].items():
        if hashlib.sha256((root/rel).read_bytes()).hexdigest()!=h:raise RuntimeError('Digest drift '+rel)
files=sorted(set(a['files'])|set(b['file_sha256'])|{'SOURCE_MANIFEST.json','SHA256SUMS_OUTPUT.json'})
dst=root.parent/(root.name+'_server_sendback.zip')
with zipfile.ZipFile(dst,'w',allowZip64=True) as z:
    for rel in files:
        file=root/rel
        z.write(file,root.name+'/'+rel,compress_type=zipfile.ZIP_STORED if file.suffix=='.zip' else zipfile.ZIP_DEFLATED)
with zipfile.ZipFile(dst) as z:
    if z.testzip() is not None or len(z.namelist())!=len(files):raise RuntimeError('Bad archive')
print('v18.50u SEND-BACK PACKAGED',dst,'members',len(files),'bytes',dst.stat().st_size)
