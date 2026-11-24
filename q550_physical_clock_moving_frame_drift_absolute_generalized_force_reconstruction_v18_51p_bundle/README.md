# Q550 — v18.51p

**Physical Clock, Moving-Frame Drift & Absolute Generalized-Force Reconstruction Audit**

This is a construction-plus-audit of the **original nonlinear Q550 10D driven solver**, not a new fit to the frozen tangent transport. It replays both independent midpoint-kappa seed preparations and derives the trajectory clock, Cartesian acceleration and on-trajectory absolute kinetic generalized force directly from the authenticated RHS and kinetic energy.

## Run on the historical server

```bash
cd /root/elab1/hysteresis/q550_physical_clock_moving_frame_drift_absolute_generalized_force_reconstruction_v18_51p_bundle
OPENBLAS_NUM_THREADS=1 PYTHON_BIN=python3.13 bash run_on_server.sh 2>&1 | tee ../v18_51p_server.log
```

The runner checks the ancestry, carries out the two genuine nonlinear physical 10D IVPs, computes the clock/force ledger and independent derivative tests, regenerates plots, verifies results, and packs the sibling `_server_sendback.zip` archive.

The original v18.51o sendback, byte-exact v18.51e tensor cache, historical v18.50x solver stage code, historical v18.50z replay helper, and historic v18.49h kinetic construction are included. Nested v18.51n→...→v18.50w and all deeper input ancestors reside inside the original v18.51o archive, which is re-verified at runtime.

**Outputs:** `results/physical_clock_absolute_force_ledger.csv`, `results/nonlinear_force_jacobian_replay.csv`, `results/clock_force_selected_sections.csv`, plots, `results/report.json`, input and output hash manifests. Scientific comments and reports are in English.

The first section of this work is *construction* from physical nonlinear equations; numerical comparisons to the historical tangent solver are subsequent *audits*. Read `MATHEMATICAL_PROTOCOL.md` and `SCIENTIFIC_DECISION_RULES.md` before interpreting physical claims.
