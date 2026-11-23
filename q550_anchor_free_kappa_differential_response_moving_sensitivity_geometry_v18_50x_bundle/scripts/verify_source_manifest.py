#!/usr/bin/env python3
from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parents[1]
m=json.loads((root/'SOURCE_MANIFEST.json').read_text())
assert m['root']==root.name
for rel,h in m['files'].items():
 if hashlib.sha256((root/rel).read_bytes()).hexdigest()!=h:raise RuntimeError('Source changed: '+rel)
print('v18.50x SOURCE VERIFIED',len(m['files']))
