#!/usr/bin/env python3
"""Create a separate reproducible manifest for regenerated output artifacts."""
import hashlib,json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
files=sorted(p for p in (root/'results').iterdir() if p.is_file())
manifest={'root':root.name,'version':'v18.51a','file_sha256':{str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}}
(root/'SHA256SUMS_OUTPUT.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('OUTPUT MANIFEST WRITTEN',len(files))
