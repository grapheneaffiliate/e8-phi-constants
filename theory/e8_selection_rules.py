#!/usr/bin/env python
"""
E8 Selection Rules for the Geometric Standard Model (GSM)
==========================================================

Derives which phi^(-n) exponents are allowed in GSM correction formulas
by computing the spectral theory of the E8 root lattice projected to 4D
via the E8 -> H4 icosahedral projection.

Four computations:
  1. E8 root system and graph Laplacian spectrum
  2. E8 -> H4 projection and mode filtering
  3. Connecting the spectrum to phi-exponents
  4. Effective coupling constants

Dependencies: numpy, scipy, matplotlib
"""

import numpy as np
from scipy import linalg as la
from itertools import combinations, product
import csv
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Golden ratio
PHI = (1 + np.sqrt(5)) / 2

# GSM exponents that appear in formulas
GSM_EXPONENTS = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17, 18, 20, 24, 26, 27, 33, 34}

# E8 Casimir degrees and Coxeter exponents
E8_CASIMIR = {2, 8, 12, 14, 18, 20, 24, 30}
E8_COXETER_EXP = {1, 7, 11, 13, 17, 19, 23, 29}
H4_COXETER_EXP = {1, 11, 19, 29}

print("=" * 80)
print("E8 SELECTION RULES FOR THE GEOMETRIC STANDARD MODEL")
print("=" * 80)

# ============================================================================
# COMPUTATION 1: E8 Root System and Lattice Laplacian
# ============================================================================
print("\n" + "=" * 80)
print("COMPUTATION 1: E8 Root System and Graph Laplacian")
print("=" * 80)

# --- Build the 240 roots of E8 ---

roots = []

# Type 1: 112 roots — permutations of (+-1, +-1, 0, 0, 0, 0, 0, 0)
# Choose 2 positions out of 8, then choose signs for each
for pos in combinations(range(8), 2):
    for signs in product([-1, 1], repeat=2):
        v = np.zeros(8)
        v[pos[0]] = signs[0]
        v[pos[1]] = signs[1]
        roots.append(v)

print(f"Type 1 roots (permutations of +-1,+-1,0,...,0): {len(roots)}")
assert len(roots) == 112, f"Expected 112, got {len(roots)}"

# Type 2: 128 roots — (+-1/2)^8 with even number of minus signs
for signs in product([-0.5, 0.5], repeat=8):
    v = np.array(signs)
    # Count number of negative entries
    n_neg = sum(1 for s in signs if s < 0)
    if n_neg % 2 == 0:
        roots.append(v)

n_type2 = len(roots) - 112
print(f"Type 2 roots (half-integer, even minus): {n_type2}")
assert n_type2 == 128, f"Expected 128, got {n_type2}"

roots = np.array(roots)
N = len(roots)
print(f"\nTotal roots: {N}")
assert N == 240, f"Expected 240, got {N}"

# Verify all norms are sqrt(2)
norms = np.linalg.norm(roots, axis=1)
print(f"Norm range: [{norms.min():.6f}, {norms.max():.6f}] (expected sqrt(2) = {np.sqrt(2):.6f})")
assert np.allclose(norms, np.sqrt(2)), "Not all roots have norm sqrt(2)!"
print("  [PASS] All 240 roots have norm sqrt(2)")

# --- Build adjacency matrix ---
# A[i,j] = 1 if <r_i, r_j> = 1  (nearest neighbors)
print("\nBuilding adjacency matrix (inner product = 1 criterion)...")
dot_matrix = roots @ roots.T
A = (np.abs(dot_matrix - 1.0) < 1e-10).astype(int)

# Check: no self-loops
np.fill_diagonal(A, 0)

# Verify kissing number = 56
degrees = A.sum(axis=1)
print(f"Degree (neighbors per root): min={degrees.min()}, max={degrees.max()}, mean={degrees.mean():.1f}")
assert np.all(degrees == 56), f"Expected all degrees = 56, got unique values {np.unique(degrees)}"
print("  [PASS] Every root has exactly 56 neighbors (E8 kissing number property)")

# Verify symmetry
assert np.allclose(A, A.T), "Adjacency matrix is not symmetric!"
print("  [PASS] Adjacency matrix is symmetric")

# --- Graph Laplacian ---
print("\nComputing graph Laplacian L = D - A ...")
D = np.diag(degrees)
L = D - A

# Eigenvalues of Laplacian
print("Computing eigenvalues of 240x240 Laplacian...")
eig_L = np.linalg.eigvalsh(L.astype(float))
eig_L = np.sort(eig_L)

# Also compute adjacency eigenvalues for reference
print("Computing eigenvalues of adjacency matrix...")
eig_A = np.linalg.eigvalsh(A.astype(float))
eig_A = np.sort(eig_A)[::-1]  # descending

# Round to remove numerical noise
eig_L_rounded = np.round(eig_L, 6)
eig_A_rounded = np.round(eig_A, 6)

# Find unique eigenvalues and multiplicities
unique_L, counts_L = np.unique(eig_L_rounded, return_counts=True)
unique_A, counts_A = np.unique(eig_A_rounded, return_counts=True)

print(f"\n--- Laplacian Spectrum (L = D - A) ---")
print(f"{'Eigenvalue':>12s}  {'Multiplicity':>12s}")
print("-" * 28)
for val, cnt in zip(unique_L, counts_L):
    print(f"{val:12.4f}  {cnt:12d}")
print(f"Total: {counts_L.sum()}")

