#!/usr/bin/env python3
"""Check that data, scientific classification, and manifest expectations match."""
import csv,json
from pathlib import Path
r=Path(__file__).resolve().parents[1]
report=json.loads((r/'results/report.json').read_text())
assert report['version']=='v18.51p'
assert all(report['checks'].values()),[k for k,v in report['checks'].items() if not v]
rows=list(csv.DictReader((r/'results/physical_clock_absolute_force_ledger.csv').open()))
checks=list(csv.DictReader((r/'results/nonlinear_force_jacobian_replay.csv').open()))
assert len(rows)==report['sections']==158
assert len(checks)==report['nonlinear_force_jacobian_sections']==6
assert {a['seed_family'] for a in rows}=={'original','autonomous'}
for seed in ('original','autonomous'):
 rr=[a for a in rows if a['seed_family']==seed]
 assert len(rr)==79 and float(rr[0]['xi'])==0
 assert abs(float(rr[-1]['xi'])-.05)<1e-12
 assert float(rr[-1]['tau_elapsed_from_turn'])>0
assert report['classification'].startswith('AUTHENTIC_NONLINEAR')
assert 'no potential' in report['scientific_boundary']['absolute_generalized_force']
print('v18.51p OUTPUT AND INTERPRETATION TESTS PASS')
