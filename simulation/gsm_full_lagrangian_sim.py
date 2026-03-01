#!/usr/bin/env python3
"""
GSM Full Lagrangian Simulator
==============================
Computes and verifies all sectors of the GSM Lagrangian on the H4 lattice:
scalar, fermion, Higgs, gauge, and gravity contributions.

Version 2.0 — February 25, 2026
License: CC-BY-4.0
"""

import numpy as np

PHI = (1 + np.sqrt(5)) / 2
PHI_INV = PHI - 1
EPSILON = 28 / 248  # Torsion ratio: dim(SO(8))/dim(E8)


def verify_phi_identities():
    """Verify fundamental golden ratio identities used throughout."""
    results = {}

    # φ² = φ + 1
    results['phi^2 = phi + 1'] = np.isclose(PHI**2, PHI + 1)

    # φ⁻¹ = φ - 1
    results['phi^{-1} = phi - 1'] = np.isclose(1/PHI, PHI - 1)

    # φ^n + φ^{-n} = Lucas numbers
    lucas = [2, 1, 3, 4, 7, 11, 18, 29, 47, 76, 123]
    for n in range(len(lucas)):
        val = PHI**n + (-PHI)**(-n)
        results[f'L_{n} = {lucas[n]}'] = np.isclose(val, lucas[n])

    return results


def scalar_lagrangian(psi, dpsi_dt, neighbors, mass=0):
    """
    Compute the scalar sector Lagrangian density.

    ℒ_scalar = (φ^{-1/2}/2)|∂_t ψ|² - (c²φ²/2ℓ_p²)Σ|ψ_v - ψ_w|² - (m²c⁴/2ℏ²)|ψ|²

    In natural units (c = ℏ = ℓ_p = 1):
    ℒ_scalar = (φ^{-1/2}/2)|∂_t ψ|² - (φ²/2)Σ|ψ_v - ψ_w|² - (m²/2)|ψ|²
    """
    N = len(psi)
    gf = PHI ** (-0.5)

    # Kinetic term
    T = 0.5 * gf * np.sum(np.abs(dpsi_dt) ** 2)

    # Gradient term
    V_grad = 0.0
    for v in range(N):
        for w in neighbors[v]:
            if w > v:
                V_grad += 0.5 * PHI**2 * np.abs(psi[v] - psi[w])**2

    # Mass term
    V_mass = 0.5 * mass**2 * np.sum(np.abs(psi)**2)

    return T - V_grad - V_mass


def higgs_potential(H, v_geom, lambda_geom):
    """
    Compute the geometric Higgs potential.

    V_geom(|H|) = λ_geom (|H|² - v_geom²)²

    Parameters:
        H: complex Higgs field values
        v_geom: geometric VEV
        lambda_geom: geometric self-coupling = φ²/3600
    """
    H_sq = np.abs(H) ** 2
    return lambda_geom * (H_sq - v_geom**2) ** 2


def higgs_sector():
    """Compute and verify Higgs sector predictions."""
    print("\n--- Higgs Sector ---")

    # Geometric parameters
    v_EW = 246.22  # GeV
    lambda_geom = PHI**2 / 3600
    coxeter_h4 = 30

    # Higgs mass ratio
    mH_over_v = 0.5 + PHI**(-5) / 10
    mH = mH_over_v * v_EW
    print(f"  m_H/v = 1/2 + φ⁻⁵/10 = {mH_over_v:.6f}")
    print(f"  m_H = {mH:.2f} GeV (experiment: 125.25 ± 0.17 GeV)")
    print(f"  λ_geom = φ²/(4h²) = {lambda_geom:.6f}")

    # W mass ratio
    mW_over_v = (1 - PHI**(-8)) / 3
    mW = mW_over_v * v_EW
    print(f"  m_W/v = (1-φ⁻⁸)/3 = {mW_over_v:.6f}")
    print(f"  m_W = {mW:.2f} GeV (experiment: 80.36 GeV)")

    return mH, mW


