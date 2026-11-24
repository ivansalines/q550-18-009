# Q550 — v18.51q

**Paired-κ₀ Shadowing, Phase-Lag & Error-Budget Audit**

## Scientific objective

Test whether the close original and autonomous historic `kappa0` parameter values lead to numerically close nonlinear Q550 trajectories, quantify local phase-equivalent displacement, and compare the observed differences to a separate numerical refinement budget. Do not presume that geometric similarity is an invariant shadowing law.

## Executable genealogy

The archive contains `inputs/q550_physical_clock_moving_frame_drift_absolute_generalized_force_reconstruction_v18_51p_bundle_server_sendback.zip` in full, authenticating v18.51p and nested ancestors. The q audit extracts the exact parent scripts into a temporary work directory, replays the physical solver source, reconstructs both natural turning seeds, and integrates the true nonlinear 10D RHS at both distinct historical kappas plus a midpoint control. No unrelated substitute model is used.

## Run on historical server

```bash
cd /root/elab1/hysteresis/q550_paired_kappa0_shadowing_phase_lag_error_budget_v18_51q_bundle
OPENBLAS_NUM_THREADS=1 PYTHON_BIN=python3.13 bash run_on_server.sh 2>&1 | tee ../v18_51q_server.log
```

The runner verifies source hashes, runs independent mathematical tests, performs the authentic replay, verifies scientific report, writes output hashes and packs a sibling `q550_paired_kappa0_shadowing_phase_lag_error_budget_v18_51q_bundle_server_sendback.zip`.

## Outputs

- `results/report.json`: summary, kappa identities, detailed checks and scientific limits.
- `results/solver_replay_error_budget.csv`: all 12 physical integrations and refinement discrepancies.
- `results/paired_clock_error_ledger.csv`: 6 x 129 individual clock histories and resolution diagnostics.
- `results/paired_kappa_shadow_phase_lag_ledger.csv`: 2 x 129 parameter-pair differences, local phase decomposition and error budget.
- `results/seed_kappa_factorial_ledger.csv`: cross-seed differences at each fixed kappa.
- `results/paired_kappa_physical_state_tensors.npz`: native states, Cartesian positions and velocities, phase and clock data for future reproducible tests.
- Three plots derived from those measured values, plus SHA-256 manifests.

All scientific documentation and code comments are in English. See `MATHEMATICAL_PROTOCOL.md` and `SCIENTIFIC_DECISION_RULES.md` before interpreting the results.
