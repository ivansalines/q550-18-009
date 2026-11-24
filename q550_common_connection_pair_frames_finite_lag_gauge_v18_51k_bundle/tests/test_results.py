#!/usr/bin/env python3
"""Independently inspect persisted v18.51k report and CSV output."""
import csv,json
from pathlib import Path
r=Path(__file__).resolve().parents[1]/'results'
d=json.loads((r/'report.json').read_text())
assert d['version']=='v18.51k' and all(d['checks'].values())
with (r/'connection_aligned_finite_lag_ledger.csv').open() as f:rs=list(csv.DictReader(f))
assert len(rs)==1362
assert all(float(x['ratio_5to4_over_4to5'])>1 for x in rs)
assert max(float(x['aligned_gauge_control_error']) for x in rs)<1e-10
assert max(float(x['interference_residual']) for x in rs)<1e-10
with (r/'moving_chart_connection_covariance.csv').open() as f:cs=list(csv.DictReader(f))
assert cs and max(float(x['metric_connection']) for x in cs)<1e-10
assert len(d['observations']['branches'])==6
print('v18.51k persisted results verification PASS',len(rs),'intervals',len(cs),'moving-chart controls')
