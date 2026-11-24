#!/usr/bin/env python3
"""Independent synthetic v18.51i tests (not Q550 data)."""
import importlib.util
from pathlib import Path
import numpy as np
spec=importlib.util.spec_from_file_location('audit',Path(__file__).resolve().parents[1]/'scripts/run_audit.py')
audit=importlib.util.module_from_spec(spec);spec.loader.exec_module(audit)
W=np.array([[1.,.20,.48,.13],[.04,1.,-.26,.21],[0.,.12,1.,-.18],[-.14,0.,.20,1.]])
Wi=np.linalg.inv(W);P0=W@np.diag([1,1,0,0])@Wi;P1=np.eye(4)-P0
B=np.array([[.1,.5,-.7,.12],[-.1,.4,.2,-.5],[.7,-.2,.3,.8],[.13,.6,-.4,.9]])
Q=P1@B@P0
U0,_=audit.orthonormal_right_range(P0);U1,_=audit.orthonormal_right_range(P1)
# The audit's actual function uses sqrt(2) for rank-two source and target.
r=audit.channel_metrics(Q,P0,U0,U1)
assert r['core_reconstruction_relative_error']<1e-12
assert r['factorization_absolute_error']<1e-12
assert r['source_projector_condition']>1.01
# Orthonormal basis changes within each right spectral plane do not change a rate.
C0=np.array([[0.,1.],[-1.,0.]])
C1=np.array([[np.cos(.34),-np.sin(.34)],[np.sin(.34),np.cos(.34)]])
rr=audit.channel_metrics(Q,P0,U0@C0,U1@C1)
assert abs(rr['restricted_rate']-r['restricted_rate'])<1e-12
# Under passive nonorthogonal coordinate changes, raw Euclidean rates need not
# agree. Pulling the metric back does preserve each 2x2 restricted core.
T=np.array([[2.2,.4,-.2,.1],[.1,.7,.2,0.],[0.,.1,1.4,.3],[.25,-.1,.15,.55]])
Ti=np.linalg.inv(T);G=Ti.T@Ti
P0t=T@P0@Ti;Qt=T@Q@Ti
U0t=T@U0;U1t=T@U1
assert np.linalg.norm(U0t.T@G@U0t-np.eye(2))<1e-12
assert np.linalg.norm(U1t.T@G@U1t-np.eye(2))<1e-12
K=U1.T@Q@U0;Kt=U1t.T@G@Qt@U0t
assert np.linalg.norm(K-Kt)<1e-12
assert abs(np.linalg.norm(K,'fro')/np.sqrt(2)-np.linalg.norm(Kt,'fro')/np.sqrt(2))<1e-12
assert abs(np.linalg.norm(Q,'fro')/np.linalg.norm(P0,'fro') - np.linalg.norm(Qt,'fro')/np.linalg.norm(P0t,'fro'))>1e-4
# Pullback Q and P, before using Euclidean SVD, reproduces the original.
Pc=Ti@P0t@T;Qc=Ti@Qt@T
Uc,_=audit.orthonormal_right_range(Pc)
P1c=np.eye(4)-Pc;U1c,_=audit.orthonormal_right_range(P1c)
rest=audit.channel_metrics(Qc,Pc,Uc,U1c)
assert abs(rest['restricted_rate']-r['restricted_rate'])<1e-12
# A purely algebraic 4/5 directional asymmetry can occur without a physical flow.
Qrev=P0@B@P1
ur=audit.channel_metrics(Qrev,P1,U1,U0)
assert r['restricted_rate']>0 and ur['restricted_rate']>0
print('Q550 v18.51i synthetic rank-two, frame-gauge, passive-metric, and extension tests PASS')
