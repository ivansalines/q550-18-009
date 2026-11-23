#!/usr/bin/env python3
"""Synthetic geometry tests: skew spectral pairs and sign/coordinate invariance."""
import sys
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from run_audit import spectral_channels,angle_from_projectors,fn

rng=np.random.default_rng(551)
Q,_=np.linalg.qr(rng.normal(size=(10,10)))
S=np.zeros((10,10))
S[0,1]=4;S[1,0]=-4;S[2,3]=1.5;S[3,2]=-1.5
M=Q@S@Q.T
st,PP,sk,pair,recon=spectral_channels(M)
assert np.allclose(st[:2],[4,1.5],rtol=0,atol=2e-14)
assert st[2]<1e-12 and recon<1e-12 and sk<1e-12 and pair<1e-12
assert np.linalg.norm(PP[0]@PP[1])<1e-12
assert angle_from_projectors(PP[0],PP[0])<1e-5
Q2,_=np.linalg.qr(rng.normal(size=(10,10)))
st2,PP2,_,_,_=spectral_channels(Q2@M@Q2.T)
assert np.allclose(st,st2,rtol=0,atol=3e-14)
for i in (0,1):assert fn(PP2[i]-Q2@PP[i]@Q2.T)<1e-13
# Spectral intensities are invariant under conjugation, but a changed metric is
# a genuinely different measurement and is NOT claimed to preserve them.
print('v18.51a synthetic skew-pair geometry tests PASS')
