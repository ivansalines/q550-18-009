# Decision rules — Q550 v18.51p

1. **Authenticate before physics.** Verify full source/output SHA-256 through each ancestor; reject drift in original v18.49h kinetic source, v18.50x solver staging source, or cached v18.51e physical tensor file.
2. **Clock closure.** Require a positive common `c` for five independent configuration velocities; report the residual rather than assuming `f_q=c*u`.
3. **Clock gradient.** Independently differentiate `c(y,t)` and verify both `A=V⊗grad_Q c` and `K=cI+V⊗grad_V c` against the original tangent chart.
4. **Absolute force.** Compute acceleration directly from the original nonlinear RHS; check independently via a centered directional derivative of `DQ*f` and the kinetic Euler–Lagrange residual.
5. **Nonlinear force Jacobian.** Reconstruct `(E,F)` independently at six selected observations, without using the inherited B matrix for the numerator. Compare with the historical frozen tangent using explicitly budgeted spline/finite-difference tolerances.
6. **No forced positive outcome.** A failed closure is a scientific finding; do not silently modify the clock, weights, trajectory, or force to make it pass. Keep the report and failing evidence. Do not promote the synthetic controls to physical evidence.
7. **Classification boundary.** The output is an on-trajectory absolute net inertial/generalized force with an explicitly reconstructed *state-dependent* clock. It is NOT a unique global force law or a proof of an unforced variational principle.
