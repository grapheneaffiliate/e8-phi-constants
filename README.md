# The Geometric Standard Model (GSM)

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

> **Physics ≡ Geometry(E₈ → H₄)**

## Overview

This repository presents **The Geometric Standard Model (GSM)** — a mathematical framework demonstrating that the 26 fundamental constants of the Standard Model and cosmology are not free parameters but **geometric invariants** of the unique projection from the E₈ Lie algebra onto the H₄ icosahedral Coxeter group.

### Key Results

| Property | Value |
|----------|-------|
| **Foundation** | E₈ lattice (unique by Viazovska 2016 Fields Medal proof) |
| **Projection** | E₈ → H₄ icosahedral mapping |
| **Selection rules** | Casimir degrees {2, 8, 12, 14, 18, 20, 24, 30} |
| **Constants derived** | 25 confirmed + 1 high-energy prediction |
| **Median deviation** | 0.03% |
| **Maximum deviation** | < 1% (all 25 confirmed constants) |
| **Free parameters** | **Zero** |

## The Master Equation

```
α⁻¹ = 137 + φ⁻⁷ + φ⁻¹⁴ + φ⁻¹⁶ - φ⁻⁸/248 = 137.0359954...
```

Where:
- **137** = Topological invariant of the gauge embedding
- **φ** = Golden ratio (1 + √5)/2 from icosahedral eigenvalue
- **248** = Dimension of E₈
- Each exponent is a Casimir eigenvalue or derived class

## Repository Structure

```
├── paper/
│   ├── GSM_v1_Complete.pdf        # Publication-ready paper (17 pages)
│   ├── GSM_v1_Complete.tex        # LaTeX source for arXiv submission
│   └── GSM_v1_Complete.md         # Markdown version of main paper
├── appendices/
│   ├── GSM_v1_Appendix_Formal_Proofs.md      # Appendix A: Theorem proofs
│   └── GSM_v1_Appendix_B_Complete_Formalization.md  # Appendix B: Complete formalization
└── verification/
    └── gsm_verification.py        # Python verification script
```

## Summary of Derived Constants

### Electromagnetic Sector
- **α⁻¹** = 137.0360 (exp: 137.0360) — 0.000003% deviation
- **sin²θ_W** = 0.23122 (exp: 0.23122) — 0.001% deviation
- **α_s(M_Z)** = 0.1179 (exp: 0.1179) — 0.01% deviation

### Mass Ratios
- **m_μ/m_e** = 206.768 (exp: 206.768) — 0.00003% deviation
- **m_s/m_d** = 20.000 (exp: 20.0) — **Exact** (Lucas eigenvalue L₃²)
- **m_p/m_e** = 1836.15 (exp: 1836.15) — 0.0001% deviation

### CKM & PMNS Mixing
- All 8 mixing parameters derived from H₄ exponents
- Jarlskog invariant J_CKM = φ⁻¹⁰/264 = 3.08×10⁻⁵

### Cosmological Parameters
- **Ω_Λ** = 0.6889 (exp: 0.6889) — 0.002% deviation
- **H₀** = 70.0 km/s/Mpc — geometric mean resolution
- **n_s** = 0.9656 (exp: 0.9649) — 0.07% deviation

### High-Energy Prediction
- **S (CHSH)** = 2 + φ⁻² = 2.382 — Icosahedral limit for quantum correlations
- Predicts suppression from Tsirelson bound at high energies

## Verification

Run the verification script to confirm all calculations:

```bash
python verification/gsm_verification.py
```

## Key Mathematical Foundations

1. **E₈ Uniqueness**: The E₈ lattice is the unique optimal sphere packing in 8D (Viazovska, 2016)
2. **H₄ Projection**: The only maximal non-crystallographic Coxeter subgroup of E₈
3. **Golden Ratio**: φ = (1+√5)/2 emerges from the icosahedral eigenvalue equation x² - x - 1 = 0
4. **Torsion Ratio**: ε = 28/248 = dim(SO(8))/dim(E₈)

## The Complete Derivation Table

| # | Constant | Value | Exp. Value | Deviation |
|---|----------|-------|------------|-----------|
| 1 | α⁻¹ | 137.0360 | 137.0360 | 0.000003% |
| 2 | sin²θ_W | 0.23122 | 0.23122 | 0.001% |
| 3 | α_s | 0.1179 | 0.1179 | 0.01% |
| 4 | m_μ/m_e | 206.768 | 206.768 | 0.00003% |
| 5 | m_τ/m_μ | 16.820 | 16.817 | 0.016% |
| 6 | m_s/m_d | 20.000 | 20.0 | 0.000% |
| 7 | m_c/m_s | 11.831 | 11.83 | 0.008% |
| 8 | m_b/m_c | 2.854 | 2.86 | 0.21% |
| 9 | m_p/m_e | 1836.15 | 1836.15 | 0.0001% |
| 10 | y_t | 0.9919 | 0.9919 | 0.001% |
| 11 | m_H/v | 0.5090 | 0.5087 | 0.064% |
| 12 | m_W/v | 0.3262 | 0.3264 | 0.063% |
| 13 | sin θ_C | 0.2250 | 0.2250 | 0.004% |
| 14 | J_CKM | 3.08×10⁻⁵ | 3.08×10⁻⁵ | 0.007% |
| 15 | V_cb | 0.0409 | 0.0410 | 0.16% |
| 16 | V_ub | 0.00363 | 0.00361 | 0.55% |
| 17 | θ₁₂ | 33.45° | 33.44° | 0.027% |
| 18 | θ₂₃ | 49.19° | 49.2° | 0.011% |
| 19 | θ₁₃ | 8.57° | 8.57° | 0.009% |
| 20 | δ_CP | 196.3° | 197° | 0.37% |
| 21 | Σm_ν | 59.2 meV | 59 meV | 0.40% |
| 22 | Ω_Λ | 0.6889 | 0.6889 | 0.002% |
| 23 | z_CMB | 1089.9 | 1089.9 | 0.002% |
| 24 | H₀ | 70.0 | 70.0 | 0.05% |
| 25 | n_s | 0.9656 | 0.9649 | 0.07% |

## Citation

```bibtex
@article{mcgirl2026gsm,
  title={The Geometric Standard Model: A Deductive Derivation of the Constants of Nature},
  author={McGirl, Timothy},
  year={2026},
  note={Version 1.0}
}
```

## Author

**Timothy McGirl**  
Independent Researcher  
Manassas, Virginia  
January 2026

## License

This work is licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

---

> *"The constants of nature are the spectral invariants of the E₈ manifold projected onto four-dimensional spacetime."*
>
> — The universe is not fine-tuned. It is **geometrically determined**.
