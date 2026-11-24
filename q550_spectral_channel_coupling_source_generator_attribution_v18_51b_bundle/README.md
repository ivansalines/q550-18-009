# Q550 v18.51b — Spectral-Channel Coupling Source & Generator Attribution Audit

This is an executable, authenticated **post-processing** of the original Q550 v18.51a server sendback and its v18.50z, v18.50y and v18.50x ancestors. No Q550 physical IVP is rerun. Every reported rate is an evolution-coordinate (`xi`) diagnostic in the fixed common Euclidean 10D chart inherited from the model family.

## Scientific purpose

The v18.51a result resolved two dominant, stable rank-two spectral projectors `Q1` and `Q2` of the skew connection defect `W=K_model-K_canonical`. In v18.51b we ask how their **relative interplane motion** and **individual singular intensities** are attributed to the components of the time derivative of W.

The decomposition separates the canonical observer connection from the model-induced offblock connection; within the latter, a *product-rule split* separates the time change of the independently calculated analytic tangent generator `J10` from the change of the observed projector `P`. This is a **defined algebraic attribution**, not an independent causal intervention.

## Numerical provenance

- Parent: `inputs/q550_model_observer_connection_defect_spectral_channels_transport_v18_51a_bundle_server_sendback.zip`, SHA-256 stored in `results/report.json`.
- Nested v18.50z/y/x source and output manifest entries are authenticated in-memory. No large `runtime/` tree is extracted.
- The same midpoint `kappa0=0.1666331385421536` and the **two different historical natural-seed preparations** are used; they are not two different kappa values in this replay.
- 79 evolution sections per seed, `[0,0.05]`; 158 output rows. Time derivatives use a cubic spline on saved sections and an independent nonuniform five-point check.
- `scripts/run_audit.py` contains the actual numerical producer; `tests/` contains independent synthetic mathematics and semantic output tests.
- Runtime bytecode (`__pycache__`, `*.pyc`) is never a manifest source. The source and output manifests are separate.

## Server execution

```bash
cd /root/elab1/hysteresis
unzip q550_spectral_channel_coupling_source_generator_attribution_v18_51b_bundle.zip
cd q550_spectral_channel_coupling_source_generator_attribution_v18_51b_bundle
set -o pipefail
PYTHON_BIN=python3.13 bash run_on_server.sh 2>&1 | tee ../v18_51b_server.log
```

This writes `../q550_spectral_channel_coupling_source_generator_attribution_v18_51b_bundle_server_sendback.zip`. The separate log in the parent directory does not enter any manifest. Rerunning outputs refreshes only `SHA256SUMS_OUTPUT.json` and packaged results; immutable sources are verified without being changed.

## Generated outputs

- `results/report.json` — exhaustive numerical summary, numerical floors and scientific limitations
- `results/spectral_source_attribution_phase_ledger.csv` — all 158 sections and source/gap diagnostics
- `results/spectral_source_attribution_summary.csv` — comparison across two historical seeds
- `results/spectral_generator_attribution_blocks.npz` — source matrices and their exact sums, for the next audit
- `results/connection_source_interplane_transport.png`
- `results/generator_posture_spectral_strength_attribution.png`
- `results/spectral_numerator_gap_rate_balance.png`

## Safety of interpretation

Read `SCIENTIFIC_DECISION_RULES.md` before calling any mode a physical transfer. No new law of material memory, polymer rheology, torsional flip, or uniquely selected physical metric is established.
