#!/usr/bin/env python3
"""
STANDALONE PERMUTATION TEST for GSM Phi-Constants
===================================================
Recomputes all 58 constants from phi, pi, and E8 data internally.
Excludes tier-P (S_CHSH, r_tensor) -> 56 validated constants.
Runs 100,000 random permutations to test whether the derived->experimental
mapping is statistically significant vs random assignment.

No imports from gsm_solver.py.
"""

import math
import numpy as np
import time

# =============================================================================
# 1. FUNDAMENTAL MATHEMATICAL INPUTS
# =============================================================================

PHI = (1 + np.sqrt(5)) / 2
PHI_INV = PHI - 1
PI = np.pi
EPSILON = 28 / 248           # dim(SO(8)) / dim(E8)
KISSING = 240                 # E8 kissing number
ANCHOR_ALPHA = 137
ANCHOR_WEAK = 3 / 13
ANCHOR_CKM = 264
ANCHOR_COXETER = 30
ANCHOR_H4_ORDER = 14400

# Lie algebra data (dimension, rank, roots, coxeter_number)
E8_dim, E8_rank, E8_roots, E8_cox = 248, 8, 240, 30
E7_dim, E7_rank, E7_roots, E7_cox = 133, 7, 126, 18
E6_dim, E6_rank, E6_roots, E6_cox = 78, 6, 72, 12
F4_dim, F4_rank, F4_roots, F4_cox = 52, 4, 48, 12
G2_dim, G2_rank, G2_roots, G2_cox = 14, 2, 12, 6
SO8_dim, SO8_rank, SO8_roots, SO8_cox = 28, 4, 24, 6
SU3_dim, SU3_rank, SU3_roots, SU3_cox = 8, 2, 6, 3
SU2_dim, SU2_rank, SU2_roots, SU2_cox = 3, 1, 2, 2

# Hyperbolic Lucas
L3 = PHI**3 + PHI**(-3)  # = sqrt(20)

m_e_eV = 510998.95  # electron mass in eV (for neutrino calc)
M_Pl_GeV = 1.22089e19  # Full Planck mass in GeV
hbar_c_fm = 0.197327    # GeV * fm

# =============================================================================
# 2. DERIVE ALL 58 CONSTANTS (same formulas as gsm_solver.py)
# =============================================================================

derived = {}

# 1. Fine Structure Constant (inverse)
derived['alpha_inv'] = (ANCHOR_ALPHA + PHI**(-7) + PHI**(-14) + PHI**(-16)
                        - PHI**(-8) / 248 + (248 / KISSING) * PHI**(-26))

# 2. Weak Mixing Angle
derived['sin2_theta_w'] = ANCHOR_WEAK + PHI**(-16)

# 3. Strong Coupling
derived['alpha_s'] = 1.0 / (2 * PHI**3 * (1 + PHI**(-14)) * (1 + 8 * PHI**(-5) / ANCHOR_H4_ORDER))

# 4. Muon/Electron Mass Ratio
derived['mu_e_ratio'] = PHI**11 + PHI**4 + 1 - PHI**(-5) - (228 / 248) * PHI**(-15)

# 5. Tau/Muon Mass Ratio
derived['tau_mu_ratio'] = PHI**6 - PHI**(-4) - 1 + (7 / E8_rank) * PHI**(-8) + PHI**(-18) / 248

# 6. Strange/Down Ratio
derived['ms_md_ratio'] = L3**2

# 7. Charm/Strange Ratio
derived['mc_ms_ratio'] = (PHI**5 + PHI**(-3)) * (1 + 28 / (KISSING * PHI**2))

# 8. Bottom/Charm Ratio
derived['mb_mc_ratio'] = PHI**2 + PHI**(-3)

# 9. Proton/Electron Mass Ratio
vol_s5 = 6 * PI**5
derived['mp_me_ratio'] = vol_s5 * (1 + PHI**(-24) + PHI**(-13) / KISSING
                                    + PHI**(-17) / KISSING + PHI**(-33) / E8_rank)

# 10. Top Yukawa Coupling
derived['y_t'] = 1 - PHI**(-10)

# 11. Higgs/VEV Ratio
derived['mH_v'] = 0.5 + PHI**(-5) / 10

