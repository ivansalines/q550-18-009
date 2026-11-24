#!/usr/bin/env python3
"""Independent analytical and adversarial controls for v18.51l.

No Q550 samples are used in these tests. A genuine direction reversal
must be detected rather than suppressed by a hard-coded survival check.
"""
import importlib.util
from pathlib import Path
import numpy as np
p=Path(__file__).resolve().parents[1]/'scripts/run_audit.py'
s=importlib.util.spec_from_file_location('metric_path_synthetic',p)
a=importlib.util.module_from_spec(s);s.loader.exec_module(a)
rng=np.random.default_rng(55151)
for _ in range(100):
 U,_=np.linalg.qr(rng.normal(size=(10,2)))
 V,_=np.linalg.qr(rng.normal(size=(10,2)))
 B4=U[5:].T@U[5:];B5=V[5:].T@V[5:]
 K54=rng.normal(size=(2,2));K45=rng.normal(size=(2,2))
 c=a.signed_polynomial(B4,B4,B5,B5,K54,K45)
 for tau in (.5,.77,1.,1.3,2.):
  s=tau*tau
  A,_,_=a.roots_of_gram(B4,s);_,IA,_=a.roots_of_gram(B4,s)
  B,_,_=a.roots_of_gram(B5,s);_,IB,_=a.roots_of_gram(B5,s)
  direct=a.fro(A@K54@IB)**2-a.fro(B@K45@IA)**2
  denom=np.linalg.det(a.H_from_B(B4,s))*np.linalg.det(a.H_from_B(B5,s))
  computed=a.poly_at(c,s)/denom
  assert abs(direct-computed)<1e-10*max(1,abs(direct),abs(computed))
# An adversarial branch where the direction flips INSIDE the kinetic interval.
# B4=I, B5=0, so ratio 5->4 / 4->5 is 0.8*tau^2.
B4=np.eye(2);B5=np.zeros((2,2));K54=.8*np.eye(2);K45=np.eye(2)
c=a.signed_polynomial(B4,B4,B5,B5,K54,K45)
assert a.poly_at(c,.25)<0 and a.poly_at(c,4.)>0
assert not a.polynomial_sign_info(c)['positive_bernstein']
assert a.polynomial_sign_info(c)['in_range_real_roots']>=1
# A strong positive branch must pass the whole-interval polynomial test.
c=a.signed_polynomial(B4,B4,B5,B5,10*np.eye(2),.1*np.eye(2))
assert a.polynomial_sign_info(c)['positive_bernstein']
# Gauge transformed bases/blocks must preserve the norm-ratio polynomial.
for _ in range(10):
 th,ph=rng.uniform(-3,3,size=2)
 O=np.array([[np.cos(th),-np.sin(th)],[np.sin(th),np.cos(th)]])
 R=np.array([[np.cos(ph),-np.sin(ph)],[np.sin(ph),np.cos(ph)]])
 B4=rng.random((2,2));B4=B4@B4.T;B4/=(1+np.linalg.norm(B4,2))
 B5=rng.random((2,2));B5=B5@B5.T;B5/=(1+np.linalg.norm(B5,2))
 K54=rng.normal(size=(2,2));K45=rng.normal(size=(2,2))
 co=a.signed_polynomial(B4,B4,B5,B5,K54,K45)
 cn=a.signed_polynomial(O.T@B4@O,O.T@B4@O,R.T@B5@R,R.T@B5@R,
                        O.T@K54@R,R.T@K45@O)
 assert np.allclose(co,cn,atol=1e-11,rtol=1e-11)
print('v18.51l independent synthetic rational-polynomial, sign-reversal and O(2) gauge tests PASS')
