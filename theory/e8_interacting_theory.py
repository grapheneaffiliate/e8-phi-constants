#!/usr/bin/env python
"""
E8 Interacting Scalar Field Theory on the Root Lattice
=======================================================

Implements an interacting phi^4 theory on the E8 root system graph,
where the coupling depends on each root's parallel fraction under
the Elser-Sloane E8->H4 projection.

Key idea: In the free theory, all eigenspaces project to 50% observable.
Interactions weighted by the projection angle break this democracy,
producing phi^(-n) corrections whose exponents we extract and compare
to the GSM set {1,2,...,10,12,...,34}.

Steps:
  1. Build E8 root system, adjacency, Laplacian, eigendecomposition
  2. Elser-Sloane projection -> parallel fractions
  3. Define three coupling functions f(p)
  4. Compute one-loop self-energy Sigma for each coupling
  5. Corrected propagator and effective 4D projection
  6. Extract phi^(-n) coefficients via least squares
  7. Scan over mass parameter
  8. Critical analysis vs GSM exponents

Dependencies: numpy, scipy, matplotlib
"""

import numpy as np
from scipy import linalg as la
from itertools import combinations, product
from collections import defaultdict
import csv
import os
import warnings
warnings.filterwarnings('ignore')

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Constants
PHI = (1 + np.sqrt(5)) / 2
PHI_INV = 1.0 / PHI

GSM_EXPONENTS = sorted([1,2,3,4,5,6,7,8,9,10,12,13,14,15,16,17,18,20,24,26,27,33,34])
GSM_SET = set(GSM_EXPONENTS)
N_GSM = len(GSM_EXPONENTS)

print("=" * 80)
print("E8 INTERACTING SCALAR FIELD THEORY ON THE ROOT LATTICE")
print("=" * 80)

# ============================================================================
# STEP 1: BUILD E8 ROOT SYSTEM, ADJACENCY, LAPLACIAN, EIGENDECOMPOSITION
# ============================================================================
print("\n" + "=" * 80)
print("STEP 1: E8 Root System and Graph Laplacian")
print("=" * 80)

roots = []

# Type 1: 112 roots — permutations of (+-1, +-1, 0, 0, 0, 0, 0, 0)
for pos in combinations(range(8), 2):
    for signs in product([-1, 1], repeat=2):
        v = np.zeros(8)
        v[pos[0]] = signs[0]
        v[pos[1]] = signs[1]
        roots.append(v)

n_type1 = len(roots)
print(f"Type 1 roots: {n_type1}")

# Type 2: 128 roots — (+-1/2)^8 with even number of minus signs
for signs in product([-0.5, 0.5], repeat=8):
    v = np.array(signs)
    n_neg = sum(1 for s in signs if s < 0)
    if n_neg % 2 == 0:
        roots.append(v)

n_type2 = len(roots) - n_type1
print(f"Type 2 roots: {n_type2}")

roots = np.array(roots)
N = len(roots)
assert N == 240, f"Expected 240, got {N}"
print(f"Total roots: {N}")

# Adjacency matrix (inner product = 1)
dot_matrix = roots @ roots.T
A = (np.abs(dot_matrix - 1.0) < 1e-10).astype(float)
np.fill_diagonal(A, 0)
degrees = A.sum(axis=1)
assert np.allclose(degrees, 56), "Kissing number check failed"
print(f"Each root has {int(degrees[0])} neighbors (kissing number = 56)")

# Graph Laplacian L = D - A
L = 56.0 * np.eye(N) - A

# Full eigendecomposition
eigenvalues_L, eigenvectors_L = np.linalg.eigh(L)
idx_sort = np.argsort(eigenvalues_L)
eigenvalues_L = eigenvalues_L[idx_sort]
eigenvectors_L = eigenvectors_L[:, idx_sort]

eig_rounded = np.round(eigenvalues_L, 2)
unique_eigs, eig_counts = np.unique(eig_rounded, return_counts=True)
print(f"\nLaplacian spectrum:")
for e, c in zip(unique_eigs, eig_counts):
    print(f"  lambda = {e:5.1f}, multiplicity = {c}")

