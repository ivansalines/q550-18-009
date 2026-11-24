#!/usr/bin/env python3
"""Independent analytic and synthetic controls for v18.51p."""
import sys,importlib.util
from pathlib import Path
import numpy as np
r=Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('q550p_tests_mod',r/'scripts/run_audit.py')
a=importlib.util.module_from_spec(s);sys.modules[s.name]=a;s.loader.exec_module(a)
# Nonlinear state-dependent clock with a known fifth-position gradient.
y=np.array([.2,.3,1.,-.2,-.5,.4,.8,-.7,.1,.02]);mx=1.3
for state in (y,y+np.array([.07,.03,.11,.04,-.03,.02,-.06,.03,.05,.01])):
 def rhs(t,z):
  c=1.4+.09*z[8]+.03*t
  f=np.zeros(10)
  f[a.QPOS]=c*z[a.UVEL]
  f[a.UVEL]=np.array([-.4,.2,-.3,.1,-.2])
  return f
 for t in (.0,.12):
  val=a.nonlinear_at(state,t,rhs,mx,h=1e-5)
  assert abs(val['c']-(1.4+.09*state[8]+.03*t))<1e-13
  assert val['rate_id']<1e-13
  assert abs(val['c_t']-.03)<1e-10
  assert abs(val['c_y'][8]-.09)<1e-10
  assert np.linalg.norm(np.delete(val['c_y'],8))<1e-10
  assert a.rel(val['forceq'],val['force_EL_cartesian'])<1e-12
  assert a.rel(a.acceleration_independent(state,t,rhs,mx,1e-5),val['acceleration'])<1e-7
  # Position-response in (Q,V) is an outer product from clock gradient.
  g=val['clock_frame'];assert np.linalg.norm(g[5:])<1e-10
  assert np.linalg.matrix_rank(np.outer(val['V'],g[:5]),tol=1e-8)==1
print('v18.51p SYNTHETIC KINEMATIC/CLOCK/EL FORCE TESTS PASS')
