# Q550 v18.50z — Model-Generated Tangent Transport vs Canonical Observer Connection Audit

This test addresses the open question from v18.50y: **Does the original dynamical Jacobian carry the rank-seven observer kernel, and its κ sensitivity, in the same way as the canonical observer-projector connection?**

The parent is the **authentic v18.50y server sendback** (it embeds the authenticated v18.50x tensors and model genealogy). The audit authenticates source and result hashes, reconstructs the genuine Q550 solver, runs **two new physical 10D midpoint-κ trajectories** (one per historical natural seed), samples the analytic physical structural jet (F,J,H) at 157 points per seed, and integrates the full nonorthogonal tangent fundamental matrix Phi with two interpolated-jet resolutions. It also integrates two independent auxiliary orthogonal-frame ODEs for a model-induced crossblock connection.

The outputs compare the same E tensor in four predeclared frames: fixed chart, canonical observed-kernel horizontal frame, orthogonalized model-J crossblock frame, and the polar factor of the full model tangent Phi. Only the latter two use the true model Jacobian; both nevertheless depend on the chosen common Euclidean state chart.

**Mathematics:**

```
K_obs  = [Pdot, P]
Pdot_J = (I-P) J P + P J^T (I-P)
K_J    = (I-P) J P - P J^T (I-P)
D_obs E = Eprime - [K_obs, E]
D_J E   = Eprime - [K_J, E]
Phi' = J Phi,  Phi(0)=I
```

No frame is fitted to E; the canonical frame comes from P, while K_J and Phi come from the independent full analytic tangent J. `K_J` uses P to extract only the off-block movement, so it is **not** the complete model connection.

## Server

```bash
cd /root/elab1/hysteresis
unzip q550_model_generated_tangent_transport_canonical_observer_connection_v18_50z_bundle.zip
cd q550_model_generated_tangent_transport_canonical_observer_connection_v18_50z_bundle
set -o pipefail
PYTHON_BIN=python3.13 bash run_on_server.sh \
  2>&1 | tee ../v18_50z_server.log
```

This reconstructs the original solver through a temporary, automatically deleted directory. Historical ancestry can temporarily require ~1.5 GB disk space; the resulting ZIP **excludes** that temporary tree. To inspect results without the expensive replay, read `results/report.json`, `results/model_vs_canonical_transport_ledger.csv` and `results/model_vs_canonical_centerline_tensors.npz`.

The script creates `../q550_model_generated_tangent_transport_canonical_observer_connection_v18_50z_bundle_server_sendback.zip` after tests and validation, with the exact original parent, sources, results and source/output SHA-256 manifests.

## Files

- `scripts/run_audit.py`: actual executable scientific analysis with authentic model reconstruction and validation.
- `scripts/verify_source_manifest.py`, `write_output_manifest.py`, `pack_sendback.py`: reproducible integrity pipeline.
- `tests/test_transport_geometry.py`, `test_output_semantics.py`: algebra and numerical result checks.
- `results/*.csv`, `*.npz`, `*.png`, `report.json`: measured data, complete selected tensor data and visual diagnostics.
- `SCIENTIFIC_REPORT.md`, `SCIENTIFIC_DECISION_RULES.md`: findings, limits and predeclared interpretation.
- Input ZIP in `inputs/`: original v18.50y *server* sendback; deeper historical artifacts are nested and certified inside it.
