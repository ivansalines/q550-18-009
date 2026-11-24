# Q550 v18.51m — Independent Material-Metric Construction & Directionality Challenge Audit

This reproducible audit tests whether the `5→4 > 4→5` **norm ranking** from v18.51l survives a materially different, model-informed positive metric. The audit is explicitly capable of returning a negative answer. **It does: the ranking reverses under the independently constructed dynamical-observability metrics.** The underlying Q550 physical material motion, Riesz spectral planes, and projected operators are unchanged. This is a counterexample to interpreting the earlier ranking as a metric-independent directionality or physical arrow.

## Server run

```bash
cd /root/elab1/hysteresis
cp /root/Downloads/q550_independent_material_metric_construction_directionality_challenge_v18_51m_bundle.zip .
unzip q550_independent_material_metric_construction_directionality_challenge_v18_51m_bundle.zip
cd q550_independent_material_metric_construction_directionality_challenge_v18_51m_bundle
set -o pipefail
PYTHON_BIN=python3.13 bash run_on_server.sh 2>&1 | tee ../v18_51m_server.log
```

`run_on_server.sh` authenticates the complete `l → k → j → i → h → g → f → e` genealogy, runs independent synthetic tests, reconstructs both genuine Q550 seed histories without a new physical IVP, constructs observation metrics, replays the tests, writes results + hashes, and packs a full `_server_sendback.zip` alongside the directory. Assumes Python 3.13, NumPy, SciPy and Matplotlib. Run from any parent location; the runner enters its own directory.

## What is independently constructed

The v18.51l family only changed the relative physical Cartesian position/velocity state weight `diag(I5,tau_ref² I5)`. Here the **output** is instead an independently declared measurement of physical Cartesian configuration `Q` or velocity `V`, followed through the **actual Q550 full 10D tangent transport** over the measured `xi ∈ [0,0.05]` interval. Its weighted observability Gramian is an operational SPD state metric, not another constant kinetic-state rescaling and not an energy-Hessian theorem. The primary protocol observes `Q` with Gaussian bandwidth `h=0.025`, with other Gaussian widths, a uniform window, and velocity-output alternatives as robustness challenges.

The primary interpolation `G_lambda = (1-lambda)I + lambda G_Q/c` has a documented global trace normalization `c` and is **not** a physically unique metric path. For each of 610 inherited fixed material observables, the signed squared-strength difference becomes a quartic polynomial in `lambda`; its root in `(0,1)` is computed and stored. The root location is convention-dependent and MUST NOT be interpreted as a Q550 activation threshold.

## Genealogy and outputs

- `inputs/q550_metric_path_continuation_directionality_survival_v18_51l_bundle_server_sendback.zip`: byte-exact parent server sendback with nested ancestors and original physical 10D tangent data.
- `reference/*.py`: byte-exact historical v18.51l/k/j/i/h/g executables used to authenticate and reconstruct the original material history.
- `scripts/run_audit.py`: mathematical construction, projection restriction, norms, quartic root tests, passive chart/gauge challenges, quadrature refinement, ledgers and plotting.
- `tests/test_geometry.py`: independent synthetic SPD, output covariance, exact polynomial identity, gauge and an adversarial true ranking flip.
- `tests/test_results.py`: persisted ledger checks; not a rerun of an assumed scientific conclusion.
- `results/*.csv`: 1,092 instantaneous and 3,178 finite-lag measurements; 610 bridge root measurements; metric conditioning, summaries and quadrature refinement.
- `results/report.json`, `SCIENTIFIC_REPORT.md`, `MATHEMATICAL_PROTOCOL.md`, `SCIENTIFIC_DECISION_RULES.md`, `SOURCE_MANIFEST.json`, `SHA256SUMS_OUTPUT.json` and figures.

All code comments and scientific documentation are in English. No result may be promoted to an intrinsic material directional or torsion law: the observed ordering is a norm ordering and changes with a legitimate alternative measuring geometry.