# 12. W/VEV Ratio
derived['mW_v'] = (1 - PHI**(-8)) / 3 + (5 / 13) * PHI**(-16)

# 13. Cabibbo Angle
derived['sin_theta_C'] = ((PHI**(-1) + PHI**(-6)) / 3) * (1 + 8 * PHI**(-6) / 248)

# 14. Jarlskog Invariant
derived['J_CKM'] = PHI**(-10) / ANCHOR_CKM

# 15. V_cb
derived['V_cb'] = (PHI**(-8) + PHI**(-15)) * (PHI**2 / np.sqrt(2)) * (1 + 1 / KISSING)

# 16. V_ub
derived['V_ub'] = 2 * PHI**(-7) / 19

# 17. PMNS Solar Angle
derived['theta_12'] = np.degrees(np.arctan(PHI**(-1) + 2 * PHI**(-8)))

# 18. PMNS Atmospheric Angle
derived['theta_23'] = np.degrees(np.arcsin(np.sqrt((1 + PHI**(-4)) / 2)))

# 19. PMNS Reactor Angle
derived['theta_13'] = np.degrees(np.arcsin(PHI**(-4) + PHI**(-12)))

# 20. PMNS CP Phase
derived['delta_CP'] = 180 + np.degrees(np.arctan(PHI**(-2) - PHI**(-5)))

# 21. Sum of Neutrino Masses (meV)
derived['Sigma_m_nu'] = m_e_eV * PHI**(-34) * (1 + EPSILON * PHI**3) * 1000

# 22. Dark Energy Fraction
derived['Omega_Lambda'] = (PHI**(-1) + PHI**(-6) + PHI**(-9) - PHI**(-13)
                           + PHI**(-28) + EPSILON * PHI**(-7))

# 23. CMB Redshift
derived['z_CMB'] = PHI**14 + 246 + (E8_dim / SO8_dim) * PHI**(-5)

# 24. Hubble Constant
derived['H0'] = 100 * PHI**(-1) * (1 + PHI**(-4) - 1 / (ANCHOR_COXETER * PHI**2))

# 25. Spectral Index
derived['n_s'] = 1 - PHI**(-7)

# 26. CHSH Bell Bound (tier-P, will be excluded)
derived['S_CHSH'] = 4 - PHI

# --- PROMOTED DISCOVERIES ---

# 27. Top/VEV Mass Ratio
derived['mt_v'] = F4_dim / F4_roots - PHI**(-2)

# 28. Baryon Fraction
derived['Omega_b'] = 1.0 / 12 - PHI**(-7)

# 29. Effective Neutrino Species
derived['N_eff'] = E8_roots / E6_dim - PHI**(-7) + EPSILON * PHI**(-9)

# 30. Z/VEV Mass Ratio
derived['mZ_v'] = E6_dim / E8_dim + PHI**(-6) + (7 / E8_cox) * PHI**(-16)

# 31. Dark Matter Fraction
derived['Omega_DM'] = 1.0 / E8_rank + PHI**(-4) - EPSILON * PHI**(-5)

# 32. CMB Temperature
derived['T_CMB'] = E6_dim / E8_cox + PHI**(-6) + EPSILON * PHI**(-1)

# 33. Neutron-Proton Mass Diff
derived['n_p_mass_diff'] = E8_rank / 3.0 - PHI**(-4) + EPSILON * PHI**(-5)

# 34. Baryon Asymmetry
derived['eta_B'] = ANCHOR_WEAK * PHI**(-34) * PHI**(-7) * (1 - PHI**(-8))

# --- v4.0: ABSOLUTE MASSES & HIERARCHY ---

# Hierarchy
hierarchy_exp = 2 * (E8_cox + E8_rank + 2)  # = 80
sub_torsion = (24 / E8_dim) * PHI**(-12)
derived['M_Pl_v'] = PHI**(hierarchy_exp - EPSILON - sub_torsion)

# Higgs VEV (GeV)
v = M_Pl_GeV / derived['M_Pl_v']
derived['v_GeV'] = v

# Top quark mass
m_t_val = derived['mt_v'] * v
derived['m_t_GeV'] = m_t_val

