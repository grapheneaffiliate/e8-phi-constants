#!/usr/bin/env python3
"""
GSM Gravitational Wave Echo Simulator
=======================================
Simulates GW echoes with exact φ-commensurate delays, φ⁻ᵏ damping,
and 72° polarization rotations predicted by the Geometric Standard Model.

Version 2.3 — February 25, 2026
License: CC-BY-4.0
"""

import numpy as np

PHI = (1 + np.sqrt(5)) / 2
PHI_INV = PHI - 1

# Physical constants
G_SI = 6.67430e-11      # m³/(kg·s²)
C_SI = 2.99792458e8     # m/s
M_SUN = 1.98892e30      # kg


def echo_delay(k, M_remnant_solar):
    """
    Compute the k-th echo time delay.

    Δt_k = φ^{k+1} × 2GM/c³

    Args:
        k: echo number (1, 2, 3, ...)
        M_remnant_solar: remnant mass in solar masses

    Returns:
        delay in seconds
    """
    t_M = 2 * G_SI * M_remnant_solar * M_SUN / C_SI**3
    return PHI**(k + 1) * t_M


def echo_amplitude(k):
    """
    Compute the k-th echo amplitude factor.

    A_k = φ^{-k}
    """
    return PHI**(-k)


def echo_polarization_angle(k):
    """
    Compute the k-th echo polarization rotation angle.

    θ_k = k × 72° + 36°/φ^k

    Returns angle in degrees.
    """
    return k * 72.0 + 36.0 / PHI**k


def polarization_rotation_matrix(theta_deg):
    """
    Compute the 2×2 polarization rotation matrix for GW.

    For spin-2 waves, the rotation is at 2θ:
    R(θ) = [[cos(2θ), -sin(2θ)],
            [sin(2θ),  cos(2θ)]]
    """
    theta_rad = np.radians(2 * theta_deg)  # Factor 2 for spin-2
    return np.array([
        [np.cos(theta_rad), -np.sin(theta_rad)],
        [np.sin(theta_rad),  np.cos(theta_rad)]
    ])


def ringdown_waveform(t, f_qnm, tau_qnm, A0=1.0, phi0=0.0):
    """
    Generate a quasi-normal mode ringdown waveform.

    h(t) = A0 × exp(-t/τ) × cos(2πf·t + φ₀)    for t ≥ 0
    h(t) = 0                                       for t < 0
    """
    h = np.zeros_like(t)
    mask = t >= 0
    h[mask] = A0 * np.exp(-t[mask] / tau_qnm) * np.cos(2 * np.pi * f_qnm * t[mask] + phi0)
    return h


def generate_echo_waveform(t, M_remnant_solar, f_qnm, tau_qnm, K_max=10,
                            A0=1.0):
    """
    Generate the complete GSM echo waveform.

    h(t) = h_ringdown(t) + Σ_{k=1}^{K} A_k × R(θ_k) × h_echo(t - Δt_k)

    Args:
        t: time array (seconds), with t=0 at merger
        M_remnant_solar: remnant mass in solar masses
        f_qnm: quasi-normal mode frequency (Hz)
        tau_qnm: QNM damping time (seconds)
        K_max: maximum number of echoes
        A0: initial amplitude

    Returns:
        h_plus: plus polarization
        h_cross: cross polarization
        echo_info: dict with echo parameters
    """
    # Ringdown waveform (plus polarization; cross is π/2 phase-shifted)
    h_ring_plus = ringdown_waveform(t, f_qnm, tau_qnm, A0)
    h_ring_cross = ringdown_waveform(t, f_qnm, tau_qnm, A0, phi0=np.pi/2)

    h_plus = h_ring_plus.copy()
    h_cross = h_ring_cross.copy()

    echo_info = {
        'delays': [],
        'amplitudes': [],
        'pol_angles': [],
        'snr_relative': [],
    }

    for k in range(1, K_max + 1):
        dt_k = echo_delay(k, M_remnant_solar)
        A_k = echo_amplitude(k)
        theta_k = echo_polarization_angle(k)

        # Rotation matrix
        R = polarization_rotation_matrix(theta_k)

        # Echo waveform (time-shifted ringdown)
        h_echo_plus = A_k * ringdown_waveform(t - dt_k, f_qnm, tau_qnm, A0)
        h_echo_cross = A_k * ringdown_waveform(t - dt_k, f_qnm, tau_qnm, A0,
                                                  phi0=np.pi/2)

        # Apply polarization rotation
        h_rotated = R @ np.array([h_echo_plus, h_echo_cross])

        h_plus += h_rotated[0]
        h_cross += h_rotated[1]

        echo_info['delays'].append(dt_k)
        echo_info['amplitudes'].append(A_k)
        echo_info['pol_angles'].append(theta_k)
        echo_info['snr_relative'].append(A_k)

    return h_plus, h_cross, echo_info


