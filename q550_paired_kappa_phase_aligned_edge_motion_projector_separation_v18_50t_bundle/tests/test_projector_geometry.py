#!/usr/bin/env python3
"""Analytic controls for common-chart comparison and stable projector gaps."""
import sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from run_audit import pair_geometry,extrema_diagnostic
import pandas as pd
rng=np.random.default_rng(20261103)
A=rng.standard_normal((10,10))
V,_=np.linalg.qr(A)
K=np.eye(10)[:,:7];P=K@K.T
zero=pair_geometry(P,K,P,K)
assert zero['projector_op_gap']<2e-15
assert zero['max_principal_angle_deg']<2e-13
rot=np.eye(10);t=.001
rot[0,0]=np.cos(t);rot[0,8]=-np.sin(t);rot[8,0]=np.sin(t);rot[8,8]=np.cos(t)
L=rot@K;Q=L@L.T
h=pair_geometry(P,K,Q,L)
assert abs(h['projector_op_gap']-np.sin(t))<1e-13
assert abs(h['max_principal_angle_deg']-np.degrees(t))<1e-10
assert h['angle_identity_abs_res']<1e-13
# Common orthogonal reference changes must leave paired distances unchanged.
U,_=np.linalg.qr(rng.standard_normal((10,10)))
h2=pair_geometry(U@P@U.T,U@K,U@Q@U.T,U@L)
assert abs(h['projector_op_gap']-h2['projector_op_gap'])<1e-14
# A diagonal change is not an orthogonal observer transformation; the chart
# must be shared, never independently optimized for the two branches.
B=rng.standard_normal((4,10));scale=np.linspace(1,4,10)
Bphysical=B*scale[None,:]
Bref=Bphysical/scale[None,:]
assert np.allclose(B,Bref,atol=1e-15)
# A monotonic gap does not count as an oscillation.
df=pd.DataFrame({'xi_original':np.linspace(0,1,101),'full_projector_gap':np.linspace(0.3,0.5,101)})
assert not extrema_diagnostic(df,'full_projector_gap')
print('v18.50t common-chart and stable-angle geometry tests PASS')
