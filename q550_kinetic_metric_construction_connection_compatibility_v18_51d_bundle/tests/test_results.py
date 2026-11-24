#!/usr/bin/env python3
"""Output checks for two true Q550 replays and three kinetic scales."""
from pathlib import Path
import csv,json,numpy as np
root=Path(__file__).resolve().parents[1]
r=json.loads((root/'results/report.json').read_text())
assert r['version']=='v18.51d'
assert len(r['comparisons'])==6
assert r['observations']==474
assert all(r['checks'].values()),r['checks']
with (root/'results/kinetic_metric_spectral_source_ledger.csv').open() as f:
 rows=list(csv.DictReader(f))
assert len(rows)==474
for row in rows:
 for v in row.values():
  try: assert np.isfinite(float(v))
  except ValueError:pass
 assert abs(float(row['signed_canonical'])+float(row['signed_model_total'])+float(row['signed_kinetic_frame'])-1)<1e-8
assert sorted(set(float(row['tau_ref']) for row in rows))==[.5,1.,2.]
assert set(row['seed_family'] for row in rows)=={'original','autonomous'}
print('v18.51d model replay and kinetic spectral attribution semantics tests PASS')
