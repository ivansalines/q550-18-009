#!/usr/bin/env python3
"""Independent synthetic test of degenerate rank-two spectral-projector identities."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import numpy as np
from scipy.linalg import expm
from run_audit import projectors_from_defect, nrm
rng=np.random.default_rng(202651)
O,_=np.linalg.qr(rng.normal(size=(10,10)))
W0=np.zeros((10,10))
for i,s in [(0,3.8),(2,1.5),(4,0.00001)]:
    W0[i,i+1]=s; W0[i+1,i]=-s
W=O@W0@O.T
V=rng.normal(size=(10,10));dW=(V-V.T)/2
p1,p2,s1,s2=projectors_from_defect(W)
Hprime=-(W@dW+dW@W)
gap=s1*s1-s2*s2
pred=p2@Hprime@p1/gap
h=3e-6
wp=projectors_from_defect(W+h*dW)[0]
wm=projectors_from_defect(W-h*dW)[0]
obs=p2@((wp-wm)/(2*h))@p1
err=nrm(pred-obs)/max(nrm(pred),1)
assert err<2e-8,err
P0=np.zeros((10,10));P0[:7,:7]=np.eye(7);P0=O@P0@O.T
G=rng.normal(size=(10,10));G=(G-G.T)/2
J=rng.normal(size=(10,10));Jprime=rng.normal(size=(10,10))
Pdot=G@P0-P0@G
q=np.eye(10)-P0
Kprime_g=q@Jprime@P0-P0@Jprime.T@q
Kprime_p=-Pdot@J@P0+q@J@Pdot-Pdot@J.T@q+P0@J.T@Pdot

def K(P,JJ):
    q=np.eye(10)-P
    return q@JJ@P-P@JJ.T@q
h=2e-6
rp=expm(h*G);rm=expm(-h*G)
finite=(K(rp@P0@rp.T,J+h*Jprime)-K(rm@P0@rm.T,J-h*Jprime))/(2*h)
err2=nrm(finite-Kprime_g-Kprime_p)/max(nrm(finite),1)
assert err2<2e-8,err2
print('v18.51b synthetic spectral gap and model-generator product-rule tests PASS',err,err2)