# W boson mass
derived['m_W_GeV'] = derived['mW_v'] * v

# Z boson mass
derived['m_Z_GeV'] = derived['mZ_v'] * v

# Higgs boson mass
derived['m_H_GeV'] = derived['mH_v'] * v

# Electron mass
me_over_v = PHI**(-27) * (1 - PHI**(-5) + EPSILON * PHI**(-9) + 3 * PHI**(-20))
m_e_val = me_over_v * v
derived['m_e_GeV'] = m_e_val

# Muon mass
derived['m_mu_GeV'] = m_e_val * derived['mu_e_ratio']

# Tau mass
derived['m_tau_GeV'] = derived['m_mu_GeV'] * derived['tau_mu_ratio']

# Quark masses (chain from top via ratios + QCD corrections)
alpha_s_MZ = derived['alpha_s']
M_Z_val = derived['m_Z_GeV']

def alpha_s_at(mu, nf):
    beta0 = (33 - 2 * nf) / 3
    return alpha_s_MZ / (1 + (beta0 / (2 * np.pi)) * alpha_s_MZ * np.log(mu / M_Z_val))

def pole_to_msbar_factor(mu, nf):
    a_s = alpha_s_at(mu, nf)
    x = a_s / np.pi
    K2 = {3: 12.4, 4: 10.2, 5: 8.0}.get(nf, 10.2)
    return 1 + (4.0 / 3) * x + K2 * x**2

mt_mb_ratio = F4_roots - PHI**4
m_b_val = m_t_val / mt_mb_ratio
derived['m_b_GeV'] = m_b_val

m_c_chain = m_b_val / derived['mb_mc_ratio']
m_s_chain = m_c_chain / derived['mc_ms_ratio']
m_d_chain = m_s_chain / derived['ms_md_ratio']
mu_md_val = PHI**(-1) - PHI**(-5)
m_u_chain = m_d_chain * mu_md_val

# QCD corrections
a_s_mc = alpha_s_at(1.3, 4)
R_c = 1 + (4.0 / 3) * (a_s_mc / np.pi)
m_c_val = m_c_chain / R_c
derived['m_c_GeV'] = m_c_val

R_light = pole_to_msbar_factor(2.0, 3)
derived['m_s_GeV'] = m_s_chain / R_light
derived['m_d_GeV'] = m_d_chain / R_light
derived['m_u_GeV'] = m_u_chain / R_light

# W/Z mass ratio
derived['mW_mZ'] = derived['m_W_GeV'] / derived['m_Z_GeV']

# Fermi constant
derived['G_F_GeV2'] = 1.0 / (np.sqrt(2) * v**2)

# Rydberg energy (eV)
alpha_val = 1.0 / derived['alpha_inv']
derived['Rydberg_eV'] = m_e_val * 1e9 * alpha_val**2 / 2

# Neutrino mass splittings
dm_ratio = E8_cox + PHI**2
sigma_eV = derived['Sigma_m_nu'] / 1000  # meV -> eV
sqrt_dm21 = sigma_eV / (np.sqrt(dm_ratio) + 1 + 0.01)
derived['dm21_sq'] = sqrt_dm21**2
derived['dm32_sq'] = dm_ratio * derived['dm21_sq']

# Proton charge radius
m_p_GeV = m_e_val * derived['mp_me_ratio']
derived['r_p_fm'] = hbar_c_fm / m_p_GeV * (E8_rank / 2)

# Pion/electron mass ratio
derived['mpi_me'] = E8_roots + E8_cox + PHI**2 + PHI**(-1) - PHI**(-7)

# Deuteron binding/proton mass
derived['Bd_mp'] = PHI**(-7) * (1 + PHI**(-7)) / E8_cox

# Tensor-to-scalar ratio (tier-P, will be excluded)
derived['r_tensor'] = 16 * PHI**(-14) / (2 * E8_cox)

# sigma_8
derived['sigma_8'] = E6_dim / (E8_rank * 12) - EPSILON * PHI**(-9)

# =============================================================================
# 3. EXPERIMENTAL VALUES WITH UNCERTAINTIES
# =============================================================================

