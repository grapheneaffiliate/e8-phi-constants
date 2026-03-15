# GSM φ-Echo Improved Search Results — Multi-Event

**Date**: March 14, 2026
**Analysis version**: 3.0 (template-ratio φ-comb + injection-recovery validation)
**Data**: Real LIGO strain data from GWOSC (4 BBH events)

## Improvements Over v1.0/v2.0
1. **Ringdown subtraction**: Best-fit Kerr QNM removed before echo search
2. **Template-ratio φ-comb** (v3.0): Full matched-filter using echo-train templates at
   φ-ratio delays vs 1000 random geometric delay ratios. Proper SNR normalization
   (peak / noise_std). Replaces v2.0's autocorrelation-based φ-comb which had
   SNR ∝ (signal_SNR)²/√N — far too weak for detection.
3. **H1×L1 cross-correlation**: Real echoes must appear in both detectors
4. **Multi-event stacking**: Combined z-scores across 4 independent BBH events
5. **Injection-recovery validation**: Pipeline proven to detect φ-echoes when present
   and reject non-φ-ratio echoes (see companion report)

## Events Analyzed

| Event | M_remnant (M☉) | χ_remnant | Distance (Mpc) | f_QNM (Hz) | t_M (ms) |
|-------|---------------|-----------|----------------|-----------|---------|
| GW150914 | 62.0 | 0.67 | 410 | 142.8 | 0.611 |
| LVT151012 | 35.0 | 0.66 | 1000 | 254.4 | 0.345 |
| GW151226 | 20.8 | 0.74 | 440 | 446.3 | 0.205 |
| GW170104 | 48.7 | 0.64 | 880 | 177.3 | 0.480 |

All data: GWOSC LOSC v1, 32 seconds at 4096 Hz, H1 + L1.

## Per-Event Results

### Test 1: Matched Filter on Ringdown-Subtracted Residual

| Event | H1 SNR | H1 p-value | H1 rank | L1 SNR | L1 p-value |
|-------|--------|-----------|---------|--------|-----------|
| GW150914 | **8.30** | 0.0000 | 100.0% | **6.73** | 0.0000 |
| LVT151012 | 4.76 | 0.2800 | 72.0% | 3.71 | 0.9450 |
| GW151226 | 4.13 | 0.8250 | 17.5% | 4.37 | 0.5500 |
| GW170104 | 4.63 | 0.1900 | 81.0% | 4.73 | 0.3400 |

**Note**: GW150914's high residual SNR reflects the GW signal tail (merger
transient not fully removed by single-mode ringdown fit). The other 3 events
show SNR consistent with noise (p > 0.05).

### Test 2: Template-Ratio φ-Comb (Primary Discriminant)

The φ-comb builds the full echo-train template at φ-ratio delays, matched-filters
the ringdown-subtracted residual, and measures peak SNR (= peak / noise_std).
Compared to 1000 templates with random geometric delay ratios (r ∈ [1.2, 2.5]).

| Event | φ-comb SNR | Control mean | z-score | p-value |
|-------|-----------|-------------|---------|---------|
| GW150914 | 8.21 | 7.79 | **+0.70** | 0.183 |
| LVT151012 | 4.60 | 4.74 | -0.35 | 0.706 |
| GW151226 | 4.27 | 4.38 | -0.40 | 0.658 |
| GW170104 | 4.59 | 4.72 | -0.39 | 0.705 |

**No event shows significant φ-ratio structure.** GW150914 shows a mild positive
fluctuation (z=0.70) but not significant (p=0.183). The other 3 events are clearly null.

### Test 3: H1×L1 Cross-Correlation

| Event | φ-delay |xcorr| | Random |xcorr| | Excess |
|-------|----------------|---------------|--------|
| GW150914 | 0.0883 | 0.0553 | +59.8% |
| LVT151012 | 0.0321 | 0.0328 | -2.3% |
| GW151226 | 0.0688 | 0.0627 | +9.8% |
| GW170104 | 0.0497 | 0.0409 | +21.5% |

