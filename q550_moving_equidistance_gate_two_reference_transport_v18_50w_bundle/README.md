# Q550 v18.50w — Moving Equidistance Gate & Two-Reference Transport Audit

This executable bundle follows the equidistance root of the two κ₀-anchored response profiles. It asks **where a reference-relative crossing moves** as the driven motion proceeds. An anchored V-shaped profile necessarily has a zero at its own anchor; that zero **is not** a newly discovered physical constraint.

The `v18.50v` authentic server sendback is included as a ZIP inside `inputs/`. Its contained `v18.50u` sendback is authenticated directly in memory. **No new Q550 integrations** are performed: this is a transparent post-processing of the parent model’s 44 genuine physical 10D integrations and 3,476 archived κ–ξ measurements. The nested genealogy is not extracted on disk.

## Command (Python 3.13)

```bash
cd /root/elab1/hysteresis
unzip q550_moving_equidistance_gate_two_reference_transport_v18_50w_bundle.zip
cd q550_moving_equidistance_gate_two_reference_transport_v18_50w_bundle
set -o pipefail
PYTHON_BIN=python3.13 bash run_on_server.sh 2>&1 | tee ../v18_50w_server.log
```

The script checks the original SOURCE_MANIFEST, authenticates the v/u parent ZIPs, recomputes every result, tests geometric and data controls, writes a new output checksum manifest, and creates `../q550_moving_equidistance_gate_two_reference_transport_v18_50w_bundle_server_sendback.zip` without copying intermediate runtimes.

## Core definition

For each response observable `m`, compute independently for each seed family its anchored distance `D_auto^m(κ,ξ)` or `D_orig^m(κ,ξ)` on the same numeric response chart. Define:

`F_m(κ,ξ)=D_auto^m(κ,ξ)-D_orig^m(κ,ξ)`.

A sign-changing bracket between the two historic κ anchors determines a crossing `κ*_m(ξ)` by monotone PCHIP interpolation in κ. Its speed is measured by `dκ*/dξ=−(∂ξ F_m)/(∂κ F_m)` when the derivative is nonzero. This is an **operational marker attached to the two chosen reference distances**, not a material gate.

The v18.50v data are sampled in the two preparations at their own turning events; equal relative ξ does not mean a common absolute clock. Four independent distance definitions are tracked: 7D projector (operator norm), structural normalized observer, driven RHS and 10D state displacement. The latter is undefined at ξ=0, when both state-displacement profiles are identically zero.

Interpolation robustness checks use linear secant, unconstrained cubic, and PCHIP without the exact center point, and independently compare the overlapping early u/v measurements. Raw signed profiles and every crossing/velocity are archived, including any failure of uniqueness or sign-change bracketing.

## Results

- `results/equidistance_gate_time_ledger.csv`: phase, crossing for each observable, bracket, implicit velocity and status.
- `results/signed_projector_distance_profiles.csv`: *raw* signed projector gap at all 22 κ and 79 ξ.
- `results/u_v_short_window_comparison.csv`: independent v18.50u-v18.50v cross-checks at ξ=0 and 0.001092.
- `results/report.json`: actual values, numerical method, parent digests and all limitations.
- `results/moving_gate_observable_comparison.png`, `equidistance_gate_drift.png`, `signed_anchor_gap_crossings.png`: plots.

See `SCIENTIFIC_DECISION_RULES.md` for the interpretation and `SCIENTIFIC_REPORT.md` for the authoring-run findings. Scripts and all methodological comments are in English.
