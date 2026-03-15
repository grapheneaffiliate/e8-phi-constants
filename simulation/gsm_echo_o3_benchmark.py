#!/usr/bin/env python3
"""
GSM φ-Echo O3 Benchmark via Noise Scaling
===========================================
Uses real O1 LIGO noise scaled to O3/O4 sensitivity to benchmark
echo detection for the highest-SNR O3 BBH events and GW250114.

Method:
  - Start with real GW150914 H1 off-source noise (whitened, bandpassed)
  - Scale noise by 1/improvement_factor to simulate better sensitivity
  - Inject GSM echo signals with O3 event remnant parameters
  - Run the validated template-ratio φ-comb
  - Measure detection z-score and p-value

This is physically valid: O1→O3 noise improvement is primarily a
broadband reduction in the noise floor. The spectrum shape at
20-500 Hz is similar across runs. For matched filtering, scaling
the noise is equivalent to scaling the signal.

Version 1.0 — March 2026
License: CC-BY-4.0
"""

import sys
import os
import numpy as np
from scipy.signal import butter, filtfilt, correlate
import h5py

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gsm_ligo_template_generator import GSMEchoTemplate

PHI = (1 + np.sqrt(5)) / 2
SAMPLE_RATE = 4096
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

H1_FILE = '/tmp/H-H1_LOSC_4_V1-1126259446-32.hdf5'

# O3 events to benchmark (highest ringdown SNR)
O3_EVENTS = {
    'GW200129': {
        'network_snr': 26.8, 'M_remnant': 60.0,
        'chi_remnant': 0.68, 'd_Mpc': 900,
    },
    'GW190521_074359': {
        'network_snr': 26.0, 'M_remnant': 63.0,
        'chi_remnant': 0.69, 'd_Mpc': 1100,
    },
    'GW190814': {
        'network_snr': 25.0, 'M_remnant': 25.6,
        'chi_remnant': 0.28, 'd_Mpc': 241,
    },
    'GW190412': {
        'network_snr': 19.1, 'M_remnant': 37.0,
        'chi_remnant': 0.67, 'd_Mpc': 740,
    },
}

# Also test GW250114 projection
GW250114 = {
    'network_snr': 80.0, 'M_remnant': 75.0,
    'chi_remnant': 0.70, 'd_Mpc': 200,
}

# Noise improvement relative to O1
NOISE_FACTORS = {
    'O1': 1.0,
    'O3': 1.8,   # O3 is ~1.8× better than O1
    'O4': 2.5,   # O4 is ~2.5× better than O1
    'O5': 5.0,   # O5 is ~5× better than O1
}


def load_and_condition():
    """Load real O1 noise, whiten, and bandpass."""
    with h5py.File(H1_FILE, 'r') as f:
        strain = f['strain/Strain'][:]
        dt = f['strain/Strain'].attrs['Xspacing']
    fs = int(round(1.0 / dt))

    from scipy.signal import welch
    nperseg = 4 * fs
    freqs, psd = welch(strain, fs=fs, nperseg=nperseg)
    N = len(strain)
    freq_full = np.fft.rfftfreq(N, d=1.0/fs)
    psd_interp = np.interp(freq_full, freqs, psd)
    psd_interp[psd_interp == 0] = np.inf
    white = np.fft.irfft(
        np.fft.rfft(strain) / np.sqrt(psd_interp / (1.0/fs) / 2.0), n=N
    )
    white /= np.std(white)

    nyq = fs / 2
    b, a = butter(4, [20/nyq, 500/nyq], btype='band')
    bp = filtfilt(b, a, white)
    return bp, fs


def build_echo_template(t_M, f_qnm, tau_qnm, ratio, duration, fs, n_echoes=7):
    """Build echo-train template with given delay ratio."""
    t = np.arange(0, duration, 1.0 / fs)
    h = np.zeros_like(t)
    for k in range(1, n_echoes + 1):
        delay = ratio**(k + 1) * t_M
        amp = PHI**(-k)
        mask = t >= delay
        if np.any(mask):
            h[mask] += amp * np.exp(-(t[mask] - delay) / tau_qnm) * \
                       np.cos(2 * np.pi * f_qnm * (t[mask] - delay))
    return h


