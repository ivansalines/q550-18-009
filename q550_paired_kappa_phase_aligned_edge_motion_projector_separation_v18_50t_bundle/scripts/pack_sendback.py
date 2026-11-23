#!/usr/bin/env python3
"""Make a compact authenticated sendback without extracted genealogical trees."""
import hashlib,json,zipfile
from pathlib import Path
root=Path(__file__).resolve().parents[1]
def check():
 src=json.loads((root/'SOURCE_MANIFEST.json').read_text());out=json.loads((root/'SHA256SUMS_OUTPUT.json').read_text())
 if src['root']!=root.name or out['root']!=root.name:raise RuntimeError('Manifest root mismatch')
 for m,key in ((src,'files'),(out,'file_sha256')):
  for n,dig in m[key].items():
   p=root/n
   if not p.exists() or hashlib.sha256(p.read_bytes()).hexdigest()!=dig:raise RuntimeError('Hash mismatch: '+n)
 return src,out
if __name__=='__main__':
 src,out=check();dest=root.parent/(root.name+'_server_sendback.zip')
 files=sorted(set(src['files'])|set(out['file_sha256'])|{'SOURCE_MANIFEST.json','SHA256SUMS_OUTPUT.json'})
 with zipfile.ZipFile(dest,'w',allowZip64=True) as z:
  for rel in files:
   p=root/rel
   compression=zipfile.ZIP_STORED if p.suffix=='.zip' else zipfile.ZIP_DEFLATED
   z.write(p,root.name+'/'+rel,compress_type=compression)
 with zipfile.ZipFile(dest) as z:
  assert z.testzip() is None
  assert len(z.namelist())==len(files)
 print('v18.50t SEND-BACK PACKAGED',dest,'members',len(files),'bytes',dest.stat().st_size)
