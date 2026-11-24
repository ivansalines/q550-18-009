# Q550 v18.51p — Physical Clock, Moving-Frame Drift & Absolute Generalized-Force Reconstruction Audit

## Status and classification

**AUTHENTIC_NONLINEAR_CLOCK_AND_ON_TRAJECTORY_KINETIC_FORCE_CONSTRUCTION_WITH_VARIATIONAL_LIMITATIONS**

The full local replay completed **18/18 scientific controls**. Both genuine Q550 10D nonlinear driven IVPs were integrated from the authenticated *independent original and autonomous turning seeds* at the same inherited midpoint `kappa=0.1666331385421536` with the authentic v18.50x/v18.50v physical solver. Each physical IVP required 602 RHS evaluations; 79 sections from `xi=0` through `xi=0.05` were evaluated for each seed. The authenticated v18.51o → ... → v18.50w source genealogy was checked, plus the unchanged v18.49h kinetic immersion.

The first part is a nonlinear **construction**; the later finite-difference, tangent, and kinetic-identity comparisons are **audits**.

## 1. An authentic state-dependent clock

The five nonlinear configuration equations obey the same scalar clock equation along both historical trajectories,

`qprime(xi) = c(y,xi) * u`, with `q=(log rho1,theta1,log rho2,theta2,logit x)` and `u=(v1,omega1,v2,omega2,vz)`.

| Measured quantity | Original | Autonomous |
|---|---:|---:|
| `c` at `xi=0` | 1.673633419432747 | 1.673633064005971 |
| `c` at `xi=0.05` | 1.673729634156072 | 1.673729281137374 |
| Material `tau` increment over observed interval | 0.083683298394394 | 0.083683280662162 |
| Maximum physical Cartesian `Qprime-cV` norm | 8.92e-16 | 6.74e-16 |
| Maximum velocity-gradient magnitude of `c` in Cartesian `(Q,V)` | 2.38e-10 | 2.88e-10 |

The clock is not merely an external `tau(xi)` imposed equally on every perturbed trajectory. Its measured physical configuration gradient at the endpoint has a fifth component `d c/d Q5 ≈ -3.31775`, with all first four components near the numerical differentiation floor. Along each particular trajectory, the clock integrates to a well-defined accumulated material time. **A common global time coordinate for all nearby states is not established.**

## 2. The historical fifth-column tangent coupling is reconstructed from the clock

From `Qprime = c(Q,V,xi)*V`, the independently computed nonlinear clock gradient produces the complete first block row of the original kinetic Cartesian tangent generator:

`A_clock = V ⊗ grad_Q(c)` and `K_clock = c*I + V ⊗ grad_V(c)`.

The maximum relative discrepancy between this independently reconstructed `A_clock` and the authenticated v18.51e `B_QQ` block is **1.781e-10**; the corresponding `K_clock` error is at most **6.603e-11**. The nontrivial approximately rank-one position block seen in v18.51o therefore has a demonstrated **state-dependent clock contribution**, rather than requiring an additional torsional force for its explanation. This does not establish a material torsion law.

## 3. Absolute on-trajectory net kinetic force

With the clock closure established on each trajectory, the original physical tau acceleration is reconstructed from the *nonlinear* RHS as

`a_tau = (DV(y)*f(y,xi))/c(y,xi)`.

The net Cartesian inertial force for the historical flat kinetic immersion is `F_Q=a_tau`. Its absolute **on-trajectory** generalized configuration force is `F_q=(DQ/dq)^T F_Q`. This agrees independently with the kinetic Euler-Lagrange residual derived from the original kinetic energy `T=||V||²/2`:

`F_q = d/dtau(∂T/∂u) - ∂T/∂q`.

The maximum on-trajectory generalized-force identity residual is **5.55e-16**. The separate centered directional-derivative calculation of the absolute xi-acceleration agrees within **5.94e-11**. At `xi=0.05`, the Cartesian force norms are about **0.40523115** (original) and **0.40523033** (autonomous), while the generalized configuration-force norms are about **0.69426208** and **0.69426342**. These are forces in declared kinetic coordinates/clock units, not measured SI forces.

Original seed final generalized-force vector in the declared `(log rho1, theta1, log rho2, theta2, logit x)` chart:

`(-0.694212224, 0.005387673, -0.002792616, 0.005387673, -0.001834595)`.

No scalar potential was fitted, and the absolute force values were not inferred from the frozen tangent matrix.

## 4. Nonlinear force response compared with the v18.51o tangent germ

At six independently selected observations across both seeds, centered perturbations of the original nonlinear acceleration field were mapped to `(Q,Qprime)`. The resulting force derivatives match the authenticated v18.51o `(E,F)` operators with maximum relative discrepancies:

- Position Jacobian `E`: **8.96e-07**.
- Velocity Jacobian `F`: **1.80e-06**.

The measured differences include finite-difference and historical spline differentiation errors. They are numerical consistency checks, not interval-valued rigorous enclosures.

## Limitations

- The solver is nonautonomous and driven; the on-trajectory net kinetic generalized force is not a uniquely identified *off-trajectory* constitutive force law.
- The kinetic Euler-Lagrange identity does not imply that the original driven dynamics is unforced or conservatively variational. No original action, dissipative law, or unique potential was recovered.
- The reconstructed clock is state dependent. Its gradient explains a specific tangent coupling, but does not imply a globally uniform reparameterization or a universal observer-independent material time.
- The observations are limited to `0<=xi<=0.05` at one historical midpoint kappa and two seed families; no return-path closure, material hysteresis certificate, universal spectral directionality or torsion law is derived.

For exact numerical and machine-provenance details consult `results/report.json`, `results/physical_clock_absolute_force_ledger.csv` and `results/nonlinear_force_jacobian_replay.csv`.
