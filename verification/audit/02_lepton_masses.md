# Audit: Lepton Mass Ratios

## #4. Muon/Electron Mass Ratio m_μ/m_e

**Formula:** m_μ/m_e = φ¹¹ + φ⁴ + 1 − φ⁻⁵ − φ⁻¹⁵

**GSM = 206.768, Exp = 206.768, Error = 0.00003%**

| Term | Value | Classification | Justification |
|------|-------|----------------|---------------|
| φ¹¹ | 199.005 | `[GEOMETRIC]` | 11 = Coxeter exponent of C₁₂ (d−1 = 12−1); also H₄ exponent e₂. Dominant scale for 2nd generation lepton |
| φ⁴ | 6.854 | `[GEOMETRIC]` | 4 = dim(H₄) as Coxeter group / half-Casimir C₈/2. Reflects 4D spacetime projection |
| +1 | 1.000 | `[GEOMETRIC]` | Trivial representation / baseline contribution. 1 = χ(E₈/H₄) |
| −φ⁻⁵ | −0.0902 | `[GEOMETRIC]` | 5 = Coxeter number of H₂ (pentagonal symmetry); half-Casimir C₁₀/2. Fermionic correction |
| −φ⁻¹⁵ | −0.000131 | `[GEOMETRIC]` | 15 = half-Casimir C₃₀/2 = h(E₈)/2. Fine correction from highest Casimir |

**Sign pattern (+,+,+,−,−):** The first three terms are additive (building up the mass), the last two are subtractive corrections. This pattern reflects that H₄ projection preserves the dominant exponents and subtracts fermionic half-Casimir contributions. The sign pattern is **not independently derived** — it is determined by the observation that φ¹¹ ≈ 199 is the dominant term and corrections must bring it to 206.77.

**Potential weakness:** The sign assignment (which terms are positive vs negative) lacks a rigorous derivation from first principles. While the EXPONENTS are fully geometric, the SIGNS are effectively constrained by matching experiment. This should be flagged.

**Classification: PARTIALLY_DERIVED** — exponents are `[GEOMETRIC]`, signs are `[CONSTRAINED]` (determined by consistency, not independently derived).

---

## #5. Tau/Muon Mass Ratio m_τ/m_μ

**Formula:** m_τ/m_μ = φ⁶ − φ⁻⁴ − 1 + φ⁻⁸

**GSM = 16.820, Exp = 16.817, Error = 0.016%**

| Term | Value | Classification | Justification |
|------|-------|----------------|---------------|
| φ⁶ | 17.944 | `[GEOMETRIC]` | 6 = half-Casimir C₁₂/2. Second-to-third generation jump governed by C₁₂ halved |
| −φ⁻⁴ | −0.1459 | `[GEOMETRIC]` | 4 = half-Casimir C₈/2 or dim(H₄). Sign flip relative to m_μ/m_e formula |
| −1 | −1.000 | `[GEOMETRIC]` | Baseline subtraction (sign flipped from m_μ/m_e) |
| +φ⁻⁸ | +0.02128 | `[GEOMETRIC]` | 8 = Casimir C₈ / rank(E₈). Fine correction |

**Sign pattern (+,−,−,+):** Compared to m_μ/m_e = (+,+,+,−,−), the sign pattern alternates. The derivation scripts note that "sign differs for higher generations" and attribute this to the subtractive nature of the τ−μ splitting versus the additive μ−e enhancement. This alternation is **suggestive but not rigorously proven** from E₈ representation theory.

**Same weakness as #4:** Sign assignments are not independently derived.

**Classification: PARTIALLY_DERIVED** — exponents `[GEOMETRIC]`, signs `[CONSTRAINED]`.
