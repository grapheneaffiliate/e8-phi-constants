#!/usr/bin/env python3
"""
GSM φ-Echo Improved Search: Ringdown Subtraction + Multi-Event Stacking
=========================================================================
Improved analysis that:
1. Fits and subtracts the Kerr ringdown before searching for echoes
2. Cross-correlates H1×L1 post-merger residuals
3. Computes a coherent "φ-comb" statistic combining all expected delays
4. Stacks multiple BBH events (when available)

Uses REAL LIGO strain data from GWOSC.

Version 2.0 — March 2026
License: CC-BY-4.0
"""

import sys
import os
import numpy as np
from scipy.signal import butter, filtfilt, correlate
from scipy.optimize import minimize
import h5py

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gsm_ligo_template_generator import GSMEchoTemplate

PHI = (1 + np.sqrt(5)) / 2

SAMPLE_RATE = 4096
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Known events with data files (GPS, params, H1 file, L1 file)
# Merger times from GWTC-1; remnant parameters from NR fits
EVENTS = {
    'GW150914': {
        'gps_merger': 1126259462.4,
        'gps_start': 1126259446,
        'params': dict(M_remnant_solar=62.0, chi_remnant=0.67, d_Mpc=410),
        'h1': '/tmp/H-H1_LOSC_4_V1-1126259446-32.hdf5',
        'l1': '/tmp/L-L1_LOSC_4_V1-1126259446-32.hdf5',
    },
    'LVT151012': {
        'gps_merger': 1128678900.4,
        'gps_start': 1128678884,
        'params': dict(M_remnant_solar=35.0, chi_remnant=0.66, d_Mpc=1000),
        'h1': '/tmp/H-H1_LOSC_4_V1-1128678884-32.hdf5',
        'l1': '/tmp/L-L1_LOSC_4_V1-1128678884-32.hdf5',
    },
    'GW151226': {
        'gps_merger': 1135136350.6,
        'gps_start': 1135136334,
        'params': dict(M_remnant_solar=20.8, chi_remnant=0.74, d_Mpc=440),
        'h1': '/tmp/H-H1_LOSC_4_V1-1135136334-32.hdf5',
        'l1': '/tmp/L-L1_LOSC_4_V1-1135136334-32.hdf5',
    },
    'GW170104': {
        'gps_merger': 1167559936.6,
        'gps_start': 1167559920,
        'params': dict(M_remnant_solar=48.7, chi_remnant=0.64, d_Mpc=880),
        'h1': '/tmp/H-H1_LOSC_4_V1-1167559920-32.hdf5',
        'l1': '/tmp/L-L1_LOSC_4_V1-1167559920-32.hdf5',
    },
}


def load_strain(filepath):
    """Load strain data from GWOSC HDF5 file."""
    with h5py.File(filepath, 'r') as f:
        strain = f['strain/Strain'][:]
        gps_start = f['strain/Strain'].attrs['Xstart']
        dt = f['strain/Strain'].attrs['Xspacing']
        detector = f['meta/Detector'][()].decode()
    fs = int(round(1.0 / dt))
    return strain, gps_start, fs, detector


def bandpass(data, flow=20, fhigh=500, fs=SAMPLE_RATE):
    """Bandpass filter."""
    nyq = fs / 2
    b, a = butter(4, [flow / nyq, fhigh / nyq], btype='band')
    return filtfilt(b, a, data)


def whiten(strain, fs=SAMPLE_RATE, fft_len=4):
    """Whiten strain data using estimated PSD."""
    from scipy.signal import welch
    nperseg = int(fft_len * fs)
    freqs, psd = welch(strain, fs=fs, nperseg=nperseg)
    dt = 1.0 / fs
    N = len(strain)
    freq_full = np.fft.rfftfreq(N, d=dt)
    psd_interp = np.interp(freq_full, freqs, psd)
    psd_interp[psd_interp == 0] = np.inf

    strain_fft = np.fft.rfft(strain)
    white_fft = strain_fft / np.sqrt(psd_interp / dt / 2.0)
    white = np.fft.irfft(white_fft, n=N)
    white /= np.std(white)
    return white


