#!/usr/bin/env python3
"""
GSM LIGO Template Generator
=============================
Generates LIGO-compatible gravitational wave echo templates with exact
φ-commensurate delays, φ⁻ᵏ damping, and 72° polarization rotations.

Outputs waveforms in formats compatible with:
- PyCBC (HDF5 / numpy arrays)
- LALSuite (time-domain arrays)
- GWpy (TimeSeries-compatible)

Version 2.4 — February 25, 2026
License: CC-BY-4.0
"""

import numpy as np
import json
import os

PHI = (1 + np.sqrt(5)) / 2
PHI_INV = PHI - 1

# Physical constants (SI)
G_SI = 6.67430e-11       # m³/(kg·s²)
C_SI = 2.99792458e8      # m/s
M_SUN_KG = 1.98892e30    # kg
MPC_M = 3.08568e22       # meters per Mpc

# LIGO parameters
LIGO_SAMPLE_RATE = 4096   # Hz (standard LIGO sample rate)
LIGO_F_LOW = 20.0         # Hz (low frequency cutoff)
LIGO_F_HIGH = 2048.0      # Hz (Nyquist)


class GSMEchoTemplate:
    """Generator for GSM gravitational wave echo templates."""

    def __init__(self, M_remnant_solar, chi_remnant=0.7, d_Mpc=100.0):
        """
        Initialize the echo template generator.

        Args:
            M_remnant_solar: remnant black hole mass (solar masses)
            chi_remnant: remnant dimensionless spin (0 to 1)
            d_Mpc: luminosity distance in Mpc
        """
        self.M = M_remnant_solar
        self.chi = chi_remnant
        self.d_Mpc = d_Mpc

        # Characteristic time scale
        self.t_M = 2 * G_SI * self.M * M_SUN_KG / C_SI**3

        # QNM frequency and damping (Kerr approximation)
        # Using fits from Berti, Cardoso & Starinets (2009)
        self.f_qnm = self._qnm_frequency()
        self.tau_qnm = self._qnm_damping()

        # Strain amplitude scale
        self.h0 = self._strain_amplitude()

    def _qnm_frequency(self):
        """Quasi-normal mode frequency for the (2,2,0) mode."""
        # Fit: f = (1/2π) × (1 - 0.63(1-χ)^{3/10}) / (2GM/c³)
        f = (1 - 0.63 * (1 - self.chi)**0.3) / (2 * np.pi * self.t_M)
        return f

    def _qnm_damping(self):
        """QNM damping time for the (2,2,0) mode."""
        # Fit: τ = 2(1-χ)^{-9/20} × 2GM/c³
        tau = 2 * (1 - self.chi)**(-0.45) * self.t_M
        return tau

    def _strain_amplitude(self):
        """Estimate strain amplitude at distance d."""
        # h ~ (G M / c² d) × (v/c)²
        # Rough estimate for ringdown amplitude
        d_m = self.d_Mpc * MPC_M
        r_s = 2 * G_SI * self.M * M_SUN_KG / C_SI**2
        return r_s / d_m * 0.1  # ~10% of Schwarzschild radius / distance

    def echo_delay(self, k):
        """k-th echo delay: Δt_k = φ^{k+1} × 2GM/c³"""
        return PHI**(k + 1) * self.t_M

    def echo_amplitude(self, k):
        """k-th echo amplitude: A_k = φ^{-k}"""
        return PHI**(-k)

    def echo_polarization(self, k):
        """k-th echo polarization angle: θ_k = k×72° + 36°/φ^k"""
        return k * 72.0 + 36.0 / PHI**k

    def ringdown(self, t, polarization='plus'):
        """
        Generate ringdown waveform.

        Args:
            t: time array (s), t=0 at merger
            polarization: 'plus' or 'cross'
        """
        phase_offset = 0.0 if polarization == 'plus' else np.pi / 2
        h = np.zeros_like(t)
        mask = t >= 0
        h[mask] = (self.h0 * np.exp(-t[mask] / self.tau_qnm) *
                   np.cos(2 * np.pi * self.f_qnm * t[mask] + phase_offset))
        return h

    def generate(self, duration=1.0, pre_merger=0.5, K_max=10,
                 sample_rate=LIGO_SAMPLE_RATE):
        """
        Generate the complete GSM echo template.

        Args:
            duration: total duration in seconds
            pre_merger: time before merger to include (s)
            K_max: maximum number of echoes
            sample_rate: sample rate in Hz

        Returns:
            t: time array
            h_plus: plus polarization strain
            h_cross: cross polarization strain
            metadata: dict with template parameters
        """
        dt = 1.0 / sample_rate
        t = np.arange(-pre_merger, duration - pre_merger, dt)

        # Ringdown
        h_plus = self.ringdown(t, 'plus')
        h_cross = self.ringdown(t, 'cross')

        # Add echoes
        for k in range(1, K_max + 1):
            delay = self.echo_delay(k)
            amp = self.echo_amplitude(k)
            theta = self.echo_polarization(k)

            # Echo waveform (delayed ringdown)
            h_echo_p = amp * self.ringdown(t - delay, 'plus')
            h_echo_c = amp * self.ringdown(t - delay, 'cross')

            # Polarization rotation (factor 2 for spin-2)
            angle = np.radians(2 * theta)
            cos_a = np.cos(angle)
            sin_a = np.sin(angle)

            h_plus += cos_a * h_echo_p - sin_a * h_echo_c
            h_cross += sin_a * h_echo_p + cos_a * h_echo_c

        metadata = self._build_metadata(K_max, sample_rate, duration)

        return t, h_plus, h_cross, metadata

    def _build_metadata(self, K_max, sample_rate, duration):
        """Build metadata dictionary for the template."""
        metadata = {
            'generator': 'GSM LIGO Template Generator v2.4',
            'model': 'Geometric Standard Model (E8 → H4)',
            'license': 'CC-BY-4.0',
            'parameters': {
                'M_remnant_solar': self.M,
                'chi_remnant': self.chi,
                'd_Mpc': self.d_Mpc,
                'f_qnm_Hz': self.f_qnm,
                'tau_qnm_s': self.tau_qnm,
                'h0': self.h0,
                'K_max': K_max,
                'sample_rate_Hz': sample_rate,
                'duration_s': duration,
            },
            'phi_constants': {
                'golden_ratio': float(PHI),
                'golden_ratio_inv': float(PHI_INV),
                'torsion_ratio': 28 / 248,
            },
            'echo_parameters': {},
            'gsm_predictions': {
                'delay_ratio': 'φ (exact)',
                'amplitude_ratio': 'φ⁻¹ (exact)',
                'polarization_step': '72° + 36°/φ^k',
                'free_parameters': 0,
            }
        }

        for k in range(1, K_max + 1):
            metadata['echo_parameters'][f'echo_{k}'] = {
                'delay_s': self.echo_delay(k),
                'delay_ms': self.echo_delay(k) * 1000,
                'amplitude': self.echo_amplitude(k),
                'polarization_deg': self.echo_polarization(k),
            }

        return metadata

    def save_numpy(self, filename, **kwargs):
        """Save template as numpy .npz file."""
        t, h_plus, h_cross, metadata = self.generate(**kwargs)
        np.savez(
            filename,
            time=t,
            h_plus=h_plus,
            h_cross=h_cross,
            sample_rate=kwargs.get('sample_rate', LIGO_SAMPLE_RATE),
            M_remnant=self.M,
            chi_remnant=self.chi,
            d_Mpc=self.d_Mpc,
        )
        # Save metadata as JSON alongside
        json_file = filename.replace('.npz', '_metadata.json')
        with open(json_file, 'w') as f:
            json.dump(metadata, f, indent=2, default=str)
        return filename, json_file

    def save_ascii(self, filename, **kwargs):
        """Save template as ASCII text file (LALSuite compatible)."""
        t, h_plus, h_cross, metadata = self.generate(**kwargs)
        header = (
            f"# GSM LIGO Echo Template v2.4\n"
            f"# M_remnant = {self.M} M_sun\n"
            f"# chi = {self.chi}\n"
            f"# d = {self.d_Mpc} Mpc\n"
            f"# sample_rate = {kwargs.get('sample_rate', LIGO_SAMPLE_RATE)} Hz\n"
            f"# columns: time(s) h_plus h_cross\n"
        )
        data = np.column_stack([t, h_plus, h_cross])
        np.savetxt(filename, data, header=header, fmt='%.10e')
        return filename


