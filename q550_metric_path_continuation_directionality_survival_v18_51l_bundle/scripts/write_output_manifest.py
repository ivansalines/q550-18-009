#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
r=Path(__file__).resolve().parents[1]
files={str(p.relative_to(r)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((r/'results').glob('*')) if p.is_file()}
assert 'results/report.json' in files
(r/'SHA256SUMS_OUTPUT.json').write_text(json.dumps(dict(root=r.name,version='v18.51l',file_sha256=files),indent=2)+'\n')
print('OUTPUT MANIFEST WRITTEN',len(files),flush=True)