print(f"\n--- Adjacency Spectrum ---")
print(f"{'Eigenvalue':>12s}  {'Multiplicity':>12s}")
print("-" * 28)
for val, cnt in zip(unique_A[::-1], counts_A[::-1]):
    print(f"{val:12.4f}  {cnt:12d}")
print(f"Total: {counts_A.sum()}")

# Note the relationship L = 56*I - A, so lambda_L = 56 - lambda_A
print(f"\nRelation check: L = {int(degrees[0])}*I - A")
print(f"  Laplacian eigenvalues = {int(degrees[0])} - (adjacency eigenvalues)")
for la_val, cnt in zip(unique_L, counts_L):
    corresponding_adj = degrees[0] - la_val
    print(f"  L_eig={la_val:8.2f} (mult {cnt:3d}) <-> A_eig={corresponding_adj:8.2f}")

# ============================================================================
# COMPUTATION 2: E8 -> H4 Projection and Mode Filtering
# ============================================================================
print("\n" + "=" * 80)
print("COMPUTATION 2: E8 -> H4 Projection and Mode Filtering")
print("=" * 80)

# The E8 -> H4 projection uses the Elser-Sloane construction.
# The 8D space splits into two 4D subspaces related by the golden ratio.
# The projection matrix is built from the eigenvectors of the E8 Cartan matrix
# that correspond to the H4 subalgebra.
#
# Standard construction: The 8x8 orthogonal matrix R block-diagonalizes
# into two 4x4 blocks. The key: R involves entries with 1/sqrt(2),
# and the golden ratio phi appears in the splitting.
#
# We use the Elser-Sloane projection matrix explicitly.
# The 4x8 projection to the "parallel" (observable) subspace:

# The Elser-Sloane projection for E8 -> H4:
# Based on the icosahedral decomposition of E8
# The 8 coordinates split into pairs: (1,2), (3,4), (5,6), (7,8)
# Each pair maps to one 4D coordinate via: x_k = a_2k-1 + phi*a_2k (parallel)
# or x_k = a_2k-1 - (1/phi)*a_2k (perpendicular)

# Normalization factor
norm_par = 1.0 / np.sqrt(1 + PHI**2)
norm_perp = 1.0 / np.sqrt(1 + 1.0/PHI**2)

# Build 4x8 projection matrices
P_parallel = np.zeros((4, 8))
P_perp = np.zeros((4, 8))
for k in range(4):
    P_parallel[k, 2*k]   = norm_par * 1.0
    P_parallel[k, 2*k+1] = norm_par * PHI
    P_perp[k, 2*k]       = norm_perp * 1.0
    P_perp[k, 2*k+1]     = norm_perp * (-1.0/PHI)

print("Projection matrices constructed (Elser-Sloane type)")
print(f"  P_parallel: {P_parallel.shape}")
print(f"  P_perp:     {P_perp.shape}")

# Project all 240 roots
proj_par = (P_parallel @ roots.T).T   # (240, 4)
proj_perp = (P_perp @ roots.T).T       # (240, 4)

# Check norms
norms_par = np.linalg.norm(proj_par, axis=1)
norms_perp = np.linalg.norm(proj_perp, axis=1)

print(f"\nProjected norms (parallel):  min={norms_par.min():.6f}, max={norms_par.max():.6f}")
print(f"Projected norms (perp):      min={norms_perp.min():.6f}, max={norms_perp.max():.6f}")

# Identify the two sectors:
# Roots that project to "large" in parallel and "small" in perp = observable (600-cell)
# Roots that project to "small" in parallel and "large" in perp = hidden (dual 600-cell)
# The ratio of norms should involve phi

ratio = norms_par / norms_perp
print(f"Norm ratio (par/perp): unique values ~ {np.unique(np.round(ratio, 4))}")

# Classify roots
# In the Elser-Sloane projection, the 240 roots split based on their projection properties
# Let's check how many distinct projected points we get
proj_par_rounded = np.round(proj_par, 8)
unique_par = np.unique(proj_par_rounded, axis=0)
print(f"\nUnique projected points (parallel): {len(unique_par)}")

# For mode filtering, we need to project eigenvectors
# First compute full eigenvectors of L
print("\nComputing full eigendecomposition of Laplacian...")
eigenvalues_L, eigenvectors_L = np.linalg.eigh(L.astype(float))

# Sort
idx_sort = np.argsort(eigenvalues_L)
eigenvalues_L = eigenvalues_L[idx_sort]
eigenvectors_L = eigenvectors_L[:, idx_sort]

print(f"Eigendecomposition complete: {eigenvalues_L.shape[0]} eigenvalues")

# For each eigenmode v_k (240-dim vector, one component per root):
# The "projection weight" measures how much the mode is localized
# in the observable sector.
#
# Strategy: Each eigenvector v_k has 240 components (one per root).
# We can define the observable sector as the roots that project predominantly
# to the parallel subspace. But since ALL roots project to both subspaces
# (just with different weights), we use a continuous measure.
#
# The projection weight for mode k:
#   w_k = sum_i |v_k[i]|^2 * (||P_par * r_i||^2 / ||r_i||^2)
# This weights each root's contribution by how much it lives in the parallel subspace.

# Compute per-root parallel fraction
par_fraction = norms_par**2 / (norms_par**2 + norms_perp**2)
print(f"\nPer-root parallel fraction: {np.unique(np.round(par_fraction, 6))}")

# For each eigenmode, compute projection weight
n_modes = len(eigenvalues_L)
projection_weights = np.zeros(n_modes)

