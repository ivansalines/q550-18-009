# Q550 — v18.51l Metric-Path Continuation & Directionality Survival Audit

**Scientific objective.** Determine whether the inherited Q550 forward crossplane norm hierarchy `5→4 > 4→5` persists as the kinetic position/velocity *state metric convention* varies continuously, not just at `tau_ref` 0.5, 1 and 2. Retain both seeds, genuine inherited 10D material history and both instantaneous and finite-lag directional observables. The new contribution is the **quartic polynomial sign reduction** in `s=tau_ref^2` for each fixed material interval.

## Server command

```bash
cd /root/elab1/hysteresis
cp /root/Downloads/q550_metric_path_continuation_directionality_survival_v18_51l_bundle.zip .
unzip q550_metric_path_continuation_directionality_survival_v18_51l_bundle.zip
cd q550_metric_path_continuation_directionality_survival_v18_51l_bundle
set -o pipefail
PYTHON_BIN=python3.13 bash run_on_server.sh 2>&1 | tee ../v18_51l_server.log
```

The runner regenerates the results, verifies source SHA-256 identity, executes synthetic and persisted-data tests, writes output hashes and packs `../q550_metric_path_continuation_directionality_survival_v18_51l_bundle_server_sendback.zip`.

## Contents

- `inputs/*k*_server_sendback.zip`: byte-exact authenticated v18.51k server sendback, with nested j/i/h/g/f/e ancestors and physical-seed genealogy.
- `reference/*.py`: byte-exact earlier generator and replay scripts (k, j, i, h, g) used in the source authentication and replay.
- `scripts/run_audit.py`: all new metric-path/polynomial sign calculations, reports and plots; readable physical/mathematical protocol also supplied.
- `tests/test_geometry.py`: synthetic independent random SPD Gram checks, an adversarial true direction flip, positive case, O(2) gauge covariance.
- `tests/test_results.py`: independently checks persisted ledgers and scientific summary.
- `results/report.json`: machine-readable audit, lineage, declared checks, quality metrics and limitations.
- `results/metric_path_instantaneous_directionality.csv`: 10,140 measured points (two seeds, 65 tau nodes, 78 xi sections).
- `results/metric_path_finite_lag_directionality.csv`: 29,510 measured points (two seeds, 65 tau nodes, 227 intervals).
- `results/metric_path_polynomial_sign_bounds.csv`: 610 independent polynomial sign diagnostics covering *the whole tau range for each fixed sampled material interval*.
- `results/metric_path_survival_summary.csv`: weakest ratios/margins by seed and lag, with positivity counts.
- `results/metric_path_plane_conditioning.csv`: selected subspace angles and metric Gram conditioning.
- `results/*.png`: transparent presentation of endpoint ratios, minimum margins and ξ-dependence.
- `SOURCE_MANIFEST.json`, `SHA256SUMS_OUTPUT.json`: archival SHA-256 verification.

## Numerical scope

The server integrates no new Q550 10D physical trajectory. It reuses exactly the inherited two Q550 seed histories and applies a smooth kinetic-state weighting. The data cover sampled `0<xi≤0.05`, positive-xi spectral pairs and specified finite lags. The polynomial sign tests constrain **continuous tau** on this finite dataset, but are numerical diagnostics on floating-point data, not interval proof of continuous physical ξ or a universal physical metric. The common-connection gauge alignment does not prove intrinsic material torsion. Documentation and script comments are deliberately in English.
