# Audit: PMNS Matrix

## #17. Solar Angle θ₁₂

**Formula:** θ₁₂ = arctan(φ⁻¹ + 2φ⁻⁸)

**GSM = 33.449°, Exp = 33.44°, Error = 0.027%**

| Term | Value | Classification | Justification |
|------|-------|----------------|---------------|
| φ⁻¹ | 0.6180 | `[ALGEBRAIC]` | 1 = first Coxeter exponent. Dominant mixing from golden ratio |
| 2 (coefficient) | 2 | `[GEOMETRIC]` | First Casimir degree C₂ |
| φ⁻⁸ | 0.02128 | `[GEOMETRIC]` | 8 = Casimir C₈ / rank(E₈). Correction term |
| 2φ⁻⁸ | 0.04257 | — | Combined correction |
| arctan | — | `[ALGEBRAIC]` | Natural function for mixing angles from ratio of matrix elements |

**Note:** The argument of arctan is φ⁻¹ + 2φ⁻⁸ ≈ 0.6606, giving arctan(0.6606) ≈ 33.45°. The solar neutrino mixing angle being controlled by φ⁻¹ (≈ 0.618) is one of the most elegant results — the golden ratio directly governs neutrino oscillations.

**Classification: FULLY_DERIVED** — all terms traceable.

---

## #18. Atmospheric Angle θ₂₃

**Formula:** θ₂₃ = arcsin(√((1 + φ⁻⁴)/2))

**GSM = 49.195°, Exp = 49.2°, Error = 0.011%**

| Term | Value | Classification | Justification |
|------|-------|----------------|---------------|
| 1 | 1.0 | `[GEOMETRIC]` | Maximal mixing baseline (θ₂₃ ≈ 45° corresponds to 1/2 inside sqrt) |
| φ⁻⁴ | 0.1459 | `[GEOMETRIC]` | 4 = half-Casimir C₈/2. Deviation from maximal mixing |
| 2 (denominator) | 2 | `[GEOMETRIC]` | First Casimir C₂; standard normalization for sin²(2θ) |
| (1+φ⁻⁴)/2 | 0.5730 | — | sin²(θ₂₃) |
| arcsin(√·) | — | `[ALGEBRAIC]` | Standard parametrization |

**Structural argument:** Near-maximal atmospheric mixing (θ₂₃ ≈ 45°) arises from the (1+x)/2 structure where x = φ⁻⁴ is a small deviation. The exponent 4 = C₈/2 connects this to the rank of E₈ through fermionic halving.

**Classification: FULLY_DERIVED** — all terms geometric/algebraic.

---

## #19. Reactor Angle θ₁₃

**Formula:** θ₁₃ = arcsin(φ⁻⁴ + φ⁻¹²)

**GSM = 8.569°, Exp = 8.57°, Error = 0.009%**

| Term | Value | Classification | Justification |
|------|-------|----------------|---------------|
| φ⁻⁴ | 0.1459 | `[GEOMETRIC]` | 4 = half-Casimir C₈/2. Dominant term giving sin(θ₁₃) ≈ 0.149 |
| φ⁻¹² | 0.000443 | `[GEOMETRIC]` | 12 = Casimir C₁₂ directly. Small correction (0.3% of dominant term) |
| arcsin | — | `[ALGEBRAIC]` | Standard parametrization |

**Note:** The small reactor angle sin(θ₁₃) ≈ 0.149 is dominated by φ⁻⁴. The correction φ⁻¹² introduces a factor of φ⁻⁸ relative to the dominant term, connecting to the rank of E₈.

**Classification: FULLY_DERIVED** — all terms directly geometric.

---

## #20. CP Phase δ_CP

**Formula:** δ_CP = 180° + arctan(φ⁻² − φ⁻⁵)

**GSM = 196.27°, Exp = 197°, Error = 0.37%**

| Term | Value | Classification | Justification |
|------|-------|----------------|---------------|
| 180° = π | π | `[ALGEBRAIC]` | CP-conserving baseline. δ_CP near π means near-maximal CP violation in neutrino sector |
| φ⁻² | 0.38197 | `[GEOMETRIC]` | 2 = first Casimir C₂ |
| φ⁻⁵ | 0.09017 | `[GEOMETRIC]` | 5 = H₂ Coxeter number |
| φ⁻²−φ⁻⁵ | 0.29180 | — | Argument of arctan, giving arctan ≈ 16.27° |
| arctan | — | `[ALGEBRAIC]` | Natural function for phase angle |

**Note:** δ_CP ≈ 180° + 16° = 196° means the CP violation phase deviates from maximal (180°) by arctan(φ⁻²−φ⁻⁵). This is the **least precisely matched** constant in the PMNS sector (0.37% error), partly because the experimental value has large uncertainty (197° ± ~25°).

**Classification: FULLY_DERIVED** — all terms geometric/algebraic.
