# Q550 v18.51g — Mathematical protocol

## Authenticity and domain

Parent: the actual v18.51f server sendback, embedding the authenticated v18.51e physical 10D trajectory and continuous tangent IVPs. Verify both ancestor ZIPs' source/output SHA-256 lists and parent scientific checks. The two seed families are `original` and `autonomous`, at one inherited common midpoint `kappa=0.1666331385421536`. Sections are `0 <= xi <= 0.05`, 79 per branch, with three kinetic-state balance conventions `tau_ref=0.5, 1, 2`. No new physical IVP is solved in this audit. Use `M` and **the independent stored physical generator `B`**, never a surrogate derived by differentiating the same spectral projectors.

## Core identity

The genuine kinetic Cartesian material propagator satisfies `M' = B M`; `B=L J10 L^-1 + L' L^-1` is inherited from the authentic v18.51e model.

For isolated finite-time conjugate pairs `lambda_j, lambda*_j` of `M(xi)`, define the **real, generally oblique** rank-2 Riesz spectral projector `P_j=R_j+R_j*`, with the complex left/right biorthogonal eigenprojector `R_a=v_a w_a^H/(w_a^H v_a)`.

Let `I_j` be the two eigenvalues in pair j. The derivative follows the full nonnormal spectral perturbation expression:

`P'_j = Re sum_{a in I_j, k outside I_j} [ R_k (B M) R_a + R_a (B M) R_k ] / (lambda_a-lambda_k)`.

Define `D_xi P_j = P'_j - [B,P_j]`. If this is zero, the instantaneous spectral subspace is advected by the cocycle at this section; otherwise it drifts relative to the actual material transport. This definition does **not** imply the five finite-time eigenplanes are independently physical or that the drift is energy transfer.

For directed channels `j -> i`, `i != j`, the measured oblique cross-rate is

`r_{j->i} = ||P_i (D_xi P_j) P_j||_F / ||P_j||_F`.

It is the first-order coefficient of the finite-increment projected leakage `||P_i(xi+dt) M(xi+dt) M(xi)^-1 P_j(xi)||_F/(dt ||M(xi+dt)M(xi)^-1 P_j(xi)||_F)` as `dt -> 0`. For finite `dt`, their disagreement is a **measured discretization effect**, not to be set to zero algebraically.

## Time-step and conditioning

Use the actual nonuniform 79-section grid. Check the analytic derivative from `B M` against independently computed local 3-point and 5-point polynomial spectral-projector differences, and compare 5-point errors across common nodes at strides 1, 2, and 4. This is discrete sample refinement; no new physical trajectory is invented.

Interpolate the inherited sampled **physical** `B(xi)` with a cubic spline as a diagnostic approximation and integrate local cocycle steps by RK4 with 1,2,4,8 subdivisions, comparing the result against the independently inherited exact finite-time increment `M_i M_{i-1}^-1`. A small residual does not establish convergence of the parent 10D physical solver between its original sections.

Near `xi=0`, the finite-time map tends to the identity and all ten eigenvalues coalesce, so `P_j(0)` is undefined. Source and target matrices `M,B` are mutually similar to double precision; **independent eigendecompositions** of almost-degenerate `M` make `P'` numerically less well conditioned. Report absolute, relative and spectral-gap-scaled residuals rather than setting arbitrary small near-zero tolerances or pretending the full interval is certified. The adopted recorded numerical controls require interior `xi >= 0.001` agreement and gap-scaled residuals in the near-degenerate region; these are numerical tolerances set during diagnostic development, not pre-registered rigorous error bars.

## Kinetic-state convention, not passive energy

A constant kinetic-scale change yields `D_tau=diag(I_5,tau_ref I_5)`, `M_tau=D_tau M_1 D_tau^-1`, `B_tau=D_tau B_1 D_tau^-1`, `P_tau=D_tau P_1 D_tau^-1` and `D_xi P_tau=D_tau (D_xi P_1) D_tau^-1`. Compare matrices in the **common tau=1 frame**. Raw Frobenius magnitudes and directional fractions are generally **not invariant** under a nonorthogonal D_tau.

## Interpretation and exclusions

- Five conjugate pairs observed at **sampled** positive sections, not a gap certificate for every continuous time.
- Coherent directed 5->4 coupling is a local full 10D projector diagnostic, not material energy transfer.
- Nothing here identifies physical torsion, hysteretic memory, unique phase-space metric, or an autonomous kappa-band trigger.
- The earlier 1/3 heuristic is retired, not promoted to an audit criterion.
