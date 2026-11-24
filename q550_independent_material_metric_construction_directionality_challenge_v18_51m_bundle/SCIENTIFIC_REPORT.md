# Q550 v18.51m — Scientific report

## Construction first — and a genuine negative robustness outcome

This audit constructs a **dynamical observability metric** from the authentic v18.51e Q550 full 10D tangent propagator (authenticated in the v18.51l sendback). It measures changes in physical Cartesian output position `Q` or velocity `V` along the actually sampled trajectory; the primary observation uses position with Gaussian width `h=0.025` over `xi∈[0,0.05]`. This is a distinct operational metric, not another `tau_ref` rescaling of the original phase-state kinetic Gram. It is physically motivated by *measurable configuration displacement* but **not** established as a unique Lagrangian or observer-independent material metric.

## Main negative result

The inherited kinetic metric had `||5→4|| > ||4→5||` in all 610 fixed Q550 material observables (156 instantaneous + 454 finite-lag) at `tau_ref=1`. The new position-output observability metric reverses the norm ordering in **all 610/610** of those exact same fixed material observables, for the two authentic seeds. Nothing changes in the original physical Q550 orbit, material tangent generator, propagator, right Riesz planes or oblique Riesz projectors. Only the measuring inner product changes.

| Seed | Observable | New 5→4 / 4→5 minimum | Maximum | Reverse count |
|---|---|---:|---:|---:|
| original | instantaneous | 0.331307 | 0.542830 | 78/78 |
| original | finite_lag | 0.331236 | 0.536625 | 227/227 |
| autonomous | instantaneous | 0.331961 | 0.545546 | 78/78 |
| autonomous | finite_lag | 0.331889 | 0.539274 | 227/227 |

Across all seven declared output/window metric protocols (position Gaussian widths 0.010, 0.025, 0.050; position uniform; velocity Gaussian widths 0.025, 0.050; velocity uniform), **all 4,270 computed channel comparisons** are below one. This is not evidence that physical material transport reversed. It is evidence that *the earlier norm hierarchy is not metric-independent*.

## Positive metric, finite conditioning, genuine discrimination

All observation metrics are SPD along the measured grid; minimum full metric eigenvalue across all profiles and seeds: `2.32079e-05`; maximum full metric condition: `44007.9`; maximum restricted two-plane metric condition: `304.543`. The legacy `tau_ref=1` ratios reproduce inherited numerical CSV data with maximum absolute difference `7.55e-07` (tolerance `2e-6`). The same physical historical material map's `tau_ref` similarities differ at most `2.24e-16`.

Passive nonorthogonal ambient chart covariance residual is `2.14e-15`; independent internal O(2) frame gauge residual is `3.33e-15`; passive `tau_ref` observation metric transformation residual is `2e-16`. The direct SPD-gram norm comparison versus the independently evaluated quartic expression differs at most `2.64e-14`. All these tests passed.

## Where the metric-dependent ranking crosses

An explicitly specified, globally trace-normalized SPD interpolation from the original Cartesian kinetic identity `I` to the new physical position-output observability metric produces one numerical root in `(0,1)` for **each of the 610 fixed observables**. The fitted root interval is `0.922639084…0.940923332`, median `0.937730202`. The quartic signed-strength polynomial reproduces directly computed squared-strength differences with the residual above. These roots are properties of a deliberately chosen metric interpolation and scalar normalization. They are **not** Q550 intrinsic phase thresholds or physical onset conditions.

Cubic-interpolated output quadrature refinements at 2× and 4× the original section mesh preserve the reversed sign in all measured directions; maximum change in the most extreme ratio compared with the original quadrature is `7.29e-06`. This comparison does not replace numerical integration of the original physical ODE.

## Scientific interpretation and decision

**Classification:** `MODEL_DYNAMICAL_OBSERVABILITY_METRIC_COUNTEREXAMPLE_TO_NORM_DIRECTIONALITY_INVARIANCE_NOT_PHYSICAL_DIRECTION_REVERSAL`.

The v18.51l statement remains accurate: along its single kinetic-position/velocity weight family, the sampled fixed material channel norm ordering survives. Its stronger extrapolation to an **observer-independent material direction hierarchy** does not follow, and the new independent observability metric provides a concrete counterexample to such extrapolation.

We must not assert material torsion, energy flux, hysteretic memory, irreversible transport, or a microscopic arrow. What the audit *does* identify is exactly where the previous robustness claim stops: a change from a kinetic state-distance inner product to a transport-conditioned physical-observation inner product changes which of two equally authentic projected channels is larger. Follow-up work, if warranted, should derive a physically preferred metric through an actual Lagrangian/variational or empirically calibrated measurement principle, rather than treating any favorable norm hierarchy as intrinsic.

## Scope and reproducibility

The scientific ancestry is authenticated byte-for-byte, with two inherited physical seed IVPs and zero new physical IVPs. Numerical analysis uses the archived 79 material sections per seed on `0≤xi≤0.05`; the positive-xi Riesz planes exist at 78 sampled sections per seed, and the finite-lag family uses lags of 1, 2 and 4 sections. Every numerical result is stored in CSV + `report.json`, scripts and tests are included, and `run_on_server.sh` generates a hashed server sendback. Double precision is not an interval enclosure of the ODE or of the entire continuous physical trajectory.
