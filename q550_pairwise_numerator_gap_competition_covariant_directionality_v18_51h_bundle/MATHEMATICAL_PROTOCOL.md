# Q550 v18.51h — Pairwise Numerator–Gap Competition & Covariant Directionality Audit

## 1. Scope and physical genealogy

The scientific parent is the **authenticated Q550 v18.51g server sendback**, transitively embedding the v18.51f source/outputs and the v18.51e genuine Q550 10D material tangent IVPs. All three archive levels have their original source/output manifests verified byte-by-byte; the previously used v18.51g audit code is separately retained byte-for-byte at `reference/g_projector_replay_v18_51g.py`. This run **does not integrate new physical Q550 IVPs**: it reanalyzes inherited physical `M(xi)` and independent `B(xi)`.

Two seeds (`original`, `autonomous`), three kinetic conventions (`tau_ref=0.5,1,2`), 79 sections per branch (`0<=xi<=0.05`), 78 positive spectral sections per branch. `M(0)=I` is tenfold degenerate; no positive-time Riesz-pair labels are assigned there.

## 2. Exact complex pairwise coupling identity

The actual inherited kinetic Cartesian propagator obeys `Mprime=B M`. For each isolated nonreal complex eigenvalue `lambda_a`, define the rank-one biorthogonal Riesz eigenprojector

`R_a = v_a w_a^H/(w_a^H v_a)`.

Each real rank-two pair projector `P_j` is the sum of the two conjugate `R_a` of that pair. Its derivative satisfies

`Pprime_j = sum_{a in j, k outside j} (R_k Mprime R_a + R_a Mprime R_k)/(lambda_a-lambda_k)`.

Define the covariant relative projector drift

`D_j = Pprime_j - (B P_j - P_j B)`.

For `i != j`, the **exact** directed cross-block is

```
Q_(j->i) = P_i D_j P_j
         = sum_{a in pair(j), k in pair(i)}
             lambda_k R_k B R_a/(lambda_a-lambda_k).
```

This is a four-term complex sum that is real after combining conjugate eigenvalues, to numerical roundoff. It is an **algebraic identity for the full inherited tangent generator** and does not assume material energy transfer. The `v18.51h` script independently constructs the full `Pprime_j` before comparing it with this directed-block sum, and checks each resulting Frobenius rate against the original parent `v18.51g` CSV.

## 3. Numerator, gap, and interference

Let `d_{a k} = lambda_a-lambda_k`. For an unordered pair `(i,j)` set

`delta_ij = min_{a in pair(j), k in pair(i)} |d_{a k}|`.

The same multiset of absolute gaps occurs in reverse, hence **`delta_ij=delta_ji` exactly**, even when directional block rates differ. An unordered scalar gap alone cannot determine orientation of coupling.

For each directed block the audit records:

- the minimum and maximum of the four absolute complex denominators;
- the complex numerator matrices `N_ak=lambda_k R_k B R_a` and their sum-of-norms;
- the four weighted terms `N_ak/d_ak` and their sum-of-norms;
- their coherent sum `Q_(j->i)` and its Frobenius norm;
- the cancellation factor `||sum N_ak/d_ak||_F / sum ||N_ak/d_ak||_F` (range `[0,1]`);
- `delta_ij ||Q_(j->i)||_F`, an **effective numerator by exact bookkeeping**, not an independent physical numerator;
- `||P_i B P_j||_F`, the unweighted oblique generator cross-block;
- the diagnostic counterfactual where every complex denominator retains its phase but has common modulus `delta_ij`.

No unique causal percentage of gap versus numerator can be extracted from these noncommuting complex matrix terms. In particular, because the four denominators can have very different magnitudes and phases, `||Q||` is *not* generally `||sum N_ak|| / delta`.

The inherited directed rate is `r_(j->i)=||Q_(j->i)||_F / ||P_j||_F`. Its 5/4 directional ratio has the **exact factorization**

```
r_(5->4) / r_(4->5)
  = [||Q_(5->4)||_F / ||Q_(4->5)||_F] * [||P_4||_F/||P_5||_F].
```

This separates the directed block asymmetry from source-normalization asymmetry. The shared gap cannot on its own create the observed ratio.

## 4. Covariance and convention dependence

For a constant kinetic-state balance `tau_ref`, define `D_tau=diag(I5,tau_ref I5)`. The inherited matrices transform by similarity:

`M_tau=D_tau M_1 D_tau^-1`, `B_tau=D_tau B_1 D_tau^-1`, `P_tau=D_tau P_1 D_tau^-1`, `Q_tau=D_tau Q_1 D_tau^-1`.

The eigenvalues and all complex spectral-gap magnitudes are invariant under this convention change. **Raw Euclidean Frobenius norms of oblique projectors and cross-blocks are not invariant** under nonorthogonal similarity. The audit independently reconstructs each convention and brings its matrices back to the common `tau_ref=1` frame, reporting both near-origin (small gap) residuals and interior residuals for `xi >= 0.001`.

The test of passive covariance must not be confused with a unique physical phase-space metric: kinetic `tau_ref` remains a declared material state balance convention. No general assertion of invariance under arbitrary unrelated metrics is made.

## 5. Numerical controls

- Check full ancestor archives' CRC, source/output SHA-256 and previously passed scientific controls.
- Independently differentiate synthetic four-dimensional complex Riesz projectors by centered finite differences; recover the numerator-gap block formula without Q550 files.
- Check 9360 Q550 directed cross-block identities and original g CSV rates.
- Check real conjugate pairing, projector resolution, positive gap, symmetric pairwise gap and ratio factorization.
- Compare all 6240 nonreference-tau directed blocks in common frame, including near-origin ill-conditioning rather than suppressing it.
- Save 468 directionality rows, all 9360 resolved numerators/gaps, 6240 common-frame controls and three diagnostic figures.

The numerical tolerances are finite-grid diagnostics, not mathematical interval bounds. Any failed gate prevents packaging of a scientifically valid sendback.

## 6. Scientific limitations

The observed `5->4` ordering is a reproducible **directed oblique spectral-projector diagnostic** on the six inherited branch representations. It does **not** establish material energy flow, constitutive torsion, hysteresis, a unique material metric, isolated spectral branches between recorded sections, or a new autonomous `kappa_0` law. The discarded `1/3` visual heuristic is not an acceptance criterion.
