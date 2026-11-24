# Q550 — v18.51h: Pairwise Numerator–Gap Competition & Covariant Directionality Audit

**Construction:** exact pairwise rank-one Riesz numerator-gap decomposition of the covariant drift from the full physically inherited Q550 10D kinetic tangent generator.

**Audit:** compare against authenticated v18.51g rates, verify synthetic finite-perturbation mathematics, isolate shared spectral gap versus matrix numerator/interference/oblique normalization, and test kinetic similarity in a common frame.

## Server commands

```bash
cd /root/elab1/hysteresis
cp /root/Downloads/q550_pairwise_numerator_gap_competition_covariant_directionality_v18_51h_bundle.zip .
unzip q550_pairwise_numerator_gap_competition_covariant_directionality_v18_51h_bundle.zip
cd q550_pairwise_numerator_gap_competition_covariant_directionality_v18_51h_bundle
set -o pipefail
PYTHON_BIN=python3.13 bash run_on_server.sh 2>&1 | tee ../v18_51h_server.log
```

The script replays the analysis of inherited genuine 10D data, regenerates all outputs and the SHA-256 output ledger, and writes

`../q550_pairwise_numerator_gap_competition_covariant_directionality_v18_51h_bundle_server_sendback.zip`

The source ZIP and the sendback have matching internal root directories. `PYTHON_BIN` may point to another installed Python with compatible dependencies in `requirements.txt`.

## What is included

- `inputs/` — the complete authenticated v18.51g server sendback, including the v18.51f and v18.51e ancestry and historical v18.51d chain.
- `reference/` — exact historical v18.51g main analysis source, checked against its ZIP ancestry.
- `scripts/run_audit.py` — reconstructed independent complex pairwise numerator-gap calculations and data checks.
- `tests/test_geometry.py` — independent synthetic four-dimensional perturbation and passive-similarity test.
- `tests/test_results.py` — scientific gates and output consistency check.
- `scripts/verify_source_manifest.py`, `scripts/write_output_manifest.py`, `scripts/pack_sendback.py` — provenance, output hashes and ZIP packaging.
- `results/report.json` — software, scientific controls, exact residuals, limitations and endpoint summaries.
- `results/pairwise_numerator_gap_ledger.csv` — 9,360 ordered source-target blocks with four-term spectral numerators, gaps, cancellations and the original rate replay.
- `results/pairwise_directionality_decomposition.csv` — 468 sections of the 5->4 / 4->5 comparison, exact factorization, shared gap and diagnostic counterfactual.
- `results/kinetic_common_frame_covariance.csv` — 6,240 cross-convention controls brought into a single tau=1 frame.
- `results/pairwise_rate_and_shared_gap.png`, `results/pairwise_numerator_cancellation.png`, `results/kinetic_directionality_convention_sensitivity.png` — diagnostic plots.
- `MATHEMATICAL_PROTOCOL.md`, `SCIENTIFIC_DECISION_RULES.md`, `requirements.txt`, manifests.

No original physical 10D IVP is recomputed in v18.51h; the parent v18.51e solver trajectory remains the authenticated source of truth. No active `1/3` heuristic.

## Interpretation in one sentence

The same unordered 4/5 eigenvalue gap is shared by 5->4 and 4->5, so a difference in their directed oblique Frobenius rates must involve the numerator/interference and source-projector geometry (and its declared kinetic convention), not the scalar minimum gap by itself.