for k in range(n_modes):
    v = eigenvectors_L[:, k]
    # Weight = sum |v_i|^2 * par_fraction_i
    projection_weights[k] = np.sum(np.abs(v)**2 * par_fraction)

print(f"\nProjection weights: min={projection_weights.min():.6f}, max={projection_weights.max():.6f}")
print(f"Mean projection weight: {projection_weights.mean():.6f}")

# Alternative: use a sharper projection based on Fourier analysis on the root system
# For each eigenmode, project the mode pattern onto the 4D parallel subspace
# using the root positions as sampling points.
#
# The "spectral projection weight" for mode k:
# Compute the 4D Fourier transform of the mode at the projected positions
# w_k = || sum_i v_k[i] * exp(i * q . proj_par(r_i)) ||^2 for relevant q

# A better approach: use the representation-theoretic decomposition
# Under E8 -> H4, the 240-dim permutation representation decomposes into
# irreps of the H4 Weyl group. Modes in H4-compatible irreps survive.
#
# Practical approach: define the "H4 projection" of a mode as the component
# of the eigenvector that is symmetric under the H4 Weyl group action.

# Let's use a more direct approach:
# Build the representation of the H4 symmetry on the root indices.
# The H4 symmetry permutes the 240 roots. Modes that are invariant (or transform
# in specific representations) under H4 are the ones that survive projection.

# For now, use the geometric projection weight computed above,
# AND a second measure: the "4D localization" of each mode.

# Second measure: project the eigenvector pattern to 4D
# For each mode k, compute the effective 4D function by evaluating
# f_k(x) = sum_i v_k[i] * delta(x - P_par * r_i)
# The "4D content" is the L2 norm of this projected function,
# normalized by the total mode norm.

# This is essentially already captured by projection_weights above.
# Let's also compute a spectral measure based on the adjacency structure
# restricted to the projected graph.

# Build the projected adjacency: how connected are roots in the parallel projection?
# Two roots are "4D-connected" if their parallel projections are close
print("\nComputing 4D-projected connectivity...")
proj_distances = np.zeros((N, N))
for i in range(N):
    proj_distances[i] = np.linalg.norm(proj_par - proj_par[i], axis=1)

# Find the minimum nonzero distance in 4D projection
nonzero_dists = proj_distances[proj_distances > 1e-8]
min_proj_dist = nonzero_dists.min()
print(f"Minimum nonzero projected distance: {min_proj_dist:.6f}")

# Count how many roots coincide in projection
coincidence = (proj_distances < 1e-6).astype(int)
np.fill_diagonal(coincidence, 0)
coincident_counts = coincidence.sum(axis=1)
print(f"Coincident roots in projection: {np.unique(coincident_counts, return_counts=True)}")

# Group roots by their projected position
from collections import defaultdict
proj_groups = defaultdict(list)
for i in range(N):
    key = tuple(np.round(proj_par[i], 6))
    proj_groups[key].append(i)

n_groups = len(proj_groups)
group_sizes = [len(g) for g in proj_groups.values()]
print(f"Number of distinct projected positions: {n_groups}")
print(f"Group sizes: {sorted(set(group_sizes))}")

# For mode filtering, a mode "survives" projection if roots that map to the
# same 4D point have the same eigenvector component (constructive interference)
# vs cancellation (destructive interference).

# Compute the "coherent projection weight" for each mode
coherent_weights = np.zeros(n_modes)
group_list = list(proj_groups.values())

for k in range(n_modes):
    v = eigenvectors_L[:, k]
    total_power = 0.0
    for group in group_list:
        # Sum of eigenvector components for roots mapping to same 4D point
        group_sum = np.sum(v[group])
        total_power += group_sum**2
    coherent_weights[k] = total_power  # / np.sum(v**2) -- already normalized

print(f"\nCoherent projection weights: min={coherent_weights.min():.6f}, max={coherent_weights.max():.6f}")

# Combine weights
combined_weights = coherent_weights  # Use coherent weight as primary filter

# Report which eigenvalues survive
print(f"\n--- Mode Survival Analysis ---")
threshold = 1e-6
surviving = combined_weights > threshold
n_surviving = np.sum(surviving)
print(f"Modes surviving projection (coherent weight > {threshold}): {n_surviving}/{n_modes}")

surv_eigenvalues = eigenvalues_L[surviving]
surv_weights = combined_weights[surviving]
surv_unique = np.unique(np.round(surv_eigenvalues, 4))
print(f"Unique surviving eigenvalues: {len(surv_unique)}")
for val in surv_unique:
    mask = np.abs(np.round(eigenvalues_L, 4) - val) < 1e-4
    total_w = combined_weights[mask].sum()
    mult = mask.sum()
    surv_count = (mask & surviving).sum()
    print(f"  lambda={val:8.4f}  multiplicity={mult:3d}  surviving_modes={surv_count:3d}  total_weight={total_w:.6f}")

# ============================================================================
# COMPUTATION 3: Connecting Spectrum to Exponents
# ============================================================================
print("\n" + "=" * 80)
print("COMPUTATION 3: Connecting Spectrum to phi-Exponents")
print("=" * 80)

# The hypothesis: eigenvalues relate to phi^n for specific integers n.
# Several possible relations:
#   (a) lambda_k / lambda_max = phi^(-n)
#   (b) lambda_k / lambda_1 = phi^n  (relative to smallest nonzero)
#   (c) lambda_k itself is a simple expression in phi
#   (d) Ratios between eigenvalues are powers of phi

# Let's explore all of these

