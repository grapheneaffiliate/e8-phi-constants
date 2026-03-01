# Complete GSM Lagrangian (All Sectors)

**Version 2.0 — February 25, 2026**
**License: CC-BY-4.0**

## 1. Overview

The Geometric Standard Model Lagrangian is a discrete variational action defined
on the H₄ quasicrystal lattice. It encompasses all sectors of physics — scalar
fields, fermions, Higgs mechanism, gauge interactions, and gravity — unified
under a single geometric principle. **Zero free parameters**: every coupling,
mass, and constant is fixed by the E₈ → H₄ projection geometry.

## 2. Total Action

```
S = Σ_v Σ_t [ ℒ_scalar + ℒ_fermion + ℒ_Higgs + ℒ_gauge + ℒ_gravity ] · V_cell · Δτ
```

where the sum runs over all vertices v of the H₄ lattice and discrete time
steps, V_cell is the Voronoi cell volume, and Δτ is the Golden Flow time step.

## 3. Scalar Sector (Golden Flow Kinetic + H₄ Laplacian)

```
ℒ_scalar = (φ^{-1/2} / 2) |∂_t ψ|²
         − (c² φ² / 2ℓ_p²) Σ_{⟨vw⟩} |ψ_v − ψ_w|²
         − (m²c⁴ / 2ℏ²) |ψ|²
```

**Terms:**
- **Kinetic:** φ^{-1/2} factor from Golden Flow time dilation τ = φ^{-1/4} t
- **Spatial gradient:** Sum over edges ⟨vw⟩ of the 600-cell (discrete gradient squared)
- **Mass:** Compton frequency from lattice geometry

The Euler-Lagrange equation recovers the GSM wave equation (see `GSM_WAVE_EQUATION.md`).

## 4. Fermion Sector

```
ℒ_fermion = ψ̄ [ i γ⁰ φ^{-1/4} ∂_t
               + i Σ_{⟨vw⟩} γ · ê_{vw} (c φ / ℓ_p) D_{vw} ] ψ
           − ψ̄ M_geom ψ
```

**Terms:**
- **Temporal derivative:** γ⁰ with φ^{-1/4} Golden Flow factor
- **Spatial hopping:** Discrete covariant derivative D_{vw} along edges with
  frame vectors ê_{vw} determined by H₄ geometry
- **Geometric mass matrix:** M_geom is diagonal in the generation basis with
  entries determined by the H₄ Casimir eigenvalues (see `GSM_FERMION_LAGRANGIAN.md`)

### 4.1 Generation Structure

Three generations arise from the SO(8) triality of the E₈ decomposition:
```
E₈ → SO(8) × SO(8)  →  3 × (8_v ⊕ 8_s ⊕ 8_c)
```

The torsion ratio ε = 28/248 = dim(SO(8))/dim(E₈) governs inter-generation
mixing.

## 5. Higgs Sector

```
ℒ_Higgs = (φ^{-1/2} / 2) |∂_t H|²
         − (c²φ² / 2ℓ_p²) Σ_{⟨vw⟩} |H_v − H_w|²
         − V_geom(|H|)
```

**Geometric potential:**
```
V_geom(|H|) = λ_geom ( |H|² − v_geom² )²
```

where:
- **VEV:** v_geom = v · φ^{-11} (from relative displacement between the two
  φ-scaled 600-cell copies in the E₈ → H₄ projection)
- **Self-coupling:** λ_geom is fixed by the H₄ Coxeter number h = 30:
  ```
  λ_geom = φ² / (4 h²) = φ² / 3600
  ```

### 5.1 Symmetry Breaking

The Higgs field H lives in the "gap" between the two φ-scaled copies of the
600-cell (primary at scale 1, dual at scale φ⁻¹). Spontaneous symmetry breaking
occurs when the inter-copy displacement exceeds the critical threshold set by
the H₄ binding energy.

