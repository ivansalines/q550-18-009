#!/usr/bin/env python3
"""Check numerical outputs without requiring byte-identical PNG files."""
from pathlib import Path
import pandas as pd
import numpy as np
ROOT=Path(__file__).resolve().parents[1];out=ROOT/'results'
a=pd.read_csv(out/'model_vs_canonical_transport_ledger.csv')
assert len(a)==158
assert set(a.seed_family)=={'original','autonomous'}
for seed in ('original','autonomous'):
    t=a[a.seed_family==seed].sort_values('xi')
    assert len(t)==79
    assert np.all(np.diff(t.xi)>0)
    assert abs(t.angle_canonical_deg.iloc[-1]-8.517)<.2
    assert abs(t.angle_raw_deg.iloc[-1]-9.64)<.2
    assert (t.model_frame_orthogonality<1e-7).all()
    assert (t.norm_connection_gap>0).all()
    assert (t.phi_condition>=1-1e-10).all()
    assert np.isfinite(t.select_dtypes('number')).all().all()
print('v18.50z result semantics PASS')
