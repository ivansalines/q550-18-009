# Q550 v18.51c — Model-Gram Metric & Spectral-Source Robustness Audit

**Scope:** Authenticated post-processing of v18.51b spectral-channel source attribution, with the canonical model and observer matrices inherited through v18.51a → v18.50z → v18.50y → v18.50x. No new Q550 physical IVPs.

## Research question

Does the signed interplane attribution seen in v18.51b survive a change from the inherited Euclidean 10D observer metric to regularized positive-definite metric families **constructed from the genuine model tangent Jacobians**?

The result can test robustness under *declared model-derived observer metrics*, not independently establish the system's physical kinetic metric or a material cause.

## Geometry and method

The same midpoint kappa is used for both historical seed preparations. Build a shared model-Gram metric

`G_alpha(xi) = I + alpha*(J_original(xi).T @ J_original(xi) + J_autonomous(xi).T @ J_autonomous(xi))/(2*lambda_max(G_J(0)))`.

Frozen comparisons use its xi=0 value with alpha=0, 0.1, 1, 4; an evolving alpha=1 metric uses the contemporaneous model Jacobians. This normalizes eigenvalues of the frozen metric into `[1,1+alpha]` and fixes the metric before looking at source-contribution outcomes.

For each metric compute `L=sqrt(G)` and the skew-symmetric Euclidean representation of the metric-skew defect, `W_G=skew(L @ (K_model-K_canonical) @ inv(L))`. Its dominant eigenprojectors are drawn from `H_G=-W_G@W_G`, and the off-block rate uses the spectral-gap identity. Algebraically separate sources from (1) `dJ`, (2) `dP` posture, (3) `-dK_canonical`. When `G(xi)` moves, include (4) the independent whitening-rate commutator.

The comparison is intentionally **not** invariant under choosing a different metric, but it **must** be invariant under a passive change of coordinates when the operator and metric are transformed together. Tests cover both requirements.

## Execute on server

```bash
cd /root/elab1/hysteresis
unzip q550_model_gram_metric_spectral_source_robustness_v18_51c_bundle.zip
cd q550_model_gram_metric_spectral_source_robustness_v18_51c_bundle
set -o pipefail
PYTHON_BIN=python3.13 bash run_on_server.sh 2>&1 | tee ../v18_51c_server.log
```

`run_on_server.sh` verifies the **immutable source manifest**, runs tests, regenerates eight results, writes a separate result manifest, and packages `../q550_model_gram_metric_spectral_source_robustness_v18_51c_bundle_server_sendback.zip` without any `runtime/` tree or Python cache. The ZIP filename and root folder deliberately match.

## Outputs

- `results/metric_spectral_source_phase_ledger.csv`: 790 model/metric/section observations.
- `results/metric_spectral_source_summary.csv`: ten seed×metric comparisons.
- `results/passive_chart_covariance_control.csv`: non-orthogonal passive-chart invariance.
- `results/weighted_spectral_channel_projectors.npz`: selected skew defects and 10×10 rank-two spectral projectors.
- `results/metric_attribution_comparison.png`: signed canonical vs model attribution.
- `results/metric_spectral_channel_emergence.png`: dominant and secondary spectral strengths.
- `results/moving_metric_source_ledger.png`: explicit contribution of a moving metric.
- `results/report.json`: quantitative findings, caveats, environment and tests.

## Reproducibility and scientific limits

The parent sendback is retained unchanged under `inputs/`, with a verified full genealogy. Python scripts in `scripts/` are executable source; do not manifest `.pyc` or `__pycache__`. Spline-based time derivatives of the inherited 79 nonuniform sections are not interval-certified. The metric-skew construction defines a particular observer response to the metric; another physically motivated metric may yield different attributions. See `SCIENTIFIC_DECISION_RULES.md` and `SCIENTIFIC_REPORT.md`.