# Get unique nonzero eigenvalues
nonzero_mask = np.abs(unique_L) > 1e-4
nonzero_eigs = unique_L[nonzero_mask]
nonzero_mults = counts_L[nonzero_mask]

print("\n(a) Eigenvalue ratios to maximum eigenvalue:")
lambda_max = nonzero_eigs[-1]
print(f"    lambda_max = {lambda_max:.6f}")
for val, mult in zip(nonzero_eigs, nonzero_mults):
    ratio = val / lambda_max
    # Find n such that phi^(-n) ~ ratio
    if ratio > 1e-10:
        n_phi = -np.log(ratio) / np.log(PHI)
        print(f"    lambda={val:8.4f} (mult {mult:3d})  ratio={ratio:.6f}  phi-exp n={n_phi:.4f}")

print("\n(b) Eigenvalue ratios to minimum nonzero eigenvalue:")
lambda_min = nonzero_eigs[0]
print(f"    lambda_min = {lambda_min:.6f}")
for val, mult in zip(nonzero_eigs, nonzero_mults):
    ratio = val / lambda_min
    if ratio > 1e-10:
        n_phi = np.log(ratio) / np.log(PHI)
        print(f"    lambda={val:8.4f} (mult {mult:3d})  ratio={ratio:.6f}  phi-exp n={n_phi:.4f}")

print("\n(c) Express eigenvalues in terms of phi:")
print("    Recall: phi^2 = phi + 1, so integer combos of {1, phi} span Z[phi]")
for val, mult in zip(nonzero_eigs, nonzero_mults):
    # Write val = a + b*phi and find best integer a, b
    # val = a + b*phi => b = (val - a)/phi
    # Try to decompose
    best_a, best_b = None, None
    best_err = 1e10
    for a in range(-100, 101):
        b = (val - a) / PHI
        if abs(b - round(b)) < best_err:
            best_err = abs(b - round(b))
            best_a = a
            best_b = round(b)
    expr = f"{best_a} + {best_b}*phi" if best_b >= 0 else f"{best_a} - {abs(best_b)}*phi"
    reconstructed = best_a + best_b * PHI
    err = abs(val - reconstructed)
    is_exact = "EXACT" if err < 0.01 else f"err={err:.4f}"
    print(f"    lambda={val:8.4f} (mult {mult:3d})  ~  {expr:20s}  [{is_exact}]")

# (d) Pairwise ratios
print("\n(d) Pairwise eigenvalue ratios that are near-integer powers of phi:")
phi_matches = []
for i, (v1, m1) in enumerate(zip(nonzero_eigs, nonzero_mults)):
    for j, (v2, m2) in enumerate(zip(nonzero_eigs, nonzero_mults)):
        if i >= j:
            continue
        ratio = v2 / v1
        if ratio > 1e-10:
            n = np.log(ratio) / np.log(PHI)
            n_round = round(n)
            if abs(n - n_round) < 0.05 and 1 <= n_round <= 40:
                phi_matches.append((v1, v2, m1, m2, n_round))
                print(f"    lambda={v1:.4f}/lambda={v2:.4f} = {ratio:.6f} ~ phi^{n_round} (err={abs(n - n_round):.4f})")

# Now build the comprehensive table
# For each Laplacian eigenvalue (with multiplicity), compute several phi-exponent candidates
print("\n\n--- COMPREHENSIVE EXPONENT TABLE ---")
print(f"{'Eig_idx':>7s} {'Eigenvalue':>11s} {'Mult':>5s} {'Coh_Weight':>11s} "
      f"{'n_ratio_max':>12s} {'n_ratio_min':>12s} {'In_GSM':>7s} {'In_Casimir':>11s} {'In_Coxeter':>11s}")
print("-" * 110)

table_rows = []
# Use unique eigenvalues
for idx, (val, mult) in enumerate(zip(unique_L, counts_L)):
    # Get coherent weight for modes at this eigenvalue
    mask = np.abs(np.round(eigenvalues_L, 4) - val) < 1e-4
    w = combined_weights[mask].sum()

    # phi-exponents
    if abs(val) > 1e-4 and abs(lambda_max) > 1e-4:
        n_max = -np.log(val / lambda_max) / np.log(PHI)
    else:
        n_max = float('nan')

    if abs(val) > 1e-4 and abs(lambda_min) > 1e-4:
        n_min = np.log(val / lambda_min) / np.log(PHI)
    else:
        n_min = float('nan')

    # Check nearest integer
    n_max_int = round(n_max) if not np.isnan(n_max) else None
    n_min_int = round(n_min) if not np.isnan(n_min) else None

    in_gsm_max = n_max_int in GSM_EXPONENTS if n_max_int is not None else False
    in_gsm_min = n_min_int in GSM_EXPONENTS if n_min_int is not None else False
    in_gsm = in_gsm_max or in_gsm_min

    in_casimir_max = n_max_int in E8_CASIMIR if n_max_int is not None else False
    in_casimir_min = n_min_int in E8_CASIMIR if n_min_int is not None else False
    in_casimir = in_casimir_max or in_casimir_min

    in_coxeter_max = n_max_int in E8_COXETER_EXP if n_max_int is not None else False
    in_coxeter_min = n_min_int in E8_COXETER_EXP if n_min_int is not None else False
    in_coxeter = in_coxeter_max or in_coxeter_min

    n_max_str = f"{n_max:.2f}" if not np.isnan(n_max) else "N/A"
    n_min_str = f"{n_min:.2f}" if not np.isnan(n_min) else "N/A"

    print(f"{idx:7d} {val:11.4f} {mult:5d} {w:11.6f} "
          f"{n_max_str:>12s} {n_min_str:>12s} "
          f"{'YES' if in_gsm else 'no':>7s} "
          f"{'YES' if in_casimir else 'no':>11s} "
          f"{'YES' if in_coxeter else 'no':>11s}")

    table_rows.append({
        'eig_idx': idx,
        'eigenvalue': val,
        'multiplicity': int(mult),
        'coherent_weight': w,
        'n_ratio_max': n_max,
        'n_ratio_min': n_min,
        'n_max_int': n_max_int,
        'n_min_int': n_min_int,
        'in_gsm': in_gsm,
        'in_casimir': in_casimir,
        'in_coxeter': in_coxeter
    })