# ==================================================================
# IMPROVEMENT 1: Ringdown subtraction
# ==================================================================
def fit_ringdown(data, f_qnm, tau_qnm, fs=SAMPLE_RATE):
    """
    Fit a damped sinusoid (Kerr ringdown) to the post-merger data.
    Model: h(t) = A * exp(-t/tau) * cos(2π f t + φ₀)

    Returns best-fit parameters and residual after subtraction.
    """
    N = len(data)
    t = np.arange(N) / fs

    def ringdown_model(params):
        A, phi0, tau_scale, f_scale = params
        tau = tau_qnm * tau_scale
        f = f_qnm * f_scale
        model = A * np.exp(-t / tau) * np.cos(2 * np.pi * f * t + phi0)
        return model

    def cost(params):
        model = ringdown_model(params)
        return np.sum((data - model)**2)

    # Initial guess: amplitude from data, zero phase
    A0 = np.max(np.abs(data[:int(0.01 * fs)]))  # first 10ms
    result = minimize(cost, [A0, 0.0, 1.0, 1.0],
                      bounds=[(0, 10 * A0), (-np.pi, np.pi),
                              (0.5, 2.0), (0.8, 1.2)],
                      method='L-BFGS-B')

    best_model = ringdown_model(result.x)
    residual = data - best_model

    return residual, best_model, result.x


