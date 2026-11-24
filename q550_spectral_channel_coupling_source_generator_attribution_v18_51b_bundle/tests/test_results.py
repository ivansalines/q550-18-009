#!/usr/bin/env python3
"""Semantic integrity checks after replay, independent of image hashes."""
from pathlib import Path
import csv,json,numpy as np
ROOT=Path(__file__).resolve().parents[1]
report=json.loads((ROOT/'results/report.json').read_text())
assert report['version']=='v18.51b'
assert report['classification'].startswith('AUTHENTICATED_NUMERICAL')
assert report['samples']==158
assert len(report['checks'])==9 and all(report['checks'].values())
with (ROOT/'results/spectral_source_attribution_phase_ledger.csv').open() as f:
    rows=list(csv.DictReader(f))
assert len(rows)==158
for seed in ('original','autonomous'):
    rr=[r for r in rows if r['seed_family']==seed]
    assert len(rr)==79 and float(rr[0]['xi'])==0 and abs(float(rr[-1]['xi'])-.05)<1e-14
    for r in rr:
        f=sum(float(r[k]) for k in ('signed_generator_fraction','signed_posture_fraction','signed_canonical_fraction'))
        assert abs(f-1)<1e-10
        assert float(r['lambda_gap'])>1
        assert float(r['projector_velocity_identity_error'])<2e-6
with np.load(ROOT/'results/spectral_generator_attribution_blocks.npz') as d:
    assert d['xi'].shape==(79,)
    for seed in ('original','autonomous'):
        A=d['generator_drift_'+seed]+d['observer_posture_'+seed]+d['canonical_connection_'+seed]
        assert A.shape==(79,10,10)
        assert np.max(abs(A-d['total_'+seed]))<2e-13
print('v18.51b semantic/source decomposition tests PASS')
