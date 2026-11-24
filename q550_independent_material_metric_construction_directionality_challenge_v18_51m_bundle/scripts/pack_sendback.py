#!/usr/bin/env python3
from pathlib import Path
import zipfile
r=Path(__file__).resolve().parents[1]
out=r.parent/(r.name+'_server_sendback.zip')
with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=4,allowZip64=True) as z:
    for p in sorted(r.rglob('*')):
        if p.is_file() and '__pycache__' not in p.parts:z.write(p,arcname=r.name+'/'+p.relative_to(r).as_posix())
with zipfile.ZipFile(out) as z:assert z.testzip() is None
print('SENDBACK PACKED',out,'members',len(z.namelist()),'bytes',out.stat().st_size,flush=True)
