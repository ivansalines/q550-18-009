#!/usr/bin/env python3
"""Regenerated-output gates (never interpret a passing gate as a physical law)."""
from pathlib import Path
import json,csv,numpy as np
root=Path(__file__).resolve().parents[1];res=root/'results'
a=json.loads((res/'report.json').read_text())
assert a['version']=='v18.51j' and len(a['checks'])==20 and all(a['checks'].values())
assert a['counts']==dict(instantaneous_sections=468,finite_lag_channels=1362,pullback_checks=312)
for name,n in [('metric_adjoint_reciprocity_ledger.csv',468),('finite_lag_bidirectional_transport_ledger.csv',1362),('passive_kinetic_metric_pullback_controls.csv',312)]:
    with (res/name).open() as f:rows=list(csv.DictReader(f))
    assert len(rows)==n,(name,len(rows))
for name in ['metric_adjoint_pair_reciprocity.png','finite_lag_material_bidirectional_transport.png','reciprocity_interference_identity.png']:
    assert (res/name).stat().st_size>1000
inst=list(csv.DictReader((res/'metric_adjoint_reciprocity_ledger.csv').open()))
lag=list(csv.DictReader((res/'finite_lag_bidirectional_transport_ledger.csv').open()))
assert max(float(r['reciprocity_identity_error']) for r in inst)<1e-12
assert max(float(r['forward_reciprocity_identity_error']) for r in lag)<1e-12
obs=a['observations']
assert obs['instantaneous_5to4_stronger_total']==sum(float(r['rate_ratio_5to4_over_4to5'])>1 for r in inst)
assert obs['finite_lag_5to4_stronger_total']==sum(float(r['forward_ratio'])>1 for r in lag)
assert a['quality']['max_propagator_composition']<1e-10
print('v18.51j regenerated 20 scientific controls and result sanity tests PASS')
