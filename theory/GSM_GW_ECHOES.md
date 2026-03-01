# Gravitational Wave Echoes in GSM

**Version 2.3 — February 25, 2026**
**License: CC-BY-4.0**

## 1. Overview

The Geometric Standard Model predicts distinctive gravitational wave (GW) echo
signatures following binary black hole mergers. Unlike generic "quantum gravity
echo" models with arbitrary parameters, the GSM echo template has **zero free
parameters** — all delays, amplitudes, and polarization rotations are fixed by
the golden ratio φ.

## 2. Physical Origin

### 2.1 Post-Merger Lattice Relaxation

After a binary black hole merger, the remnant's H₄ quasicrystal core undergoes
discrete relaxation through nested φ-scaled shells. Each shell boundary acts as
a partial reflector for gravitational perturbations.

### 2.2 Echo Mechanism

1. The initial ringdown (quasi-normal mode) propagates outward
2. At each φ-scaled shell boundary (R_k = φ^k × 2GM/c²), partial reflection occurs
3. The reflected wave bounces between boundaries, producing echoes
4. Each echo is delayed, damped, and polarization-rotated by amounts
   determined by the H₄ geometry

## 3. Echo Template

### 3.1 Master Formula

```
h(t) = h_IMR(t) + Σ_{k=1}^{K} A_k · R(θ_k) · h_echo(t − t_merger − Δt_k)
```

where:
- **h_IMR(t):** Standard inspiral-merger-ringdown waveform
- **A_k:** Amplitude of k-th echo
- **R(θ_k):** Polarization rotation matrix
- **h_echo:** Echo waveform (time-reversed and filtered ringdown)
- **Δt_k:** Time delay of k-th echo

### 3.2 Time Delays

```
Δt_k = φ^{k+1} × (2GM/c³)     [k = 1, 2, 3, ...]
```

For a 30 M☉ remnant:
```
2GM/c³ = 2 × 6.674×10⁻¹¹ × 30 × 1.989×10³⁰ / (3×10⁸)³
       ≈ 2.95×10⁻⁴ s ≈ 0.295 ms

Δt₁ = φ² × 0.295 ms ≈ 0.772 ms
Δt₂ = φ³ × 0.295 ms ≈ 1.249 ms
Δt₃ = φ⁴ × 0.295 ms ≈ 2.021 ms
Δt₄ = φ⁵ × 0.295 ms ≈ 3.270 ms
```

**Key property:** Ratios of consecutive delays are exactly φ:
```
Δt_{k+1} / Δt_k = φ    (for all k)
```

### 3.3 Damping (Amplitude Decay)

```
A_k = φ^{-k}     [k = 1, 2, 3, ...]
```

| Echo k | Amplitude A_k | Relative to ringdown |
|--------|--------------|---------------------|
| 1      | φ⁻¹ ≈ 0.618 | 61.8% |
| 2      | φ⁻² ≈ 0.382 | 38.2% |
| 3      | φ⁻³ ≈ 0.236 | 23.6% |
| 4      | φ⁻⁴ ≈ 0.146 | 14.6% |
| 5      | φ⁻⁵ ≈ 0.090 | 9.0%  |

**Key property:** Each echo retains a fraction 1/φ of the previous amplitude.
The total energy in echoes converges (geometric series sum = φ).

### 3.4 Polarization Rotation

```
θ_k = k × 72° + 36°/φ^k
```

This rotation arises from the 5-fold (pentagonal) symmetry of the H₄ lattice:
- **Base rotation:** 72° = 360°/5 per echo (one step around the pentagon)
- **Drift correction:** 36°/φ^k accounts for the aperiodic lattice mismatch

| Echo k | θ_k | Interpretation |
|--------|-----|---------------|
| 1      | 72° + 22.2° = 94.2° | Nearly quarter-turn |
| 2      | 144° + 13.7° = 157.7° | Nearly π |
| 3      | 216° + 8.5° = 224.5° | Third pentagon vertex |
| 4      | 288° + 5.2° = 293.2° | Fourth pentagon vertex |
| 5      | 360° + 3.2° = 363.2° | Full cycle + drift |

### 3.5 Polarization Rotation Matrix

For each echo, the + and × polarizations mix according to:

```
R(θ_k) = | cos(2θ_k)  -sin(2θ_k) |
          | sin(2θ_k)   cos(2θ_k) |
```

Note the factor of 2 because gravitational waves are spin-2 (tensor perturbations
rotate at twice the geometric angle).

## 4. Observational Signatures

### 4.1 Unique GSM Fingerprint

The combination of φ-commensurate delays, φ-damping, and 72° polarization
flips is unique to the GSM. No other echo model predicts this specific pattern.

### 4.2 Detection Strategy

1. **Matched filtering:** Inject the GSM echo template into LIGO/Virgo data
2. **Time-frequency analysis:** Look for power at φ-spaced intervals post-merger
3. **Polarization tracking:** Monitor the polarization angle evolution
4. **Stacking:** Coherently add echoes from multiple events using φ-scaling

### 4.3 Signal-to-Noise Estimates

For a GW150914-like event (M ≈ 62 M☉, d ≈ 410 Mpc):
- First echo SNR: ~0.6 × ringdown SNR ≈ 5
- Stacking N events: SNR grows as √N
- With O4 sensitivity (~50 BBH/year): detectable after ~10 events

### 4.4 Current Status

Marginal evidence in LIGO data:
- GW190521: Bayes factor ~9 for post-merger echoes (Abedi et al. 2025)
- Not yet significant (requires Bayes factor > 100 for detection claim)
- O4/O5 data will be decisive

## 5. Falsification Criteria

The GSM echo prediction is falsified if:
1. Echoes are detected with delays **not** in φ ratios (|Δt_{k+1}/Δt_k − φ| > 0.05)
2. Amplitude decay is **not** φ⁻ᵏ (|A_{k+1}/A_k − φ⁻¹| > 0.1)
3. Polarization rotation is **not** ~72° per echo (|Δθ − 72°| > 10°)
4. No echoes are detected after O5 with sufficient sensitivity (SNR > 20 for ringdown)

## 6. Comparison with Other Models

| Property | GSM | Abedi et al. | Quantum BH (Cardoso) |
|----------|-----|-------------|---------------------|
| Free parameters | **0** | 2 (Δt, γ) | 1 (reflectivity) |
| Delay spacing | φ^{k+1}×2M | Uniform Δt | Uniform Δt |
| Damping | φ⁻ᵏ | e^{-γk} | Constant |
| Polarization | 72° rotation | None | None |
| Testable? | **Yes** | Partially | Partially |

## 7. Template for LIGO Injection

The complete waveform for LIGO analysis (see `simulation/gsm_ligo_template_generator.py`):

```python
def gsm_echo_template(t, t_merger, M_remnant, h_ringdown, K_max=10):
    phi = (1 + 5**0.5) / 2
    t_M = 2 * G * M_remnant / c**3
    h_total = h_ringdown.copy()
    for k in range(1, K_max + 1):
        dt_k = phi**(k+1) * t_M
        A_k = phi**(-k)
        theta_k = k * 72 + 36 / phi**k  # degrees
        h_echo = A_k * rotate_polarization(h_ringdown, theta_k)
        h_total += time_shift(h_echo, dt_k)
    return h_total
```

## 8. References

- Regge, T. "General Relativity without Coordinates" (1961)
- Abedi, J. et al. "Echoes from the Abyss" PRD 96, 082004 (2017)
- Cardoso, V. et al. "Is the GW ringdown a probe of the event horizon?" PRL 116, 171101 (2016)
- LIGO/Virgo Collaboration, GW190521 (2020)