def generate_template_bank(mass_range=(10, 100), n_masses=10,
                            chi_range=(0.0, 0.95), n_spins=5,
                            output_dir='gsm_templates'):
    """
    Generate a bank of GSM echo templates spanning parameter space.

    Args:
        mass_range: (min, max) remnant mass in solar masses
        n_masses: number of mass points
        chi_range: (min, max) dimensionless spin
        n_spins: number of spin points
        output_dir: directory for output files
    """
    os.makedirs(output_dir, exist_ok=True)

    masses = np.linspace(mass_range[0], mass_range[1], n_masses)
    spins = np.linspace(chi_range[0], chi_range[1], n_spins)

    bank_info = []
    total = n_masses * n_spins

    print(f"Generating template bank: {total} templates")
    print(f"  Mass range: {mass_range[0]}-{mass_range[1]} M☉ ({n_masses} points)")
    print(f"  Spin range: {chi_range[0]}-{chi_range[1]} ({n_spins} points)")

    idx = 0
    for M in masses:
        for chi in spins:
            idx += 1
            gen = GSMEchoTemplate(M, chi)

            filename = f"gsm_echo_M{M:.1f}_chi{chi:.2f}"
            filepath = os.path.join(output_dir, filename)

            # Adjust duration based on mass (heavier → longer echoes)
            duration = max(0.5, 10 * gen.echo_delay(5))

            t, h_plus, h_cross, metadata = gen.generate(
                duration=duration, K_max=10
            )

            bank_info.append({
                'M': M, 'chi': chi,
                'f_qnm': gen.f_qnm,
                'tau_qnm': gen.tau_qnm,
                'echo_1_delay_ms': gen.echo_delay(1) * 1000,
                'filename': filename,
            })

            if idx % 10 == 0 or idx == total:
                print(f"  [{idx}/{total}] M={M:.1f} χ={chi:.2f} "
                      f"f_qnm={gen.f_qnm:.1f}Hz Δt₁={gen.echo_delay(1)*1000:.3f}ms")

    # Save bank catalog
    catalog_file = os.path.join(output_dir, 'template_bank_catalog.json')
    with open(catalog_file, 'w') as f:
        json.dump({
            'generator': 'GSM Template Bank v2.4',
            'n_templates': total,
            'mass_range': list(mass_range),
            'spin_range': list(chi_range),
            'templates': bank_info,
        }, f, indent=2, default=str)

    print(f"\nTemplate bank catalog: {catalog_file}")
    return bank_info


