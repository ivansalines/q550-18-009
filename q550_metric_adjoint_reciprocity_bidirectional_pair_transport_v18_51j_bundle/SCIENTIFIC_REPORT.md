# Q550 v18.51j — Scientific report

**Title:** Metric-Adjoint Reciprocity & Bidirectional Pair Transport Audit  
**Classification:** Numerical same-metric adjoint and finite-lag tangent diagnostic;
not an observer-independent material energy transfer certificate.  
**Origin:** Authenticated v18.51i server sendback, recursively including v18.51h,
v18.51g, v18.51f, v18.51e and two historical physical Q550 10D tangent IVPs.
**Additional physical IVPs:** zero.

## Main observations

The restricted instantaneous 5→4 channel remains stronger than 4→5 in all
**468 of 468 positive sections** (two seeds, three tau conventions, 78 sections
per branch). The same directional ordering survives the **1,362 measured
forward-time finite-lag intervals** covering one, two and four section spacings,
with source spectral restriction at the beginning and target oblique Riesz
projection at the end. The finite-lag rates are not being inferred by
multiplying instantaneous coupling numbers; they are computed from the
historic Q550 material tangent matrices `M(xi_b)M(xi_a)^-1`.

### Original-seed endpoint (xi=0.05)

| tau_ref | Instantaneous restricted 5→4 / 4→5 | Finite-lag, last one-step 5→4 / 4→5 | Normalized same-metric adjoint defect |
|---:|---:|---:|---:|
| 0.5 | 1.596846 | 1.606221 | 0.979478 |
| 1.0 | 1.706214 | 1.717683 | 0.987514 |
| 2.0 | 1.328822 | 1.332232 | 0.948530 |

For the autonomous seed the respective instantaneous endpoint ratios are
1.589410, 1.696504, 1.323502; the last one-step ratios are 1.598813,
1.707970, 1.326840.

In the tau=1 original final section the actual restricted rates are 6.301207
(5→4) and 3.693093 (4→5). With

```
S = (K_4<-5 + K_5<-4.T)/2
A = (K_4<-5 - K_5<-4.T)/2
```

we find `||S||_F ≈ 2.154187`, `||A||_F ≈ 6.978798` and the positive
interference `4<S,A>_F ≈ 52.132539`, equal to the squared-core difference.
This equality is algebraic and cannot on its own establish a material
interaction mechanism. The adjoint defect is substantial, but it remains
dependent on the declared metric.

## Numerical controls

- **20/20** scientific/genealogy checks passed in local replay; separate
  independent synthetic geometry and regenerated-output tests are included.
- Maximum normalized Frobenius reciprocity-identity residual:
  **4.83×10⁻¹⁶**.
- Maximum orthogonal within-plane gauge perturbation discrepancy:
  **2.85×10⁻¹⁴**.
- Material propagator composition residual:
  **3.69×10⁻¹⁶**; inverse residual **2.77×10⁻¹⁶**.
- After metric pullback into tau=1 and for xi≥0.001, maximum restricted
  rate discrepancy is **7.61×10⁻⁹** and maximum adjoint-defect discrepancy
  **3.99×10⁻¹⁰**. Near xi=0 the worst rate discrepancy is about
  **7.32×10⁻⁷**, retaining the known sensitivity of the small spectral gaps.
- Three lags are evaluated on **actual inherited section spacings**, not a
  uniform-step surrogate.

## Scientific decision

The forward-time directional asymmetry of the 4↔5 restricted spectral
crossblocks **survives both the same-metric adjoint test and these finite-lag
material transport diagnostics** on the available local Q550 sample. The
identity used to expose symmetric/antisymmetric interference is exact, but
does not assign causality to the terms. Inverse-time propagators are a
separate diagnostic, and cannot be equated with the opposite forward-time
spectral channel. The plotted spectral plane labels are not unique at xi=0.

The result is **not** proof of physical irreversibility, conserved or exchanged
energy, universal material torsion, or hysteretic memory. The magnitude changes
when changing the kinetic position/velocity scale tau; only pulled-back
metric comparisons justify passive covariance. The finite sample through
xi=0.05 cannot exclude behavior between sections or in a wider dynamical
window.

## Next possible discriminator

A next audit could compare a genuinely independently justified material
quadratic form and a parallel-transported pair frame along the Q550 orbit,
and test whether the finite-lag channel ordering persists outside the narrow
local section window. Do not assume a unique metric or use a fitted 1/3 rule.
