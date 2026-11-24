#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
root=Path(__file__).resolve().parents[1];results=root/'results'
files={}
for f in sorted(results.iterdir()):
 if f.is_file():files[f.relative_to(root).as_posix()]=hashlib.sha256(f.read_bytes()).hexdigest()
(root/'SHA256SUMS_OUTPUT.json').write_text(json.dumps({'root':root.name,'version':'v18.51f','file_sha256':files},indent=2)+'\n')
print('OUTPUT MANIFEST WRITTEN',len(files))
