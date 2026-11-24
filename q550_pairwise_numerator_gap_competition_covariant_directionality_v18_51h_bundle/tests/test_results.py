#!/usr/bin/env python3
"""Audit generated outputs, cardinalities, and scientific decision criteria."""
import csv,json,math
from pathlib import Path
p=Path(__file__).resolve().parents[1]
r=json.loads((p/'results/report.json').read_text())
assert r['version']=='v18.51h' and all(r['checks'].values()),r['checks']
assert r['counts']['directed_crossblocks']==9360
assert r['counts']['directionality_sections']==468
assert r['counts']['cross_convention_comparisons']==6240
assert r['lineage']['no_new_physical_ivp']
with (p/'results/pairwise_directionality_decomposition.csv').open() as f:
    rows=list(csv.DictReader(f))
assert len(rows)==468
assert all(x['strongest_channel']=='5->4' for x in rows)
assert all(float(x['directional_rate_ratio'])>1 for x in rows)
assert max(abs(float(x['directional_rate_ratio'])-
               float(x['crossblock_norm_ratio_5to4_over_4to5'])*
               float(x['source_projector_norm_ratio_P4_over_P5'])) for x in rows)<1e-10
with (p/'results/pairwise_numerator_gap_ledger.csv').open() as f:
    ledger=list(csv.DictReader(f))
assert len(ledger)==9360
assert min(float(x['pair_min_complex_gap']) for x in ledger)>0
assert max(float(x['cross_block_identity_error']) for x in ledger)<2e-7
assert all(math.isfinite(float(x['covariant_directed_rate'])) for x in ledger)
with (p/'results/kinetic_common_frame_covariance.csv').open() as f:
    cov=list(csv.DictReader(f))
assert len(cov)==6240
for fn in ('pairwise_rate_and_shared_gap.png','pairwise_numerator_cancellation.png','kinetic_directionality_convention_sensitivity.png'):
    assert (p/'results'/fn).stat().st_size>10000
print('v18.51h 9360 crossblocks / 468 sections / 6240 similarity controls PASS')
