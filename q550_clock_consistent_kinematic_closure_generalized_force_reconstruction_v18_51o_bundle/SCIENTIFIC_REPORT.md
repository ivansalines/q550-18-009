# Q550 v18.51o — Scientific report (local replay)

## Classification

**NUMERICAL_AUTHENTIC_FROZEN_TANGENT_SECOND_ORDER_CLOSURE_EFFECTIVE_FORCE_JACOBIAN_ONLY**

The original and autonomous historical preparations have been audited at the same inherited Q550 midpoint-κ setting. The physical full 10D material-state and tangent IVPs belong to the authenticated ancestor v18.51e. The new v18.51o run constructs a second-order tangent representation **without rerunning the physical solver** or assuming a unique kinetic phase-space metric.

## Key measured distinction: not merely a scalar clock

The Cartesian kinetic 10D tangent generator has a position–velocity block `K=alpha(xi)*I5` to within maximum Frobenius residual `1.94e-15`, but its position–position block `A` is nonzero. Its first four columns are nearly zero (largest Frobenius residual `5.05e-10`), while the fifth-column coupling remains substantial (`||A||` at the final section approximately `2.84188`). The kinematic equation in perturbations is therefore `delta Qprime=A delta Q+alpha delta W_tau`.

For `tau_ref=1`, the effective velocity sensitivity varies from roughly `alpha=1.6736334` to `1.6737296` on the inherited interval. The same physical tangent representation with `tau_ref=0.5` and `2` rescales alpha by the reciprocal reference weight. Thus alpha is a **tangent sensitivity**, and the observed nonzero A must not be erased when discussing a possible physical clock reparameterization.

## Correct second-order linearized closure

With `delta U=delta Qprime`, a time-dependent coordinate transformation produces `delta Qsecond=E delta Q+F delta Qprime`. This is exact for the specified frozen linearized first-order system when its continuously differentiable coefficients are known; in this audit the derivatives are evaluated by splines of authenticated sampled tensors.

At the end of the local interval for the original seed and `tau_ref=1`:

| Measured diagnostic | Value |
|---|---:|
| `||A||` | `2.84188068` |
| `||E||` | `11.31488078` |
| `||F||` | `2.97047526` |
| `||E-E.T||/||E||` | `0.59148759` |

The autonomous seed is close but not identical. The nonzero velocity Jacobian and nonsymmetric position Jacobian prevent identification with the **narrow** fixed-Cartesian, unforced natural xi-time Lagrangian `L=0.5||Qprime||²-U(Q,xi)`. They do **not** rule out more general forced, driven, velocity-dependent, time-dependent or time-reparameterized variational formulations.

## Numerical controls

**19/19 scientific gates passed** in the local replay. Source chain authentication verifies the v18.51n sendback and nested v18.51m/l/k/j/i/h/g/f/e results and source manifests, with byte-exact historical v18.49h kinetic source.

- Maximum identity residual of the time-dependent second-order generator transform: `2.86e-16`.
- Maximum independently spline-differentiated finite-time `delta Qprime` residual: `7.49e-09`.
- Maximum independent second-derivative finite-time tangent residual: `9.44e-06`; the larger error reflects the more sensitive numerical second derivative.
- Cross-`tau_ref` relative disagreement in the effective acceleration Jacobians `(E,F)`: `2.65e-12`.
- Cross-`tau_ref` effective sensitivity scaling disagreement: `6.34e-17`.
- Passive nonorthogonal GL(5) configuration-chart covariance error: `2.11e-16`.
- Three synthetic independent controls pass: changing-clock-only, quadratic potential and driven drift/damping.

## What is — and is not — reconstructed

The **linearized effective acceleration-force Jacobian**, `(E,F)`, is reconstructed and numerically checked on the inherited trajectory: `delta f_eff=E delta Q+F delta Qprime`. The zeroth-order force `f_eff(Q_*(xi),Qprime_*(xi),xi)` is **not** recoverable from the propagator alone. Neither the absolute nonlinear generalized-force field nor an original action has been derived. A separate solver-level audit must replay the actual physical trajectory and independently identify the clock, moving-chart drift and generalized forces before testing Euler–Lagrange or Helmholtz constraints.

No material torsion, phase-space metric uniqueness, hysteretic memory or direction-independent physical-energy-transfer law is certified by this work.