# Alternative approach: use ADJACENCY eigenvalues (which are more natural for
# representation theory) and look for phi-structure
print("\n\n--- ADJACENCY EIGENVALUES AND PHI STRUCTURE ---")
unique_A_sorted = np.sort(np.unique(eig_A_rounded))[::-1]
print(f"{'Adj_Eigenvalue':>15s}  {'= a + b*phi':>20s}  {'a':>5s} {'b':>5s} {'n if phi^n':>10s}")
print("-" * 60)

adj_phi_exponents = []
for val in unique_A_sorted:
    # Decompose in Z[phi]
    best_a, best_b = 0, 0
    best_err = 1e10
    for a in range(-200, 201):
        b = (val - a) / PHI
        if abs(b - round(b)) < best_err:
            best_err = abs(b - round(b))
            best_a = a
            best_b = round(b)

    # Also check if it's a power of phi (up to sign/scaling)
    n_phi_str = ""
    if abs(val) > 0.01:
        n_test = np.log(abs(val)) / np.log(PHI)
        if abs(n_test - round(n_test)) < 0.1:
            n_phi_str = f"phi^{round(n_test)}"
            adj_phi_exponents.append(round(n_test))

    expr = f"{best_a} + {best_b}*phi"
    print(f"{val:15.6f}  {expr:>20s}  {best_a:5d} {best_b:5d} {n_phi_str:>10s}")

# Now try: differences between adjacent unique eigenvalues
print("\n--- EIGENVALUE SPACINGS AND PHI STRUCTURE ---")
unique_L_nonzero = unique_L[unique_L > 0.01]
spacings = np.diff(unique_L_nonzero)
print(f"{'Spacing':>10s}  {'= a + b*phi':>20s}  {'ratio to min spacing':>20s}")
for sp in spacings:
    best_a, best_b = 0, 0
    best_err = 1e10
    for a in range(-100, 101):
        b = (sp - a) / PHI
        if abs(b - round(b)) < best_err:
            best_err = abs(b - round(b))
            best_a = a
            best_b = round(b)
    expr = f"{best_a} + {best_b}*phi"
    ratio_str = f"{sp/spacings.min():.4f}" if spacings.min() > 0 else "N/A"
    print(f"{sp:10.4f}  {expr:>20s}  {ratio_str:>20s}")

# KEY ANALYSIS: Which integer exponents can be generated?
print("\n\n" + "=" * 80)
print("KEY ANALYSIS: Exponent Generation from E8 Spectral Data")
print("=" * 80)

# The E8 Casimir degrees generate exponents via sums
# Casimir: {2, 8, 12, 14, 18, 20, 24, 30}
# Coxeter: {1, 7, 11, 13, 17, 19, 23, 29}
# All sums and differences (mod small numbers) of Casimir degrees:

generated_from_casimir = set()
casimir_list = sorted(E8_CASIMIR)
for i, c1 in enumerate(casimir_list):
    generated_from_casimir.add(c1)
    for c2 in casimir_list[i:]:
        generated_from_casimir.add(c1 + c2)
        if c2 > c1:
            generated_from_casimir.add(c2 - c1)

# Also include half-sums (for Coxeter exponents)
coxeter_list = sorted(E8_COXETER_EXP)
generated_from_coxeter = set()
for c in coxeter_list:
    generated_from_coxeter.add(c)
for i, c1 in enumerate(coxeter_list):
    for c2 in coxeter_list[i:]:
        generated_from_coxeter.add(c1 + c2)
        if c2 > c1:
            generated_from_coxeter.add(c2 - c1)

# Also H4 Coxeter exponents and their combinations
h4_list = sorted(H4_COXETER_EXP)
generated_from_h4 = set()
for c in h4_list:
    generated_from_h4.add(c)
for i, c1 in enumerate(h4_list):
    for c2 in h4_list[i:]:
        generated_from_h4.add(c1 + c2)
        if c2 > c1:
            generated_from_h4.add(c2 - c1)

# Combined: E8 Casimir + Coxeter + H4
all_generated = generated_from_casimir | generated_from_coxeter | generated_from_h4

print(f"\nGSM exponents:                       {sorted(GSM_EXPONENTS)}")
print(f"Generated from E8 Casimir (+-):      {sorted(generated_from_casimir & GSM_EXPONENTS)}")
print(f"Generated from E8 Coxeter (+-):      {sorted(generated_from_coxeter & GSM_EXPONENTS)}")
print(f"Generated from H4 Coxeter (+-):      {sorted(generated_from_h4 & GSM_EXPONENTS)}")
print(f"Total coverage from algebra (+-):    {sorted(all_generated & GSM_EXPONENTS)}")
print(f"NOT covered:                          {sorted(GSM_EXPONENTS - all_generated)}")

