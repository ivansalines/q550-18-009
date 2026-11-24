#!/usr/bin/env python3
"""Persisted-output audit, independent of in-memory reporting."""
from pathlib import Path
import csv,json,numpy as np
p=Path(__file__).resolve().parents[1]/'results'
d=json.loads((p/'report.json').read_text())
assert d['version']=='v18.51l' and all(d['checks'].values())
def read(n):
 with (p/n).open(newline='',encoding='utf-8') as f:return list(csv.DictReader(f))
inst=read('metric_path_instantaneous_directionality.csv')
finite=read('metric_path_finite_lag_directionality.csv')
poly=read('metric_path_polynomial_sign_bounds.csv')
summary=read('metric_path_survival_summary.csv')
assert len(inst)==10140 and len(finite)==29510 and len(poly)==610 and len(summary)==8
for rows in (inst,finite):
 assert all(float(x['ratio_5to4_over_4to5'])>0 for x in rows)
 for x in rows:
  n1=float(x['norm_5to4']);n2=float(x['norm_4to5'])
  assert abs(n1/n2-float(x['ratio_5to4_over_4to5']))<1e-10
  assert abs((n1*n1-n2*n2)/(n1*n1+n2*n2)-float(x['relative_squared_margin']))<1e-10
assert sum(x['positive_bernstein']=='True' for x in poly)==d['counts']['polynomial_positive_bernstein']
assert all((float(x['bernstein_lower_bound'])>float(x['bernstein_error_guard'])) == (x['positive_bernstein']=='True') for x in poly)
assert sum(int(x['n_observations']) for x in summary)==len(inst)+len(finite)
assert len({float(x['tau_ref']) for x in inst})==65
assert sum(int(x['direction_5to4_survival_on_nodes']) for x in summary)==sum(float(x['ratio_5to4_over_4to5'])>1 for x in inst+finite)
assert abs(min(float(x['ratio_5to4_over_4to5']) for x in finite)-d['quality']['min_finite_ratio'])<1e-11
assert bool(all(float(x['ratio_5to4_over_4to5'])>1 for x in finite))==d['observations']['all_finite_node_5to4_dominant']
print('v18.51l persisted results PASS',len(inst),'instantaneous',len(finite),'finite',len(poly),'polynomial positivity diagnostics')