**Higgs mass prediction:**
```
m_H / v = 1/2 + φ⁻⁵/10 = 0.5090
→ m_H ≈ 125.3 GeV  (experiment: 125.25 ± 0.17 GeV)
```

## 6. Gauge Sector

Gauge fields live on the edges of the H₄ lattice (link variables):

```
ℒ_gauge = − (1/4g²) Σ_{□} Tr[ F_{□} F_{□} ]
```

where:
- **F_{□}** is the lattice field strength (plaquette variable): the product of
  link variables around an elementary square
- **g** is determined by the E₈ → H₄ branching:

```
E₈ → H₄: 248 = (120 ⊕ 128)
```

The 120 adjoint roots give the gauge degrees of freedom. The Standard Model
gauge group SU(3) × SU(2) × U(1) is embedded via:

```
E₈ → E₆ × SU(3)  →  SU(3)_c × SU(2)_L × U(1)_Y
```

Gauge couplings at the Planck scale are:
```
α⁻¹(M_Pl) = 137 + φ⁻⁷ + φ⁻¹⁴ + φ⁻¹⁶ − φ⁻⁸/248
sin²θ_W = 3/13 + φ⁻¹⁶
α_s(M_Z) = 1/[2φ³(1 + φ⁻¹⁴)(1 + 8φ⁻⁵/14400)]
```

## 7. Gravity Sector (Regge Calculus)

```
S_gravity = (c³ / 16πG) Σ_h A_h ε_h
          − (Λc³ / 8πG) Σ_v V_v
          + S_matter-gravity coupling
```

**Terms:**
- **A_h:** Area of hinge (2-simplex) h in the triangulated H₄ lattice
- **ε_h:** Deficit angle at hinge h (discrete curvature)
- **V_v:** 4-volume of Voronoi cell at vertex v
- **Λ:** Cosmological constant (derived, not free):
  ```
  Ω_Λ = φ⁻¹ + φ⁻⁶ + φ⁻⁹ − φ⁻¹³ + φ⁻²⁸ + ε·φ⁻⁷ ≈ 0.6889
  ```

See `GSM_GRAVITY_REGGE.md` for the full Regge calculus formulation.

## 8. Matter-Gravity Coupling

The fermion and scalar fields couple to gravity through the lattice vierbein:

```
S_coupling = Σ_v √(det g_v) · (ℒ_scalar + ℒ_fermion + ℒ_Higgs + ℒ_gauge)
```

where g_v is the discrete metric at vertex v, determined by the edge lengths
of the simplices meeting at v.

## 9. Equations of Motion

Varying the total action with respect to each field:

| Field | Equation |
|-------|----------|
| ψ (scalar) | GSM wave equation (discrete Klein-Gordon) |
| ψ (fermion) | Discrete Dirac equation on H₄ |
| H (Higgs) | Discrete Klein-Gordon + geometric potential |
| A_{vw} (gauge) | Discrete Yang-Mills on H₄ lattice |
| ℓ_{vw} (edge lengths) | Regge-Einstein equations |

## 10. Symmetries and Conservation Laws

**Exact discrete symmetries:**
- H₄ reflection group (order 14400) → spatial rotations
- Golden Flow time translation → energy conservation
- Gauge invariance on links → charge conservation
- CPT as geometric involution

**Approximate continuous symmetries (emergent at low energy):**
- Lorentz invariance (from continuum limit of H₄ lattice)
- Diffeomorphism invariance (from continuum limit of Regge calculus)

## 11. Parameter Count

| Standard Model | GSM |
|---------------|-----|
| 25+ free parameters | **0 free parameters** |
| Gauge couplings fitted | Derived from E₈ Casimirs |
| Yukawa couplings fitted | Derived from H₄ representations |
| Higgs potential fitted | Derived from inter-copy geometry |
| Λ fitted | Derived from lattice growth rate |

Every term in the Lagrangian is determined by the single geometric axiom:
**spacetime is the E₈ → H₄ quasicrystal.**
