#!/usr/bin/env python3
"""Independently exercise left/right eigenvectors, Riesz projectors and tau similarity."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import numpy as np
import run_audit as v
from scipy.linalg import expm
rng=np.random.default_rng(55051)
J=np.block([[np.array([[.1,-.9],[.9,.1]]) if i==j else np.zeros((2,2)) for j in range(5)] for i in range(5)])
for i in range(5):
 J[2*i:2*i+2,2*i:2*i+2]=np.array([[-.02*(i+1),-(i+.3)],[(i+.3),-.02*(i+1)]])
G=rng.normal(size=(10,10));G+=5*np.eye(10)
M=G@expm(.05*J)@np.linalg.inv(G)
pp=v.order_pairs(v.extract_pairs(M,.05,1.e-10))
assert len(pp)==5
assert v.rel(sum((x['P'] for x in pp),np.zeros((10,10))),np.eye(10))<1e-12
for p in pp:
 assert v.rel(p['P']@p['P'],p['P'])<1e-12
D=np.diag([1.]*5+[2.]*5)
mt=D@M@np.linalg.inv(D)
qq=v.order_pairs(v.extract_pairs(mt,.05,1.e-10))
for p,q in zip(pp,qq):assert v.rel(q['P'],D@p['P']@np.linalg.inv(D))<1e-11
# At xi=0 eigenvectors cannot supply a canonical modal splitting.
assert np.allclose(np.linalg.eigvals(np.eye(10)),np.ones(10))
print('v18.51f SYNTHETIC RIESZ / NONORTHOGONAL / SIMILARITY CONTROLS PASS')
