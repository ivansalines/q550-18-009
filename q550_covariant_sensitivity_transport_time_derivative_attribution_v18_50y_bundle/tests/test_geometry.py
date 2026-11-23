#!/usr/bin/env python3
"""Synthetic identities independent of the actual Q550 observations."""
from pathlib import Path
import importlib.util,sys
import numpy as np
from scipy.linalg import expm
file=Path(__file__).resolve().parents[1]/'scripts'/'run_audit.py'
spec=importlib.util.spec_from_file_location('v1850y',file)
m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)
P0=np.diag([1.]*7+[0.]*3)
W=np.zeros((10,10));W[0,7]=.3;W[7,0]=-.3;W[1,8]=-.2;W[8,1]=.2
H=np.zeros((10,10));H[2,9]=.7;H[9,2]=-.7
p=expm(.47*W)@P0@expm(-.47*W)
pdot=m.comm(W,p)
k=m.comm(pdot,p)
assert np.linalg.norm(m.comm(k,p)-pdot)<1e-12
assert np.linalg.norm(k+k.T)<1e-12
E=m.comm(H,p)
assert np.linalg.norm(p@E@p)<1e-12
assert np.linalg.norm((np.eye(10)-p)@E@(np.eye(10)-p))<1e-12
A=m.comm(W,E)
D=A-m.comm(k,E)
S=expm(.035*(W+np.diag([2.,0,0,0,0,-1.,0,0,0,0])))
Si=np.linalg.inv(S)
G=Si.T@Si
assert abs(m.metricnorm(S@D@Si,G)-np.linalg.norm(D))<1e-12
assert abs(float(np.sum(E*m.comm(k,E))))<1e-12
print('v18.50y synthetic geometry, projector transport and metric gauge tests PASS')
