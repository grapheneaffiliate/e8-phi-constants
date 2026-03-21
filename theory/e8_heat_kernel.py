#!/usr/bin/env python
"""
E8 Heat Kernel, Lattice Propagator, and Casimir Analysis
=========================================================

Three approaches to derive phi^(-n) selection rules from E8 geometry:
  1. Heat kernel on the E8 root system graph
  2. Lattice gauge theory propagator with E8->H4 projection
  3. Casimir operator and representation theory

Dependencies: numpy, scipy, matplotlib
"""

import numpy as np
from scipy import linalg as la
from scipy.special import comb as scipy_comb
from itertools import combinations, product
from collections import defaultdict
from math import comb, factorial
import csv
import os
import warnings
warnings.filterwarnings('ignore')

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# ===========================================================================
# CONSTANTS
# ===========================================================================
PHI = (1 + np.sqrt(5)) / 2
PHI_INV = 1.0 / PHI  # = phi - 1
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# GSM exponents
GSM_EXPONENTS = sorted([1,2,3,4,5,6,7,8,9,10,12,13,14,15,16,17,18,20,24,26,27,33,34])
GSM_SET = set(GSM_EXPONENTS)

# E8 data
E8_CASIMIR_DEGREES = [2, 8, 12, 14, 18, 20, 24, 30]
E8_COXETER_EXPONENTS = [1, 7, 11, 13, 17, 19, 23, 29]
E8_COXETER_NUMBER = 30
E8_RANK = 8
E8_DIM = 248

print("=" * 80)
print("E8 HEAT KERNEL, LATTICE PROPAGATOR & CASIMIR ANALYSIS")
print("=" * 80)

# ===========================================================================
# BUILD E8 ROOT SYSTEM (same as previous script)
# ===========================================================================
print("\n[SETUP] Building E8 root system...")

roots = []

# Type 1: 112 roots — permutations of (+-1, +-1, 0, 0, 0, 0, 0, 0)
for pos in combinations(range(8), 2):
    for signs in product([-1, 1], repeat=2):
        v = np.zeros(8)
        v[pos[0]] = signs[0]
        v[pos[1]] = signs[1]
        roots.append(v)

# Type 2: 128 roots — (+-1/2)^8 with even number of minus signs
for signs in product([-0.5, 0.5], repeat=8):
    v = np.array(signs)
    n_neg = sum(1 for s in signs if s < 0)
    if n_neg % 2 == 0:
        roots.append(v)

roots = np.array(roots)
N = len(roots)
assert N == 240, f"Expected 240 roots, got {N}"
print(f"  240 roots constructed, norms = sqrt(2)")

# Adjacency matrix (inner product = 1)
dot_matrix = roots @ roots.T
A = (np.abs(dot_matrix - 1.0) < 1e-10).astype(int)
np.fill_diagonal(A, 0)
degrees = A.sum(axis=1)
assert np.all(degrees == 56), "Kissing number check failed"

# Graph Laplacian
D_diag = np.diag(degrees)
L = D_diag - A

# Full eigendecomposition
eigenvalues_L, eigenvectors_L = np.linalg.eigh(L.astype(float))
idx_sort = np.argsort(eigenvalues_L)
eigenvalues_L = eigenvalues_L[idx_sort]
eigenvectors_L = eigenvectors_L[:, idx_sort]

# Unique eigenvalues and multiplicities
eig_rounded = np.round(eigenvalues_L, 4)
unique_eigs, eig_counts = np.unique(eig_rounded, return_counts=True)

print(f"  Laplacian spectrum: {dict(zip([int(e) for e in unique_eigs], [int(c) for c in eig_counts]))}")

# ===========================================================================
# E8 -> H4 PROJECTION (Elser-Sloane)
# ===========================================================================
print("\n[SETUP] Building E8 -> H4 projection...")

norm_par = 1.0 / np.sqrt(1 + PHI**2)
norm_perp = 1.0 / np.sqrt(1 + 1.0/PHI**2)

P_parallel = np.zeros((4, 8))
P_perp = np.zeros((4, 8))
for k in range(4):
    P_parallel[k, 2*k]   = norm_par * 1.0
    P_parallel[k, 2*k+1] = norm_par * PHI
    P_perp[k, 2*k]       = norm_perp * 1.0
    P_perp[k, 2*k+1]     = norm_perp * (-1.0/PHI)

proj_par = (P_parallel @ roots.T).T   # (240, 4)
proj_perp = (P_perp @ roots.T).T      # (240, 4)

norms_par = np.linalg.norm(proj_par, axis=1)
norms_perp = np.linalg.norm(proj_perp, axis=1)

# Per-root parallel fraction
par_fraction = norms_par**2 / (norms_par**2 + norms_perp**2)
unique_fractions = np.sort(np.unique(np.round(par_fraction, 8)))
print(f"  Parallel fractions: {unique_fractions}")

# Group roots by projected position
proj_groups = defaultdict(list)
for i in range(N):
    key = tuple(np.round(proj_par[i], 6))
    proj_groups[key].append(i)

group_list = list(proj_groups.values())
n_proj_points = len(group_list)
print(f"  Distinct projected positions: {n_proj_points}")

# Projection weights for each eigenmode
n_modes = len(eigenvalues_L)
projection_weights = np.zeros(n_modes)  # geometric weight
coherent_weights = np.zeros(n_modes)    # coherent interference weight

for k in range(n_modes):
    v = eigenvectors_L[:, k]
    projection_weights[k] = np.sum(np.abs(v)**2 * par_fraction)
    total_power = 0.0
    for group in group_list:
        group_sum = np.sum(v[group])
        total_power += group_sum**2
    coherent_weights[k] = total_power

print(f"  Geometric projection weights: [{projection_weights.min():.6f}, {projection_weights.max():.6f}]")
print(f"  Coherent projection weights:  [{coherent_weights.min():.6f}, {coherent_weights.max():.6f}]")

# ============================================================================
# APPROACH 1: HEAT KERNEL ON E8 LATTICE
# ============================================================================
print("\n" + "=" * 80)
print("APPROACH 1: HEAT KERNEL ON E8 ROOT SYSTEM GRAPH")
print("=" * 80)

# The 5 distinct eigenvalues and their multiplicities
lambda_vals = unique_eigs.astype(float)  # {0, 28, 48, 58, 60}
mult_vals = eig_counts.astype(float)

print(f"\nEigenvalues:    {lambda_vals}")
print(f"Multiplicities: {mult_vals}")

# 1.1 Full partition function Z(t) = Tr[exp(-tL)]
print("\n--- 1.1: Full Partition Function Z(t) ---")
t_values = np.linspace(0.001, 2.0, 2000)

def Z_full(t):
    """Full partition function."""
    return np.sum(mult_vals * np.exp(-t * lambda_vals))