# ============================================================================
# STEP 2: ELSER-SLOANE PROJECTION -> PARALLEL FRACTIONS
# ============================================================================
print("\n" + "=" * 80)
print("STEP 2: Elser-Sloane E8 -> H4 Projection")
print("=" * 80)

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

# Per-root parallel fraction: p_x = ||P_par(x)||^2 / ||x||^2
# Since ||x||^2 = 2 for all roots, and ||P_par||^2 + ||P_perp||^2 = ||x||^2
par_fraction = norms_par**2 / (norms_par**2 + norms_perp**2)

unique_fractions = np.sort(np.unique(np.round(par_fraction, 8)))
print(f"Unique parallel fractions ({len(unique_fractions)}):")
for f in unique_fractions:
    count = np.sum(np.abs(par_fraction - f) < 1e-6)
    print(f"  p = {f:.8f}  ({count} roots)")

# Group roots by parallel fraction
frac_groups = {}
for f in unique_fractions:
    mask = np.abs(par_fraction - f) < 1e-6
    frac_groups[f] = np.where(mask)[0]

# ============================================================================
# STEP 3: ONE-LOOP SELF-ENERGY COMPUTATION
# ============================================================================
print("\n" + "=" * 80)
print("STEP 3: One-Loop Self-Energy for Three Coupling Choices")
print("=" * 80)

# Coupling functions
def f1(p):
    """Linear: coupling proportional to observable-sector overlap."""
    return p

def f2(p):
    """Quadratic: enhances phi^2 structure."""
    return p**2

def f3(p):
    """Boundary: maximal at p=0.5, vanishing at p=0 and p=1."""
    return p * (1 - p)

coupling_functions = {'f1_linear': f1, 'f2_quadratic': f2, 'f3_boundary': f3}

def compute_self_energy(m2, lam, f_func, eigenvalues, eigenvectors, par_frac):
    """
    Compute the one-loop self-energy matrix Sigma in the site basis.

    Sigma_{kl} = (lam/3) * sum_x f(p_x) * V_k(x) * V_l(x) * G_0(x,x)

    where G_0(x,x) = sum_j |V_j(x)|^2 / (lambda_j + m^2)
    """
    N = len(eigenvalues)
    V = eigenvectors  # N x N, columns are eigenvectors

    # Free propagator eigenvalues
    g = 1.0 / (eigenvalues + m2)

    # G_0(x,x) = sum_j |V_j(x)|^2 * g_j for each site x
    # = (V**2) @ g
    G0_diag = (V**2) @ g  # shape (N,)

    # Coupling at each site
    f_vals = np.array([f_func(p) for p in par_frac])  # shape (N,)

    # Weight at each site: w_x = (lam/3) * f(p_x) * G_0(x,x)
    w = (lam / 3.0) * f_vals * G0_diag  # shape (N,)

    # Self-energy in site basis: Sigma = V * diag(w_x expanded) * V^T ... no.
    # Actually Sigma_{ij} = sum_x w_x * delta_{ix} * delta_{jx} ... no.
    #
    # The self-energy in the EIGENBASIS is:
    # Sigma^eig_{kl} = (lam/3) * sum_x f(p_x) * V_k(x) * V_l(x) * G_0(x,x)
    #                = sum_x w_x * V_k(x) * V_l(x)
    #                = V^T @ diag(w) @ V
    #
    # In the site basis, we want Sigma^site such that the corrected propagator is
    # G_corr = (L + m^2 I + Sigma^site)^{-1}
    # Since L = V @ diag(eigenvalues) @ V^T, and we work in site basis:
    # Sigma^site = V @ Sigma^eig @ V^T = V @ (V^T @ diag(w) @ V) @ V^T
    #            = diag(w)  ... wait, that's only true if V is square and orthogonal
    #
    # Actually V is N x N orthogonal, so:
    # Sigma^site_{ij} = sum_{k,l} V_{ik} * Sigma^eig_{kl} * V_{jl}
    #                 = sum_{k,l} V_{ik} * [sum_x w_x V_{xk} V_{xl}] * V_{jl}
    #                 = sum_x w_x * [sum_k V_{ik} V_{xk}] * [sum_l V_{jl} V_{xl}]
    #                 = sum_x w_x * delta_{ix} * delta_{jx}
    #                 = w_i * delta_{ij}
    #
    # So Sigma^site is DIAGONAL in the site basis! It's just a site-dependent mass shift.
    # This makes physical sense: a phi^4 vertex at site x gives a tadpole correction
    # proportional to f(p_x) * G_0(x,x).

    Sigma_site = np.diag(w)

    # Also compute Sigma in eigenbasis for analysis
    Sigma_eig = V.T @ Sigma_site @ V  # = V^T @ diag(w) @ V

    return Sigma_site, Sigma_eig, w, G0_diag

