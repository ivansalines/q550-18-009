# Q550 v18.50s — Principal-Angle Conditioning & Tangent-Integrator Convergence Audit

## Purpose

Check whether the small principal angle between the dynamically transported
7D kernel and the instantaneous analytic observer kernel is a robust numerical
consequence of the inherited Q550 dynamics, or an artifact of `arccos` rounding,
tangent integrator tolerances, step caps, or incomplete ODE integrations.

**This is a numerical diagnostic in the inherited Euclidean 10D chart.** It
does not certify a material kinetic metric, physical torsional flip, polymer
constitutive relation, material memory, or exact continuous-time angle.

## Provenance

`inputs/q550_differential_kernel_invariance_analytic_tangent_generator_v18_50r_bundle_server_sendback.zip`
is the authentic server sendback received after v18.50r, containing the
v18.50q sendback and the complete authenticated executable genealogy.

The runner checks every source and result SHA-256 of v18.50r, and through the
original r/q staging functions authenticates v18.50q. Its inherited structural
jet and driven 10D physical RHS prepare the initial state at each of the two
previously determined event sections.

The **100D fundamental matrix IVP is genuinely reintegrated** from the
analytic 10D variational generator (`J10` from the structural jet), not
interpolated from the parent CSV. Both κ₀ families are run independently.

The temporary genealogy is extracted only inside a temporary directory and
removed at completion; it is never included in the sendback ZIP.

## Independent principal-angle estimators

For orthonormal bases `K` (instantaneous observer kernel) and `Q` (transported
kernel), with `P=K Kᵀ`, the following calculate the maximum angle:

- `asin(sigma_max((I-P) Q))` — primary stable, *sin-based* estimator.
- `asin(||P-Q Qᵀ||_2)` — independent projector estimator.
- `acos(sigma_min(Kᵀ Q))` — historical overlap estimator; loses precision for
  angles close to zero. Its disagreement is explicitly reported.
- `atan2(sinθ, sqrt(1-sin²θ))` — another stable reporting identity.

All solver runs record `success`, `status`, `message`, `nfev`, `njev`, `nlu`,
`t_end`, `t_target` and endpoint equality. **An incomplete integration is
excluded from convergence statistics, even if it emits a plausible number.**

## Run on server

```bash
cd /root/elab1/hysteresis
unzip q550_principal_angle_conditioning_tangent_integrator_convergence_v18_50s_bundle.zip
cd q550_principal_angle_conditioning_tangent_integrator_convergence_v18_50s_bundle
set -o pipefail
PYTHON_BIN=python3.13 bash run_on_server.sh \
  2>&1 | tee ../v18_50s_server.log
```

This starts from the original archived solver genealogy. By default it runs
DOP853 and Radau, with tolerances `1e-8, 1e-10, 1e-12` and step caps of
`span/8` and `span/16`, for both κ₀ branches (24 tangent integrations).
Use `--tolerances 1e-8 1e-12` for the 16-run reference grid.

For a rapid check **without running the model**, use:

```bash
python3.13 tests/test_angle_conditioning.py
python3.13 scripts/run_audit.py --preflight-only
```

For a stricter one-off diagnostic near SciPy's tolerance floor, append
`--tolerances 1e-13 1e-14`. Such runs may issue an `rtol` clipping warning or
fail; the runner records actual completion and never treats failed runs as a
convergence point.

## Files

- `scripts/run_audit.py` — executable model replay, analytic tangent IVP and
  three independent angle estimators.
- `tests/test_angle_conditioning.py` — analytic known-angle and basis-gauge
  control independent of Q550.
- `results/principal_angle_integrator_convergence.csv` — entire solver scan.
- `results/parent_q_angle_comparison.csv` — authenticated original q angles and
  event interval per branch.
- `results/report.json` — decision-relevant summary, limitations, environment.
- `results/*.png` — cross method and tolerance comparison.
- `SOURCE_MANIFEST.json` — immutable original sources and parent bytes.
- `SHA256SUMS_OUTPUT.json` — regenerated result bytes, kept separate from source.

`run_on_server.sh` selects `PYTHON_BIN` from the environment, without changing
its bytes. The sendback is automatically written one directory above the bundle
and excludes temporary runtime and console log. Console log is kept separately
via the command above.
