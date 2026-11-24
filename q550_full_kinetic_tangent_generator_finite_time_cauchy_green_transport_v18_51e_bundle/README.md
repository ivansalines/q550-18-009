# Q550 — v18.51e: Full Kinetic Tangent Generator & Finite-Time Cauchy–Green Transport Audit

**Construction is inherited; audit is new.** Original kinetic 5D Cartesian immersion and 10D tangent-state representation are the byte-exact historical v18.49h source. Original driven Q550 solver genealogy is cryptographically authenticated through the supplied v18.51d server sendback (nested v18.51c → b → a → v18.50z → y → x → w → ...). Nothing is generated from an unrelated surrogate equation.

## Server execution

From `/root/elab1/hysteresis`:

```bash
unzip q550_full_kinetic_tangent_generator_finite_time_cauchy_green_transport_v18_51e_bundle.zip
cd q550_full_kinetic_tangent_generator_finite_time_cauchy_green_transport_v18_51e_bundle
set -o pipefail
PYTHON_BIN=python3.13 bash run_on_server.sh 2>&1 | tee ../v18_51e_server.log
```

For optional sensitivity reruns, runner forwards CLI options to `scripts/run_audit.py`: `--rtol`, `--atol`, `--max-step`, `--fd-epsilon`, `--fd-directions 0..4`, `--third-tolerance` (absolute signed-ratio tolerance). Baseline: rtol=2e-11, atol=2e-12, max-step=0.0003, finite-difference epsilon=2e-5, two independent directions, one-third tolerance 0.025. **Scientific identity checks are required; the 1/3 heuristic is never a PASS criterion.**

The parent v18.51d ZIP contains **results** but no full 10D state trajectory series. Therefore this script legitimately reconstructs the original physical Q550 solver once and replays two independent seed IVPs at the same midpoint κ, then integrates the authentic **full 10D tangent ODE continuously along the solutions**. This is intentionally more expensive than post-processing only the archived 79-section tables. The source ledger, tensor archive and all generated outputs are created afresh on your server.

**Chart-consistency correction:** The authenticated shared jet explicitly uses `Jz = S Jy S^-1`, with `S=diag(shared_scale_10d)`, hence `z=S y`; for this propagator the physical kinetic pullback must use `L=DH_tau S^-1`. The v18.51d derived report instead paired the same shared chart with `L=DH_tau S`. Its metric-compatibility identity is algebraically true but does not validate that coordinate identification. v18.51e independently compares physical/raw and shared-chart material transport and records the discrepancy with the previous convention. This is an explicit finding to test, **not** a claim of unique material metric or invalidity of all prior numeric observations.

## Outputs (after successful replay)

- `results/full_generator_and_cauchy_green_ledger.csv`: 474 time × seed × tau-ref records of the entire kinetic generator, symmetric strain, skew rotation and finite-time transport.
- `results/finite_time_cauchy_green_summary.csv`: six metric-convention branch endpoints, volume and rate controls.
- `results/nonlinear_chart_covariance_controls.csv`: passive chart change consistency of `M` and `C` at three sections per branch.
- `results/one_third_hypothesis_ledger.csv`, `one_third_hypothesis_summary.csv`: historical signed-share ratio from v18.51d and its failure/success against a **declared but exploratory** 1/3 proximity.
- `results/material_tangent_cauchy_green_tensors.npz`: complete `F`, `M`, `C`, `L`, `B` tensor series on the 79-section common grid.
- Figures: `full_generator_strain_fraction.png`, `finite_time_cauchy_green_stretches.png`, `one_third_hypothesis_comparison.png`.
- `results/report.json`: lineage, real scientific controls, numerical errors, convention sensitivity and explicit limitations.

`SOURCE_MANIFEST.json` hashes immutable source files. `SHA256SUMS_OUTPUT.json` is generated **only after successful replay** and lists the ten measured output files. `pack_sendback.py` writes `../q550_full_kinetic_tangent_generator_finite_time_cauchy_green_transport_v18_51e_bundle_server_sendback.zip` with matching internal root directory, immutable sources and generated outputs. No transient runtime, `.pyc` or previous output substitution.

## Claims and non-claims

We test a genuine finite-time deformation and its symmetric/stretching and skew/rotation components **in a declared metric family**. The kinetic Cartesian state immersion uses freely chosen `tau_ref` and is not a unique physical phase metric. Neither finite-time Cauchy–Green stretch nor an orthogonal polar factor proves unique material torsion, hysteretic memory, conserved energy transfer, or the proposed one-third rule. Two seeds use the **same** midpoint κ: not simultaneous distinct-κ trajectories.

Read `MATHEMATICAL_PROTOCOL.md`, `SCIENTIFIC_DECISION_RULES.md`, and the full output report after running.
