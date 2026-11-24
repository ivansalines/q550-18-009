#!/usr/bin/env python3
"""Synthetic independent algebraic tests for the v18.51g spectral derivative."""
from pathlib import Path
import sys
import numpy as np
from scipy.linalg import expm
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from run_audit import spectral_jets,fnorm,rel,EYE,rk4_propagate
from scipy.interpolate import CubicSpline

def test():
    block=np.zeros((10,10))
    for j in range(5):
        a=2*j;w=.35+.17*j;dec=.03*j
        block[a,a]=-dec;block[a+1,a+1]=-dec
        block[a,a+1]=-w;block[a+1,a]=w
    t=.4;mat=expm(block*t);base=spectral_jets(mat,block,t)
    assert len(base)==5
    assert max(fnorm(q['Pdot']) for q in base)<1.e-11
    assert max(fnorm(q['drift']) for q in base)<1.e-11
    assert rel(sum((q['P'] for q in base),np.zeros((10,10))),EYE)<1.e-12
    D=np.diag([1,2,1.4,.8,1.6,1.,.8,1.3,1.2,.7]);Di=np.linalg.inv(D)
    changed=spectral_jets(D@mat@Di,D@block@Di,t)
    for q,r in zip(base,changed):
        assert rel(r['P'],D@q['P']@Di)<1.e-11
        assert rel(r['Pdot'],D@q['Pdot']@Di)<1.e-10
        assert rel(r['drift'],D@q['drift']@Di)<1.e-10
    # Nonconstant conjugation: P'=[K,P], independently check resolvent derivative.
    K=np.zeros((10,10));K[0,2]=.4;K[2,0]=-.4;K[1,3]=.2;K[3,1]=-.2
    S=expm(K*t);Si=np.linalg.inv(S)
    V=S@mat@Si
    Mprime=K@V-V@K+S@block@mat@Si
    B=Mprime@np.linalg.inv(V)
    rotated=spectral_jets(V,B,t)
    for q in rotated:
        assert rel(q['Pdot'],K@q['P']-q['P']@K)<1e-10
        assert rel(q['Pdot']-B@q['P']+q['P']@B,q['drift'])<1e-12
    x=np.linspace(0,.05,7);bb=np.repeat(block[None],len(x),axis=0)
    cs=CubicSpline(x,bb,axis=0)
    assert rel(rk4_propagate(cs,0.,.05,16),expm(block*.05))<1e-10
    print('v18.51g synthetic spectral derivative, similarity, rotating-frame and RK4 controls PASS')

if __name__=='__main__':test()
