# Q550 — v18.51h scientific report

**Pairwise Numerator–Gap Competition & Covariant Directionality Audit**

## Executive conclusion

The authenticated full 10D kinetic tangent data from Q550 v18.51e (inherited through f and g) supports a persistent numerical ordering of the ordered Riesz-projector drift channels: **5->4 has the largest raw covariant cross-rate among 20 directed channels at all 468 positive sampled sections** across two physical seed families and three kinetic-state balance conventions. The same result survives independent reconstruction through the exact rank-one complex numerator-gap identity. This remains a spectral/projector diagnostic, not material energy transfer or an observer-independent physical transfer law.

The **minimum complex eigenvalue gap between pairs 4 and 5 is exactly the same under direction reversal**. Thus the scalar pair gap alone cannot be the source of directed 5->4 versus 4->5 asymmetry. The asymmetry is resolved in the complex matrix numerator terms, their coherent cancellation, the source-projector normalization, and the declared nonorthogonal kinetic-state convention. This audit does not convert those algebraic factors into unique causal percentages.

## What was measured

- Parent: byte-verified v18.51g server sendback, containing v18.51f and v18.51e authentic source/output ancestry and two genuine physical seed IVPs.
- Sections: 78 positive-time sections per branch, six branches = **468** observations.
- Ordered channels: 5 source pairs x 4 target pairs = 20 per section, hence **9,360** resolved complex pairwise calculations.
- Kinetic similarity controls: four nonreference-`tau_ref` branches, 78 sections and 20 channels = **6,240** comparisons.
- Independent synthetic finite-perturbation test confirms the complex directed Riesz derivative identity and the distinction between common-frame covariance and raw Euclidean norm invariance.
- Scientific decision gates: **22 / 22 PASS** in the local Python 3.13 replay. Reproduction on a separate server should be checked from its sendback.

## Endpoint directional audit — xi = 0.05

| Seed | tau_ref | 5->4 | 4->5 | rate ratio | directed block norm ratio | source projector norm P4/P5 |
|---|---:|---:|---:|---:|---:|---:|
| original | 0.5 | 5.920056 | 3.898071 | 1.518714 | 1.794565 | 0.846286 |
| original | 1.0 | 6.302200 | 3.729568 | 1.689793 | 1.865645 | 0.905742 |
| original | 2.0 | 5.672042 | 4.552847 | 1.245823 | 1.354460 | 0.919793 |
| autonomous | 0.5 | 5.946045 | 3.933899 | 1.511489 | 1.783833 | 0.847327 |
| autonomous | 1.0 | 6.324498 | 3.765444 | 1.679616 | 1.853221 | 0.906322 |
| autonomous | 2.0 | 5.680683 | 4.596061 | 1.235989 | 1.343157 | 0.920212 |

The table is an **exact algebraic factorization of the measured rate ratio**: the product of the last two columns equals the directional rate ratio. It should not be read as a multiplicative conservation law or energy budget.

For the original seed at the endpoint, the shared complex pair-gap minimum is approximately **0.00507240347** regardless of kinetic scale, and the corresponding maximum among the four complex gap magnitudes is approximately **0.249681**. There is consequently no legitimate replacement of all four denominators by their minimum without explicitly marking it as a counterfactual.

For the original seed at `tau_ref=1`, the ratio of weighted termwise Frobenius sums (5->4 divided by 4->5) is **1.97755**, while the ratio of coherent cancellation factors is **0.94341**. Their product is the cross-block norm ratio **1.86564**, followed by the source-projector norm factor **0.90574** to give the observed rate ratio **1.68979**.

At `tau_ref=2`, the weighted termwise ratio is **2.03571** but the cancellation ratio falls to **0.66535**. The resulting block norm ratio decreases to **1.35446** and the final directed rate ratio to **1.24582**. This demonstrates why a numerator-only, gap-only, or naïve percentage interpretation would be misleading.

## Mathematical identity, numerical quality and limits

For `i != j`, let `R_a` be the rank-one biorthogonal complex eigenprojectors of `M`, and let `P_j` sum the conjugate pair. With physical `Mprime=B M`, the resolved directed block is

`Q_(j->i)=P_i [Pprime_j-[B,P_j]] P_j = sum_{a in j,k in i} lambda_k R_k B R_a / (lambda_a-lambda_k)`.

The **maximum normalized cross-block identity error** across all branches is approximately **1.85e-10**, the maximum absolute discrepancy relative to the independently archived v18.51g rate is **8.31e-7** (dominated by near-origin small-gap conditioning), and the worst positive-time complex pair gap across all pairs is approximately **9.47e-6**. The maximum common-`tau=1` frame cross-block relative error for `xi >= 0.001` is approximately **4.41e-9**; the corresponding raw norms are not invariant under the nonorthogonal kinetic scaling.

The results certify neither continuous-time gap isolation nor physical material torsion, hysteretic memory, unique phase-space kinetic metric, independent `kappa_0` activation, or real energy-transfer fractions. At `xi=0` there is tenfold spectral degeneracy. No new physical Q550 IVPs were run in this version. The earlier visual `1/3` hypothesis is retired.

**Decision:** PASS as a reproducible numerical pairwise spectral diagnostic. Next possible audit: separate oblique left-right eigenvector conditioning and metric-normalized directionality without assuming that the five instantaneous spectral planes are material invariant subspaces.
