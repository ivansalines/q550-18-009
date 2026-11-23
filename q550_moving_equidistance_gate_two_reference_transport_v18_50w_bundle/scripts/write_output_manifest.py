#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
items={p.relative_to(root).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((root/'results').iterdir()) if p.is_file()}
(root/'SHA256SUMS_OUTPUT.json').write_text(json.dumps({'root':root.name,'version':'v18.50w','file_sha256':items},indent=2)+'\n')
print('v18.50w OUTPUT MANIFEST WRITTEN',len(items))
