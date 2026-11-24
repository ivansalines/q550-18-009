# Q550 — v18.51f: Finite-Time Spectral Pairing & Kinetic Similarity Transport Audit

**Post-processing of authenticated original Q550 trajectories; NOT a new IVP.**

The immutable parent is `inputs/q550_full_kinetic_tangent_generator_finite_time_cauchy_green_transport_v18_51e_bundle_server_sendback.zip`. It contains all 79 physical-cartesian kinetic material transports `M` for both original and autonomous 10D Q550 seed trajectories, their continually integrated 10D tangent jets `F`, and kinetic embeddings `L`. This version verifies the parent source and output hashes before using the tensors. The ancestor d→c→b→a→50z→y→x… genealogy remains nested and authenticated by the inherited report.

## Server

```bash
cd /root/elab1/hysteresis
cp /root/Downloads/q550_finite_time_spectral_pairing_kinetic_similarity_transport_v18_51f_bundle.zip .
unzip q550_finite_time_spectral_pairing_kinetic_similarity_transport_v18_51f_bundle.zip
cd q550_finite_time_spectral_pairing_kinetic_similarity_transport_v18_51f_bundle
set -o pipefail
PYTHON_BIN=python3.13 bash run_on_server.sh 2>&1 | tee ../v18_51f_server.log
```

`run_on_server.sh` authenticates all sources, runs synthetic geometry controls, calculates genuine Q550 finite-time spectral diagnostics, validates output rows, writes SHA-256 output hashes, and generates a sendback ZIP in `/root/elab1/hysteresis` with the matching root name.

Optional thresholds: `--imag-tolerance 1e-10 --spectral-gap-floor 1e-8`. The midpoint κ is inherited unmodified. No historical tuning and no `1/3` heuristic in PASS criteria.

## Outputs

`results/spectral_pair_ledger.csv`: 2×3×78×5=2340 pair records. `spectral_sections_ledger.csv`: 468 sections. `spectral_pair_transport_cross_coupling.csv`: 11550 interplane cocycle projections. `kinetic_similarity_covariance.csv`: 312 passive tau similarity checks. `original_autonomous_pair_comparison.csv`: 1170 seed comparisons. `spectral_branch_summary.csv`: six branch summaries. `report.json`, three plots and both manifests.

## Scientific interpretation

Positive-time matrices have five complex conjugate eigenpairs. At ξ=0, `M=I` and the decomposition is 10-fold degenerate. The finite-time eigenpairs are *not* five physical subsystems or five invariant loops. Real modal Riesz projectors are **oblique** and non-orthogonal; cross-pair projections are not physical energy fractions. There is no unique metric on the full phase state. See `MATHEMATICAL_PROTOCOL.md` and `SCIENTIFIC_DECISION_RULES.md`.