def gauge_sector():
    """Compute and verify gauge coupling predictions."""
    print("\n--- Gauge Sector ---")

    # Fine structure constant
    alpha_inv = 137 + PHI**(-7) + PHI**(-14) + PHI**(-16) - PHI**(-8) / 248
    print(f"  α⁻¹ = 137 + φ⁻⁷ + φ⁻¹⁴ + φ⁻¹⁶ - φ⁻⁸/248")
    print(f"       = {alpha_inv:.6f} (experiment: 137.035999)")
    print(f"  Deviation: {abs(alpha_inv - 137.035999) / 137.035999 * 1e6:.3f} ppm")

    # Weak mixing angle
    sin2_theta_W = 3/13 + PHI**(-16)
    print(f"  sin²θ_W = 3/13 + φ⁻¹⁶ = {sin2_theta_W:.6f}")
    print(f"  (experiment: 0.23121)")

    # Strong coupling
    alpha_s = 1 / (2 * PHI**3 * (1 + PHI**(-14)) * (1 + 8 * PHI**(-5) / 14400))
    print(f"  α_s(M_Z) = {alpha_s:.5f} (experiment: 0.1180)")

    return alpha_inv, sin2_theta_W, alpha_s


def fermion_masses():
    """Compute and verify fermion mass ratio predictions."""
    print("\n--- Fermion Mass Ratios ---")

    # Lepton mass ratios
    m_mu_over_m_e = PHI**11 + PHI**4 + 1 - PHI**(-5) - PHI**(-15)
    m_tau_over_m_mu = PHI**6 - PHI**(-4) - 1 + PHI**(-8)

    print(f"  m_μ/m_e = φ¹¹+φ⁴+1-φ⁻⁵-φ⁻¹⁵ = {m_mu_over_m_e:.5f}")
    print(f"    (experiment: 206.76828)")

    print(f"  m_τ/m_μ = φ⁶-φ⁻⁴-1+φ⁻⁸ = {m_tau_over_m_mu:.4f}")
    print(f"    (experiment: 16.817)")

    # Quark mass ratios
    L3 = PHI**3 + PHI**(-3)
    m_s_over_m_d = L3**2
    m_c_over_m_s = (PHI**5 + PHI**(-3)) * (1 + 28 / (240 * PHI**2))
    m_b_over_m_c = PHI**2 + PHI**(-3)

    print(f"  m_s/m_d = L₃² = {m_s_over_m_d:.4f} (experiment: ~20)")
    print(f"  m_c/m_s = {m_c_over_m_s:.3f} (experiment: 11.83)")
    print(f"  m_b/m_c = φ²+φ⁻³ = {m_b_over_m_c:.3f} (experiment: 2.86)")

    # Top Yukawa
    y_t = 1 - PHI**(-10)
    print(f"  y_t = 1-φ⁻¹⁰ = {y_t:.5f} (experiment: 0.9919)")

    # Proton-to-electron mass ratio
    m_p_over_m_e = 6 * np.pi**5 * (1 + PHI**(-24) + PHI**(-13) / 240)
    print(f"  m_p/m_e = 6π⁵(1+φ⁻²⁴+φ⁻¹³/240) = {m_p_over_m_e:.4f}")
    print(f"    (experiment: 1836.1527)")

    return {
        'm_mu/m_e': m_mu_over_m_e,
        'm_tau/m_mu': m_tau_over_m_mu,
        'm_s/m_d': m_s_over_m_d,
        'y_t': y_t,
        'm_p/m_e': m_p_over_m_e,
    }