EXPERIMENT = {
    'alpha_inv':     (137.035999177, 0.000000021),
    'sin2_theta_w':  (0.23121,       0.00004),
    'alpha_s':       (0.1180,        0.0009),
    'mu_e_ratio':    (206.7682830,   0.0000046),
    'tau_mu_ratio':  (16.8170,       0.0010),
    'ms_md_ratio':   (20.0,          2.0),
    'mc_ms_ratio':   (11.83,         0.20),
    'mb_mc_ratio':   (2.86,          0.10),
    'mp_me_ratio':   (1836.15267343, 0.00000011),
    'y_t':           (0.9919,        0.0025),
    'mH_v':          (0.5087,        0.0007),
    'mW_v':          (0.3264,        0.0002),
    'sin_theta_C':   (0.2250,        0.0008),
    'J_CKM':         (3.08e-5,       0.15e-5),
    'V_cb':          (0.0410,        0.0011),
    'V_ub':          (0.00361,       0.00011),
    'theta_12':      (33.44,         0.77),
    'theta_23':      (49.2,          1.0),
    'theta_13':      (8.57,          0.12),
    'delta_CP':      (197.0,         25.0),
    'Sigma_m_nu':    (59.0,          10.0),
    'Omega_Lambda':  (0.6889,        0.0056),
    'z_CMB':         (1089.80,       0.21),
    'H0':            (70.0,          2.0),
    'n_s':           (0.9649,        0.0042),
    'S_CHSH':        (2.828,         0.001),       # tier-P EXCLUDED
    'mt_v':          (0.7014,        0.0025),
    'Omega_b':       (0.0489,        0.0003),
    'N_eff':         (3.044,         0.10),
    'mZ_v':          (0.3702,        0.0001),
    'Omega_DM':      (0.2607,        0.0020),
    'T_CMB':         (2.7255,        0.0006),
    'n_p_mass_diff': (2.53091,       0.00023),
    'eta_B':         (6.1e-10,       0.04e-10),
    'm_e_GeV':       (0.000510999,   0.000001),
    'm_mu_GeV':      (0.105658,      0.0001),
    'm_tau_GeV':     (1.77686,       0.00012),
    'm_u_GeV':       (0.00216,       0.00049),
    'm_d_GeV':       (0.00467,       0.00048),
    'm_s_GeV':       (0.0934,        0.0086),
    'm_c_GeV':       (1.27,          0.02),
    'm_b_GeV':       (4.18,          0.03),
    'm_t_GeV':       (172.69,        0.30),
    'm_W_GeV':       (80.3692,       0.0133),
    'm_Z_GeV':       (91.1876,       0.01),
    'm_H_GeV':       (125.25,        0.17),
    'v_GeV':         (246.22,        0.05),
    'M_Pl_v':        (4.959e16,      0.001e16),
    'dm21_sq':       (7.53e-5,       0.50e-5),
    'dm32_sq':       (2.453e-3,      0.10e-3),
    'r_p_fm':        (0.8414,        0.0019),
    'mpi_me':        (273.13,        0.10),
    'Bd_mp':         (0.001188,      0.000001),
    'mW_mZ':         (0.88145,       0.00013),
    'r_tensor':      (0.0,           0.036),       # tier-P EXCLUDED
    'sigma_8':       (0.8111,        0.0060),
    'G_F_GeV2':      (1.1663788e-5,  0.0001e-5),
    'Rydberg_eV':    (13.605693,     0.001),
}

# =============================================================================
# 4. EXCLUDE TIER-P (S_CHSH, r_tensor) -> 56 CONSTANTS
# =============================================================================

EXCLUDE = {'S_CHSH', 'r_tensor'}

keys = [k for k in derived if k not in EXCLUDE and k in EXPERIMENT]
assert len(keys) == 56, f"Expected 56 constants, got {len(keys)}"

derived_vals = np.array([derived[k] for k in keys])
exp_vals = np.array([EXPERIMENT[k][0] for k in keys])
unc_vals = np.array([EXPERIMENT[k][1] for k in keys])

print("=" * 72)
print("  GSM PERMUTATION TEST -- 56 VALIDATED CONSTANTS")
print("=" * 72)
print(f"\n  Constants included: {len(keys)}")
print(f"  Constants excluded (tier-P): {sorted(EXCLUDE)}")
print()

