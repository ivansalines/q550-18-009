# Q550 v18.50s — Principal-Angle Conditioning & Tangent-Integrator Convergence Audit

## Executive finding

The small subspace gap first reported in v18.50q is **resolved in the declared
numerical model and coordinate chart**, and the historical `arccos` estimator
is measurably less well conditioned than a sine-based calculation. This audit
does **not** establish a chart-independent material rotation or a rigorous
continuous-time error enclosure.

The authentic v18.50r server sendback was authenticated before the replay:
**11/11 source hashes and 6/6 result hashes match**, including the intact
v18.50q genealogy. The original physical 10D dynamics were re-staged and two
natural trajectories reconstructed, one for each κ₀.

## Numerical experiment

- Branches: original κ₀ = 1/6, autonomous κ₀ ≈ 0.16659961041764054.
- Event window: each branch's inherited *parity → stationary cancellation*
  interval, with ε = 10⁻⁴, in the common normalized observer metric.
- Observer: exactly the normalized 4D structural jet inherited from q;
  analytic Jacobian B, numerical sampled rank 3, seven-dimensional 10D kernel.
- Variational flow: genuine integration of the 10×10 fundamental matrix,
  using **analytic 10D tangent generator** extracted from the original 11D
  structural-Jacobian jet (the same structural construction verified in r).
- Solvers: DOP853 and Radau.
- Tolerances: rtol = 10⁻⁸, 10⁻¹⁰, 10⁻¹², atol = rtol/10.
- Step caps: Δξ/8 and Δξ/16.
- Total: 2 branches × 2 integrators × 3 tolerance levels × 2 step caps =
  **24 completed integrations**; all passed `success=True`, reached the
  required endpoint, and retained diagnostic evaluation counts.

## Principal-angle result

| Quantity | Original κ₀ | Autonomous κ₀ |
|---|---:|---:|
| Sine-based maximum principal angle (degrees), representative | 0.00215148933034 | 0.00215056688338 |
| Spread across 12 complete integrations per branch (degrees) | 2.52 × 10⁻¹⁵ | 3.46 × 10⁻¹⁵ |
| Maximum difference between two sine estimators | 2.77 × 10⁻¹⁶ | 1.44 × 10⁻¹⁶ |
| Maximum `arccos` vs `arcsin` angle difference (degrees) | 2.39 × 10⁻¹⁰ | 2.99 × 10⁻¹⁰ |
| Historical v18.50q `arccos` angle (degrees) | 0.00215148959944 | 0.00215056701261 |
| Smallest gap to historical q angle (degrees) | 2.69 × 10⁻¹⁰ | 1.29 × 10⁻¹⁰ |

The two sine formulations agree to near floating-point precision; both
integrators agree, and reducing the maximum permitted step changes the
sine-based angle by only a few 10⁻¹⁵ degrees in this particular short window.

**Interpretation:** the discrepancy between the historical q angle and the
sine-based angle is of the same order as the condition-dependent `arccos`
rounding discrepancy, and there is a minor generator difference (historical q
used numerical J10; this audit uses analytic J10). These influences are not
causally separated by the present data, so the whole difference must not be
attributed exclusively to `arccos`.

## What do invariant function-evaluation counts mean?

The counts remain constant when rtol decreases, but change substantially when
we halve `max_step`:

| Branch | DOP853 span/8 → span/16 | Radau span/8 → span/16 |
|---|---:|---:|
| Original | 110 → 194 | 65 → 114 |
| Autonomous | 98 → 194 | 58 → 114 |

Thus a prescribed step cap is exerting substantial control over both
integrators. **Repeated angle values under tighter tolerances are not by
themselves proof of solver error convergence.** The separate step-cap test is
necessary, and here it preserves the small angle.

The user's earlier scan reported a Radau run at rtol = 10⁻¹⁴ with only six
function evaluations, but did not include the solver's `success`, `status`,
`message`, or final time. **That row cannot be accepted as a completed replay
without those checks.** This version's default 24-run grid does not include
that extreme tolerance; a separately requested stress test is supported by
`--tolerances` and the runner records endpoint status and SciPy warnings.

## Why a sine-based diagnostic is preferable

For orthonormal 10×7 bases K and Q and corresponding projectors P=KKᵀ and
P_Q=QQᵀ, the largest principal angle obeys

```math
sin(theta_max) = ||(I-P) Q||_2 = ||P-P_Q||_2,
cos(theta_max) = sigma_min(K^T Q).
```

Close to parallel subspaces, `cos(theta_max)` is close to unity. An absolute
rounding perturbation in the overlap singular value is then magnified by the
slope of `arccos`. The sine-based calculation operates on a quantity of the
same order as the sought small angle. The projector route offers a
basis-invariant cross-check of the calculation.

## What is and is not established

**Supported:** the inherited 10D chart exhibits a repeatable nonzero
principal-angle separation between an analytically defined instantaneous
kernel and a kernel transported by the analytic tangent generator, across the
specified solver and step-cap grid. This is compatible with the differential
kernel defect analyzed in r.

**Not supported:** an interval-certified lower bound on the true continuous
angle, a physically privileged state-space metric, a unique 10D material
connection, a torsional flip, material memory, stress overshoot or any
constitutive equivalence with metallic/polymer glasses.

The inherited event times are numerical estimates. Their own uncertainties,
plus possible errors in reconstructing the natural driven trajectory, are not
bounded by this tangent-integrator convergence scan.

## Reproducibility

`scripts/run_audit.py` is the actual generator of the CSV, JSON and PNG output;
`tests/test_angle_conditioning.py` checks known angles and invariance under a
change of orthonormal basis; `SOURCE_MANIFEST.json` binds immutable source
files and the exact parent r sendback; `SHA256SUMS_OUTPUT.json` records
regenerated outputs independently. Runtime extraction is temporary; the
sendback does not include the 1.4+ GB nested genealogy workspace.

Classification:
`INHERITED_CHART_NUMERICAL_PRINCIPAL_ANGLE_INTEGRATOR_CONVERGENCE_NOT_MATERIAL_CERTIFICATE`.
