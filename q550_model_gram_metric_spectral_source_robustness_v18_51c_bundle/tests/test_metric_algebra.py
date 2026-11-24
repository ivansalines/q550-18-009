#!/usr/bin/env python3
"""Synthetic geometry and metric-weighted skew tests independent of Q550 data."""
import importlib.util
from pathlib import Path
import numpy as np
p=Path(__file__).resolve().parents[1]/'scripts/run_audit.py'
s=importlib.util.spec_from_file_location('v1851c_geometry',p)
m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
r=np.random.default_rng(51)
for alpha in (0,.1,1,4):
    J=r.normal(size=(10,10))/5
    G=np.eye(10)+alpha*(J.T@J)
    W=m.skew(r.normal(size=(10,10)))
    S=m.skew(r.normal(size=(10,10)))
    check=m.passive_control(W,G,S)
    assert max(check.values())<2e-12,check
    L,Li,cond=m.whiten(G)
    assert cond>=1 and m.fn(L@L-G)<1e-11
    A=m.skew(L@W@Li)
    assert m.fn(A+A.T)<1e-11
print('v18.51c synthetic SPD metric, passive covariance, skew reduction tests PASS')
