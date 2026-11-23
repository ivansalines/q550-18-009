#!/usr/bin/env python3
"""Independent analytic and falsification tests; no physical replay needed."""
from __future__ import annotations
import importlib.util,sys
from pathlib import Path
import numpy as np
p=Path(__file__).resolve().parents[1]/'scripts'/'run_audit.py'
spec=importlib.util.spec_from_file_location('v18_50v_testing',p)
m=importlib.util.module_from_spec(spec)
sys.modules[spec.name]=m
spec.loader.exec_module(m)
# Historic interval, deterministic interior/exterior ordering.
a=m.OFFSETS
assert len(a)==22 and np.all(np.diff(a)>0)
assert len(a[(a>=0)&(a<=1)])==13 and len(a[a<0])==5 and len(a[a>1])==4
# Time grid resolves the historic event region as well as longer evolution.
x=m.phase_grid(.05)
assert x[0]==0 and abs(x[-1]-.05)<1e-15
for xi in [.00105,.001059,.001068,.001075,.001092,.0125]:
    assert np.any(np.isclose(x,xi,rtol=0,atol=1e-14))
# No artificial peaks at anchors for a monotonic smooth family.
k=.1666+.00007*a
fleft=np.where(a<=-.5)[0];fright=np.where(a>=1.5)[0]
inside=(a>0)&(a<1)
assert not m.peak_candidates(k,np.linspace(.1,.2,len(k)),(fleft,fright),inside,1.15)
assert not m.peak_candidates(k,np.abs(a-.5),(fleft,fright),inside,1.15)
# A pronounced genuine interior peak is not silently suppressed.
peak=1+2*np.exp(-((a-.5)/.13)**2)
assert len(m.peak_candidates(k,peak,(fleft,fright),inside,1.15))==1
# Sensitivity MUST be differentiated as vectors before taking norms.
X=k[:,None,None]*np.array([[[2.,-1.]]])
obs=np.zeros((len(k),1,4));proj=np.zeros((len(k),1,10,10));rate=X.copy()
fields=m.sensitivity_fields({'Z':X,'D':obs,'P':proj,'F':rate},k,np.ones(2))
assert np.allclose(fields['state_gain'],np.sqrt(5),rtol=1e-11)
# Orthogonal projectors in shared chart: angle via arcsin stable at tiny scales.
q=np.eye(10)
u=q[:,:7];P0=u@u.T
th=3e-5
rot=np.eye(10)
rot[6,6]=np.cos(th);rot[6,7]=-np.sin(th)
rot[7,6]=np.sin(th);rot[7,7]=np.cos(th)
P1=(rot@u)@(rot@u).T
assert abs(np.linalg.norm(P0-P1,2)-np.sin(th))<1e-10
print('v18.50v analytic geometry, false-positive and passage-grid tests PASS')
