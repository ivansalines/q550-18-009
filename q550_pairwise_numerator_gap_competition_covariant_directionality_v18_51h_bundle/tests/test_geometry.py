#!/usr/bin/env python3
"""Independent four-dimensional synthetic cross-projector derivative test.

This small analytic/synthetic control does not use any Q550 data, and does
not authenticate or certify Q550 physics. It checks the exact left/right
rank-one numerator-gap identity against a centered finite perturbation of M.
"""
import numpy as np
from scipy.linalg import eig, block_diag

R=np.array([[0.,-1.],[1.,0.]])
def block(scale,phase):return scale*(np.cos(phase)*np.eye(2)+np.sin(phase)*R)
S=np.array([[1.2,.05,0.,.2],[.0,1.,.2,0.],[.0,0.,.9,-.1],[.08,0.,.02,1.3]])
Mi=block_diag(block(1.03,.23),block(.95,.62))
M=S@Mi@np.linalg.inv(S)
B=np.array([[.14,.11,-.27,.1],[.09,.08,.13,.22],[-.16,.17,.1,-.12],[.23,-.18,.09,.04]])

def spectral(A):
    val,vl,vr=eig(A,left=True,right=True)
    Rs=[]
    for k in range(4):
        Rs.append(np.outer(vr[:,k],vl[:,k].conj())/np.vdot(vl[:,k],vr[:,k]))
    pos=np.flatnonzero(val.imag>1.e-9)
    assert len(pos)==2
    pos=sorted(pos,key=lambda j:val[j].imag)
    pairs=[]
    for a in pos:
        c=int(np.argmin(abs(val-np.conj(val[a]))))
        pairs.append((a,c))
    return val,Rs,pairs
v,rs,pairs=spectral(M)
P=[(rs[a]+rs[c]).real for a,c in pairs]

def get_pair_proj(A,index):
    vals,proj,pairs=spectral(A)
    return (proj[pairs[index][0]]+proj[pairs[index][1]]).real

# Direction pair 2 -> pair 1; Riesz and centered finite perturbation.
frm=1;to=0
terms=[]
for a in pairs[frm]:
    for k in pairs[to]:
        terms.append(v[k]*(rs[k]@B@rs[a])/(v[a]-v[k]))
Q=sum(terms).real
h=1e-6
Pplus=get_pair_proj(M+h*B@M,frm)
Pminus=get_pair_proj(M-h*B@M,frm)
Pdot=(Pplus-Pminus)/(2*h)
D=Pdot-(B@P[frm]-P[frm]@B)
Qfd=P[to]@D@P[frm]
assert np.linalg.norm(Q-Qfd)<1e-7,(np.linalg.norm(Q-Qfd),np.linalg.norm(Q))
# All pair gap magnitudes are invariant under reversal of direction.
d12=min(abs(v[a]-v[k]) for a in pairs[frm] for k in pairs[to])
d21=min(abs(v[a]-v[k]) for a in pairs[to] for k in pairs[frm])
assert abs(d12-d21)<1e-14
# Nonorthogonal similarity leaves the exact block covariant, not its raw norm.
U=np.diag([1.,.5,1.8,.75]);Ui=np.linalg.inv(U)
Mu=U@M@Ui;Bu=U@B@Ui
v2,rs2,pairs2=spectral(Mu)
nu=[]
for a in pairs2[frm]:
    for k in pairs2[to]:
        nu.append(v2[k]*rs2[k]@Bu@rs2[a]/(v2[a]-v2[k]))
Qu=sum(nu).real
assert np.linalg.norm(Qu-U@Q@Ui)<1e-10
assert np.linalg.norm(Q)>1e-9
assert abs(np.linalg.norm(Q)-np.linalg.norm(Qu))>1e-4
print('v18.51h synthetic Riesz crossblock perturbation / gap symmetry / similarity PASS')
