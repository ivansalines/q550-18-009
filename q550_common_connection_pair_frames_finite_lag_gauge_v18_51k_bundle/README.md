# Q550 v18.51k — Common-Connection Pair Frames & Finite-Lag Gauge Audit

Scientific input: authenticated Q550 v18.51j server sendback, including the complete nested v18.51i/h/g/f/e genealogy and original two 10D physical seed IVPs. This version adds **no new physical IVPs** and uses the already-integrated material tangent transport.

## Run on the Linux server

```bash
cd /root/elab1/hysteresis
unzip q550_common_connection_pair_frames_finite_lag_gauge_v18_51k_bundle.zip
cd q550_common_connection_pair_frames_finite_lag_gauge_v18_51k_bundle
set -o pipefail
PYTHON_BIN=python3.13 bash run_on_server.sh 2>&1 | tee ../v18_51k_server.log
```

Requires Python 3.13 or a compatible Python 3 interpreter with NumPy, SciPy and Matplotlib; see `requirements.txt`. A complete original input ZIP is under `inputs/` and checked by the manifest.

## Scientific method

Read `MATHEMATICAL_PROTOCOL.md` and `SCIENTIFIC_DECISION_RULES.md` before interpreting the figures. The pairwise finite-time maps have moving source and target spectral frames. Both planes use the *same* ambient kinetic Cartesian flat metric connection, followed by independent **induced subbundle** polar lifts. These are geometric identifications of frames, not extra physical forces or new model generators.

- `results/connection_aligned_finite_lag_ledger.csv`: every measured finite interval, the two norm ratios, the new aligned and historical unaligned defects, the interference identity and independent gauge checks.
- `results/pair_frame_overlap_conditioning.csv`: adjacent-plane singular overlap, revealing whether the induced frame connection is well defined.
- `results/moving_chart_connection_covariance.csv`: nonorthogonal, xi-dependent ambient chart with its **metric and parallel map** transported correctly.
- `results/common_connection_pair_frame_transport.png`: lag comparison and strength ratio.
- `results/connection_adjoint_metric_sensitivity.png`: lag-one aligned defect across kinetic metric weights.
- `results/report.json`: complete machine-readable quality, observations, limitations and PASS/FAIL criteria.
- `SCIENTIFIC_REPORT.md`: interpretation of the authenticated local replay.
- `SOURCE_MANIFEST.json`, `SHA256SUMS_OUTPUT.json`: SHA-256 source and output verification.
- `reference/`: byte-exact historic runnable Python analysis sources from the j sendback.
- `scripts/`: v18.51k implementation and automatic sendback repackaging.
- `tests/`: independent synthetic connection/gauge and persisted-results tests.

`run_on_server.sh` runs source checks, independent tests, analysis, persisted-results validation, output manifest generation, and packs the full `q550_common_connection_pair_frames_finite_lag_gauge_v18_51k_bundle_server_sendback.zip` in the parent folder.

**Limitations:** No assertion of physical energy transfer, global material torsion, interval-certified spectral separation or universal reciprocity. Endpoint basis invariance is distinct from independence of physical metric. The former is tested; the latter is not certified. No 1/3 hypothesis is used.
