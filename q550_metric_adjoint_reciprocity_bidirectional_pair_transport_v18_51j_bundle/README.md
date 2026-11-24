# Q550 — v18.51j

**Metric-Adjoint Reciprocity & Bidirectional Pair Transport Audit**

This is a server-executable, source-authenticated numerical audit based on the
Q550 v18.51i **server sendback**. It preserves its nested h/g/f/e genealogy,
including the two historic 10D physical tangent integrations. It does not
perform a new physical IVP or fit any additional model parameter.

## Run

From the extracted root folder:

```bash
PYTHON_BIN=python3.13 bash run_on_server.sh 2>&1 | tee ../v18_51j_server.log
```

The runner verifies SHA-256 source identity and nested source and output
manifests, runs independent synthetic geometry tests, reconstructs all six
kinetic branches, verifies 20 result/algorithmic checks, writes output hashes,
and creates a sibling archive:

`q550_metric_adjoint_reciprocity_bidirectional_pair_transport_v18_51j_bundle_server_sendback.zip`

The root folder in the sendback matches the basename of the ZIP.

## Inputs and provenance

- `inputs/q550_projector_conditioning_separation_covariant_directionality_v18_51i_bundle_server_sendback.zip`
- `reference/i_projector_replay_v18_51i.py`: exact ancestor reconstruction implementation.
- `reference/h_pairwise_replay_v18_51h.py` and `reference/g_projector_replay_v18_51g.py`: byte-exact historical code.
- `SOURCE_MANIFEST.json`, `SHA256SUMS_OUTPUT.json`: source/output hashes.

## Outputs

- `results/metric_adjoint_reciprocity_ledger.csv`: 468 positive sections,
  same-metric 4↔5 adjoint rates and exact symmetric/antisymmetric interference.
- `results/finite_lag_bidirectional_transport_ledger.csv`: 1,362 real
  finite-time intervals of 1, 2 and 4 sampled sections, both forward-time
  pair channels and separately marked inverted-time controls.
- `results/passive_kinetic_metric_pullback_controls.csv`: 312 common-metric
  controls for tau=0.5 and 2 against tau=1.
- Three figures and `results/report.json` with all branch observations and
  numerical limitation statements.

## Semantic safeguards

The "forward" 5→4 and 4→5 channels are *both* measured in increasing time.
Time reversal is a distinct operation, implemented using the inverse
propagator and reported in different columns. An adjoint comparison within a
kinetic metric is not itself a time reversal or physical energy transport.
Absolute rates, reciprocity defects and source-condition measures depend on the
chosen kinetic state metric. Covariance is checked only after pullback to the
same tau=1 metric. At xi=0 the finite-time spectrum is degenerate, so
spectral pair projectors are not claimed there. The historic 1/3 hypothesis
is not used as a decision gate.