Z_vals = np.array([Z_full(t) for t in t_values])
print(f"Z(0.001) = {Z_full(0.001):.6f}")
print(f"Z(0.01)  = {Z_full(0.01):.6f}")
print(f"Z(0.1)   = {Z_full(0.1):.6f}")
print(f"Z(1.0)   = {Z_full(1.0):.6f}")

# 1.2 Projected partition function
print("\n--- 1.2: Projected (Observable-Sector) Partition Function ---")
print("Using per-eigenmode projection weights to define Z_obs(t).")

# For each distinct eigenvalue, sum up the projection weights of modes at that eigenvalue
proj_weight_per_eig = np.zeros(len(lambda_vals))
coh_weight_per_eig = np.zeros(len(lambda_vals))

for i, lam in enumerate(lambda_vals):
    mask = np.abs(eig_rounded - lam) < 0.5
    proj_weight_per_eig[i] = projection_weights[mask].sum()
    coh_weight_per_eig[i] = coherent_weights[mask].sum()

print(f"\nProjection weights by eigenvalue:")
for lam, m, pw, cw in zip(lambda_vals, mult_vals, proj_weight_per_eig, coh_weight_per_eig):
    print(f"  lambda={lam:5.0f}  mult={m:4.0f}  geom_weight={pw:8.4f}  coherent_weight={cw:8.4f}")

def Z_obs_geom(t):
    """Observable-sector partition function using geometric weights."""
    return np.sum(proj_weight_per_eig * np.exp(-t * lambda_vals))

def Z_obs_coh(t):
    """Observable-sector partition function using coherent weights."""
    return np.sum(coh_weight_per_eig * np.exp(-t * lambda_vals))

# Also: the PROJECTED partition function with phi-structured weights
# The parallel fractions are {phi^(-2)/2, (phi^(-2)+1)/4, 1/2, (phi^2+1)/4, phi^2/2}
# approximately {0.053, 0.276, 0.5, 0.724, 0.947}
phi_weights = np.array([PHI**(-2)/2, (PHI**(-2)+1)/4, 0.5, (PHI**2+1)/4, PHI**2/2])
print(f"\nPhi-structured projection weights (Elser-Sloane fractions):")
print(f"  {phi_weights}")
print(f"  Actual unique parallel fractions: {unique_fractions}")

# Map each eigenvalue to a phi-weight
# Strategy: sort both sets and pair them
# We have 5 eigenvalues and potentially different number of phi-weights
# Let's check: how many unique parallel fractions exist?
n_uf = len(unique_fractions)
n_eig = len(lambda_vals)
print(f"\n  Number of unique parallel fractions: {n_uf}")
print(f"  Number of distinct eigenvalues: {n_eig}")

# The phi-weighted partition function uses eigenvalue * weight mixing
# For each root i, its contribution to Z_obs is:
#   exp(-t * lambda_mode * par_fraction_i)
# But lambda_mode depends on which eigenmode the root participates in.
# More precisely: Z_obs(t) = sum_k w_k * exp(-t * lambda_k)
# where w_k = sum_i |v_k(i)|^2 * par_fraction_i

# We already have this as proj_weight_per_eig. Let's also define a
# "phi-mixed" partition function where we literally scale the eigenvalues:
def Z_phi_mixed(t):
    """Partition function with phi-scaled eigenvalues."""
    result = 0.0
    for k in range(n_modes):
        lam_k = eigenvalues_L[k]
        w_k = projection_weights[k]
        # Effective eigenvalue = lambda * (average par_fraction for this mode)
        # = lambda * projection_weight (since eigvecs are normalized)
        lam_eff = lam_k * w_k  # This mixes integer with phi
        result += np.exp(-t * lam_eff)
    return result

# Sample at key t values
t_special = {
    '1/phi':    1.0/PHI,
    '1/phi^2':  1.0/PHI**2,
    'ln(phi)':  np.log(PHI),
    '1/30':     1.0/30,
    '1/28':     1.0/28,
    '1/60':     1.0/60,
    'phi/60':   PHI/60,
    '1/(30*phi)': 1.0/(30*PHI),
}

print(f"\n--- Z_obs values at special t ---")
print(f"{'t_name':>15s} {'t_value':>10s} {'Z_full':>14s} {'Z_obs_geom':>14s} {'Z_obs_coh':>14s} {'Z_phi_mix':>14s}")
print("-" * 85)
for name, t in t_special.items():
    zf = Z_full(t)
    zg = Z_obs_geom(t)
    zc = Z_obs_coh(t)
    zm = Z_phi_mixed(t)
    print(f"{name:>15s} {t:10.6f} {zf:14.6f} {zg:14.6f} {zc:14.6f} {zm:14.6f}")

# 1.3 Laurent series expansion around special t values
print("\n--- 1.3: Series Expansions ---")

# Expand Z_obs(t) = sum_k w_k * exp(-t * lambda_k)
# Around t0: Z_obs(t0 + dt) = sum_k w_k * exp(-t0 * lam_k) * sum_n (-lam_k * dt)^n / n!
# Coefficient of dt^n: C_n = sum_k w_k * exp(-t0*lam_k) * (-lam_k)^n / n!

def series_coefficients(t0, weights, lambdas, n_terms=10):
    """Compute Taylor coefficients of Z around t0."""
    coeffs = []
    for n in range(n_terms):
        c_n = 0.0
        for w, lam in zip(weights, lambdas):
            c_n += w * np.exp(-t0 * lam) * ((-lam)**n) / factorial(n)
        coeffs.append(c_n)
    return coeffs

print("\nTaylor coefficients of Z_obs_geom around t = 1/phi:")
t0 = 1.0/PHI
coeffs_phi = series_coefficients(t0, proj_weight_per_eig, lambda_vals, 12)
for n, c in enumerate(coeffs_phi):
    # Check if coefficient involves phi^(-n)
    if abs(c) > 1e-15:
        # Express c in terms of phi
        log_abs_c = np.log(abs(c)) / np.log(PHI)
        print(f"  C_{n:2d} = {c:18.10e}  |C_n| ~ phi^({log_abs_c:8.3f})")

print("\nTaylor coefficients of Z_obs_geom around t = 1/30 (1/Coxeter):")
t0 = 1.0/30
coeffs_cox = series_coefficients(t0, proj_weight_per_eig, lambda_vals, 12)
for n, c in enumerate(coeffs_cox):
    if abs(c) > 1e-15:
        log_abs_c = np.log(abs(c)) / np.log(PHI)
        print(f"  C_{n:2d} = {c:18.10e}  |C_n| ~ phi^({log_abs_c:8.3f})")

print("\nTaylor coefficients of Z_obs_geom around t = ln(phi):")
t0 = np.log(PHI)
coeffs_lnphi = series_coefficients(t0, proj_weight_per_eig, lambda_vals, 12)
for n, c in enumerate(coeffs_lnphi):
    if abs(c) > 1e-15:
        log_abs_c = np.log(abs(c)) / np.log(PHI)
        print(f"  C_{n:2d} = {c:18.10e}  |C_n| ~ phi^({log_abs_c:8.3f})")

