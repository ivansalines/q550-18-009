#!/usr/bin/env python3
"""Regenerate SHA-256 manifest for current, verified outputs."""
from pathlib import Path
import json,hashlib
root=Path(__file__).resolve().parents[1]
files=sorted(p for p in (root/'results').iterdir() if p.is_file())
manifest={'root':root.name,'version':'v18.50z',
          'file_sha256':{str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}}
(root/'SHA256SUMS_OUTPUT.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('OUTPUT MANIFEST WRITTEN',len(files))