# --- Extended generation: triple combinations ---
# The remaining exponents {3, 5, 9, 15, 27, 33} may come from triple sums/differences
# of Coxeter exponents, or from multiplicative (modular) structure.
all_sources = sorted(E8_CASIMIR | E8_COXETER_EXP | H4_COXETER_EXP)
generated_triple = set(all_generated)  # start with pairwise
for a in all_sources:
    for b in all_sources:
        for c in all_sources:
            for val in [a+b+c, a+b-c, a-b+c, a-b-c, abs(a+b-c), abs(a-b-c)]:
                if 1 <= val <= 40:
                    generated_triple.add(val)

# Also: Laplacian eigenvalue multiplicities: {1, 8, 35, 84, 112}
# These are dimensions of E8 irreps restricted to the root system
# The multiplicities themselves generate exponents
mults_set = {1, 8, 35, 84, 112}
generated_from_mults = set()
for m in mults_set:
    generated_from_mults.add(m)
    for m2 in mults_set:
        if abs(m - m2) >= 1:
            generated_from_mults.add(abs(m - m2))

# Multiplicative: Casimir degree divided by rank or Coxeter number
generated_from_ratios = set()
for c in E8_CASIMIR:
    for d in [2, 3, 4, 5, 6, 8, 10, 15, 30]:
        val = c * d
        if 1 <= val <= 40:
            generated_from_ratios.add(val)
        if c % d == 0:
            generated_from_ratios.add(c // d)

# Fibonacci indices: phi^n relates to Fibonacci via F_n*phi + F_{n-1}
# The Fibonacci numbers themselves may define allowed exponents
fib = [1, 1, 2, 3, 5, 8, 13, 21, 34]
generated_from_fib = set(fib) & set(range(1, 41))
for i, f1 in enumerate(fib):
    for f2 in fib[i:]:
        if 1 <= f1 + f2 <= 40:
            generated_from_fib.add(f1 + f2)
        if 1 <= abs(f1 - f2) <= 40:
            generated_from_fib.add(abs(f1 - f2))

# Lucas numbers: L_n = phi^n + (-phi)^{-n}  — directly related to phi structure
lucas = [2, 1, 3, 4, 7, 11, 18, 29]
generated_from_lucas = set(lucas) & set(range(1, 41))

all_generated_extended = generated_triple | generated_from_mults | generated_from_ratios | generated_from_fib | generated_from_lucas

remaining = GSM_EXPONENTS - all_generated
remaining_after_ext = GSM_EXPONENTS - all_generated_extended

print(f"\n--- Extended Generation (triple combos + multiplicities + Fibonacci + Lucas) ---")
print(f"Previously uncovered:                 {sorted(remaining)}")
print(f"Triple Coxeter/Casimir combos cover:  {sorted(generated_triple & remaining)}")
print(f"Multiplicity structure covers:        {sorted(generated_from_mults & remaining)}")
print(f"Casimir*integer ratios cover:         {sorted(generated_from_ratios & remaining)}")
print(f"Fibonacci sums cover:                 {sorted(generated_from_fib & remaining)}")
print(f"Lucas numbers cover:                  {sorted(generated_from_lucas & remaining)}")
print(f"Extended total coverage:              {sorted(all_generated_extended & GSM_EXPONENTS)}")
print(f"Still uncovered:                      {sorted(remaining_after_ext)}")

# Update the combined coverage
all_generated = all_generated_extended

# More refined: use the SPECTRAL eigenvalue indices
# The Laplacian eigenvalues form a specific set. The selection rule is:
# "n is allowed if it can be written as a Z-linear combination of the
# spectral indices where the mode has nonzero H4-projection weight"

# Map eigenvalues to their indices (0-based, by distinct eigenvalue)
spectral_indices = set()
for idx, row in enumerate(table_rows):
    if row['coherent_weight'] > threshold:
        spectral_indices.add(idx)

print(f"\nSpectral indices with nonzero H4-projection: {sorted(spectral_indices)}")

# Generate exponents from spectral data
# Use the eigenvalue RATIOS to define exponents
if len(nonzero_eigs) > 0:
    # Define a base eigenvalue (the smallest nonzero)
    base = nonzero_eigs[0]
    spectral_exponents = set()
    for val in nonzero_eigs:
        ratio = val / base
        n = np.log(ratio) / np.log(PHI)
        n_int = round(n)
        if abs(n - n_int) < 0.2:  # Allow 0.2 tolerance
            spectral_exponents.add(n_int)

    print(f"Spectral phi-exponents (from ratios): {sorted(spectral_exponents)}")
    print(f"Overlap with GSM:                     {sorted(spectral_exponents & GSM_EXPONENTS)}")

# ============================================================================
# COMPUTATION 4: Effective Coupling Constants
# ============================================================================
print("\n" + "=" * 80)
print("COMPUTATION 4: Effective Coupling Constants")
print("=" * 80)

# For modes surviving projection, compute g_k = weight_k / eigenvalue_k
print(f"\n{'Eigenvalue':>11s} {'Mult':>5s} {'Coh_Weight':>11s} {'Coupling g_k':>13s} {'g_k/g_max':>10s}")
print("-" * 60)

couplings = []
for idx, (val, mult) in enumerate(zip(unique_L, counts_L)):
    mask = np.abs(np.round(eigenvalues_L, 4) - val) < 1e-4
    w = combined_weights[mask].sum()

    if abs(val) > 1e-4 and w > threshold:
        g = w / val
        couplings.append((val, int(mult), w, g))

if couplings:
    g_max = max(c[3] for c in couplings)
    for val, mult, w, g in couplings:
        print(f"{val:11.4f} {mult:5d} {w:11.6f} {g:13.8f} {g/g_max:10.6f}")

    # Check ratios between couplings
    print("\n--- Coupling Ratios ---")
    print(f"{'g_i/g_j':>10s}  {'lambda_i':>10s}  {'lambda_j':>10s}  {'Near GSM ratio?':>20s}")
    print("-" * 55)

    gsm_ratios = {
        248/240: "248/240",
        7/30: "7/30",
        3.0: "3",
        1/3: "1/3",
        30/7: "30/7",
        240/248: "240/248",
        2.0: "2",
        0.5: "1/2",
        7.0: "7",
        1/7: "1/7",
        8.0: "8",
        1/8: "1/8",
        PHI: "phi",
        1/PHI: "1/phi",
        PHI**2: "phi^2",
        1/PHI**2: "1/phi^2",
    }

    for i, (v1, m1, w1, g1) in enumerate(couplings):
        for j, (v2, m2, w2, g2) in enumerate(couplings):
            if i >= j:
                continue
            ratio = g1 / g2
            # Check against known GSM ratios
            for target, name in gsm_ratios.items():
                if abs(ratio - target) / max(abs(target), 1e-10) < 0.05:
                    print(f"{ratio:10.6f}  {v1:10.4f}  {v2:10.4f}  ~ {name}")
                    break
            else:
                # Check if it's a power of phi
                if ratio > 1e-10:
                    n = np.log(ratio) / np.log(PHI)
                    if abs(n - round(n)) < 0.1 and abs(round(n)) <= 40:
                        print(f"{ratio:10.6f}  {v1:10.4f}  {v2:10.4f}  ~ phi^{round(n)}")

# Dimensionality analysis
print("\n\n--- Key Dimensional Numbers ---")
print(f"E8 dimension: 248")
print(f"E8 roots: 240")
print(f"E8 rank: 8")
print(f"E8 Coxeter number: 30")
print(f"H4 roots: 120 (600-cell vertices)")
print(f"H4 Coxeter number: 30 (same as E8!)")
print(f"Ratio 248/240 = {248/240:.10f}")
print(f"Ratio 240/120 = {240/120} (E8 roots / H4 roots)")
print(f"7/30 = {7/30:.10f}")
print(f"phi = {PHI:.10f}")

# ============================================================================
# SAVE RESULTS
# ============================================================================
print("\n" + "=" * 80)
print("SAVING RESULTS")
print("=" * 80)

# Save CSV
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, "e8_spectrum_analysis.csv")

