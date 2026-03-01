# GSM Wave Equation on the H₄ 600-Cell

**Version 1.1 — February 24, 2026**
**License: CC-BY-4.0**

## 1. Overview

The fundamental dynamical equation of the Geometric Standard Model is a discrete
Klein-Gordon equation defined on the 120-vertex graph of the H₄ 600-cell, with
time evolution governed by the Golden Flow operator. This document provides the
complete derivation, operator definitions, and continuum limit.

## 2. Setup: The 600-Cell Graph

The 600-cell is the 4-dimensional regular polytope with:
- **120 vertices** (the roots of the H₄ reflection group)
- **720 edges** (each vertex has exactly **12 neighbors**)
- **1200 triangular faces**, **600 tetrahedral cells**

The vertices, after E₈ → H₄ projection, sit at positions determined by the
Golden Ratio. The minimal edge length is:

```
ℓ_min = ℓ_p / φ
```

where ℓ_p is the Planck length and φ = (1+√5)/2.

## 3. The Graph Laplacian

Let ψ(v, t) be the scalar field at vertex v at time t. The discrete graph
Laplacian on the 600-cell is:

```
Δ_{H₄} ψ(v) = Σ_{w ~ v} [ψ(w) - ψ(v)]
```

where the sum runs over the 12 nearest neighbors w of vertex v. This operator:
- Is symmetric: ⟨f, Δg⟩ = ⟨Δf, g⟩
- Has non-positive spectrum: eigenvalues λ_k ≤ 0
- Respects the full H₄ symmetry group (order 14400)

### 3.1 Eigenvalue Spectrum

The graph Laplacian on the 600-cell has eigenvalues determined by the irreducible
representations of H₄. The spectrum is:

| Multiplicity | Eigenvalue λ | Representation |
|-------------|-------------|----------------|
| 1           | 0           | Trivial        |
| 4           | -φ²·4       | Standard (4D)  |
| 5           | -12         | 5D irrep       |
| 4           | -φ⁻²·4      | Dual standard  |
| ...         | ...         | Higher irreps  |

The spectral gap is Δλ = 4φ², which sets the fundamental frequency scale.

## 4. Golden Flow Time Reparameterization

### 4.1 Definition

The Golden Flow operator defines the natural time coordinate:

```
τ(t) = φ^{-1/4} · t
```

This is the spectral flow along the dominant φ-eigenvector of the H₄ Coxeter
element. The exponent -1/4 normalizes the 4-dimensional volume form.

**Note on β:** In the general form 𝒯(t) = φ^{-1/4} t + β, we set β = 0 for
the wave equation (β encodes initial phase offset and is absorbed into boundary
conditions).

### 4.2 Properties

- **Unitarity:** 𝒯†𝒯 = I (information preserving)
- **Time dilation factor:** dτ/dt = φ^{-1/4} ≈ 0.8090
- **Inverse:** t(τ) = φ^{1/4} · τ

## 5. The Wave Equation

### 5.1 Natural Form (Golden-Flow Time τ)

```
∂²ψ/∂τ² = c² (φ / ℓ_p)² Δ_{H₄} ψ  −  (mc² / ℏ)² ψ
```

This is a discrete Klein-Gordon equation with:
- **Spatial coupling:** c²(φ/ℓ_p)² sets the lattice speed of propagation
- **Mass term:** (mc²/ℏ)² gives the Compton frequency squared
- **Massless case (m = 0):** reduces to the discrete wave equation

### 5.2 Cosmic Time Form

Converting τ → t via the chain rule (∂/∂τ = φ^{1/4} ∂/∂t):

```
φ^{-1/2} ∂²ψ/∂t² = c² (φ / ℓ_p)² Δ_{H₄} ψ  −  (mc² / ℏ)² ψ
```

The factor φ^{-1/2} = (∂τ/∂t)² is the Golden Flow time-dilation.

### 5.3 Component Form

Writing out explicitly for vertex v with neighbors w₁, w₂, ..., w₁₂:

```
φ^{-1/2} ψ̈(v, t) = c²(φ/ℓ_p)² [ψ(w₁) + ψ(w₂) + ... + ψ(w₁₂) - 12·ψ(v)]
                     − (mc²/ℏ)² ψ(v)
```

This is a system of 120 coupled ODEs — one per vertex.

## 6. Dispersion Relation

For a mode with eigenvalue λ_k of the graph Laplacian:

```
φ^{-1/2} ω² = c²(φ/ℓ_p)² |λ_k|  +  (mc²/ℏ)²
```

Solving for ω:

```
ω² = φ^{1/2} [ c²(φ/ℓ_p)² |λ_k|  +  (mc²/ℏ)² ]
```

The group velocity for mode k is:

```
v_g = ∂ω/∂k → c  (in the continuum limit)
```

## 7. Continuum Limit

When the wavelength λ ≫ ℓ_p/φ (far above the lattice scale), the graph
Laplacian converges to the continuum Laplacian:

```
(φ/ℓ_p)² Δ_{H₄} ψ  →  ∇² ψ
```

and the full equation becomes:

```
φ^{-1/2} ∂²ψ/∂t²  =  c² ∇² ψ  −  (mc²/ℏ)² ψ
```

Rescaling t → τ = φ^{-1/4} t recovers the standard Klein-Gordon equation:

```
∂²ψ/∂τ²  =  c² ∇² ψ  −  (mc²/ℏ)² ψ
```

This proves the GSM wave equation reduces to standard relativistic QFT in the
low-energy (long-wavelength) limit.

## 8. Conserved Quantities

The H₄ symmetry of the wave equation guarantees conserved currents:

**Energy (time-translation invariance):**
```
E = Σ_v [ (φ^{-1/2}/2)|∂_t ψ(v)|² + (c²φ²/2ℓ_p²) Σ_{w~v} |ψ(v)-ψ(w)|²
        + (m²c⁴/2ℏ²)|ψ(v)|² ]
```

**H₄ Angular Momentum (rotation invariance):**
The 6 generators of SO(4) restricted to H₄ give conserved angular momentum
components, quantized in units related to the 5-fold symmetry.

**Discrete Charge (pentagonal current):**
```
Q = Σ_v Im[ψ*(v) ∂_t ψ(v)]
```

## 9. Physical Interpretation

| Feature | Meaning |
|---------|---------|
| 120 vertices | Fundamental degrees of freedom at Planck scale |
| 12 neighbors | Icosahedral coordination (maximal in 4D) |
| φ^{-1/2} prefactor | Golden Flow time dilation |
| Mass term | Compton frequency from lattice geometry |
| Continuum limit | Standard Klein-Gordon recovered |

The wave equation describes how excitations (particles) propagate through the
discrete spacetime lattice. Different particle species correspond to different
representations of H₄ acting on the 600-cell.

## 10. References

- Coxeter, H.S.M. "Regular Polytopes" (1973) — 600-cell geometry
- Moody, R.V. & Patera, J. "Quasicrystals and Icosians" — H₄ root systems
- Viazovska, M. "The sphere packing problem in dimension 8" (2017) — E₈ uniqueness
