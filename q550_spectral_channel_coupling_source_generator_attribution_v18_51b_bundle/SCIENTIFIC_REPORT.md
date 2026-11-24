# Scientific report — Q550 v18.51b

**Spectral-Channel Coupling Source & Generator Attribution Audit**

## Question

The v18.51a parent found a pair of dominant two-dimensional spectral planes rotating approximately 9° on the interval `xi ∈ [0,0.05]`, with roughly 92% of the first plane's out-of-plane rate pointing toward the second, while the first singular strength increased and the second decreased. What terms in the inherited Q550 matrices sustain these **different** developments? Is the interplane motion attributable to the change in the model-derived tangent generator, to the posture of the observed projector, or to the canonical observer connection? Does the changing spectral gap explain the diminishing interplane rate?

## Parentage and scope

The input is the actual **v18.51a server sendback** containing the original v18.50z tensor replay, which itself contains the v18.50y and v18.50x projector results. All manifest hashes from these four direct ancestors are verified in memory. No new Q550 physical or tangent integration is performed in v18.51b.

The two branches are **different natural-seed preparations** evaluated at the **same** midpoint κ₀ = `0.1666331385421536`. This is not a simultaneous comparison of two κ₀ values. We inherit the fixed common Euclidean 10D chart and 79 nonuniform evolution sections per branch.

## Exact spectral attribution

Use `W = K_model - K_canonical` (real skew symmetric), and `H = -W²`. Its two dominant rank-two projectors `Q1` and `Q2` from v18.51a have eigenvalues `lambda_i = sigma_i²`. They remain separated throughout the interval. The projector derivative identity is

```
Q2 Q1' Q1 = Q2 H' Q1 / (lambda1-lambda2)
```

Since `K_model = (I-P)JP - PJᵀ(I-P)`, a product rule gives independent **algebraic source terms** in `K_model'`: change of model generator `J'`, and change of observed projector posture `P'`. Differentiating `-K_canonical` gives the third source. Their matrix sum reconstructs the interplane velocity, while the pair strengths use `sigma_i' = tr(Q_i H')/(4 sigma_i)`.

There is a useful distinction between (i) changes of `sigma_i` and (ii) the interplane motion `||Q2 Q1' Q1||_F`: the two observables can have very different source balances.

## Numerical results — original seed

At `xi=0`:

| Source | Contribution to `sigma1'` | Contribution to `sigma2'` | Interplane block Frobenius norm |
|---|---:|---:|---:|
| Generator drift (`J'` inside `K_model'`) | +5.288624 | +0.028448 | 0.781982 |
| Observed-projector posture (`P'` inside `K_model'`) | −1.577663 | −1.050003 | 1.303974 |
| Canonical observer connection (`−K_canonical'`) | −0.724730 | +0.322355 | 2.962213 |
| **Total spectral strength derivative** | **+2.986231** | **−0.699200** | **3.777137 total interplane rate** |

**Important:** the last column contains *norms of different source matrices*. The total (3.777137) is the norm of their **matrix sum**, not the sum of listed positive norms.

The two model terms combine to a block norm 1.416424. The canonical source has block norm 2.962213. Signed projections of the three blocks onto the total block account for about **19.41% generator drift**, **6.87% projector posture**, and **73.72% canonical connection**. These fractions are algebraic projections, not energy fractions. The total model contribution is ≈26.28% in this signed-projection convention.

At `xi=0.05`, interplane block norm declines to 2.642368. The model-source norm is 0.960316 and the canonical-source norm 2.256944; signed canonical projection rises to about 79.87%. The first pair's singular strength continues increasing and the second decreasing.

## Numerator versus spectral gap

The spectral gap `lambda1-lambda2` increases from **12.421534** to **13.944422** (original seed). At the interval start:

```
(log ||Q2 H' Q1||)'       = -3.115525 per unit xi
-(log (lambda1-lambda2))'= -2.034204 per unit xi
(log interplane rate)'   = -5.149729 per unit xi
```

Thus the shrinking interplane rate is caused **algebraically** by both a decreasing spectral numerator and a widening denominator. The same qualitative ordering is seen in the autonomous seed. This is a numerator-gap decomposition, **not a causal counterfactual**.

## Two preparations agree on the qualitative result

The autonomous seed starts with interplane rate **3.775384**, model-source norm **1.416282** and canonical-source norm **2.960679**, and ends with **2.641293**, **0.960250** and **2.256029**, respectively. The near agreement does not mean the two trajectories or seed preparations are identical.

## Numerical controls and limits

- 158 sections in total. Nine explicit semantic/math controls are checked after numerical replay, in addition to two independent synthetic algebra tests.
- The spectral projector source identity reconstructs the direct parent derivative within relative residual **below 5×10⁻⁷** on the saved samples.
- `K_model'` reconstructed by the analytic product rule matches the saved-time spline derivative within relative residual **below 8×10⁻⁸**.
- An independent local five-point stencil versus the cubic spline shows a maximum relative discrepancy **about 3.0×10⁻⁵**, concentrated near the inherited grid-density transition at approximately `xi=0.001092`. This is explicitly visible in the ledger.
- The tiny third singular pair is not treated as a stable physical plane.
- No physical kinetic metric, globally unique observer connection, energy transfer, material causality, or memory certificate is inferred.

## Scientific classification

**`AUTHENTICATED_NUMERICAL_SPECTRAL_SOURCE_IDENTITY_NOT_UNIQUE_CAUSAL_OR_MATERIAL_ENERGY_ATTRIBUTION`**

This audit has separated *what changes the strength of the two channels* from *what moves their planes*. It has not established that any one source is a privileged physical mechanism. The next useful control would test whether the observed attribution is stable under another justified metric/observer and under direct perturbations of the model's tangent-generator evolution, rather than relying only on the chosen product-rule decomposition.
