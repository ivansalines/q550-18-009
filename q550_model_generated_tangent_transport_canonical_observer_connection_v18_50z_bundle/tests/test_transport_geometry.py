#!/usr/bin/env python3
"""Independent algebraic controls for observer/model comparison."""
import importlib.util
from pathlib import Path
import sys
import numpy as np
path=Path(__file__).resolve().parents[1]/'scripts/run_audit.py'
spec=importlib.util.spec_from_file_location('v50z',path)
m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)
rng=np.random.default_rng(550)
Q,_=np.linalg.qr(rng.standard_normal((10,10)))
P=Q[:,:7]@Q[:,:7].T
J=rng.standard_normal((10,10))
K=m.offblock_generator(P,J)
R=m.projector_rate_J(P,J)
assert m.fn(K+K.T)<1e-13
assert m.fn(m.comm(K,P)-R)<1e-12
assert m.fn(P@P-P)<1e-13
E=rng.standard_normal((10,10));E=(E+E.T)/2
assert abs(float(np.sum(E*m.comm(K,E))))<1e-11
assert abs(m.unit_angle(E,E))<1e-12
# Coordinate-covariant check for a fixed orthogonal change of chart:
O,_=np.linalg.qr(rng.standard_normal((10,10)))
assert m.fn(m.offblock_generator(O@P@O.T,O@J@O.T)-O@K@O.T)<1e-11
print('v18.50z independent algebraic geometry tests PASS')
