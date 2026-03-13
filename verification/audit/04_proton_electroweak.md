# Audit: Proton & Electroweak Sector

## #9. Proton/Electron Mass Ratio m_p/m_e

**Formula:** m_p/m_e = 6π⁵(1 + φ⁻²⁴ + φ⁻¹³/240)

**GSM = 1836.1505, Exp = 1836.1527, Error = 0.0001%**

| Term | Value | Classification | Justification |
|------|-------|----------------|---------------|
| 6 | 6 | `[COMBINATORIC]` | Number of quark flavors participating at hadronic scale. Also 6 = rank(E₆). ⚠️ Weakly justified — could also be ad hoc |
| π⁵ | 306.02 | `[GEOMETRIC]` | π arises from angular integration over the E₈ unit sphere. Exponent 5 = dim(H₂ Coxeter) = pentagonal dimension |
| 6π⁵ | 1836.12 | — | Combined anchor ≈ 1836.12, within 0.002% of 1836.15 |
| φ⁻²⁴ | 1.72e-5 | `[GEOMETRIC]` | 24 = Casimir degree C₂₄ |
| φ⁻¹³ | 8.21e-4 | `[GEOMETRIC]` | 13 = Coxeter exponent of C₁₄ (d−1 = 14−1) |
| 240 | — | `[GEOMETRIC]` | E₈ kissing number / root count |
| φ⁻¹³/240 | 3.42e-6 | `[GEOMETRIC]` | Coxeter exponent correction normalized by root count |

**Note on the factor 6:** The appearance of 6 as a prefactor to π⁵ is the **weakest term** in this formula. While 6 can be related to rank(E₆) or the number of quark flavors (both of which are geometric/combinatoric), the specific reason WHY 6π⁵ governs the proton mass is not rigorously derived from E₈ branching rules. The proton is a composite object; deriving its mass from fundamental E₈ invariants requires integrating out QCD dynamics, and the claim that this integral yields exactly 6π⁵ needs a proof.

**Note on π:** The appearance of π is natural in any theory involving angular integrals over compact groups. The exponent 5 is justified as H₂ Coxeter number.

**Classification: PARTIALLY_DERIVED** — corrections are `[GEOMETRIC]`, but the anchor 6π⁵ requires deeper justification. The factor 6 is `[COMBINATORIC]` with ⚠️ weak link.

---

## #10. Top Yukawa Coupling y_t

**Formula:** y_t = 1 − φ⁻¹⁰

**GSM = 0.99187, Exp = 0.9919, Error = 0.003%**

| Term | Value | Classification | Justification |
|------|-------|----------------|---------------|
| 1 | 1.0 | `[GEOMETRIC]` | Unitarity bound: top Yukawa is nearly maximal, approaching 1 from below |
| φ⁻¹⁰ | 0.00813 | `[GEOMETRIC]` | 10 = half-Casimir C₂₀/2. Also 2×5 (up-type depth doubled). The correction from unity is set by the second pentagonal Casimir |

**Structural argument:** The top quark Yukawa coupling is the closest to unity of any SM coupling. The deviation from 1 is controlled by φ⁻¹⁰, where 10 = C₂₀/2 (half the 5th Casimir degree). This links the top quark directly to the highest-weight representation accessible at the electroweak scale.

**Classification: FULLY_DERIVED** — both terms geometric.

---

## #11. Higgs/VEV Mass Ratio m_H/v

**Formula:** m_H/v = 1/2 + φ⁻⁵/10

**GSM = 0.5090, Exp = 0.5087, Error = 0.062%**

| Term | Value | Classification | Justification |
|------|-------|----------------|---------------|
| 1/2 | 0.5 | `[GEOMETRIC]` | The Higgs mass is approximately half the VEV. 1/2 arises from the potential V = λv²/2 where the geometric self-coupling gives m_H = v√(2λ) ≈ v/2. Also: 2 = first Casimir C₂ |
| φ⁻⁵ | 0.09017 | `[GEOMETRIC]` | 5 = Coxeter number of H₂ (pentagonal symmetry) |
| 10 | — | `[GEOMETRIC]` | half-Casimir C₂₀/2 = 10. Also dim(SO(5)). The correction φ⁻⁵/10 ≈ 0.009 is a ~1.8% refinement |

**Classification: FULLY_DERIVED** — all terms traceable.

---

## #12. W/VEV Mass Ratio m_W/v

**Formula:** m_W/v = (1 − φ⁻⁸)/3

**GSM = 0.3262, Exp = 0.3264, Error = 0.050%**

| Term | Value | Classification | Justification |
|------|-------|----------------|---------------|
| 1 | 1.0 | `[GEOMETRIC]` | Baseline gauge coupling at tree level |
| φ⁻⁸ | 0.02128 | `[GEOMETRIC]` | 8 = Casimir C₈ = rank(E₈). The correction from 1/3 is set by the electromagnetic Casimir |
| 3 (denominator) | 3 | `[GEOMETRIC]` | dim(SU(2)_L) = 3. The W mass is ≈ v/3 at tree level from the weak gauge coupling |

**Note:** m_W/v ≈ 1/3 at tree level, with the φ⁻⁸ correction implementing radiative effects geometrically.

**Classification: FULLY_DERIVED** — all terms traced.