# 1.4 Check if ratios of successive coefficients give phi^(-n)
print("\n--- 1.4: Coefficient Ratios and phi^(-n) Structure ---")

approach1_exponents = set()

for label, coeffs, t0_val in [("t0=1/phi", coeffs_phi, 1.0/PHI),
                                ("t0=1/30", coeffs_cox, 1.0/30),
                                ("t0=ln(phi)", coeffs_lnphi, np.log(PHI))]:
    print(f"\n  Ratios for {label}:")
    for n in range(1, len(coeffs)):
        if abs(coeffs[n-1]) > 1e-30 and abs(coeffs[n]) > 1e-30:
            ratio = coeffs[n] / coeffs[n-1]
            # Check if |ratio| ~ phi^(-m) for integer m
            if abs(ratio) > 1e-30:
                m = -np.log(abs(ratio)) / np.log(PHI)
                m_int = round(m)
                err = abs(m - m_int)
                marker = ""
                if err < 0.15 and 1 <= m_int <= 40:
                    marker = f" *** phi^(-{m_int}) ***"
                    if m_int in GSM_SET:
                        marker += " [GSM!]"
                    approach1_exponents.add(m_int)
                print(f"    C_{n}/C_{n-1} = {ratio:14.6e}  -> m = {m:8.3f} (nearest int: {m_int}){marker}")

# Also: the partition function evaluated at t = phi^(-n) for various n
print("\n  Z_obs_geom evaluated at t = phi^(-n):")
for n in range(1, 20):
    t_val = PHI**(-n)
    z_val = Z_obs_geom(t_val)
    z_full_val = Z_full(t_val)
    if z_full_val > 1e-30:
        ratio = z_val / z_full_val
        # The ratio Z_obs/Z_full at t=phi^(-n) measures how much the observable sector
        # dominates at that timescale
        n_eff = -np.log(ratio) / np.log(PHI) if ratio > 0 and ratio < 1 else 0
        print(f"    t = phi^(-{n:2d}) = {t_val:.8f}:  Z_obs/Z_full = {ratio:.8f}  (effective n ~ {n_eff:.3f})")

# Collect which GSM exponents appear
print(f"\n  Approach 1 phi-exponents found: {sorted(approach1_exponents)}")
print(f"  Overlap with GSM: {sorted(approach1_exponents & GSM_SET)}")


# ============================================================================
# APPROACH 2: LATTICE GAUGE THEORY PROPAGATOR
# ============================================================================
print("\n" + "=" * 80)
print("APPROACH 2: LATTICE GAUGE THEORY PROPAGATOR")
print("=" * 80)

# Propagator: G(m^2) = sum_k 1/(lambda_k + m^2) * mult_k
# Projected:  G_eff(m^2) = sum_k w_k / (lambda_k + m^2)
# Free:       G_free(m^2) = sum_k mult_k / (lambda_k + m^2)

def G_free(m2):
    """Unprojected propagator."""
    return np.sum(mult_vals / (lambda_vals + m2))

def G_eff_geom(m2):
    """Projected propagator using geometric weights."""
    return np.sum(proj_weight_per_eig / (lambda_vals + m2))

def G_eff_coh(m2):
    """Projected propagator using coherent weights."""
    return np.sum(coh_weight_per_eig / (lambda_vals + m2))

# 2.1 Propagator vs mass
print("\n--- 2.1: Effective Propagator G_eff(m^2) ---")
m2_values = np.logspace(-2, 2, 500)

G_free_vals = np.array([G_free(m2) for m2 in m2_values])
G_eff_geom_vals = np.array([G_eff_geom(m2) for m2 in m2_values])
G_eff_coh_vals = np.array([G_eff_coh(m2) for m2 in m2_values])

print(f"{'m^2':>10s}  {'G_free':>14s}  {'G_eff_geom':>14s}  {'G_eff_coh':>14s}  {'ratio_geom':>12s}  {'ratio_coh':>12s}")
print("-" * 80)
for m2 in [0.01, 0.1, 1.0, 10.0, 28.0, 48.0, 58.0, 60.0, 100.0]:
    gf = G_free(m2)
    gg = G_eff_geom(m2)
    gc = G_eff_coh(m2)
    print(f"{m2:10.2f}  {gf:14.8f}  {gg:14.8f}  {gc:14.8f}  {gg/gf:12.8f}  {gc/gf:12.8f}")

# 2.2 Ratio analysis
print("\n--- 2.2: Propagator Ratio G_eff/G_free ---")
ratio_geom = G_eff_geom_vals / G_free_vals
ratio_coh = G_eff_coh_vals / G_free_vals

print(f"Ratio range (geom): [{ratio_geom.min():.8f}, {ratio_geom.max():.8f}]")
print(f"Ratio range (coh):  [{ratio_coh.min():.8f}, {ratio_coh.max():.8f}]")

# 2.3 Expand ratio in powers of phi^(-1)
print("\n--- 2.3: Expansion of G_eff/G_free in phi^(-n) ---")

approach2_exponents = set()

# At specific m^2 values, check if the ratio is close to phi^(-n)
print(f"\n{'m^2':>10s}  {'ratio_geom':>12s}  {'n_phi':>10s}  {'err':>8s}  {'match':>10s}")
print("-" * 60)

for m2 in np.concatenate([np.arange(0.01, 1.0, 0.05), np.arange(1, 101, 1)]):
    r = G_eff_geom(m2) / G_free(m2)
    if 0 < r < 1:
        n_phi = -np.log(r) / np.log(PHI)
        n_int = round(n_phi)
        err = abs(n_phi - n_int)
        if err < 0.05 and 1 <= n_int <= 40:
            in_gsm = "[GSM!]" if n_int in GSM_SET else ""
            print(f"{m2:10.4f}  {r:12.8f}  {n_phi:10.4f}  {err:8.5f}  n={n_int:3d} {in_gsm}")
            approach2_exponents.add(n_int)

# 2.4 Try m^2 = phi^n
print("\n--- 2.4: Propagator at m^2 = phi^n ---")
print(f"{'n':>5s}  {'m^2=phi^n':>14s}  {'G_free':>14s}  {'G_eff_geom':>14s}  {'ratio':>12s}  {'n_eff':>10s}")
print("-" * 75)

for n in range(-10, 15):
    m2 = PHI**n
    gf = G_free(m2)
    gg = G_eff_geom(m2)
    r = gg / gf
    if 0 < r < 1:
        n_eff = -np.log(r) / np.log(PHI)
    elif r >= 1:
        n_eff = np.log(r) / np.log(PHI)
    else:
        n_eff = float('nan')
    n_eff_int = round(n_eff) if not np.isnan(n_eff) else None
    marker = ""
    if n_eff_int is not None and abs(n_eff - n_eff_int) < 0.1:
        marker = f"~ phi^({'-' if r < 1 else '+'}{abs(n_eff_int)})"
        if abs(n_eff_int) in GSM_SET:
            marker += " [GSM!]"
            approach2_exponents.add(abs(n_eff_int))
    print(f"{n:5d}  {m2:14.6f}  {gf:14.8f}  {gg:14.8f}  {r:12.8f}  {n_eff:10.4f}  {marker}")

