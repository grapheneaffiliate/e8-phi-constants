"""
Cosmological Constant Derivation from 600-Cell Casimir Energy
=============================================================

Claim: Omega_Lambda = 0.6889 from E8 geometry.

Current formula: phi^(-1) + phi^(-6) + phi^(-9) - phi^(-13) + phi^(-28) + eps*phi^(-7)

This script attempts to derive that value from the Casimir (vacuum) energy
of a scalar field on the 600-cell lattice.

Approach:
  1. Build the 600-cell graph (120 vertices, each with 12 neighbors)
  2. Compute the graph Laplacian eigenvalues
  3. Compute the zeta-regularized vacuum energy E_vac = (1/2) * sum sqrt(lambda_k)
  4. Normalize and check if the result relates to 0.6889

References:
  - 600-cell: regular 4-polytope with 120 vertices, 720 edges, 1200 triangular faces, 600 tetrahedral cells
  - Each vertex has exactly 12 nearest neighbors
  - Vertices can be constructed from quaternionic icosians
"""

import numpy as np
from itertools import product

# ==============================================================================
# Constants
# ==============================================================================
phi = (1 + np.sqrt(5)) / 2
eps = 28 / 248
OMEGA_LAMBDA_OBS = 0.6889  # Planck 2018 value

# Known GSM formula
omega_formula = (phi**(-1) + phi**(-6) + phi**(-9) - phi**(-13)
                 + phi**(-28) + eps * phi**(-7))
print(f"GSM formula value: {omega_formula:.6f}")
print(f"Observed value:    {OMEGA_LAMBDA_OBS:.6f}")
print(f"Formula error:     {abs(omega_formula - OMEGA_LAMBDA_OBS)/OMEGA_LAMBDA_OBS*100:.4f}%")
print()

# ==============================================================================
# Step 1: Build 600-cell vertices
# ==============================================================================
print("=" * 70)
print("STEP 1: Building 600-cell vertices")
print("=" * 70)

vertices = []

# Type 1: 8 vertices — permutations of (+-1, 0, 0, 0)
for i in range(4):
    for s in [1, -1]:
        v = [0, 0, 0, 0]
        v[i] = s
        vertices.append(v)

# Type 2: 16 vertices — (+-1/2, +-1/2, +-1/2, +-1/2)
for signs in product([0.5, -0.5], repeat=4):
    vertices.append(list(signs))

# Type 3: 96 vertices — even permutations of (0, +-1/2, +-phi/2, +-1/(2*phi))
# "Even permutations" of 4 elements: there are 12 even permutations
# The values at the non-zero positions have independent signs, but with
# the constraint that the number of minus signs is even.
base_vals = [0, 0.5, phi / 2, 1 / (2 * phi)]

# Generate all even permutations of (0, 1, 2, 3)
# Even permutations of {0,1,2,3}: 12 total
even_perms = []
from itertools import permutations

for p in permutations(range(4)):
    # Count inversions to determine parity
    inv = 0
    for i in range(4):
        for j in range(i + 1, 4):
            if p[i] > p[j]:
                inv += 1
    if inv % 2 == 0:
        even_perms.append(p)

for perm in even_perms:
    # The values are (0, +-1/2, +-phi/2, +-1/(2*phi))
    # Apply signs to the three nonzero positions
    # Constraint: even number of minus signs (from the 600-cell construction)
    for s1 in [1, -1]:
        for s2 in [1, -1]:
            for s3 in [1, -1]:
                if s1 * s2 * s3 > 0:  # even number of minus signs
                    vals = [0, s1 * 0.5, s2 * phi / 2, s3 / (2 * phi)]
                    v = [vals[perm[i]] for i in range(4)]
                    vertices.append(v)

vertices = np.array(vertices)

# Remove duplicates (some constructions may produce duplicates)
# Round to avoid floating point issues
rounded = np.round(vertices, decimals=10)
_, unique_idx = np.unique(rounded, axis=0, return_index=True)
vertices = vertices[sorted(unique_idx)]

