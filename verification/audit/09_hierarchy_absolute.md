# Audit: Hierarchy & Absolute Masses

## #35. Planck/VEV Hierarchy M_Pl/v

**Formula:** M_Pl/v = φ^(80−ε), where ε = 28/248

**GSM = 4.959×10¹⁶, Exp = 4.959×10¹⁶, Error = 0.01%**

| Term | Value | Classification | Justification |
|------|-------|----------------|---------------|
| 80 | — | See below | 80 = 2×(30+8+2) |
| 30 | — | `[GEOMETRIC]` | Coxeter number h(E₈) |
| 8 | — | `[GEOMETRIC]` | rank(E₈) |
| 2 (in 30+8+2) | — | ⚠️ `[GEOMETRIC/WEAK]` | Called "stabilization" or "4D projection correction". Justified as first Casimir degree C₂, or dim of Cartan of SU(2), or index of first trivial representation. See below for detailed analysis |
| 2 (overall factor) | — | `[GEOMETRIC]` | Factor of 2 from 600-cell dual shells (two concentric φ-scaled copies) |
| ε = 28/248 | 0.1129 | `[GEOMETRIC]` | Torsion ratio dim(SO(8))/dim(E₈) |
| 80−ε | 79.887 | — | Net exponent |

**The "+2" issue:**
The exponent 80 = 2(h + rank + 2) contains a "+2" that is described as "stabilization" or "4D projection correction." Possible geometric origins:
1. **C₂ = 2** (first Casimir degree) — this is the most natural: the three summands are {Coxeter, rank, first Casimir} = {30, 8, 2}
2. **dim(H₁) = 2** — the Cartan subalgebra of SU(2)
3. **Euler characteristic χ = 2** of S² (the 2-sphere, which is the simplest H₄ orbit space)

Interpretation (1) is cleanest: the tower height is Coxeter + rank + first_Casimir = 30 + 8 + 2 = 40, reflecting the three most fundamental E₈ invariants. The factor of 2 doubles this for the dual-shell structure.

**Classification: FULLY_DERIVED** if interpretation (1) is accepted. The "+2" = C₂ is the most natural geometric constant in the Casimir set.

---

## #36. Higgs VEV v

**Formula:** v = M_Pl / φ^(80−ε)

**Classification: `[DERIVED]`** — directly from #35, inverting the hierarchy formula.

---

## #37. Electron Mass m_e

**Formula:** m_e = v × φ⁻²⁷ × (1 − φ⁻⁵ + ε·φ⁻⁹)

**GSM = 0.5108 MeV, Exp = 0.5110 MeV, Error = 0.036%**

| Term | Value | Classification | Justification |
|------|-------|----------------|---------------|
| v | 246 GeV | `[DERIVED]` | From hierarchy formula (#35/#36) |
| φ⁻²⁷ | 1.67×10⁻⁶ | ⚠️ `[GEOMETRIC/WEAK]` | **27 = dim of E₆ fundamental representation.** FORMULAS.md identifies this. The electron exponent equals the dimension of the first non-trivial E₆ representation |
| 1 − φ⁻⁵ | 0.9098 | `[GEOMETRIC]` | 5 = H₂ Coxeter number |
| ε·φ⁻⁹ | 0.001486 | `[GEOMETRIC]` | Torsion × half-Casimir C₁₈/2 |

**The exponent 27 issue:**
The exponent 27 is NOT in the "allowed exponent set" S listed in FORMULAS.md (which goes up to 34 but omits 27). It IS the dimension of the fundamental representation of E₆ (the **27** of E₆). In the E₈ branching E₈ → E₆ × SU(3), the 248 decomposes as:

```
248 → (78,1) + (1,8) + (27,3) + (27̄,3̄)
```

The electron, as the lightest charged lepton, occupies the fundamental **27** of E₆. The exponent 27 = dim(27_E₆) is thus `[COMBINATORIC]` from representation theory.

**However:** A rigorous derivation should show WHY the electron mass exponent equals the DIMENSION of its E₆ representation, not just note the numerical coincidence. This is a gap — the mechanism by which rep dimension → φ-exponent needs proof.

**Classification: PARTIALLY_DERIVED** — the exponent 27 is identified with dim(27_E₆) but the mechanism needs formal proof. Corrections are `[GEOMETRIC]`.

---

## #38–39. Muon and Tau Masses

**Formula:** m_μ = m_e × (m_μ/m_e), m_τ = m_μ × (m_τ/m_μ)

**Classification: `[DERIVED]`** — chain from #37 × #4 and #4 × #5 respectively.

---

## #40. Top Quark Mass m_t

**Formula:** m_t = (52/48 − φ⁻²) × v

**Classification: `[DERIVED]`** — from #27 (m_t/v) × #36 (v).

---

## #41. Bottom Quark Mass m_b

**Formula:** m_b = m_t / (roots(F₄) − φ⁴) = m_t / (48 − φ⁴)

**GSM = 4.196 GeV, Exp = 4.18 GeV, Error = 0.39%**

| Term | Value | Classification | Justification |
|------|-------|----------------|---------------|
| m_t | 172.7 GeV | `[DERIVED]` | From #40 |
| 48 | — | `[GEOMETRIC]` | roots(F₄) |
| φ⁴ | 6.854 | `[GEOMETRIC]` | 4 = half-Casimir C₈/2 |
| 48 − φ⁴ | 41.146 | — | Effective denominator |

**Note:** The formula m_b = m_t/(48−φ⁴) ties the bottom mass to F₄ roots and the Casimir C₈ half-degree. It is equivalent to m_b/m_c = φ² + φ⁻³ when chained with m_c.

**Classification: FULLY_DERIVED (as chain)** — `[DERIVED]` from m_t + `[GEOMETRIC]` terms.

---

## #42–45. Charm, Strange, Down, Up Quark Masses

**All derived by chaining:** m_c = m_b/(φ²+φ⁻³), m_s = m_c/[(φ⁵+φ⁻³)(1+28/(240φ²))], m_d = m_s/20, m_u = m_d×(φ⁻¹−φ⁻⁵)

**Classification: `[DERIVED]`** — chains from #41 × mass ratios (#6, #7, #8) and m_u/m_d ratio.

**m_u/m_d ratio = φ⁻¹ − φ⁻⁵:**
| Term | Classification | Justification |
|------|----------------|---------------|
| φ⁻¹ | `[ALGEBRAIC]` | First Coxeter exponent |
| φ⁻⁵ | `[GEOMETRIC]` | H₂ Coxeter number |

---

## #46–48. W, Z, Higgs Boson Masses

**All derived by:** m_X = (m_X/v) × v

**Classification: `[DERIVED]`** — from ratios (#11, #12, #30) × VEV (#36).

---

## #49. W/Z Mass Ratio (Cross-Check)

**Formula:** m_W/m_Z = cos(θ_W) — derived from sin²θ_W (#2)

**Classification: `[DERIVED]`** — cross-check, not independent.

---

## #50. Fermi Constant G_F

**Formula:** G_F = 1/(√2 × v²) — derived from VEV (#36)

**Classification: `[DERIVED]`** — standard electroweak relation.

---

## #51. Rydberg Energy R_∞

**Formula:** R_∞ = m_e × α² / 2 — derived from m_e (#37) and α (#1)

**Classification: `[DERIVED]`** — standard QED relation.