def phi_comb_test(data, gen, fs=SAMPLE_RATE, n_controls=1000):
    """Run template-ratio φ-comb on data."""
    duration = len(data) / fs
    t_M = gen.t_M

    def mf_snr(template):
        c = correlate(data, template, mode='same')
        tn = np.sqrt(np.sum(template**2))
        if tn > 0:
            c /= tn
        cs = np.std(c)
        return np.max(np.abs(c)) / cs if cs > 0 else 0

    phi_t = build_echo_template(t_M, gen.f_qnm, gen.tau_qnm,
                                 PHI, duration, fs)
    phi_snr = mf_snr(phi_t)

    rng = np.random.default_rng(42)
    ctrl = []
    for _ in range(n_controls):
        r = rng.uniform(1.2, 2.5)
        t = build_echo_template(t_M, gen.f_qnm, gen.tau_qnm,
                                 r, duration, fs)
        ctrl.append(mf_snr(t))
    ctrl = np.array(ctrl)

    z = (phi_snr - np.mean(ctrl)) / np.std(ctrl) if np.std(ctrl) > 0 else 0
    p = np.mean(ctrl >= phi_snr)
    return z, p, phi_snr


def generate_echo_signal(gen, duration, amplitude, fs=SAMPLE_RATE):
    """Generate synthetic GSM echo signal."""
    t = np.arange(0, duration, 1.0 / fs)
    h = np.zeros_like(t)
    for k in range(1, 10):
        delay = gen.echo_delay(k)
        amp = gen.echo_amplitude(k) * amplitude
        mask = t >= delay
        if np.any(mask):
            h[mask] += amp * np.exp(-(t[mask] - delay) / gen.tau_qnm) * \
                       np.cos(2 * np.pi * gen.f_qnm * (t[mask] - delay))
    return h


