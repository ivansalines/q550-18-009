# Q550 v18.50x — Scientific report

## Purpose and prior finding

The v18.50u and v18.50v fixed-seed κ scans showed smooth parameter responses without a qualified narrow-band activation; v18.50w traced crossings of **two anchored distances**. Those crossing zeros exist by construction. The present audit removes anchor-distance subtraction from its primary observable and measures the tensor-valued **local κ response** of the analytic rank-three seven-dimensional observation kernel.

## Definition and geometric identities

Let \(P(\kappa,\xi)\in\mathbb{R}^{10\times10}\) be the orthogonal projector onto the seven-dimensional nullspace of the analytic Jacobian of the normalized structural observer in the inherited, shared 10D chart. We study

\[
E=\partial_\kappa P,\quad A=\partial_\xi E,\quad
S=\|E\|_F,\quad
S'=\frac{\langle E,A\rangle_F}{\|E\|_F}.
\]

The perpendicular rate \(A_\perp=A-S'E/S\) and orientation speed \(\Omega=\|A_\perp\|_F/S\) distinguish **change in sensitivity magnitude** from **change in sensitivity direction**. The identity \(\|A\|^2=(S')^2+\|A_\perp\|^2\) is monitored numerically.

Because \(P^2=P\), the exact derivative obeys \(PEP=0\) and \((I-P)E(I-P)=0\). The audit evaluates their finite-grid residuals and compares nonuniform three-node and five-node κ derivatives, as well as a time gradient and cubic spline derivative. There is **no imposed zero** at either historical κ value in the definition of E.

## Replay design

- Authentic ancestors: server sendback v18.50w, its nested server v18.50v, and v18.50u, all source/output SHA-256 manifests checked before replay.
- Two separately prepared fixed natural turning seeds, not an independently continued natural state for each κ.
- 22 κ values (13 within the historical pair), 79 ξ sections, ξ from 0 to 0.05, 44 controlled new 10D integrations with DOP853 and the original model.
- 3,476 projector observations, including their 10×10 matrices and κ/ξ derivatives saved in a compressed NPZ for reproducibility and efficient follow-on audits.
- The Frobenius norm on the inherited common 10D chart is a *declared observable metric*, not a physical kinetic-metric certificate. The time origins of the two seeds are separately inherited.

## Measured central-band passage (κ offset 0.5)

| Quantity | Original at ξ=0 | Original at ξ=0.05 | Autonomous at ξ=0 | Autonomous at ξ=0.05 |
|---|---:|---:|---:|---:|
| \(\|E\|_F\) | 3.81878135 | 3.97919450 | 3.81894064 | 3.97945196 |
| \(\|A\|_F\) | 14.39081031 | 12.87371638 | 14.39314558 | 12.87680280 |
| \(d\|E\|_F/d\xi\) | 1.86012750 | 4.50488465 | 1.86166503 | 4.50729080 |
| \(\|A_\perp\|_F\) | 14.27008575 | 12.05979219 | 14.27224029 | 12.06218803 |
| \(\Omega\) (radians per ξ) | 3.73681665 | 3.03071192 | 3.73722497 | 3.03111789 |
| Angle between \(E(\kappa,\xi)\) and \(E(\kappa,0)\) | 0° | **9.639478°** | 0° | **9.640635°** |

The norm of the parameter-response tensor changes **+4.2006%** in the original seed and **+4.2030%** in the autonomous seed. The **direction** of that tensor nevertheless changes by about **9.64°** in the chosen matrix-space metric. At ξ=0, the transverse component accounts for ~99.16% of the *speed norm* \(\|A\|\), decreasing to ~93.68% by ξ=0.05. **These are not energy fractions.**

## Numerical integrity and ridge screening

- All 44 physical IVPs finish normally with the inherited tolerances.
- Projector idempotency error is at the level of floating-point roundoff (below 3×10⁻¹⁵ in the local run).
- Relative κ stencil differences within the historical interval are at most about 3.4×10⁻⁹, whereas ξ-gradient versus spline derivative differences reach approximately 1.3×10⁻⁴ relative. These are *diagnostic comparisons*, not rigorous truncation-error bounds.
- The old v18.50v three-point projector-gain values are reproduced by the same 3-point differentiation within ~2×10⁻¹¹ absolute; the new five-point gain differs by up to about 1.3×10⁻⁸ relative.
- The orientation-rate screen finds **no qualifying strict internal κ ridge** across the 79 sections in either seed, under the declared 5%-over-external-controls criterion. A smooth change in posture **is observed**, but a narrow-band activator is **not established**.

## Decision and limitations

**Classification: `FIXED_SEED_ANCHOR_FREE_PROJECTOR_DERIVATIVE_DIAGNOSTIC_NOT_MATERIAL_EDGE_OR_ACTIVATION_CERTIFICATE`.**

1. The primary sensitivity field does not inherit the forced V-shape zeros from two anchor distances.
2. In the chosen chart and finite grid, the sensitivity direction rotates appreciably while its norm changes more modestly.
3. The two independently fixed natural seeds show consistent trends, but their turn-relative ξ clocks are not a common absolute physical time.
4. The tensor derivative and its angular rate remain sensitive in principle to the observer and metric; they do not prove a material torsional flip, an intrinsic oscillator, or the existence of moving physical borders.
5. The 22×79 grid and finite horizon cannot exclude smaller, later or narrower parameter transitions.

The next scientifically distinct test would compare the **transport of this tensor-valued sensitivity field** under a candidate dynamical connection and a physically motivated metric, rather than treating its Frobenius angle as universal.
