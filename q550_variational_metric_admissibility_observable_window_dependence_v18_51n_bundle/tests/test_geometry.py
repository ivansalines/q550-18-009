#!/usr/bin/env python3
"""Independent synthetic controls: valid and degenerate observation windows."""
import importlib.util,sys
from pathlib import Path
import numpy as np
r=Path(__file__).resolve().parents[1]
p=r/'scripts/run_audit.py'
spec=importlib.util.spec_from_file_location('q550_n_geometry',p)
m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)
k=m.kinetic_hessian_test()
assert k['finite_difference_kinetic_hessian_max_relative_error'] < 5e-6
# Fixed material identity with position-only output is rank five: SPD MUST
# NOT be presumed on a zero-duration or uncontrollable observation window.
t=np.linspace(0,.05,12);M=np.broadcast_to(np.eye(10),(12,10,10)).copy()
G,d=m.physical_output_gram(t,M,'position','bilateral',.025)
assert max(abs(np.linalg.eigvalsh(G[-1])[:5]))<1e-12
assert not d[-1]['raw_well_resolved']
# Kinematic coupling of velocity to position restores full observability
# on a finite positive interval.
M=np.asarray([np.block([[np.eye(5),float(u)*np.eye(5)],
                        [np.zeros((5,5)),np.eye(5)]]) for u in t])
Gp,dp=m.physical_output_gram(t,M,'position','past',.025)
assert np.linalg.eigvalsh(Gp[-1])[0]>1e-8
Gf,df=m.physical_output_gram(t,M,'position','future',.025)
assert df[-1]['window_span']==0
assert not df[-1]['raw_well_resolved']
# An arbitrary change of 2D orthonormal bases cannot change a restricted norm.
O=np.array([[np.cos(.3),-np.sin(.3)],[np.sin(.3),np.cos(.3)]])
K=np.array([[1.,.3],[-.2,.8]])
H=np.array([[2.,.4],[.4,1.]])
root=lambda x: m.restricted(np.eye(2),x)
def norm(A,G):
 R,IR=root(G);return m.fro(R@A@IR)
assert abs(norm(K,H)-norm(O.T@K@O,O.T@H@O))<1e-12
print('v18.51n independent geometry / rank / gauge tests PASS')
