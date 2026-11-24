# Q550 v18.51d — Kinetic-Metric Construction & Connection Compatibility Audit

**Two distinct stages:** the mathematical kinetic-state metric is **constructed** from the original physical model (not an empirical audit); only then do we audit connection compatibility and source attribution.

This bundle uses the original v18.49h kinetic Cartesian immersion `H=(Q,tau_ref*V)` with its byte-exact historical Python source, the genuine v18.51c server sendback, and its authenticated b → a → z → y → x → w → ... Q550 genealogy. No surrogate solver is used.

It recomputes **two physically driven 10D Q550 seed trajectories** at one midpoint κ₀ and 79 sections through ξ=0.05. In the same inherited observer chart, it constructs the 10D Sasaki-type kinetic pullback metric `G=L.T L` with `L=DH@diag(shared_scale)` at tau_ref = 0.5, 1 and 2.

It then evaluates the compatible connection `Gamma=L^-1 Lprime`, compares model/canonical/kinetic-frame contributions to the spectral coupling, and tests covariance under a passive non-orthogonal chart change. Crucially, no kinetic metric is inferred from `J.T@J`: that was only the diagnostic metric in v18.51c.

Read **`KINETIC_METRIC_DERIVATION.md` first**, then `SCIENTIFIC_DECISION_RULES.md` and `SCIENTIFIC_REPORT.md`. The tau_ref scaling remains a declared modeling convention; do not claim a unique material phase-space metric.

## Run on the server

```bash
cd /root/elab1/hysteresis
unzip q550_kinetic_metric_construction_connection_compatibility_v18_51d_bundle.zip
cd q550_kinetic_metric_construction_connection_compatibility_v18_51d_bundle
set -o pipefail
PYTHON_BIN=python3.13 bash run_on_server.sh 2>&1 | tee ../v18_51d_server.log
```

The runner authenticates the immutable sources, checks algebraic derivations, regenerates two authentic Q550 driven IVPs, computes metric observations, runs output tests, hashes generated results separately and writes `../q550_kinetic_metric_construction_connection_compatibility_v18_51d_bundle_server_sendback.zip` **without** `runtime`, `.pyc` or logs.

## Results

- `results/kinetic_metric_spectral_source_ledger.csv`: six seed×tau_ref series of 79 sections (474 observations).
- `results/kinetic_vs_model_gram_source_summary.csv`: compared start/end signed attributions, conditioning, independent rate checks.
- `results/passive_kinetic_chart_controls.csv`: passive observer-chart invariance.
- `results/kinetic_metric_source_attribution.png`, `moving_kinetic_frame_source.png`, `kinetic_metric_secondary_spectrum.png`: genuine result figures.
- `results/report.json`: provenance, numerical gates, decision and caveats.
- `reference/kinetic_metric_v18_49h.py`: exact historical source code of the original Q550 kinetic state construction.
- `reference/z_replay_helpers_v18_50z.py`: exact historical model-replay helpers from the v18.50z sendback.

**Important:** spectral signed fractions are metric-dependent diagnostics, not fractions of stress or energy. A passing metric-compatibility identity certifies an internally consistent construction, not physical material-memory causality.
