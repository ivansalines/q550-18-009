#!/usr/bin/env python3
"""Scientific regression tests for archived v18.51n results."""
import csv,json
from pathlib import Path
p=Path(__file__).resolve().parents[1];d=p/'results'
r=json.loads((d/'report.json').read_text())
assert r['version']=='v18.51n' and len(r['checks'])==16 and all(r['checks'].values())
assert len(r['ancestor_verification'])==9
assert r['observations']['n_profiles']==9
assert r['observations']['kinetic_mass_hessian']['unique_10d_phase_state_metric_from_T_alone'] is False
s=list(csv.DictReader((d/'window_directionality_summary.csv').open()))
for mode in ('position_past_h0.025','position_future_h0.025','position_bilateral_h0.025'):
 rows=[x for x in s if x['metric']==mode and x['observable']=='instant' and float(x['epsilon'])==1e-5]
 assert len(rows)==2 and sum(int(x['n_4to5']) for x in rows)==156
 assert all(int(x['n_5to4'])==0 for x in rows)
for mode in ('position_past_h0.025','position_future_h0.025','position_bilateral_h0.025'):
 rows=[x for x in s if x['metric']==mode and x['observable']=='finite_lag' and float(x['epsilon'])==1e-5]
 assert len(rows)==2 and sum(int(x['n_4to5']) for x in rows)==454
assert all(float(x['ratio_max'])<1 for x in s if x['ratio_max'])
assert any(int(x['n_well_resolved']) < int(x['n_measured']) for x in s)
print('v18.51n measured output / finite-lag / noncertification tests PASS')
