# Construction first, audit second — Q550 v18.51d

## Historical physical kinetic energy

The authenticated v18.49h ancestor already identifies the **tau-time** kinetic energy in the original 10-dimensional material coordinates

`y=(log(rho1),v1,theta1,omega1,log(rho2),v2,theta2,omega2,logit(x),vz)`:

\[
 T=\frac12\left[\rho_1^2(v_1^2+\omega_1^2)+\rho_2^2(v_2^2+\omega_2^2)+m_x\{x(1-x)v_z\}^2\right].
\]

The 5D Cartesian physical configuration is

\[
 Q=(\rho_1\cos\theta_1,\rho_1\sin\theta_1,\rho_2\cos\theta_2,\rho_2\sin\theta_2,\sqrt{m_x}\,x).
\]

Writing `V=dQ/dtau`, it follows **exactly** that `T=V.T@V/2`. The original v18.49h historical implementation constructs a 10D tangent-bundle immersion `H_tau(y)=(Q,tau_ref*V)` and its Jacobian `L_y=DH_tau(y)`. Thus

\[
 G_y(y;\tau_{\rm ref})=L_y^T L_y,
\]

is a positive-definite pullback of the Euclidean metric wherever `rho1,rho2,m_x,tau_ref>0` and `0<x<1`. It is a **Sasaki-type material state metric associated with the kinetic Cartesian base**, not merely the 5D configuration-space mass metric, not a unique physical metric on phase space, and not a new Lagrangian theorem.

The contemporary v18.50x/z common observer chart has `dy/dz=diag(shared_scale_10d)=S`, so

`L=DH_tau(y)@S`, `G_z=L.T@L`.

This pullback is necessary: one must not apply the raw physical Jacobian to the historically rescaled observer chart without `S`.

## Compatible connection along the observed material trajectory

Let `L(xi)` be the immersion Jacobian on the **same** trajectory as the contemporary v18.50z model generators. The coordinate connection along the material path is

`Gamma=L^{-1}Lprime` (the flat Cartesian / induced Levi-Civita connection), and

`Gprime=Gamma.T@G+G@Gamma`.

This is a metric-compatibility identity, not an equation of motion and not a proof that the model dynamics is metric-preserving. A transported tangent vector obeys `D_xi v = vprime+Gamma@v`; its Cartesian representation is `L@v`.

For an arbitrary chart endomorphism `W`, define `A=L@W@inv(L)` and its physical Cartesian skew part `W_kin=skew(A)`. With `D=Lprime@inv(L)`, the complete rate obeys

`W_kin_prime=skew(L@Wprime@inv(L) + [D,A])`.

The **first term** contains exactly the inherited v18.51b algebraic model-generator, projector-posture, and observer-canonical contributions. The **second term** records the motion of the kinetic embedding frame, and must not be reassigned silently to either source.

## Sensitivity conventions and non-claims

- `tau_ref` is a declared position/velocity balance convention, not derivable from `T` alone. Compare 0.5, 1 and 2.
- The original model is driven and nonautonomous in xi; the kinetic energy need not be conserved.
- The comparison uses the **skew part** of the velocity-space endomorphism in physical Cartesian state coordinates. Symmetric strain is excluded from the selected spectral observable and is measured separately.
- The historical Euclidean observer chart and the kinetic Cartesian state are different geometries; their signed source percentages need not agree.
- Comparing source attributions under an actual metric change is not a passive coordinate transformation. A separate passive-chart covariance test is required.
- No material hysteresis, narrow-band activation, or observer-independent torsion is certified.

The first section is **construction**, not an empirical audit. Only the subsequent reproducibility, compatibility and spectral-source comparisons are the audit.
