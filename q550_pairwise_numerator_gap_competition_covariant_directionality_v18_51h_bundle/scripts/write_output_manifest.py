#!/usr/bin/env python3
"""Write SHA-256 manifest for the regenerated v18.51h results."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
files=sorted(p for p in (ROOT/'results').rglob('*') if p.is_file() and p.suffix!='.pyc')
assert len(files)>=7
out={'version':'v18.51h','root':ROOT.name,
     'file_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}}
(ROOT/'SHA256SUMS_OUTPUT.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
print('OUTPUT MANIFEST WRITTEN',len(files))