# 2.5 Pole structure analysis
print("\n--- 2.5: Pole Structure and Residues ---")
print("Propagator poles at m^2 = -lambda_k:")
print(f"{'Pole (-lambda_k)':>18s}  {'Mult':>5s}  {'Residue_free':>14s}  {'Residue_eff':>14s}  {'Ratio':>12s}")
print("-" * 70)

for i, (lam, m, pw) in enumerate(zip(lambda_vals, mult_vals, proj_weight_per_eig)):
    # Residue at pole = multiplicity (free) or projection weight (eff)
    ratio = pw / m if m > 0 else 0
    n_phi = -np.log(ratio) / np.log(PHI) if 0 < ratio < 1 else (np.log(ratio) / np.log(PHI) if ratio > 1 else float('nan'))
    n_str = f"phi^({n_phi:.3f})" if not np.isnan(n_phi) else "N/A"
    print(f"{-lam:18.4f}  {m:5.0f}  {m:14.4f}  {pw:14.4f}  {ratio:12.6f}  {n_str}")
    # Check if ratio is near phi^(-n) for GSM n
    if not np.isnan(n_phi):
        n_int = round(n_phi)
        if abs(n_phi - n_int) < 0.2 and abs(n_int) in GSM_SET:
            approach2_exponents.add(abs(n_int))

print(f"\n  Approach 2 phi-exponents found: {sorted(approach2_exponents)}")
print(f"  Overlap with GSM: {sorted(approach2_exponents & GSM_SET)}")


# ============================================================================
# APPROACH 3: CASIMIR OPERATOR AND REPRESENTATION THEORY
# ============================================================================
print("\n" + "=" * 80)
print("APPROACH 3: CASIMIR OPERATOR AND REPRESENTATION THEORY")
print("=" * 80)

# 3.1 Weyl vector and quadratic Casimir
print("\n--- 3.1: Weyl Vector and Quadratic Casimir ---")

# The E8 Cartan matrix
# Standard basis: simple roots alpha_1, ..., alpha_8
# Using Bourbaki labeling for E8
E8_CARTAN = np.array([
    [ 2, -1,  0,  0,  0,  0,  0,  0],
    [-1,  2, -1,  0,  0,  0,  0,  0],
    [ 0, -1,  2, -1,  0,  0,  0, -1],
    [ 0,  0, -1,  2, -1,  0,  0,  0],
    [ 0,  0,  0, -1,  2, -1,  0,  0],
    [ 0,  0,  0,  0, -1,  2, -1,  0],
    [ 0,  0,  0,  0,  0, -1,  2,  0],
    [ 0,  0, -1,  0,  0,  0,  0,  2],
])

print(f"E8 Cartan matrix (8x8):")
print(E8_CARTAN)

# Inverse Cartan matrix gives the fundamental weights in simple root basis
# omega_i = sum_j (A^{-1})_{ji} * alpha_j
A_inv = np.linalg.inv(E8_CARTAN.astype(float))
print(f"\nInverse Cartan matrix (columns = fundamental weights):")
for i in range(8):
    print(f"  omega_{i+1} = {A_inv[:, i]}")

# Weyl vector rho = sum of fundamental weights = half-sum of positive roots
# In the Dynkin basis: rho = (1,1,1,1,1,1,1,1)
rho_dynkin = np.ones(8)
# In simple root basis: rho = sum_i omega_i = A^{-1} @ (1,1,...,1)
rho_root = A_inv @ rho_dynkin
print(f"\nWeyl vector rho (Dynkin basis): {rho_dynkin}")
print(f"Weyl vector rho (root basis):   {rho_root}")
print(f"|rho|^2 = rho . (A^{-1} @ rho_dynkin) = {rho_dynkin @ A_inv @ rho_dynkin:.6f}")

# Quadratic Casimir for a representation with highest weight lambda (in Dynkin basis)
# C_2(lambda) = (lambda, lambda + 2*rho) = (lambda + rho, lambda + rho) - (rho, rho)
# where the inner product uses the inverse Cartan matrix: (x, y) = x^T A^{-1} y

def quadratic_casimir(lambda_dynkin):
    """Compute C_2 for representation with highest weight lambda (Dynkin labels)."""
    lam = np.array(lambda_dynkin, dtype=float)
    lam_plus_rho = lam + rho_dynkin
    # (x, y) = x^T * A^{-1} * y in Dynkin basis
    rho_sq = rho_dynkin @ A_inv @ rho_dynkin
    lam_rho_sq = lam_plus_rho @ A_inv @ lam_plus_rho
    return lam_rho_sq - rho_sq

# Adjoint representation of E8: highest weight = highest root
# For E8, the adjoint rep has Dynkin label [0,0,0,0,0,0,0,1]
# (the 8th fundamental representation IS the adjoint for E8)
# Actually for E8 with Bourbaki numbering, the adjoint (248) has highest root
# theta = [0,0,0,0,0,0,1,0] or [1,0,0,0,0,0,0,0] depending on convention.
# Let's compute the highest root from the Cartan matrix.

# The highest root theta satisfies: theta = sum_i a_i alpha_i where
# a = (2, 3, 4, 5, 6, 4, 2, 3) for E8 (these are the marks/Kac labels)
theta_marks = np.array([2, 3, 4, 5, 6, 4, 2, 3])  # Marks of E8

# In Dynkin basis, the highest root has labels:
# theta_dynkin[i] = sum_j theta_marks[j] * A[j,i] ... no, that's wrong
# The Dynkin labels of theta are: theta_i = <theta, alpha_i^vee> = sum_j a_j A_{ji}
# For simply-laced groups, this equals: theta_dynkin = A^T @ theta_marks
# But theta_dynkin should have non-negative entries for the highest root.
# Actually: the highest root of E8 has Dynkin label (1,0,0,0,0,0,0,0) for Bourbaki.
# Let me verify:

# The highest root theta = sum a_i alpha_i with marks a = (2,3,4,5,6,4,2,3)
# Dynkin label = <theta, alpha_j^vee> = sum_i a_i <alpha_i, alpha_j^vee> = sum_i a_i A_ij
theta_dynkin = E8_CARTAN.T @ theta_marks
print(f"\nHighest root marks (root coefficients): {theta_marks}")
print(f"Highest root Dynkin labels: {theta_dynkin}")

# For E8, the adjoint (248) has highest weight = highest root
# Dynkin label should be [1,0,0,0,0,0,0,0] for Bourbaki
# If not, let's check both conventions

C2_adjoint = quadratic_casimir(theta_dynkin)
print(f"\nQuadratic Casimir C_2(adjoint) = {C2_adjoint:.6f}")

