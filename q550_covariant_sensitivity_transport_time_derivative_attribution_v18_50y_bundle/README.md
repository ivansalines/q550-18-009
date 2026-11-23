# Q550 v18.50y — Covariant Sensitivity Transport & Time-Derivative Attribution Audit

This audit follows the full **matrix-valued κ response** of the rank-three structural observer's 7D kernel, using the **authenticated server sendback of v18.50x**. Its central distinction is between `A = ∂ξE` in the inherited common 10D chart and the change relative to a **canonical horizontal frame that transports the observed kernel**. The connection is not chosen to follow E. It is nonetheless derived from the observed projector, **not an independently derived physical material connection**.

## Inputs and reproducibility

- `inputs/q550_anchor_free_kappa_differential_response_moving_sensitivity_geometry_v18_50x_bundle_server_sendback.zip`: authentic parent, including 44 successful 10D IVPs, the original `P`, `E`, and `A` tensor arrays; verify all 12 source hashes and 11 output hashes before use.
- 22 κ samples, 79 turn-relative ξ sections, 2 fixed natural seeds, 3,476 tensor samples. No new Q550 10D IVPs are required.
- 6 *geometric orthogonal-frame* ODE integrations for offsets 0, 0.5 and 1, in each seed. These are NOT physical replays.
- Time derivatives re-estimated from the inherited matrices with cubic splines; independent nonuniform five-node polynomial stencils quantify sensitivity to interpolation.
- `SOURCE_MANIFEST.json` is immutable. `SHA256SUMS_OUTPUT.json` is regenerated after each run. Image encoding/library version changes can legitimately change output hashes.

## Mathematics

For the 10×10 orthogonal projector `P(κ,ξ)` and its κ derivative `E=∂κP`, define

\[
K=[\dot P,P],\quad \dot P=[K,P],\qquad
D_\xi E=\dot E-[K,E].
\]

`K` is skew symmetric. The connection follows only the motion of `P`, and yields a metric-preserving orthogonal frame `U'=KU`. Thus `Uᵀ E U` is the κ-response tensor seen in this **kernel-parallel frame**. The Frobenius growth rate of `||E||` is identical before and after correction, while the direction-changing rate need not be.

Under a moving invertible coordinate change `S(ξ)`, transport **both** `E -> S E S⁻¹`, `K -> S K S⁻¹ + S' S⁻¹` and `G -> S⁻ᵀ G S⁻¹`. The audit uses an explicit nonorthogonal gauge and checks invariant inner products. Computing `[P',P]` *anew* in transformed coordinates, with no information about the moving frame, is not equivalent in general.

## Server command

```bash
cd /root/elab1/hysteresis
unzip q550_covariant_sensitivity_transport_time_derivative_attribution_v18_50y_bundle.zip
cd q550_covariant_sensitivity_transport_time_derivative_attribution_v18_50y_bundle
set -o pipefail
PYTHON_BIN=python3.13 bash run_on_server.sh \
  2>&1 | tee ../v18_50y_server.log
```

The script itself verifies the input, runs synthetic tests and the audit, verifies the produced data, writes the output manifest and packages `../q550_covariant_sensitivity_transport_time_derivative_attribution_v18_50y_bundle_server_sendback.zip`. No nested runtime genealogy is unpacked, and no generated console log is placed inside the manifest-checked bundle.

## Outputs

- `results/report.json`: computed numerical checks, exact classifications, environment and limitations.
- `results/covariant_kappa_sensitivity_ledger.csv`: all 3,476 tensor-derived rates.
- `results/transported_sensitivity_angles.csv`: raw and kernel-frame-corrected angles at all sampled ξ for six chosen (seed, κ) paths.
- `results/observer_coordinate_gauge_controls.csv`: explicit nonorthogonal gauge checks.
- `results/transported_sensitivity_centerline_tensors.npz`: centerline `E`, `DξE`, `K`, transported `E`, and `U` for independent subsequent work.
- Three diagnostic PNG charts and separate source/output SHA-256 manifests.

## Interpretation

This is an **observer-projector, finite-grid transport diagnostic**. The corrected angle is neither a proven physical rotation nor a gauge-universal scalar absent a declared connection and metric. It does not establish a material edge, narrow-band activator, or torsional flip. A separate, physically grounded 10D generator/metric comparison remains open.
