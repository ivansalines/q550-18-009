#!/usr/bin/env python3
"""Analytic pullback/connection and passive chart tests independent of Q550 replay."""
import importlib.util,sys
from pathlib import Path
import numpy as np
p=Path(__file__).resolve().parents[1]/'scripts/run_audit.py'
s=importlib.util.spec_from_file_location('v1851d_math',p)
m=importlib.util.module_from_spec(s);sys.modules[s.name]=m;s.loader.exec_module(m)
r=np.random.default_rng(51)
for tau in (.5,1,2):
    y=np.array([.2,.12,.5,-.08,.3,.17,-.31,.11,.2,-.22])
    H,D=m.kin.embedding_and_jac(y,1.2,tau)
    G=D.T@D
    assert np.linalg.eigvalsh(G).min()>1e-6
    # Check explicit Cartesian gradient with centered directional differences.
    for k in range(10):
        h=2e-6
        yp=y.copy();yp[k]+=h
        ym=y.copy();ym[k]-=h
        Hplus=m.kin.embedding_and_jac(yp,1.2,tau)[0]
        Hminus=m.kin.embedding_and_jac(ym,1.2,tau)[0]
        assert np.linalg.norm((Hplus-Hminus)/(2*h)-D[:,k])<4e-10
    # Check historical kinetic energy is exactly the last 5 coordinates.
    assert abs(m.kin.kinetic_energy(y,1.2)-.5*np.dot(m.kin.embedding_and_jac(y,1.2)[0][5:],m.kin.embedding_and_jac(y,1.2)[0][5:]))<1e-14
    W=m.skew(r.normal(size=(10,10)))
    chk=m.passive_chart(D,W)
    assert max(chk.values())<1e-11
    Dp=r.normal(size=(10,10))*.01
    Gamma=np.linalg.solve(D,Dp)
    Gp=Dp.T@D+D.T@Dp
    assert np.linalg.norm(Gp-Gamma.T@G-G@Gamma)<1e-11
print('v18.51d historical kinetic pullback, metric compatibility, and passive covariance tests PASS')
