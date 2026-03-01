# GSM Gravity: Regge Calculus on the H₄ Quasicrystal

**Version 2.0 — February 25, 2026**
**License: CC-BY-4.0**

## 1. Overview

Gravity in the Geometric Standard Model is formulated via Regge calculus on the
H₄ quasicrystal lattice. This is a discrete version of General Relativity where:
- **Edge lengths** replace the metric tensor
- **Deficit angles** replace the Riemann curvature tensor
- **Hinge areas** replace the volume form

The resulting theory is background-independent, UV-finite (regulated by the
lattice), and reduces to Einstein's equations in the continuum limit.

## 2. Regge Calculus: Review

### 2.1 Triangulation

The H₄ quasicrystal provides a natural simplicial decomposition of 4D spacetime.
The 600-cell itself is composed of 600 regular tetrahedra, which serve as the
fundamental 4-simplices.

**Simplicial complex:**
- **0-simplices (vertices):** 120 lattice sites
- **1-simplices (edges):** 720 edges with lengths ℓ_{vw}
- **2-simplices (triangles/hinges):** 1200 triangular faces
- **3-simplices (tetrahedra):** 600 tetrahedral cells
- **4-simplices:** Built from pentachoral (5-cell) decomposition

### 2.2 The Metric

In Regge calculus, the metric is entirely encoded in the edge lengths {ℓ_{vw}}.
The flat-space value is:

```
ℓ_{vw}^{(0)} = ℓ_p / φ     (for nearest neighbors)
```

Gravitational curvature corresponds to deviations from this flat value.

## 3. Deficit Angles (Discrete Curvature)

### 3.1 Definition

At each triangular hinge h (2-simplex), the deficit angle ε_h measures the
failure of the surrounding 4-simplices to close flat:

```
ε_h = 2π − Σ_{σ ⊃ h} θ_h(σ)
```

where θ_h(σ) is the dihedral angle at hinge h in 4-simplex σ.

### 3.2 Flat Space

In the undeformed H₄ lattice, the deficit angles are:

```
ε_h^{(0)} = 2π − n_h × arccos(-1/4)
```

where n_h is the number of 4-simplices meeting at hinge h. For the regular
600-cell, n_h = 5 and arccos(-1/4) ≈ 104.48°, giving:

```
ε_h^{(0)} = 2π − 5 × 1.8235 = 2π − 9.1174 ≈ -2.834 rad
```

This residual deficit angle encodes the intrinsic curvature of the H₄
polytope — it is the discrete analogue of the cosmological constant.

### 3.3 Curvature from Edge Deformation

Small perturbations δℓ_{vw} of the edge lengths produce deficit angle changes:

```
δε_h = Σ_{vw ∈ ∂h} (∂ε_h / ∂ℓ_{vw}) δℓ_{vw}
```

This is the discrete analogue of the Riemann curvature perturbation.

## 4. The Regge Action

### 4.1 Einstein-Hilbert on the Lattice

```
S_Regge = (c³ / 16πG) Σ_h A_h · ε_h
```

where:
- **A_h:** Area of hinge h
- **ε_h:** Deficit angle at hinge h

### 4.2 Cosmological Term

```
S_Λ = −(Λc³ / 8πG) Σ_v V_v
```

where V_v is the 4-volume of the Voronoi cell at vertex v.

### 4.3 Full Gravitational Action

```
S_gravity = (c³ / 16πG) Σ_h A_h ε_h  −  (Λc³ / 8πG) Σ_v V_v  +  S_matter
```

### 4.4 GSM-Specific Features

In the GSM, Newton's constant is not free but derived:

```
G = (ℏc / v²) × φ^{-160+2ε}
```

where v = 246.22 GeV is the electroweak VEV and ε = 28/248.

The cosmological constant density:
```
Ω_Λ = φ⁻¹ + φ⁻⁶ + φ⁻⁹ − φ⁻¹³ + φ⁻²⁸ + ε·φ⁻⁷ ≈ 0.6889
```

## 5. Area Law (Bekenstein-Hawking from Regge)

### 5.1 Black Hole as Maximal Packing

When all edge lengths reach the minimum ℓ_min = ℓ_p/φ, the lattice is maximally
packed. The deficit angles saturate at their maximum values, and the enclosed
region forms a discrete black hole.

### 5.2 Horizon Area Quantization

The horizon area is quantized in units of the minimal hinge area:

```
A_h^{min} = (√3/4)(ℓ_p/φ)²     (equilateral triangle with edge ℓ_p/φ)
```

The total horizon area:
```
A = N_h × A_h^{min}
```

where N_h is the number of hinges on the horizon surface.

### 5.3 Entropy

Each hinge carries one bit of geometric information:
```
S_BH = k_B · N_h = k_B · A / A_h^{min}
```

Substituting A_h^{min} = (√3/4)(ℓ_p/φ)²:
```
S_BH = k_B · 4A / (√3 · ℓ_p²/φ²)
     = k_B · 4φ² A / (√3 · ℓ_p²)
```

This reproduces the Bekenstein-Hawking formula S = A·c³/(4ℏG) up to a
geometric factor of order unity that depends on the exact triangulation.

## 6. Linearized Gravity and Gravitons

### 6.1 Perturbation Theory

Around flat H₄ lattice: ℓ_{vw} = ℓ_0 + h_{vw}

The quadratic action for perturbations h_{vw} yields a discrete
spin-2 propagator — the lattice graviton.

### 6.2 Graviton Spectrum

The graviton dispersion relation on the H₄ lattice:
```
ω² = c² (φ/ℓ_p)² |λ_k^{(2)}|
```

where λ_k^{(2)} are eigenvalues of the tensor Laplacian (spin-2 sector of
the graph Laplacian on edge-valued fields).

### 6.3 UV Finiteness

The lattice provides a hard cutoff at momentum:
```
k_max = π φ / ℓ_p
```

All graviton loop integrals are manifestly finite. The non-renormalizability
problem of continuum quantum gravity does not arise.

## 7. Gravitational Waves on the Lattice

Gravitational waves are coherent excitations of edge-length perturbations:

```
h_{vw}(t) = h₀ e^{i(ω t − k·r_{vw})}
```

In the continuum limit, these reduce to the standard +/× polarizations of
linearized GR. On the lattice, additional discrete polarizations exist at
frequencies near k_max, providing a potential observational signature
(see `GSM_GW_ECHOES.md`).

## 8. Connection to Standard GR

| Regge (discrete) | Einstein (continuum) |
|------------------|---------------------|
| Edge lengths ℓ_{vw} | Metric tensor g_μν |
| Deficit angle ε_h | Riemann tensor R_μνρσ |
| Hinge area A_h | Volume form √g d⁴x |
| Regge action | Einstein-Hilbert action |
| Schläfli identity | Bianchi identity |
| Vertex equation | Einstein equation |

The continuum limit (ℓ_{vw} → 0 with fixed macroscopic curvature) recovers
Einstein's equations exactly (Regge 1961, proved by Cheeger-Müller-Schrader).
