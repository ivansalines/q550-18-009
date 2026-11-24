# Q550 — v18.51o

**Clock-Consistent Kinematic Closure & Generalized-Force Reconstruction Audit**

This is a full, reproducible **frozen-tangent** construction and audit. It authenticates the v18.51n server sendback and all nested v18.51m → e ancestors, including the genuine historical v18.49h kinetic source and both genuine v18.51e physical tangent IVPs. It does not re-integrate the original 10D physical state IVPs.

## Run

```bash
cd /root/elab1/hysteresis/q550_clock_consistent_kinematic_closure_generalized_force_reconstruction_v18_51o_bundle
OPENBLAS_NUM_THREADS=1 PYTHON_BIN=python3.13 bash run_on_server.sh 2>&1 | tee ../v18_51o_server.log
```

Expected deliverable: sibling `q550_clock_consistent_kinematic_closure_generalized_force_reconstruction_v18_51o_bundle_server_sendback.zip` containing scripts, inputs, data, figures, `results/report.json`, source and result hash manifests.

The cached `inputs/material_tangent_cauchy_green_tensors_v18_51e.npz` is **byte-verified** against its original nested ancestor at every run; it is not a new solver output or a substituted synthetic data source. This avoids unnecessary decompression on each numerical operation without weakening ancestry.

### Output interpretation

- `results/clock_kinematic_force_germ_ledger.csv`: all 474 branch/metric/section observations.
- `results/clock_kinematic_force_germ_summary.csv`: six branch summaries.
- `results/report.json`: scientific controls, provenance, error budgets, interpretation boundary.
- `results/effective_clock_sensitivity.png`: measured coefficient `alpha(xi)`, not yet a certified physical clock ratio.
- `results/effective_force_linearization.png`: `E,F` norms and positional Jacobian antisymmetry.
- `results/second_order_tangent_closure.png`: independent second-derivative rate check on frozen tangent matrices.

Please read `MATHEMATICAL_PROTOCOL.md` and `SCIENTIFIC_DECISION_RULES.md` before interpreting the plots. Scientific text and code comments are in English.