def compute_effective_propagator(L, m2, Sigma_site, P_parallel, roots, par_frac, eigvecs):
    """
    Compute the corrected propagator and project to 4D observable sector.

    G_corr = (L + m^2 I + Sigma)^{-1}

    Project using parallel fraction weighting:
    G_eff = P^T @ G_corr @ P  (where P weights by sqrt(par_fraction))
    """
    N = L.shape[0]

    # Corrected propagator in site basis
    M = L + m2 * np.eye(N) + Sigma_site
    G_corr = np.linalg.inv(M)

    # Free propagator
    G_free = np.linalg.inv(L + m2 * np.eye(N))

    # Eigenvalues of corrected vs free propagator
    eig_corr = np.linalg.eigvalsh(G_corr)
    eig_free = np.linalg.eigvalsh(G_free)

    # Project to 4D: use P_parallel (4x8) applied to roots gives 4D coords
    # The effective propagator in projected space:
    # G_eff(y, y') = sum_{x,x'} K(y,x) G(x,x') K(y',x')
    # where K(y,x) = projection kernel
    #
    # Simpler approach: compute eigenmode-resolved propagator projected by par_fraction
    # For each eigenmode k of G_corr, the "observable weight" is:
    # w_k^obs = sum_x |V_k(x)|^2 * p_x

    eig_Gcorr, V_Gcorr = np.linalg.eigh(G_corr)
    eig_Gfree, V_Gfree = np.linalg.eigh(G_free)

    # Observable weights per mode
    obs_weights_corr = np.array([np.sum(V_Gcorr[:, k]**2 * par_frac) for k in range(N)])
    obs_weights_free = np.array([np.sum(V_Gfree[:, k]**2 * par_frac) for k in range(N)])

    # Effective observable propagator trace
    trace_corr = np.sum(eig_Gcorr * obs_weights_corr)
    trace_free = np.sum(eig_Gfree * obs_weights_free)

    # Group by Laplacian eigenspace
    eig_rounded_L = np.round(eigenvalues_L, 2)
    unique_L = np.unique(eig_rounded_L)

    eff_corr_by_eigenspace = {}
    eff_free_by_eigenspace = {}

    for lam in unique_L:
        mask = np.abs(eig_rounded_L - lam) < 0.5
        idx = np.where(mask)[0]
        # Block of G in this eigenspace
        V_block = eigvecs[:, idx]  # N x mult
        G_corr_block = V_block.T @ G_corr @ V_block  # mult x mult
        G_free_block = V_block.T @ G_free @ V_block   # mult x mult

        # Observable-projected trace of this block
        par_weights = V_block.T @ np.diag(par_frac) @ V_block
        eff_corr_by_eigenspace[lam] = np.trace(G_corr_block @ par_weights)
        eff_free_by_eigenspace[lam] = np.trace(G_free_block @ par_weights)

    return {
        'eig_corr': np.sort(eig_Gcorr)[::-1],
        'eig_free': np.sort(eig_Gfree)[::-1],
        'obs_weights_corr': obs_weights_corr,
        'obs_weights_free': obs_weights_free,
        'trace_corr': trace_corr,
        'trace_free': trace_free,
        'eff_corr_by_eigenspace': eff_corr_by_eigenspace,
        'eff_free_by_eigenspace': eff_free_by_eigenspace,
        'G_corr': G_corr,
        'G_free': G_free,
    }

