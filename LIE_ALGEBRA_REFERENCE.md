# Lie Algebra Reference: Root Systems from G₂ to E₈

**Version 2.1 — March 2026**
**License: CC-BY-4.0**

---

## Complete Exceptional Lie Algebra Table

| Group | Rank | Dimension | Roots | Coxeter # | Casimir Degrees | Role in GSM |
|-------|------|-----------|-------|-----------|-----------------|-------------|
| **G₂** | 2 | 14 | 12 | 6 | {2, 6} | Color confinement symmetry |
| **F₄** | 4 | 52 | 48 | 12 | {2, 6, 8, 12} | Maximal subgroup of E₈; 48D topology (Wits 2025) |
| **E₆** | 6 | 78 | 72 | 12 | {2, 5, 6, 8, 9, 12} | GUT candidate; trinification |
| **E₇** | 7 | 133 | 126 | 18 | {2, 6, 8, 10, 12, 14, 18} | EM branching: E₈ → E₇ × U(1) |
| **E₈** | 8 | 248 | 240 | 30 | {2, 8, 12, 14, 18, 20, 24, 30} | **Fundamental spacetime lattice** |

---

## Coxeter Group Table (Non-Crystallographic)

| Group | Rank | Order | Polytope | Eigenvalue | Role in GSM |
|-------|------|-------|----------|-----------|-------------|
| **H₂** | 2 | 10 | Pentagon/Decagon | φ | 5-fold planar symmetry |
| **H₃** | 3 | 120 | Icosahedron/Dodecahedron | φ | 3D quasicrystal symmetry |
| **H₄** | 4 | 14400 | 600-cell/120-cell | φ | **Spacetime projection target** |

---

## Root Systems: Explicit Counts

### E₈ Root System (240 roots)

The 240 root vectors of E₈ in ℝ⁸ are:

**Type 1: Permutations of (±1, ±1, 0, 0, 0, 0, 0, 0)**
- Choose 2 of 8 positions: C(8,2) = 28
- Choose signs: 2² = 4
- Total: 28 × 4 = **112 roots**

**Type 2: (±½, ±½, ±½, ±½, ±½, ±½, ±½, ±½) with even number of minus signs**
- 2⁸/2 = **128 roots** (half-integer vectors with even sign parity)

**Total: 112 + 128 = 240 roots** ✓

### Root Decompositions

```
E₈ (240) = H₄ (120) ⊕ H₄' (120)     [icosian decomposition]
E₈ (240) = F₄ (48) × 5                [pentagonal decomposition]
E₈ (240) = D₈ (112) ⊕ half-spinor (128)  [SO(16) decomposition]
```

### F₄ Root System (48 roots)

The 48 roots of F₄ in ℝ⁴:
- 24 roots of type (±1, ±1, 0, 0) — all permutations: forms D₄
- 8 roots of type (±1, 0, 0, 0) — short roots
- 16 roots of type (±½, ±½, ±½, ±½) — half-integer vectors
- **Total: 24 + 8 + 16 = 48 roots** ✓

---

## Key Branching Rules

### E₈ → E₇ × U(1) (Electromagnetic Decomposition)

```
248 → 133₀ ⊕ 1₀ ⊕ 56₊₁ ⊕ 56̄₋₁ ⊕ 1₊₂ ⊕ 1₋₂
```

| Representation | Dimension | U(1) Charge | Physical Role |
|---------------|-----------|-------------|--------------|
| 133₀ | 133 | 0 | Neutral (E₇ adjoint) |
| 1₀ | 1 | 0 | Neutral (U(1) generator) |
| 56₊₁ | 56 | +1 | Charged matter (one-loop dominant) |
| 56̄₋₁ | 56 | −1 | Anti-matter |
| 1₊₂ | 1 | +2 | Doubly-charged (two-loop significant) |
| 1₋₂ | 1 | −2 | Anti-doubly-charged |

This branching determines which Casimir operators contribute to the fine-structure constant:
- **C₈** acts on 56₊₁ (charge Q=1) → exponent 7 in α⁻¹
- **C₁₄** acts on 1₊₂ (charge Q=2) → exponent 14 in α⁻¹
- **C₁₂** acts on 133₀ (charge Q=0) → does NOT contribute

### E₈ → SU(3) × SU(2) × U(1) (Standard Model)