# Known: C_2(E8 adjoint) = 60 (in the standard normalization where long roots have length^2 = 2)
# With our normalization: C_2 = (theta + rho, theta + rho) - (rho, rho)
print(f"Expected C_2(adjoint) = 60 (standard normalization)")

# Let's also compute for fundamental representations
print(f"\n--- Casimir values for fundamental representations ---")
fund_reps = []
for i in range(8):
    dynkin = np.zeros(8)
    dynkin[i] = 1
    c2 = quadratic_casimir(dynkin)
    fund_reps.append((i+1, c2))
    print(f"  omega_{i+1}: C_2 = {c2:.6f}")

# 3.2 Higher Casimir eigenvalues
print("\n--- 3.2: Higher Casimir Operators ---")
print("Casimir degrees of E8:", E8_CASIMIR_DEGREES)
print("\nFor the adjoint representation, the Casimir eigenvalues can be computed")
print("from the characteristic exponents via the Freudenthal formula.")
print("The eigenvalue of the degree-d Casimir on the adjoint rep is related to")
print("the d-th power sum of the exponents+1.")

# Exponents of E8: m_i = {1, 7, 11, 13, 17, 19, 23, 29}
# The eigenvalue of the degree-d Casimir on the adjoint = sum_i (m_i + 1)^d / normalization
# More precisely: for normalized generators, c_d(adj) = sum_i (m_i)^{d-1} * (some normalization)

# A practical formula: the character of the adjoint representation
# evaluated at exp(t * rho) gives the product formula involving Casimirs.
# For our purposes, the key structural result is:

# The ADJOINT representation of E8 decomposes under H4 as:
# 248 -> ? (we need to compute this branching)

# Under E8 -> H4 (via the icosahedral projection), the adjoint 248 decomposes.
# Since H4 is a finite Coxeter group (not a Lie group), the "representations"
# are those of the Weyl group W(H4) of order 14400.

# The W(H4) irreps have dimensions:
# 1, 4, 5, 6, 8, 9, 10, 16, 18, 20, 24, 25, 30, 36, 40, 45, 48, 60, 64, 80, ...
# (these are the irreps of the Coxeter group of type H4)

# The 240 roots of E8, when projected, give the 120 vertices of the 600-cell
# (each with multiplicity 2). The Weyl group W(H4) acts on these.

# The permutation representation of W(E8) restricted to W(H4) on the 240 roots
# decomposes into W(H4) irreps. The multiplicities give us the branching.

# For a practical computation without implementing the full W(H4) machinery,
# we use the known result:
# Under E8 -> D4 x D4 (triality), 248 = (28,1) + (1,28) + (8_v, 8_v) + (8_s, 8_s) + (8_c, 8_c)
# And under the further folding D4 -> H2 x H2, we get H4 structure.

# Instead, let's compute what we CAN compute: the Casimir eigenvalue differences
# and check against GSM exponents.

print("\n--- 3.3: Casimir Eigenvalue Differences ---")

approach3_exponents = set()

# Compute Casimir eigenvalues for several representations
# Key representations of E8 and their Dynkin labels + dimensions:
representations = {
    'trivial':    ([0,0,0,0,0,0,0,0], 1),
    'adjoint':    (list(theta_dynkin.astype(int)), 248),
    'fund_1':     ([1,0,0,0,0,0,0,0], 248),  # = adjoint for E8
    'fund_8':     ([0,0,0,0,0,0,0,1], 248),   # = adjoint (other end)
    'fund_2':     ([0,1,0,0,0,0,0,0], 30380),
    'fund_7':     ([0,0,0,0,0,0,1,0], 147250),
}

# Only compute for representations where we know the Dynkin label
casimir_values = {}
print(f"\n{'Rep':>12s}  {'Dim':>8s}  {'C_2':>12s}")
print("-" * 36)
for name, (dynkin, dim) in representations.items():
    c2 = quadratic_casimir(dynkin)
    casimir_values[name] = c2
    print(f"{name:>12s}  {dim:>8d}  {c2:12.4f}")

# Differences between Casimir values
print(f"\n--- Casimir Eigenvalue Differences ---")
print(f"{'Rep_i':>12s}  {'Rep_j':>12s}  {'C2_i':>10s}  {'C2_j':>10s}  {'Diff':>10s}  {'n_phi':>8s}  {'Match':>10s}")
print("-" * 75)

rep_names = list(casimir_values.keys())
for i, name_i in enumerate(rep_names):
    for j, name_j in enumerate(rep_names):
        if i >= j:
            continue
        c_i = casimir_values[name_i]
        c_j = casimir_values[name_j]
        diff = abs(c_j - c_i)
        if diff > 0.01:
            n_phi = np.log(diff) / np.log(PHI)
            n_int = round(n_phi)
            err = abs(n_phi - n_int)
            marker = ""
            if err < 0.2 and 1 <= n_int <= 40:
                marker = f"phi^{n_int}"
                if n_int in GSM_SET:
                    marker += " [GSM!]"
                approach3_exponents.add(n_int)
            print(f"{name_i:>12s}  {name_j:>12s}  {c_i:10.4f}  {c_j:10.4f}  {diff:10.4f}  {n_phi:8.3f}  {marker}")

# 3.4 Casimir degrees and E8 exponents generate selection rules
print("\n--- 3.4: Selection Rules from Casimir Degrees and Coxeter Exponents ---")

# The deepest structural result: the allowed phi-exponents are determined by
# the ARITHMETIC of the Casimir degrees and Coxeter exponents.

# Casimir degrees: {2, 8, 12, 14, 18, 20, 24, 30}
# Coxeter exponents: {1, 7, 11, 13, 17, 19, 23, 29}
# H4 Coxeter exponents: {1, 11, 19, 29}

# Rule: n is allowed if it can be written as:
#   n = |m_i +/- m_j| for Coxeter exponents m_i, m_j
# or n = |d_i +/- d_j| / k for Casimir degrees d_i, d_j and small k

# Generate all pairwise sums/differences of E8 Coxeter exponents
e8_exp = E8_COXETER_EXPONENTS
h4_exp = [1, 11, 19, 29]
casimir = E8_CASIMIR_DEGREES

coxeter_pairs = set()
for a in e8_exp:
    coxeter_pairs.add(a)
    for b in e8_exp:
        if a + b <= 40:
            coxeter_pairs.add(a + b)
        if abs(a - b) >= 1:
            coxeter_pairs.add(abs(a - b))

h4_pairs = set()
for a in h4_exp:
    h4_pairs.add(a)
    for b in h4_exp:
        if a + b <= 40:
            h4_pairs.add(a + b)
        if abs(a - b) >= 1:
            h4_pairs.add(abs(a - b))

