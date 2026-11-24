# v18.51d — Scientific decision rules

1. **Construction before audit:** use the exact historical Q550 kinetic energy and v18.49h `kinetic_metric.py` (source bytes SHA256 `29bef2c91899a9da46bc8c9159b89c70362f505e0adead3f814c487a9a17bb1a`). Never infer a physical kinetic metric from the v18.51c Jacobian Gram alone.
2. **Common physical states:** recompute both independently prepared seed trajectories at the same midpoint κ₀ used in the authenticated v18.50z/y/x. Their natural seed differences are not a κ₀-pair experiment.
3. **Conventional state metric:** `G=(DH diag(shared_scale_10d))^T(DH diag(shared_scale_10d))`, and `tau_ref∈{0.5,1,2}` MUST be varied. A unique physical phase-space metric is NOT established.
4. **Connection compatibility:** check `Gprime≈Gamma.T G+G Gamma`, `Gamma=L^-1 Lprime`; independently check metric time differentiation.
5. **Frame-rate contribution:** for `W=K_model-K_canonical`, compare its material Cartesian skew reduction. The kinetic frame motion must be a separate source, not silently combined with model or canonical components.
6. **Spectral isolation:** require a positive gap for the first and second rank-two eigenprojectors in the declared kinetic metric frame; record new secondary modes and condition numbers. Failure is an informative outcome.
7. **Passive chart covariance:** a constant invertible change of observer coordinates, when applied consistently to `G`, `L`, and `W`, must leave the material Cartesian reduced operator identical.
8. **Attribution classification:** if canonical signed source dominance persists for all declared tau_ref, report tested-family persistence only. If not, report its dependence on the state metric convention explicitly. Negative signed fractions are allowed.
9. **Numerical methods:** spline derivatives of 79 nonuniform sections are not continuum derivative certificates; original kinetic base energy agreement is checked against physical components, and model jet is independently regenerated.
10. **Genealogy:** no `.pyc` or `runtime/` in source manifests, source ZIP/directory root must match; manifests for immutable sources and generated outputs must be separate. No real Q550 dynamics are altered.