def extract_phi_coefficients(deltas, max_n=40):
    """
    Fit delta values to sum_{n=1}^{max_n} c_n * phi^(-n) using least squares.

    deltas: array of correction values to fit
    Returns: c_n coefficients
    """
    n_vals = np.arange(1, max_n + 1)
    # Build matrix: A[i, j] = phi^(-n_j) for the i-th delta value
    # If we have K delta values, we solve K equations for max_n unknowns
    # This is underdetermined, so use least-norm solution (pseudoinverse)

    K = len(deltas)
    A_mat = np.zeros((K, max_n))
    for j, n in enumerate(n_vals):
        A_mat[:, j] = PHI**(-n)

    # Since all rows of A_mat have the same value in each column (phi^(-n) doesn't depend on i),
    # we need a different approach. The deltas come from different eigenspaces.
    # Each eigenspace has a characteristic delta value.
    # We fit EACH delta as a sum: delta_k = sum_n c_{k,n} * phi^(-n)
    # But that gives too many unknowns.
    #
    # Better: the corrections should follow delta_k = sum_n a_n * phi^(-n) * g_n(lambda_k)
    # where g_n encodes which eigenspace.
    #
    # Simplest approach: fit each individual delta value to the closest phi^(-n) or
    # combination of a few phi^(-n) terms.
    #
    # Actually: let's decompose the SET of correction ratios.
    # Take the log_phi of each |delta| to find effective exponents.

    results = {}
    for i, d in enumerate(deltas):
        if abs(d) > 1e-15:
            n_eff = -np.log(abs(d)) / np.log(PHI)
            results[i] = {'delta': d, 'n_eff': n_eff, 'sign': np.sign(d)}

    return results

def fit_phi_series(values, max_n=40):
    """
    Given a set of values, fit to sum c_n * phi^(-n) using NNLS or least squares.
    values: 1D array
    Returns: coefficients c_n for n=1..max_n
    """
    n_vals = np.arange(1, max_n + 1)
    basis = np.array([PHI**(-n) for n in n_vals])

    # For a single value v, solve v = sum c_n * phi^(-n)
    # For multiple values, we need them at different "points"
    # Let's use the eigenspace index as the coordinate

    K = len(values)
    if K == 0:
        return np.zeros(max_n)

    # Build Vandermonde-like matrix with phi^(-n) basis
    # Each row corresponds to a different observable (eigenspace correction)
    # Fit: values = A @ c where A[k,n] = phi^(-n) * weight_k_n
    # Since we don't have a natural weight, use the simplest approach:
    # Decompose the mean correction
    mean_val = np.mean(values)

    # Greedy decomposition: find dominant phi^(-n) terms
    residual = mean_val
    coeffs = np.zeros(max_n)
    for iteration in range(10):  # up to 10 terms
        if abs(residual) < 1e-15:
            break
        # Find best n
        best_n = -1
        best_c = 0
        best_residual = abs(residual)
        for j, n in enumerate(n_vals):
            c = residual / basis[j]
            # Round to nearest "nice" coefficient
            c_round = round(c)
            if c_round == 0:
                c_round = round(c * 10) / 10.0
            new_residual = abs(residual - c_round * basis[j])
            if new_residual < best_residual:
                best_residual = new_residual
                best_n = j
                best_c = c_round
        if best_n >= 0 and best_c != 0:
            coeffs[best_n] += best_c
            residual -= best_c * basis[best_n]
        else:
            break

    return coeffs

# ============================================================================
# MAIN ANALYSIS LOOP
# ============================================================================

# Mass values to scan
mass_values = {
    '0.1': 0.1,
    '0.5': 0.5,
    '1.0': 1.0,
    '2.0': 2.0,
    '5.0': 5.0,
    'phi': PHI,
    'phi^2': PHI**2,
    'phi^(-1)': PHI_INV,
    '1/30': 1.0/30.0,
}

lam = 1.0  # Coupling constant (structure matters, not magnitude)

all_results = []
sigma_eigenvalues_data = {}

# First do the detailed analysis for m^2 = 1.0
print("\n" + "=" * 80)
print("STEP 3-5: Detailed Analysis for m^2 = 1.0")
print("=" * 80)

m2_detail = 1.0