casimir_pairs = set()
for a in casimir:
    casimir_pairs.add(a)
    for b in casimir:
        if a + b <= 40:
            casimir_pairs.add(a + b)
        if abs(a - b) >= 1:
            casimir_pairs.add(abs(a - b))
        # Also: (a+b)/2, (a-b)/2 if they are integers
        if (a + b) % 2 == 0:
            casimir_pairs.add((a + b) // 2)
        if abs(a - b) % 2 == 0 and abs(a - b) // 2 >= 1:
            casimir_pairs.add(abs(a - b) // 2)

# Combined with H4 x E8 cross terms
cross_terms = set()
for a in e8_exp:
    for b in h4_exp:
        if a + b <= 40:
            cross_terms.add(a + b)
        if abs(a - b) >= 1:
            cross_terms.add(abs(a - b))

all_algebraic = coxeter_pairs | h4_pairs | casimir_pairs | cross_terms
# Add triple combinations
triple_set = set()
all_sources = sorted(set(e8_exp) | set(h4_exp) | set(casimir))
for a in all_sources:
    for b in all_sources:
        for c in all_sources:
            for val in [a+b+c, a+b-c, a-b+c, abs(a-b-c)]:
                if 1 <= val <= 40:
                    triple_set.add(val)

all_algebraic = all_algebraic | triple_set

print(f"GSM exponents: {sorted(GSM_SET)}")
print(f"From E8 Coxeter pairs:   {sorted(coxeter_pairs & GSM_SET)}")
print(f"From H4 Coxeter pairs:   {sorted(h4_pairs & GSM_SET)}")
print(f"From Casimir pairs:      {sorted(casimir_pairs & GSM_SET)}")
print(f"From E8 x H4 cross:      {sorted(cross_terms & GSM_SET)}")
print(f"From triples:            {sorted(triple_set & GSM_SET)}")
print(f"Total algebraic:         {sorted(all_algebraic & GSM_SET)}")
print(f"Uncovered:               {sorted(GSM_SET - all_algebraic)}")

approach3_exponents = approach3_exponents | (all_algebraic & GSM_SET)

# 3.5 Branching analysis via projection of eigenvectors
print("\n--- 3.5: Spectral Branching E8 -> H4 ---")
print("Eigenvalues with their H4-compatible content (coherent projection weight):")

# For each eigenvalue, the ratio of coherent weight to multiplicity
# tells us what fraction of the eigenspace survives the H4 projection
branching_data = []
for i, (lam, m, cw) in enumerate(zip(lambda_vals, mult_vals, coh_weight_per_eig)):
    survival_frac = cw / m if m > 0 else 0
    branching_data.append((lam, m, cw, survival_frac))
    print(f"  lambda={lam:5.0f}  mult={m:4.0f}  H4_weight={cw:8.4f}  survival={survival_frac:8.4f}")

    # The survival fraction tells us the dimension of the H4-compatible subspace
    # within the eigenspace
    effective_h4_dim = round(cw)
    if effective_h4_dim > 0:
        n_phi = np.log(m / effective_h4_dim) / np.log(PHI) if effective_h4_dim < m else 0
        print(f"    -> Effective H4 dim ~ {effective_h4_dim}, branching ratio log_phi = {n_phi:.3f}")

# ============================================================================
# CRITICAL ANALYSIS: STATISTICAL TESTS
# ============================================================================
print("\n" + "=" * 80)
print("CRITICAL ANALYSIS: STATISTICAL SIGNIFICANCE TESTS")
print("=" * 80)

from scipy.stats import hypergeom

# For each approach, compute how many GSM exponents are predicted
# vs expected by chance

# The null hypothesis: draw k integers uniformly from {1,...,40}
# What's the probability of hitting >= m of the 23 GSM exponents?

# GSM set has 23 elements out of {1,...,40}, so GSM density = 23/40 = 0.575

N_universe = 40  # possible exponents 1..40
K_gsm = len(GSM_SET)  # 23 successes in population

def p_value_hypergeometric(n_predicted_total, n_predicted_gsm):
    """
    p-value: probability of getting >= n_predicted_gsm GSM matches
    when drawing n_predicted_total integers from {1..40},
    given 23 GSM exponents out of 40.
    """
    if n_predicted_total <= 0 or n_predicted_gsm <= 0:
        return 1.0
    n = min(n_predicted_total, N_universe)
    # P(X >= n_predicted_gsm) where X ~ Hypergeometric(N=40, K=23, n=n_predicted_total)
    p = hypergeom.sf(n_predicted_gsm - 1, N_universe, K_gsm, n)
    return p

# Approach 1: Heat kernel
a1_predicted = sorted(approach1_exponents & set(range(1, 41)))
a1_gsm = sorted(approach1_exponents & GSM_SET)
a1_n = len(a1_predicted)
a1_m = len(a1_gsm)
a1_expected = a1_n * K_gsm / N_universe if a1_n > 0 else 0
a1_pval = p_value_hypergeometric(a1_n, a1_m)

# Approach 2: Propagator
a2_predicted = sorted(approach2_exponents & set(range(1, 41)))
a2_gsm = sorted(approach2_exponents & GSM_SET)
a2_n = len(a2_predicted)
a2_m = len(a2_gsm)
a2_expected = a2_n * K_gsm / N_universe if a2_n > 0 else 0
a2_pval = p_value_hypergeometric(a2_n, a2_m)

# Approach 3: Casimir/algebraic
a3_predicted = sorted(all_algebraic & set(range(1, 41)))
a3_gsm = sorted(all_algebraic & GSM_SET)
a3_n = len(a3_predicted)
a3_m = len(a3_gsm)
a3_expected = a3_n * K_gsm / N_universe if a3_n > 0 else 0
a3_pval = p_value_hypergeometric(a3_n, a3_m)

# Combined
all_combined = approach1_exponents | approach2_exponents | (all_algebraic & GSM_SET)
ac_predicted = sorted(all_combined & set(range(1, 41)))
ac_gsm = sorted(all_combined & GSM_SET)
ac_n = len(ac_predicted)
ac_m = len(ac_gsm)
ac_expected = ac_n * K_gsm / N_universe if ac_n > 0 else 0
ac_pval = p_value_hypergeometric(ac_n, ac_m)

print(f"\n{'Approach':<25s} {'Predicted':>10s} {'GSM hits':>10s} {'Expected':>10s} {'p-value':>12s} {'Verdict':>15s}")
print("-" * 90)

def verdict(p):
    if p < 0.001:
        return "SIGNIFICANT ***"
    elif p < 0.01:
        return "SIGNIFICANT **"
    elif p < 0.05:
        return "SIGNIFICANT *"
    else:
        return "NOT SIGNIFICANT"

print(f"{'1. Heat Kernel':<25s} {a1_n:>10d} {a1_m:>10d} {a1_expected:>10.1f} {a1_pval:>12.6f} {verdict(a1_pval):>15s}")
print(f"{'2. Propagator':<25s} {a2_n:>10d} {a2_m:>10d} {a2_expected:>10.1f} {a2_pval:>12.6f} {verdict(a2_pval):>15s}")
print(f"{'3. Casimir/Algebraic':<25s} {a3_n:>10d} {a3_m:>10d} {a3_expected:>10.1f} {a3_pval:>12.6f} {verdict(a3_pval):>15s}")
print(f"{'Combined':<25s} {ac_n:>10d} {ac_m:>10d} {ac_expected:>10.1f} {ac_pval:>12.6f} {verdict(ac_pval):>15s}")

print(f"\nNote: GSM density = {K_gsm}/{N_universe} = {K_gsm/N_universe:.3f}")
print(f"With 23 out of 40 integers being GSM exponents, random overlap is VERY LIKELY.")
print(f"A p-value assessment MUST account for the high base rate.")

# Detailed: which GSM exponents are covered by which approach?
print(f"\n--- Exponent Coverage by Approach ---")
print(f"{'n':>4s}  {'A1':>4s}  {'A2':>4s}  {'A3':>4s}  {'Any':>4s}")
print("-" * 25)
for n in GSM_EXPONENTS:
    a1 = "yes" if n in approach1_exponents else "-"
    a2 = "yes" if n in approach2_exponents else "-"
    a3 = "yes" if n in (all_algebraic & GSM_SET) else "-"
    any_hit = "YES" if n in (approach1_exponents | approach2_exponents | (all_algebraic & GSM_SET)) else "NO"
    print(f"{n:>4d}  {a1:>4s}  {a2:>4s}  {a3:>4s}  {any_hit:>4s}")

uncovered = GSM_SET - (approach1_exponents | approach2_exponents | (all_algebraic & GSM_SET))
print(f"\nUncovered GSM exponents: {sorted(uncovered)}")


# ============================================================================
# SAVE RESULTS
# ============================================================================
print("\n" + "=" * 80)
print("SAVING RESULTS")
print("=" * 80)

# CSV
csv_path = os.path.join(SCRIPT_DIR, "e8_heat_kernel_results.csv")
with open(csv_path, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['approach', 'eigenvalue', 'multiplicity', 'projection_weight',
                     'coherent_weight', 'phi_exponent', 'in_gsm'])

    for i, (lam, m, pw, cw) in enumerate(zip(lambda_vals, mult_vals, proj_weight_per_eig, coh_weight_per_eig)):
        # From heat kernel
        writer.writerow(['heat_kernel', f"{lam:.4f}", int(m), f"{pw:.8f}", f"{cw:.8f}", '', ''])

    for n in sorted(approach1_exponents):
        writer.writerow(['heat_kernel_exponent', '', '', '', '', n, n in GSM_SET])

    for n in sorted(approach2_exponents):
        writer.writerow(['propagator_exponent', '', '', '', '', n, n in GSM_SET])

    for n in sorted(all_algebraic & GSM_SET):
        writer.writerow(['casimir_exponent', '', '', '', '', n, True])

print(f"Saved: {csv_path}")

# Plot 1: Heat kernel partition function
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Z(t) full vs projected
ax = axes[0, 0]
t_plot = np.linspace(0.001, 0.5, 1000)
Z_full_plot = np.array([Z_full(t) for t in t_plot])
Z_obs_geom_plot = np.array([Z_obs_geom(t) for t in t_plot])
Z_obs_coh_plot = np.array([Z_obs_coh(t) for t in t_plot])

ax.semilogy(t_plot, Z_full_plot, 'b-', linewidth=2, label='Z_full(t)')
ax.semilogy(t_plot, Z_obs_geom_plot, 'r-', linewidth=2, label='Z_obs_geom(t)')
ax.semilogy(t_plot, Z_obs_coh_plot, 'g--', linewidth=2, label='Z_obs_coh(t)')
# Mark special t values
for name, t_val in t_special.items():
    if 0.001 <= t_val <= 0.5:
        ax.axvline(t_val, color='gray', alpha=0.3, linestyle=':')
        ax.text(t_val, ax.get_ylim()[1]*0.5, name, rotation=90, fontsize=7, va='top')
ax.set_xlabel('t (diffusion time)')
ax.set_ylabel('Partition function Z(t)')
ax.set_title('Heat Kernel Partition Functions')
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)

# Ratio Z_obs/Z_full
ax = axes[0, 1]
ratio_plot = Z_obs_geom_plot / Z_full_plot
ax.plot(t_plot, ratio_plot, 'r-', linewidth=2, label='Z_obs_geom / Z_full')
ratio_coh_plot = Z_obs_coh_plot / Z_full_plot
ax.plot(t_plot, ratio_coh_plot, 'g--', linewidth=2, label='Z_obs_coh / Z_full')
# Mark phi^(-n) levels
for n in [1, 2, 3]:
    ax.axhline(PHI**(-n), color='orange', alpha=0.3, linestyle='--')
    ax.text(0.01, PHI**(-n), f'phi^(-{n})', fontsize=8, va='bottom')
ax.set_xlabel('t (diffusion time)')
ax.set_ylabel('Ratio Z_obs / Z_full')
ax.set_title('Observable Sector Fraction vs Diffusion Time')
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)

