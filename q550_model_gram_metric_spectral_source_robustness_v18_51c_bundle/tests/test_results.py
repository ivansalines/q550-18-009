#!/usr/bin/env python3
"""Test completed scientific results, including negative/evolving metric sources."""
from pathlib import Path
import csv,json
r=Path(__file__).resolve().parents[1]/'results'
report=json.loads((r/'report.json').read_text())
assert report['version']=='v18.51c' and report['all_rows']==790
assert all(report['checks'].values()),report['checks']
assert report['euclidean_parent_b_max_abs_diff']<3e-6
assert report['max_independent_weighted_time_derivative_relative_error']<2e-4
with open(r/'metric_spectral_source_phase_ledger.csv',newline='') as f:rows=list(csv.DictReader(f))
assert len(rows)==790
for seed in ('original','autonomous'):
    for variant in ('euclidean','Jgram_0p1_frozen','Jgram_1_frozen','Jgram_4_frozen','Jgram_1_evolving'):
        filtered=[row for row in rows if row['seed_family']==seed and row['metric']==variant]
        assert len(filtered)==79
        assert all(float(row['pair_gap'])>1 for row in filtered)
        assert all(float(row['signed_sum_residual'])<1e-10 for row in filtered)
        assert all(float(row['signed_canonical'])>float(row['signed_model_total']) for row in filtered)
        assert float(filtered[-1]['signed_canonical'])>float(filtered[0]['signed_canonical'])
        assert float(filtered[-1]['sigma1'])>float(filtered[0]['sigma1'])
        assert float(filtered[-1]['sigma2'])<float(filtered[0]['sigma2'])
        if variant=='Jgram_1_evolving':assert float(filtered[-1]['signed_metric'])<0
print('v18.51c results and scientific decision rules PASS')
