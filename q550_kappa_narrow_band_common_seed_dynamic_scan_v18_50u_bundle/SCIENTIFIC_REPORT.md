# Q550 v18.50u — Narrow-κ₀ Band & Fixed-Seed Driven Projector Scan

## Scientific status

**Classification: `CONTROLLED_COMMON_SEED_PARAMETER_SCAN_NOT_DYNAMIC_ACTIVATION_CERTIFICATE`.**

The genuine v18.50t server sendback authenticates as **11/11 source files and 8/8 output files**; the original Q550 10D model and normalized structural observer were recovered through the documented nested genealogy. This audit integrates new physical 10D driven trajectories across 15 values of κ₀, using **two fixed previously prepared seed states** and their respective prescribed drive clocks. Each parameter value is compared to the matching reference within the same seed family.

The data **do not support a narrow isolated activation band in the measured projector response** over the scanned κ₀ region and short evolution window. They do support a smooth, distinguishable, parameter-sensitive 7D observer nullspace geometry, with small but nonzero state-trajectory effects.

## Historical endpoints and sweep

- κ_auto = 0.16659961041764054
- κ_orig = 0.16666666666666666
- Δκ = 0.00006705624902611507
- Normalized offsets `(κ−κ_auto)/Δκ`: −2, −1, −0.5, 0, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875, 1, 1.5, 2, 3.
- Time/turn-relative window: ξ ∈ [0, 0.001092], sampled at 21 positions.

Totals: **28 new driven 10D IVPs** plus the two re-used natural reference IVPs from the authentic model staging, 13,916 evaluations of the newly integrated RHS, **630 recorded vector-projection rows**, and **588 parameter-secant measurements**. All parameter IVPs succeeded and reached the requested final time.

The same seeded state and imposed clock were used for each κ variant within a seed family. The two seed families were prepared independently; this audit does not claim equal initial physical states across those families.

## Model-relative geometric measurements

At the **midpoint of the historical parameter interval** (offset 0.5) and final time ξ = 0.001092, distances from the seed-specific reference are:

| Quantity (operator norm) | Original seed | Autonomous seed |
|---|---:|---:|
| Full `||P(y_κ,κ)−P(y_ref,κ_ref)||₂` | 9.05779037e−05 | 9.05919781e−05 |
| Parameter-only, same state | 9.05198118e−05 | 9.05338654e−05 |
| Changed-state contribution, same κ | 1.52806060e−07 | 1.52841905e−07 |
| State-only / full (ratio of norms) | 0.16870% | 0.16871% |

These three operator norms are **not** additive. The underlying operator identity is exact:

`ΔP_total = ΔP_parameter_at_reference_state + ΔP_new_trajectory_at_same_parameter`.

The maximum arithmetic closure residual of this matrix identity was 0 in the stored calculation. The minimum strong third singular value of the analytic observer Jacobian was 0.487047, and its largest fourth singular value was 7.53e−14: the expected rank-three normalized observer structure persists across the scan.

## Narrow-band screen: negative result under the chosen observable

At the final section, the absolute scalar secant slope of `||P_κ−P_seed_anchor||₂` changes by approximately **0.0905%** across the entire parameter scan for each fixed seed:

- Original seed: minimum 2.700479, maximum 2.702926.
- Autonomous seed: minimum 2.700593, maximum 2.703041.

There are **zero interior local peaks** satisfying the predeclared criterion of at least 20% excess over the outer control flanks (evaluated separately for each fixed seed). The very weak variation is compatible with an almost smooth linear local parameter response. The two κ endpoints do not define edges of an *active* band under this observable.

A distance-to-anchor function naturally vanishes at the anchor and grows to either side. Its corresponding V-shape, and the mere existence of two nearby responses, are not activation evidence. The screen is intentionally conservative and is not a detector of every possible nonlinear effect.

## Interpretation and next discriminator

The v18.50t compensation between parameter-only and preparation-related changes occurs when comparing **different natural preparations**. The v18.50u scan eliminates that preparation difference *within each seed family*; it finds a smooth response and a much smaller changed-state component on the short window. The two findings do not contradict one another because they ask different questions.

A credible *dynamic activation band* would require an independently motivated response quantity (e.g. long-time growth rate, robust sign change, return/branch condition, or defined energy/strain threshold), plus κ-dependent natural-state continuation or a wider driven evolution; then define the activation threshold and width **before** looking at peak locations. The short projector-gap scan alone cannot certify or rule out all such bands.

## Reliability and limitations

- Strictly source-and-output authenticated v18.50t parent; Python 3.13-compatible launch path, separate source/output SHA-256, and the generated sendback excludes temporary genealogy.
- The 10D IVPs are genuine, but each scan changes κ from a *fixed historic initial seed* rather than producing a new natural orbit at every κ.
- The metric is a declared **shared diagonal chart**, not a certified material kinetic metric.
- All observed nullspaces are seven-dimensional **observer** nullspaces; no material invariant or torsional flip is inferred.
- Fifteen κ samples and 21 time samples over a short interval do not exclude very narrow features between samples or features of other physical response variables.
- A direct comparison to constitutive polymer/metallic glass laws would require defining corresponding physical stress/strain observables first.