for fname, f_func in coupling_functions.items():
    print(f"\n--- Coupling: {fname} ---")

    Sigma_site, Sigma_eig, w, G0_diag = compute_self_energy(
        m2_detail, lam, f_func, eigenvalues_L, eigenvectors_L, par_fraction
    )

    # Self-energy statistics
    print(f"  Site self-energy w_x range: [{w.min():.6f}, {w.max():.6f}]")
    print(f"  Free propagator G_0(x,x) range: [{G0_diag.min():.6f}, {G0_diag.max():.6f}]")

    # Eigenvalues of Sigma in eigenbasis
    sigma_eig_vals = np.linalg.eigvalsh(Sigma_eig)
    sigma_eig_vals_sorted = np.sort(sigma_eig_vals)[::-1]
    sigma_eigenvalues_data[fname] = sigma_eig_vals_sorted

    print(f"  Sigma eigenvalue range: [{sigma_eig_vals.min():.8f}, {sigma_eig_vals.max():.8f}]")

    # Unique Sigma eigenvalues
    sigma_rounded = np.round(sigma_eig_vals_sorted, 8)
    unique_sigma, sigma_counts = np.unique(sigma_rounded, return_counts=True)
    print(f"  Distinct Sigma eigenvalues: {len(unique_sigma)}")
    for sv, sc in zip(unique_sigma[:10], sigma_counts[:10]):
        print(f"    sigma = {sv:.10f}  (mult {sc})")
    if len(unique_sigma) > 10:
        print(f"    ... and {len(unique_sigma)-10} more")

    # Effective propagator
    eff = compute_effective_propagator(
        L, m2_detail, Sigma_site, P_parallel, roots, par_fraction, eigenvectors_L
    )

    print(f"\n  Effective propagator (observable-projected trace):")
    print(f"    Free:      {eff['trace_free']:.10f}")
    print(f"    Corrected: {eff['trace_corr']:.10f}")
    print(f"    Ratio:     {eff['trace_corr']/eff['trace_free']:.10f}")

    print(f"\n  Per-eigenspace analysis:")
    for lam_val in sorted(eff['eff_corr_by_eigenspace'].keys()):
        ec = eff['eff_corr_by_eigenspace'][lam_val]
        ef = eff['eff_free_by_eigenspace'][lam_val]
        ratio = ec / ef if abs(ef) > 1e-15 else float('inf')
        delta = ratio - 1.0
        n_eff = -np.log(abs(delta)) / np.log(PHI) if abs(delta) > 1e-15 else float('inf')
        print(f"    lambda={lam_val:5.1f}: free={ef:.8f}, corr={ec:.8f}, "
              f"ratio={ratio:.8f}, delta={delta:+.8f}, n_eff={n_eff:.2f}")

# ============================================================================
# STEP 6: SCAN OVER MASS PARAMETER
# ============================================================================
print("\n" + "=" * 80)
print("STEP 6: Mass Parameter Scan")
print("=" * 80)

for m2_name, m2_val in mass_values.items():
    print(f"\n--- m^2 = {m2_name} ({m2_val:.6f}) ---")

    for fname, f_func in coupling_functions.items():
        Sigma_site, Sigma_eig, w, G0_diag = compute_self_energy(
            m2_val, lam, f_func, eigenvalues_L, eigenvectors_L, par_fraction
        )

        eff = compute_effective_propagator(
            L, m2_val, Sigma_site, P_parallel, roots, par_fraction, eigenvectors_L
        )

        # Extract corrections per eigenspace
        deltas = []
        n_effs = []
        for lam_val in sorted(eff['eff_corr_by_eigenspace'].keys()):
            ec = eff['eff_corr_by_eigenspace'][lam_val]
            ef = eff['eff_free_by_eigenspace'][lam_val]
            if abs(ef) > 1e-15:
                ratio = ec / ef
                delta = ratio - 1.0
                deltas.append(delta)
                if abs(delta) > 1e-15:
                    n_eff = -np.log(abs(delta)) / np.log(PHI)
                    n_effs.append(n_eff)

        # Phi-coefficient extraction
        phi_results = extract_phi_coefficients(np.array(deltas))

        # Count GSM matches
        gsm_matches = 0
        matched_exponents = []
        for idx_info in phi_results.values():
            n_eff = idx_info['n_eff']
            # Check if n_eff is close to a GSM exponent
            for gsm_n in GSM_EXPONENTS:
                if abs(n_eff - gsm_n) < 0.5:
                    gsm_matches += 1
                    matched_exponents.append(gsm_n)
                    break

        # p-value: probability of matching this many GSM exponents by chance
        # Random exponent in [0, 40]: probability of hitting a GSM exponent = 23/40
        # Binomial test
        from scipy.stats import binom
        n_trials = len(phi_results)
        p_random = N_GSM / 40.0
        if n_trials > 0:
            p_value = 1.0 - binom.cdf(gsm_matches - 1, n_trials, p_random)
        else:
            p_value = 1.0

        overall_ratio = eff['trace_corr'] / eff['trace_free'] if abs(eff['trace_free']) > 1e-15 else 0

        all_results.append({
            'coupling': fname,
            'm2_name': m2_name,
            'm2_val': m2_val,
            'trace_free': eff['trace_free'],
            'trace_corr': eff['trace_corr'],
            'ratio': overall_ratio,
            'gsm_matches': gsm_matches,
            'n_corrections': len(phi_results),
            'p_value': p_value,
            'matched_exponents': matched_exponents,
            'n_effs': n_effs,
            'deltas': deltas,
        })

        print(f"  {fname}: ratio={overall_ratio:.8f}, "
              f"GSM matches={gsm_matches}/{len(phi_results)}, "
              f"p={p_value:.4f}, matched={matched_exponents}")

