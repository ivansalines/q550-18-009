# v18.50v — Predeclared scientific decision rules

## Question
Does a response localized in the narrow historical κ interval develop at later
turn-relative ξ, in the actual Q550 driven 10D trajectory, rather than only in
an anchor-dependent projector gap?

## Controls

- 22 κ samples: 13 uniformly spaced inside/including the historical bounds,
  five outside on the left, four outside on the right.
- Two distinct inherited turning-state preparations, each held FIXED while κ
  changes, each using its own fixed imposed drive clock.
- Four measured sensitivities: actual 10D state, actual driven RHS, normalized
  4D structural observer, and 7D-kernel projector in one shared state chart.
- Parameter derivative is estimated on the VECTOR or projector first, using an
  uneven-grid second-order scheme; its norm is taken only afterward. This
  eliminates the trivial |κ-κ_anchor| cusp as an activation proxy.
- Early (0..0.001092), medium (to 0.0125) and long (to 0.05) windows, with
  complete time histories. An entire phase/κ ledger is mandatory, regardless
  of whether a ridge is found.

## Candidate criterion (screening, not a certificate)

- A *strict* interior sample point in 0 < offset < 1 must be a local κ maximum,
  and must exceed the strongest outer-flank response by at least 15%.
- It must persist on two adjacent time samples in both 10D dynamical
  measures and at least one geometric observer measure, both seed families,
  with κ peaks aligned within one inner-grid interval before **model-wide candidate** is allowed.
- Isolated peaks, boundary peaks, one-seed effects, different reference charts,
  and scalar anchor-induced V shapes are **not activation certificates**.
- A model-wide candidate would still require finer κ/time sampling, perturbation
  and seed controls, convergence of a non-observer physical response,
  and confirmation beyond the prescribed drive phase.

## Allowed outcomes

- `NO_LOCALIZED_CONTRAST_DETECTED_WITHIN_WINDOW` if no candidate passes.
- `CONTROLLED_LOCALIZED_CONTRAST_CANDIDATE` if persistent peaks pass, still not
  a physical/material actuation certificate.
- `STATE_PREPARATION_DEPENDENT_CANDIDATE` if a localized feature appears
  persistently in one seed but not the other.

In all cases preserve **where, when and how** the sensitivity evolves, even
when the response is smooth. No guessed tooth position if there is no peak.

## Limitations

- The historical two κ values are **parameters**; no material boundary has been
  established. Distinct fixed seeds do not certify natural preparation at each κ.
- The shared diagonal state chart and normalized observer are declared, not
  a derivation of a physical kinetic metric.
- A long but finite window cannot exclude delayed effects outside it.
- No rigorous error enclosure, no full continuum search and no physical
  polymer constitutive equivalence is claimed.