with open(csv_path, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['eig_idx', 'eigenvalue', 'multiplicity', 'coherent_weight',
                      'n_ratio_max', 'n_ratio_min', 'n_max_int', 'n_min_int',
                      'in_gsm', 'in_casimir', 'in_coxeter'])
    for row in table_rows:
        writer.writerow([
            row['eig_idx'], f"{row['eigenvalue']:.6f}", row['multiplicity'],
            f"{row['coherent_weight']:.8f}",
            f"{row['n_ratio_max']:.4f}" if not np.isnan(row['n_ratio_max']) else 'N/A',
            f"{row['n_ratio_min']:.4f}" if not np.isnan(row['n_ratio_min']) else 'N/A',
            row['n_max_int'], row['n_min_int'],
            row['in_gsm'], row['in_casimir'], row['in_coxeter']
        ])

print(f"Saved: {csv_path}")

# --- Plot 1: Eigenvalue spectrum with projection weights ---
fig, axes = plt.subplots(2, 1, figsize=(14, 10))

# Histogram colored by projection weight
ax = axes[0]
for idx, (val, mult) in enumerate(zip(unique_L, counts_L)):
    mask = np.abs(np.round(eigenvalues_L, 4) - val) < 1e-4
    w = combined_weights[mask].mean()
    color = plt.cm.hot(w / max(combined_weights.max(), 1e-10))
    ax.bar(val, mult, width=0.8, color=color, edgecolor='black', linewidth=0.5)

ax.set_xlabel('Laplacian Eigenvalue', fontsize=12)
ax.set_ylabel('Multiplicity', fontsize=12)
ax.set_title('E8 Root System Graph Laplacian Spectrum\n(color = H4 projection weight: dark=low, bright=high)', fontsize=13)
ax.grid(True, alpha=0.3)

# Add colorbar
sm = plt.cm.ScalarMappable(cmap=plt.cm.hot, norm=plt.Normalize(0, combined_weights.max()))
sm.set_array([])
plt.colorbar(sm, ax=ax, label='Coherent Projection Weight')

# Also show adjacency spectrum
ax2 = axes[1]
unique_A_for_plot = np.unique(eig_A_rounded)
for val in unique_A_for_plot:
    mult = np.sum(np.abs(eig_A_rounded - val) < 1e-4)
    # Color by whether the corresponding Laplacian eigenvalue survives
    lap_val = 56 - val
    mask_l = np.abs(np.round(eigenvalues_L, 4) - round(lap_val, 4)) < 1e-3
    w = combined_weights[mask_l].mean() if mask_l.sum() > 0 else 0
    color = plt.cm.hot(w / max(combined_weights.max(), 1e-10))
    ax2.bar(val, mult, width=0.8, color=color, edgecolor='black', linewidth=0.5)

ax2.set_xlabel('Adjacency Eigenvalue', fontsize=12)
ax2.set_ylabel('Multiplicity', fontsize=12)
ax2.set_title('E8 Root System Adjacency Spectrum', fontsize=13)
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plot1_path = os.path.join(script_dir, "e8_eigenvalue_spectrum.png")
plt.savefig(plot1_path, dpi=150, bbox_inches='tight')
plt.close()
print(f"Saved: {plot1_path}")

