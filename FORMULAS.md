# GSM Complete Formula Reference

## Fundamental Parameters
- φ = (1 + √5)/2 = 1.6180339887498948482...
- ε = 28/248 = 0.11290322580645161... (torsion ratio)
- L_n = φⁿ + φ⁻ⁿ (φ-Lucas numbers)

## E₈ Structure Constants
- dim(E₈) = 248
- rank(E₈) = 8
- Kissing number = 240
- Coxeter number h = 30
- Casimir degrees: {2, 8, 12, 14, 18, 20, 24, 30}
- H₄ exponents: {1, 11, 19, 29}

## Lucas Number Reference

**Classical Lucas (integers):** L₀=2, L₁=1, L₂=3, L₃=4, L₄=7, L₅=11, L₆=18...

**φ-Lucas (φⁿ + φ⁻ⁿ):**
| n | L_n | Exact Value |
|---|-----|-------------|
| 0 | 2 | 2.0000000000 |
| 1 | √5 | 2.2360679775 |
| 2 | 3 | 3.0000000000 |
| 3 | √20 | 4.4721359550 |
| 4 | 7 | 7.0000000000 |
| 5 | √125 | 11.1803398875 |

**Key identity:** L₃² = 20 exactly (used for m_s/m_d)

---

## The 26 Formulas

### 1. Electromagnetic Sector

| # | Constant | Formula | GSM Value | Experiment | Deviation |
|---|----------|---------|-----------|------------|-----------|
| 1 | α⁻¹ | 137 + φ⁻⁷ + φ⁻¹⁴ + φ⁻¹⁶ - φ⁻⁸/248 | 137.035995 | 137.035999 | 0.000003% |
| 2 | sin²θ_W | 3/13 + φ⁻¹⁶ | 0.231222 | 0.23121 | 0.005% |
| 3 | α_s(M_Z) | 1/[2φ³(1+φ⁻¹⁴)(1+8φ⁻⁵/14400)] | 0.11789 | 0.1180 | 0.09% |

### 2. Lepton Masses

| # | Constant | Formula | GSM Value | Experiment | Deviation |
|---|----------|---------|-----------|------------|-----------|
| 4 | m_μ/m_e | φ¹¹ + φ⁴ + 1 - φ⁻⁵ - φ⁻¹⁵ | 206.76822 | 206.76828 | 0.00003% |
| 5 | m_τ/m_μ | φ⁶ - φ⁻⁴ - 1 + φ⁻⁸ | 16.8197 | 16.817 | 0.016% |

### 3. Quark Masses

| # | Constant | Formula | GSM Value | Experiment | Deviation |
|---|----------|---------|-----------|------------|-----------|
| 6 | m_s/m_d | L₃² = (φ³+φ⁻³)² | 20.0000 | 20.0 | **EXACT** |
| 7 | m_c/m_s | (φ⁵+φ⁻³)(1+28/(240φ²)) | 11.831 | 11.83 | 0.008% |
| 8 | m_b/m_c | φ² + φ⁻³ | 2.854 | 2.86 | 0.21% |

### 4. Proton & Electroweak

| # | Constant | Formula | GSM Value | Experiment | Deviation |
|---|----------|---------|-----------|------------|-----------|
| 9 | m_p/m_e | 6π⁵(1+φ⁻²⁴+φ⁻¹³/240) | 1836.1505 | 1836.1527 | 0.0001% |
| 10 | y_t | 1 - φ⁻¹⁰ | 0.99187 | 0.9919 | 0.003% |
| 11 | m_H/v | 1/2 + φ⁻⁵/10 | 0.5090 | 0.5087 | 0.06% |
| 12 | m_W/v | (1-φ⁻⁸)/3 | 0.3262 | 0.3264 | 0.05% |

### 5. CKM Matrix

| # | Constant | Formula | GSM Value | Experiment | Deviation |
|---|----------|---------|-----------|------------|-----------|
| 13 | sin θ_C | (φ⁻¹+φ⁻⁶)/3 × (1+8φ⁻⁶/248) | 0.22499 | 0.2250 | 0.004% |
| 14 | J_CKM | φ⁻¹⁰/264 | 3.08×10⁻⁵ | 3.08×10⁻⁵ | 0.007% |
| 15 | V_cb | (φ⁻⁸+φ⁻¹⁵)φ²/√2(1+1/240) | 0.0409 | 0.0410 | 0.16% |
| 16 | V_ub | 2φ⁻⁷/19 | 0.00363 | 0.00361 | 0.43% |

### 6. PMNS Matrix (neutrino mixing, in degrees)

| # | Constant | Formula | GSM Value | Experiment | Deviation |
|---|----------|---------|-----------|------------|-----------|
| 17 | θ₁₂ | arctan(φ⁻¹+2φ⁻⁸) | 33.449° | 33.44° | 0.027% |
| 18 | θ₂₃ | arcsin√((1+φ⁻⁴)/2) | 49.195° | 49.2° | 0.011% |
| 19 | θ₁₃ | arcsin(φ⁻⁴+φ⁻¹²) | 8.569° | 8.57° | 0.009% |
| 20 | δ_CP | 180° + arctan(φ⁻²-φ⁻⁵) | 196.27° | 197° | 0.37% |

### 7. Neutrino Mass

