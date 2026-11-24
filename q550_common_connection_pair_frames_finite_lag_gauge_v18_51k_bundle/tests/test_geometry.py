#!/usr/bin/env python3
"""Synthetic, source-independent gauge and connection regression tests."""
import importlib.util
from pathlib import Path
import numpy as np
p=Path(__file__).resolve().parents[1]/'scripts/run_audit.py'
s=importlib.util.spec_from_file_location('independent_k_geometry',p);k=importlib.util.module_from_spec(s);s.loader.exec_module(k)
U4a=np.array([[1.,0],[0,1],[0,0],[0,0]])
U5a=np.array([[0.,0],[0,0],[1,0],[0,1]])
# For synthetic tests use arbitrary distinct rotations inside each plane.
O4a=k.rot(.41);O4b=k.rot(-.27);O5a=k.rot(-.64);O5b=k.rot(.81)
W4,_=k.orthogonal_polar((U4a@O4b).T@(U4a@O4a))
W5,_=k.orthogonal_polar((U5a@O5b).T@(U5a@O5a))
assert k.fro(W4-O4b.T@O4a)<1e-13
assert k.fro(W5-O5b.T@O5a)<1e-13
K54=np.array([[.4,-.25],[.9,1.1]]);K45=np.array([[.1,.6],[-.2,.4]])
base=k.aligned_measure(K54,K45,k.rot(.31),k.rot(-.22))
T4a=k.rot(.13);T4b=k.rot(-.35);T5a=k.rot(.59);T5b=k.rot(.11)
alt=k.aligned_measure(T4b.T@K54@T5a,T5b.T@K45@T4a,
                        T4b.T@k.rot(.31)@T4a,T5b.T@k.rot(-.22)@T5a)
for n in ('gauge_aligned_adjoint_defect','ratio_5to4_over_4to5','paired_symmetric_norm',
          'paired_antisymmetric_norm','signed_interference'):
    assert abs(base[n]-alt[n])<1e-12,(n,base[n],alt[n])
assert abs(base['squared_rate_difference']-base['signed_interference'])<1e-13
assert abs(base['naive_endpoint_adjoint_defect']-alt['naive_endpoint_adjoint_defect'])>1e-3
# A moving nonorthogonal chart must carry a compatible metric/parallel map.
Aa=k.passive_chart(.012);Ab=k.passive_chart(.042)
Ga=np.linalg.inv(Aa).T@np.linalg.inv(Aa)
Gb=np.linalg.inv(Ab).T@np.linalg.inv(Ab)
C=Ab@np.linalg.inv(Aa)
assert k.relative(C.T@Gb@C,Ga)<1e-12
print('v18.51k synthetic common-connection, independent O(2) gauge and passive-chart tests PASS')
