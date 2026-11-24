# Q550 v18.51o — Decision rules

**The construction comes before the audit.** The equations transforming `X_tau=(delta Q,delta W_tau)` to `(delta Q,delta Qprime)` are algebraic. The Q550-specific content is the authenticated data, the measured scalar nature of the position/velocity block, the nonzero extra position coupling, and the independently tested finite-time tangent rates.

All of the following are required for a local numerical success:

- The v18.51n parent, every nested ancestor down to v18.51e, and the exact original kinetic-source bytes pass CRC and manifest authentication.
- Two historical seeds, three tau-ref conventions, and 79 xi samples per branch must be present.
- `||K-alpha I||` < 1e-10; `alpha` > 0. The first four columns of `A` must have norm < 1e-7; its fifth column must be retained and measured.
- Relative first-derivative finite-tangent residual < 1e-6, relative second-derivative residual < 1e-4. These thresholds are **numerical regression thresholds**, not physical limits.
- Exact moving-frame generator identity residual < 1e-11, `E,F` same under three tau-ref conventions to relative 1e-8; `alpha*tau_ref` same to 1e-11.
- Nonorthogonal constant passive-chart covariance and three independent synthetic controls pass.

### Classification permitted upon success

`NUMERICAL_AUTHENTIC_FROZEN_TANGENT_SECOND_ORDER_CLOSURE_EFFECTIVE_FORCE_JACOBIAN_ONLY`.

### Forbidden upgrade

Do NOT promote `alpha` to an independently established physical time conversion. Do NOT present `E,F` as the unique nonlinear physical generalized forces, or the non-symmetry of `E` as a no-go theorem for all variational formulations. Do NOT infer a material direction, hysteresis, torsion, or time irreversibility. The tests are local sampled numerical checks; they are not interval certificates for the entire Q550 dynamics.
