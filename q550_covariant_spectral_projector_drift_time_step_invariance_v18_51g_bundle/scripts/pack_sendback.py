#!/usr/bin/env python3
"""Produce a server sendback containing all source scripts, input genealogy and results."""
import zipfile,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
source=json.loads((ROOT/'SOURCE_MANIFEST.json').read_text())
output=json.loads((ROOT/'SHA256SUMS_OUTPUT.json').read_text())
for name,hash0 in {**source['files'],**output['file_sha256']}.items():
    assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==hash0,name
assert all(json.loads((ROOT/'results/report.json').read_text())['checks'].values())
target=ROOT.parent/(ROOT.name+'_server_sendback.zip')
with zipfile.ZipFile(target,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6,allowZip64=True) as zz:
    for p in sorted(ROOT.rglob('*')):
        if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc':
            zz.write(p,arcname=ROOT.name+'/'+str(p.relative_to(ROOT)))
with zipfile.ZipFile(target) as z:assert z.testzip() is None
print('SENDBACK PACKED',target,'bytes',target.stat().st_size,'members',len(z.namelist()))