# Print each constant's derived vs experimental value
print(f"  {'Key':>20s}  {'Derived':>15s}  {'Experimental':>15s}  {'Unc':>12s}  {'Sigma':>8s}")
print(f"  {'-'*20}  {'-'*15}  {'-'*15}  {'-'*12}  {'-'*8}")
for k in keys:
    d = derived[k]
    e, u = EXPERIMENT[k]
    sigma = (d - e) / u
    print(f"  {k:>20s}  {d:15.7g}  {e:15.7g}  {u:12.4g}  {sigma:+8.3f}")

# =============================================================================
# 5. COMPUTE ACTUAL CHI^2 AND LOG-CHI^2
# =============================================================================

def compute_chi2(d_vals, e_vals, u_vals):
    """Standard chi^2 = sum((derived - exp) / unc)^2"""
    return np.sum(((d_vals - e_vals) / u_vals)**2)

def compute_log_chi2(d_vals, e_vals):
    """Log chi^2 = sum(log10(derived / exp))^2"""
    # Protect against sign issues (all should be positive but be safe)
    with np.errstate(divide='ignore', invalid='ignore'):
        ratios = np.abs(d_vals) / np.abs(e_vals)
        ratios = np.where(ratios > 0, ratios, 1e-30)
    return np.sum(np.log10(ratios)**2)

actual_chi2 = compute_chi2(derived_vals, exp_vals, unc_vals)
actual_log_chi2 = compute_log_chi2(derived_vals, exp_vals)

print(f"\n  ACTUAL METRICS:")
print(f"    chi^2           = {actual_chi2:.4f}")
print(f"    chi^2 / N       = {actual_chi2 / len(keys):.4f}")
print(f"    log-chi^2       = {actual_log_chi2:.6f}")
print(f"    log-chi^2 / N   = {actual_log_chi2 / len(keys):.6f}")

# =============================================================================
# 6. RUN 100,000 RANDOM PERMUTATIONS
# =============================================================================

N_PERM = 100_000
rng = np.random.default_rng(seed=42)

perm_chi2 = np.zeros(N_PERM)
perm_log_chi2 = np.zeros(N_PERM)

print(f"\n  Running {N_PERM:,} random permutations...")
t0 = time.time()

for i in range(N_PERM):
    # Shuffle the derived values -> random mapping to experimental targets
    perm_idx = rng.permutation(len(keys))
    d_shuffled = derived_vals[perm_idx]

    perm_chi2[i] = compute_chi2(d_shuffled, exp_vals, unc_vals)
    perm_log_chi2[i] = compute_log_chi2(d_shuffled, exp_vals)

    if (i + 1) % 10_000 == 0:
        elapsed = time.time() - t0
        rate = (i + 1) / elapsed
        eta = (N_PERM - i - 1) / rate
        print(f"    [{i+1:>7,} / {N_PERM:,}]  elapsed={elapsed:.1f}s  ETA={eta:.1f}s")

total_time = time.time() - t0
print(f"  Permutations complete in {total_time:.1f}s")

# =============================================================================
# 7. REPORT: ACTUAL VS PERMUTED, P-VALUE, Z-SCORE
# =============================================================================

# Chi^2 metric
perm_chi2_mean = np.mean(perm_chi2)
perm_chi2_std = np.std(perm_chi2)
p_value_chi2 = np.mean(perm_chi2 <= actual_chi2)
z_score_chi2 = (perm_chi2_mean - actual_chi2) / perm_chi2_std

# Log-chi^2 metric
perm_log_mean = np.mean(perm_log_chi2)
perm_log_std = np.std(perm_log_chi2)
p_value_log = np.mean(perm_log_chi2 <= actual_log_chi2)
z_score_log = (perm_log_mean - actual_log_chi2) / perm_log_std

print("\n" + "=" * 72)
print("  PERMUTATION TEST RESULTS")
print("=" * 72)