GW150914's +59.8% excess is from the shared GW merger transient, not echoes.
Other events show cross-correlation consistent with noise.

## Stacked Analysis (4 Events Combined)

| Metric | Value |
|--------|-------|
| Individual φ-comb z-scores | [+0.70, -0.35, -0.40, -0.39] |
| Combined z-score (Fisher) | **-0.22** |
| Combined p-value | **0.587** |

The stacked φ-comb across all 4 events is consistent with noise (p = 0.587).

## Pipeline Validation: Injection-Recovery

The pipeline was validated with synthetic echo injection into real LIGO noise:

| Test | φ-comb z | p-value | Result |
|------|---------|---------|--------|
| Pure noise (no injection) | -0.52 | 0.732 | Correctly null |
| Inject **φ-ratio** echoes | **+2.23** | **0.000** | **Detected** |
| Inject ratio=1.3 echoes | +1.07 | 0.147 | Correctly null |
| Inject ratio=1.5 echoes | +0.99 | 0.077 | Correctly null |
| Inject ratio=1.8 echoes | +0.48 | 0.283 | Correctly null |
| Inject ratio=2.0 echoes | +0.11 | 0.376 | Correctly null |
| Inject ratio=2.3 echoes | -0.62 | 0.699 | Correctly null |

The φ-comb is both **sensitive** (detects φ-ratio echoes, z=2.23) and
**specific** (rejects all non-φ delay ratios). The null results on real
data are genuine, not pipeline artifacts.

## Verdict: **NULL RESULT**

No φ-echo signal detected in any of 4 BBH events at O1/O2 sensitivity.
The template-ratio φ-comb — the cleanest test for φ-ratio structure — shows
no preference for φ-delays over random delay ratios in any individual
event or in the 4-event stack.

### Why This Is Expected

| Factor | Impact |
|--------|--------|
| GW150914 ringdown SNR | ~7 (out of total SNR ~24) |
| First echo amplitude | φ⁻¹ × ringdown = 62% → echo SNR ~4 |
| Third echo amplitude | φ⁻³ × ringdown = 24% → echo SNR ~1.7 |
| O1 noise floor at 150 Hz | ~3×10⁻²³ /√Hz |
| Expected echo SNR at O1 | Near or below detection threshold |

### What Would Change the Result

| Improvement | Expected gain | When |
|-------------|--------------|------|
| **GW250114** (SNR ~80) | ~3× higher echo SNR | May 2026 (O4b public release) |
| **O5 sensitivity** | ~5× noise reduction | ~2027 |
| **20+ event stack** | √20 ≈ 4.5× from stacking | With GWTC-3 full data |
| **Multi-mode ringdown subtraction** | Cleaner residual | Requires LALSuite |

## Pipeline Status

The analysis pipeline is complete and validated:
- `gsm_echo_improved_search.py` — multi-event search with 3 independent tests
- `gsm_echo_injection_test.py` — injection-recovery pipeline validation
- Template-ratio φ-comb, ringdown subtraction, H1×L1 cross-correlation, time-slide significance
- Ready to run on any new GWOSC event by adding GPS time and remnant parameters

## Plots
![GSM Echo Improved Results](gsm_echo_improved_results.png)
![Injection-Recovery Sensitivity](gsm_echo_injection_recovery.png)

## Data Provenance
- **Source**: GWOSC (Gravitational Wave Open Science Center)
- **GW150914**: Abbott et al. (2016), Phys. Rev. Lett. 116, 061102
- **LVT151012**: Abbott et al. (2016), Phys. Rev. D 93, 122003
- **GW151226**: Abbott et al. (2016), Phys. Rev. Lett. 116, 241103
- **GW170104**: Abbott et al. (2017), Phys. Rev. Lett. 118, 221101
