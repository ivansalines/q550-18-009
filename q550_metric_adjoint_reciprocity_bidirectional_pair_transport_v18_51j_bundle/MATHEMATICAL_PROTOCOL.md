# Q550 v18.51j — Mathematical protocol

## 1. Authentic instantaneous spectral drift

Let `M(xi)` be the genuine Q550 10D material tangent propagator, and
`B(xi)` its kinetic generator. For strictly positive xi, the v18.51h ancestor
constructs five real rank-two Riesz spectral projectors `P_j` from the isolated
complex conjugate eigenvalue pairs of `M`. Define the off-diagonal covariant
spectral-projector drift from j to i:

```
Q_(i<-j) = P_i (P'_j - [B,P_j]) P_j,  i != j.
```

This is reconstructed from authenticated historic numerator–gap spectral
identities; the v18.51i ancestor validates its restricted representation.

With orthonormal right-plane frames `U4`, `U5` in a **declared single kinetic
state metric**, define the two real 2×2 matrices:

```
K_4<-5 = U4.T Q_4<-5 U5
K_5<-4 = U5.T Q_5<-4 U4
```

The adjoint of one 2×2 block *within the same metric* is its transpose. Compare
`K_4<-5` with `K_5<-4.T`. Both describe forward-time channels.

## 2. Exact reciprocity identity

```
S = (K_4<-5 + K_5<-4.T)/2
A = (K_4<-5 - K_5<-4.T)/2

||K_4<-5||_F² - ||K_5<-4||_F² = 4 <S,A>_F.
```

The normalized nonreciprocity defect is

```
R_adj = ||K_4<-5 - K_5<-4.T||_F /
        (||K_4<-5||_F + ||K_5<-4||_F).
```

The restricted rates are `||K||_F/sqrt(2)`. Under orthogonal gauge changes
`U4→U4 O4`, `U5→U5 O5`, the two matrices transform in compatible ways and
the norms, `R_adj`, and interference identity are unchanged. This is not a
symmetry proof for the physical equations of motion.

## 3. Real finite-time bidirectional material crossblocks

For two **strictly positive** sampled sections a < b, define the actual
inherited material tangent map

```
T(b,a) = M(xi_b) inv(M(xi_a)).
```

Then extract, for the same increasing-time direction,

```
K_fin_(i<-j)(b,a) = U_i(xi_b).T P_i(xi_b) T(b,a) U_j(xi_a).
```

The target **Riesz** projector is applied before restriction; using just
`U_i.T T U_j` would mix planes artificially because the right spectral planes
are generally not mutually orthogonal. Compare forward-time 5→4 and 4→5
at lags of one, two, and four samples. Normalize each rate by the real elapsed
`d_xi = xi_b - xi_a`, not the number of samples. Record the inverse-time
propagator separately as `T(a,b)=inv(T(b,a))` and never confuse this with the
opposite-channel forward-time rate.

Check exact composition `T(c,b)T(b,a)=T(c,a)` on sampled triples. This identity
is a consistency control, not a new numerical dynamical discovery.

## 4. Metric covariance and limits

For inherited kinetic state conventions tau, `D=diag(I5,tau I5)`, and

```
Q_tau = D Q_1 D^-1,  P_tau = D P_1 D^-1.
```

Euclidean metric in the tau=1 chart appears in tau coordinates as
`G_tau=D^-T D^-1`. Transporting the metric as well as the operators is essential.
The audit compares `D^-1 Q_tau D` and `D^-1 P_tau D` in the common tau=1
chart, with fresh orthonormal frames, and records error maxima both for all
positive sections and the better-conditioned xi>=0.001 interior. A chart
change is not proof of robustness to arbitrary *physical* metric changes.

No data between sampled sections are certified. The identity section xi=0 is
fully degenerate, so no five distinct spectral pair projectors exist there.
Neither adjoint nonreciprocity nor finite-lag crossblock strength equals
physical energy exchange, microscopic irreversibility, intrinsic torsion, or
hysteretic material memory.
