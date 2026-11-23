#!/usr/bin/env python3
"""Deterministic principal-angle stress tests; no Q550 model replay required."""
import importlib.util
import pathlib
import sys
import numpy as np
ROOT=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('q550_v1850s_testing',ROOT/'scripts/run_audit.py')
a=importlib.util.module_from_spec(spec);sys.modules[spec.name]=a;spec.loader.exec_module(a)
rng=np.random.default_rng(185050)
base,_=np.linalg.qr(rng.standard_normal((10,10)))
K=base[:,:7];extra=base[:,7:]
# Rotate one in-plane direction into a transverse direction while leaving six others intact.
for ang in (0.00215149,0.02,2.,40.):
    t=np.deg2rad(ang)
    Q=K.copy();Q[:,0]=np.cos(t)*K[:,0]+np.sin(t)*extra[:,0]
    d=a.angle_measures(K,Q)
    assert abs(d['asin_angle_deg']-ang)<2e-10,(ang,d)
    assert abs(d['projector_sin_angle_deg']-ang)<2e-10
    assert d['sin_method_abs_diff']<1e-12
    assert d['ortho_instant_defect']<1e-12
    assert d['ortho_transported_defect']<1e-12
# Invariance under changes of orthonormal basis within the same subspace.
Ua,_=np.linalg.qr(rng.standard_normal((7,7)))
Ub,_=np.linalg.qr(rng.standard_normal((7,7)))
Q=K.copy();Q[:,1]=np.cos(0.0005)*K[:,1]+np.sin(0.0005)*extra[:,1]
a0=a.angle_measures(K,Q)
a1=a.angle_measures(K@Ua,Q@Ub)
assert abs(a0['asin_angle_deg']-a1['asin_angle_deg'])<2e-10
print('v18.50s stable sin-principal-angle tests PASS')
