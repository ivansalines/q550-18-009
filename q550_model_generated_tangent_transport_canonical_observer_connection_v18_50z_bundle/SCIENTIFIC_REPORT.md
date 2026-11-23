# Scientific report — Q550 v18.50z

**Model-Generated Tangent Transport vs Canonical Observer Connection Audit**

## Question

Does the projector-canonical connection `Kobs=[Pdot,P]` from v18.50y agree with a transport generated *independently from the original Q550 dynamical Jacobian*, on the same seed, κ and evolution interval? What happens to the parameter-sensitivity tensor `E=∂κP` when compared in these frames?

## Authentic inputs and computation

- SHA-256-authenticated **v18.50y server sendback**, including the **v18.50x server sendback** with all ten-by-ten `P` and `E` matrices. Authentication of y: 12 source, 8 output entries; x: 12 source, 11 output entries. No historical file is changed.
- The genuine historical Q550 model and its analytic 11D structural jet `(F,J,H)` were staged via authenticated model ancestry. The first ten states are the actual externally driven 10D RHS, and the tangent generator is the physical jet's upper-left 10×10 block, transformed into the **shared normalized chart** used by x/y.
- Two freshly integrated Q550 driven 10D midpoint-κ trajectories, one for each historical fixed natural seed. Midpoint κ = **0.1666331385421536**; common ξ interval `[0,0.05]`; **79** original sampled sections, **157** analytic-J interpolation nodes per seed. The midpoint is the SAME parameter for the two seed preparations; the seed preparation itself differs.
- The model tangent fundamental operator obeys `Phi'=J10 Phi`. Both a 79-node and a 157-node interpolated analytic-jet model are integrated to control interpolation sensitivity. We also integrate an **independent skew crossblock model frame**. These auxiliary matrix IVPs are distinct from the two newly integrated physical trajectories.

## Distinguish the three model/observer operations

Let `P` be the observed 7D orthogonal kernel projector, `Q=I-P`, and `J` the independently computed physical tangent generator in the shared chart.

```
Kobs  = [Pdot,P]
Pdot_model = Q J P + P J^T Q
Kmodel = Q J P - P J^T Q
Dobs E = Eprime - [Kobs,E]
Dmodel E = Eprime - [Kmodel,E]
Phi' = J Phi
```

`Kmodel` is an *orthogonal crossblock reduction of J* using the instantaneous observed P; it is **not** the full model tangent transport and is not a privileged material spin. For that reason the study ALSO tracks the actual nonorthogonal Phi, its transported kernel plane, and the polar factor of Phi as another independently defined (but metric-dependent) readout. No connection is fitted to E.

## Numerical findings

### Endpoint rotation of the exact same sensitivity E, ξ=0 to 0.05

| Observer frame | Original seed | Autonomous seed |
|---|---:|---:|
| Fixed shared 10D chart | 9.639478022° | 9.640634814° |
| Canonical projector-horizontal transport from y | **8.516607799°** | **8.517357765°** |
| Model-J induced skew offblock transport | **14.639920929°** | **14.642384170°** |
| Polar rotation of nonorthogonal model fundamental Phi | 14.081066177° | 14.083314030° |

**These angles are not additive portions of a physical rotation.** The marked difference between 8.52° and 14.64° shows that the independently defined transports do **not** produce the same relative posture of E in the declared Euclidean common chart.

### Transport-rate discrepancy and full 7D-plane mismatch

| Quantity | Original start → endpoint | Autonomous start → endpoint |
|---|---:|---:|
| `||Kobs-Kmodel||F` | 5.898956 → 6.105700 | 5.900388 → 6.107201 |
| `||Pdotobs-Pdotmodel||F` | 5.898956 → 6.105700 | 5.900388 → 6.107201 |
| `||Pobserved-P(Phi·ker(P0))||F` | 0 → **0.298746763** | 0 → **0.298818231** |
| `cond(Phi)` at ξ=0.05 | **1.329174** | **1.329173** |
| Canonical angular rate of E at endpoint (rad/ξ) | 2.692526 | 2.692745 |
| Model crossblock angular rate of E at endpoint (rad/ξ) | 5.014858 | 5.015695 |

The accumulated 7D-plane gap is not zero at ξ=0.05, and is substantial compared with the much shorter earlier v18.50q/r gate. This wider horizon is **not** an extrapolation of the short-gate angle 0.00215149°. The measured gap is a comparison of two physically distinct subspace trajectories: an observer-reconstructed kernel P(ξ) and the original tangent flow acting on ker(P(0)).

## Controls, conditioning, limitations

- Recomputed projector P from the authentic analytic observer/physical state agrees with the stored x projector to Frobenius difference **≤3.02×10⁻¹⁴** at checked sections. Original structural jet's first ten entries agree with the actual driven RHS to relative error **≤1.48×10⁻¹⁵**.
- `Kmodel` is skew; its commutator with P reproduces the model-induced orthogonal projector rate with error **≤4.68×10⁻¹⁵**. Canonical spline Pdot has a finite projector-kinematic residual up to **3.56×10⁻⁷**, which must not be mistaken for material leakage.
- The two interpolations of J (79 vs 157 analytic samples) give an endpoint full-Phi Frobenius difference **≤2.19×10⁻¹³**. This is a **consistency check**, not a rigorous continuous integration error bound. The full fundamental matrices have moderate conditioning (~1.33 at the sampled endpoint).
- The original v18.50r independently checked `J10` against finite differences of the driven 10D RHS. This audit uses the same analytic 11D structural-jet construction on its longer midpoint path; it does not claim a third-derivative proof or interval verification.
- The shared Euclidean chart was inherited from v18.50x; **a physical kinetic metric is not derived**. The polar decomposition and orthogonal crossblock projection depend on this metric. A general time-dependent coordinate change must transform both connection and metric for invariant comparisons.
- Nothing here establishes a physical torsional flip, two material edges, κ narrow-band activation, material memory, universal observer-independent holonomy, or a glass/polymer constitutive law.

**Scientific classification:** `AUTHENTICATED_MODEL_TANGENT_VS_OBSERVER_GEOMETRIC_TRANSPORT_DIAGNOSTIC_NOT_MATERIAL_CONNECTION_CERTIFICATE`.

## Next discriminating question

Instead of promoting one of the two angles as material, examine the **offblock source of the discrepancy** `Pdot_observer-Pdot_model` in the common chart, its singular values and preferred subspaces, and test how its composition changes under an independently justified kinetic metric. This would measure the orientation of the transport discrepancy itself, not force a symbolic physical interpretation onto an observer-based quantity.
