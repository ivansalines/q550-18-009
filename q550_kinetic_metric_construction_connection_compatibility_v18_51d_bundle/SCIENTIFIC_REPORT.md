# Q550 v18.51d — Kinetic-Metric Construction & Connection Compatibility Audit

## The first piece is a construction, not an audit

The original historical v18.49h source (`reference/kinetic_metric_v18_49h.py`, exact SHA-256 `29bef2c91899a9da46bc8c9159b89c70362f505e0adead3f814c487a9a17bb1a`) already derives Q550's tau-time kinetic state immersion from its authentic kinetic energy. The 5D configuration immersion `Q` satisfies `T = ||V||²/2`, and the declared 10D material state immersion is `H=(Q,tau_ref V)`. The new metric in the inherited shared 10D observer chart is the exact pullback `G=(DH diag(shared_scale))^T(DH diag(shared_scale))`. See `KINETIC_METRIC_DERIVATION.md` for the derivation and the substantial convention dependence of `tau_ref`.

The induced flat Levi-Civita connection in the inherited chart along the actual trajectory is `Gamma=L^-1 Lprime`, where `L=DH diag(shared_scale)`. It is compatible with `G` by construction. This is not the assertion that the Q550 flow preserves `G`, nor that there is a unique physical metric on phase space.

## The audit: reconstruction and measured results

The parent is the authenticated v18.51c server sendback (with inherited v18.51b → a → v18.50z → y → x genealogy); original Q550 physical seed states are recomputed at the **same midpoint κ₀** for two independently prepared seed families. There are **two new Q550 10D driven IVPs**, 79 sections per seed, and three kinetic state-weight conventions `tau_ref=0.5,1,2`, yielding **474 measured sections**. These are not two concurrent distinct-κ₀ boundaries.

The historic b attribution was made from the fixed-Euclidean skew defect `W=K_model-K_canonical`. The present audit maps this same defect into physical Cartesian kinetic coordinates, `A=L W L^-1`, and studies `skew(A)`. The rate is decomposed without suppressing the moving material frame:

`d[skew(A)]/dξ = skew(L Wprime L^-1) + skew([Lprime L^-1, A])`.

The first term preserves the three inherited *algebraic* b source categories (model-generator drift, projector posture, minus canonical-observer drift). The second term is a separately recorded kinetic-frame contribution. The spectral planes are selected using the leading isolated rank-two eigenspaces of `-skew(A)^2`; signed percentages derive from the interplane spectral-gap identity. They are **not** energy transfer fractions.

### Original seed — signed spectral interplane attribution

| Metric convention | Canonical start | Canonical end | Model end | Kinetic-frame end |
|---|---:|---:|---:|---:|
| Historical Euclidean v18.51c | 73.72% | 79.87% | 20.13% | not present |
| Kinetic tau_ref=0.5 | 141.53% | **30.41%** | −36.89% | +106.48% |
| Kinetic tau_ref=1 | 136.51% | **50.54%** | −111.65% | +161.12% |
| Kinetic tau_ref=2 | 98.42% | **86.39%** | −166.29% | +179.90% |

Rows including a frame contribution sum to approximately 100%; individual signed fractions can be negative or over 100% because of cancellation and need not sum in absolute value to 100%. The autonomous seed shows the same qualitative behavior but distinct numbers (see the CSV and JSON).

**Decision:** the *increasing* canonical-share pattern seen in the Euclidean/Jacobian-Gram metrics of v18.51c is **not retained** in the historical kinetic state-metric family. Its share **decreases** over the measured interval for each declared `tau_ref`. The dominance hierarchy is now source-convention dependent; the metric-frame contribution is very large at the endpoint and must not be suppressed. Therefore the v18.51c tested-family robustness must not be presented as physical metric invariance.

### Kinetic spectral structure and conditioning

The kinetic Cartesian analysis reveals appreciable higher spectral pairs: the maximum third singular strength is approximately 2.01, 3.08 and 4.82 for tau_ref=0.5,1,2 respectively, unlike the near-zero third mode in the original Euclidean chart. The first and second paired spectral eigenprojectors remain isolated within this scan. Maximum metric condition numbers lie between roughly 6.2×10³ and 1.02×10⁴ across the six branches; these are finite but emphasize that this is **not a numerically innocuous metric change**.

### Authenticity and controls

All 12 declared scientific controls passed in the local replay:

- Source archives v18.51c/b/a and v18.50z/y/x verified by SHA-256; byte-exact historic kinetic-source hash checked.
- Original model 10D analytic tangent jet replay max relative mismatch ~`7.10e-16`.
- Kinetic Cartesian energy reconstruction max relative mismatch ~`2.22e-16`.
- Metric-connection compatibility residual max ~`1.41e-14`.
- Independent kinetic-frame derivative check max relative mismatch ~`1.10e-7`; independent metric-rate check max ~`1.82e-8`.
- Passive nonorthogonal chart control, source accounting and spectral fraction sum checks passed.

These results are local numerical consistency tests, not interval-valued mathematical certificates. The log, machine-specific checks, exact endpoint shares and environmental information appear in `results/report.json`.

## Scientific interpretation

The metric derived from Q550 kinetic energy provides a **better physically motivated geometric comparison than an arbitrary Jacobian Gram**. But it still inherits a freely specified phase-state position/velocity relative scale (`tau_ref`). The material-state immersion is a metric construction, not a conserved dynamical quantity, and the connection is its geometric pullback, not a newly discovered material flow law. The metric-skew projection excludes symmetric strain and does not measure physical energies or stress. The inherited full Q550 dynamics has not been shown to be an isometry of this metric.

**Outcome:** the elementary kinetic construction is recovered, the compatible state connection is demonstrated, and the earlier signed spectral source attribution is found to be **sensitive to the material state metric convention**. The absence of a unique certified material metric remains explicit. A sensible next comparison would test the full `L J10 L^-1 + Lprime L^-1` generator including **symmetric stretch**, rather than only its kinetic-skew part, and check tau_ref sensitivity and finite-time material Cauchy–Green transport.

## Limitations

No Q550 material torsion, intrinsic κ₀-band activation, universal canonical dominance, hysteretic memory or observer-independent kinetic-energy transfer is established. The result is one well-specified physically motivated **construction-plus-audit** with three deliberately different material-state scale conventions; it does not replace a Lagrangian variational derivation of a unique phase-space geometry.
