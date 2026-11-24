#!/usr/bin/env python3
"""Post-audit result and numerical bookkeeping controls."""
import csv,json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; O=ROOT/'results'
r=json.loads((O/'report.json').read_text())
assert r['version']=='v18.51g' and all(r['checks'].values())
assert r['lineage']['no_new_physical_ivp'] and r['lineage']['physical_seed_ivps']==2
expected={'covariant_spectral_projector_ledger.csv':2340,
          'instantaneous_covariant_interplane_rate.csv':9360,
          'finite_step_vs_instantaneous_cross_rate.csv':9240,
          'time_grid_derivative_refinement.csv':18,
          'kinetic_similarity_covariant_control.csv':312,
          'rk4_cocycle_step_refinement.csv':468,
          'endpoint_cross_pair_summary.csv':6}
for name,n in expected.items():
    with (O/name).open(newline='') as f: count=sum(1 for _ in csv.DictReader(f))
    assert count==n,(name,count,n)
for name in ('covariant_spectral_projector_drift.png','spectral_covariant_cross_pair_rates.png','time_grid_refinement.png'):
    assert (O/name).stat().st_size>10000
assert len(r['endpoint_cross_pair'])==6
assert all(x['largest_endpoint_pair']=='5->4' for x in r['endpoint_cross_pair'])
assert r['numerical_quality']['coarse_grid_p90']['1']<r['numerical_quality']['coarse_grid_p90']['4']
assert math.isfinite(r['numerical_quality']['max_finite_to_instantaneous_rate_relative_error'])
print('v18.51g results schema and count checks PASS')
