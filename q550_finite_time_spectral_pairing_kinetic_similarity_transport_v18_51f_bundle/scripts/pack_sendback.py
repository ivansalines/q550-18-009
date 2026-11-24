#!/usr/bin/env python3
from pathlib import Path
import zipfile,json,hashlib
root=Path(__file__).resolve().parents[1]
out=root.parent/(root.name+'_server_sendback.zip')
sm=json.loads((root/'SOURCE_MANIFEST.json').read_text())
om=json.loads((root/'SHA256SUMS_OUTPUT.json').read_text())
files=set(sm['files'])|set(om['file_sha256'])|{'SOURCE_MANIFEST.json','SHA256SUMS_OUTPUT.json'}
for name in files:
 if not (root/name).is_file():raise RuntimeError('Missing sendback file: '+name)
with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for name in sorted(files):z.write(root/name,arcname=f'{root.name}/{name}')
with zipfile.ZipFile(out) as z:
 assert z.testzip() is None and len(z.namelist())==len(files)
print('SENDBACK PACKED',out,'members',len(files),'bytes',out.stat().st_size)
