# Q550 v18.51i — Scientific report

**Title:** Projector Conditioning Separation & Covariant Directionality Audit  
**Status:** Complete local numerical replay, 19/19 scientific algorithmic and genealogy checks passed. A separate synthetic geometry test and regenerated-result test passed. Server replay pending.  
**Input:** authenticated original v18.51h server sendback, including v18.51g/f/e lineage and the original two physical 10D seed integrations. No independent physical model was re-integrated.

## Main result

The directed 5->4 dominance remains present after restricting the exact off-diagonal covariant projector-drift block to the true orthonormal right eigenspaces and removing the historical source-projector Frobenius denominator. For every positive sampled section of both original and autonomous seeds, and each of tau_ref=0.5,1,2, the restricted 5->4 channel is not only stronger than the reverse 4->5 channel but also the strongest of all 20 ordered pairwise restricted channels: **468 of 468**.

Original-seed endpoint at xi=0.05:

| tau_ref | historical oblique ratio 5->4/4->5 | new restricted ratio | ambient extension ratio | source-condition ratio |
|---:|---:|---:|---:|---:|
| 0.5 | 1.518714 | 1.596846 | 1.123818 | 0.846286 |
| 1.0 | 1.689793 | 1.706214 | 1.093441 | 0.905742 |
| 2.0 | 1.245823 | 1.328822 | 1.019294 | 0.919793 |

Autonomous-seed restricted endpoint ratios: 1.589410, 1.696504, 1.323502 respectively. Each original ratio factors exactly as `restricted * ambient_extension * source_condition`, with the condition factor defined as C_4/C_5.

This separates **one specific projector-conditioning artifact**; it does not remove all effects of nonorthogonality of the right eigenspaces or the generator. The restricted channel still depends on the chosen inner product, and it is not a physical flux. The principal-angle comparison likewise changes with tau_ref.

## Quantitative quality

- Maximum crossblock reconstruction relative residual from the rank-two restricted matrix: **5.32e-12**.
- Maximum exact rate-factor residual: **1.78e-15**; maximum direction-ratio factor residual: **1.33e-15**.
- Historical raw-rate replay discrepancy: **8.30e-7**; directional ratio discrepancy **7.49e-7**, influenced by initial narrow eigenvalue gaps and independently recorded rather than hidden.
- Same-metric kinetic similarity after pullback to tau=1: maximum restricted-rate absolute mismatch at xi>=0.001 **7.60e-9**. The all-positive-section maximum is **7.31e-7**, reflecting the initial spectral conditioning.
- All six branches, 468 section summaries, 9,360 directed restricted block measurements, and 624 paired kinetic-similarity controls are written to CSV.

The synthetic independent test confirms that nonorthogonal passive chart transformation changes a naive Euclidean directed rate while the transported-metric right-subspace restricted core remains invariant.

## Interpretation

The numerical directional persistence is not only a denominator artifact of the historical oblique Frobenius rate. The evidence is stronger *within the declared observation protocol*, but not a certificate of an observer- or metric-independent physical directionality. Spectral labels 4 and 5 are continued from the positive-time resolved branches; the identity section remains degenerate and cannot be assigned five unique planes. The result has no claimed implication for physical energy transfer, a universal torsion, or an independent Q550 material memory law.

## Next empirical discriminator

A future test might perturb the **physically justified** kinetic-state inner product more broadly, or directly transport time-dependent orthonormal frames in the pair planes and compare the 5->4 restricted channel to a common material Lagrangian metric. Such a test must distinguish a metric change from a passive chart change. The local v18.51i result by itself cannot settle the existence of a unique physical metric.
