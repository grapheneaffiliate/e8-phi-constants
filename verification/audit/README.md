# GSM Derivation Audit

## Methodology

Every term in every GSM formula is classified as one of:

| Tag | Meaning | Requirement |
|-----|---------|-------------|
| `[GEOMETRIC]` | Directly from E₈/H₄ structure (dim, rank, Coxeter, Casimir, roots, etc.) | Must cite specific invariant |
| `[ALGEBRAIC]` | From φ-algebra identities (Lucas, Fibonacci, φⁿ = F(n)φ + F(n-1)) | Must cite specific identity |
| `[COMBINATORIC]` | From representation theory counting or branching rules | Must cite specific branching |
| `[DERIVED]` | Follows from a prior GSM result via proven theorem | Must cite the parent result |
| `[AD_HOC]` | Chosen to fit data, no structural justification | **MUST BE ELIMINATED OR RECLASSIFIED** |

## Allowed First-Principles Quantities

```
FROM E₈:
  dim(E₈) = 248, rank = 8, h = 30
  Casimir degrees: {2, 8, 12, 14, 18, 20, 24, 30}
  Exponents: {1, 7, 11, 13, 17, 19, 23, 29}
  dim(SO(16)) = 120, dim(SO(16)_spinor) = 128, dim(SO(8)) = 28
  |W(E₈)| = 696,729,600, roots = 240
  dim(E₆) = 78, dim(E₇) = 133, dim(F₄) = 52, roots(F₄) = 48

FROM H₄:
  |W(H₄)| = 14400, h = 30, degrees {2, 12, 20, 30}
  φ = (1+√5)/2, 120-cell (600 vertices), 600-cell (120 vertices)

FROM E₈ → H₄ PROJECTION:
  Torsion ratio ε = 28/248 = dim(SO(8))/dim(E₈)
  Fiber dimension 244

FROM φ-ALGEBRA:
  φ² = φ+1, φⁿ = F(n)φ+F(n-1), L(n) = φⁿ+φ⁻ⁿ, 1/φ = φ-1

FROM MATHEMATICS:
  π (appears in mp/me via sphere-packing integrals)
```

## Files

| File | Constants | Count |
|------|-----------|-------|
| [01_gauge_couplings.md](01_gauge_couplings.md) | α⁻¹, sin²θ_W, α_s | 3 |
| [02_lepton_masses.md](02_lepton_masses.md) | m_μ/m_e, m_τ/m_μ | 2 |
| [03_quark_masses.md](03_quark_masses.md) | m_s/m_d, m_c/m_s, m_b/m_c | 3 |
| [04_proton_electroweak.md](04_proton_electroweak.md) | m_p/m_e, y_t, m_H/v, m_W/v | 4 |
| [05_ckm_matrix.md](05_ckm_matrix.md) | sin θ_C, J_CKM, V_cb, V_ub | 4 |
| [06_pmns_matrix.md](06_pmns_matrix.md) | θ₁₂, θ₂₃, θ₁₃, δ_CP | 4 |
| [07_neutrino_cosmology.md](07_neutrino_cosmology.md) | Σm_ν, Ω_Λ, z_CMB, H₀, n_s | 5 |
| [08_extended_constants.md](08_extended_constants.md) | m_t/v, Ω_b, N_eff, m_Z/v, Ω_DM, T_CMB, Δm_np, η_B | 8 |
| [09_hierarchy_absolute.md](09_hierarchy_absolute.md) | M_Pl/v, v, m_e, all absolute masses | 18 |
| [10_composite_predictions.md](10_composite_predictions.md) | m_π/m_e, r_p, B_d/m_p, σ₈, S_CHSH, Δm², r | 7 |
| [SUMMARY.md](SUMMARY.md) | All constants classification summary | 58 |

## Classification Counts

See [SUMMARY.md](SUMMARY.md) for the definitive tally.
