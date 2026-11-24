#!/usr/bin/env python3
"""Standalone mathematical controls: no physical Q550 outcome is hardcoded."""
import importlib.util,sys
from pathlib import Path
import numpy as np
from scipy.linalg import expm
p=Path(__file__).resolve().parents[1]/'scripts/run_audit.py'
spec=importlib.util.spec_from_file_location('v1851e_math',p)
m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)
rng=np.random.default_rng(1851)
scales=np.linspace(.8,1.4,10)
y0=np.array([.2,.12,.5,-.08,.3,.17,-.31,.11,.2,-.22])
y1=y0+np.linspace(-.01,.02,10)
vel=(y1-y0)/.01
for tau in (.5,1.,2.):
 L0,dL=m.l_and_lprime(y0,vel,1.2,tau,scales)
 L1=m.l_and_lprime(y1,vel,1.2,tau,scales)[0]
 assert np.linalg.eigvalsh(L0.T@L0).min()>0
 h=2e-5
 LF=m.kin.embedding_and_jac(y0+h*vel,1.2,tau)[1]/scales[np.newaxis,:]
 LR=m.kin.embedding_and_jac(y0-h*vel,1.2,tau)[1]/scales[np.newaxis,:]
 assert m.max_rel(dL,(LF-LR)/(2*h))<5e-9
 J=rng.normal(size=(10,10))*.1
 F=expm(.01*J)
 M=L1@F@np.linalg.inv(L0)
 C=M.T@M
 assert np.linalg.eigvalsh(C).min()>0
 chk=m.passive_checks(F,L0,L1,y0,y1,scales)
 assert max(chk.values())<1e-11,chk
 B=L0@J@np.linalg.inv(L0)+dL@np.linalg.inv(L0)
 assert m.max_rel(B,m.sym(B)+m.skew(B))<1e-13
 # Exact analytic constant-B test for the material strain rate identity.
 A=rng.normal(size=(10,10))*.03
 M_a=expm(.01*A)
 C_a=M_a.T@M_a
 eps=1e-6
 Cp=(expm((.01+eps)*A).T@expm((.01+eps)*A)-expm((.01-eps)*A).T@expm((.01-eps)*A))/(2*eps)
 assert m.max_rel(Cp,2*M_a.T@m.sym(A)@M_a)<2e-9
 assert abs(np.linalg.slogdet(M_a)[1]-.01*np.trace(A))<1e-12
# Ensure a genuinely nontrivial scale is not silently interpreted as its inverse.
S=np.diag([1.,1.,3.261619,1.,1.96519474,1.,1.,1.,1.,1.])
DH0=m.kin.embedding_and_jac(y0,1.2,1.)[1]
DH1=m.kin.embedding_and_jac(y1,1.2,1.)[1]
A=rng.normal(size=(10,10))*.4
F=expm(.05*A)
Fy=np.linalg.inv(S)@F@S
Mcorrect=DH1@Fy@np.linalg.inv(DH0)
Mlegacy=(DH1@S)@F@np.linalg.inv(DH0@S)
assert m.max_rel(Mcorrect,Mlegacy)>1e-4
assert len(m.TAUS)==3
print('v18.51e synthetic kinetic, finite-time Cauchy–Green, nonlinear-chart and rate identities PASS')
