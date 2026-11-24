#!/usr/bin/env python3
"""Independent synthetic checks for observability geometry, not Q550 replay."""
from __future__ import annotations
from pathlib import Path
import importlib.util,numpy as np
from scipy.linalg import expm
ROOT=Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('m_geometry',ROOT/'scripts/run_audit.py')
m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
rng=np.random.default_rng(1684)
# A true second-order kinematic linear flow, measured only via position.
I=np.eye(5);Z=np.zeros((5,5))
B=np.block([[Z,I],[-np.diag(np.linspace(.3,1.4,5)),Z]])
t=np.linspace(0,.1,101);M=np.stack([expm(B*q) for q in t])
G,spec=m.gram_observation(t,M,'position','gaussian',.025)
assert np.min(spec[:,0])>1e-8
assert np.max(spec[:,1])<1e7
# Full time-dependent and nonorthogonal passive chart, with output C'=C Z^-1.
for i in (4,57,100):
    A=np.eye(10)+.12*rng.normal(size=(10,10));Ai=np.linalg.inv(A)
    Gp=Ai.T@G[i]@Ai
    c=np.c_[np.eye(5),np.zeros((5,5))]
    Cnew=c@Ai
    v=rng.normal(size=10)
    assert abs(v@G[i]@v-(A@v)@Gp@(A@v))<1e-11
    assert np.linalg.norm(Cnew@A@v-c@v)<1e-12
# Exact polynomial vs SPD direct norm difference at arbitrary inputs.
for _ in range(20):
    H=[]
    for i in range(4):
        q=rng.normal(size=(2,2));H.append(.2*np.eye(2)+q.T@q)
    f=rng.normal(size=(2,2));r=rng.normal(size=(2,2))
    p=m.crossing_polynomial(*H,f,r)
    for lam in (0.,.11,.34,.8,1.):
        h=[m.E2+lam*(v-m.E2) for v in H]
        q54=m.gram2(h[1])[0]@f@m.gram2(h[2])[1]
        q45=m.gram2(h[3])[0]@r@m.gram2(h[0])[1]
        expected=m.fro(q54)**2-m.fro(q45)**2
        actual=np.polynomial.polynomial.polyval(lam,p)/(np.linalg.det(h[0])*np.linalg.det(h[2]))
        assert abs(expected-actual)<1e-9
        assert m.gauge_control(f,r,*H)<1e-10
# An independent synthetic metric counterexample, with an exact flip.
f=1.4*np.eye(2);rev=.9*np.eye(2)
Hi4=.2*np.eye(2);Hi5=5*np.eye(2)
old=m.fro(f)/m.fro(rev)
new=m.fro(m.gram2(Hi4)[0]@f@m.gram2(Hi5)[1])/m.fro(m.gram2(Hi5)[0]@rev@m.gram2(Hi4)[1])
assert old>1 and new<1
p=m.crossing_polynomial(Hi4,Hi4,Hi5,Hi5,f,rev)
assert p[0]>0 and np.sum(p)<0
print('v18.51m independent synthetic geometry, SPD, polynomial, gauge, passive chart, and adversarial reversal PASS',flush=True)
