#!/usr/bin/env python3
"""Hash regenerated Q550 v18.51i results."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
files=sorted(p for p in (ROOT/'results').rglob('*') if p.is_file() and p.suffix!='.pyc')
assert len(files)>=7
m={'root':ROOT.name,'version':'v18.51i','file_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}}
(ROOT/'SHA256SUMS_OUTPUT.json').write_text(json.dumps(m,indent=2)+'\n')
print('OUTPUT MANIFEST WRITTEN',len(files))
