#!/usr/bin/env python3
"""Independent persisted-output audit: count, sign, bridge and convergence."""
import csv,json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'results'
rep=json.loads((OUT/'report.json').read_text())
assert rep['version']=='v18.51m' and all(rep['checks'].values())
def read(name):
    with (OUT/name).open(newline='',encoding='utf-8') as f:return list(csv.DictReader(f))
i=read('independent_observability_instantaneous_channels.csv')
f=read('independent_observability_finite_lag_channels.csv')
r=read('kinetic_to_observability_metric_bridge_roots.csv')
s=read('independent_observability_directionality_summary.csv')
c=read('physical_observability_quadrature_refinement.csv')
assert len(i)==1092 and len(f)==3178 and len(r)==610 and len(s)==28 and len(c)==6
for row in i+f:
    x=float(row['ratio_5to4_over_4to5']);b=float(row['baseline_kinetic_ratio'])
    assert 0<x<1<b
    n54=float(row['norm_5to4']);n45=float(row['norm_4to5'])
    assert abs(x-n54/n45)<1e-12
    assert abs(float(row['signed_squared_margin'])-(n54*n54-n45*n45)/(n54*n54+n45*n45))<1e-12
for row in r:
    assert float(row['positive_at_kinetic_identity'])>0
    assert float(row['negative_at_observability'])<0
    assert 0<float(row['critical_lambda'])<1
    assert int(row['real_roots_0_to_1'])==1
    poly=json.loads(row['polynomial_coefficients'])
    assert abs(np.polynomial.polynomial.polyval(float(row['critical_lambda']),poly))<1e-8
for row in s:
    assert int(row['observation_forward_count'])==0
    assert int(row['observation_reverse_count'])==int(row['count'])
    assert int(row['baseline_forward_count'])==int(row['count'])
for row in c:assert int(row['forward_count'])==0
q=rep['quality']
assert q['max_polynomial_direct_error']<1e-10
assert q['max_O2_gauge_error']<1e-11
assert q['max_passive_chart_error']<1e-11
assert q['max_parent_baseline_ratio_error']<2e-6
assert q['max_passive_tau_observation_metric_error']<1e-11
print('v18.51m persisted scientific outputs and adversarial directionality challenge PASS',flush=True)
