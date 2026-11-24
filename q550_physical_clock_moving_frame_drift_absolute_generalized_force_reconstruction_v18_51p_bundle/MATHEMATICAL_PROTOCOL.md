# Q550 v18.51p — Mathematical protocol

## Construction first, audit second

The original nonautonomous driven solver is replayed at its *authenticated midpoint kappa*, for two independently prepared historical turning-point seeds. The same imposed external drive and original RHS are used at each seed's own historical event time. No substitute nonlinear dynamics and no synthetic Q550 trajectory are used.

The original 10D material chart is

`y=(log rho1,v1,theta1,omega1,log rho2,v2,theta2,omega2,logit x,vz)`.

Let `q=(log rho1,theta1,log rho2,theta2,logit x)` and `u=(v1,omega1,v2,omega2,vz)`.
The reconstructed clock is computed directly from the nonlinear RHS `f(y,t)`:

`c(y,t) = <u, f_q(y,t)>/<u,u>`.

Its independent consistency residual is `f_q - c*u`. This is meaningful only where `<u,u> > 0`. If this residual fails, the scalar clock reconstruction MUST be rejected. Here `xi=t-event`, so `d tau/d xi=c` along each *specific* material trajectory. A state-dependent clock is **not** a global prescribed independent variable transformation across perturbed trajectories.

The authentic historical kinetic immersion is

`H(y)=(Q(y),V(y))`, where `Q=(rho1 cos theta1, rho1 sin theta1, rho2 cos theta2, rho2 sin theta2, sqrt(m_x)*x)` and `T=||V||²/2`.

The full physical nonlinear field implies `Qprime = DQ*f`. Its clock-specific identity is `Qprime=c*V`. Finite differences at fixed physical time find `grad_y c` and the explicit drive term `partial_t c`. These yield

`dc/dxi = grad_y(c)*f + partial_t(c)` and `Qsecond = (dc/dxi)*V + c*(DV*f)`.

The same acceleration is checked independently by a centered directional difference of the original `Qprime(y,t)` field along `(f,1)`.

## Why the inherited rank-one position block can be explained

At fixed time, variations of `Qprime=c(Q,V,t)*V` obey

`delta Qprime = V*(grad_Q c · delta Q) + (c I + V*(grad_V c)^T) delta V`.

Thus the *source-derived* first two tangent blocks are

`A_clock = V ⊗ grad_Q c`, `K_clock = c*I + V ⊗ grad_V c`.

The gradients in `(Q,V)` are obtained via the **inverse of the original authenticated immersion Jacobian**: `grad_H c = grad_y c * (DH)^-1`. Compare against both original v18.51e physical tangent-generator blocks. The small fifth-column specificity must be reconstructed, not assumed. This identity is a clock/representation effect; it is not a certificate of material torsion.

## Absolute kinetic force (on the original trajectory)

If `d tau/d xi=c` and `Qprime=c V` hold, then the original physical tau acceleration is

`a_tau = (DV*f)/c`.

The Cartesian net inertial force for the unit-mass kinetic Cartesian immersion is `F_Q = a_tau`, and its generalized force in material configuration coordinates is

`F_q = (DQ/dq)^T F_Q`.

Independently, let `M(q)=(DQ/dq)^T (DQ/dq)`; the historical kinetic energy is `T=1/2 u^T M(q) u`. The generalized kinetic Euler–Lagrange residual is

`F_EL = (1/c) d/dxi (∂T/∂u) - ∂T/∂q`.

The two on-trajectory forces must agree. This **constructs the absolute net force evaluated on the original driven trajectory**. It does not identify a unique force-field extension off that trajectory, an original scalar potential, a conservative force, a memory law, or a global action principle. In particular, `F_EL` is an identity for kinetic energy plus applied generalized force, not proof of unforced Euler–Lagrange dynamics.

## Independent force linearization audit

At selected sections, compute the Jacobian of the nonlinear `Qsecond(y,t)` at fixed forcing time through independent centered state perturbations; transform it to `(delta Q,delta Qprime)` using the Jacobian of `(Q,Qprime)` at the same point. Compare its `(E,F)` blocks with those from the authenticated v18.51o frozen-tangent reconstruction. This is a distinct nonlinear replay, with finite-difference and inherited spline errors reported separately.

## Numerical limitations

Source-preserving finite differences test the scalar clock and inertial-force formulas, not continuum interval enclosures. Time derivatives at fixed state include the external driven phase `theta(t)`, and the two seed event times are distinct. The analysis horizon is only `0 <= xi <= 0.05` and is not a material return closure. A common time reparameterization for all nearby states cannot be inferred from a state-dependent clock.