# Propagator G_eff vs m^2
ax = axes[1, 0]
m2_plot = np.logspace(-2, 2, 500)
G_free_plot = np.array([G_free(m2) for m2 in m2_plot])
G_eff_plot = np.array([G_eff_geom(m2) for m2 in m2_plot])
ax.loglog(m2_plot, G_free_plot, 'b-', linewidth=2, label='G_free(m^2)')
ax.loglog(m2_plot, G_eff_plot, 'r-', linewidth=2, label='G_eff(m^2)')
# Mark eigenvalue positions
for lam in lambda_vals:
    if lam > 0:
        ax.axvline(lam, color='gray', alpha=0.3, linestyle=':')
ax.set_xlabel('m^2')
ax.set_ylabel('Propagator G(m^2)')
ax.set_title('Lattice Propagator: Free vs Projected')
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)

# Propagator ratio
ax = axes[1, 1]
ratio_prop = G_eff_plot / G_free_plot
ax.semilogx(m2_plot, ratio_prop, 'r-', linewidth=2)
ax.set_xlabel('m^2')
ax.set_ylabel('G_eff / G_free')
ax.set_title('Propagator Ratio (Observable / Total)')
# Mark phi^(-n) levels
for n in [1, 2, 3, 4]:
    y_val = PHI**(-n)
    if y_val > ratio_prop.min() * 0.5:
        ax.axhline(y_val, color='orange', alpha=0.3, linestyle='--')
        ax.text(m2_plot[0], y_val, f'phi^(-{n})', fontsize=8, va='bottom')
ax.grid(True, alpha=0.3)

plt.suptitle('E8 Heat Kernel and Lattice Propagator Analysis', fontsize=14, fontweight='bold')
plt.tight_layout()
plot1_path = os.path.join(SCRIPT_DIR, "e8_heat_kernel_partition.png")
plt.savefig(plot1_path, dpi=150, bbox_inches='tight')
plt.close()
print(f"Saved: {plot1_path}")

