#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
items=sorted(p for p in (root/'results').iterdir() if p.is_file() and p.suffix in ('.csv','.json','.png'))
if not (root/'results/report.json').exists():raise RuntimeError('No scientific report generated')
m={'root':root.name,'version':'v18.50v','file_sha256':{
    str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in items}}
(root/'SHA256SUMS_OUTPUT.json').write_text(json.dumps(m,indent=2)+'\n')
print('v18.50v OUTPUT MANIFEST',len(items))
