# Q550 v18.50v — Long-Horizon κ₀ Response & Activation-Threshold Audit

This executable experiment watches whether the proposed **very narrow dynamical
activator** behaves differently *while passing* the interval bounded by the
historical `κ_auto = 7π/132` and `κ_original = 1/6`. The phrase **"moving
tooth"** is a working observational metaphor, not a claimed physical structure.

Scientific focus: **watch the complete parameter/time response even if there
is no activation peak.** This is an extension of the controlled fixed-seed
v18.50u scan, NOT a new material law.

## Genealogy

`inputs/q550_kappa_narrow_band_common_seed_dynamic_scan_v18_50u_bundle_server_sendback.zip`
is the immutable real-server input. Its SOURCE_MANIFEST and output manifest are
verified first; then the ancestor 10D solver is reconstructed temporarily
for driven integrations. An ancestor runtime tree (which can exceed 1 GB) is
never included in the final sendback.

## Parameter and time design

- 22 κ values: 13 including the two endpoints, 9 external controls.
- Two distinct inherited natural turning preparations as fixed initial states.
- Every κ receives a **new complete** 10D DOP853 IVP, including the fixed-seed
  anchor because the original v18.50u baseline ends at ξ = 0.001092.
- Turn-relative time grid includes a dense early gate, a medium window through
  ξ = 0.0125, and a longer window through ξ = 0.05 (default).
- Drive shape is inherited beta:2:2, ramp ξ=0.24, clock fixed **within** each
  seed. Two seed clocks are not assumed to be the same physical clock.

## Actual dynamic measurements

At every (seed, κ, ξ), measure the driven 10D state, its RHS, the 4D normalized
structural observable, and its rank-three Jacobian 7D-kernel projector.
Store raw departures from the fixed-seed reference and norms of
**parameter derivatives before their norms**. This avoids the trivial
anchor-induced V of v18.50u. Full heatmaps and ridges are saved even when no
localized maxima are found.

## Run

```bash
cd /root/elab1/hysteresis
unzip q550_long_horizon_kappa_response_activation_threshold_v18_50v_bundle.zip
cd q550_long_horizon_kappa_response_activation_threshold_v18_50v_bundle
set -o pipefail
PYTHON_BIN=python3.13 bash run_on_server.sh 2>&1 | tee ../v18_50v_server.log
```

To inspect provenance only (no physical integrations):

```bash
python3.13 scripts/run_audit.py --preflight-only
```

Optional shorter pilot, still with genuine physical IVPs:

```bash
PYTHON_BIN=python3.13 bash run_on_server.sh --end 0.0125
```

`run_on_server.sh` verifies original sources, runs independent mathematical
tests, computes results, writes an **independent new output manifest**, and
packages a compact sendback alongside the extracted bundle. Select Python
using the `PYTHON_BIN` environment variable, NOT by editing the launcher.

## Output

- `results/long_horizon_kappa_response_ledger.csv` — every (κ, ξ) measurement,
  including state/RHS/observer/projector sensitivities and rank diagnostics.
- `results/moving_tooth_ridge_watch.csv` — κ maxima and screening at each ξ,
  including explicit "no qualified peak" records.
- `results/candidate_peak_events.csv` — only qualified interior candidates;
  can be empty, with a column header.
- `results/integration_completion.csv` — completion, evaluation counts,
  times for all 44 IVPs.
- `results/*.png` — heatmaps, trajectory/response snapshots, contrast histories.
- `results/report.json` — reproducible measured outcomes, caveats and design.
- `SOURCE_MANIFEST.json` / `SHA256SUMS_OUTPUT.json` — separate source and output
  SHA-256 checks. PNG metadata need not reproduce byte-for-byte between systems.

Source code and notes are in English. No physical activation is assumed.
