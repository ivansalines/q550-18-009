#!/usr/bin/env python3
"""Verify archived v18.50w measurements, including the negative controls."""
from pathlib import Path
import json,pandas as pd,numpy as np
root=Path(__file__).resolve().parents[1]
r=json.loads((root/'results/report.json').read_text())
d=pd.read_csv(root/'results/equidistance_gate_time_ledger.csv')
assert len(d)==4*79
for m in ('projector_gap','observer_gap','rhs_gap'):
 c=d[d.measure==m].sort_values('xi')
 assert c.crossing_detected.eq(1).all() and (c.root_normalized.between(0,1)).all()
assert (d[d.measure=='state_gap'].crossing_detected==0).sum()==1
assert r['measurements']['projector_gap']['decreasing_steps']==78
assert r['measurements']['observer_gap']['increasing_steps']==78
assert r['measurements']['rhs_gap']['increasing_steps']==78
assert abs(r['measurements']['projector_gap']['start_root']-.4999612)<2e-6
assert abs(r['measurements']['projector_gap']['end_root']-.49995837)<2e-6
assert len(pd.read_csv(root/'results/signed_projector_distance_profiles.csv'))==22*79
assert len(pd.read_csv(root/'results/u_v_short_window_comparison.csv'))==4
print('v18.50w measured data and provenance negative controls PASS')
