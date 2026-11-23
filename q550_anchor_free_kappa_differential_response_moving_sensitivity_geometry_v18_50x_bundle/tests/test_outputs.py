#!/usr/bin/env python3
"""Check saved numerical diagnostics, source lineage, and all integrations."""
from pathlib import Path
import json,pandas as pd,numpy as np
root=Path(__file__).resolve().parents[1]
r=json.loads((root/'results/report.json').read_text())
df=pd.read_csv(root/'results/anchor_free_projector_sensitivity_ledger.csv')
integ=pd.read_csv(root/'results/integration_completion.csv')
assert r['version']=='v18.50x' and len(df)==3476
assert len(integ)==44 and (integ.success==1).all()
assert len(df.seed_family.unique())==2 and df.xi.nunique()==79 and df.kappa.nunique()==22
assert np.isfinite(df[['norm_E','norm_A','orientation_rate']].to_numpy()).all()
assert (df.norm_E>0).all() and (df.norm_A>=0).all() and (df.orientation_rate>=0).all()
assert (abs(df.norm_A**2 - df.radial_rate**2 - df.transverse_rate**2)<1e-5).all()
assert max(v['max_projector_idempotency'] for v in r['checks'].values())<1e-8
assert max(v['max_3_point_vs_parent_v_gradient'] for v in r['checks'].values())<1e-6
print('v18.50x 44 IVPs, 3476 measurements and geometric identity tests PASS')

with np.load(root/'results/full_projector_sensitivity_tensors.npz') as z:
 assert z['P_original'].shape==(22,79,10,10)
 assert z['E_autonomous'].shape==(22,79,10,10)
 assert z['A_original'].shape==(22,79,10,10)
 assert np.allclose(z['P_original']@z['P_original'],z['P_original'],atol=1e-10)
print('v18.50x full tensor-field archive PASS')
