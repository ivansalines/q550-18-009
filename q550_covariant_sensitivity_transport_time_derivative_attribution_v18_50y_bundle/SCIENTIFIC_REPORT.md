# Scientific report — Q550 v18.50y

## Question

How much of the previously measured ~9.64° rotation of the κ-sensitivity tensor `E=∂κP` remains after following the **observed 7D kernel projector** with a well-defined metric-preserving frame? And how much of the apparent instantaneous change is sensitive to numerical differentiation?

## Observation and method

The input is the authenticated **server v18.50x** tensor dataset. All 44 driven physical 10D IVPs were executed in the parent, not in this audit. The present calculation uses 3,476 observations of 10×10 projectors and their κ derivatives, and integrates six *auxiliary, geometric* frame ODEs.

For a differentiable orthogonal projector `P`, choose the minimal off-diagonal/horizontal skew generator

\[
K=[\dot P,P],\qquad \dot P=[K,P],\qquad \nabla_\xi E=\dot E-[K,E].
\]

The correction depends on `P` and its motion, **not on tailoring a rotation to E**. Yet this is a connection *associated with the observed projector and inherited Frobenius metric*, not a constitutive/material 10D connection independently supplied by the model.

## Main numerical findings

At the midpoint of the historical interval, ξ from 0 to 0.05:

| Seed preparation | Angle in fixed 10D chart | Angle in the kernel-parallel frame | Endpoint change in angle |
|---|---:|---:|---:|
| Original κ preparation | 9.63947802° | **8.51660780°** | −1.12287022° |
| Autonomous κ preparation | 9.64063481° | **8.51735776°** | −1.12327705° |

This angular difference is not itself an additive partition of physical rotations. The remaining ~8.52° is a residual **relative to the explicitly declared kernel-parallel frame**.

In the same midpoint original preparation:

| Quantity | ξ=0 | ξ=0.05 |
|---|---:|---:|
| `||dE/dξ||_F` using cubic spline | 14.390835 | 12.873741 |
| `||∇ξE||_F` after projector transport | 12.590443 | 11.622672 |
| `||[K,E]||_F` (frame correction) | 6.969712 | 5.535947 |
| Ordinary direction rate (rad/ξ) | 3.736823 | 3.030709 |
| Kernel-horizontal direction rate (rad/ξ) | **3.260798** | **2.692526** |
| `d||E||_F/dξ` | +1.860136 | +4.504983 |

The radial growth rate is invariant under the skew-connection correction to floating-point precision, as expected analytically.

## Numerical controls

- The parent ZIP has **12/12 source** hashes and **11/11 output** hashes verified.
- A separate nonorthogonal time-dependent coordinate transform preserves the corrected derivative to relative Frobenius error ≤ `1.1×10⁻¹⁵` and the transported-metric norm to ≤ `4.6×10⁻¹⁶`. The negative control omitting the frame connection fails substantially.
- The transported projector at ξ=0.05 agrees with the independently observed projector to Frobenius error ≤ `3.9×10⁻¹¹` in all six ODE replays. Frame orthogonality remains within `3.3×10⁻¹⁵`.
- The spline vs independent five-node time derivative produces a maximal relative discrepancy of approximately `7.1×10⁻⁵` for the corrected rate (all κ and ξ), 99th percentile around `2.3×10⁻⁵`. These are numerical consistency diagnostics, **not certified continuous derivative bounds**.
- All six geometric frame ODEs complete. No physical Q550 IVPs are rerun.

## Interpretation

The ~9.64° change of sensitivity direction from v18.50x is **not entirely explained** by following the observed kernel's own horizontal frame, but is **partly frame-dependent**. The remaining ~8.52° is still conditional on the chosen metric, projector and connection; it is not an intrinsic or material torsion certificate.

A physically independent next test would reconstruct the true tangent generator `J_10` and a dynamically justified material metric on the same states, then compare that model-derived transport against the canonical projector transport **without fitting either to E**. The x archive stores `P/E/A`, not the full state trajectories, so that additional comparison cannot be inferred from this dataset alone.

**Classification:** `CANONICAL_OBSERVER_PROJECTOR_TRANSPORT_DIAGNOSTIC_NOT_MODEL_PRIVILEGED_MATERIAL_CONNECTION_OR_ACTIVATION_CERTIFICATE`.
