# Q550 v18.51n — Mathematical protocol

## 1. Two distinct mathematical questions

The original authenticated v18.49h physical kinetic energy in tau time is

\[
T=\frac12[\rho_1^2(v_1^2+\omega_1^2)+\rho_2^2(v_2^2+\omega_2^2)+m_x x^2(1-x)^2v_z^2].
\]

Using configuration coordinates `q=(log rho1,theta1,log rho2,theta2,logit x)` and matching generalized velocities `(v1,omega1,v2,omega2,vz)`, the **configuration velocity Hessian** is

\[
M(q)=\partial_{\dot q}^2T
=\operatorname{diag}(\rho_1^2,\rho_1^2,\rho_2^2,\rho_2^2,m_x x^2(1-x)^2).
\]

It is SPD for `rho1,rho2,m_x>0` and `0<x<1`. The original kinetic immersion of v18.49h into `H_tau=(Q,tau_ref V)` gives a **declared** Sasaki-type 10D state-space lift; kinetic energy alone does not fix the relative position/velocity measurement scale `tau_ref`. Proving the kinetic Hessian is **not** proving a unique Lagrangian, unique 10D state metric, or identifying conservative generalized forces. The kinetic source is checked against its authenticated historical SHA-256 and finite-difference Hessian tests are performed independently at 32 regular configurations.

A *formal* necessary diagnostic for the simple Cartesian **unforced** ansatz `L(Q,Qprime,xi)=|Qprime|²/2-U(Q,xi)`, if `xi` were the physical time and `Qprime=V`, is reported using the authentic 10D generator blocks `B_QQ,B_QV,B_VQ,B_VV`. Such a diagnostic MUST NOT be used to reject a driven, velocity-dependent, or time-reparameterized variational formulation. This model includes a driven clock and no complete Euler-Lagrange force audit is supplied in v18.51n.

## 2. Causal and noncausal measurement windows

The inherited authentic physical Cartesian material tangent maps `M(xi)` from v18.51e remain unchanged; `T(u,i)=M(u)M(i)^{-1}`. An output selector `C` is one of `C_Q=[I5,0]` or `C_V=[0,I5]`. For each section, a normalized Gaussian output kernel defines

\[
G_i=\int_{I_i} w_i(u)T(u,i)^T C^T C T(u,i)\,du,\qquad
w_i(u)\propto\exp(-(u-\xi_i)^2/(2h^2)).
\]

The three explicit measurement protocols are: `past` on `[0,xi_i]` (uses no future output, history-conditioned); `future` on `[xi_i,.05]` (predictive, not causal at `xi_i`); `bilateral` on `[0,.05]` (noncausal if `xi_i` is interior). Truncating the observation interval near an endpoint may make a 5-output/10-state Gram poorly conditioned. No full-rank claim is assumed. All outputs are integrated from a cubic spline through the **authentic 79 frozen material matrices**, with 64-point Gauss-Legendre quadrature. These additional quadrature nodes are not new original Q550 IVP integrations.

Raw Grams must have span at least `min(h/5,.005)` and `lambda_min/lambda_max>1e-8`, with condition <=`1e8`, to be labelled *well resolved*. The archive records rejected raw windows explicitly. As a stress test, we also study `G_i(epsilon)=G_i+epsilon*c I`, `epsilon in {1e-5,1e-3}`, with a fixed within-seed/profile scalar `c=mean_{i>0}tr(G_i)/10`. **This regularizer is a measurement convention, not the kinetic Hessian and not derived from the action.** All raw vs regularized claims are kept separate.

## 3. No changes to the material map or spectral planes

The same authenticated real Riesz planes `E4,E5` are used for all metrics, with fixed Cartesian-orthonormal frames `U4,U5` and the historical obliquely projected 2×2 cross-plane operators. The norm is

\[
\lVert K_{i\leftarrow j}(b,a)\rVert_{G_b,G_a}
=\lVert H_i(b)^{1/2}K_{i\leftarrow j}^{E}(b,a)H_j(a)^{-1/2}\rVert_F,
\quad H_j(a)=U_j(a)^TG_aU_j(a).
\]

The ratio `||K_4<-5|| / ||K_5<-4||` is measured independently for the instantaneous covariant drift and finite material propagators with 1, 2 and 4 section lag. Both arrows denote cross-subspace source-to-target at the SAME **forward** temporal direction; they are not forward/reversed physical time. Only the metric changes. Norms are gauge invariant under orthonormal internal plane-frame changes but not invariant under changing the physical metric definition.

## 4. Scientific decision rules

- A raw near-boundary or badly conditioned observation Gram is `UNRESOLVED`, not a physical failure or a sign inversion.
- A sign found under regularization is labelled `REGULARIZED_OBSERVER_DIAGNOSTIC`, not a variational certificate.
- A sign found consistently with well-resolved causal past and bilateral windows supports **operational window robustness**, not observer-independent material direction.
- The mathematical existence of `partial² T / partial qdot²` supports a **configuration kinetic mass metric only**. Full Lagrangian admissibility requires verification of the dynamics, generalized forces, boundary/action principles and, where needed, Helmholtz inverse-problem conditions.
- No numerical result on these inherited 79 sections is an interval certificate for the full Q550 flow or a demonstration of memory, torsion or irreversibility.
