# Scientific report — Q550 v18.50t

**Title:** Paired-κ₀ Phase-Aligned Edge Motion & Projector Separation Audit  
**Classification:** `PAIRED_PARAMETER_AND_INITIAL_STATE_SENSITIVE_10D_OBSERVER_PROJECTOR_DIAGNOSTIC_NOT_DYNAMIC_ACTIVATION_BAND_CERTIFICATE`

## Hypothesis under test

Two close κ₀ choices might trace a pair of dynamically moving edges, possibly defining a very narrow activation band. The objective is to test their **relative geometry**, not to infer a physical boundary from visual similarity.

The authenticated v18.50s ancestry provides original κ₀=`1/6` and autonomous κ₀=`0.16659961041764054` (`7π/132` within displayed precision). The parameter spacing is approximately `6.70562490261e-05`.

## Analytic observable and shared frame

For a normalized four-vector observer `d(y) = u(y)/||u(y)||`, the analytic tangent Jacobian `B = ∂d/∂z` obeys `d^T B=0`. On the sampled trajectories it has numerical rank three, giving two independently defined seven-dimensional nullspaces in the physical ten-dimensional tangent space.

We use **one** comparison chart formed by the componentwise maximum of both natural preparation scales and 1, with the same inherited observer weights for both. Each Jacobian is correctly converted from its inherited branch chart. Comparison in raw physical units is reported separately because the Euclidean projector metric changes under nonorthogonal rescaling.

## Results from the completed authoring replay

- Authentic parent s: 11 source file digests, 6 result file digests and 24 completed tangent integrator runs authenticated.
- Two genuine natural-state preparations and two Q550 driven 10D integrations were completed.
- 129 common turn-relative ξ sections, 65 gate-fraction sections and 17 raw-coordinate sensitivity sections were evaluated.
- In the shared chart, the maximum inter-branch kernel principal angle across the common-offset interval ranges from **0.008105476328° to 0.008107299520°**.
- The corresponding projector operator gap decreases from **0.000141499069600** to **0.000141467248895** (a change of about `-3.18e-8`, approximately `-0.0225%` of the initial gap) over ξ in `[0,0.001092]`.
- There are **zero sign changes of the sampled first-difference slope** of the gap and no prominent interior extrema under the predefined test; the decimated grid agrees. This interval contains **no sampled evidence for an oscillation of inter-branch separation**.
- At the first common-offset sample, the three potentially nonzero principal angles are approximately **0.00810730°, 0.00393499°, 0.00007060°**. The remaining ≥4 angles are mathematically zero for dimensional reasons.
- The instantaneous **parameter-only** swap at the original state has an average projector gap **0.0001810590**, while the **state-only** comparison at original κ₀ has an average gap **0.0000738701**. The full paired gap is only ≈`0.00014148`; state differences therefore alter and partly counteract the parameter-only effect in this specific comparison. These norms are *not* linearly additive.
- Event-normalized parities and stationary points give a paired angle around **0.00809465°–0.00809480°** (not exactly the same as common-ξ alignment).
- The largest measured relative clock-phase mismatch across the common-ξ interval is about **2.71e-7** in inherited clock units. Common turn-relative ξ is therefore not a perfectly matched physical phase.
- The raw-physical-coordinate chart yields a different gap around **0.000156344–0.000156346**, confirming chart dependence.
- The independent stable principal-angle/projector identity discrepancy was at most approximately **3e-16**; sampled analytic observer third singular values remain above ~**0.4873**, with rank three.

## Interpretation

**Supported:** the two κ₀ choices lead to distinct, smoothly varying kernel projectors in a shared 10D chart, and the relative separation can be measured. The counterfactual probe reveals a meaningful separation between immediate parameter sensitivity and preparation-state sensitivity.

**Not supported by this window:** an oscillating separation or narrow-band dynamical activation. No pair of alternating interior extrema was observed, and no continuous-κ sweep or independently defined activation threshold was run. The distance is slightly monotone over this short interval. Absence of extrema in the samples is not an interval proof of absence of faster fluctuations.

Two nearby parameter choices alone do not establish that they are literal edges of an activation region. A future audit should dynamically sweep several intermediate/exterior κ₀ values under common initial conditions, define an activation observable before scanning, and test widening or narrowing with observation interval and perturbation amplitude. No polymer constitutive equivalence is asserted.

## Scope and provenance

Original solver and analytic structural jet from the authenticated predecessor genealogy are replayed, not replaced by a fitted model. Counterfactual Jacobian evaluations at crossed κ₀ use existing physical states, not reintegrations under crossed parameters. The source and output manifests are independent; the long nested provenance is staged only temporarily.