# --- Plot 2: Eigenvalue vs projection weight scatter ---
fig, ax = plt.subplots(figsize=(12, 8))

for idx, (val, mult) in enumerate(zip(unique_L, counts_L)):
    mask = np.abs(np.round(eigenvalues_L, 4) - val) < 1e-4
    w = combined_weights[mask].sum()
    # Check if this eigenvalue's phi-exponent is in GSM
    in_gsm = table_rows[idx]['in_gsm'] if idx < len(table_rows) else False

    marker = 'o' if not in_gsm else '*'
    color = 'red' if in_gsm else 'steelblue'
    size = 50 + 5 * mult if not in_gsm else 200

    ax.scatter(val, w, s=size, c=color, marker=marker, edgecolors='black',
              linewidth=0.5, zorder=5 if in_gsm else 3)
    if in_gsm or w > 0.01:
        ax.annotate(f'm={mult}', (val, w), fontsize=7, ha='center', va='bottom')

ax.set_xlabel('Laplacian Eigenvalue', fontsize=12)
ax.set_ylabel('Coherent Projection Weight (H4 compatibility)', fontsize=12)
ax.set_title('E8 Modes: Eigenvalue vs H4-Projection Weight\n(red stars = phi-exponent matches GSM set)', fontsize=13)
ax.grid(True, alpha=0.3)

# Legend
from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], marker='*', color='w', markerfacecolor='red', markersize=15,
           label='GSM exponent match'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor='steelblue', markersize=10,
           label='Non-GSM eigenvalue'),
]
ax.legend(handles=legend_elements, fontsize=11)

plt.tight_layout()
plot2_path = os.path.join(script_dir, "e8_mode_projection.png")
plt.savefig(plot2_path, dpi=150, bbox_inches='tight')
plt.close()
print(f"Saved: {plot2_path}")

# ============================================================================
# FINAL VERDICT
# ============================================================================
print("\n" + "=" * 80)
print("FINAL ANALYSIS AND VERDICT")
print("=" * 80)

# Count how many GSM exponents are explained
gsm_covered_by_spectrum = set()
gsm_covered_by_casimir = set()
gsm_covered_by_coxeter = set()
gsm_covered_by_h4 = set()

for row in table_rows:
    if row['in_gsm']:
        for n in [row['n_max_int'], row['n_min_int']]:
            if n is not None and n in GSM_EXPONENTS:
                gsm_covered_by_spectrum.add(n)

gsm_covered_by_casimir = generated_from_casimir & GSM_EXPONENTS
gsm_covered_by_coxeter = generated_from_coxeter & GSM_EXPONENTS
gsm_covered_by_h4 = generated_from_h4 & GSM_EXPONENTS
total_covered = all_generated & GSM_EXPONENTS

n_total = len(GSM_EXPONENTS)
n_covered_spectrum = len(gsm_covered_by_spectrum)
n_covered_algebra = len(total_covered)

print(f"\nGSM exponents to explain:    {n_total} values: {sorted(GSM_EXPONENTS)}")
print(f"Covered by spectral ratios:  {n_covered_spectrum}/{n_total}: {sorted(gsm_covered_by_spectrum)}")
print(f"Covered by Casimir sums:     {len(gsm_covered_by_casimir)}/{n_total}: {sorted(gsm_covered_by_casimir)}")
print(f"Covered by Coxeter sums:     {len(gsm_covered_by_coxeter)}/{n_total}: {sorted(gsm_covered_by_coxeter)}")
print(f"Covered by H4 Coxeter sums:  {len(gsm_covered_by_h4)}/{n_total}: {sorted(gsm_covered_by_h4)}")
print(f"Total algebraic coverage:    {n_covered_algebra}/{n_total}: {sorted(total_covered)}")
print(f"Uncovered exponents:         {sorted(GSM_EXPONENTS - total_covered)}")

# Detailed source attribution
print("\n--- Exponent Source Attribution ---")
for n in sorted(GSM_EXPONENTS):
    sources = []
    if n in generated_from_casimir:
        sources.append("Casimir(+-)")
    if n in generated_from_coxeter:
        sources.append("E8-Coxeter(+-)")
    if n in generated_from_h4:
        sources.append("H4-Coxeter(+-)")
    if n in generated_triple:
        sources.append("Triple-combo")
    if n in generated_from_mults:
        sources.append("Multiplicity")
    if n in generated_from_fib:
        sources.append("Fibonacci")
    if n in generated_from_lucas:
        sources.append("Lucas")
    if n in gsm_covered_by_spectrum:
        sources.append("Spectral")
    source_str = ", ".join(sources) if sources else "UNEXPLAINED"
    print(f"  n={n:2d}:  {source_str}")

coverage_fraction = n_covered_algebra / n_total
if coverage_fraction >= 0.90:
    verdict = "DERIVED"
elif coverage_fraction >= 0.60:
    verdict = "PARTIALLY DERIVED"
else:
    verdict = "NOT DERIVED"

print(f"\n{'=' * 80}")
print(f"VERDICT: Selection rules {verdict} from E8 spectral theory")
print(f"  Coverage: {n_covered_algebra}/{n_total} = {100*coverage_fraction:.1f}% of GSM exponents")
print(f"  explained by E8 Casimir/Coxeter algebra + H4 projection")
print(f"{'=' * 80}")
