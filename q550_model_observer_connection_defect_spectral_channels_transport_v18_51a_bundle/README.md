# Q550 v18.51a — Model–Observer Connection Defect: Spectral Channels & Transport Audit

This is a **post-processing audit** of the user-authenticated **v18.50z server sendback**, not a new numerical integration of the Q550 physical state or its tangent flow.

## Scientific question

Given the independently computed model-induced skew off-block comparator `K_model` and the observable-projector canonical connection `K_canonical` in the **same shared Euclidean 10D chart**, follow the spectral channels of

```
W(xi) = K_model(xi) - K_canonical(xi)
```

Does the spectral discrepancy merely change intensity, or do its **rank-2 pair planes** rotate and couple as `xi` advances?

## Method

A real 10×10 skew-symmetric W has duplicated positive singular intensities. For each of the 79 nonuniform phase sections and each of the two natural-seed preparations, we calculate the SVD of W and its two dominant 2D orthogonal spectral projectors `Q_1` and `Q_2`. Projectors avoid arbitrary SVD signs and rotations within a degenerate pair. The third pair is about 1e-9 or smaller; its orientation is **not** interpreted.

We measure the largest principal angle from the initial rank-2 plane via the `arcsin` of its off-plane projection. The local inter-channel coupling is

```
mix_1_to_2 = ||Q_2 (dQ_1/dxi) Q_1||_F,
out_1 = ||(I-Q_1) (dQ_1/dxi) Q_1||_F,
fraction = mix_1_to_2 / out_1.
```

Time derivatives are taken from a cubic spline through the projector-valued samples and compared with a separate three-point nonuniform finite difference. All norms use the inherited 10D Euclidean chart, **not a certified kinetic metric**.

## Source and provenance

- `inputs/q550_model_generated_tangent_transport_canonical_observer_connection_v18_50z_bundle_server_sendback.zip`: original authentic z sendback, preserved byte-for-byte.
- The audit checks its ZIP CRC, source manifest (12 entries), output manifest (6 entries), and declared physical-integration success. It reads the 79-section 10D `K_model` and `K_canonical` matrices without unzipping the historical `runtime/` ancestry.
- The two branch labels mean **two natural initial seed preparations at the same midpoint κ0 = 0.1666331385421536**. These are NOT simultaneous measurements at distinct κ0 values.

## How to run

From `/root/elab1/hysteresis`:

```bash
unzip q550_model_observer_connection_defect_spectral_channels_transport_v18_51a_bundle.zip
cd q550_model_observer_connection_defect_spectral_channels_transport_v18_51a_bundle
set -o pipefail
PYTHON_BIN=python3.13 bash run_on_server.sh 2>&1 | tee ../v18_51a_server.log
```

The script verifies immutable inputs, performs synthetic tests, regenerates all derived figures and tables, runs semantic tests, writes a **separate results SHA-256 manifest**, and packages the sendback alongside this directory. Do not modify the launcher to select Python; use `PYTHON_BIN` as above.

## Contents

- `scripts/run_audit.py`: executed Python generator (entire numerical audit)
- `scripts/verify_source_manifest.py`: immutable source/input verifier
- `scripts/write_output_manifest.py`: hash regenerated outputs
- `scripts/pack_sendback.py`: archive only manifest-listed source/output artifacts
- `tests/test_geometry.py`, `tests/test_results.py`: synthetic / real output checks
- `results/spectral_channel_phase_ledger.csv`: 158 rows = 2 branches × 79 sections
- `results/spectral_channel_summary.csv`: end-to-end comparisons and checks
- `results/dominant_spectral_channel_projectors.npz`: both full rank-2 plane projectors and singular intensities on all sections
- `results/*.png`: three diagnostic plots
- `results/report.json`: exact machine-readable findings and caveats
- `SCIENTIFIC_DECISION_RULES.md`, `SCIENTIFIC_REPORT.md`: scope, definitions and interpretation
- `SOURCE_MANIFEST.json`, `SHA256SUMS_OUTPUT.json`: independent source/output integrity ledgers

## Scientific status

`AUTHENTICATED_SPECTRAL_PROJECTOR_CHANNEL_DIAGNOSTIC_NOT_PHYSICAL_MODE_OR_ENERGY_TRANSFER_CERTIFICATE`

The source is model-based, but neither the Euclidean metric nor the K_model skew comparator establishes a privileged physical connection. No physical transfer of energy, torsional flip, κ0 band activation, material memory or glass/polymer constitutive equivalence is claimed.
