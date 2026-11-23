#!/usr/bin/env python3
"""Audit-specific output integrity and dimensional regression checks."""
from pathlib import Path
import pandas as pd,json,numpy as np
root=Path(__file__).resolve().parents[1]
r=json.loads((root/'results/report.json').read_text())
assert r['version']=='v18.50y'
assert r['parent_authentication']['x_sources']==12
assert r['parent_authentication']['x_outputs']==11
assert r['inputs']['new_physical_10d_ivps']==0
assert r['inputs']['new_geometric_frame_ivps']==6
df=pd.read_csv(root/'results/covariant_kappa_sensitivity_ledger.csv')
assert len(df)==3476 and len(df.seed_family.unique())==2
assert df.groupby('seed_family').size().to_dict()=={'autonomous':1738,'original':1738}
assert np.isfinite(df.select_dtypes(include='number').to_numpy()).all()
for seed in ('original','autonomous'):
 a=r['transported_angles'][f'{seed}_offset_0.5']
 assert a['success']
 assert 9<a['raw_angle_final_deg']<11
 assert 8<a['horizontal_transport_corrected_angle_final_deg']<9
 assert a['projector_transport_endpoint_frobenius']<1e-7
 assert a['frame_orthogonality_max']<1e-10
assert r['gauge_checks']['max_covariance_relative_residual']<1e-11
assert r['gauge_checks']['max_transported_metric_relative_residual']<1e-11
assert max(c['stencil']['spline_vs_five_node_covrate_relative_max'] for c in r['derivative_and_geometry_checks'].values())<2e-4
print('v18.50y authenticated x tensor, derivative convergence and result tests PASS')