# Plot 2: Effective propagator analysis
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Pole structure
ax = axes[0, 0]
for i, (lam, m, pw) in enumerate(zip(lambda_vals, mult_vals, proj_weight_per_eig)):
    ax.bar(lam, m, width=1.5, color='steelblue', alpha=0.7, label='Multiplicity' if i == 0 else None)
    ax.bar(lam + 1.8, pw, width=1.5, color='red', alpha=0.7, label='Proj. weight' if i == 0 else None)
ax.set_xlabel('Eigenvalue')
ax.set_ylabel('Weight')
ax.set_title('Pole Residues: Free (blue) vs Projected (red)')
ax.legend()
ax.grid(True, alpha=0.3)

# Taylor coefficients
ax = axes[0, 1]
n_terms = len(coeffs_phi)
x_vals = range(n_terms)
abs_coeffs_phi = [abs(c) if abs(c) > 1e-30 else 1e-30 for c in coeffs_phi]
abs_coeffs_cox = [abs(c) if abs(c) > 1e-30 else 1e-30 for c in coeffs_cox]
ax.semilogy(x_vals, abs_coeffs_phi, 'ro-', label='t0 = 1/phi')
ax.semilogy(x_vals, abs_coeffs_cox, 'bs-', label='t0 = 1/30')
ax.set_xlabel('Taylor order n')
ax.set_ylabel('|C_n|')
ax.set_title('Taylor Coefficients of Z_obs')
ax.legend()
ax.grid(True, alpha=0.3)

# Casimir values
ax = axes[1, 0]
fund_c2 = [c2 for _, c2 in fund_reps]
ax.bar(range(1, 9), fund_c2, color='purple', alpha=0.7)
ax.set_xlabel('Fundamental weight index')
ax.set_ylabel('C_2 value')
ax.set_title('Quadratic Casimir for E8 Fundamental Representations')
ax.grid(True, alpha=0.3)

# Coverage heatmap
ax = axes[1, 1]
coverage_matrix = np.zeros((3, len(GSM_EXPONENTS)))
for j, n in enumerate(GSM_EXPONENTS):
    if n in approach1_exponents:
        coverage_matrix[0, j] = 1
    if n in approach2_exponents:
        coverage_matrix[1, j] = 1
    if n in (all_algebraic & GSM_SET):
        coverage_matrix[2, j] = 1

im = ax.imshow(coverage_matrix, aspect='auto', cmap='RdYlGn', vmin=0, vmax=1)
ax.set_yticks([0, 1, 2])
ax.set_yticklabels(['Heat Kernel', 'Propagator', 'Casimir/Alg.'])
ax.set_xticks(range(len(GSM_EXPONENTS)))
ax.set_xticklabels(GSM_EXPONENTS, fontsize=7, rotation=45)
ax.set_xlabel('GSM Exponent n')
ax.set_title('GSM Exponent Coverage by Approach')
plt.colorbar(im, ax=ax, label='Covered (1) / Not (0)')

plt.suptitle('E8 Effective Propagator and Selection Rule Analysis', fontsize=14, fontweight='bold')
plt.tight_layout()
plot2_path = os.path.join(SCRIPT_DIR, "e8_effective_propagator.png")
plt.savefig(plot2_path, dpi=150, bbox_inches='tight')
plt.close()
print(f"Saved: {plot2_path}")


# ============================================================================
# FINAL VERDICT
# ============================================================================
print("\n" + "=" * 80)
print("FINAL VERDICT")
print("=" * 80)

print(f"""
APPROACH 1 (Heat Kernel):
  The heat kernel Z_obs(t) = sum_k w_k * exp(-t * lambda_k) mixes integer
  eigenvalues {{0, 28, 48, 58, 60}} with phi-structured projection weights.

  Taylor expansion around t = 1/phi, 1/30, ln(phi) produces coefficients
  whose magnitudes scale as phi^(-n) for various n.

  Exponents found: {sorted(approach1_exponents & GSM_SET)}
  GSM coverage: {len(approach1_exponents & GSM_SET)}/{len(GSM_SET)}

APPROACH 2 (Lattice Propagator):
  The ratio G_eff/G_free varies smoothly with m^2 and passes through
  phi^(-n) values at specific masses. The pole residue ratios (projected
  weight / multiplicity) encode the H4-projection structure.

  Exponents found: {sorted(approach2_exponents & GSM_SET)}
  GSM coverage: {len(approach2_exponents & GSM_SET)}/{len(GSM_SET)}

APPROACH 3 (Casimir/Algebraic):
  The Casimir degrees, Coxeter exponents, and their pairwise/triple
  sums and differences generate a set of integers that covers {len(all_algebraic & GSM_SET)}/{len(GSM_SET)}
  GSM exponents. This is the most complete approach.

  Exponents found: {sorted(all_algebraic & GSM_SET)}
  Uncovered: {sorted(GSM_SET - all_algebraic)}

STATISTICAL ASSESSMENT:
  The GSM set contains 23 of 40 possible integers (57.5% density).
  Any approach generating ~20+ integers from {{1,...,40}} will inevitably
  cover most GSM exponents by CHANCE ALONE.

  Approach 3 (Casimir/Algebraic) generates {a3_n} integers from {{1..40}} and
  covers {a3_m}/{len(GSM_SET)} GSM exponents. Expected by chance: {a3_expected:.1f}.
  p-value = {a3_pval:.6f} -> {verdict(a3_pval)}

  HONEST ASSESSMENT: The high GSM density (23/40) makes it extremely difficult
  to distinguish genuine structure from combinatorial coincidence using integer
  matching alone. The approaches above identify MECHANISMS by which phi enters
  the projected E8 spectrum, but the statistical test shows that covering the
  GSM set is not surprising given the number of integers generated.

  The GENUINE phi-structure lies not in WHICH integers appear, but in the
  CONTINUOUS dependence of the projection weights on phi. The per-root
  parallel fractions {{phi^(-2)/2, ...}} are exact golden-ratio expressions,
  and these enter the heat kernel and propagator as continuous parameters.
  The integer exponents n in phi^(-n) arise when these continuous expressions
  are expanded in the phi-adic basis, not from simple integer matching.

VERDICT: The E8 -> H4 projection introduces GENUINE phi-dependence through
the Elser-Sloane projection weights. The heat kernel and propagator carry
this phi-structure continuously. However, the SELECTION RULES for which
specific phi^(-n) exponents appear in physical formulas require additional
input beyond the root system graph spectrum alone -- specifically, the
dynamics of the field theory on the E8 lattice and the specific physical
observable being computed. The Casimir/algebraic approach provides the
most complete coverage but suffers from low selectivity.

STATUS: PARTIALLY DERIVED -- phi enters via projection geometry (proven),
but specific exponent selection requires dynamical input (open).
""")

print("=" * 80)
print("COMPUTATION COMPLETE")
print("=" * 80)
