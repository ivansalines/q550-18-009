# Q550 v18.50x — Anchor-Free κ₀ Differential Response & Moving Sensitivity Geometry Audit

Independent κ₀ sensitivity of the **analytic rank-three 7D-nullspace projector** in the inherited common 10D coordinate chart. Unlike v18.50w, this audit does **not subtract distances from either reference κ₀** to define its principal response.

## Inputs and authenticity

- `inputs/q550_moving_equidistance_gate_two_reference_transport_v18_50w_bundle_server_sendback.zip` is the authenticated **server** ancestor.
- The code verifies the SHA-256 source/output manifest of w, then v and u, and reuses the original driven Q550 solver from the full earlier genealogy.
- 22 κ samples, 79 ξ sections, two inherited fixed turning seeds; 44 new driven 10D IVPs over ξ∈[0, 0.05].
- Intermediate parent solver files are extracted into a temporary directory that is removed after calculation; **runtime is never packed**.

## Research objects

Let `P(κ,ξ)` denote the **10×10 orthogonal projector** onto the analytic observation kernel, computed in the same inherited common coordinate chart for every κ.

`E=∂κP`, `A=∂ξE`, `S=||E||F`, `S'=⟨E,A⟩/S`, `A⊥=A−⟨E,A⟩E/||E||²`, `Ω=||A⊥||F/S`.

The principal metric is Frobenius. This is not an independently proven physical kinetic metric. Differencing `P` happens **before taking norms**, avoiding the anchored V cusp.

## Reproduction on server

```bash
cd /root/elab1/hysteresis
unzip q550_anchor_free_kappa_differential_response_moving_sensitivity_geometry_v18_50x_bundle.zip
cd q550_anchor_free_kappa_differential_response_moving_sensitivity_geometry_v18_50x_bundle
set -o pipefail
PYTHON_BIN=python3.13 bash run_on_server.sh 2>&1 | tee ../v18_50x_server.log
```

The sendback is created beside this directory and does not include temporary ancestor trees. Do not modify run_on_server.sh; choose the interpreter through `PYTHON_BIN`.

## Classification

Finite-grid projector sensitivity, orientation, and transport geometry; **not** a proven intrinsic material edge, oscillation, or activation. A fixed-seed perturbation is not natural-state continuation in κ.