n_verts = len(vertices)
print(f"Number of vertices: {n_verts}")
if n_verts != 120:
    print(f"WARNING: Expected 120 vertices, got {n_verts}")
    print("Attempting to fix...")
    # Try with odd number of minus signs too
    vertices_list = []
    # Type 1
    for i in range(4):
        for s in [1, -1]:
            v = [0.0, 0.0, 0.0, 0.0]
            v[i] = float(s)
            vertices_list.append(v)
    # Type 2
    for signs in product([0.5, -0.5], repeat=4):
        vertices_list.append(list(signs))
    # Type 3: ALL even permutations with ALL sign combinations
    for perm in even_perms:
        for s1 in [1, -1]:
            for s2 in [1, -1]:
                for s3 in [1, -1]:
                    vals = [0.0, s1 * 0.5, s2 * phi / 2, s3 / (2 * phi)]
                    v = [vals[perm[i]] for i in range(4)]
                    vertices_list.append(v)

    vertices = np.array(vertices_list)
    rounded = np.round(vertices, decimals=10)
    _, unique_idx = np.unique(rounded, axis=0, return_index=True)
    vertices = vertices[sorted(unique_idx)]
    n_verts = len(vertices)
    print(f"After fix: {n_verts} vertices")

# Verify: all vertices should have the same norm
norms = np.linalg.norm(vertices, axis=1)
print(f"Vertex norms: min={norms.min():.6f}, max={norms.max():.6f}")

# Normalize all vertices to unit sphere
vertices = vertices / norms[:, np.newaxis]

# ==============================================================================
# Step 2: Build adjacency matrix
# ==============================================================================
print()
print("=" * 70)
print("STEP 2: Building adjacency matrix")
print("=" * 70)

# Compute all pairwise inner products
inner_products = vertices @ vertices.T

# In the unit 600-cell, two vertices are neighbors if their inner product
# equals phi/2 = cos(pi/5). Due to floating point, use a tolerance.
target_ip = phi / 2
# Actually, for the 600-cell with unit-norm vertices, the nearest-neighbor
# inner product is cos(pi/5) = phi/2 ≈ 0.80902

# Find the distinct inner product values to identify the neighbor threshold
ip_flat = inner_products[np.triu_indices(n_verts, k=1)]
ip_rounded = np.round(ip_flat, decimals=6)
unique_ips = np.sort(np.unique(ip_rounded))[::-1]
print(f"Distinct inner products (top 10): {unique_ips[:10]}")

# The largest inner product < 1 should be the nearest neighbor distance
nn_ip = unique_ips[0]
print(f"Nearest-neighbor inner product: {nn_ip:.6f}")
print(f"phi/2 = {phi/2:.6f}")

# Build adjacency: connect if inner product is close to nn_ip
tol = 1e-4
adjacency = (np.abs(inner_products - nn_ip) < tol).astype(float)
np.fill_diagonal(adjacency, 0)

# Check degree (should be 12 for 600-cell)
degrees = adjacency.sum(axis=1)
print(f"Vertex degrees: min={degrees.min():.0f}, max={degrees.max():.0f}")
print(f"Total edges: {adjacency.sum() / 2:.0f}")

if degrees.min() != 12 or degrees.max() != 12:
    print("WARNING: Expected degree 12 (600-cell). Trying different threshold...")
    # Try using the actual nearest-neighbor distance
    for test_ip in unique_ips[:5]:
        adj_test = (np.abs(inner_products - test_ip) < tol).astype(float)
        np.fill_diagonal(adj_test, 0)
        deg_test = adj_test.sum(axis=1)
        print(f"  IP={test_ip:.6f}: degrees min={deg_test.min():.0f} max={deg_test.max():.0f}")
        if deg_test.min() == 12 and deg_test.max() == 12:
            adjacency = adj_test
            degrees = deg_test
            nn_ip = test_ip
            print(f"  -> Using this threshold")
            break

# ==============================================================================
# Step 3: Graph Laplacian eigenvalues
# ==============================================================================
print()
print("=" * 70)
print("STEP 3: Computing Laplacian eigenvalues")
print("=" * 70)

D = np.diag(degrees)
L = D - adjacency  # Unnormalized Laplacian

eigenvalues = np.linalg.eigvalsh(L)
eigenvalues = np.sort(eigenvalues)

print(f"Number of eigenvalues: {len(eigenvalues)}")
print(f"Smallest eigenvalue: {eigenvalues[0]:.6e} (should be ~0)")
print(f"Largest eigenvalue:  {eigenvalues[-1]:.6f}")
print(f"Second smallest:     {eigenvalues[1]:.6f}")

