# Q550 v18.51o — Mathematical protocol

## Purpose and evidentiary boundary

The source is the historical Q550 v18.51e physical **full 10-dimensional tangent generator** and material propagator, cryptographically authenticated transitively through the new v18.51n parent. The preexisting original/autonomous material trajectories were integrated by v18.51e; **no original physical ODE is reintegrated by v18.51o**. This is a construction and audit of the *linearized, clock-coordinate-consistent kinematics*, followed by a **local effective acceleration-force Jacobian**. It is not the reconstruction of a unique nonlinear generalized force, of an action, or of a unique physical phase-space metric.

## Physical kinetic base versus tangent chart

The authenticated v18.49h source uses `y=(log rho1,v1,theta1,omega1,log rho2,v2,theta2,omega2,logit x,vz)`. The historical physical tau-coordinate Cartesian configuration and velocity obey

\[
Q=(\rho_1\cos\theta_1,\rho_1\sin\theta_1,\rho_2\cos\theta_2,\rho_2\sin\theta_2,\sqrt{m_x}\,x),\quad V=dQ/d\tau,\quad T=\tfrac12 V^TV.
\]

The v18.51e declared 10D measurement states are `X_tau=(delta Q,delta W_tau)` with `W_tau=tau_ref V`. Its true model parameter is `xi` (not asserted to equal tau). We read the matrices `B_tau(xi)` from the authenticated source and partition

\[
B_\tau=\begin{pmatrix}A&K\\C&D\end{pmatrix},\qquad
\alpha(\xi;\tau_{ref})=\tfrac15\operatorname{tr}K.
\]

The measured `K=alpha*I5` is tested *independently*, rather than imposed as a definition. The `A` block is also measured, without suppressing its nonzero fifth-column coupling. Thus the exact **linearized** kinematic identity on the frozen material trajectory is

\[
\delta Q' = A\,\delta Q+\alpha\,\delta W_\tau.
\]

`alpha` is an effective tangent coefficient. It is **not** by itself a certificate that `d tau / d xi = alpha`; additional additive configuration drift, a moving chart, and nonlinear clock specification may be present.

## Correct second-order tangent closure and effective-force germ

Set `delta U=delta Q'` and write the time-dependent invertible transformation

\[
Y=\begin{pmatrix}\delta Q\\\delta U\end{pmatrix}=
\mathcal T(\xi)\begin{pmatrix}\delta Q\\\delta W_\tau\end{pmatrix},\quad
\mathcal T=\begin{pmatrix}I&0\\A&\alpha I\end{pmatrix}.
\]

The transformed generator is `B_second=(Tprime+T B_tau)T^-1`. Because of the explicit transformation derivative, it has canonical kinematic upper blocks `[[0,I],...]` with

\[
\delta Q''=E\,\delta Q+F\,\delta Q',
\]

\[
\boxed{E=A'+\alpha C-\frac{\alpha'}{\alpha}A-DA},\qquad
\boxed{F=A+D+\frac{\alpha'}{\alpha}I}.
\]

These formulas constitute the local *linearization of the effective xi-time acceleration force*: `delta f_eff = E delta Q + F delta Qprime`. The zeroth-order force on the trajectory, as well as its nonlinear extension off the trajectory, **cannot be uniquely reconstructed from `B_tau` and a propagator alone**. A physical tau-time generalized force would require the authentic underlying state trajectory and clock convention, and independent verification against the driven equations. Calling `E,F` a unique original Q550 force law would be incorrect.

## Tests and discriminants

1. **Historical identity:** verify the SHA-256 and CRC of v18.51n and each nested v18.51m..e ancestor, plus the exact historical v18.49h kinetic-source hash and v18.51e frozen-tensor hash.
2. **Scalar kinematic block:** verify `K-alpha I=0` to numerical tolerance and explicitly retain `A`.
3. **Independent tangent-rate test:** differentiate the **stored finite-time propagators** by cubic splines and compare `delta Qprime` against `A delta Q + alpha delta W_tau`.
4. **Independent second-order tangent-rate test:** differentiate the finite-time position propagators *twice* and compare to `E delta Q+F delta Qprime`. Spline curvature is expected to be less accurate than the first-rate identity.
5. **Transform identity:** calculate `(Tprime+T B)T^-1` separately and check it equals `[[0,I],[E,F]]`.
6. **Metric-weight invariance:** test `alpha_tau*tau_ref = alpha_1`, `E_tau=E_1`, and `F_tau=F_1`; these are passive velocity units of the same trajectory, not independently selected physical clocks.
7. **Passive configuration chart:** apply a nonorthogonal constant GL(5) to configuration and velocity and verify similarity of `E,F`.
8. **Synthetic independent controls:** pure changing clock (no spurious positional force), conservative quadratic stiffness, and driven drift/velocity damping. A failed test stops the runner.

The sampled xi-grid is the inherited 79-section interval `0 <= xi <= 0.05`; slopes are from nonuniform-grid cubic splines, not from an analytic `dB/dxi` produced by the original physical solver.

## Variational admissibility: deliberately narrow statement

With the flat kinetic Cartesian base, a **naive unforced xi-time** natural-Lagrangian ansatz `L=0.5|Qprime|^2-U(Q,xi)` would require an instantaneous position Jacobian symmetric and an instantaneous `F=0`. The observed nonsymmetric part of `E` and nonzero `F` rule out that *narrow ansatz in these variables* on the tested trajectory. They **do not** exclude driven, dissipative, magnetic/gyroscopic, velocity-dependent, explicit-time, moving-chart, or reparametrized variational formulations. The reconstructed force germ is a gauge-dependent local dynamical representation; it is not a global Helmholtz/inverse-variational certificate.

No unproven material torsion, material hysteresis, observer-independent transfer or 1/3 law is used in the decisions.