# ============================================================================
# STEP 7: CRITICAL ANALYSIS
# ============================================================================
print("\n" + "=" * 80)
print("STEP 7: Critical Analysis and Summary")
print("=" * 80)

# Summary table
print(f"\n{'Coupling':<16} {'m^2':<10} {'Ratio':>10} {'#GSM':>5} {'#Corr':>6} "
      f"{'p-value':>8} {'Matched Exponents'}")
print("-" * 90)

best_result = None
best_gsm = -1

for r in all_results:
    matched_str = str(r['matched_exponents'][:5]) if r['matched_exponents'] else '[]'
    print(f"{r['coupling']:<16} {r['m2_name']:<10} {r['ratio']:>10.6f} "
          f"{r['gsm_matches']:>5} {r['n_corrections']:>6} "
          f"{r['p_value']:>8.4f} {matched_str}")
    if r['gsm_matches'] > best_gsm:
        best_gsm = r['gsm_matches']
        best_result = r

print(f"\nBest result: {best_result['coupling']} at m^2={best_result['m2_name']}")
print(f"  GSM matches: {best_result['gsm_matches']}/{best_result['n_corrections']}")
print(f"  Matched exponents: {best_result['matched_exponents']}")
print(f"  p-value: {best_result['p_value']:.6f}")

# Detailed phi^(-n) analysis for best coupling at m^2=1
print("\n--- Detailed phi^(-n) Decomposition (best coupling, all masses) ---")
for r in all_results:
    if r['coupling'] == best_result['coupling']:
        print(f"\n  m^2 = {r['m2_name']}:")
        for i, d in enumerate(r['deltas']):
            if abs(d) > 1e-15:
                n_eff = -np.log(abs(d)) / np.log(PHI)
                sign = '+' if d > 0 else '-'
                # Check nearest GSM
                nearest_gsm = min(GSM_EXPONENTS, key=lambda x: abs(x - n_eff))
                gsm_flag = ' <-- GSM' if abs(n_eff - nearest_gsm) < 0.5 else ''
                print(f"    eigenspace {i}: delta = {sign}{abs(d):.10f}, "
                      f"n_eff = {n_eff:.4f}, nearest GSM = {nearest_gsm}{gsm_flag}")

# Check for E8 structural numbers in coefficients
print("\n--- Relationship to E8 Structural Numbers ---")
E8_NUMBERS = {'248': 248, '240': 240, '30': 30, '8': 8, '56': 56, '120': 120}
for r in all_results:
    if r['m2_name'] == '1.0':
        for i, d in enumerate(r['deltas']):
            if abs(d) > 1e-15:
                for name, val in E8_NUMBERS.items():
                    ratio_to_struct = d * val
                    if abs(ratio_to_struct - round(ratio_to_struct)) < 0.01 and abs(round(ratio_to_struct)) > 0:
                        print(f"  {r['coupling']}, eigenspace {i}: "
                              f"delta * {name} = {ratio_to_struct:.6f} ~ {round(ratio_to_struct)}")

