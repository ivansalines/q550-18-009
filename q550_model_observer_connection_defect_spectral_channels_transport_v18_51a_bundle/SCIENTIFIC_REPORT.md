# Scientific report — Q550 v18.51a

**Model–Observer Connection Defect: Spectral Channels & Transport Audit**

## Research question

Can the two dominant spectral pairs of the v18.50z **model–observer connection difference** be distinguished as separate moving planes, and does their dominance change as the evolution coordinate advances?

## Provenance, coordinate choice and assumptions

The parent is the authenticated **v18.50z server sendback**, including 79 computed 10D Jacobian/canonical connection sections per branch and earlier y/x genealogy. This study reads the actual parent `model_vs_canonical_centerline_tensors.npz` and does not perform new Q550 physical integrations.

The two labels `original` and `autonomous` are **different naturally prepared seeds integrated at one shared midpoint κ0 = 0.1666331385421536**. The branches are not separate κ0 endpoints in this audit. All measurements use the **shared Euclidean 10D chart** declared in the parent. Neither this metric nor the skew off-block projection of the analytic J10 model generator has been established as a preferred material construction.

The tested skew operator is

```
W(xi) = K_model_crossblock(xi) - K_canonical(xi),  W^T = -W.
```

A 10D real skew generator has positive singular values in **repeated pairs**. We call the two dominant pair intensities σ1 and σ2; the corresponding **two-dimensional projectors** are `Q1`, `Q2`. Their SVD vector signs are not meaningful, whereas their projectors are basis independent within each separated spectral pair.

## Measured results — original-seed preparation

| Quantity | ξ=0 | ξ=0.05 |
|---|---:|---:|
| First pair singular intensity σ1 | 3.861371303 | 4.036347876 |
| Second pair singular intensity σ2 | 1.577546972 | 1.532214842 |
| First pair share of squared Frobenius norm | 85.69644% | 87.40499% |
| Second pair share (complement, to numerical floor) | 14.30356% | 12.59501% |
| Largest principal angle of Q1 relative to its start | 0° | **9.467830°** |
| Largest principal angle of Q2 relative to its start | 0° | **9.013988°** |
| Local Q1→Q2 coupling rate `||Q2 Q1' Q1||F` | 3.777137 | 2.642367 |
| Fraction of Q1 out-of-plane rate entering Q2 | 92.1603% | 91.6730% |

Across all 79 sections the first intensity increases on each successive sample, the second decreases, and the spectral gap remains larger than 2.28. **No dominance handover** is observed. Both rank-2 planes rotate by approximately nine degrees in the chosen chart.

For the **autonomous-seed preparation**, σ1 changes from 3.862491885 to 4.037507442, σ2 from 1.577481659 to 1.532151028, with endpoint pair-plane angles **9.464152°** and **9.010610°**. Its first-channel quadratic share rises from **85.70456% to 87.41223%**. The inter-channel coupling fraction is likewise around 92% at the start and 91.67% at the endpoint.

The coupling percentage is **a fraction of a Frobenius norm of a *projector derivative***, NOT the percentage of energy transmitted to another dynamical mode. It shows how much of one plane's instantaneous *out-of-plane movement* lies toward the other measured dominant plane.

## Numerical diagnostic checks

- All 158 measured skew defects have a symmetry residual of zero to machine representation, and two top paired singular intensities agree within approximately `7e-16` relative precision.
- The rank-2 spectral projectors are idempotent and mutually orthogonal to approximately `2e-15` or better in the cases checked.
- The two most energetic-in-the-matrix-norm pairs reconstruct the skew difference with a maximum **relative Frobenius residual ≈ 1.64e-9**.
- The third singular pair reaches at most about **7.1e-9** in the sampled data, and its plane is ill-conditioned. No orientation or material meaning is assigned to it.
- Projector time derivatives computed by cubic splines and a nonuniform three-point gradient differ by at most **6.1e-5 relative to the declared normalization** over this nonuniform grid. No continuous error enclosure is claimed.
- Two fixed seed preparations give similar but not identical numbers: no claim is made that two *different κ0 parameter values* have been compared during this audit.

## Interpretation and limitations

The data support **two distinct yet coupled moving spectral planes** in the parent model–observer skew connection difference. Dominance changes smoothly without a swap in the sampled interval. The prominent geometry is the **motion of the channels**, not a handover of which channel is larger.

This does **not** prove an exchange of mechanical energy, a physical torsion, a material connection, a κ0 narrow-band activation, observer-independent holonomy, physical memory, or a glass/polymer mechanical constitutive relation. In particular, `K_model` here is the parent-defined **skew offblock reduction** of the analytic 10D Jacobian, not its full nonorthogonal tangent evolution.

**Classification:** `AUTHENTICATED_SPECTRAL_PROJECTOR_CHANNEL_DIAGNOSTIC_NOT_PHYSICAL_MODE_OR_ENERGY_TRANSFER_CERTIFICATE`.

## Next discriminating test

Compare the **orientation/mixing of the two dominant spectral projectors** against a kinetic metric independently justified from the actual model, or against directly transported full tangent singular subspaces. If the channel directions persist under a physical change of metric and independently derived transport, their material interpretation becomes a testable proposal rather than a projection-dependent label.
