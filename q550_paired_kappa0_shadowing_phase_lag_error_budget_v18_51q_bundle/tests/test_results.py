#!/usr/bin/env python3
"""Independent audit-output reconstruction tests."""
import csv,json,numpy as np
from pathlib import Path
P=Path(__file__).resolve().parents[1]/'results'
r=json.loads((P/'report.json').read_text())
assert r['version']=='v18.51q'
assert len(r['checks'])>=15 and all(r['checks'].values())
assert r['physical_ivps']==12
assert 0<r['kappa_delta']<1e-3
with (P/'paired_kappa_shadow_phase_lag_ledger.csv').open() as f:
 rows=list(csv.DictReader(f))
assert len(rows)==258
for a in rows:
 assert np.isfinite(float(a['physical_Q_gap']))
 assert float(a['physical_Q_gap'])>=0
 assert np.isfinite(float(a['phase_orthogonal_relative']))
 if int(a['index'])==0:assert abs(float(a['physical_Q_gap']))<1e-12
with (P/'solver_replay_error_budget.csv').open() as f:
 runs=list(csv.DictReader(f))
assert len(runs)==6
with np.load(P/'paired_kappa_physical_state_tensors.npz') as z:
 for seed in ('original','autonomous'):
  a=z[f'{seed}_original_Q'];b=z[f'{seed}_autonomous_Q'];m=z[f'{seed}_midpoint_Q']
  assert a.shape==(129,5) and np.all(np.isfinite(a))
  assert np.linalg.norm(a[0]-b[0])<1e-13
  gap=np.linalg.norm(a-b,axis=1)
  for row in rows:
   if row['seed_family']==seed:
    assert abs(gap[int(row['index'])]-float(row['physical_Q_gap']))<1e-10
  assert np.all(np.isfinite(m))
print('Q550 v18.51q independent output replay tests PASS')