def main():
    print("=" * 70)
    print("GSM LIGO TEMPLATE GENERATOR")
    print("Version 2.4 — Zero-Parameter GW Echo Templates")
    print("=" * 70)

    # Example 1: GW150914-like event
    print("\n1. GW150914-like template (62 M☉, χ=0.67, 410 Mpc)")
    gen = GSMEchoTemplate(M_remnant_solar=62, chi_remnant=0.67, d_Mpc=410)

    print(f"   f_QNM = {gen.f_qnm:.1f} Hz")
    print(f"   τ_QNM = {gen.tau_qnm*1000:.3f} ms")
    print(f"   h₀ = {gen.h0:.3e}")
    print(f"   2GM/c³ = {gen.t_M*1000:.4f} ms")

    print(f"\n   Echo table:")
    for k in range(1, 8):
        print(f"     k={k}: Δt={gen.echo_delay(k)*1000:.3f}ms, "
              f"A={gen.echo_amplitude(k):.4f}, "
              f"θ={gen.echo_polarization(k):.1f}°")

    # Generate waveform
    t, h_plus, h_cross, metadata = gen.generate(
        duration=0.5, pre_merger=0.1, K_max=10
    )

    print(f"\n   Waveform generated:")
    print(f"     Duration: {t[-1]-t[0]:.3f} s ({len(t)} samples)")
    print(f"     Max |h+|: {np.max(np.abs(h_plus)):.3e}")
    print(f"     Max |h×|: {np.max(np.abs(h_cross)):.3e}")

    # Example 2: Lighter BBH
    print("\n2. Light BBH template (15 M☉, χ=0.5, 200 Mpc)")
    gen2 = GSMEchoTemplate(M_remnant_solar=15, chi_remnant=0.5, d_Mpc=200)
    print(f"   f_QNM = {gen2.f_qnm:.1f} Hz")
    print(f"   First echo delay: {gen2.echo_delay(1)*1000:.4f} ms")

    # Verify φ structure
    print("\n3. φ-Structure Verification:")
    for k in range(1, 6):
        ratio = gen.echo_delay(k+1) / gen.echo_delay(k)
        print(f"   Δt_{k+1}/Δt_{k} = {ratio:.12f} (φ = {PHI:.12f})")

    # Template bank (small example)
    print("\n4. Template Bank Generation (demo)")
    print("   Generating a small demo bank...")
    bank = generate_template_bank(
        mass_range=(20, 80), n_masses=4,
        chi_range=(0.2, 0.8), n_spins=3,
        output_dir='/tmp/gsm_templates_demo'
    )

    print(f"\n   Generated {len(bank)} templates")

    # Summary
    print("\n" + "=" * 70)
    print("TEMPLATE GENERATOR SUMMARY")
    print("=" * 70)
    print(f"  Echo delays:       Δt_k = φ^(k+1) × 2GM/c³")
    print(f"  Echo amplitudes:   A_k = φ^(-k)")
    print(f"  Polarization:      θ_k = k×72° + 36°/φ^k")
    print(f"  Free parameters:   0")
    print(f"  Output formats:    numpy (.npz), ASCII, JSON metadata")
    print(f"  Compatible with:   PyCBC, LALSuite, GWpy")
    print("=" * 70)


if __name__ == "__main__":
    main()