print(f"\n  CHI-SQUARED METRIC: sum((derived - exp) / unc)^2")
print(f"    Actual chi^2:         {actual_chi2:>18.4f}")
print(f"    Permuted mean:        {perm_chi2_mean:>18.4f}")
print(f"    Permuted std:         {perm_chi2_std:>18.4f}")
print(f"    Permuted min:         {np.min(perm_chi2):>18.4f}")
print(f"    p-value:              {p_value_chi2:>18.6g}")
print(f"    Z-score:              {z_score_chi2:>18.2f}")

print(f"\n  LOG-CHI-SQUARED METRIC: sum(log10(derived / exp))^2")
print(f"    Actual log-chi^2:     {actual_log_chi2:>18.6f}")
print(f"    Permuted mean:        {perm_log_mean:>18.6f}")
print(f"    Permuted std:         {perm_log_std:>18.6f}")
print(f"    Permuted min:         {np.min(perm_log_chi2):>18.6f}")
print(f"    p-value:              {p_value_log:>18.6g}")
print(f"    Z-score:              {z_score_log:>18.2f}")

if p_value_chi2 == 0:
    print(f"\n  Chi^2 p-value < {1/N_PERM:.1e} (none of {N_PERM:,} permutations beat actual)")
if p_value_log == 0:
    print(f"  Log-chi^2 p-value < {1/N_PERM:.1e} (none of {N_PERM:,} permutations beat actual)")

print(f"\n  INTERPRETATION:")
print(f"    The correct derived->experimental mapping produces chi^2 = {actual_chi2:.1f}.")
print(f"    Random permutations produce chi^2 = {perm_chi2_mean:.1f} +/- {perm_chi2_std:.1f}.")
if z_score_chi2 > 5:
    print(f"    The actual mapping is {z_score_chi2:.1f} sigma better than random (p < {max(p_value_chi2, 1/N_PERM):.1e}).")
    print(f"    This decisively rejects the null hypothesis that the formulas")
    print(f"    are randomly matched to experimental values.")
else:
    print(f"    Z-score = {z_score_chi2:.1f} sigma.")

# =============================================================================
# 8. SAVE HISTOGRAM
# =============================================================================

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Chi^2 histogram
    ax = axes[0]
    ax.hist(perm_chi2, bins=100, color='steelblue', alpha=0.7, edgecolor='navy', linewidth=0.3, label='Permuted')
    ax.axvline(actual_chi2, color='red', linewidth=2, linestyle='--', label=f'Actual = {actual_chi2:.1f}')
    ax.set_xlabel(r'$\chi^2$', fontsize=13)
    ax.set_ylabel('Count', fontsize=13)
    ax.set_title(r'$\chi^2$ Permutation Test (56 constants, 100K trials)', fontsize=12)
    ax.legend(fontsize=11)
    # Add Z-score annotation
    ax.text(0.97, 0.95, f'Z = {z_score_chi2:.1f}\np < {max(p_value_chi2, 1/N_PERM):.1e}',
            transform=ax.transAxes, fontsize=11, verticalalignment='top', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

    # Log-chi^2 histogram
    ax = axes[1]
    ax.hist(perm_log_chi2, bins=100, color='coral', alpha=0.7, edgecolor='darkred', linewidth=0.3, label='Permuted')
    ax.axvline(actual_log_chi2, color='red', linewidth=2, linestyle='--', label=f'Actual = {actual_log_chi2:.4f}')
    ax.set_xlabel(r'$\sum \log_{10}^2(d_i/e_i)$', fontsize=13)
    ax.set_ylabel('Count', fontsize=13)
    ax.set_title(r'Log-$\chi^2$ Permutation Test (56 constants, 100K trials)', fontsize=12)
    ax.legend(fontsize=11)
    ax.text(0.97, 0.95, f'Z = {z_score_log:.1f}\np < {max(p_value_log, 1/N_PERM):.1e}',
            transform=ax.transAxes, fontsize=11, verticalalignment='top', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

    plt.tight_layout()
    out_path = r'C:/Users/atchi/e8-phi-constants/scripts/permutation_test_results.png'
    plt.savefig(out_path, dpi=150, bbox_inches='tight')
    print(f"\n  Histogram saved to: {out_path}")
    plt.close()

except ImportError:
    print("\n  [WARNING] matplotlib not available -- histogram not saved.")

print("\n" + "=" * 72)
print("  DONE")
print("=" * 72)