def main():
    print("=" * 80)
    print("GSM φ-ECHO O3 BENCHMARK: Noise-Scaled Injection-Recovery")
    print("Using real O1 noise scaled to O3/O4/O5 sensitivity")
    print("=" * 80)

    if not os.path.exists(H1_FILE):
        print(f"ERROR: {H1_FILE} not found")
        sys.exit(1)

    print("\n[1] Loading and conditioning real O1 noise...")
    bp, fs = load_and_condition()
    post_len = int(0.5 * fs)
    noise_start = 4096  # off-source

    # Collect 5 noise segments for averaging
    noise_segments = []
    for i in range(5):
        offset = noise_start + i * post_len
        if offset + post_len < len(bp) // 2:
            noise_segments.append(bp[offset:offset + post_len])
    o1_noise_rms = np.mean([np.std(seg) for seg in noise_segments])
    print(f"  O1 noise RMS: {o1_noise_rms:.6f}")
    print(f"  Noise segments: {len(noise_segments)}")

    # Test each O3 event at different sensitivity levels
    all_events = {**O3_EVENTS, 'GW250114': GW250114}
    all_results = []

    for event_name, info in all_events.items():
        gen = GSMEchoTemplate(
            M_remnant_solar=info['M_remnant'],
            chi_remnant=info['chi_remnant'],
            d_Mpc=info['d_Mpc']
        )

        ringdown_snr = info['network_snr'] * 0.30
        echo_snr_1 = ringdown_snr * PHI**(-1)

        print(f"\n{'='*80}")
        print(f"EVENT: {event_name}")
        print(f"  M_remnant = {info['M_remnant']:.0f} M☉, "
              f"χ = {info['chi_remnant']:.2f}, "
              f"f_QNM = {gen.f_qnm:.1f} Hz")
        print(f"  Network SNR = {info['network_snr']:.1f}, "
              f"Ringdown SNR ≈ {ringdown_snr:.1f}, "
              f"Echo₁ SNR ≈ {echo_snr_1:.1f}")

        # Compute echo signal amplitude to match expected echo SNR
        # at each sensitivity level
        echo_unit = generate_echo_signal(gen, 0.5, 1.0, fs)
        echo_rms = np.std(echo_unit)

        print(f"\n  {'Sensitivity':<12} {'Noise scale':>11} {'Eff echo SNR':>13} "
              f"{'z-score':>8} {'p-value':>8} {'Detection':>10}")
        print(f"  {'-'*12} {'-'*11} {'-'*13} {'-'*8} {'-'*8} {'-'*10}")

        event_results = []
        for run, improvement in NOISE_FACTORS.items():
            # Scale noise to simulate this run's sensitivity
            # Higher improvement = lower noise = higher effective echo SNR
            noise_scale = 1.0 / improvement
            eff_echo_snr = echo_snr_1 * improvement

            # Set echo amplitude to match expected echo SNR at this sensitivity
            # SNR = amplitude * echo_rms / (noise_rms * noise_scale)
            amplitude = eff_echo_snr * (o1_noise_rms * noise_scale) / echo_rms \
                if echo_rms > 0 else 0

            # Average over noise segments
            z_scores = []
            p_values = []
            for seg in noise_segments:
                scaled_noise = seg * noise_scale
                echo_sig = generate_echo_signal(gen, 0.5, amplitude, fs)
                injected = scaled_noise + echo_sig[:post_len]
                z, p, _ = phi_comb_test(injected, gen, fs, n_controls=500)
                z_scores.append(z)
                p_values.append(p)

            mean_z = np.mean(z_scores)
            mean_p = np.mean(p_values)

            if mean_p < 0.001:
                det = "STRONG"
            elif mean_p < 0.05:
                det = "YES"
            elif mean_p < 0.1:
                det = "MARGINAL"
            else:
                det = "no"

            print(f"  {run:<12} {noise_scale:>11.3f} {eff_echo_snr:>13.1f} "
                  f"{mean_z:>8.2f} {mean_p:>8.4f} {det:>10}")

            event_results.append({
                'run': run, 'noise_scale': noise_scale,
                'eff_echo_snr': eff_echo_snr,
                'z': mean_z, 'p': mean_p, 'det': det,
            })

        all_results.append({
            'name': event_name, 'results': event_results,
            'echo_snr_1': echo_snr_1, 'ringdown_snr': ringdown_snr,
            'f_qnm': gen.f_qnm,
        })

    # =====================================================================
    # Summary and plot
    # =====================================================================
    print(f"\n{'='*80}")
    print("SUMMARY: Detection at O3 Sensitivity")
    print(f"{'='*80}\n")

    print(f"  {'Event':<22} {'Echo₁ SNR':>10} {'O1 z':>6} {'O3 z':>6} "
          f"{'O4 z':>6} {'O5 z':>6}")
    print(f"  {'-'*20} {'-'*10} {'-'*6} {'-'*6} {'-'*6} {'-'*6}")

    for ar in all_results:
        o1_z = next(r['z'] for r in ar['results'] if r['run'] == 'O1')
        o3_z = next(r['z'] for r in ar['results'] if r['run'] == 'O3')
        o4_z = next(r['z'] for r in ar['results'] if r['run'] == 'O4')
        o5_z = next(r['z'] for r in ar['results'] if r['run'] == 'O5')

        print(f"  {ar['name']:<20} {ar['echo_snr_1']:>10.1f} "
              f"{o1_z:>6.2f} {o3_z:>6.2f} {o4_z:>6.2f} {o5_z:>6.2f}")

    # Generate plot
    print(f"\n  Generating benchmark plot...")
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, 2, figsize=(16, 7))

    # Panel 1: z-score vs sensitivity for each event
    ax = axes[0]
    colors = {'GW200129': 'green', 'GW190521_074359': 'blue',
              'GW190814': 'purple', 'GW190412': 'orange',
              'GW250114': 'red'}

    for ar in all_results:
        runs = [r['run'] for r in ar['results']]
        zs = [r['z'] for r in ar['results']]
        x = [NOISE_FACTORS[run] for run in runs]
        c = colors.get(ar['name'], 'gray')
        lw = 3 if ar['name'] == 'GW250114' else 1.5
        ls = '-' if ar['name'] == 'GW250114' else '--'
        ax.plot(x, zs, f'{ls}', color=c, linewidth=lw, marker='o',
                markersize=6, label=ar['name'])

    ax.axhline(1.645, color='orange', linestyle=':', alpha=0.5,
               label='p = 0.05')
    ax.axhline(2.576, color='red', linestyle=':', alpha=0.5,
               label='p = 0.005')
    ax.axhline(0, color='gray', linestyle='-', alpha=0.3)

    ax.set_xlabel('Noise Improvement Factor (relative to O1)', fontsize=12)
    ax.set_ylabel('φ-comb z-score', fontsize=12)
    ax.set_title('Echo Detection vs Detector Sensitivity', fontsize=13)
    ax.legend(fontsize=7, loc='upper left')
    ax.grid(True, alpha=0.3)

    # Panel 2: effective echo SNR vs z-score (all events combined)
    ax = axes[1]
    for ar in all_results:
        eff_snrs = [r['eff_echo_snr'] for r in ar['results']]
        zs = [r['z'] for r in ar['results']]
        c = colors.get(ar['name'], 'gray')
        ax.scatter(eff_snrs, zs, c=c, s=60, edgecolors='black',
                   linewidths=0.5, label=ar['name'], zorder=5)

    ax.axhline(1.645, color='orange', linestyle=':', alpha=0.5,
               label='p = 0.05')
    ax.axhline(0, color='gray', linestyle='-', alpha=0.3)

    ax.set_xlabel('Effective First Echo SNR', fontsize=12)
    ax.set_ylabel('φ-comb z-score', fontsize=12)
    ax.set_title('φ-Comb Response vs Echo SNR (Noise-Scaled)', fontsize=13)
    ax.legend(fontsize=7)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    outpath = os.path.join(REPO_ROOT, 'gsm_echo_o3_benchmark.png')
    plt.savefig(outpath, dpi=150)
    print(f"  Saved: {outpath}")
    plt.close()

    # Write report
    report_path = os.path.join(REPO_ROOT, 'GSM_ECHO_O3_BENCHMARK.md')
    with open(report_path, 'w') as f:
        f.write("# GSM φ-Echo O3 Benchmark: Noise-Scaled Injection-Recovery\n\n")
        f.write("**Date**: March 14, 2026\n")
        f.write("**Method**: Real O1 noise scaled to O3/O4/O5 sensitivity\n\n")
        f.write("## Results\n\n")
        f.write("| Event | Echo₁ SNR | O1 z | O3 z | O4 z | O5 z |\n")
        f.write("|-------|-----------|------|------|------|------|\n")
        for ar in all_results:
            o1_z = next(r['z'] for r in ar['results'] if r['run'] == 'O1')
            o3_z = next(r['z'] for r in ar['results'] if r['run'] == 'O3')
            o4_z = next(r['z'] for r in ar['results'] if r['run'] == 'O4')
            o5_z = next(r['z'] for r in ar['results'] if r['run'] == 'O5')
            f.write(f"| {ar['name']} | {ar['echo_snr_1']:.1f} | "
                    f"{o1_z:.2f} | {o3_z:.2f} | {o4_z:.2f} | {o5_z:.2f} |\n")
        f.write(f"\n![O3 Benchmark](gsm_echo_o3_benchmark.png)\n")
    print(f"  Saved: {report_path}")

    print(f"\n{'='*80}")
    print("DONE")
    print(f"{'='*80}")


if __name__ == "__main__":
    main()
