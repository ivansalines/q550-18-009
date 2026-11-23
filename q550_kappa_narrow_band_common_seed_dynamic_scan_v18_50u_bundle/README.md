# Q550 — v18.50u Narrow-κ₀ Band & Fixed-Seed Driven Projector Scan

This audit tests the *hypothesis* of a narrow dynamical activation band between the two historically inherited κ₀ values. It does not presume that either historical value is a physical band edge.

## Inputs and provenance

`inputs/q550_paired_kappa_phase_aligned_edge_motion_projector_separation_v18_50t_bundle_server_sendback.zip` is the immutable, authenticated v18.50t server parent. The nested provenance is validated and the same Q550 physical 10D RHS / analytic observer chain is reconstructed. Two historical natural turning preparations (original and autonomous) are recovered once; the parameter sweep then runs fresh driven IVPs from each **fixed** seed. This means the sweep is controlled for initial state preparation *within each seed family*, but does not re-prepare a natural orbit for every κ₀.

Historical parameter endpoints:

- κ_auto = 0.16659961041764054
- κ_orig = 0.16666666666666666
- Δκ = κ_orig − κ_auto ≈ 6.705624902612×10⁻⁵

The scan includes κ values both within and outside `[κ_auto, κ_orig]`. See the JSON report for all offsets and the actual numeric values.

## Scope of the measurement

For every κ and each of the two fixed seeds, the actual driven Q550 10D equations are integrated over the same short turn-relative evolution window `0 ≤ ξ ≤ 0.001092`. The same prescribed drive phase is used for all variants within a seed family. The normalized analytic 4D observer Jacobian is computed in one shared 10D state chart; its seven-dimensional nullspace projector `P_κ(ξ)` is compared with the matching fixed-seed reference projector `P_ref(ξ)`.

The exact operator decomposition is

`P(y_κ,κ) − P(y_ref,κ_ref) = [P(y_ref,κ) − P(y_ref,κ_ref)] + [P(y_κ,κ) − P(y_ref,κ)]`.

The first term isolates parameter changes at the same state (no replay); the second term isolates dynamical state change under the perturbed κ. Norms of the summands are **not** additive.

## Reproduction on server

```bash
cd /root/elab1/hysteresis
unzip q550_kappa_narrow_band_common_seed_dynamic_scan_v18_50u_bundle.zip
cd q550_kappa_narrow_band_common_seed_dynamic_scan_v18_50u_bundle
set -o pipefail
PYTHON_BIN=python3.13 bash run_on_server.sh 2>&1 | tee ../v18_50u_server.log
```

Do not modify `run_on_server.sh`: set the interpreter using `PYTHON_BIN` to preserve the source manifest. The extracted ancestor runtime tree is created in an automatic temporary directory and excluded from the sendback.

## Outputs

- `results/fixed_seed_kappa_dynamic_scan.csv`: dynamic and instantaneous parameter-only projector gaps across κ and ξ, plus exact operator decomposition residual.
- `results/kappa_secant_response_screen.csv`: finite secant slope of *distance to a fixed anchor* (screening only, **not** an invariant constitutive response function).
- `results/*.png`: original plots from the numerical audit.
- `results/report.json`: full sample counts, predeclared decision rules and limitations.
- `SCIENTIFIC_REPORT.md`: interpretation, including negative evidence if present.

The archive contains the actual source scripts and the immutable parent ZIP; SHA-256 manifests for source and regenerated outputs are separate. Files under temporary runtime trees are not included in the sendback. All scripts/docs/comments are in English.
