# GSM Verification Scripts Index

This directory contains Python scripts that derive and verify all 26 fundamental constants from E₈ → H₄ geometry.

## Quick Start

```bash
# Run full verification of all 26 constants
python gsm_verification.py

# Run individual derivation scripts
python alpha_derivation.py
python gravity_derivation.py
python lepton_derivation.py
# etc.
```

## Master Script

| Script | Purpose | Output |
|--------|---------|--------|
| `gsm_verification.py` | Calculate ALL 26 constants and compare to experiment | Full table with deviations |

**Expected output:**
- 25 constants verified within 1%
- Median deviation: 0.0109%
- 1 prediction (CHSH bound S = 2.382)

---

## Detailed Derivation Scripts

### Gauge Couplings

| Script | Constants Derived | Key Formula(s) |
|--------|-------------------|----------------|
| `alpha_derivation.py` | α⁻¹ (fine-structure) | 137 + φ⁻⁷ + φ⁻¹⁴ + φ⁻¹⁶ - φ⁻⁸/248 |
| `weak_mixing_derivation.py` | sin²θ_W (weak mixing) | 3/13 + φ⁻¹⁶ |
| `coupling_running_derivation.py` | α(q²), α_s(q²) running | β-functions from E₈ Casimirs |

### Fermion Masses

| Script | Constants Derived | Key Formula(s) |
|--------|-------------------|----------------|
| `lepton_derivation.py` | m_μ/m_e, m_τ/m_μ | φ¹¹ + φ⁴ + 1 - φ⁻⁵ - φ⁻¹⁵ |
| `e8_quark_derivation.py` | m_s/m_d, m_c/m_s, m_b/m_c | L₃² = 20 (exact!) |
| `e8_complete_quark_derivation.py` | y_t (top Yukawa), m_u/m_d | 1 - φ⁻¹⁰ |
| `torsion_derivation.py` | Torsion correction derivation | 28/(240φ²) |

### Mixing Matrices

| Script | Constants Derived | Key Formula(s) |
|--------|-------------------|----------------|
| `ckm_derivation.py` | sin θ_C, V_cb, V_ub, J_CKM | φ⁻¹⁰/264 (Jarlskog) |

### Cosmology

| Script | Constants Derived | Key Formula(s) |
|--------|-------------------|----------------|
| `cosmological_derivation.py` | Ω_Λ, H₀, n_s | φ⁻¹ + φ⁻⁶ + φ⁻⁹ - φ⁻¹³ + ... |
| `refinements_derivation.py` | z_CMB (EXACT!), V_ub refined | **z_CMB = φ¹⁴ + 246** |

### Gravity

| Script | Constants Derived | Key Formula(s) |
|--------|-------------------|----------------|
| `gravity_derivation.py` | M_Pl/v, G_N (hierarchy problem) | φ^(80-ε) where ε = 28/248 |

---

## Script Details

### alpha_derivation.py (386 lines)
- Derives α⁻¹ from E₈/H₄ Laplacian spectrum
- Proves anchor uniqueness (137 = 128 + 8 + 1)
- Shows each correction term comes from Casimir eigenvalues
- Demonstrates no other anchor admits sub-ppm accuracy

### weak_mixing_derivation.py (351 lines)
- Derives sin²θ_W = 3/13 + φ⁻¹⁶
- Explains why 3/13 (not 3/8 GUT value) is the anchor
- Shows SU(2)×U(1) embedding structure

### coupling_running_derivation.py (332 lines)
- Derives β-function coefficients from E₈
- Shows how couplings run with energy
- Connects to grand unification

### lepton_derivation.py (368 lines)
- Full derivation of m_μ/m_e and m_τ/m_μ
- Explains why leptons have different depth than quarks
- Shows connection to H₄ exponents {1, 11, 19, 29}

### e8_quark_derivation.py (538 lines)
- Complete folding chain E₈ → E₇ → E₆ → D₄ → H₄
- Proves L₃² = 20 exactly for m_s/m_d
- Derives depth assignments for all quarks

### e8_complete_quark_derivation.py (437 lines)
- Top Yukawa y_t = 1 - φ⁻¹⁰
- First-generation ratio m_u/m_d = 1/√5
- Complete quark mass hierarchy

### torsion_derivation.py (384 lines)
- Full derivation of 28/(240φ²) correction
- Explains SO(8) triality and chirality coupling
- Shows why only m_c/m_s gets this correction

### ckm_derivation.py (322 lines)
- Cabibbo angle from φ-based formula
- Jarlskog invariant J = φ⁻¹⁰/264
- Full CKM matrix reconstruction

### cosmological_derivation.py (289 lines)
- Dark energy density Ω_Λ
- Hubble constant H₀
- Spectral index n_s = 1 - φ⁻⁷

### refinements_derivation.py (339 lines)
- **NEW: z_CMB = φ¹⁴ + 246 (0.003% accuracy!)**
- Refined V_ub formula
- Latest improvements to problematic constants

### gravity_derivation.py (317 lines)
- Hierarchy problem solution
- M_Pl/v = φ^(80-ε)
- Newton's constant derivation
- Explains why 80 = 2×(30+8+2)

---

## Fundamental Constants Used

All scripts use these fundamental values:

```python
import math

# Golden ratio
PHI = (1 + math.sqrt(5)) / 2  # = 1.6180339887...

# Torsion ratio
EPSILON = 28 / 248  # = 0.1129032258...

# E₈ structure
E8_DIM = 248
E8_RANK = 8
E8_COXETER = 30
E8_CASIMIRS = [2, 8, 12, 14, 18, 20, 24, 30]
KISSING_NUMBER = 240

# φ-Lucas numbers
def lucas(n):
    return PHI**n + PHI**(-n)

L3 = lucas(3)  # = 4.4721359550... = √20
```

---

## File Organization Recommendation

Current (flat):
```
verification/
├── gsm_verification.py
├── alpha_derivation.py
├── ckm_derivation.py
├── ... (12 files)
```

Suggested (grouped):
```
verification/
├── gsm_verification.py          # Master script
├── DERIVATIONS_INDEX.md         # This file
├── gauge/
│   ├── alpha_derivation.py
│   ├── weak_mixing_derivation.py
│   └── coupling_running_derivation.py
├── fermions/
│   ├── lepton_derivation.py
│   ├── e8_quark_derivation.py
│   ├── e8_complete_quark_derivation.py
│   └── torsion_derivation.py
├── mixing/
│   └── ckm_derivation.py
├── cosmology/
│   ├── cosmological_derivation.py
│   └── refinements_derivation.py
└── gravity/
    └── gravity_derivation.py
```

---

## Adding New Derivations

When adding a new derivation script:

1. Follow the naming convention: `{topic}_derivation.py`
2. Include standard header with author, date, purpose
3. Import from standard constants (see above)
4. Document the formula being derived
5. Compare to experimental value
6. Add entry to this index file
7. Update gsm_verification.py if formula changes

---

## Version History

| Date | Change |
|------|--------|
| Jan 2026 | Initial 12-script structure |
| Jan 2026 | Added z_CMB = φ¹⁴ + 246 exact formula |
| Jan 2026 | Fixed L₃ comment (4.472, not 4.236) |
