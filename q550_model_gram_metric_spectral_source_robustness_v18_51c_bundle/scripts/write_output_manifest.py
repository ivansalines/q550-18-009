#!/usr/bin/env python3
"""Hash regenerated results, separately from immutable parent/source inputs."""
from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parents[1]
files=sorted(p for p in (root/'results').iterdir() if p.is_file())
if len(files)!=8:raise RuntimeError('Expected eight result files, got '+str(len(files)))
m={'root':root.name,'version':'v18.51c','file_sha256':{str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}}
(root/'SHA256SUMS_OUTPUT.json').write_text(json.dumps(m,indent=2)+'\n',encoding='utf8')
print('OUTPUT MANIFEST WRITTEN',len(files))
