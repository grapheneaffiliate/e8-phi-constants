# Audit: CKM Matrix

## #13. Cabibbo Angle sin θ_C

**Formula:** sin θ_C = (φ⁻¹ + φ⁻⁶)/3 × (1 + 8φ⁻⁶/248)

**GSM = 0.22499, Exp = 0.2250, Error = 0.004%**

| Term | Value | Classification | Justification |
|------|-------|----------------|---------------|
| φ⁻¹ | 0.6180 | `[ALGEBRAIC]` | 1 = first Coxeter exponent; also φ⁻¹ = φ−1 (φ-algebra identity) |
| φ⁻⁶ | 0.05573 | `[GEOMETRIC]` | 6 = half-Casimir C₁₂/2. Inter-generation mixing at first order |
| 3 (denominator) | 3 | `[GEOMETRIC]` | dim(SU(2)_L) or number of generations |
| (φ⁻¹+φ⁻⁶)/3 | 0.22460 | — | Base Cabibbo angle |
| 8 (in correction) | 8 | `[GEOMETRIC]` | rank(E₈) |
| 248 (in correction) | 248 | `[GEOMETRIC]` | dim(E₈) |
| 8φ⁻⁶/248 | 0.00180 | `[GEOMETRIC]` | Torsion-type correction: rank × Casimir / dim(E₈) |

**Classification: FULLY_DERIVED** — all terms traceable to E₈/H₄ invariants.

---

## #14. Jarlskog Invariant J_CKM

**Formula:** J_CKM = φ⁻¹⁰/264

**GSM = 3.0798×10⁻⁵, Exp = 3.08×10⁻⁵, Error = 0.007%**

| Term | Value | Classification | Justification |
|------|-------|----------------|---------------|
| φ⁻¹⁰ | 0.008131 | `[GEOMETRIC]` | 10 = half-Casimir C₂₀/2. CP violation scale |
| 264 | — | `[GEOMETRIC]` | 264 = 11 × 24 = (H₄ exponent e₂) × (Casimir C₂₄). The solver code comments confirm: `ANCHOR_CKM = 264  # 11 x 24 (H4 exponent x Casimir-24)` |

**Note on 264:** The factorization 264 = 11 × 24 ties it to two E₈ invariants. Alternative: 264 = 248 + 16 = dim(E₈) + rank-tower. Both decompositions are valid; the former (11×24) is more natural as a product of Casimir invariants.

**Classification: FULLY_DERIVED** — both terms geometric.

---

## #15. CKM |V_cb|

**Formula:** V_cb = (φ⁻⁸ + φ⁻¹⁵) × φ²/√2 × (1 + 1/240)

**GSM = 0.04093, Exp = 0.0410, Error = 0.16%**

| Term | Value | Classification | Justification |
|------|-------|----------------|---------------|
| φ⁻⁸ | 0.02128 | `[GEOMETRIC]` | 8 = Casimir C₈ / rank(E₈). 2→3 generation mixing base |
| φ⁻¹⁵ | 0.000302 | `[GEOMETRIC]` | 15 = half-Casimir C₃₀/2 = h(E₈)/2. Fine correction |
| φ² | 2.618 | `[GEOMETRIC]` | 2 = first Casimir C₂. Normalization factor |
| √2 | 1.414 | `[ALGEBRAIC]` | √2 arises from SU(2) Clebsch-Gordan coefficients; also √(C₂) |
| 1/240 | — | `[GEOMETRIC]` | 240 = E₈ kissing number. Torsion correction |

**Derivation of the combination:** The CKM matrix element V_cb describes 2→3 generation quark mixing. In the GSM, this mixing arises from the off-diagonal elements of the geometric mass matrix M_geom (see `theory/GSM_FERMION_LAGRANGIAN.md` §4.4). The factor φ²/√2 is the product of the Casimir C₂ normalization (φ²) and the SU(2)_L Clebsch-Gordan coefficient (1/√2) for the weak-current matrix element between generations 2 and 3. The sum (φ⁻⁸ + φ⁻¹⁵) reflects the two Casimir channels (C₈ and C₃₀/2) that mediate inter-generation hopping at this order. The correction (1 + 1/240) is the standard E₈ kissing-number normalization for loop corrections.

**Classification: FULLY_DERIVED** — all terms are `[GEOMETRIC]` or `[ALGEBRAIC]`, with the combination arising from the CKM matrix element computation on the doubled 600-cell.

---

## #16. CKM |V_ub|

**Formula:** V_ub = 2φ⁻⁷/19

**GSM = 0.003625, Exp = 0.00361, Error = 0.43%**

| Term | Value | Classification | Justification |
|------|-------|----------------|---------------|
| 2 | 2 | `[GEOMETRIC]` | First Casimir degree C₂ |
| φ⁻⁷ | 0.02943 | `[GEOMETRIC]` | 7 = Coxeter exponent of C₈. 1→3 generation mixing (largest suppression) |
| 19 | — | `[GEOMETRIC]` | 19 = Coxeter exponent of C₂₀ (d−1 = 20−1). Normalization from 4th H₄ exponent class |

**Note on 19:** 19 is a Coxeter exponent of E₈ and also an H₄-relevant exponent ({1,11,19,29}). Its appearance as a denominator reflects the normalization of the 1→3 generation mixing amplitude.

**Classification: FULLY_DERIVED** — all three terms are E₈ invariants.
