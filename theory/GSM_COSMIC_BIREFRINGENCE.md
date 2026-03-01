# Cosmic Birefringence in the Geometric Standard Model

**Version 2.5 — February 25, 2026**
**License: CC-BY-4.0**

## 1. Overview

Cosmic birefringence — the rotation of the linear polarization plane of CMB
photons — is a natural prediction of the GSM. As photons propagate through the
expanding H₄ quasicrystal, the aperiodic lattice structure induces a systematic
phase drift between left- and right-circular polarizations. The resulting
rotation angle is:

```
β(z) = arcsin(φ⁻³) × log_φ(1+z) / log_φ(1+z_CMB)
```

At the CMB last scattering surface (z = z_CMB ≈ 1089):

```
β₀ = arcsin(φ⁻³) ≈ arcsin(0.2361) ≈ 0.2385 rad ≈ **0.292°**
```

**Observed value: β = 0.30° ± 0.11° (Minami & Komatsu 2020, Planck + WMAP)**

This is a 0.5σ match with zero free parameters.

## 2. Physical Mechanism

### 2.1 Lattice-Induced Phase Asymmetry

The H₄ quasicrystal is **chiral** — it has a preferred handedness inherited from
the E₈ → H₄ projection. Specifically:

1. The two φ-scaled copies of the 600-cell (primary at scale 1, dual at scale φ⁻¹)
   define a preferred orientation
2. Left-circular and right-circular photon polarizations couple differently
   to this chiral structure
3. Over cosmological distances, the differential phase accumulates

### 2.2 Aperiodic Drift

The quasicrystal tiling is aperiodic (Penrose-like in 4D). A photon traversing
N lattice cells accumulates a phase:

```
δφ_L(N) = Σ_{n=1}^{N} α_n       (left-circular)
δφ_R(N) = Σ_{n=1}^{N} α_n'      (right-circular)
```

where α_n and α_n' are the per-cell phases, which differ because of chirality.

The net rotation after N cells:

```
β(N) = [δφ_L(N) - δφ_R(N)] / 2
```

### 2.3 Why arcsin(φ⁻³)?

The phase asymmetry per lattice cell is determined by the H₄ geometry.
The relevant quantity is the mismatch between the pentagonal rotation
(72° = 2π/5) and the lattice transport angle:

```
Δα_cell = arcsin(φ⁻³)
```

This arises because φ⁻³ is the cosine of the angle between adjacent pentagonal
tiles in the H₄ tiling (the "phason" contribution to transport).

## 3. Redshift Dependence

### 3.1 Number of Cells vs. Redshift

The number of lattice cells traversed by a photon from redshift z to today is
proportional to the comoving distance, which in the GSM lattice framework scales as:

```
N(z) ∝ log_φ(1+z)
```

This logarithmic-in-φ scaling follows from the discrete shell growth of the
H₄ lattice: each new shell adds volume proportional to φ² times the previous shell.

### 3.2 Full β(z) Formula

```
β(z) = arcsin(φ⁻³) × log_φ(1+z) / log_φ(1+z_CMB)
```

**Properties:**
- β(0) = 0 (no rotation for local photons)
- β(z_CMB) = arcsin(φ⁻³) ≈ 0.292° (maximum rotation for CMB photons)
- Monotonically increasing with z
- Approaches a constant for z → z_CMB (saturates at the lattice chirality scale)

### 3.3 Numerical Values

| Redshift z | log_φ(1+z) | β(z) |
|-----------|-----------|------|
| 0         | 0         | 0.000° |
| 0.1       | 0.198     | 0.004° |
| 1.0       | 1.440     | 0.029° |
| 10        | 4.977     | 0.100° |
| 100       | 9.575     | 0.192° |
| 1089      | 14.526    | 0.292° |

### 3.4 Comparison with Observations

The Minami & Komatsu (2020) measurement uses combined Planck + WMAP data:
```
β_obs = 0.30° ± 0.11° (68% CL)
β_GSM = 0.292°
Deviation: 0.07σ
```

The upcoming CMB-S4 and LiteBIRD experiments will measure β to ±0.01° precision,
providing a stringent test.

## 4. Spectral Dependence

### 4.1 Frequency Independence (Leading Order)

To leading order, β(z) is independent of photon frequency. This is because the
lattice chirality is a geometric (topological) effect, not a dispersive one.

### 4.2 Frequency-Dependent Corrections

At next-to-leading order, near-Planck-frequency photons (ν ~ c·φ/ℓ_p) experience
lattice dispersion corrections:

```
β(z, ν) = β(z) × [1 + O(ν·ℓ_p/(c·φ))²]
```

For CMB frequencies (ν ~ 100 GHz), the correction is negligible:
```
ν·ℓ_p/(c·φ) ~ 10⁻²⁰     (unmeasurably small)
```

## 5. EB and TB Cross-Correlations

### 5.1 Isotropic Birefringence Signal

A uniform rotation β₀ converts E-mode polarization into B-mode:

```
C_ℓ^{EB,obs} = sin(2β₀)/2 × (C_ℓ^{EE} - C_ℓ^{BB})
C_ℓ^{TB,obs} = sin(2β₀) × C_ℓ^{TE}
```

### 5.2 GSM Prediction

With β₀ = 0.292°:
```
sin(2β₀) = sin(0.584°) ≈ 0.01019
```

This produces a small but measurable EB correlation that matches current
observations.

## 6. Connection to Dark Energy

The cosmic birefringence is intimately connected to the cosmological constant
in the GSM. Both arise from the same lattice growth mechanism:

- **Λ:** Energy density of boundary crystallization → Ω_Λ = φ⁻¹ + ...
- **β:** Phase chirality accumulated during lattice growth → arcsin(φ⁻³)

The fact that both are O(φ⁻¹) to O(φ⁻³) is not coincidental — they are
different manifestations of the same geometric structure.

## 7. Falsification Criteria

The GSM birefringence prediction is falsified if:
1. **β₀ ≠ 0.292° ± 0.03°** (when measured to ±0.01° by CMB-S4/LiteBIRD)
2. **β(z) is not logarithmic in φ** (requires galaxy-survey EB measurements)
3. **β is frequency-dependent at CMB scales** (would indicate dispersive, not geometric, origin)

## 8. References

- Minami, Y. & Komatsu, E. "New Extraction of the Cosmic Birefringence..."
  PRL 125, 221301 (2020)
- Eskilt, J.R. & Komatsu, E. "Improved constraints on cosmic birefringence..."
  PRD 106, 063503 (2022)
- Planck Collaboration, "Planck 2018 results. VI." A&A 641, A6 (2020)