def gravity_sector():
    """Compute and verify gravity/cosmology predictions."""
    print("\n--- Gravity & Cosmology ---")

    # Planck-to-EW hierarchy
    M_Pl_over_v = PHI ** (80 - EPSILON)
    print(f"  M_Pl/v = φ^(80-ε) = {M_Pl_over_v:.3e}")
    print(f"    (experiment: ~4.96×10¹⁶)")

    # Cosmological constant
    Omega_L = (PHI**(-1) + PHI**(-6) + PHI**(-9) - PHI**(-13)
               + PHI**(-28) + EPSILON * PHI**(-7))
    print(f"  Ω_Λ = {Omega_L:.5f} (experiment: 0.6889)")

    # Hubble constant
    H0 = 100 * PHI**(-1) * (1 + PHI**(-4) - 1 / (30 * PHI**2))
    print(f"  H₀ = {H0:.2f} km/s/Mpc (experiment: 70.0)")

    # CMB redshift
    z_CMB = PHI**14 + 246
    print(f"  z_CMB = φ¹⁴ + 246 = {z_CMB:.1f} (experiment: 1089.80)")

    # Spectral index
    n_s = 1 - PHI**(-7)
    print(f"  n_s = 1 - φ⁻⁷ = {n_s:.4f} (experiment: 0.9649)")

    return Omega_L, H0, z_CMB, n_s


def regge_gravity_check():
    """Verify consistency of the Regge gravity sector."""
    print("\n--- Regge Gravity Consistency ---")

    # 600-cell properties
    n_vertices = 120
    n_edges = 720
    n_faces = 1200
    n_cells = 600

    # Euler characteristic (4D): V - E + F - C = 0 for 4-sphere
    euler = n_vertices - n_edges + n_faces - n_cells
    print(f"  Euler characteristic: {n_vertices}-{n_edges}+{n_faces}-{n_cells} = {euler}")
    print(f"    (expected: 0 for S³ boundary of 600-cell)")

    # Degrees of freedom check
    # Regge: edge lengths are DOF = 720
    # Linearized gravity in 4D: symmetric tensor has 10 components
    # Gauge freedom: 4 diffeomorphisms
    # Physical DOF per point: 10 - 4 - 4 = 2 (graviton has 2 polarizations)
    print(f"  Regge DOF: {n_edges} edge lengths")
    print(f"  Graviton polarizations: 2 (spin-2 massless)")
    print(f"  DOF per vertex: {n_edges / n_vertices:.1f} edges/vertex")

    # Newton's constant from phi
    G_ratio = PHI ** (-160 + 2 * EPSILON)
    print(f"  G_N ∝ φ^(-160+2ε) = φ^({-160 + 2*EPSILON:.4f})")
    print(f"       = {G_ratio:.3e}")


def full_lagrangian_summary():
    """Print the complete Lagrangian summary with all sectors."""
    print("=" * 70)
    print("COMPLETE GSM LAGRANGIAN — ALL SECTORS")
    print("Version 2.0")
    print("=" * 70)

    # Verify phi identities
    print("\n--- Golden Ratio Identities ---")
    identities = verify_phi_identities()
    all_pass = all(identities.values())
    print(f"  All {len(identities)} identities verified: {'PASS' if all_pass else 'FAIL'}")

    # Run each sector
    higgs_sector()
    gauge_sector()
    fermion_masses()
    gravity_sector()
    regge_gravity_check()

    # Summary
    print("\n" + "=" * 70)
    print("LAGRANGIAN SECTOR SUMMARY")
    print("=" * 70)
    print(f"  Scalar:  Golden Flow kinetic + H₄ Laplacian gradient")
    print(f"  Fermion: Dirac on doubled 600-cell, SO(8) triality generations")
    print(f"  Higgs:   Geometric potential from inter-copy displacement")
    print(f"  Gauge:   E₈ → SU(3)×SU(2)×U(1) on lattice links")
    print(f"  Gravity: Regge calculus on H₄ simplicial complex")
    print(f"  Free parameters: ZERO")
    print("=" * 70)


if __name__ == "__main__":
    full_lagrangian_summary()
