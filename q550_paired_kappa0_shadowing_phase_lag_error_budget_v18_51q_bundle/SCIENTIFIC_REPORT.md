# Q550 v18.51q — Scientific report

**Paired-κ₀ Shadowing, Phase-Lag & Error-Budget Audit**

## Decision

**All 16/16 scientific and numerical consistency controls pass in the local replay.** Two authenticated historical kappa values were propagated independently for each of the two genuinely different natural turning seeds. A midpoint parameter control is included. The 2-seed x 3-kappa factorial was repeated at two DOP853 numerical budgets, for **12 authentic nonlinear physical IVPs** and 129 saved event-relative sections per branch.

The historical parameters are `kappa_original = 0.1666666666666667` and `kappa_autonomous = 0.1665996104176405` (distance `delta_kappa = 6.705624902611507e-05`). `kappa_midpoint = 0.1666331385421536` is only a parameter-curvature control, not a third coexisting physical boundary.

## Measured same-seed parameter response

| Quantity at xi=0.05 | Original preparation | Autonomous preparation |
|---|---:|---:|
| Cartesian position separation `||delta Q||` | 2.030443969e-07 | 2.030435753e-07 |
| Maximum physical velocity separation `||delta V||` | 4.827223914e-06 | 4.827203823e-06 |
| Local phase-equivalent xi shift | -2.011336939e-08 | -2.010937393e-08 |
| Fractional orthogonal residual `||r_perp||/||delta Q||` | 0.989864182 | 0.989868292 |
| Accumulated material-time difference | -5.023759186e-15 | -4.996003611e-15 |
| First operationally resolved section | 0.000390625 | 0.000390625 |
| Resolved sections (factor 20 against proxy) | 128/129 | 128/129 |

The **local phase projection does not absorb the difference**: around 99% of the Cartesian position-discrepancy norm is orthogonal to the instantaneous reference velocity. This excludes a *pure local time shift* as an adequate first-order account of the measured difference. This is a metric-specific Euclidean Cartesian statement on the observed interval, not a theorem about global phase locking or orbit conjugacy.

Numerical proxies from the difference of two DOP853 settings have maxima `Q=6.139e-15`, `V=3.086e-15`, accumulated `tau=2.776e-17`. The measured same-seed parameter-induced Q separation is well above this numerical discrepancy at every **positive** saved section, but the discrepancies are *not certified error bounds*. At xi=0 the two parameter branches share precisely the same initial state, as they should.

## Why the 2 x 3 intervention matters

The original/autonomous seed **initial-condition difference** is a separate effect from the same-seed parameter response. At the final section the position difference between the two seeds at fixed parameter is approximately `4.786e-05`, about 235 times larger than the `2.030e-07` same-seed kappa response. Conflating seed and parameter would therefore conceal the physical source of the observed closeness.

The midpoint second difference at the endpoint is below `1e-14` in both cases, compatible with almost linear parameter response over an extremely narrow `delta_kappa`. This does **not** demonstrate a new nonlinear parameter law; at this scale finite precision is relevant.

## Clock and sensitivity

The authentic nonlinear clock closure `Q_xi = c V` has maximum relative defect `6.246e-16`. Both kappa runs have nearly indistinguishable accumulated material clocks; the observed pair difference near `5e-15` in elapsed tau is extremely small. Clock similarity alone cannot establish matching 10D trajectories.

The original Q550 driving protocol and historic nonlinear solver are preserved. The present experiment deliberately does **not** propagate two concurrent material boundaries, prove a long-time shadowing lemma, prove hysteretic memory, or certify metric-independent torsion. The natural next discriminator is an independently error-controlled, longer-horizon two-kappa analysis with an explicit observability and phase-matching rule fixed *before* inspection.

## Reproducibility

The parent v18.51p sendback and its 19 authenticated ancestors are included as original source bytes. All Python scripts, tests, input and output hashes, saved physical state tensors, CSV ledgers and plotting code are included. This is a numerical construction-plus-audit, not an interval-valued shadowing certificate.
