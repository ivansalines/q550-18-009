# Q550 v18.51n — Scientific report (local replay)

## Principal distinction

The kinetic-energy velocity Hessian is a model-grounded, positive-definite **configuration** metric. Its numerical finite-difference reconstruction matches the historic source to within approximately `1.02e-8` relative (32 independent regular configurations). This does not select a unique ten-dimensional metric on material state space, certify an unforced natural Lagrangian, or uniquely identify generalized forces for the driven Q550 equations.

## Window stress test on the unchanged physical transport

The inherited v18.51m reversal is not merely an artifact of its bilateral Gaussian window. On the authenticated 79-section material histories (two seeds), the **position-output, 0.025 bandwidth, raw well-resolved** windows yielded:

| Window | Well-resolved measurements (instantaneous + finite lag) | 5→4 greater | 4→5 greater |
|---|---:|---:|---:|
| Past-only (no future output) | 386 | 0 | 386 |
| Future-only predictive | 570 | 0 | 570 |
| Bilateral | 610 | 0 | 610 |

These numbers include both seeds and reflect the declared span/conditioning filter. With a small declared ridge regularization `epsilon=1e-5` all three protocols include 610 measures, all with `4→5` greater. The ridge is a measurement choice, **not** evidence that the near-origin past Gram is well determined. The initial/final one-sided windows have limited support and are not counted as raw well-resolved without the filter.

The inherited kinetic metric gives the opposite ordering on the same operator blocks. Thus the operational reversal survives the observation-window challenge, but **the norm direction remains metric-dependent**, and none of these 610 comparisons demonstrate physical motion reversing in time. The original bilateral Gaussian v18.51m ratios agree with independent 64-node quadrature to about `8.36e-6` absolute (two independent quadrature protocols).

## Genuine mathematical result versus open inverse-variational task

The historic kinetic energy yields the exact algebraic mass Hessian
`diag(rho1²,rho1²,rho2²,rho2²,m_x[x(1-x)]²)`. This identity and its SPD domain are mathematical consequences of the declared energy. A **full variational admissibility judgment** remains open because the complete driven dynamics, generalized forces and clock reparameterization have not been reconstructed from an action. A formal diagnostic against the much narrower unforced Cartesian ansatz is recorded, without treating it as a no-go theorem.

## Limitations

All window metrics use cubic interpolation of authenticated frozen material tangent maps, not new physical ODE integrations; 64-point Gaussian quadrature is not interval arithmetic. The raw-window conditioning criteria and ridge strengths are declared numerical diagnostics, not canonical thresholds. A small or narrow causal window can be uninformative even when a ridge makes its Gram positive definite. No 10D variational uniqueness, observer-independent physical directionality, Q550 intrinsic torsion, material hysteresis or temporal irreversibility is established.
