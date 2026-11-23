#!/usr/bin/env python3
"""Separately hash regenerated results, not inherited sources or temporary runtime."""
import hashlib,json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
expected={'results/report.json','results/principal_angle_integrator_convergence.csv',
          'results/parent_q_angle_comparison.csv','results/angle_conditioning_original.png',
          'results/angle_conditioning_autonomous.png','results/tangent_integrator_effort.png'}
found={p.relative_to(root).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
       for p in sorted((root/'results').glob('*')) if p.is_file()}
if not expected.issubset(found):raise RuntimeError('Missing required results: '+str(expected-set(found)))
(root/'SHA256SUMS_OUTPUT.json').write_text(json.dumps({'root':root.name,'file_sha256':found},indent=2)+'\n')
print('v18.50s OUTPUT MANIFEST WRITTEN',len(found))
