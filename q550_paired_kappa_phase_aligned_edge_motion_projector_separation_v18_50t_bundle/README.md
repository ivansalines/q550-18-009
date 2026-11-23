# Q550 v18.50t — Paired-κ₀ Phase-Aligned Edge Motion & Projector Separation Audit

## Scientific purpose

Examine the user's **two moving edges / narrow-band dynamical activator hypothesis** by comparing the rank-three analytic structural-observer Jacobian's seven-dimensional tangent kernels on **two separately driven physical Q550 trajectories**. This study is a test of a proposed interpretation, not a confirmation of dynamic activation, material memory, physical interfaces or polymer rheology.

The audit verifies the server-authenticated **v18.50s sendback** (the packaged scientific ancestor). Its nested genealogy supplies the original solver. No response vector L or T is used to fit or rotate these projectors.

## Central design: a common 10D comparison chart

The parent v18.50q defines the normalized observer

`d = normalize(diag(1 / w) [F_2, F_6, (JF)_2, (JF)_6])`.

Its Jacobian `B` has structural rank ≤3; the replay finds rank three and therefore a 7D nullspace. Parent routines express derivatives in branch-specific seed charts. **They must not be compared directly.** Here each `B` is transformed to a shared chart:

`B_shared = B_branch @ diag(scale_branch / scale_shared)`.

The shared scale uses the elementwise maximum of one and the two inherited state-preparation scales. A raw-physical-coordinate chart is also evaluated as a deliberate sensitivity test.

For each pair of nullspace projectors `P_original`, `P_autonomous`, we report the operator norm `||P_original - P_autonomous||_2`, the Frobenius norm, and stable principal angles via `asin(sigma_max((I-P_original) K_autonomous))`.

Since two 7D subspaces in 10D must intersect in at least four dimensions, at most three principal angles are nonzero. No individual singular vector is promoted to a physical edge.

## Three comparisons

1. **Common turn-relative ξ:** two independently prepared trajectories are sampled at the same ξ offset from their respective natural turning sections (129 sections over `[0, 0.001092]`). This is a convention, not proof of identical clock phase; the phase mismatch is recorded.
2. **Normalized parity-to-stationary gate:** each branch traverses its own inherited event bracket using a shared coordinate `[0,1]` (65 samples). This compares corresponding event fractions, *not* identical physical time or drive phase.
3. **Controlled state/parameter swaps:** the observer Jacobian is evaluated at the same physical 10D state with the other κ₀, as well as at the other prepared state with κ₀ fixed. These are **instantaneous counterfactual evaluations**, not full new trajectories at crossed parameters.

The raw-physical chart control uses 17 additional sections.

## Run on the server

```bash
cd /root/elab1/hysteresis
unzip q550_paired_kappa_phase_aligned_edge_motion_projector_separation_v18_50t_bundle.zip
cd q550_paired_kappa_phase_aligned_edge_motion_projector_separation_v18_50t_bundle
set -o pipefail
PYTHON_BIN=python3.13 bash run_on_server.sh 2>&1 | tee ../v18_50t_server.log
```

`run_on_server.sh` performs source verification and geometric unit tests, replays the authentic model, writes an independent output manifest and packs a **compact server sendback** in the parent directory. The transient nested genealogy is reconstructed within an automatically removed temporary directory; it is **not** included in the sendback. Do not edit the launcher to select Python: set `PYTHON_BIN` as shown.

Optional development checks:

```bash
python3.13 scripts/run_audit.py --preflight-only
python3.13 tests/test_projector_geometry.py
```

## Contents

- `scripts/run_audit.py` — executable scientific algorithm and original-solver staging
- `tests/test_projector_geometry.py` — independent analytic/projection controls
- `results/paired_kappa_same_phase_10d.csv` — common-ξ ledger
- `results/paired_kappa_event_aligned_gate.csv` — event-fraction comparison
- `results/paired_kappa_raw_chart_control.csv` — metric/chart sensitivity
- `results/report.json` — numerical results and limitations
- `results/*.png` — generated diagnostic figures, including a magnified micro-gap drift panel
- `inputs/*v18_50s*sendback.zip` — immutable genealogical input, with its own manifests
- `SOURCE_MANIFEST.json` / `SHA256SUMS_OUTPUT.json` — source and output integrity separated
- `SCIENTIFIC_REPORT.md` / `SCIENTIFIC_DECISION_RULES.md` — interpretation and falsification criteria

## Reproducibility scope

The authoring run replayed **two natural preparations and two short 10D integrations**, using the authentic Q550 model's analytic structural jet. Counterfactual Jacobian evaluations reused those sampled states. This audit does **not** sweep intermediate κ₀ values dynamically; a narrow activation *bandwidth* cannot be inferred from two endpoints alone.