```
248 → (8,1)₀ ⊕ (1,3)₀ ⊕ (1,1)₀             [gauge bosons: 12]
    ⊕ (3,2)₁/₆ ⊕ (3̄,2)₋₁/₆                  [left-handed quarks]
    ⊕ (1,2)₋₁/₂ ⊕ (1,2)₁/₂                   [leptons]
    ⊕ (3,1)₂/₃ ⊕ (3̄,1)₋₂/₃                  [right-handed up]
    ⊕ (3,1)₋₁/₃ ⊕ (3̄,1)₁/₃                  [right-handed down]
    ⊕ (1,1)₁ ⊕ (1,1)₋₁                        [charged singlets]
    ⊕ ...                                       [remaining representations]
```

All Standard Model matter content emerges from the E₈ adjoint decomposition.

### E₈ → H₄ ⊕ H₄' (Icosian Decomposition)

```
240 roots → 120 (H₄) ⊕ 120 (H₄')
```

The 120 vertices of each H₄ copy form the vertices of the 600-cell, the 4D analogue of the icosahedron.

---

## Cartan Matrices

### H-type Cartan Determinant Pattern

| Group | Cartan Determinant | Value | Pattern |
|-------|-------------------|-------|---------|
| H₂ | 3 − φ | 1.382 | (n+1) − (n−1)φ, n=2 |
| H₃ | 4 − 2φ | 0.764 | (n+1) − (n−1)φ, n=3 |
| H₄ | 5 − 3φ | 0.146 | (n+1) − (n−1)φ, n=4 |

**General formula:** det(C_Hₙ) = (n+1) − (n−1)φ

This pattern is central to the CHSH derivation:
```
S = 4 − φ = 1 + det(C_H₂) = 1 + (3 − φ)
```

### E₈ Casimir Degrees and Their Physical Roles

| Degree | Casimir | Physical Role |
|--------|---------|--------------|
| 2 | C₂ | Quadratic Casimir → gauge coupling normalization |
| 8 | C₈ | Primary EM Casimir → α exponent 7 (= 8−1) |
| 12 | C₁₂ | Neutral Casimir → no EM contribution |
| 14 | C₁₄ | Secondary EM Casimir → α exponent 14 |
| 18 | C₁₈ | Neutral → PMNS mixing contributions |
| 20 | C₂₀ | Neutral → mass ratio contributions |
| 24 | C₂₄ | Neutral → cosmological contributions |
| 30 | C₃₀ | Coxeter Casimir → gravity (h = 30) |

---

## Structural Constants

| Constant | Value | Meaning |
|----------|-------|---------|
| φ = (1+√5)/2 | 1.6180339887... | Golden ratio; H₄ eigenvalue |
| ε = 28/248 | 0.1129032258... | Torsion ratio: dim(SO(8))/dim(E₈) |
| 137 = 128+8+1 | 137 | EM anchor: SO(16)₊ + rank + Euler |
| 240 | 240 | E₈ root count |
| 120 | 120 | H₄ vertex count (600-cell) |
| 14400 | 14400 | H₄ Coxeter group order |
| 696729600 | 696729600 | E₈ Weyl group order |

---

## Key Identities

```
φ² = φ + 1                          (defining property)
φ⁻¹ = φ − 1                         (reciprocal)
L_n = φⁿ + φ⁻ⁿ                      (Lucas numbers, n even)
L₃ = φ³ + φ⁻³ = 2√5                 (mass ratio root)
L₃² = 20                             (exact, algebraic)
L₆ = φ⁶ + φ⁻⁶ = 18                  (used in identities)
4 − φ = (7 − √5)/2 = 2.382...       (CHSH bound)
φ⁸⁰ ≈ 4.96 × 10¹⁶                   (hierarchy ratio)
```

---

## Visual: The Exceptional Lie Algebra Chain

```
G₂ (14) ──→ contained in ──→ F₄ (52) ──→ contained in ──→ E₈ (248)
                                                               │
                                                    E₈ → E₇ (133) × U(1)
                                                               │
                                                    E₇ → E₆ (78) × U(1)
                                                               │
                                                    E₆ → SU(3) × SU(3) × SU(3)
                                                               │
                                                    → SU(3) × SU(2) × U(1)
                                                               │
                                                    = Standard Model gauge group
```

**E₈ contains the entire Standard Model. Nothing is added — everything is projected out.**
