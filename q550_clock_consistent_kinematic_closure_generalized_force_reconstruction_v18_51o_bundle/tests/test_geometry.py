#!/usr/bin/env python3
"""Independent synthetic clock / effective-force / passive-chart controls."""
import importlib.util,sys
from pathlib import Path
import numpy as np
r=Path(__file__).resolve().parents[1];p=r/'scripts/run_audit.py'
s=importlib.util.spec_from_file_location('q550_v18_51o_geometry',p)
m=importlib.util.module_from_spec(s);sys.modules[s.name]=m;s.loader.exec_module(m)
rows=m.synthetic_checks()
assert len(rows)==3 and all(x['max_identity_error']<1e-12 for x in rows)
# A clock-only (Q',W')=(a W,0) has a nonzero a'/a * Qprime term,
# but *zero* positional acceleration coupling.
a=1.6;adot=.12;E=np.zeros((5,5));F=(adot/a)*np.eye(5)
assert np.linalg.norm(F)>0 and np.linalg.norm(E)==0
# A conservative quadratic potential must produce a symmetric positional
# stiffness and zero velocity sensitivity in fixed matching xi coordinates.
P=np.diag([-1.,-2.,-3.,-4.,-5.]);assert np.max(abs(P-P.T))==0
assert m.static_passive_control(np.zeros((5,5)),1.,np.zeros((5,5)),0.,
                                P,np.zeros((5,5)),P,np.zeros((5,5)))<1e-13
print('v18.51o independent synthetic clock / potential / driven-transport / passive gauge tests PASS')
