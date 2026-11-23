#!/usr/bin/env python3
"""Exact projector derivative geometry, coordinate and ridge negative controls."""
import importlib.util,sys
from pathlib import Path
import numpy as np
p=Path(__file__).resolve().parents[1]/'scripts/run_audit.py'
spec=importlib.util.spec_from_file_location('q550_v18_50x',p)
mod=importlib.util.module_from_spec(spec);sys.modules[spec.name]=mod;spec.loader.exec_module(mod)
x=np.array([-2.,-1.,0.,1.,2.])
y=x**4+3*x**3-2*x**2+5*x+7
w=mod.finite_weights(0.,x)
assert abs(w@y-5)<1e-12
ang=np.linspace(-.02,.02,21)
P=np.zeros((21,5,2,2))
for i,a in enumerate(ang):
 for j,t in enumerate(np.linspace(0,.01,5)):
  v=np.array([np.cos(a+t),np.sin(a+t)])
  P[i,j]=np.outer(v,v)
m=mod.metrics(P,ang,np.linspace(0,.01,5))
assert np.max(m['projector_idempotency'])<1e-14
assert np.max(m['stencil_3_vs_5_relative'])<2e-3
assert np.max(m['off_tangent_P'])<1e-2
print('v18.50x exact projection geometry and finite-weight controls PASS')
