#!/usr/bin/env python3
"""Check generated scientific measurements rather than image-byte identity."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
root=Path(__file__).resolve().parents[1]
out=root/'results'
report=json.loads((out/'report.json').read_text())
assert report['version']=='v18.50v'
assert report['design']['parameter_points']==22
assert report['design']['two_fixed_natural_seeds']
assert report['diagnostics']['complete_ivps']==44
assert report['design']['new_10d_driven_ivps']==44
D=pd.read_csv(out/'long_horizon_kappa_response_ledger.csv')
I=pd.read_csv(out/'integration_completion.csv')
R=pd.read_csv(out/'moving_tooth_ridge_watch.csv')
P=pd.read_csv(out/'candidate_peak_events.csv')
assert len(D)==report['design']['rows']
assert len(D)==22*2*report['design']['phase_sections']
assert len(I)==44 and I.success.eq(1).all()
assert (D.observer_strong_s3>0.45).all()
assert (D.observer_weak_s4.abs()<1e-9).all()
for x in ['state_gain','rate_gain','observer_gain','projector_gain',
          'state_delta_from_seed_anchor','projector_gap_from_seed_anchor']:
    assert np.isfinite(D[x]).all() and (D[x]>=0).all()
for seed,kind in [('original','original'),('autonomous','autonomous')]:
    k=report['kappa'][kind]
    rows=D[(D.seed_family==seed)&np.isclose(D.kappa,k,rtol=0,atol=1e-15)]
    assert len(rows)==report['design']['phase_sections']
    assert rows.state_delta_from_seed_anchor.abs().max()<1e-15
    assert rows.projector_gap_from_seed_anchor.abs().max()<1e-15
assert len(R)==2*4*report['design']['phase_sections']
assert len(P)==report['diagnostics']['candidate_rows']
print('v18.50v full data consistency, rank and fixed-seed baseline checks PASS')
