#!/usr/bin/env python3
"""Independent synthetic controls for local time-lag and factorial attribution."""
import numpy as np
from scipy.integrate import solve_ivp

# A translated two-dimensional curve: projection detects lag to first order,
# and leaves transverse displacement visible, not spuriously interpreted as phase.
t=np.array([1.2,-.3]);ds=.0002;perp=np.array([.3,1.2]);perp=perp/np.linalg.norm(perp)
D=ds*t+.0003*perp
ell=D@t/(t@t)
rem=D-ell*t
assert abs(ell-ds)<1e-14
assert abs(rem@t)<1e-14
assert np.linalg.norm(rem)>.00029

# Explicit same-seed parameter intervention distinguishes seed offset:
# x'=k x, x(0)=seed. Different seeds can mimic a parameter difference.
k1=.1666;k2=.1667;T=.05
f=lambda t,x,k:k*x
end=lambda s,k:solve_ivp(lambda t,x:f(t,x,k),(0,T),[s],rtol=1e-12,atol=1e-13).y[0,-1]
for seed in (1.2,1.3):
 assert abs((end(seed,k2)-end(seed,k1))-seed*np.exp(k1*T)*T*(k2-k1))<1e-8
assert abs(end(1.2,k1)-end(1.3,k1))>1e-2
# Midpoint curvature of an exponential k-dependent response is small but nonzero.
mid=(k1+k2)/2
assert 0<end(1.2,k1)+end(1.2,k2)-2*end(1.2,mid)<1e-8
print('Q550 v18.51q synthetic local projection, seed-factorial, midpoint controls PASS')
