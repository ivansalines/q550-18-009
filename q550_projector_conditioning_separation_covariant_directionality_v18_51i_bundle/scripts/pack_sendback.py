#!/usr/bin/env python3
"""Package the exact full Q550 v18.51i server sendback including source."""
from pathlib import Path
import hashlib,json,zipfile
ROOT=Path(__file__).resolve().parents[1]
s=json.loads((ROOT/'SOURCE_MANIFEST.json').read_text())
o=json.loads((ROOT/'SHA256SUMS_OUTPUT.json').read_text())
assert s['root']==o['root']==ROOT.name and s['version']==o['version']=='v18.51i'
for filename,digest in {**s['files'],**o['file_sha256']}.items():
 assert hashlib.sha256((ROOT/filename).read_bytes()).hexdigest()==digest,filename
assert all(json.loads((ROOT/'results/report.json').read_text())['checks'].values())
out=ROOT.parent/(ROOT.name+'_server_sendback.zip')
with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6,allowZip64=True) as z:
 for p in sorted(ROOT.rglob('*')):
  if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc':
   z.write(p,ROOT.name+'/'+str(p.relative_to(ROOT)))
with zipfile.ZipFile(out) as z:assert z.testzip() is None
print('SENDBACK PACKED',out,'members',len(z.namelist()),'bytes',out.stat().st_size)
