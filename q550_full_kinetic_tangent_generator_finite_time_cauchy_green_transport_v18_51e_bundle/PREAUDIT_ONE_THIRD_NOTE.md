# Exploratory 1/3 visual observation — imported verified v18.51d measurements

These numbers are obtained from the actual `results/kinetic_metric_spectral_source_ledger.csv` of the fully hash-authenticated v18.51d server sendback, **not** results from a v18.51e run. Define `r=C/F`, where `C` and `F` are the **signed** canonical and moving kinetic-frame fractions of the historical spectral interplane differential projector. The ratio is not a calorimetric or kinetic-energy partition.

| Seed | tau_ref | Endpoint C/F | Fraction of 79 sections within absolute 0.025 of 1/3 |
|---|---:|---:|---:|
| original | 0.5 | 0.285588 | 4/79 (5.06%) |
| original | 1.0 | 0.313676 | 6/79 (7.59%) |
| original | 2.0 | 0.480225 | 0/79 (0%) |
| autonomous | 0.5 | 0.284006 | 4/79 (5.06%) |
| autonomous | 1.0 | 0.312949 | 6/79 (7.59%) |
| autonomous | 2.0 | 0.479767 | 0/79 (0%) |

This is an important **falsifying control for naive universality**: the endpoint ratio under tau_ref=2 is not close to 1/3, and no section in that branch is within tolerance. The closeness in some sections of the other branches may be geometrically suggestive but is not a physical law. The new v18.51e records the full finite-time Cauchy–Green deformation separately and must not misidentify signed projector-source shares as finite-time stretching energies.

Also, the shared chart orientation requires independent scrutiny. The v18.50z archived generator is `J_z=S J_y S^-1`, whereas v18.51d assembled `L=DH S`. The consistently conjugated kinetic material map uses `L=DH S^-1`; this is a **coordinate compatibility issue** not detected by a stand-alone metric compatibility identity. v18.51e exposes the comparison rather than silently carrying forward the old choice.
