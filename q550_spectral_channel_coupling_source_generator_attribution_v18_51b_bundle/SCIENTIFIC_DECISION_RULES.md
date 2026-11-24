# v18.51b — Scientific decision rules

## A. Authentication

All files of the received v18.51a sendback and its nested v18.50z/y/x parent outputs must match their independently provided source and output manifests. Nested checks are in-memory and do not modify historical bundles.

## B. Mathematical identities

Let `P` be the 7D projector observed by v18.50x, `Q=I-P`, `J` the original Q550 analytic 10D tangent generator saved by z, and `K_model = QJP - PJ^TQ` the model's **skew offblock reduction** (not full tangent flow). Set `W = K_model-K_canonical`, `H=-W^2`, and let `Q1,Q2` be the stable two-dimensional projectors on `H` with eigenvalues `lambda1=sigma1^2`, `lambda2=sigma2^2`.

For separated clusters:

```
Q2 Q1' Q1 = (Q2 H' Q1) / (lambda1 - lambda2).
```

Writing `W' = K_model' - K_canonical'` gives

```
H' = -(K_model' W + W K_model')
     + (K_canonical' W + W K_canonical').
```

The exact model product rule (for exact differentiable inputs) is:

```
K_model' = K_generator + K_posture,
K_generator = Q J' P - P J'^T Q,
K_posture = -P' J P + Q J P' - P' J^T Q + P J^T P'.
```

Thus three **matrices** — generator drift, projector posture and canonical-connection drift — add to the observed interplane rate. Their **norms must never be added as scalars**. We also report signed Frobenius projections onto the total rate; these sum to one but are not percentages of a conserved physical resource.

The singular-strength derivatives obey `sigma_i' = Tr(Q_i H')/(4*sigma_i)` and can be decomposed by exactly the same three `H'` sources. The interplane-rate magnitude obeys a separate, purely mathematical numerator/gap relation:

```
rate = ||Q2 H' Q1||_F / (lambda1-lambda2)
(log rate)' = (log numerator)' - (log gap)'.
```

## C. Numerical checks

1. Synthetic double-degenerate skew pair perturbation matches the spectral derivative formula independently.
2. Synthetic projector rotation matches the model-generator product rule independently.
3. Saved model `K_model` matches the offblock reduction of the authenticated `J` and `P` at every section.
4. Source reconstruction matches direct cubic-spline `Q2 Q1' Q1` with relative residual below `2e-6`.
5. Spline derivative of the model offblock reduction matches its exact product-rule decomposition with relative residual below `2e-6`.
6. A five-point nonuniform local polynomial derivative independently checks `K_model'` and `K_canonical'`, residual below `1e-4` on the inherited variable-density grid.
7. Logarithmic numerator/gap decomposition closes to `1e-7` in its numerical algebra; this is **not an independent physical validation**, since it follows from a definition.
8. The two historical seed preparations are compared at the **same** midpoint κ₀. All 158 sections must exist.
9. No mode plane is assigned to the tiny third singular pair (near numerical floor); no physical causal or energy-transfer attribution is permitted.

The cross-stencil discrepancy is locally larger near the grid transition around `xi=0.001092`; this is documented, not silently filtered. These finite-data checks do not produce rigorous continuous-time interval bounds.

## D. Classification

`AUTHENTICATED_NUMERICAL_SPECTRAL_SOURCE_IDENTITY_NOT_UNIQUE_CAUSAL_OR_MATERIAL_ENERGY_ATTRIBUTION`

A source decomposition does not establish which independent mechanical subsystem drives a channel. It partitions derivatives of **chosen observed matrices**, and changes of metric/observer can change the partition.