def print_echo_table(M_remnant_solar, K_max=10):
    """Print a detailed table of echo parameters."""
    t_M = 2 * G_SI * M_remnant_solar * M_SUN / C_SI**3

    print(f"\n  Remnant mass: {M_remnant_solar:.1f} M☉")
    print(f"  2GM/c³ = {t_M*1000:.4f} ms")
    print(f"\n  {'Echo k':>8} | {'Delay Δt_k':>12} | {'Amplitude':>10} | "
          f"{'Pol angle':>10} | {'Delay ratio':>12}")
    print(f"  {'-'*8}-+-{'-'*12}-+-{'-'*10}-+-{'-'*10}-+-{'-'*12}")

    prev_delay = None
    for k in range(1, K_max + 1):
        dt = echo_delay(k, M_remnant_solar)
        A = echo_amplitude(k)
        theta = echo_polarization_angle(k)
        ratio = dt / prev_delay if prev_delay else float('nan')

        print(f"  {k:>8} | {dt*1000:>10.4f} ms | {A:>10.6f} | "
              f"{theta:>9.2f}° | {ratio:>12.6f}")
        prev_delay = dt

    print(f"\n  Expected delay ratio: φ = {PHI:.6f}")
    print(f"  Expected amplitude ratio: φ⁻¹ = {PHI_INV:.6f}")
    print(f"  Expected base polarization step: 72° = 360°/5")


def energy_budget(K_max=20):
    """Compute the total energy in echoes vs ringdown."""
    print("\n--- Energy Budget ---")

    # Total echo energy (proportional to Σ A_k²)
    total_echo_energy = sum(PHI**(-2*k) for k in range(1, K_max + 1))
    # Geometric series: Σ_{k=1}^∞ φ^{-2k} = φ⁻²/(1-φ⁻²) = 1/(φ²-1) = 1/φ
    analytical_total = 1 / PHI

    print(f"  Ringdown energy (normalized): 1.000")
    print(f"  Total echo energy (K={K_max}): {total_echo_energy:.6f}")
    print(f"  Analytical (K→∞): 1/φ = {analytical_total:.6f}")
    print(f"  Echo/ringdown ratio: {total_echo_energy:.4f}")
    print(f"  Energy in first 5 echoes: {sum(PHI**(-2*k) for k in range(1,6)):.4f}")


def detection_forecast():
    """Estimate detection prospects for LIGO O4/O5."""
    print("\n--- Detection Forecast ---")

    # GW150914-like event
    M_remnant = 62  # solar masses
    d_Mpc = 410     # distance in Mpc
    snr_ringdown = 8  # approximate ringdown SNR

    print(f"  Reference: GW150914-like event")
    print(f"  M_remnant = {M_remnant} M☉, d = {d_Mpc} Mpc")
    print(f"  Ringdown SNR ≈ {snr_ringdown}")

    for k in range(1, 6):
        snr_echo = snr_ringdown * echo_amplitude(k)
        print(f"  Echo {k} SNR ≈ {snr_echo:.2f}")

    # Stacking N events
    print(f"\n  Stacking multiple events (SNR ∝ √N):")
    for N in [1, 10, 50, 100]:
        stacked_snr = snr_ringdown * echo_amplitude(1) * np.sqrt(N)
        print(f"    N={N:>3}: combined echo-1 SNR ≈ {stacked_snr:.1f}"
              f" ({'detectable' if stacked_snr > 5 else 'marginal' if stacked_snr > 3 else 'below threshold'})")


def main():
    print("=" * 70)
    print("GSM GRAVITATIONAL WAVE ECHO SIMULATOR")
    print("Version 2.3")
    print("=" * 70)

    # 1. Echo parameter table
    print("\n1. Echo Parameters (30 M☉ remnant)")
    print_echo_table(30.0, K_max=8)

    print("\n   Echo Parameters (62 M☉ remnant, GW150914-like)")
    print_echo_table(62.0, K_max=8)

    # 2. Generate waveform
    print("\n2. Generating GSM echo waveform...")
    M_remnant = 30.0  # solar masses
    f_qnm = 250.0     # Hz (approximate for 30 M☉)
    tau_qnm = 4e-3    # 4 ms damping time

    dt = 1.0 / 4096   # LIGO sample rate
    t = np.arange(-0.1, 0.05, dt)  # 100ms pre-merger to 50ms post

    h_plus, h_cross, echo_info = generate_echo_waveform(
        t, M_remnant, f_qnm, tau_qnm, K_max=5
    )

    print(f"   Sample rate: {1/dt:.0f} Hz")
    print(f"   Duration: {t[-1]-t[0]:.3f} s")
    print(f"   Max |h+|: {np.max(np.abs(h_plus)):.6f}")
    print(f"   Max |h×|: {np.max(np.abs(h_cross)):.6f}")

    # 3. Verify φ-commensurate structure
    print("\n3. Verifying φ-commensurate structure:")
    delays = echo_info['delays']
    for k in range(len(delays) - 1):
        ratio = delays[k+1] / delays[k]
        print(f"   Δt_{k+2}/Δt_{k+1} = {ratio:.10f} (expected φ = {PHI:.10f})")

    amps = echo_info['amplitudes']
    for k in range(len(amps) - 1):
        ratio = amps[k+1] / amps[k]
        print(f"   A_{k+2}/A_{k+1} = {ratio:.10f} (expected φ⁻¹ = {PHI_INV:.10f})")

    # 4. Energy budget
    energy_budget()

    # 5. Detection forecast
    detection_forecast()

    # 6. Falsification criteria
    print("\n6. Falsification Criteria:")
    print(f"   Delay ratio ≠ φ: |Δt_{{k+1}}/Δt_k - φ| > 0.05")
    print(f"   Amplitude ratio ≠ φ⁻¹: |A_{{k+1}}/A_k - φ⁻¹| > 0.1")
    print(f"   Polarization step ≠ 72°: |Δθ - 72°| > 10°")
    print(f"   No echoes with SNR_ringdown > 20 after O5")

    print("\n" + "=" * 70)
    print("GW echo simulation complete.")
    print("Zero-parameter template ready for LIGO matched filtering.")
    print("=" * 70)


if __name__ == "__main__":
    main()
