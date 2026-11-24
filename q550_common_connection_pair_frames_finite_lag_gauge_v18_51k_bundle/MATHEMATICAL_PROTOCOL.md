# Q550 v18.51k — Mathematical protocol

## 1. Authenticated material transport and spectral channels

The input is the **v18.51j server sendback**, verified by archive CRC and SHA-256 manifests. Its nested v18.51i → h → g → f → e genealogy is reauthenticated by the byte-exact historic scripts. No new Q550 physical IVP is integrated. The two original 10D trajectories and tangent solutions are inherited.

At each strictly positive sampled section, let `E_i(xi)` be the real rank-two *right* spectral subspace of the complex conjugate pair `i` of the finite-time tangent map `M(xi)`, `i=4,5`. Choose Euclidean-orthonormal frames `U_i(xi)` in the **single declared kinetic Cartesian chart** for a given `tau_ref`. The full-state Riesz projectors `P_i` need not be self-adjoint; the right-plane frames need not be mutually orthogonal.

For `a<b` in sampled positive sections and physical forward-time tangent map `T(b,a)=M(b) M(a)^-1`, the inherited projected material crossblocks are

```
K_(4<-5)(b,a) = U_4(b)^T P_4(b) T(b,a) U_5(a)
K_(5<-4)(b,a) = U_5(b)^T P_5(b) T(b,a) U_4(a)
```

The two operators act between *different* endpoint spaces. Their unaligned matrix difference is not a basis-independent reciprocity defect.

## 2. Common ambient connection and induced plane-frame lifts

The common ambient connection is the flat Levi-Civita connection of the kinetic Cartesian state metric. Parallel ambient transport is the identity in this Cartesian chart; it is **not** the physical tangent propagator `T`. For each spectral plane separately, the induced metric/Grassmann discrete parallel alignment is the orthogonal polar factor of the overlap

```
R_i(k+1,k) = polar[ U_i(k+1)^T U_i(k) ]  in O(2).
R_i(b,a)   = R_i(b,b-1) ... R_i(a+1,a).
```

The *same ambient connection and state metric* are used for both planes. A separate induced subbundle lift is required because the planes themselves move differently. The two lifts are not independent arbitrarily chosen dynamical connections.

When adjacent spectral right planes remain sufficiently close, polar factors are uniquely defined. The audit records the minimum singular value of every adjacent overlap, connection composition, and the difference between direct endpoint polar alignment and chained-step alignment. Direct and chained alignment need not coincide: a moving subspace can generate finite Grassmann geometric effects.

## 3. Gauge-aligned reciprocal comparison

To compare both channels in the shared **start-section** frame, form

```
X = R_4(b,a)^T K_(4<-5)(b,a)
Y = K_(5<-4)(b,a)^T R_5(b,a)
S=(X+Y)/2,    A=(X-Y)/2
```

Here `X` and `Y` both have rows in the frame of `E_4(a)` and columns in the frame of `E_5(a)`. The gauge-aligned defect is

```
D_aligned = ||X-Y||_F / (||K_(4<-5)||_F + ||K_(5<-4)||_F).
```

The exact interference identity `||X||_F^2-||Y||_F^2 = 4<S,A>_F` is checked. This is a decomposition of two forward-time crossblocks, **not** a physical time-reversal or energy-flux law.

Under arbitrary **independent, section-dependent** orthogonal gauges `U_i(k) -> U_i(k) O_i(k)`,

```
R_i(b,a) -> O_i(b)^T R_i(b,a) O_i(a)
X -> O_4(a)^T X O_5(a)
Y -> O_4(a)^T Y O_5(a).
```

Thus `D_aligned`, the norms, interference, and the directional strength ratio are invariant. By contrast, `||K_(4<-5)-K_(5<-4)^T||/(||K_(4<-5)||+||K_(5<-4)||)` generally changes under independent endpoint gauges.

## 4. Moving nonorthogonal ambient-chart covariance

A second, independent control uses an explicitly xi-dependent invertible nonorthogonal passive chart `A(xi)`. The transformed geometric data are

```
G_A(xi) = A(xi)^-T A(xi)^-1
C_A(b,a) = A(b) A(a)^-1
P_i^A(xi) = A(xi) P_i(xi) A(xi)^-1
T_A(b,a) = A(b) T(b,a) A(a)^-1
U_i^A(xi) = A(xi) U_i(xi).
```

The metric-compatible ambient parallel map satisfies `C_A(b,a)^T G_A(b) C_A(b,a) = G_A(a)`. The transformed projected crossblocks and connection overlaps are computed with **endpoint metrics and ambient parallel maps**. Naively dropping them would conflate a coordinate change with a changed metric or connection.

## 5. Scope and possible falsification

- Test both seeds, three declared kinetic weights `tau_ref=0.5, 1, 2`, and finite lags of 1, 2, and 4 sampled sections, only at `xi>0`.
- Validate equality with the recorded j bidirectional strength ratios to within `2e-6`. This is a *numerical replay tolerance* necessitated by ill-conditioning near `xi=0`, not an exact symbolic identity.
- Accept a gauge-independent finite-lag defect only if both endpoint-independent `O(2)` tests and the moving nonorthogonal metric/connection pullback pass.
- If one direction dominates, report it as a finite-sample restricted operator-norm statement. It does **not** establish physical kinetic-energy transfer, torsion, hysteretic memory, a universal law, or separation in the continuum between samples.
- No fifth-pair spectral planes are claimed at the fully degenerate identity section `xi=0`.
