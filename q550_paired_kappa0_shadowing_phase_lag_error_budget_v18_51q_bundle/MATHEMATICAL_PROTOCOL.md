# Q550 v18.51q — Mathematical protocol

## Authentic ancestry and independent physical IVPs

The immutable v18.51p server-sendback ZIP is the parent. Its SOURCE_MANIFEST and SHA256SUMS_OUTPUT are checked byte-for-byte, and its own historical v18.51o → ... → v18.50w chain is re-authenticated by the exact v18.51p replay code. The original v18.50x nonlinear 10D driven RHS, genuine natural seed preparations and forcing clock are staged **without replacing the equations**.

The parameters are read from the authenticated v18.50x report, not fitted:

- `kappa_original = 1/6`;
- `kappa_autonomous = 0.16659961041764054` (historical autonomous construction);
- `kappa_midpoint = (kappa_original + kappa_autonomous)/2`, used **only** to check parameter nonlinearity.

For each of the two **independently prepared seeds**, integrate all three parameter values to the common event-relative time `0 <= xi <= 0.05`. This 2x3 factorial is crucial: comparing only the original seed at original kappa to the autonomous seed at autonomous kappa confounds parameter effects and initial-condition effects. The original driving protocol remains the historical `beta:2:2` ramp implemented by the authenticated solver.

Run DOP853 twice per physical branch: a standard tolerance/step budget and a tighter reference budget. `max_step` is halved in the latter. The difference is a **numerical resolution probe**, not a certified upper bound on integration error.

## State, clock and phase diagnostics

The authentic historical kinetic immersion defines five Cartesian positions `Q` and their tau-time velocities `V`. The nonlinear clock `c(y,xi)` is recovered from the authentic RHS, with `Q_xi = c V`; its cumulative material-time parameter is

\[
\tau(\xi)-\tau(0)=\int_0^\xi c(y(u),u)\,du.
\]

For fixed seed `s` and the two historical parameters, define `delta Q_s = Q_s(kappa_original) - Q_s(kappa_autonomous)` and analogously for `V`, `tau`, and the two internal polar angles. Report the raw difference, not a normalization designed to force a positive answer.

The **local phase-equivalent xi lag** is the orthogonal projection of `delta Q` on the physical velocity of the autonomous-parameter reference trajectory:

\[
\ell_s=\frac{\langle\delta Q_s,Q'_{s,-}\rangle}{\|Q'_{s,-}\|^2}, \qquad
r_{\perp,s}=\delta Q_s-\ell_s Q'_{s,-}.
\]

The residual fraction `||r_perp|| / ||delta Q||` is reported independently of the local lag. This is a **first-order local projection**, not an optimized global time correspondence, an orbit conjugacy or a demonstration of phase locking. The two polar-angle differences are also retained as independent phase diagnostics. The phase projection identity is tested with the independently evaluated `Q' = DQ(y) RHS(y,xi)`.

The midpoint defect

\[
Q(k_+) + Q(k_-) - 2Q((k_++k_-)/2)
\]

checks nonlinear dependence on the control parameter. Small residuals should be interpreted in light of the very small `delta kappa`.

## Numerical error budget and limits

For each parameter branch, compare standard and reference solutions at identical `xi` grid points. For the pair, add the two discrepancies as a **numerical proxy** and combine with an explicit floating-point resolution floor. A section is labeled `resolved_factor20` only when its `||delta Q||` exceeds 20 times that proxy. Such a label is an operational numerical decision, **not** an a posteriori validated ODE error estimate. Near `xi=0`, both kappa variants begin at the exact same state and the parameter separation necessarily vanishes.

Both seeds, all kappa branches, the accumulated clock, phase decomposition and numerical proxies are stored as CSV plus raw tensors in NPZ. No interval analysis, long-time orbital shadowing, topological conjugacy, hysteresis, or independently flowing simultaneous kappa-boundaries are established.
