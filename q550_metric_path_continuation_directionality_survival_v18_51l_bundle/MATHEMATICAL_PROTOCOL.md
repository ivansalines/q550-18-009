# Q550 v18.51l — Mathematical protocol

## Question

Does the forward-time spectral 5→4 channel norm remain greater than the forward-time 4→5 norm *as the declared kinetic-state weighting changes continuously* from `tau_ref=0.5` to `2.0`, at the already observed positive-time Q550 sections? A metric convention test is not by itself a material-law invariance test.

## Inherited material data

The parent is the byte-authenticated v18.51k server sendback with exact nested v18.51j/i/h/g/f/e genealogy. The authentic Q550 material history comprises **two** previously integrated 10D physical seed IVPs and 78 strictly positive-xi sections per seed. This audit performs **zero** new 10D physical IVPs, and it does **not** invent a second trajectory at another kappa. The spectral-plane labels 4 and 5 are the inherited isolated real rank-two Riesz right-plane labels. The ξ=0 identity map has no isolated pair decomposition.

The finite-lag observables use 227 sampled positive-time intervals per seed: 77 lag-1, 76 lag-2, and 74 lag-4. The instantaneous observables use 78 positive sections. All original section times, models, spectral projector labels and finite propagators are held fixed.

## Continuous kinetic-state weight path

In kinetic Cartesian tangent-state coordinates, with `tau_ref=1` the reference chart, set

\[
D_\tau=\operatorname{diag}(I_5,\tau I_5),\quad
M_\tau(\xi)=D_\tau M_1(\xi)D_\tau^{-1},\quad
P_{j,\tau}(\xi)=D_\tau P_{j,1}(\xi)D_\tau^{-1}.
\]

This is a metric-weight continuation of the **same** material cocycle and its spectral planes. In the original unweighted chart its metric is `diag(I5,tau^2 I5)`; it is *not* a new model dynamical equation and is not a passive isometry between physically distinct declared state metrics.

For an orthonormal `10×2` frame `U_j(xi)` in the tau=1 chart, define `s=tau²`,

\[
B_j=U_j^T\operatorname{diag}(0_5,I_5)U_j,\quad
H_j(s)=I_2+(s-1)B_j.
\]

Here `0 <= B_j <= I` and `H_j(s)` is SPD for all `s>0`. Its canonically reweighted orthonormal frame is

\[
\widetilde U_j(\xi,s)=D_\tau U_j(\xi)H_j(\xi,s)^{-1/2}.
\]

For either an instantaneous spectral crossblock or a finite-time projected material crossblock with start `a`, target `b`, the exact metric continuation is

\[
K_{i\leftarrow j}(b,a;s)=H_i(b,s)^{1/2}
K_{i\leftarrow j}(b,a;1)H_j(a,s)^{-1/2}.
\]

For instantaneous blocks, `a=b`. The projection range must be the spectral target plane: this formula is independently checked against the fully transformed 10D operators at selected path nodes.

The measured ratio `R=||K_(4<-5)||_F / ||K_(5<-4)||_F` is a **same-metric, same-forward-time** operator norm ratio. It does not measure physical energy transfer or microscopic time reversal.

## Polynomial positive-sign reduction across the entire tau interval

Since `H_j(s)=A_j+s B_j` with `A_j=I-B_j`,

\[
\|K_{4\leftarrow5}(s)\|_F^2
=\frac{N_{54}(s)}{\det H_5(a,s)},\quad
N_{54}(s)=\operatorname{tr}\big[H_4(b,s)K_{54}\,\operatorname{adj}(H_5(a,s))K_{54}^T\big],
\]

and analogously

\[
\|K_{5\leftarrow4}(s)\|_F^2
=\frac{N_{45}(s)}{\det H_4(a,s)}.
\]

Each numerator and each 2×2 Gram determinant has degree at most two in `s`. Therefore, for `s>0` both Gram determinants are positive and the directionality is exactly the sign of the degree-at-most-four polynomial

\[
F(s)=N_{54}(s)\det H_4(a,s)-N_{45}(s)\det H_5(a,s).
\]

The code checks its reconstructed rational identity against direct 2×2 square-root Gram calculations at `s={0.25,0.73,1,1.67,4}` for all 610 baseline observables. It then converts `F` into Bernstein coefficients over `[0.25,4]` (with optional bisections) and reports lower bounds and a floating-point roundoff heuristic guard. **Positivity of the coefficients certifies the sign of the rounded polynomial in exact arithmetic, but the present double-precision computation is NOT validated interval arithmetic and cannot certify the original continuous-time physical IVP.**

## Common-connection gauge and anchor controls

At each tau node, both right planes are reweighted from the same ambient state metric. Their adjacent-section polar/Procrustes lift is recomputed from the new orthonormal frames. Forward-time finite-lag crossblocks are then aligned before the metric-adjoint comparison. Randomly changing independent O(2) pair-frame gauges at endpoints must not change the aligned scalar or the channel norm ratio.

At `tau={0.5,1,2}`, the new ratios are compared with the independently reconstructed v18.51j/k values. The near-origin spectral numerical replay tolerance is declared as `2e-6`; it is not an algebraic machine-precision identity. Direct transformed 10D blocks and material similarity are separately checked.

## Scope and non-claims

Nothing is certified between physical ξ sections, outside `tau_ref in [0.5,2]`, across different independently derived material metrics, or over a full hysteretic return loop. This is a **fixed-model finite-time metric weighting path**, not an interval-valued proof of a universal constitutive law, material torsion, irreversible energy flux or memory.