# Count distinct eigenvalues (the 600-cell has high symmetry -> many degeneracies)
unique_evals = np.unique(np.round(eigenvalues, decimals=6))
print(f"Number of distinct eigenvalues: {len(unique_evals)}")
print(f"Distinct eigenvalues: {unique_evals}")

# ==============================================================================
# Step 4: Casimir (vacuum) energy — multiple regularization schemes
# ==============================================================================
print()
print("=" * 70)
print("STEP 4: Vacuum energy computation")
print("=" * 70)

# Nonzero eigenvalues only
nonzero_evals = eigenvalues[eigenvalues > 1e-10]
print(f"Nonzero eigenvalues: {len(nonzero_evals)}")

# --- Method 1: Raw sum of sqrt(eigenvalues) ---
E_raw = 0.5 * np.sum(np.sqrt(nonzero_evals))
print(f"\nMethod 1: Raw Casimir energy")
print(f"  E_raw = (1/2) * sum sqrt(lambda) = {E_raw:.6f}")
print(f"  E_raw / 120 (per vertex) = {E_raw / 120:.6f}")
print(f"  E_raw / 720 (per edge) = {E_raw / 720:.6f}")

# --- Method 2: Zeta-function regularization ---
# Spectral zeta: zeta_L(s) = sum lambda_k^(-s)
# Vacuum energy = -(1/2) * zeta_L'(0) or evaluated at s = -1/2

# E_zeta(s) = (1/2) * sum lambda_k^(1/2 - s) evaluated at s -> 0 with subtraction
# For finite lattice, the sum is already finite, so "regularization" just means
# the raw sum above. But we can also compute the spectral zeta function.

def spectral_zeta(evals, s):
    """Compute sum_k lambda_k^(-s) for nonzero eigenvalues."""
    return np.sum(evals**(-s))

# Zeta at s = -1/2 gives sum lambda^(1/2) = 2 * E_raw
zeta_neg_half = spectral_zeta(nonzero_evals, -0.5)
print(f"\nMethod 2: Spectral zeta function")
print(f"  zeta_L(-1/2) = {zeta_neg_half:.6f}")
print(f"  (1/2) * zeta_L(-1/2) = {zeta_neg_half/2:.6f} (should equal E_raw)")

# --- Method 3: Heat kernel regularization ---
# E(t) = (1/2) * sum sqrt(lambda_k) * exp(-t * lambda_k)
# Take t -> 0 limit (but for finite lattice, t=0 is fine)
for t in [0.001, 0.01, 0.1]:
    E_heat = 0.5 * np.sum(np.sqrt(nonzero_evals) * np.exp(-t * nonzero_evals))
    print(f"  Heat kernel E(t={t}) = {E_heat:.6f}")

# ==============================================================================
# Step 5: Relate to Omega_Lambda
# ==============================================================================
print()
print("=" * 70)
print("STEP 5: Relating to Omega_Lambda")
print("=" * 70)

# The key question: can we normalize E_raw to get 0.6889?
# Try various normalizations involving E8 constants

normalizations = {
    "E / n_vertices": E_raw / n_verts,
    "E / n_edges": E_raw / 720,
    "E / dim(E8)": E_raw / 248,
    "E / |roots(E8)|": E_raw / 240,
    "E / (n_verts * degree)": E_raw / (n_verts * 12),
    "E / (n_verts * phi)": E_raw / (n_verts * phi),
    "E / (n_edges * phi)": E_raw / (720 * phi),
    "E * phi / dim(E8)": E_raw * phi / 248,
    "E * phi^2 / |roots|": E_raw * phi**2 / 240,
    "E / (600 cells)": E_raw / 600,
    "E / 1200 (faces)": E_raw / 1200,
}

print(f"\nTarget: Omega_Lambda = {OMEGA_LAMBDA_OBS:.6f}")
print(f"\nE_raw = {E_raw:.6f}")
print()

best_match = None
best_err = 1e10

for name, val in normalizations.items():
    err = abs(val - OMEGA_LAMBDA_OBS) / OMEGA_LAMBDA_OBS * 100
    marker = " <---" if err < 5 else ""
    print(f"  {name:40s} = {val:.6f}  (err: {err:.2f}%){marker}")
    if err < best_err:
        best_err = err
        best_match = (name, val)