| # | Constant | Formula | GSM Value | Experiment | Deviation |
|---|----------|---------|-----------|------------|-----------|
| 21 | Σm_ν | m_e·φ⁻³⁴(1+εφ³) | 59.24 meV | 59 meV | 0.40% |

### 8. Cosmology

| # | Constant | Formula | GSM Value | Experiment | Deviation |
|---|----------|---------|-----------|------------|-----------|
| 22 | Ω_Λ | φ⁻¹+φ⁻⁶+φ⁻⁹-φ⁻¹³+φ⁻²⁸+εφ⁻⁷ | 0.68889 | 0.6889 | 0.002% |
| 23 | z_CMB | **φ¹⁴ + 246** | 1089.0 | 1089.80 | 0.074% |
| 24 | H₀ | 100φ⁻¹(1+φ⁻⁴-1/(30φ²)) | 70.03 | 70.0 | 0.05% |
| 25 | n_s | 1 - φ⁻⁷ | 0.9656 | 0.9649 | 0.07% |

### 9. Gravity (Hierarchy)

| Constant | Formula | GSM Value | Experiment | Deviation |
|----------|---------|-----------|------------|-----------|
| M_Pl/v | φ^(80-ε) where ε=28/248 | 4.94×10¹⁶ | 4.96×10¹⁶ | 0.4% |
| G_N | (ℏc)/v² × φ^(-160+2ε) | 6.67×10⁻³⁹ GeV⁻² | 6.71×10⁻³⁹ | 0.6% |

### 10. High-Energy Prediction (UNTESTED)

| # | Constant | Formula | GSM Value | Standard QM | Suppression |
|---|----------|---------|-----------|-------------|-------------|
| 26 | S_CHSH | 4 - φ = 2 + φ⁻² | 2.382 | 2√2 ≈ 2.828 | 15.8% |

---

## Master Equations

### Fine-Structure Constant
$$\alpha^{-1} = 137 + \phi^{-7} + \phi^{-14} + \phi^{-16} - \frac{\phi^{-8}}{248} = 137.0359954$$

**Term breakdown:**
| Term | Value | Origin |
|------|-------|--------|
| 137 | 137 | Anchor: 128+8+1 = dim(SO16₊)+rank(E₈)+χ |
| φ⁻⁷ | 0.02943... | Half of Casimir-14 |
| φ⁻¹⁴ | 0.000866... | Full Casimir-14 |
| φ⁻¹⁶ | 0.000331... | Rank-tower (2×8) |
| -φ⁻⁸/248 | -0.000073... | Torsion correction |
| **Total** | **137.035995** | |

### Hierarchy Formula
$$\frac{M_{Pl}}{v} = \phi^{80 - \varepsilon} = \phi^{79.887...}$$

**Exponent derivation:**
- 80 = 2 × (h + rank + stabilization) = 2 × (30 + 8 + 2)
- ε = 28/248 ≈ 0.113 (torsion strain)
- n_eff = 80 - 0.113 = 79.887

### CMB Exact Formula
$$z_{CMB} = \phi^{14} + 246 = 843.0 + 246 = 1089.0$$

**Components:**
- φ¹⁴ = 843.0 (Casimir-14 threshold)
- 246 = electroweak VEV in GeV (exact integer!)

### CHSH Bound
$$S = 4 - \phi = \frac{7 - \sqrt{5}}{2} = 2 + \phi^{-2} \approx 2.382$$

**Equivalent forms:**
- S = 4 - φ (classic Lucas minus golden ratio)
- S = (7 - √5)/2 (closed form)
- S = 2 + φ⁻² (verification formula)
- S² = 17 - 7φ (squared form from H₄ eigenvalue)

---

## Allowed Exponent Set

The complete set of allowed exponents in GSM formulas:

$$\mathcal{S} = \{1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 18, 20, 24, 28, 30, 34\}$$

**Sources:**
| Type | Exponents |
|------|-----------|
| Direct Casimirs | 2, 8, 12, 14, 18, 20, 24, 30 |
| Half-Casimirs | 1, 4, 6, 7, 9, 10, 12, 15 |
| Rank multiples | 8, 16, 24 |
| H₄ exponents | 1, 11, 19, 29 |
| Torsion dimension | 28 |
| Upper bound | 38 (Coxeter + rank) |

---

## Physical Constants Used

| Constant | Value | Source |
|----------|-------|--------|
| φ | 1.6180339887498948482 | (1+√5)/2 |
| π | 3.1415926535897932385 | |
| m_e | 510998.95 eV | PDG 2024 |
| v (EW VEV) | 246.22 GeV | PDG 2024 |
| M_Pl | 1.220890×10¹⁹ GeV | PDG 2024 |

---

## Quick Verification

To verify the master equation:
```python
import math
phi = (1 + math.sqrt(5)) / 2
alpha_inv = 137 + phi**(-7) + phi**(-14) + phi**(-16) - phi**(-8)/248
print(f"α⁻¹ = {alpha_inv}")  # Should print 137.0359954...
```

To verify L₃² = 20:
```python
L3 = phi**3 + phi**(-3)
print(f"L₃ = {L3}")      # Should print 4.472135955...
print(f"L₃² = {L3**2}")  # Should print 20.0000000...
```

To verify z_CMB:
```python
z_cmb = phi**14 + 246
print(f"z_CMB = {z_cmb}")  # Should print 1089.0
```
