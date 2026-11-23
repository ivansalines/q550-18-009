# v18.50v — Scientific interpretation and reproducibility

## A moving tooth is a hypothesis about response, not about a graph shape

The v18.50u controlled fixed-seed study found smooth, nearly linear parameter
sensitivity over the very short turn-relative window. The proposed next step
is to remain present as the response progresses: sample the same full driven
10D trajectories over a longer interval and measure the continuous *sequence*
of sensitivity across parameter and time, rather than relying on endpoint
projector distances.

## Predeclared measurement

The primary non-observer diagnostic is the normalized-state-chart sensitivity
`||∂z/∂κ||`, formed by differentiating the 10D driven physical state with
respect to κ using the parameter samples. A second independent dynamical
measure is `||∂F/∂κ||` of the driven RHS evaluated on those trajectories.
Observer and nullspace-projector sensitivities remain valuable geometric
controls, not evidence of physical activation on their own.

Data are collected for two independent, fixed turning seeds, at 22 κ values
and densely across three turn-relative time scales. Actual per-κ driven IVPs
are integrated to the long endpoint, including baseline trajectories. There is
no extrapolation of the inherited short `ctx.sol` beyond ξ=0.001092.

## Decision rule

A candidate narrow-band response must have an internal κ maximum at least 15%
above both outer flanks, persist at two consecutive times, and be seen in both
10D dynamical measures, one geometric observer measure, and both seeds. This is a *screen*, not a
rigorous proof of an activation threshold. Smooth monotone passage remains a
valuable and fully archived result.

## Scientific classification

`CONTROLLED_DYNAMIC_PARAMETER_RESPONSE_DIAGNOSTIC_NOT_MATERIAL_ACTIVATION_CERTIFICATE`

The generated `results/report.json` is the authoritative numerical report.
It records whatever the actual server integration finds; no anticipated
peak or threshold is assigned in advance. This static report is intentionally
methodological and therefore remains valid if rendering/library versions
change on another machine.

## Local authoring-run measurements (2026-11-03)

The complete real-solver local run used 22 κ values (13 within the historical
bounds), two fixed natural preparations, 79 ξ samples from 0 to 0.05,
44 completed 10D DOP853 integrations (26,488 RHS evaluations), and 3,476
state/observer/projector measurements. The predeclared screening recorded **zero
qualified interior κ ridges** over this interval. This does **not** exclude a
narrower, later, differently prepared, or differently observed activation.

At κ interval midpoint, the shared-chart norm of the driven-state parameter
derivative grows along ξ:

| ξ | Original seed | Autonomous seed |
|---|---:|---:|
| 0.001092 | 0.011361503 | 0.011364280 |
| 0.012500 | 0.131959185 | 0.131991352 |
| 0.050000 | 0.553797846 | 0.553929326 |

The original-seed increase from ξ=0.001092 to 0.05 is approximately 48.74×.
At ξ=0.05, the within-band relative spread of the state-gain diagnostic is
only about 2.92×10⁻⁶ in both seeds, far below the 15% screening threshold.
The response evolves strongly with ξ but remains extremely smooth with κ over
this very narrow interval in the declared chart.

This pattern is **a measured evolving response**, not evidence of a localized
activator. The study preserves the full κ–ξ ledger for follow-on analyses.
The independent server sendback remains to be checked; do not equate it with
this authoring run until its manifest and outputs are verified.
