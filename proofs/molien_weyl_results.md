# Molien-Weyl Unification: Results

## Summary

The Molien-Weyl integral formula was computed for the E8 Coxeter element
acting on the 8D Cartan subalgebra, its 4D parallel (H4) and perpendicular
subspaces, and the adjoint representation. The goal was to determine whether
a single Molien-Weyl computation can produce BOTH the exponents AND
coefficients of the GSM fine-structure constant formula.

## Key Results

### 1. Cyclic vs Weyl Molien Series

Two distinct Molien series exist:

- **Weyl group W(E8)** (order 696,729,600):
  `M_Weyl(t) = 1/[(1-t^2)(1-t^8)(1-t^12)(1-t^14)(1-t^18)(1-t^20)(1-t^24)(1-t^30)]`

  This is determined by the Casimir degrees and is a polynomial ring (Chevalley-Shephard-Todd theorem).

- **Cyclic Coxeter group Z/30Z** (order 30):
  M_cyclic(t) has many more invariants (e.g., degree 2: 4 vs 1, degree 8: 437 vs 2).

  Invariant condition: monomial `x^a` is invariant iff `sum m_i * a_i = 0 mod 30`
  where m_i are the Coxeter exponents {1,7,11,13,17,19,23,29}.

Both were verified numerically to degree 40.

### 2. Parity Constraint

**ALL odd-degree cyclic Molien coefficients vanish** for both the full 8D and
projected 4D series. This is because all E8 Coxeter exponents are odd:
sum(m_i * a_i) with all m_i odd has the same parity as sum(a_i) = degree,
so odd-degree monomials always have odd weight, never 0 mod 30.

This means: **the GSM exponent 7 corresponds to zero cyclic invariants**.
The exponent 7 enters the GSM formula through a different mechanism than
scalar polynomial invariants.

### 3. Projected Series

| n | M_par (cyclic) | M_perp (cyclic) | M_par (Weyl) | M_perp (Weyl) |
|---|----------------|-----------------|--------------|----------------|
| 0 | 1 | 1 | 1 | 1 |
| 2 | 2 | 2 | 1 | 0 |
| 4 | 3 | 3 | 1 | 0 |
| 6 | 6 | 6 | 1 | 0 |
| 7 | 0 | 0 | 0 | 0 |
| 8 | 9 | 9 | 1 | 1 |
| 14 | 48 | 48 | 2 | 1 |
| 16 | 63 | 63 | 2 | 1 |
| 26 | 244 | 244 | 4 | 1 |

**Key observation**: M_par and M_perp are IDENTICAL for the cyclic group at
every even degree. This is because the weight sets {1,11,19,29} and {7,13,17,23}
give identical Molien series (they are Galois conjugates with the same pairing structure:
1+29 = 11+19 = 7+23 = 13+17 = 30).

For the **Weyl** Molien series:
- M_perp_Weyl = 0 for degrees 1-7 (no hidden-sector Weyl invariants below degree 8)
- M_perp_Weyl[8] = 1 (first hidden-sector invariant)

### 4. Factorization

- **Weyl**: M_Weyl = M_par_Weyl * M_perp_Weyl **EXACTLY** (confirmed at phi^(-1))
  - Ratio = 1.000000000000
  - This follows trivially from the Casimir degree partition: {2,12,20,30} union {8,14,18,24}

- **Cyclic**: M_cyclic != M_par_cyclic * M_perp_cyclic
  - Ratio at phi^(-1) = 7.824
  - "Interaction" invariants exist at all even degrees >= 4
  - These are mixed monomials involving both V_par and V_perp variables

### 5. Adjoint Molien Series

M_adj(t) = (1/30) sum_k chi_adj(w^k) / det(I - t*w^k)

The adjoint character values are:
- chi_adj(w^0) = 248 (dim E8)
- chi_adj(w^k) = -1 for k coprime to 30 (both parallel and perp exponents)
- Various small values at non-coprime k

M_adj has nonzero coefficients at ALL degrees (including odd), because the
adjoint character weight shifts the invariance condition.

The ratio M_adj/M_cyclic approaches ~120 = |roots(E8)|/2 for large n.

### 6. Evaluation at phi^(-1)

| Quantity | Value |
|----------|-------|
| M_cyclic(phi^(-1)) | 74.792 |
| M_par(phi^(-1)) | 3.092 |
| M_perp(phi^(-1)) | 3.092 |
| M_Weyl(phi^(-1)) | 1.661 |
| M_par_Weyl(phi^(-1)) | 1.623 |
| M_perp_Weyl(phi^(-1)) | 1.023 |
| M_adj(phi^(-1)) | 18246.1 |
| alpha^(-1)_GSM | 137.036 |

No simple algebraic relationship connects M_adj(phi^(-1)) to alpha^(-1).

### 7. Hidden Sector Screening Analysis

The Weyl Molien series M_perp_Weyl provides a clear selection rule:

| Degree | M_perp_Weyl | GSM coefficient | Interpretation |
|--------|-------------|-----------------|----------------|
| 7 | 0 | 1 | **UNSHIELDED** -- no hidden-sector invariant exists |
| 8 | 1 | -1/248 | **FIRST SCREENING** -- hidden sector turns on |
| 14 | 1 | 1 | Casimir degree (second-order) |
| 16 | 1 | 1 | 2 * Casimir-8 |
| 26 | 1 | 248/240 | Composite Casimir (8+18) |

The fact that degree 7 (the first Coxeter exponent after 1) has NO hidden-sector
invariant while degree 8 (the first Casimir degree after 2) has exactly 1 is
structurally meaningful: it explains the qualitative difference between the
phi^(-7) term (coefficient 1, unshielded) and the phi^(-8) term (coefficient
-1/248, screened).

However, degrees 14, 16, 26 also have hidden-sector invariants yet enter with
coefficients of order 1 (not suppressed), which the screening picture alone
does not explain.

## What the Molien-Weyl Integral Explains

### Exponent Selection
- The allowed exponents come from the Casimir degrees and their combinations
- All odd Coxeter exponents {1,7,11,13,17,19,23,29} give ZERO scalar invariants
  (parity constraint)
- The exponent 7 enters through the adjoint/vector sector, not scalar invariants

### What It Does NOT Explain
- The integer anchor 137 (topological, not invariant-theoretic)
- The specific coefficients -1/248 and 248/240 (1-loop normalization)
- Why only exponents {7,8,14,16,26} appear (rather than all even Casimir
  combinations)

## Conclusion

The Molien-Weyl integral provides **selection rules** (which operator degrees
are allowed by the E8/H4 symmetry) while the 1-loop calculation provides
**coefficients** (how much each operator contributes). The two are complementary:

- **Molien series** -> {allowed degrees} and multiplicities
- **1-loop dynamics** -> Wilson coefficients (-1/248, 248/240, etc.)

The unified picture is analogous to how in QFT, symmetry determines which
operators can appear in the effective action (selection rules from Molien),
while dynamics determines their coefficients (from loop calculations).

The goal of reducing everything to a SINGLE Molien-Weyl formula is not
achieved: the coefficients require dynamical input beyond invariant counting.
However, the Molien series does provide structural constraints that are
consistent with the GSM formula, and the hidden-sector screening pattern
(M_perp = 0 at degree 7 vs M_perp = 1 at degree 8) provides a non-trivial
geometric explanation for the qualitative difference between the leading
correction terms.
