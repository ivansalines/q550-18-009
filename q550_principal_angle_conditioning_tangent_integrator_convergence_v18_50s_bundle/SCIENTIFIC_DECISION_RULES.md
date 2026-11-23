# v18.50s — Scientific decision rules

1. **Authenticity first.** Parent r source/output digests must match, and the
   original q/r scripts must be used to reconstruct the model and gate.
2. **Completion first.** Only `solve_ivp.success=True` with a last reported time
   at the requested gate endpoint may enter the convergence estimate. A run
   with `nfev=6` must be checked through `success`, `message` and `t_end` rather
   than called converged on count alone.
3. **Angle conditioning.** Prefer the sine-of-principal-angle route; demand
   agreement between the residual-SVD and projector-difference routes.
   Agreement with overlap `arccos` is limited by floating-point conditioning.
4. **Independent solver axes.** Vary the integration method, error tolerance,
   and the maximum-step cap. A constant evaluation count under a binding step
   cap does not on its own prove tolerance independence.
5. **Keep mathematical sources distinct.** The historical q parent used a
   numerically differentiated 10D tangent generator; the r/s audits use the
   original analytic structural-Jacobian block. Compare them as a regression
   but do not assert an identical internal numerical algorithm.
6. **No physical attribution.** The computed projector is orthogonal in the
   chosen 10D scaled Euclidean coordinate chart. Convergence of its angle is
   not proof of a metric-independent material rotation, geometric holonomy,
   stress response, or physical memory.
7. **Separate provenance from reconstruction.** Immutable source SHA-256
   checks byte identity, while numerical outputs are evaluated with explicit
   error and convergence controls. PNG encoding metadata is not evidence of a
   scientific discrepancy.
8. **No silent tolerances.** Report any SciPy warning about machine-precision
   clamping and all failed endpoint or singular-basis cases.
9. **Event uncertainty.** Both gate endpoints are inherited numeric estimates
   from l; the current scan holds those estimates fixed. It does not certify
   their continuous-time uniqueness or uncertainty.

Classification: `INHERITED_CHART_NUMERICAL_PRINCIPAL_ANGLE_INTEGRATOR_CONVERGENCE_NOT_MATERIAL_CERTIFICATE`.
