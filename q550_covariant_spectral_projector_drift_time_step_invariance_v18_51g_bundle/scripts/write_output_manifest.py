#!/usr/bin/env python3
"""Write the exactly reproduced results' SHA-256 ledger."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
files=sorted(p for p in (ROOT/'results').rglob('*') if p.is_file() and '__pycache__' not in p.parts)
assert len(files)>=10
m={'version':'v18.51g','root':ROOT.name,'file_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}}
(ROOT/'SHA256SUMS_OUTPUT.json').write_text(json.dumps(m,indent=2)+'\n')
print('OUTPUT MANIFEST WRITTEN',len(files))
