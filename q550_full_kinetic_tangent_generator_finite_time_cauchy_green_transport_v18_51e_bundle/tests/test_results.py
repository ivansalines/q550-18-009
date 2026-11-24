#!/usr/bin/env python3
"""Tests real server replay outputs; executed only after run_audit.py succeeds."""
import csv,json
from pathlib import Path
import numpy as np
root=Path(__file__).resolve().parents[1]
r=json.loads((root/'results/report.json').read_text())
assert r['version']=='v18.51e'
assert r['num_rows']==474
assert len(r['finite_time_branches'])==6
assert len(r['one_third_branches'])==6
assert all(r['scientific_checks'].values()),r['scientific_checks']
with (root/'results/full_generator_and_cauchy_green_ledger.csv').open() as f:
 rows=list(csv.DictReader(f))
assert len(rows)==474
assert set(x['seed_family'] for x in rows)=={'original','autonomous'}
assert set(float(x['tau_ref']) for x in rows)=={.5,1.,2.}
for x in rows:
 assert float(x['cg_lambda_min'])>0
 assert abs(float(x['det_M_sign'])-1)<1e-10
 assert abs(float(x['logdet_C'])-2*float(x['logdet_M']))<1e-9
 assert 0<=float(x['symmetric_fraction_of_full_generator'])<=1+1e-10
with np.load(root/'results/material_tangent_cauchy_green_tensors.npz',allow_pickle=False) as z:
 for seed in ('original','autonomous'):
  assert z[f'F_{seed}'].shape==(79,10,10)
  for tau in (.5,1.,2.):
   name=str(tau).replace('.','p')
   M=z[f'M_{seed}_tau_{name}'];C=z[f'C_{seed}_tau_{name}']
   assert M.shape==C.shape==(79,10,10)
   assert np.linalg.norm(M[0]-np.eye(10))<1e-9
   assert np.linalg.norm(C[-1]-M[-1].T@M[-1])<1e-8
print('v18.51e complete Q550 full tangent transport results tests PASS')
