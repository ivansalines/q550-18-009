# Scientific decision gates — Q550 v18.51f

All required for a measured diagnostic PASS:

- Parent v18.51e archive passes SHA-256 source+output manifests, ZIP CRC and parent scientific checks; no synthetic substitute for physical Q550 arrays.
- All six (2 seeds×3 `tau_ref`) branches have five non-real conjugate pairs at every **positive** sampled `xi`, isolated by the declared gap floor; no claim of a splitting at `xi=0`.
- Real Riesz projectors are idempotent, mutually disjoint, resolve identity and commute with finite-time `M` within tolerances; conjugacy and volume-product identities pass.
- Exact declared `D_tau` similarity matches actual data, and both eigenvalues and modal projectors exhibit passive similarity covariance. Cauchy–Green is recomputed from transformed M, **not** subjected to false tensor similarity.
- Finite eigenvector conditioning. Pair tracking, oblique interplane mixing and original/autonomous differences must be reported, even when they are not zero.
- Valid per-section and per-pair CSVs, plots, machine-readable report and source/output hashes. Exit nonzero on check failure.

**Classification:** `NUMERICAL_FINITE_TIME_SPECTRAL_PAIRING_AND_SIMILARITY_DIAGNOSTIC_NOT_INTRINSIC_TORSION_OR_MEMORY_CERTIFICATE`.

No certified orientation memory, unique phase-space kinetic metric, eigenplane orthogonality, material torsion, conserved spectral energy or universal 1/3 ratio follows from this audit. Invariant eigenvalues under `tau_ref` are a similarity identity, not a new material conservation law.
