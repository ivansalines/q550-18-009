#!/usr/bin/env python3
"""Independent output and decision-ledger consistency checks for v18.51i."""
from pathlib import Path
import csv,json,math
P=Path(__file__).resolve().parents[1]
r=json.loads((P/'results/report.json').read_text())
assert r['version']=='v18.51i' and len(r['checks'])>=18 and all(r['checks'].values())
def get(n):
 with (P/'results'/n).open(newline='') as f:return list(csv.DictReader(f))
channels=get('subspace_restricted_channel_ledger.csv')
direction=get('projector_conditioning_directionality.csv')
cov=get('pulled_back_kinetic_similarity_controls.csv')
assert len(channels)==9360 and len(direction)==468 and len(cov)==624
assert {x['seed_family'] for x in direction}=={'original','autonomous'}
assert {float(x['tau_ref']) for x in direction}=={0.5,1.,2.}
assert {int(x['index']) for x in direction}==set(range(1,79))
assert all(float(x['core_reconstruction_relative_error'])<3e-7 for x in channels)
assert all(abs(float(x['raw_rate'])-float(x['restricted_rate'])*float(x['ambient_extension_factor'])/float(x['source_projector_condition']))<5e-10 for x in channels)
assert all(abs(float(x['raw_ratio_5to4_over_4to5']) - float(x['restricted_ratio_5to4_over_4to5'])*float(x['ambient_extension_ratio'])*float(x['source_condition_ratio']))<5e-10 for x in direction)
raw=sum(x['raw_5to4_exceeds_reverse']=='True' for x in direction)
restricted=sum(x['restricted_5to4_exceeds_reverse']=='True' for x in direction)
strongest=sum(x['restricted_5to4_largest_of_20']=='True' for x in direction)
assert raw==r['observations']['raw_survival']
assert restricted==r['observations']['restricted_survival']
assert strongest==r['observations']['largest_restricted_5to4']
assert r['quality']['kinetic_common_frame']['max_restricted_common_interior']<1e-6
assert math.isfinite(max(float(a['largest_principal_angle_4_5_degrees']) for a in direction))
print('Q550 v18.51i independent scientific output tests PASS; raw',raw,'restricted',restricted,'rank1',strongest)
