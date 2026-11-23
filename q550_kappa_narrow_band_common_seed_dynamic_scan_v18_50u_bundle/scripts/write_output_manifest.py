#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
files=sorted(p for p in (root/'results').iterdir() if p.is_file() and p.suffix in ('.csv','.json','.png'))
m={'root':root.name,'version':'v18.50u','file_sha256':{str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}}
(root/'SHA256SUMS_OUTPUT.json').write_text(json.dumps(m,indent=2)+'\n')
print('v18.50u output manifest',len(files))