# Also try: what normalization factor N would give Omega_Lambda?
N_needed = E_raw / OMEGA_LAMBDA_OBS
print(f"\n  Normalization needed: E_raw / {N_needed:.4f} = Omega_Lambda")
print(f"  Is {N_needed:.4f} an E8 invariant?")
print(f"    {N_needed:.4f} / 120 = {N_needed/120:.4f}")
print(f"    {N_needed:.4f} / 240 = {N_needed/240:.4f}")
print(f"    {N_needed:.4f} / 248 = {N_needed/248:.4f}")
print(f"    {N_needed:.4f} / phi = {N_needed/phi:.4f}")
print(f"    {N_needed:.4f} / phi^2 = {N_needed/phi**2:.4f}")

# ==============================================================================
# Step 6: Check phi-power structure in eigenvalues
# ==============================================================================
print()
print("=" * 70)
print("STEP 6: Checking phi-power structure in eigenvalues")
print("=" * 70)

print("\nDistinct eigenvalues and their relation to phi:")
for ev in unique_evals:
    if ev > 1e-10:
        log_phi = np.log(ev) / np.log(phi)
        print(f"  lambda = {ev:10.6f},  log_phi(lambda) = {log_phi:8.4f}")

# ==============================================================================
# Step 7: Alternative — direct phi-expansion of vacuum energy
# ==============================================================================
print()
print("=" * 70)
print("STEP 7: Checking if E_raw has a phi-power expansion matching the formula")
print("=" * 70)

# The GSM formula is: phi^(-1) + phi^(-6) + phi^(-9) - phi^(-13) + phi^(-28) + eps*phi^(-7)
# Let's see what the per-vertex energy looks like in phi powers
E_per_vertex = E_raw / n_verts
E_per_edge = E_raw / 720

for label, val in [("E_per_vertex", E_per_vertex), ("E_per_edge", E_per_edge),
                    ("E_raw", E_raw), ("E_raw/248", E_raw/248)]:
    log_phi_val = np.log(val) / np.log(phi)
    print(f"  {label:20s} = {val:.6f}, log_phi = {log_phi_val:.4f}")

# ==============================================================================
# Summary
# ==============================================================================
print()
print("=" * 70)
print("SUMMARY")
print("=" * 70)
print(f"""
600-cell Casimir energy computation:
  Vertices:   {n_verts}
  Edges:      {int(adjacency.sum() / 2)}
  Degree:     {int(degrees[0])}

  Raw vacuum energy:  E = {E_raw:.6f}
  Best normalization: {best_match[0]} = {best_match[1]:.6f} (err: {best_err:.2f}%)

  Target (Omega_Lambda): {OMEGA_LAMBDA_OBS:.6f}
  GSM formula value:     {omega_formula:.6f}
""")

if best_err < 1:
    print("RESULT: The Casimir energy on the 600-cell, with the normalization")
    print(f"  '{best_match[0]}',")
    print(f"  matches Omega_Lambda to {best_err:.2f}%.")
    print("  This provides a geometric derivation of the cosmological constant.")
elif best_err < 10:
    print("RESULT: The Casimir energy on the 600-cell is APPROXIMATELY related")
    print(f"  to Omega_Lambda via '{best_match[0]}' (error: {best_err:.2f}%).")
    print("  This is suggestive but not a clean derivation.")
else:
    print("RESULT: No simple normalization of the 600-cell Casimir energy")
    print(f"  reproduces Omega_Lambda = {OMEGA_LAMBDA_OBS}.")
    print(f"  The raw energy E = {E_raw:.4f} requires dividing by {N_needed:.4f}")
    print("  to match, which is not an obvious E8 structural constant.")
    print()
    print("  HONEST ASSESSMENT: The phi-power formula for Omega_Lambda may not")
    print("  emerge directly from the 600-cell Casimir energy. The formula")
    print("  phi^(-1) + phi^(-6) + phi^(-9) - phi^(-13) + phi^(-28) + eps*phi^(-7)")
    print("  may require a different derivation pathway, or the connection to")
    print("  the 600-cell vacuum energy may involve additional structure (e.g.,")
    print("  spinor fields, gauge fields, or a different regularization scheme).")
