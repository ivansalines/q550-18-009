#!/usr/bin/env python3
from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parents[1]
paths=sorted(p for p in (root/'results').iterdir() if p.is_file() and p.suffix in ('.csv','.json','.png'))
if len(paths)!=7:raise RuntimeError(f'Expected 7 scientific output files, found {len(paths)}')
m={'root':root.name,'version':'v18.51d','file_sha256':{str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}}
(root/'SHA256SUMS_OUTPUT.json').write_text(json.dumps(m,indent=2)+'\n')
print('OUTPUT MANIFEST WRITTEN',len(paths))
