# Mathematical protocol: Q550 v18.51e

## Existing physical model and kinetic pullback

Historical model: `y=(log rho_1,v_1,theta_1,omega_1,log rho_2,v_2,theta_2,omega_2,logit x,v_z)`. Tau-time kinetic energy:

`T=(rho1^2 (v1^2+omega1^2) + rho2^2 (v2^2+omega2^2) + m_x (x(1-x)v_z)^2)/2`.

Authentic 5D Cartesian configuration `Q=(rho1 cos theta1,rho1 sin theta1,rho2 cos theta2,rho2 sin theta2,sqrt(m_x) x)`, tau-time velocity `V=dQ/dtau`, historical 10D state immersion `H_tau(y)=(Q,tau_ref V)`. The legacy shared Euclidean observer state `z=S y` uses `S=diag(shared_scale_10d)`: the exact historical v18.50z Jacobian is `J_z=S J_y S^-1`. Therefore `dy=S^-1 dz`, and the *physically consistent* pullback is `L=DH_tau(y) S^-1`, `G=L.T L`. This chart orientation is independently cross-checked by comparing `L_end F_z L_0^-1` with `DH_end (S^-1 F_z S) DH_0^-1`. **Important:** v18.51d used `DH_tau S` for its declared Gram metric; that construction may be algebraically compatible as an immersion pullback, but does NOT match the v18.50z shared-jet coordinates as interpreted here. v18.51e records the legacy discrepancy; it must not silently inherit the earlier physical identification.

## Full material generator; not merely antisymmetric cross-plane defect

For an authenticated driven model trajectory at the inherited common midpoint κ, the true 10D variational propagator is

`F'(xi)=J_10(xi) F(xi), F(0)=I`,

where `J_10` is the analytic Q550 physical jet expressed in the **same fixed inherited shared chart** as v18.50z. This is the full generator including shear, symmetric strain and skew rotation. `F` is integrated along a new true 10D IVP; cubic interpolation of the 79-tabulated parent `J` is only an independent numerical comparator.

In Cartesian kinetic state coordinates:

`M(xi)=L(xi) F(xi) L(0)^-1`, `B(xi)=L J_10 L^-1 + Lprime L^-1`.

Then `Mprime=B M`. Split the same full generator `B=S_B+Omega_B` with `S_B=sym(B)`, `Omega_B=skew(B)`. The moving frame term `Lprime L^-1` stays explicit. We compute `Lprime` from the historical explicit Jacobian via material directional central differentiation with `dy/dxi` from the genuine jet. Independent cubic-spline differentiation of sampled `L` checks this step; neither is interval certified.

`C=M.T M` is the **right** finite-time Cauchy–Green tensor in the initial physical Cartesian kinetic basis. Its differential identity is `Cprime=2 M.T S_B M`, and the volume identity is `d/dxi log det M = tr B`. Singular values of `M` are stretches in the declared kinetic state metric family, not energy fractions. Polar `M=R U` gives one 10D rotation diagnostic; `||R-I||_F` is not a unique material torsion angle.

## Passive chart and independent physical controls

A nonlinear passive chart change `z -> z+a sin z`, with different Jacobians `D0` and `Dxi` at initial/final states, gives `Fnew=Dxi F D0^-1`, `Lnew_i=Li Di^-1`, and **the exact same physical** `M` and `C`. This is a passive-coordinate control; changing tau_ref is **not** a passive transformation.

The independent physical finite-difference comparator perturbs genuine initial Q550 states in the inherited shared chart and re-integrates the original 10D driven model. A distinct interpolation-based tangent run compares the original analytic-jet continuous transport against the archived sampled-grid representation. Explicit numerical error checks apply.

## The 1/3 observation

The user noticed a visual near-1/3 structure in v18.51d spectral accounting. We preserve that observation as a **falsifiable heuristic**: use the historical `signed_canonical / signed_kinetic_frame` ratio along 79 sections for both seed families and three tau-ref conventions, with a predeclared absolute ratio tolerance of 0.025. Its closeness is NOT a required scientific control. Neither this ratio nor the underlying signed fractions measure kinetic energy or correspond to the eigenvalues of C. If it fails under other tau-ref conventions, report the failure rather than promoting a formula.