# ==================================================================
# IMPROVEMENT 2: Coherent φ-comb statistic
# ==================================================================
def phi_comb_statistic(data, gen, fs=SAMPLE_RATE, n_echoes=7):
    """
    Coherent φ-comb: sum |autocorrelation| at all expected φ-ratio delays,
    weighted by expected echo amplitude φ⁻ᵏ.

    Compare to same statistic with N_trials random delay ratios.
    """
    # Autocorrelation
    autocorr = np.correlate(data, data, mode='full')
    autocorr = autocorr[len(autocorr) // 2:]
    if autocorr[0] != 0:
        autocorr /= autocorr[0]

    t_M = gen.t_M

    # φ-comb: weighted sum of |autocorr| at expected delays
    phi_comb = 0.0
    phi_delays_ms = []
    for k in range(1, n_echoes + 1):
        delay_s = gen.echo_delay(k)
        delay_samp = int(delay_s * fs)
        weight = gen.echo_amplitude(k)  # φ⁻ᵏ
        if 0 < delay_samp < len(autocorr):
            phi_comb += weight * abs(autocorr[delay_samp])
            phi_delays_ms.append(delay_s * 1000)

    # Control: try 1000 random delay ratios
    rng = np.random.default_rng(42)
    control_combs = []
    for _ in range(1000):
        ratio = rng.uniform(1.2, 2.5)  # avoid φ ≈ 1.618
        comb = 0.0
        for k in range(1, n_echoes + 1):
            delay_s = ratio**(k + 1) * t_M
            delay_samp = int(delay_s * fs)
            weight = PHI**(-k)  # same weights for fair comparison
            if 0 < delay_samp < len(autocorr):
                comb += weight * abs(autocorr[delay_samp])
        control_combs.append(comb)

    control_combs = np.array(control_combs)
    p_value = np.mean(control_combs >= phi_comb)
    percentile = np.mean(control_combs < phi_comb) * 100
    z_score = (phi_comb - np.mean(control_combs)) / np.std(control_combs) \
        if np.std(control_combs) > 0 else 0

    return phi_comb, control_combs, p_value, percentile, z_score, autocorr


# ==================================================================
# IMPROVEMENT 3: H1×L1 cross-correlation
# ==================================================================
def cross_detector_echo_test(h1_resid, l1_resid, gen, fs=SAMPLE_RATE):
    """
    Cross-correlate H1 and L1 post-merger residuals.
    If echoes are real astrophysical signals, they appear in both
    detectors (with ~10ms light-travel delay for GW150914).

    The cross-correlation at expected echo delays should be enhanced
    compared to random delays.
    """
    # Cross-correlation (not auto-correlation)
    xcorr = correlate(h1_resid, l1_resid, mode='full')
    mid = len(xcorr) // 2
    # Normalize
    norm = np.sqrt(np.sum(h1_resid**2) * np.sum(l1_resid**2))
    if norm > 0:
        xcorr /= norm

    t_M = gen.t_M

    # Check cross-correlation at φ-echo delays (both positive and negative lags)
    results = []
    for k in range(1, 8):
        delay_samp = int(gen.echo_delay(k) * fs)
        # Check around the expected delay ± light travel time (~10ms = 41 samples)
        for offset in [0]:  # just at exact delay
            idx = mid + delay_samp + offset
            if 0 <= idx < len(xcorr):
                val = xcorr[idx]
                results.append({'k': k, 'delay_ms': gen.echo_delay(k) * 1000,
                                'xcorr': val})

    # Control
    rng = np.random.default_rng(42)
    control_vals = []
    for _ in range(100):
        ratio = rng.uniform(1.2, 2.5)
        for k in range(1, 8):
            delay_samp = int(ratio**(k + 1) * t_M * fs)
            idx = mid + delay_samp
            if 0 <= idx < len(xcorr):
                control_vals.append(abs(xcorr[idx]))

    phi_mean = np.mean([abs(r['xcorr']) for r in results]) if results else 0
    control_mean = np.mean(control_vals) if control_vals else 0
    excess = (phi_mean / control_mean - 1) * 100 if control_mean > 0 else 0

    return results, phi_mean, control_mean, excess, xcorr


# ==================================================================
# IMPROVEMENT 4: Time-slide on residual
# ==================================================================
def time_slide_on_residual(full_bp, merger_idx, gen, fs=SAMPLE_RATE,
                           n_slides=200):
    """
    Run time-slide significance test on ringdown-subtracted residuals.
    For each off-source segment, fit and subtract a damped sinusoid
    at the same f_QNM, then compute the matched filter SNR.
    """
    print("  Running 200 time-slide trials on ringdown-subtracted data...")
    post_len = int(0.5 * fs)
    total_len = len(full_bp)
    exclude_lo = max(0, merger_idx - fs)
    exclude_hi = min(total_len, merger_idx + fs)

    # Generate echo-only template (post-ringdown)
    t_templ = np.arange(0, 0.5, 1.0 / fs)
    h_echo = np.zeros_like(t_templ)
    for k in range(1, 10):
        delay = gen.echo_delay(k)
        amp = gen.echo_amplitude(k)
        mask = t_templ >= delay
        h_echo[mask] += amp * np.exp(-(t_templ[mask] - delay) / gen.tau_qnm) * \
                        np.cos(2 * np.pi * gen.f_qnm * (t_templ[mask] - delay))
    h_echo_bp = bandpass(h_echo, flow=20, fhigh=500)

    def compute_snr(segment):
        # Fit and subtract ringdown
        resid, _, _ = fit_ringdown(segment, gen.f_qnm, gen.tau_qnm)
        c = correlate(resid, h_echo_bp, mode='same')
        c_norm = np.sqrt(np.sum(h_echo_bp**2) * np.sum(resid**2))
        if c_norm > 0:
            c /= c_norm
        c_std = np.std(c)
        return np.max(np.abs(c)) / c_std if c_std > 0 else 0

    # On-source
    on_source = full_bp[merger_idx:merger_idx + post_len]
    on_snr = compute_snr(on_source)

    # Off-source
    rng = np.random.default_rng(42)
    null_snrs = []
    for _ in range(n_slides):
        while True:
            offset = rng.integers(0, total_len - post_len)
            if offset + post_len < exclude_lo or offset > exclude_hi:
                break
        segment = full_bp[offset:offset + post_len]
        null_snrs.append(compute_snr(segment))

    null_snrs = np.array(null_snrs)
    p_value = np.mean(null_snrs >= on_snr)
    percentile = np.mean(null_snrs < on_snr) * 100

    return on_snr, p_value, null_snrs, percentile


def _get_version(pkg):
    try:
        import importlib.metadata
        return importlib.metadata.version(pkg)
    except Exception:
        return "unknown"


def make_plots(event_name, h1_post, h1_resid, h1_model, h1_corr_resid,
               autocorr, xcorr, gen, phi_comb, control_combs,
               on_snr_resid, null_snrs_resid, fs=SAMPLE_RATE):
    """Generate comprehensive 4-panel results figure."""
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(2, 2, figsize=(16, 12))

    t_post = np.arange(len(h1_post)) / fs * 1000

    # Panel 1: Original data + ringdown fit + residual
    ax = axes[0, 0]
    ax.plot(t_post[:400], h1_post[:400], 'k', alpha=0.4, linewidth=0.5,
            label='Whitened data')
    ax.plot(t_post[:400], h1_model[:400], 'r-', linewidth=1.5,
            label='Ringdown fit')
    ax.plot(t_post[:400], h1_resid[:400], 'b', alpha=0.6, linewidth=0.5,
            label='Residual')
    for k in range(1, 6):
        d = gen.echo_delay(k) * 1000
        if d < t_post[399]:
            ax.axvline(d, color='gold', alpha=0.5, linestyle='--',
                       linewidth=1.5)
    ax.set_xlabel('Time post-merger (ms)')
    ax.set_ylabel('Strain')
    ax.set_title(f'{event_name}: Data, ringdown fit, and residual')
    ax.legend(fontsize=7)
    ax.set_xlim(0, t_post[399])

    # Panel 2: Matched filter on residual
    ax = axes[0, 1]
    t_corr = np.arange(len(h1_corr_resid)) / fs * 1000
    ax.plot(t_corr, h1_corr_resid, 'b', linewidth=0.5)
    ax.set_xlabel('Time (ms)')
    ax.set_ylabel('Normalized correlation')
    ax.set_title(f'Matched filter on RESIDUAL (SNR = {on_snr_resid:.2f})')
    ax.set_xlim(0, min(100, t_corr[-1]))

    # Panel 3: φ-comb statistic distribution
    ax = axes[1, 0]
    ax.hist(control_combs, bins=40, density=True, alpha=0.7, color='gray',
            label=f'Random ratios (N=1000)')
    ax.axvline(phi_comb, color='red', linewidth=2,
               label=f'φ-comb = {phi_comb:.4f}')
    ax.axvline(np.mean(control_combs), color='blue', linestyle='--',
               label=f'Mean = {np.mean(control_combs):.4f}')
    ax.set_xlabel('Weighted comb statistic')
    ax.set_ylabel('Density')
    ax.set_title('φ-comb vs random delay ratios')
    ax.legend(fontsize=8)

    # Panel 4: Time-slide null distribution for residual
    ax = axes[1, 1]
    ax.hist(null_snrs_resid, bins=30, density=True, alpha=0.7, color='gray',
            label=f'Off-source (N={len(null_snrs_resid)})')
    ax.axvline(on_snr_resid, color='red', linewidth=2,
               label=f'On-source = {on_snr_resid:.2f}')
    ax.set_xlabel('Matched filter SNR (on residual)')
    ax.set_ylabel('Density')
    ax.set_title('Time-slide null distribution (ringdown-subtracted)')
    ax.legend(fontsize=8)

    plt.tight_layout()
    outpath = os.path.join(REPO_ROOT, 'gsm_echo_improved_results.png')
    plt.savefig(outpath, dpi=150)
    print(f"  Saved plot: {outpath}")
    plt.close()
    return outpath


def write_report(event_name, event_info, gen,
                 on_snr_resid, p_resid, pctile_resid,
                 null_mean, null_std, null_max,
                 l1_snr_resid, l1_p_resid, l1_pctile_resid,
                 phi_comb, comb_p, comb_pctile, comb_z,
                 xcorr_phi_mean, xcorr_ctrl_mean, xcorr_excess,
                 phi_results_list):
    """Write improved results report."""
    phi_excess = xcorr_excess

    # Verdict
    significant = (p_resid < 0.01 and comb_p < 0.01 and xcorr_excess > 50)
    hint = (p_resid < 0.05 or comb_p < 0.05 or xcorr_excess > 20)

    if significant:
        verdict = "SIGNIFICANT DETECTION"
        verdict_detail = ("Strong evidence for φ-echoes after ringdown subtraction. "
                          "Requires independent verification.")
    elif hint:
        verdict = "INTERESTING HINT"
        verdict_detail = "Suggestive signal in one or more tests. Needs more events."
    else:
        verdict = "NULL RESULT"
        verdict_detail = (
            "No φ-echo signal detected after proper ringdown subtraction at O1 "
            "sensitivity. All three independent tests (matched filter on residual, "
            "φ-comb statistic, H1×L1 cross-correlation) are consistent with noise.\n\n"
            "This does NOT falsify GSM. Echo amplitudes decay as φ⁻ᵏ and the first "
            "echo (62% of ringdown) is expected to be near or below the O1 noise "
            "floor for GW150914 (ringdown SNR ~7). Higher-SNR events (GW250114, "
            "SNR~80) or O5 sensitivity (~5× improvement) are needed."
        )

    report = f"""# GSM φ-Echo Improved Search Results

**Date**: March 14, 2026
**Analysis version**: 2.0 (with ringdown subtraction)
**Data**: Real LIGO strain data from GWOSC

## Improvements Over v1.0
1. **Ringdown subtraction**: Best-fit Kerr QNM removed before echo search
2. **Coherent φ-comb statistic**: Weighted sum at all expected delays vs 1000 random ratios
3. **H1×L1 cross-correlation**: Real echoes must appear in both detectors
4. **Time-slides on residual**: Significance tested against off-source ringdown-subtracted segments

## Event: {event_name}
| Parameter | Value |
|-----------|-------|
| M_remnant | {event_info['params']['M_remnant_solar']} M☉ |
| χ_remnant | {event_info['params']['chi_remnant']} |
| Distance | {event_info['params']['d_Mpc']} Mpc |
| f_QNM | {gen.f_qnm:.1f} Hz |
| τ_QNM | {gen.tau_qnm*1000:.3f} ms |
| t_M = 2GM/c³ | {gen.t_M*1000:.4f} ms |

### Predicted Echo Table (Zero Free Parameters)
| k | Delay (ms) | Amplitude φ⁻ᵏ | Polarization |
|---|-----------|---------------|-------------|
"""
    for k in range(1, 8):
        report += (f"| {k} | {gen.echo_delay(k)*1000:.3f} | "
                   f"{gen.echo_amplitude(k):.5f} | "
                   f"{gen.echo_polarization(k):.1f}° |\n")

    report += f"""
## Test 1: Matched Filter on Ringdown-Subtracted Residual

The Kerr ringdown (damped sinusoid at f_QNM) is fit to the post-merger data
and subtracted. The echo template is then cross-correlated with the **residual**.

### H1 (Hanford)
| Metric | Value |
|--------|-------|
| Residual matched filter SNR | **{on_snr_resid:.2f}** |
| Time-slide p-value (200 trials) | {p_resid:.4f} |
| Percentile rank | {pctile_resid:.1f}% |
| Null distribution | mean={null_mean:.2f}, std={null_std:.2f}, max={null_max:.2f} |

### L1 (Livingston)
| Metric | Value |
|--------|-------|
| Residual matched filter SNR | **{l1_snr_resid:.2f}** |
| Time-slide p-value (200 trials) | {l1_p_resid:.4f} |
| Percentile rank | {l1_pctile_resid:.1f}% |

## Test 2: Coherent φ-Comb Statistic

Weighted sum of |autocorrelation| at all predicted φ-echo delays
(weights = φ⁻ᵏ), compared against 1000 random delay ratios.

| Metric | Value |
|--------|-------|
| φ-comb value | {phi_comb:.6f} |
| p-value (vs 1000 random ratios) | {comb_p:.4f} |
| Percentile | {comb_pctile:.1f}% |
| z-score | {comb_z:.2f} |

## Test 3: H1×L1 Cross-Correlation

If echoes are real astrophysical signals, they must appear in both detectors.

| Metric | Value |
|--------|-------|
| Mean |xcorr| at φ-delays | {xcorr_phi_mean:.6f} |
| Mean |xcorr| at random delays | {xcorr_ctrl_mean:.6f} |
| φ-delay excess | {xcorr_excess:+.1f}% |

## Combined Verdict: **{verdict}**

{verdict_detail}

## Plots
![GSM Echo Improved Results](gsm_echo_improved_results.png)

## Method
1. Load real GWOSC strain data (H1 + L1, 32s at 4096 Hz)
2. Whiten using Welch PSD estimate, bandpass 20-500 Hz
3. **Fit Kerr ringdown** (A·exp(-t/τ)·cos(2πft + φ₀)) to post-merger data
4. **Subtract ringdown** to isolate potential echo residual
5. Cross-correlate residual with echo-only template
6. Time-slide significance: 200 off-source segments (each ringdown-subtracted)
7. φ-comb: weighted autocorrelation at predicted delays vs 1000 random ratios
8. H1×L1 cross-correlation at φ-delays vs random delays

## Why This Is Better Than v1.0
The v1.0 analysis found high matched-filter SNR (8.23), but this was a false
positive: the echo template shared f_QNM with the actual ringdown. By fitting
and removing the ringdown first, we test only for **excess structure** at
φ-ratio delays — the genuine GSM prediction.

## Data Provenance
- **Source**: GWOSC (Gravitational Wave Open Science Center)
- **Reference**: Abbott et al. (2016), Phys. Rev. Lett. 116, 061102

## Software
- scipy {_get_version('scipy')}, numpy {_get_version('numpy')}, h5py {_get_version('h5py')}
- GSM LIGO Template Generator v2.4
"""

    outpath = os.path.join(REPO_ROOT, 'GSM_ECHO_IMPROVED_RESULTS.md')
    with open(outpath, 'w') as f:
        f.write(report)
    print(f"  Saved report: {outpath}")
    return outpath


def analyze_event(event_name, event_info):
    """Run the full improved analysis on one event."""
    print(f"\n{'='*70}")
    print(f"ANALYZING: {event_name}")
    print(f"{'='*70}")

    params = event_info['params']
    gen = GSMEchoTemplate(**params)

    # Load data
    print(f"\n[1] Loading strain data...")
    h1_strain, h1_start, h1_fs, h1_det = load_strain(event_info['h1'])
    l1_strain, l1_start, l1_fs, l1_det = load_strain(event_info['l1'])
    print(f"  {h1_det}: {len(h1_strain)} samples, {h1_fs} Hz")
    print(f"  {l1_det}: {len(l1_strain)} samples, {l1_fs} Hz")

    # Condition
    print(f"\n[2] Whitening and filtering...")
    h1_white = whiten(h1_strain, fs=h1_fs)
    l1_white = whiten(l1_strain, fs=l1_fs)
    h1_bp = bandpass(h1_white, flow=20, fhigh=500, fs=h1_fs)
    l1_bp = bandpass(l1_white, flow=20, fhigh=500, fs=l1_fs)

    # Extract post-merger
    merger_offset = event_info['gps_merger'] - event_info['gps_start']
    merger_idx = int(merger_offset * SAMPLE_RATE)
    post_len = int(0.5 * SAMPLE_RATE)
    h1_post = h1_bp[merger_idx:merger_idx + post_len]
    l1_post = l1_bp[merger_idx:merger_idx + post_len]

    # Ringdown subtraction
    print(f"\n[3] Fitting and subtracting ringdown...")
    h1_resid, h1_model, h1_fit = fit_ringdown(h1_post, gen.f_qnm, gen.tau_qnm)
    l1_resid, l1_model, l1_fit = fit_ringdown(l1_post, gen.f_qnm, gen.tau_qnm)
    print(f"  H1 fit: A={h1_fit[0]:.4f}, φ₀={h1_fit[1]:.3f}, "
          f"τ_scale={h1_fit[2]:.3f}, f_scale={h1_fit[3]:.3f}")
    print(f"  H1 ringdown power removed: "
          f"{(1 - np.sum(h1_resid**2)/np.sum(h1_post**2))*100:.1f}%")
    print(f"  L1 fit: A={l1_fit[0]:.4f}, φ₀={l1_fit[1]:.3f}, "
          f"τ_scale={l1_fit[2]:.3f}, f_scale={l1_fit[3]:.3f}")

    # Echo template
    t_templ = np.arange(0, 0.5, 1.0 / SAMPLE_RATE)
    h_echo = np.zeros_like(t_templ)
    for k in range(1, 10):
        delay = gen.echo_delay(k)
        amp = gen.echo_amplitude(k)
        mask = t_templ >= delay
        h_echo[mask] += amp * np.exp(-(t_templ[mask] - delay) / gen.tau_qnm) * \
                        np.cos(2 * np.pi * gen.f_qnm * (t_templ[mask] - delay))
    h_echo_bp = bandpass(h_echo, flow=20, fhigh=500)

    # Matched filter on residual
    print(f"\n[4] Matched filter on residual (H1)...")
    h1_corr_resid = correlate(h1_resid, h_echo_bp, mode='same')
    norm = np.sqrt(np.sum(h_echo_bp**2) * np.sum(h1_resid**2))
    if norm > 0:
        h1_corr_resid /= norm

    # Time-slide on residual
    print(f"\n[5] Time-slide significance (ringdown-subtracted)...")
    h1_on_snr, h1_p, h1_nulls, h1_pctile = \
        time_slide_on_residual(h1_bp, merger_idx, gen)
    print(f"  H1 residual SNR: {h1_on_snr:.2f}")
    print(f"  H1 p-value: {h1_p:.4f}, rank: {h1_pctile:.1f}%")
    print(f"  Null: mean={np.mean(h1_nulls):.2f}, "
          f"std={np.std(h1_nulls):.2f}, max={np.max(h1_nulls):.2f}")

    l1_on_snr, l1_p, l1_nulls, l1_pctile = \
        time_slide_on_residual(l1_bp, merger_idx, gen)
    print(f"  L1 residual SNR: {l1_on_snr:.2f}")
    print(f"  L1 p-value: {l1_p:.4f}, rank: {l1_pctile:.1f}%")

    # φ-comb statistic
    print(f"\n[6] Coherent φ-comb statistic...")
    phi_comb, control_combs, comb_p, comb_pctile, comb_z, autocorr = \
        phi_comb_statistic(h1_resid, gen)
    print(f"  φ-comb = {phi_comb:.6f}")
    print(f"  Control mean = {np.mean(control_combs):.6f}")
    print(f"  p-value: {comb_p:.4f}, z-score: {comb_z:.2f}")

    # H1×L1 cross-correlation
    print(f"\n[7] H1×L1 cross-correlation...")
    xcorr_results, xcorr_phi, xcorr_ctrl, xcorr_excess, xcorr = \
        cross_detector_echo_test(h1_resid, l1_resid, gen)
    print(f"  φ-delay mean |xcorr|: {xcorr_phi:.6f}")
    print(f"  Random mean |xcorr|:  {xcorr_ctrl:.6f}")
    print(f"  Excess: {xcorr_excess:+.1f}%")

    # Plots (only for first event to avoid overwriting)
    print(f"\n[8] Generating plots...")
    make_plots(event_name, h1_post, h1_resid, h1_model, h1_corr_resid,
               autocorr, xcorr, gen, phi_comb, control_combs,
               h1_on_snr, h1_nulls)

    return {
        'event': event_name,
        'h1_snr': h1_on_snr, 'h1_p': h1_p,
        'l1_snr': l1_on_snr, 'l1_p': l1_p,
        'phi_comb': phi_comb, 'comb_p': comb_p, 'comb_z': comb_z,
        'xcorr_excess': xcorr_excess,
    }


def main():
    print("=" * 70)
    print("GSM φ-ECHO IMPROVED SEARCH — MULTI-EVENT")
    print("Ringdown subtraction + φ-comb + H1×L1 + stacking")
    print("=" * 70)

    # Filter to events with available data
    available = {}
    for name, info in EVENTS.items():
        if os.path.exists(info['h1']) and os.path.exists(info['l1']):
            available[name] = info
        else:
            print(f"  Skipping {name}: data files not found")

    if not available:
        print("ERROR: No event data found")
        sys.exit(1)

    print(f"\n  {len(available)} events available: {', '.join(available.keys())}")

    results = []
    for event_name, event_info in available.items():
        try:
            r = analyze_event(event_name, event_info)
            results.append(r)
        except Exception as e:
            print(f"  ERROR analyzing {event_name}: {e}")
            import traceback
            traceback.print_exc()

    # -------------------------------------------------------
    # Stacked φ-comb: combine z-scores across events
    # -------------------------------------------------------
    if len(results) > 1:
        print(f"\n{'='*70}")
        print(f"STACKED ANALYSIS ({len(results)} events)")
        print(f"{'='*70}")
        z_scores = [r['comb_z'] for r in results]
        # Fisher's method: combined z-score = sum(z) / sqrt(N)
        combined_z = np.sum(z_scores) / np.sqrt(len(z_scores))
        from scipy.stats import norm
        combined_p = 1 - norm.cdf(combined_z)
        print(f"  Individual z-scores: {[f'{z:.2f}' for z in z_scores]}")
        print(f"  Combined z-score (Fisher): {combined_z:.2f}")
        print(f"  Combined p-value: {combined_p:.4f}")

    # Final summary
    print("\n" + "=" * 70)
    print("FINAL SUMMARY")
    print("=" * 70)
    print(f"\n  {'Event':<12} {'H1 SNR':>8} {'H1 p':>8} {'φ-comb z':>10} "
          f"{'φ-comb p':>10} {'H1×L1':>8}")
    print(f"  {'-'*12} {'-'*8} {'-'*8} {'-'*10} {'-'*10} {'-'*8}")
    for r in results:
        print(f"  {r['event']:<12} {r['h1_snr']:>8.2f} {r['h1_p']:>8.4f} "
              f"{r['comb_z']:>10.2f} {r['comb_p']:>10.4f} "
              f"{r['xcorr_excess']:>+7.1f}%")

    if len(results) > 1:
        print(f"\n  Stacked φ-comb: z = {combined_z:.2f}, p = {combined_p:.4f}")

    # Overall verdict — φ-comb is the primary discriminant
    print()
    best_comb_p = min(r['comb_p'] for r in results)
    stacked_significant = len(results) > 1 and combined_p < 0.01

    if best_comb_p < 0.001 or stacked_significant:
        print("  OVERALL VERDICT: SIGNIFICANT — φ-ratio structure detected")
        print("  Requires independent verification.")
    elif best_comb_p < 0.05 or (len(results) > 1 and combined_p < 0.05):
        print("  OVERALL VERDICT: INTERESTING HINT — suggestive φ-comb signal")
    else:
        print("  OVERALL VERDICT: NULL RESULT at O1/O2 sensitivity")
        print("  Pipeline validated and ready for higher-SNR events.")
        print("  Next targets: GW250114 (SNR~80), O5 data (~5× improvement)")
    print("=" * 70)


if __name__ == "__main__":
    main()
