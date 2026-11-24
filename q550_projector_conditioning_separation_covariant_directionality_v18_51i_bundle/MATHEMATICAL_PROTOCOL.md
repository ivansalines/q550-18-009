# Q550 v18.51i — Mathematical construction and validation protocol

## 1. Inherited exact crossblock

For each positive finite-time section, the historical full 10D material tangent map M(xi) has five numerically isolated conjugate eigenvalue pairs. Each real rank-two (oblique) Riesz projector is P_j, with j in {1,...,5}. The inherited kinetic tangent generator is B. The exact off-diagonal covariant spectral drift block from j to i is

```
Q_(i<-j) = P_i (dP_j/dxi - [B,P_j]) P_j,      i != j,
```

computed by the authenticated v18.51h complex numerator-gap algorithm. It is not inferred from a plotted curve. By projector algebra,

```
Q_(i<-j) = P_i Q_(i<-j) P_j.
```

## 2. Restrict to the domain actually represented by the source spectral plane

Choose any orthonormal 10x2 right-range bases U_j and U_i of P_j and P_i **in a declared Euclidean kinetic Cartesian chart**, using rank-two SVD. These are not left eigenspace or dual-projector bases. Define

```
K_(i<-j) = U_i.T Q_(i<-j) U_j         (2x2 real),
r_restricted = ||K_(i<-j)||_F / sqrt(2).
```

The Frobenius norm of K is invariant to independent orthogonal redefinitions of U_i,U_j in each plane. This rate is defined only for perturbations belonging to E_j=range(P_j), and need not be equal to the ambient-source projector-normalized rate used historically:

```
r_oblique = ||Q_(i<-j)||_F / ||P_j||_F.
```

The matrix reconstruction identity is exact:

```
Q_(i<-j) = U_i K_(i<-j) U_j.T P_j.
```

## 3. Isolate oblique extension and projector conditioning

For rank-two planes, the factors

```
A_(i<-j) = ||Q_(i<-j)||_F / ||K_(i<-j)||_F    (ambient extension),
C_j = ||P_j||_F / sqrt(2)                     (source condition)
```

obey precisely

```
r_oblique = r_restricted * A_(i<-j) / C_j.
```

For the opposed channels 5->4 and 4->5, with Q_45 interpreted as from pair 5 to pair 4,

```
r_oblique(5->4) / r_oblique(4->5)
  = [r_restricted(5->4) / r_restricted(4->5)]
  * [A_(4<-5) / A_(5<-4)] * [C_4 / C_5].
```

This three-factor identity is bookkeeping rather than a unique causal decomposition: changing the metric changes the factors. In particular K still inherits the oblique Riesz projectors in Q and is *not* evidence of a metric-free phenomenon.

## 4. Genuine metric covariance versus naive similarity

The kinetic conventions from the verified v18.51e material Cartesian state are connected by

```
D_tau = diag(I_5, tau I_5),
Q_tau = D_tau Q_1 D_tau^-1,    P_tau = D_tau P_1 D_tau^-1.
```

Euclidean norms of Q_tau and P_tau are not similarity invariant. The metric in tau coordinates corresponding to the tau=1 Euclidean kinetic metric is

```
G_tau = D_tau^-T D_tau^-1.
```

The reference-chart comparison is therefore carried out on

```
Q_common = D_tau^-1 Q_tau D_tau,
P_common = D_tau^-1 P_tau D_tau,
```

with fresh right-range orthonormalization in that common chart. The metric-covariant restricted norm agrees with its tau=1 reference within numerical error. This is **covariance under the inherited similarity with its metric**, not physical invariance across arbitrary new choices of metric.

## 5. Additional conditioning and sensitivity controls

Compute the principal angles between the right spectral planes 4 and 5; record both angles but do not interpret them as material torsion. For each section, compare all 20 non-self-directed restricted rates and record the largest channel. Record raw and restricted directional survival counts separately, so a failed directionality test remains visible.

At xi=0 the finite-time map is identity and the spectral decomposition is exactly degenerate. No projector continuation or statement at that time is claimed. The measured grid consists of 78 positive sections per seed/tau branch through xi=0.05. Since sensitivity to the small initial eigenvalue gaps is large, report common-frame errors both across all xi>0 and for xi >= 0.001; do not erase early errors or relax unconditionally.

## 6. Independently reproducible gates

Authenticate every source and result through the complete inherited nested SHA-256 manifests and CRC. Reproduce the inherited raw rates and directionality ledger, reconstruct all Q from restricted K to numerical precision, check exact factor identities, rank-two geometry, passive nonorthogonal synthetic chart covariance, and original versus pulled-back kinetic rates. The observed number of dominant channels is *reported*, not imposed as a success condition. A result can pass the mathematical audit while falsifying the original directionality hypothesis.
