#!/usr/bin/env python3
"""Independent synthetic tests; no Q550 ancestors or sampled Q550 data used."""
from pathlib import Path
import importlib.util,numpy as np
r=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('j_mathematical_protocol',r/'scripts/run_audit.py')
j=importlib.util.module_from_spec(spec);spec.loader.exec_module(j)
K=np.array([[.4,-.2],[.6,1.3]])
L=np.array([[.1,.5],[-.7,.2]])
p=j.reciprocity(K,L)
assert abs(p['squared_core_difference']-p['reciprocity_interference'])<1e-13
assert p['adjoint_reciprocity_defect']>0
Q4=j.rotate(.13);Q5=j.rotate(-.31)
pg=j.reciprocity(Q4.T@K@Q5,Q5.T@L@Q4)
for k in ['rate_ratio_5to4_over_4to5','reciprocity_interference','adjoint_reciprocity_defect']:
    assert abs(p[k]-pg[k])<1e-13
pe=j.reciprocity(L,K)
assert abs(pe['reciprocity_interference']+p['reciprocity_interference'])<1e-13
zero=j.reciprocity(K,K.T)
assert zero['adjoint_reciprocity_defect']<1e-13
assert abs(zero['squared_core_difference'])<1e-13

# Synthetic material propagator and orthogonal rank-two Riesz planes.
U4=np.eye(10)[:,:2];U5=np.eye(10)[:,2:4]
P4=U4@U4.T;P5=U5@U5.T
z={}
for ix in (1,2):
    z[(ix,5,4)]={'Uj':U5,'Ui':U4,'P':P5}
    z[(ix,4,5)]={'Uj':U4,'Ui':U5,'P':P4}
M=np.stack([np.eye(10),np.eye(10),np.eye(10)])
M[2,0,2]=.30;M[2,2,0]=.10
w=j.finite_lag(z,M,np.array([0,.1,.2]),1,2)
assert abs(w['forward_ratio']-3)<1e-13
assert w['forward_reciprocity_identity_error']<1e-13

# Changing a passive non-orthogonal state chart without transporting its
# metric alters naive Euclidean rates but not pulled-back metric rates.
D=np.diag([2.,.5]+[1.]*8)
K_orig=U4.T@P4@M[2]@U5
K_naive=(D@U4).T@(D@P4@np.linalg.inv(D))@(D@M[2]@np.linalg.inv(D))@(D@U5)
assert np.linalg.norm(K_naive-K_orig)>0.01
K_common=U4.T@np.linalg.inv(D)@(D@P4@np.linalg.inv(D))@(D@M[2]@np.linalg.inv(D))@D@U5
assert np.linalg.norm(K_common-K_orig)<1e-13
print('v18.51j independent adjoint-gauge, synthetic transport, metric-pullback tests PASS')
