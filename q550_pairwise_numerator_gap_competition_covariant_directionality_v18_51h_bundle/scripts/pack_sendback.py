#!/usr/bin/env python3
"""Verify hashes and package entire Q550 v18.51h executable genealogy."""
from pathlib import Path
import hashlib,json,zipfile
ROOT=Path(__file__).resolve().parents[1]
source=json.loads((ROOT/'SOURCE_MANIFEST.json').read_text())
output=json.loads((ROOT/'SHA256SUMS_OUTPUT.json').read_text())
assert source['root']==output['root']==ROOT.name
for k,h in {**source['files'],**output['file_sha256']}.items():
    assert hashlib.sha256((ROOT/k).read_bytes()).hexdigest()==h,k
assert all(json.loads((ROOT/'results/report.json').read_text())['checks'].values())
zipname=ROOT.parent/(ROOT.name+'_server_sendback.zip')
with zipfile.ZipFile(zipname,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6,allowZip64=True) as z:
    for p in sorted(ROOT.rglob('*')):
        if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc':
            z.write(p,ROOT.name+'/'+str(p.relative_to(ROOT)))
with zipfile.ZipFile(zipname) as z:
    assert z.testzip() is None
    n=len(z.namelist())
print('SENDBACK PACKED',zipname,'members',n,'bytes',zipname.stat().st_size)
