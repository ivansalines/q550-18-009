#!/usr/bin/env python3
"""Recompute key semantic controls from the generated ledger and NPZ."""
import csv,json,sys
from pathlib import Path
import numpy as np
root=Path(__file__).resolve().parents[1]
report=json.loads((root/'results/report.json').read_text())
with (root/'results/spectral_channel_phase_ledger.csv').open() as f: rows=list(csv.DictReader(f))
assert len(rows)==158 and report['samples']==158 and all(report['checks'].values())
n=np.load(root/'results/dominant_spectral_channel_projectors.npz')
assert len(n['xi'])==79 and n['projector_pair1_original'].shape==(79,10,10)
for seed in ('original','autonomous'):
    rr=[r for r in rows if r['seed_family']==seed]
    assert len(rr)==79
    a=n['projector_pair1_'+seed];b=n['projector_pair2_'+seed]
    assert np.linalg.norm(a@a-a)<1e-11
    assert np.linalg.norm(a@b)<1e-11
    assert float(rr[-1]['sigma_pair_1'])>float(rr[0]['sigma_pair_1'])
    assert float(rr[-1]['sigma_pair_2'])<float(rr[0]['sigma_pair_2'])
    assert float(rr[-1]['angle_pair_1_from_start_deg'])>8
    assert .8<float(rr[-1]['pair1_coupling_fraction_of_out_rate'])<1
print('v18.51a output semantics tests PASS')