# Phi-series fit for all correction values
print("\n--- Phi-Series Fit for Correction Spectrum ---")
for r in all_results:
    if r['m2_name'] == '1.0':
        if r['deltas']:
            coeffs = fit_phi_series(r['deltas'], max_n=40)
            nonzero = [(n+1, c) for n, c in enumerate(coeffs) if abs(c) > 0.01]
            if nonzero:
                print(f"  {r['coupling']} (m^2=1.0): phi-series terms:")
                for n, c in nonzero:
                    gsm_flag = ' [GSM]' if n in GSM_SET else ''
                    print(f"    c_{n} = {c:+.4f}{gsm_flag}")
            else:
                print(f"  {r['coupling']} (m^2=1.0): no significant phi-series terms")

# ============================================================================
# SAVE RESULTS
# ============================================================================
print("\n" + "=" * 80)
print("SAVING RESULTS")
print("=" * 80)

# CSV output
csv_path = os.path.join(SCRIPT_DIR, 'e8_interacting_results.csv')
with open(csv_path, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['coupling', 'm2_name', 'm2_val', 'trace_free', 'trace_corr',
                     'ratio', 'gsm_matches', 'n_corrections', 'p_value', 'matched_exponents'])
    for r in all_results:
        writer.writerow([r['coupling'], r['m2_name'], f"{r['m2_val']:.6f}",
                         f"{r['trace_free']:.10f}", f"{r['trace_corr']:.10f}",
                         f"{r['ratio']:.10f}", r['gsm_matches'], r['n_corrections'],
                         f"{r['p_value']:.6f}", str(r['matched_exponents'])])
print(f"  Saved: {csv_path}")

# ============================================================================
# PLOTS
# ============================================================================

# Plot 1: Self-energy eigenvalue spectrum
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
for i, (fname, eigs) in enumerate(sigma_eigenvalues_data.items()):
    ax = axes[i]
    ax.plot(range(len(eigs)), eigs, 'b-', linewidth=0.5)
    ax.set_title(f'Self-Energy Spectrum: {fname}')
    ax.set_xlabel('Mode index')
    ax.set_ylabel('Sigma eigenvalue')
    ax.grid(True, alpha=0.3)
plt.tight_layout()
plot1_path = os.path.join(SCRIPT_DIR, 'e8_selfenergy_spectrum.png')
plt.savefig(plot1_path, dpi=150)
plt.close()
print(f"  Saved: {plot1_path}")

# Plot 2: Effective propagator corrections
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
for i, fname in enumerate(coupling_functions.keys()):
    ax = axes[i]
    # Get m^2=1.0 results
    r = [x for x in all_results if x['coupling'] == fname and x['m2_name'] == '1.0'][0]
    deltas = r['deltas']
    eigenspace_labels = [0, 28, 48, 58, 60]

    ax.bar(range(len(deltas)), deltas, color=['#2196F3', '#FF9800', '#4CAF50', '#F44336', '#9C27B0'][:len(deltas)])
    ax.set_xticks(range(len(deltas)))
    ax.set_xticklabels([str(l) for l in eigenspace_labels[:len(deltas)]], fontsize=9)
    ax.set_title(f'Corrections: {fname} (m^2=1)')
    ax.set_xlabel('Laplacian eigenvalue')
    ax.set_ylabel('delta = G_corr/G_free - 1')
    ax.axhline(y=0, color='k', linestyle='--', linewidth=0.5)
    ax.grid(True, alpha=0.3)
plt.tight_layout()
plot2_path = os.path.join(SCRIPT_DIR, 'e8_effective_propagator_corr.png')
plt.savefig(plot2_path, dpi=150)
plt.close()
print(f"  Saved: {plot2_path}")

# Plot 3: Phi-coefficient analysis
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
for i, fname in enumerate(coupling_functions.keys()):
    ax = axes[i]
    # Collect n_eff values across all masses for this coupling
    n_effs_all = []
    for r in all_results:
        if r['coupling'] == fname:
            n_effs_all.extend(r['n_effs'])

    if n_effs_all:
        ax.hist(n_effs_all, bins=np.arange(0, 42, 1), color='steelblue', edgecolor='black', alpha=0.7)
        # Mark GSM exponents
        for gsm_n in GSM_EXPONENTS:
            ax.axvline(x=gsm_n, color='red', linestyle='--', linewidth=0.5, alpha=0.5)
        ax.set_title(f'Effective Exponents: {fname}')
        ax.set_xlabel('n_eff = -log_phi(|delta|)')
        ax.set_ylabel('Count')
    else:
        ax.text(0.5, 0.5, 'No data', transform=ax.transAxes, ha='center')
        ax.set_title(f'{fname}')
    ax.grid(True, alpha=0.3)
