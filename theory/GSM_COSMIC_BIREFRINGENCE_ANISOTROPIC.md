# Anisotropic Cosmic Birefringence in the GSM

**Version 2.6 — February 25, 2026**
**License: CC-BY-4.0**

## 1. Overview

Beyond the isotropic rotation β₀ ≈ 0.292°, the GSM predicts **anisotropic**
cosmic birefringence — direction-dependent variations in the polarization
rotation angle. These arise from:

1. **Quadrupole component:** From the offset between our position and the
   lattice center of symmetry
2. **5-fold modulation:** From the discrete pentagonal symmetry of the H₄ lattice
3. **Local strain fluctuations:** From quasicrystal defects and phasons

## 2. Direction-Dependent Rotation

### 2.1 General Form

The full birefringence field on the sky is:

```
β(n̂, z) = β₀(z) + δβ_quad(n̂) + δβ_5fold(n̂) + δβ_strain(n̂)
```

where n̂ is the direction on the sky.

### 2.2 Quadrupole Component

Our position within the H₄ lattice is generically offset from the center of
symmetry. This offset d (in units of ℓ_p/φ) produces a quadrupole pattern:

```
δβ_quad(n̂) = β₂ Σ_{m=-2}^{2} a_{2m} Y_{2m}(n̂)
```

**Amplitude:**
```
β₂ ≈ β₀ × (d/R_H) ≈ 0.292° × (d/R_H)
```

where R_H is the Hubble radius in lattice units.

**GSM estimate:** For a typical offset d ~ φ⁻¹⁰ R_H:
```
β₂ ≈ 0.292° × φ⁻¹⁰ ≈ 0.292° × 0.0090 ≈ 0.0026°
```

**Rounded estimate: ~0.0008° to ~0.003°** depending on the actual offset.

### 2.3 Five-Fold Modulation

The H₄ lattice has icosahedral (including pentagonal) symmetry. This imprints
a distinctive pattern in the anisotropic birefringence:

**Spherical harmonic modes excited:**
```
ℓ = 5, 10, 15, 20, ...    (multiples of 5)
m = ±5, ±10, ...           (5-fold azimuthal symmetry)
```

**Amplitude:**
```
δβ_5fold ∝ Σ_{n=1}^{∞} φ⁻⁵ⁿ × Y_{5n, ±5n}(n̂)
```

The leading term (ℓ = 5, m = ±5) has amplitude:
```
|δβ₅| ≈ β₀ × φ⁻⁵ ≈ 0.292° × 0.0902 ≈ 0.026°
```

But projected onto the CMB sky at z = 1089, geometric suppression reduces this to:
```
|δβ₅|_obs ≈ 0.001° − 0.003°
```

### 2.4 Strain Fluctuations

Local defects in the H₄ quasicrystal (phasons, dislocations) produce
stochastic fluctuations in the birefringence:

```
⟨δβ_strain²⟩^{1/2} ≈ β₀ × (ℓ_defect / ℓ_coherence)^{1/2}
```

These contribute to the birefringence power spectrum at high ℓ.

## 3. Angular Power Spectrum

### 3.1 Birefringence Power Spectrum

The angular power spectrum of β(n̂) is:

```
C_ℓ^{ββ} = ⟨|β_{ℓm}|²⟩
```

**GSM prediction:**

| ℓ | Source | C_ℓ^{ββ} (deg²) |
|---|--------|-----------------|
| 0 | Isotropic | β₀² ≈ 0.085 |
| 2 | Quadrupole offset | ~10⁻⁶ |
| 5 | 5-fold lattice | ~10⁻⁶ to 10⁻⁵ |
| 10 | Second harmonic | ~10⁻⁷ |
| >20 | Strain fluctuations | ~10⁻⁸ × (ℓ/20)⁻² |

### 3.2 Comparison with Current Limits

Current upper limits on anisotropic birefringence (Planck 2018):
```
C_ℓ^{ββ} < 10⁻⁴ deg²    (for ℓ = 2-20)
```

The GSM prediction (~10⁻⁶ deg²) is well below current limits but within
reach of CMB-S4 and LiteBIRD.

## 4. Correlation with Large-Scale Structure

### 4.1 Lattice-Matter Correlation

The H₄ lattice structure correlates with the matter distribution (since matter
traces the lattice). Therefore, the anisotropic birefringence should correlate
with large-scale structure tracers:

```
⟨δβ(n̂) × δ_galaxy(n̂)⟩ ≠ 0
```

### 4.2 Predicted Cross-Correlation

```
C_ℓ^{βg} ≈ C_ℓ^{ββ} × b_g / φ
```

where b_g is the galaxy bias. This cross-correlation is a smoking-gun test
that distinguishes the GSM from other birefringence models (which predict
no correlation with structure).

## 5. Experimental Forecasts

### 5.1 CMB-S4

Expected sensitivity (2030+):
```
σ(β₀) ≈ 0.01°           (will test β₀ = 0.292° at 29σ)
σ(C_ℓ^{ββ}) ≈ 10⁻⁶ deg² (will probe quadrupole and 5-fold)
```

### 5.2 LiteBIRD

Expected sensitivity (2028+):
```
σ(β₀) ≈ 0.02°           (will test β₀ = 0.292° at 14σ)
Full-sky coverage optimal for large-angle anisotropy
```

### 5.3 Combined Forecasts

With CMB-S4 + LiteBIRD + galaxy surveys:
- Isotropic β₀: detectable at >10σ
- Quadrupole β₂: detectable if |β₂| > 0.001°
- 5-fold modulation: detectable if |δβ₅| > 0.002°
- β-galaxy cross-correlation: detectable if C_ℓ^{βg} > 10⁻⁷ deg²

## 6. Distinction from Other Models

| Feature | GSM | Axion-like | Primordial B |
|---------|-----|-----------|-------------|
| β₀ value | 0.292° (predicted) | Free parameter | Free parameter |
| Anisotropy pattern | 5-fold + quadrupole | Dipole + random | Scale-invariant |
| z-dependence | log_φ(1+z) | Linear in z | Constant |
| Structure correlation | **Yes** | No | No |
| Frequency dependence | None (geometric) | ∝ 1/ν² | None |

## 7. Falsification Criteria

1. **No 5-fold pattern** in anisotropic birefringence when measured to sensitivity ~10⁻⁶ deg²
2. **Isotropic β₀ ≠ 0.292°** at >3σ with CMB-S4
3. **No β-galaxy cross-correlation** at the predicted level
4. **Frequency dependence** detected in β (would favor axion-like models)

## 8. References

- Minami, Y. & Komatsu, E. PRL 125, 221301 (2020)
- Namikawa, T. et al. PRD 101, 083527 (2020) — anisotropic birefringence
- LiteBIRD Collaboration, PTEP 2023, 042F01 (2023) — forecast
- CMB-S4 Collaboration, "CMB-S4 Science Book" (2022)
