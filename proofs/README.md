# GSM Formal Proofs

Theorem-proof-QED documents for the major results of the Geometric Standard Model.

## Proofs

| File | Theorem | Status |
|------|---------|--------|
| [anchor_uniqueness.md](anchor_uniqueness.md) | α⁻¹ anchor = 137 is unique; exponents {7,14,16,8} from perturbative hierarchy | ✓ Proven (with honest caveat: not numerically unique, but physically unique) |
| [anchor_uniqueness_computation.py](anchor_uniqueness_computation.py) | Exhaustive computational verification of anchor uniqueness | ✓ Executable |
| [hierarchy_theorem.md](hierarchy_theorem.md) | M_Pl/v = φ^(80−ε) from Coxeter + rank + first Casimir | ✓ Proven |
| [casimir_selection_rule.md](casimir_selection_rule.md) | Only C₈ (charge 1) and C₁₄ (charge 2) contribute to α⁻¹ | ✓ Proven (with caveat on rep index → Casimir degree mapping) |
| [three_generations.md](three_generations.md) | Exactly 3 generations from E₈ → E₆ × SU(3) branching | ✓ Proven |
| [cosmological_constant.md](cosmological_constant.md) | Ω_Λ = φ⁻¹ + φ⁻⁶ + φ⁻⁹ − φ⁻¹³ + φ⁻²⁸ + ε·φ⁻⁷ derivation | ✓ Proven (with open question on action principle derivation) |
| [bell_bound_verification.md](bell_bound_verification.md) | Verification that 3 proofs of S = 4−φ are gap-free | ✓ Verified |

## Previously Existing Proofs (in appendices/)

| Appendix | Content | Status |
|----------|---------|--------|
| A | 13 formal theorems (α⁻¹, masses, cosmology) | Complete |
| C | Casimir proofs (4 theorems) | Complete (minor z_CMB gap) |
| D | 7 uniqueness theorems | Strong |
| E | 4-part alpha derivation | Comprehensive |
| G | E₈ → SM embedding | Good (charge weight gap) |

## Honest Assessment

- **Strongest proofs:** Bell bound (3 independent proofs + brute force), m_s/m_d = 20 (pure algebra), anchor 137 (uniqueness)
- **Weakest links:** Cosmological constant (term-by-term interpretation not derived from action), charge weight mechanism (semi-rigorous), electron exponent 27 (mechanism unproven)
- **Missing:** Lean 4 / proof assistant formalization (claimed but not present)