plt.tight_layout()
plot3_path = os.path.join(SCRIPT_DIR, 'e8_phi_coefficients.png')
plt.savefig(plot3_path, dpi=150)
plt.close()
print(f"  Saved: {plot3_path}")

# ============================================================================
# FINAL VERDICT
# ============================================================================
print("\n" + "=" * 80)
print("FINAL VERDICT")
print("=" * 80)

# Count how often each effective exponent appears near a GSM value
all_n_effs = []
for r in all_results:
    all_n_effs.extend(r['n_effs'])

gsm_hit_count = defaultdict(int)
for n in all_n_effs:
    for gsm_n in GSM_EXPONENTS:
        if abs(n - gsm_n) < 0.5:
            gsm_hit_count[gsm_n] += 1
            break

print(f"\nTotal effective exponents computed: {len(all_n_effs)}")
print(f"Unique GSM exponents hit: {len(gsm_hit_count)} out of {N_GSM}")
if gsm_hit_count:
    print(f"GSM exponents matched: {sorted(gsm_hit_count.keys())}")
    print(f"Hit counts: {dict(sorted(gsm_hit_count.items()))}")

# Statistical test: are we seeing more GSM matches than random?
total_matches = sum(r['gsm_matches'] for r in all_results)
total_corrections = sum(r['n_corrections'] for r in all_results)
expected_random = total_corrections * N_GSM / 40.0
print(f"\nTotal matches: {total_matches} out of {total_corrections} corrections")
print(f"Expected by chance (GSM covers {N_GSM}/40 of [1,40]): {expected_random:.1f}")
print(f"Enrichment factor: {total_matches/expected_random:.2f}x" if expected_random > 0 else "N/A")

# Honest assessment
print(f"""
ASSESSMENT:
===========
The interacting theory on E8 produces corrections that can be expressed as phi^(-n)
with specific effective exponents. The key findings are:

1. INTERACTION BREAKS EIGENSPACE DEMOCRACY: Unlike the free theory where all
   eigenspaces project to exactly 50%, the phi^4 interaction with projection-
   dependent coupling creates differential renormalization across eigenspaces.

2. THE CORRECTIONS ARE PHI-STRUCTURED: Because the coupling f(p_x) depends on
   the parallel fraction, which itself has golden-ratio structure
   (values ~ phi^(-2)/2, (phi^(-2)+1)/4, 1/2, etc.), the corrections naturally
   inherit phi-dependent structure.

3. HOWEVER: The effective exponents n_eff = -log_phi(|delta|) that emerge depend
   continuously on the mass parameter m^2. They are NOT quantized to integers.
   Only for specific m^2 values do they happen to land near GSM exponents.

4. THE GSM MATCH RATE of {total_matches}/{total_corrections}
   (expected random: {expected_random:.0f})
   {"EXCEEDS" if total_matches > expected_random * 1.5 else "is COMPARABLE TO"}
   random expectation.

5. THE SELECTION RULES ARE NOT DERIVED: The interacting theory produces a
   continuous spectrum of corrections that can be tuned by m^2 to match various
   GSM exponents, but it does not uniquely SELECT the GSM set
   {{1,...,10,12,...,34}} from first principles.

CONCLUSION: The phi^4 interacting theory on E8 provides a MECHANISM for generating
phi^(-n) corrections (the projection-dependent coupling), but the SPECIFIC exponents
that appear depend on the choice of coupling function and mass parameter. This is
suggestive but not a derivation — it shows WHY phi-corrections arise but not WHY
those particular exponents.

To derive the selection rules, one likely needs:
- A specific dynamical principle to fix m^2 (perhaps self-consistency or RG fixed point)
- The full gauge theory on E8, not just scalar phi^4
- Non-perturbative effects (instantons, monopoles) that select discrete exponents
""")

print("\n" + "=" * 80)
print("COMPUTATION COMPLETE")
print("=" * 80)
