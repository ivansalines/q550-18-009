#!/usr/bin/env python3
from pathlib import Path
import hashlib,json,zipfile
root=Path(__file__).resolve().parents[1]
s=json.loads((root/'SOURCE_MANIFEST.json').read_text());o=json.loads((root/'SHA256SUMS_OUTPUT.json').read_text())
assert (s['root'],s['version'],o['root'],o['version'])==(root.name,'v18.51d',root.name,'v18.51d')
files={**s['files'],**o['file_sha256']}
for rel,hash0 in files.items():
 if '__pycache__' in rel or '.pyc' in rel or rel.startswith('runtime/'):raise RuntimeError('Transient file in manifest')
 f=root/rel
 if not f.is_file() or hashlib.sha256(f.read_bytes()).hexdigest()!=hash0:raise RuntimeError('Source/output drift: '+rel)
names=sorted(set(files)|{'SOURCE_MANIFEST.json','SHA256SUMS_OUTPUT.json'})
dest=root.parent/(root.name+'_server_sendback.zip')
with zipfile.ZipFile(dest,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6,allowZip64=True) as z:
 for rel in names:z.write(root/rel,root.name+'/'+rel)
with zipfile.ZipFile(dest) as z:
 if z.testzip() is not None:raise RuntimeError('CRC error in sendback')
 assert set(z.namelist())=={root.name+'/'+n for n in names}
print('SENDBACK PACKED',dest, 'members',len(names),'bytes',dest.stat().st_size)
