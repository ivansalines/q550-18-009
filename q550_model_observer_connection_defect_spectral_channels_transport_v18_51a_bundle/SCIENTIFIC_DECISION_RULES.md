# Decision rules — Q550 v18.51a

These rules are fixed independently of the observed curves.

1. **Authenticity:** read the exact v18.50z server sendback; demand correct ZIP CRC, source SHA-256 entries, and output SHA-256 entries. Preserve the parent ZIP unchanged.
2. **Comparable phase:** use the 79 sampled `xi` sections shared between the original-seed and autonomous-seed branches, at the **same midpoint κ0**. Never treat them as a sweep of κ0.
3. **Skew generator:** `W = K_model - K_canonical` must be real skew (relative symmetry residual below 2e-12).
4. **Channel identification:** SVD singular values of W occur in pairs. Track dominant rank-2 **projectors**, not signed SVD vectors. Require a gap σ1−σ2 greater than 0.5 for the top two individual pair channels; otherwise flag an unresolved combined cluster.
5. **Monotonic intensity:** declare sampled monotonic change only if the sign of all 78 adjacent increments agrees. Never infer a strict continuous monotonicity theorem from discrete samples.
6. **Pair-plane transport:** calculate principal angles with a sin-based stable estimator, independently for both planes, relative to their own initial projectors in the common chart.
7. **Inter-channel coupling:** record the magnitude `||Q2 Q1' Q1||F`, compare with total out-of-plane rate `||(I-Q1)Q1'Q1||F`. This measures **subspace motion**, not flow of energy or causal transfer between physical modes.
8. **Derivative controls:** compare `CubicSpline(xi,Q).derivative()` against a separate nonuniform three-point gradient. Differences reveal discretization sensitivity and are not rigorous continuous error estimates.
9. **Near-null warning:** do not track the third pair as a stable plane when σ3 is near 1e-9. A small singular intensity is not a certified rank/nullity or an independently identified material mode.
10. **Outcome classification:** report `NO_DOMINANCE_HANDOVER_WITH_MOVING_PLANES` when the main pair remains stronger, gains weight, and both pair projectors rotate; do not elevate the classification to energy exchange, holonomy, physical mode coupling or material memory without independent kinetic-metric and tangent-flow tests.
11. **Integrity separation:** immutable sources include a copy of the parent zip; outputs are regenerated with a distinct SHA-256 manifest. PNG byte differences caused by plotting versions do not by themselves negate numerical reproduction.
