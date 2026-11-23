#!/usr/bin/env python3
"""Preflight geometric identities and strict peak detection."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import numpy as np
from run_audit import projector_gap, local_peak_candidates
rng=np.random.default_rng(517)
a=rng.normal(size=(3,10));b=rng.normal(size=(3,10))
qa=np.linalg.qr(a.T)[0];qb=np.linalg.qr(b.T)[0]
P=np.eye(10)-qa@qa.T;Q=np.eye(10)-qb@qb.T
x=projector_gap(P,Q)
assert abs(x-projector_gap(Q,P))<1e-13
assert projector_gap(P,P)<1e-13
assert not local_peak_candidates(np.arange(17),np.linspace(0,1,17),min_prominence=0.1)
assert len(local_peak_candidates(np.arange(17),np.r_[np.linspace(0,1,9),np.linspace(.875,0,8)],min_prominence=.2))==1
print('v18.50u geometry and peak decision rules PASS')
