#!/usr/bin/env python3
"""Source-level invariants and negative controls; no physical IVPs."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from run_audit import find_bracket
import numpy as np
from scipy.interpolate import PchipInterpolator
from scipy.optimize import brentq
x=np.linspace(-1,2,32)
A=np.abs(x-0.)
O=np.abs(x-1.)
F=A-O
b=find_bracket(x,F)
assert b is not None and abs(brentq(PchipInterpolator(x,F),x[b],x[b+1])-.5)<1e-12
assert find_bracket(x,np.ones_like(x)) is None
assert find_bracket(x,F)==find_bracket(x,-F)
# Linear signed difference F=(x-.5)-3e-3*t provides a moving zero
# with exact implicit velocity 3e-3, independent of units.
t=.15
ff=x-.5-.003*t
b=find_bracket(x,ff)
assert b is not None
root=brentq(PchipInterpolator(x,ff),x[b],x[b+1])
assert abs(root-(.5+.003*t))<1e-12
print('v18.50w geometry, order and drifting-root controls PASS')
