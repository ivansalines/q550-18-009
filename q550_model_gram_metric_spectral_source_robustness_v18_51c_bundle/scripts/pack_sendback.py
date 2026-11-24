#!/usr/bin/env python3
"""Pack ONLY whitelisted immutable sources and freshly hashed outputs."""
from pathlib import Path
import hashlib,json,zipfile
root=Path(__file__).resolve().parents[1]
s=json.loads((root/'SOURCE_MANIFEST.json').read_text());o=json.loads((root/'SHA256SUMS_OUTPUT.json').read_text())
if (s['root'],s['version'],o['root'],o['version'])!=(root.name,'v18.51c',root.name,'v18.51c'):
    raise RuntimeError('Manifest identity conflict')
files={**s['files'],**o['file_sha256']}
for rel,dig in files.items():
    if '__pycache__' in rel or rel.endswith('.pyc') or '/runtime/' in rel or rel.startswith('runtime/'):
        raise RuntimeError('Transient file in manifest: '+rel)
    p=root/rel
    if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=dig:
        raise RuntimeError('Source/output drift: '+rel)
names=sorted(set(files)|{'SOURCE_MANIFEST.json','SHA256SUMS_OUTPUT.json'})
dest=root.parent/(root.name+'_server_sendback.zip')
with zipfile.ZipFile(dest,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6,allowZip64=True) as z:
    for name in names:z.write(root/name,root.name+'/'+name)
with zipfile.ZipFile(dest) as z:
    if z.testzip() is not None:raise RuntimeError('Sendback CRC error')
    if set(z.namelist())!={root.name+'/'+n for n in names}:raise RuntimeError('Unexpected sendback members')
print('SENDBACK PACKED',dest,'members',len(names),'bytes',dest.stat().st_size)
