#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
r=Path(__file__).resolve().parents[1];m=json.loads((r/'SOURCE_MANIFEST.json').read_text())
assert m['root']==r.name and m['version']=='v18.51m'
for name,digest in m['files'].items():
    assert (r/name).is_file(),name
    assert hashlib.sha256((r/name).read_bytes()).hexdigest()==digest,name
print('SOURCE IDENTITY VERIFIED',len(m['files']),flush=True)
