#!/usr/bin/env python3
import csv,json
from pathlib import Path
r=Path(__file__).resolve().parents[1]/'results'
p=json.loads((r/'report.json').read_text())
assert p['version']=='v18.51f' and all(p['checks'].values())
assert p['counts']['pair_records']==2*3*78*5
assert p['counts']['interplane_cocycle_records']==2*3*77*25
assert p['counts']['similarity_records']==2*2*78
assert p['counts']['cross_seed_records']==3*78*5
for name,expected in [('spectral_pair_ledger.csv',2340),('spectral_sections_ledger.csv',468),
                      ('spectral_pair_transport_cross_coupling.csv',11550),('kinetic_similarity_covariance.csv',312),
                      ('original_autonomous_pair_comparison.csv',1170),('spectral_branch_summary.csv',6)]:
 with (r/name).open(newline='') as f:assert len(list(csv.DictReader(f)))==expected,name
print('v18.51f OUTPUT / ROW COUNTS / SCIENTIFIC GATES PASS')
