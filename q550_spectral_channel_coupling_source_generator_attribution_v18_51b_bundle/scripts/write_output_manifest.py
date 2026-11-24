#!/usr/bin/env python3
"""Fresh manifest for reproducibly regenerated outputs (distinct from sources)."""
import hashlib,json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
files=sorted(p for p in (root/'results').iterdir() if p.is_file())
if len(files)!=7:raise RuntimeError('Expected seven scientific output artifacts, saw '+str(len(files)))
m={'root':root.name,'version':'v18.51b', 'file_sha256':{str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}}
(root/'SHA256SUMS_OUTPUT.json').write_text(json.dumps(m,indent=2)+'\n',encoding='utf8')
print('OUTPUT MANIFEST WRITTEN',len(files))
