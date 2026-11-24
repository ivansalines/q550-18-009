#!/usr/bin/env python3
"""Regression tests on replay outputs, including noncertification safeguards."""
import csv,json
from pathlib import Path
r=Path(__file__).resolve().parents[1];out=r/'results'
d=json.loads((out/'report.json').read_text());assert d['version']=='v18.51o'
assert len(d['source_lineage'])==10 and all(d['checks'].values()) and len(d['checks'])==19
assert d['new_physical_ivps']==0 and d['inherited_physical_ivps']==2
assert 'ONLY' in d['classification']
rows=list(csv.DictReader((out/'clock_kinematic_force_germ_ledger.csv').open()))
assert len(rows)==474 and len(d['summary'])==6
assert {r['seed_family'] for r in rows}=={'original','autonomous'}
assert {float(r['tau_ref']) for r in rows}=={.5,1.,2.}
assert max(float(x['finite_tangent_qprime_residual']) for x in rows)<1e-6
assert max(float(x['finite_tangent_qsecond_residual']) for x in rows)<1e-4
assert min(float(x['q_q_column5_norm']) for x in rows)>.01
assert min(float(x['effective_force_position_nonsymmetric_fraction']) for x in rows)>.1
assert min(float(x['effective_force_velocity_jacobian_norm']) for x in rows)>.1
assert 'no nonlinear baseline force' in d['formal_identification']['force_warning']
print('v18.51o source / second-order tangent / refusal-of-unique-force tests PASS')
