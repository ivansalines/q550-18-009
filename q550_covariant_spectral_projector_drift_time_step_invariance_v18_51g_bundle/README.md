# Q550 v18.51g — Covariant Spectral-Projector Drift & Time-Step Invariance Audit

This numerical construction-and-audit uses the **full kinetic Cartesian generator** from authenticated Q550 v18.51e, carried forward through the original v18.51f server sendback. It asks whether finite-time Riesz spectral eigenplanes are materially advected or drift relative to the genuine tangent cocycle, and whether the putative `5 -> 4` coupling persists under time-grid diagnostics and the declared kinetic-state similarity.

## Run

```bash
cd /root/elab1/hysteresis
cp /root/Downloads/q550_covariant_spectral_projector_drift_time_step_invariance_v18_51g_bundle.zip .
unzip q550_covariant_spectral_projector_drift_time_step_invariance_v18_51g_bundle.zip
cd q550_covariant_spectral_projector_drift_time_step_invariance_v18_51g_bundle
set -o pipefail
PYTHON_BIN=python3.13 bash run_on_server.sh 2>&1 | tee ../v18_51g_server.log
```

The runner verifies source SHA-256, executes independent synthetic algebraic tests, reconstructs all spectral projectors and their analytic derivatives from authentic `B M`, checks finite-grid and full-generator covariance, runs output tests, writes output hashes and packs `../q550_covariant_spectral_projector_drift_time_step_invariance_v18_51g_bundle_server_sendback.zip`. The ZIP root matches its filename. The parent archive in `inputs/` is not modified.

## Inputs, outputs and provenance

- `inputs/q550_finite_time_spectral_pairing_kinetic_similarity_transport_v18_51f_bundle_server_sendback.zip`: entire verified parent genealogy; contains genuine v18.51e physical 10D finite-time `M`, generator `B`, and the initial historical Q550 chain.
- `reference/f_spectral_replay_v18_51f.py`: byte-exact historical v18.51f audit script, checked against the parent archive. The v18.51g `scripts/run_audit.py` independently derives and evaluates projector rates.
- `results/report.json`: scientific checks, residuals and scope.
- `results/covariant_spectral_projector_ledger.csv`: section and pair rates, gaps, derivative errors.
- `results/instantaneous_covariant_interplane_rate.csv`: all 20 directed pair-to-pair rates per section.
- `results/finite_step_vs_instantaneous_cross_rate.csv`: finite cocycle leakage versus differential rate.
- `results/time_grid_derivative_refinement.csv`: stride-1/2/4 derivative convergence.
- `results/kinetic_similarity_covariant_control.csv`: raw/common-frame similarity and near-identity conditioning.
- `results/rk4_cocycle_step_refinement.csv`: RK4 1/2/4/8 subdivision tests.
- `results/endpoint_cross_pair_summary.csv`: seed/convention endpoint 5->4 versus 4->5 and dominant channel.
- PNG figures in `results/`: covariant drift, directed rates, grid refinement.
- Source and output manifests, `requirements.txt`, tests and server runner.

**Classification:** numerical covariant finite-time spectral-projector diagnostic, not an intrinsic material torsion, energy transfer, hysteresis, or memory certificate. No 1/3 assumption is used.
