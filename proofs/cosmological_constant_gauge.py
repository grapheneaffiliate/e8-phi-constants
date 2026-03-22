"""
Cosmological Constant from E8/H4 Lattice — Three Independent Approaches
========================================================================

The scalar field Casimir energy on the 600-cell gave E=204.29, which doesn't
match Omega_Lambda=0.6889. Here we try three fundamentally different approaches:

  Approach 1: Gauge Field Casimir Energy (1-form Laplacian on 600-cell)
  Approach 2: Regge Calculus / Deficit Angles (phi-deformed 600-cell)
  Approach 3: Spectral Action Principle (Connes-style noncommutative geometry)

Completely honest: we report what matches and what doesn't.
"""

import numpy as np
from itertools import product, permutations, combinations
from scipy import sparse
from scipy.sparse.linalg import eigsh

phi = (1 + np.sqrt(5)) / 2
eps = 28 / 248
OMEGA_LAMBDA_OBS = 0.6889

omega_formula = (phi**(-1) + phi**(-6) + phi**(-9) - phi**(-13)
                 + phi**(-28) + eps * phi**(-7))

print("=" * 78)
print("COSMOLOGICAL CONSTANT FROM E8/H4 — THREE APPROACHES")
print("=" * 78)
print(f"Target: Omega_Lambda = {OMEGA_LAMBDA_OBS}")
print(f"GSM formula value:     {omega_formula:.6f}")
print()

# ======================================================================
# BUILD THE 600-CELL
# ======================================================================
print("BUILDING 600-CELL...")
print("-" * 78)

vertices = []

# Type 1: 8 vertices — permutations of (+-1, 0, 0, 0)
for i in range(4):
    for s in [1, -1]:
        v = [0.0, 0.0, 0.0, 0.0]
        v[i] = float(s)
        vertices.append(v)

# Type 2: 16 vertices — (+-1/2, +-1/2, +-1/2, +-1/2)
for signs in product([0.5, -0.5], repeat=4):
    vertices.append(list(signs))

# Type 3: 96 vertices — even permutations of (0, +-1/2, +-phi/2, +-1/(2*phi))
even_perms = []
for p in permutations(range(4)):
    inv = sum(1 for i in range(4) for j in range(i + 1, 4) if p[i] > p[j])
    if inv % 2 == 0:
        even_perms.append(p)

for perm in even_perms:
    for s1 in [1, -1]:
        for s2 in [1, -1]:
            for s3 in [1, -1]:
                vals = [0.0, s1 * 0.5, s2 * phi / 2, s3 / (2 * phi)]
                v = [vals[perm[i]] for i in range(4)]
                vertices.append(v)

vertices = np.array(vertices)
rounded = np.round(vertices, decimals=10)
_, unique_idx = np.unique(rounded, axis=0, return_index=True)
vertices = vertices[sorted(unique_idx)]
n_verts = len(vertices)

if n_verts != 120:
    # Try with all sign combinations (not just even)
    vertices_list = []
    for i in range(4):
        for s in [1, -1]:
            v = [0.0, 0.0, 0.0, 0.0]
            v[i] = float(s)
            vertices_list.append(v)
    for signs in product([0.5, -0.5], repeat=4):
        vertices_list.append(list(signs))
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

# Normalize to unit sphere
norms = np.linalg.norm(vertices, axis=1)
vertices = vertices / norms[:, np.newaxis]

print(f"Vertices: {n_verts}")

# Build adjacency
inner_products = vertices @ vertices.T
ip_flat = inner_products[np.triu_indices(n_verts, k=1)]
ip_rounded = np.round(ip_flat, decimals=6)
unique_ips = np.sort(np.unique(ip_rounded))[::-1]

# Find nearest-neighbor inner product
nn_ip = unique_ips[0]
tol = 1e-4
adjacency = (np.abs(inner_products - nn_ip) < tol).astype(float)
np.fill_diagonal(adjacency, 0)
degrees = adjacency.sum(axis=1)

if degrees.min() != 12 or degrees.max() != 12:
    for test_ip in unique_ips[:5]:
        adj_test = (np.abs(inner_products - test_ip) < tol).astype(float)
        np.fill_diagonal(adj_test, 0)
        deg_test = adj_test.sum(axis=1)
        if deg_test.min() == 12 and deg_test.max() == 12:
            adjacency = adj_test
            degrees = deg_test
            nn_ip = test_ip
            break

n_edges_total = int(adjacency.sum() / 2)
print(f"Edges: {n_edges_total}")
print(f"Degree: {int(degrees[0])}")
print(f"Nearest-neighbor inner product: {nn_ip:.6f}")

# Build edge list
edge_list = []
for i in range(n_verts):
    for j in range(i + 1, n_verts):
        if adjacency[i, j] > 0.5:
            edge_list.append((i, j))
edge_list = np.array(edge_list)
n_edges = len(edge_list)
print(f"Edge list size: {n_edges}")

# Build face list (triangles)
# A triangle exists when three vertices are mutually adjacent
print("Finding triangular faces...")
adj_set = set()
for i, j in edge_list:
    adj_set.add((i, j))
    adj_set.add((j, i))

neighbor_sets = [set() for _ in range(n_verts)]
for i, j in edge_list:
    neighbor_sets[i].add(j)
    neighbor_sets[j].add(i)

face_list = []
for i, j in edge_list:
    common = neighbor_sets[i] & neighbor_sets[j]
    for k in common:
        if k > j:  # Avoid duplicates: require i < j < k
            face_list.append((i, j, k))

face_list = np.array(face_list)
n_faces = len(face_list)
print(f"Triangular faces: {n_faces}")

# ======================================================================
# Scalar Laplacian eigenvalues (for reference)
# ======================================================================
D_mat = np.diag(degrees)
L0 = D_mat - adjacency
evals_L0 = np.linalg.eigvalsh(L0)
evals_L0 = np.sort(evals_L0)
E_scalar = 0.5 * np.sum(np.sqrt(evals_L0[evals_L0 > 1e-10]))
print(f"\nScalar Casimir energy (reference): E_scalar = {E_scalar:.4f}")

# ######################################################################
# APPROACH 1: GAUGE FIELD CASIMIR ENERGY (1-FORM LAPLACIAN)
# ######################################################################
print()
print("=" * 78)
print("APPROACH 1: GAUGE FIELD CASIMIR ENERGY (1-form Laplacian)")
print("=" * 78)

# Build boundary operator d_0: maps vertices to edges
# d_0 is n_edges x n_verts
# For edge (i,j) with i<j: d_0[e, i] = -1, d_0[e, j] = +1
print("\nBuilding boundary operator d_0 (vertices -> edges)...")
d0 = np.zeros((n_edges, n_verts))
for e_idx, (i, j) in enumerate(edge_list):
    d0[e_idx, i] = -1.0
    d0[e_idx, j] = 1.0

print(f"d_0 shape: {d0.shape}")

# Build boundary operator d_1: maps edges to faces
# d_1 is n_faces x n_edges
# For face (i,j,k) with i<j<k, the boundary edges are (i,j), (i,k), (j,k)
# with signs from orientation: +e_{ij} - e_{ik} + e_{jk}
print("Building boundary operator d_1 (edges -> faces)...")
# Create edge lookup
edge_to_idx = {}
for e_idx, (i, j) in enumerate(edge_list):
    edge_to_idx[(i, j)] = e_idx

d1 = np.zeros((n_faces, n_edges))
for f_idx, (i, j, k) in enumerate(face_list):
    # Face boundary: edge(i,j) - edge(i,k) + edge(j,k)
    # With orientation convention for simplex boundary
    e_ij = edge_to_idx.get((i, j))
    e_ik = edge_to_idx.get((i, k))
    e_jk = edge_to_idx.get((j, k))
    if e_ij is not None:
        d1[f_idx, e_ij] = 1.0
    if e_ik is not None:
        d1[f_idx, e_ik] = -1.0
    if e_jk is not None:
        d1[f_idx, e_jk] = 1.0

print(f"d_1 shape: {d1.shape}")

# Hodge Laplacian on 1-forms: L_1 = d_0^T d_0 + d_1^T d_1
# Note: L_1 = (d_0^T)(d_0) + (d_1^T)(d_1)
# d_0^T d_0 is n_edges x n_edges (the "coboundary" part)
# d_1^T d_1 is n_edges x n_edges (the "boundary" part)
print("\nComputing Hodge Laplacian L_1 = d_0^T d_0 + d_1^T d_1 ...")
L1_down = d0.T @ d0  # This is actually a vertex Laplacian
# Wait: the Hodge Laplacian on 1-forms is L_1 = d_0 d_0^T + d_1^T d_1
# d_0 d_0^T acts on edges (n_edges x n_edges): "down" Laplacian
# d_1^T d_1 acts on edges (n_edges x n_edges): "up" Laplacian

L1_down_part = d0 @ d0.T  # n_edges x n_edges
L1_up_part = d1.T @ d1    # n_edges x n_edges
L1 = L1_down_part + L1_up_part

print(f"L_1 shape: {L1.shape}")
print(f"L_1 symmetry check: {np.allclose(L1, L1.T)}")

# Compute eigenvalues
print("Computing eigenvalues of L_1...")
evals_L1 = np.linalg.eigvalsh(L1)
evals_L1 = np.sort(evals_L1)

n_zero_L1 = np.sum(np.abs(evals_L1) < 1e-8)
print(f"Total eigenvalues: {len(evals_L1)}")
print(f"Zero eigenvalues (Betti number b_1): {n_zero_L1}")
print(f"  (S^3 has b_1 = 0, so expect 0 zero eigenvalues)")
print(f"Smallest eigenvalue: {evals_L1[0]:.6e}")
print(f"Largest eigenvalue:  {evals_L1[-1]:.6f}")

# Distinct eigenvalues
unique_evals_L1 = np.unique(np.round(evals_L1, decimals=4))
print(f"Distinct eigenvalues: {len(unique_evals_L1)}")
if len(unique_evals_L1) <= 30:
    print(f"Values: {unique_evals_L1}")

# Gauge Casimir energy
nonzero_L1 = evals_L1[evals_L1 > 1e-8]
E_gauge_raw = 0.5 * np.sum(np.sqrt(nonzero_L1))
print(f"\nRaw 1-form Casimir energy: E_1 = {E_gauge_raw:.6f}")

# With E8 gauge DOF: multiply by dim(adjoint) = 248
dim_E8 = 248
n_roots_E8 = 240
E_gauge_E8 = dim_E8 * E_gauge_raw
print(f"E8 gauge Casimir: E_gauge = dim(E8) * E_1 = {E_gauge_E8:.4f}")

# Try normalizations
print(f"\n--- Gauge field normalizations (target = {OMEGA_LAMBDA_OBS}) ---")
gauge_norms = {
    "E_1 / edges":                    E_gauge_raw / n_edges,
    "E_1 / verts":                    E_gauge_raw / n_verts,
    "E_1 / faces":                    E_gauge_raw / n_faces,
    "E_1 / (edges * phi)":            E_gauge_raw / (n_edges * phi),
    "E_1 / dim(E8)":                  E_gauge_raw / dim_E8,
    "E_1 / roots(E8)":                E_gauge_raw / n_roots_E8,
    "E_1 / (verts * dim(E8))":        E_gauge_raw / (n_verts * dim_E8),
    "E_1 / (edges * dim(E8))":        E_gauge_raw / (n_edges * dim_E8),
    "E_1 * phi / edges":              E_gauge_raw * phi / n_edges,
    "E_1 * phi / dim(E8)":            E_gauge_raw * phi / dim_E8,
    "E_1 / (verts * roots)":          E_gauge_raw / (n_verts * n_roots_E8),
    "E_1 / (cells * phi)":            E_gauge_raw / (600 * phi),
    "dim(E8)*E_1 / edges^2":          dim_E8 * E_gauge_raw / n_edges**2,
    "dim(E8)*E_1 / (verts*edges)":    dim_E8 * E_gauge_raw / (n_verts * n_edges),
    "E_1 / (edges*phi^2)":            E_gauge_raw / (n_edges * phi**2),
    "E_1 * phi^(-2)":                 E_gauge_raw * phi**(-2),
    "E_1 * phi^(-3)":                 E_gauge_raw * phi**(-3),
    "E_1 * phi^(-4)":                 E_gauge_raw * phi**(-4),
    "E_1 / (edges*12)":               E_gauge_raw / (n_edges * 12),
    "E_1 / (verts*12)":               E_gauge_raw / (n_verts * 12),
    "E_1 / (verts*phi^2)":            E_gauge_raw / (n_verts * phi**2),
    "E_1 / (8*pi^2*verts)":           E_gauge_raw / (8 * np.pi**2 * n_verts),
}

# Also search: E8 * E_1 with various divisors
gauge_norms["E8*E_1 / (edges*verts)"] = dim_E8 * E_gauge_raw / (n_edges * n_verts)
gauge_norms["E8*E_1 / (edges*faces)"] = dim_E8 * E_gauge_raw / (n_edges * n_faces)
gauge_norms["E8*E_1 / edges^2"] = dim_E8 * E_gauge_raw / n_edges**2
gauge_norms["E8*E_1 / (verts^2)"] = dim_E8 * E_gauge_raw / n_verts**2
gauge_norms["E8*E_1 / (faces*phi)"] = dim_E8 * E_gauge_raw / (n_faces * phi)
gauge_norms["roots*E_1 / edges^2"] = n_roots_E8 * E_gauge_raw / n_edges**2

best_gauge = None
best_gauge_err = 1e10
for name, val in sorted(gauge_norms.items(), key=lambda x: abs(x[1] - OMEGA_LAMBDA_OBS)):
    err = abs(val - OMEGA_LAMBDA_OBS) / OMEGA_LAMBDA_OBS * 100
    marker = " *** MATCH ***" if err < 1 else (" <-- close" if err < 5 else "")
    print(f"  {name:45s} = {val:12.6f}  ({err:7.2f}%){marker}")
    if err < best_gauge_err:
        best_gauge_err = err
        best_gauge = (name, val, err)

N_needed_gauge = E_gauge_raw / OMEGA_LAMBDA_OBS
print(f"\n  To get 0.6889 from E_1, need to divide by: {N_needed_gauge:.6f}")
print(f"    / 120 = {N_needed_gauge/120:.4f}")
print(f"    / 240 = {N_needed_gauge/240:.4f}")
print(f"    / 248 = {N_needed_gauge/248:.4f}")
print(f"    / 720 = {N_needed_gauge/720:.4f}")
print(f"    / phi = {N_needed_gauge/phi:.4f}")
print(f"    / phi^2 = {N_needed_gauge/phi**2:.4f}")

# Decompose spectrum
print("\n--- L_1 spectrum decomposition ---")
print(f"  Down Laplacian (d0 d0^T) eigenvalues:")
evals_down = np.linalg.eigvalsh(L1_down_part)
evals_down = np.sort(evals_down)
unique_down = np.unique(np.round(evals_down, 4))
print(f"    Distinct: {len(unique_down)}")
if len(unique_down) <= 20:
    print(f"    Values: {unique_down}")
E_down = 0.5 * np.sum(np.sqrt(evals_down[evals_down > 1e-8]))
print(f"    Casimir from down part: {E_down:.6f}")

print(f"  Up Laplacian (d1^T d1) eigenvalues:")
evals_up = np.linalg.eigvalsh(L1_up_part)
evals_up = np.sort(evals_up)
unique_up = np.unique(np.round(evals_up, 4))
print(f"    Distinct: {len(unique_up)}")
if len(unique_up) <= 20:
    print(f"    Values: {unique_up}")
E_up = 0.5 * np.sum(np.sqrt(evals_up[evals_up > 1e-8]))
print(f"    Casimir from up part: {E_up:.6f}")


# ######################################################################
# APPROACH 2: REGGE CALCULUS / DEFICIT ANGLES
# ######################################################################
print()
print("=" * 78)
print("APPROACH 2: REGGE CALCULUS — DEFICIT ANGLES ON 600-CELL")
print("=" * 78)

# The 600-cell has 600 regular tetrahedral cells
# For a regular 600-cell inscribed in a unit 3-sphere:

# Step 1: Compute edge length
# Nearest-neighbor distance on unit sphere
nn_dist = np.sqrt(2 - 2 * nn_ip)
print(f"\nEdge length (on unit S^3): {nn_dist:.6f}")
print(f"1/phi = {1/phi:.6f}")
print(f"Edge length ~= 1/phi: {np.isclose(nn_dist, 1/phi, atol=1e-4)}")

# Step 2: Dihedral angle of the 600-cell
# The dihedral angle of the 600-cell is arccos(-phi/sqrt(5))
# or equivalently pi - arctan(2)
# Actually, for a regular 600-cell, the dihedral angle along each edge is
# the angle between two tetrahedra sharing that edge.

# Number of tetrahedra meeting at each edge in the 600-cell: 5
# (The edge figure of the 600-cell is a pentagon)
tets_per_edge = 5

# Dihedral angle of a regular tetrahedron (in flat space)
dihedral_tet_flat = np.arccos(1/3)  # ~70.53 degrees
print(f"\nDihedral angle of flat tetrahedron: {np.degrees(dihedral_tet_flat):.4f} deg")
print(f"Tetrahedra per edge (edge figure = pentagon): {tets_per_edge}")
print(f"Sum of dihedral angles at each edge: {tets_per_edge} * {np.degrees(dihedral_tet_flat):.4f} = {np.degrees(tets_per_edge * dihedral_tet_flat):.4f} deg")

# In Regge calculus on a 3-manifold triangulated by tetrahedra:
# The deficit angle at each edge is:
# delta_e = 2*pi - sum of dihedral angles of tets sharing that edge
# For the 600-cell, the dihedral angle is NOT the flat tet angle;
# it's the angle between adjacent cells in the curved polytope.

# The 600-cell dihedral angle (between adjacent cells along shared face):
# This is the supplement: dihedral_600cell
# For 600-cell: dihedral angle = arccos(-1/(3*phi - 1)) ...
# Actually let's compute it directly from vertex data.

# Pick an edge and find the 5 tetrahedra around it
print("\nComputing dihedral angles from vertex data...")

# First, find all tetrahedra (cells)
# A tetrahedron exists when 4 vertices are mutually adjacent
# Faster: for each face (i,j,k), find vertices adjacent to all three
print("Finding tetrahedral cells...")
cells = []
face_set = set()
for f_idx, (i, j, k) in enumerate(face_list):
    face_set.add((i, j, k))

for f_idx, (i, j, k) in enumerate(face_list):
    # Find vertices adjacent to i, j, and k
    common = neighbor_sets[i] & neighbor_sets[j] & neighbor_sets[k]
    for l in common:
        if l > k:  # Avoid duplicates: i < j < k < l
            cell = tuple(sorted([i, j, k, l]))
            cells.append(cell)

# Remove duplicates
cells = list(set(cells))
n_cells = len(cells)
print(f"Tetrahedral cells: {n_cells}")

if n_cells != 600:
    print(f"WARNING: Expected 600 cells, got {n_cells}")
    # Try finding cells differently: for each vertex triple that forms
    # a face, also check common neighbors below k
    cells2 = set()
    for f_idx, (i, j, k) in enumerate(face_list):
        common = neighbor_sets[i] & neighbor_sets[j] & neighbor_sets[k]
        for l in common:
            cell = tuple(sorted([i, j, k, l]))
            cells2.add(cell)
    cells = list(cells2)
    n_cells = len(cells)
    print(f"After dedup: {n_cells} cells")

# Compute dihedral angle: for an edge (a,b), find the cells containing it,
# then compute the angle between opposite edges in those cells
# Actually: the dihedral angle at edge (a,b) in a cell is the angle between
# the two face normals (or equivalently between the face planes)

def compute_dihedral_at_edge(v0, v1, v2, v3, edge_verts):
    """Compute dihedral angle at given edge in tetrahedron (v0,v1,v2,v3).
    edge_verts = (a,b) indices into [v0,v1,v2,v3].
    """
    # The four vertices
    verts_tet = np.array([v0, v1, v2, v3])
    a, b = edge_verts
    # The two faces sharing this edge each have one other vertex
    others = [i for i in range(4) if i != a and i != b]
    c, d = others

    # Edge vector
    edge_vec = verts_tet[b] - verts_tet[a]
    # Vectors from a to the two opposite vertices
    vc = verts_tet[c] - verts_tet[a]
    vd = verts_tet[d] - verts_tet[a]

    # Project vc and vd perpendicular to edge
    edge_unit = edge_vec / np.linalg.norm(edge_vec)
    vc_perp = vc - np.dot(vc, edge_unit) * edge_unit
    vd_perp = vd - np.dot(vd, edge_unit) * edge_unit

    # Dihedral angle
    cos_angle = np.dot(vc_perp, vd_perp) / (np.linalg.norm(vc_perp) * np.linalg.norm(vd_perp))
    cos_angle = np.clip(cos_angle, -1, 1)
    return np.arccos(cos_angle)

# Build edge-to-cells mapping
edge_to_cells = {(i, j): [] for i, j in edge_list}
for c_idx, cell in enumerate(cells):
    # Each tet has 6 edges
    for pair in combinations(range(4), 2):
        a, b = cell[pair[0]], cell[pair[1]]
        key = (min(a, b), max(a, b))
        if key in edge_to_cells:
            edge_to_cells[key].append(c_idx)

# Check how many cells per edge
cells_per_edge_counts = [len(v) for v in edge_to_cells.values()]
print(f"Cells per edge: min={min(cells_per_edge_counts)}, max={max(cells_per_edge_counts)}, mode={max(set(cells_per_edge_counts), key=cells_per_edge_counts.count)}")

# Compute deficit angles
print("\nComputing deficit angles at each edge...")
deficit_angles = []
dihedral_sums = []

for (ei, ej), cell_indices in edge_to_cells.items():
    dihedral_sum = 0
    for c_idx in cell_indices:
        cell = cells[c_idx]
        cell_verts = [vertices[v] for v in cell]
        # Find which local indices correspond to ei, ej
        local_a = list(cell).index(ei)
        local_b = list(cell).index(ej)
        angle = compute_dihedral_at_edge(cell_verts[0], cell_verts[1],
                                          cell_verts[2], cell_verts[3],
                                          (local_a, local_b))
        dihedral_sum += angle
    deficit = 2 * np.pi - dihedral_sum
    deficit_angles.append(deficit)
    dihedral_sums.append(dihedral_sum)

deficit_angles = np.array(deficit_angles)
dihedral_sums = np.array(dihedral_sums)

print(f"Deficit angles: min={np.degrees(deficit_angles.min()):.4f} deg, "
      f"max={np.degrees(deficit_angles.max()):.4f} deg, "
      f"mean={np.degrees(deficit_angles.mean()):.4f} deg")
print(f"Dihedral sum per edge: mean={np.degrees(dihedral_sums.mean()):.4f} deg")
print(f"  (If = 360 deg, deficit = 0, flat; < 360 = positive curvature)")

total_deficit = np.sum(deficit_angles)
print(f"\nTotal deficit angle sum: {total_deficit:.6f} rad = {np.degrees(total_deficit):.4f} deg")

# For Regge calculus: the Regge action is S = sum_edges (edge_length * deficit_angle)
# For the 600-cell on a unit 3-sphere, all edges have the same length
edge_length = nn_dist
S_regge = edge_length * total_deficit
print(f"Regge action: S = l * sum(deficit) = {edge_length:.6f} * {total_deficit:.6f} = {S_regge:.6f}")

# The cosmological constant in Regge calculus: Lambda * V = S (for pure gravity)
# Volume of the 600-cell inscribed in unit S^3
# Volume of unit S^3 = 2*pi^2
vol_S3 = 2 * np.pi**2
print(f"Volume of unit S^3: {vol_S3:.6f}")

# Volume of one regular tetrahedron with edge length l
l = edge_length
vol_tet = l**3 / (6 * np.sqrt(2))
vol_600cell = n_cells * vol_tet
print(f"Volume of one tet (edge={l:.6f}): {vol_tet:.8f}")
print(f"Total 600-cell volume (600 tets): {vol_600cell:.6f}")

# Lambda from Regge
if abs(vol_600cell) > 1e-15:
    Lambda_regge = S_regge / vol_600cell
    print(f"\nLambda_Regge = S / V = {Lambda_regge:.6f}")
else:
    Lambda_regge = 0
    print("Volume too small to compute Lambda_Regge")

# Gauss-Bonnet check
# For a 3-sphere (which the 600-cell triangulates), chi = 0
# So the total curvature should sum to 8*pi^2 * chi = 0
chi_600cell = n_verts - n_edges + n_faces - n_cells
print(f"\nEuler characteristic: V - E + F - C = {n_verts} - {n_edges} + {n_faces} - {n_cells} = {chi_600cell}")
print(f"  (S^3 has chi = 0)")

# --- PHI-DEFORMED 600-CELL ---
print("\n--- PHI-DEFORMED 600-CELL ---")
print("Deforming edge lengths by phi^alpha and computing how deficit angles change")

def compute_regge_for_deformation(alpha):
    """Compute Regge action for 600-cell with edges scaled by phi^alpha."""
    l_def = edge_length * phi**alpha
    # For small deformations, the deficit angles change
    # In a homogeneous deformation, deficit angles stay the same
    # But the Regge action scales as l * deficit
    S_def = l_def * total_deficit
    V_def = n_cells * (l_def**3 / (6 * np.sqrt(2)))
    if abs(V_def) > 1e-15:
        Lambda_def = S_def / V_def
    else:
        Lambda_def = 0
    return S_def, V_def, Lambda_def

print(f"\n  {'alpha':>10s}  {'S_Regge':>12s}  {'Volume':>12s}  {'Lambda':>12s}  {'Lambda/4pi':>12s}")
for alpha in np.linspace(-2, 2, 21):
    S_def, V_def, L_def = compute_regge_for_deformation(alpha)
    print(f"  {alpha:10.2f}  {S_def:12.6f}  {V_def:12.6f}  {L_def:12.6f}  {L_def/(4*np.pi):12.6f}")

# Non-uniform deformation: split edges into types based on phi structure
# The E8 -> H4 projection creates two types of edges:
# "observable" (phi-weighted) and "hidden" (1-weighted)
print("\n--- Non-uniform deformation: observable vs hidden edges ---")
print("In E8->H4 projection, edge weights differ by phi factors")

# Classify edges by the phi-content of their vertex coordinates
# The 600-cell vertices come in 3 types; edges between different types
# may have different "phi weight"
# Simple model: deform edges whose midpoint has large phi-component

midpoints = np.array([(vertices[i] + vertices[j]) / 2 for i, j in edge_list])
# The "phi content" of a vector: project onto phi-dependent basis
# Use the absolute value of the coordinate closest to phi/2
phi_content = np.max(np.abs(midpoints), axis=1)

# Split edges into "high phi" and "low phi"
median_phi = np.median(phi_content)

for delta in [0.01, 0.05, 0.1, 0.2, 0.5]:
    # Scale "high phi" edges by (1+delta), "low phi" by (1-delta)
    deficit_deformed = []
    for e_idx, (ei, ej) in enumerate(edge_list):
        if phi_content[e_idx] > median_phi:
            l_e = edge_length * (1 + delta)
        else:
            l_e = edge_length * (1 - delta)
        deficit_deformed.append(l_e * deficit_angles[e_idx])
    S_deformed = np.sum(deficit_deformed)
    # Approximate volume (first-order)
    avg_scale = 1  # Mean scale factor
    V_deformed = vol_600cell  # Approximate
    Lambda_deformed = S_deformed / V_deformed if V_deformed > 1e-15 else 0
    print(f"  delta={delta:.2f}: S_deformed={S_deformed:.6f}, Lambda={Lambda_deformed:.6f}")

# Normalizations for Regge approach
print(f"\n--- Regge normalizations (target = {OMEGA_LAMBDA_OBS}) ---")
regge_vals = {
    "Lambda_regge":                          Lambda_regge,
    "Lambda_regge / (4*pi)":                 Lambda_regge / (4 * np.pi),
    "Lambda_regge / (8*pi^2)":               Lambda_regge / (8 * np.pi**2),
    "Lambda_regge * l^2":                    Lambda_regge * edge_length**2,
    "Lambda_regge * l^2 / (4*pi)":           Lambda_regge * edge_length**2 / (4 * np.pi),
    "S_regge":                               S_regge,
    "S_regge / (2*pi)":                      S_regge / (2 * np.pi),
    "S_regge / (4*pi)":                      S_regge / (4 * np.pi),
    "S_regge / (8*pi^2)":                    S_regge / (8 * np.pi**2),
    "S_regge / vol_S3":                      S_regge / vol_S3,
    "S_regge / (vol_S3 * 4*pi)":             S_regge / (vol_S3 * 4 * np.pi),
    "total_deficit / (2*pi*n_edges)":        total_deficit / (2 * np.pi * n_edges),
    "total_deficit / (4*pi*n_edges)":        total_deficit / (4 * np.pi * n_edges),
    "mean_deficit / (2*pi)":                 deficit_angles.mean() / (2 * np.pi),
    "S_regge * phi / vol_S3":               S_regge * phi / vol_S3,
    "S_regge / (dim(E8)*vol_S3)":            S_regge / (dim_E8 * vol_S3),
}

for name, val in sorted(regge_vals.items(), key=lambda x: abs(x[1] - OMEGA_LAMBDA_OBS)):
    err = abs(val - OMEGA_LAMBDA_OBS) / OMEGA_LAMBDA_OBS * 100
    marker = " *** MATCH ***" if err < 1 else (" <-- close" if err < 5 else "")
    print(f"  {name:45s} = {val:12.6f}  ({err:7.2f}%){marker}")


# ######################################################################
# APPROACH 3: SPECTRAL ACTION PRINCIPLE (CONNES-STYLE)
# ######################################################################
print()
print("=" * 78)
print("APPROACH 3: SPECTRAL ACTION (Connes NCG)")
print("=" * 78)

# In the spectral action: S = Tr(f(D^2/Lambda^2))
# The Seeley-DeWitt coefficients determine the action:
# S ~ f_4 * a_0 * Lambda^4 + f_2 * a_2 * Lambda^2 + f_0 * a_4 + ...
# where a_0 = total volume, a_2 ~ integral of scalar curvature, etc.

# For a lattice Dirac operator:
# D = oriented adjacency (with signs from edge orientation)
print("\nBuilding lattice Dirac operator...")

# Simple lattice Dirac: D_{ij} = +1 if edge i->j, -1 if edge j->i, 0 otherwise
# Use the adjacency with signs from a fixed orientation
D_dirac = np.zeros((n_verts, n_verts))
for i, j in edge_list:
    D_dirac[i, j] = 1.0
    D_dirac[j, i] = -1.0

# D should be anti-symmetric (anti-Hermitian up to i factor)
print(f"Dirac operator shape: {D_dirac.shape}")
print(f"Anti-symmetry check: {np.allclose(D_dirac, -D_dirac.T)}")

# D^2 = -D^T D (since D is anti-symmetric, D^2 = D @ D = -D^T @ D)
D2 = D_dirac @ D_dirac
evals_D2 = np.linalg.eigvalsh(D2)
evals_D2 = np.sort(evals_D2)
print(f"D^2 eigenvalues: min={evals_D2[0]:.6f}, max={evals_D2[-1]:.6f}")
print(f"  (Note: D^2 should be negative semi-definite since D is anti-symmetric)")

# Use |D^2| eigenvalues
absD2 = np.abs(evals_D2)
absD2_sorted = np.sort(absD2)

# Actually, use D^T D which is positive semi-definite
DtD = D_dirac.T @ D_dirac
evals_DtD = np.linalg.eigvalsh(DtD)
evals_DtD = np.sort(evals_DtD)
print(f"\nD^T D eigenvalues: min={evals_DtD[0]:.6f}, max={evals_DtD[-1]:.6f}")
print(f"  Note: D^T D = graph Laplacian (for oriented adjacency)")
print(f"  Check: DtD ~= L0? {np.allclose(DtD, L0)}")

# Seeley-DeWitt coefficients for the lattice
# a_0 = Tr(1) = dimension of Hilbert space
# On the lattice: a_0 = N_verts (or N_verts * internal DOF)
a_0_plain = n_verts
a_0_E8 = n_verts * dim_E8  # With E8 gauge
a_0_spinor_E8 = n_verts * dim_E8 * 4  # With 4D spinors

print(f"\n--- Seeley-DeWitt a_0 ---")
print(f"  a_0 (plain):          {a_0_plain}")
print(f"  a_0 (E8 gauge):       {a_0_E8}")
print(f"  a_0 (spinor x E8):    {a_0_spinor_E8}")

# The spectral action: S = sum_k f(lambda_k / Lambda_cutoff^2)
# For f = characteristic function (sharp cutoff at Lambda):
# S_cutoff = number of eigenvalues of |D| below Lambda

# a_2 involves scalar curvature
# For lattice: a_2 ~ sum_edges (edge_length * deficit_angle) ~ Regge action
a_2_lattice = S_regge
print(f"  a_2 (Regge):          {a_2_lattice:.6f}")

# The cosmological constant in the spectral action is:
# Lambda_cosmo = (f_2 / f_4) * (a_0 / a_2) * (something)
# But we can be more direct.

# In Connes' model: Lambda_cosmo ~ a_0 / volume in Planck units
# The ratio a_0 / vol gives the cosmological constant scale

# On the 600-cell: vol = vol_600cell, a_0 = n_verts
print(f"\n--- Spectral action normalizations (target = {OMEGA_LAMBDA_OBS}) ---")

# The key spectral action quantities
# Spectral action with cutoff: S(Lambda) = sum_k f(lambda_k/Lambda^2)
# For f = step function and Lambda -> infinity, dominated by a_0 * Lambda^4
# For the lattice, the natural cutoff is the maximum eigenvalue

Lambda_max = np.sqrt(evals_DtD[-1])
print(f"  Natural lattice cutoff Lambda_max = sqrt(max eig) = {Lambda_max:.6f}")

# Counting function N(E) = number of eigenvalues of |D| below E
# This is the "spectral density"
evals_absD = np.sqrt(np.abs(evals_DtD))
evals_absD_sorted = np.sort(evals_absD)

# Spectral action quantities
S_spectral_total = np.sum(evals_DtD)  # Tr(D^2) = total spectral weight
print(f"  Tr(D^T D) = {S_spectral_total:.6f}")

# Heat kernel: Tr(exp(-t D^T D))
for t in [0.01, 0.1, 1.0]:
    Z_t = np.sum(np.exp(-t * evals_DtD))
    print(f"  Tr(exp(-{t} D^T D)) = {Z_t:.6f}")

# The cosmological constant relates to the spectral zeta function
# zeta_D(s) = sum |lambda_k|^(-2s)
# Lambda_cosmo ~ zeta_D(0) / zeta_D(1) or similar

nonzero_DtD = evals_DtD[evals_DtD > 1e-8]
zeta_D_1 = np.sum(nonzero_DtD**(-1))  # = Tr(|D|^{-2})
zeta_D_half = np.sum(nonzero_DtD**(-0.5))  # = Tr(|D|^{-1})
print(f"\n  zeta_D(1) = Tr(|D|^{{-2}}) = {zeta_D_1:.6f}")
print(f"  zeta_D(1/2) = Tr(|D|^{{-1}}) = {zeta_D_half:.6f}")

spectral_norms = {
    "a_0 / (a_0_E8)":                       a_0_plain / a_0_E8,
    "a_0 / (dim(E8) * phi^2)":              a_0_plain / (dim_E8 * phi**2),
    "a_0_E8 / (a_0_spinor_E8)":             a_0_E8 / a_0_spinor_E8,
    "1/phi":                                 1/phi,
    "zeta_D(1) / n_verts":                   zeta_D_1 / n_verts,
    "zeta_D(1) / dim(E8)":                   zeta_D_1 / dim_E8,
    "zeta_D(1) / edges":                     zeta_D_1 / n_edges,
    "zeta_D(1/2) / n_verts":                 zeta_D_half / n_verts,
    "zeta_D(1/2) / dim(E8)":                 zeta_D_half / dim_E8,
    "zeta_D(1/2) / edges":                   zeta_D_half / n_edges,
    "zeta_D(1/2) / (n_verts*phi)":           zeta_D_half / (n_verts * phi),
    "Tr(DtD) / (n_verts * dim(E8))":         S_spectral_total / (n_verts * dim_E8),
    "Tr(DtD) / (edges * dim(E8))":           S_spectral_total / (n_edges * dim_E8),
    "Tr(DtD) / edges^2":                     S_spectral_total / n_edges**2,
    "n_verts / (edges*phi)":                  n_verts / (n_edges * phi),
    "a_2 / (4*pi*a_0)":                      a_2_lattice / (4 * np.pi * a_0_plain),
    "a_2 / (4*pi*a_0_E8)":                   a_2_lattice / (4 * np.pi * a_0_E8),
    "a_2 / (8*pi^2*a_0)":                    a_2_lattice / (8 * np.pi**2 * a_0_plain),
    "a_2 / (vol_S3 * a_0)":                  a_2_lattice / (vol_S3 * a_0_plain),
    "a_2 / (vol_S3 * dim(E8))":              a_2_lattice / (vol_S3 * dim_E8),
    "E_scalar / (verts * dim(E8) * phi)":     E_scalar / (n_verts * dim_E8 * phi),
    "E_scalar * phi^(-7)":                    E_scalar * phi**(-7),
    "E_scalar * phi^(-8)":                    E_scalar * phi**(-8),
}

for name, val in sorted(spectral_norms.items(), key=lambda x: abs(x[1] - OMEGA_LAMBDA_OBS)):
    err = abs(val - OMEGA_LAMBDA_OBS) / OMEGA_LAMBDA_OBS * 100
    marker = " *** MATCH ***" if err < 1 else (" <-- close" if err < 5 else "")
    print(f"  {name:45s} = {val:12.6f}  ({err:7.2f}%){marker}")


# ######################################################################
# COMPREHENSIVE SCAN: ALL COMBINATIONS
# ######################################################################
print()
print("=" * 78)
print("COMPREHENSIVE SCAN: searching for ANY combination giving 0.6889")
print("=" * 78)

# All the key quantities we've computed
quantities = {
    "E_scalar": E_scalar,
    "E_1form": E_gauge_raw,
    "E_down": E_down,
    "E_up": E_up,
    "S_regge": S_regge,
    "total_deficit": total_deficit,
    "Lambda_regge": Lambda_regge,
    "vol_600cell": vol_600cell,
    "edge_length": edge_length,
    "zeta_D_1": zeta_D_1,
    "zeta_D_half": zeta_D_half,
    "Tr_DtD": S_spectral_total,
}

constants = {
    "phi": phi,
    "phi^2": phi**2,
    "phi^3": phi**3,
    "pi": np.pi,
    "2pi": 2*np.pi,
    "4pi": 4*np.pi,
    "8pi^2": 8*np.pi**2,
    "2pi^2": 2*np.pi**2,
    "dim_E8": 248,
    "roots_E8": 240,
    "n_verts": 120,
    "n_edges": 720,
    "n_faces": 1200,
    "n_cells": 600,
    "12 (degree)": 12,
    "30 (Coxeter)": 30,
    "eps": eps,
}

matches = []

for q_name, q_val in quantities.items():
    if abs(q_val) < 1e-15:
        continue
    for c1_name, c1_val in constants.items():
        # q / c1
        ratio1 = q_val / c1_val
        err1 = abs(ratio1 - OMEGA_LAMBDA_OBS) / OMEGA_LAMBDA_OBS * 100
        if err1 < 1.0:
            matches.append((f"{q_name} / {c1_name}", ratio1, err1))

        # q * c1
        prod1 = q_val * c1_val
        err_p1 = abs(prod1 - OMEGA_LAMBDA_OBS) / OMEGA_LAMBDA_OBS * 100
        if err_p1 < 1.0:
            matches.append((f"{q_name} * {c1_name}", prod1, err_p1))

        for c2_name, c2_val in constants.items():
            # q / (c1 * c2)
            ratio2 = q_val / (c1_val * c2_val)
            err2 = abs(ratio2 - OMEGA_LAMBDA_OBS) / OMEGA_LAMBDA_OBS * 100
            if err2 < 1.0:
                matches.append((f"{q_name} / ({c1_name} * {c2_name})", ratio2, err2))

            # q * c1 / c2
            if abs(c2_val) > 1e-15:
                ratio3 = q_val * c1_val / c2_val
                err3 = abs(ratio3 - OMEGA_LAMBDA_OBS) / OMEGA_LAMBDA_OBS * 100
                if err3 < 1.0:
                    matches.append((f"{q_name} * {c1_name} / {c2_name}", ratio3, err3))

# Deduplicate and sort by error
seen = set()
unique_matches = []
for name, val, err in sorted(matches, key=lambda x: x[2]):
    val_rounded = round(val, 8)
    if val_rounded not in seen:
        seen.add(val_rounded)
        unique_matches.append((name, val, err))

if unique_matches:
    print(f"\nFound {len(unique_matches)} combinations matching 0.6889 to < 1%:")
    for name, val, err in unique_matches[:50]:
        print(f"  {name:60s} = {val:.6f}  (err: {err:.4f}%)")
else:
    print("\nNo combinations of the form Q / (C1*C2) or Q*C1/C2 match 0.6889 to < 1%.")
    print("Expanding search to < 5%...")
    for q_name, q_val in quantities.items():
        if abs(q_val) < 1e-15:
            continue
        for c1_name, c1_val in constants.items():
            ratio1 = q_val / c1_val
            err1 = abs(ratio1 - OMEGA_LAMBDA_OBS) / OMEGA_LAMBDA_OBS * 100
            if err1 < 5.0:
                matches.append((f"{q_name} / {c1_name}", ratio1, err1))
            for c2_name, c2_val in constants.items():
                ratio2 = q_val / (c1_val * c2_val)
                err2 = abs(ratio2 - OMEGA_LAMBDA_OBS) / OMEGA_LAMBDA_OBS * 100
                if err2 < 5.0:
                    matches.append((f"{q_name} / ({c1_name} * {c2_name})", ratio2, err2))

    seen = set()
    unique_matches = []
    for name, val, err in sorted(matches, key=lambda x: x[2]):
        val_rounded = round(val, 6)
        if val_rounded not in seen:
            seen.add(val_rounded)
            unique_matches.append((name, val, err))

    if unique_matches:
        print(f"Found {len(unique_matches)} combinations matching to < 5%:")
        for name, val, err in unique_matches[:30]:
            print(f"  {name:60s} = {val:.6f}  (err: {err:.4f}%)")
    else:
        print("No combinations match even to 5%.")


# ######################################################################
# SUMMARY
# ######################################################################
print()
print("=" * 78)
print("FINAL SUMMARY")
print("=" * 78)

print(f"""
600-cell structure:
  Vertices: {n_verts}, Edges: {n_edges}, Faces: {n_faces}, Cells: {n_cells}
  Euler char: {chi_600cell}
  Edge length: {edge_length:.6f} (~1/phi = {1/phi:.6f})

APPROACH 1: Gauge Field Casimir (1-form Laplacian)
  E_1 (raw 1-form Casimir): {E_gauge_raw:.6f}
  E_1 with E8 (x248):       {E_gauge_E8:.4f}
  Best match: {best_gauge[0] if best_gauge else 'None'}
              = {best_gauge[1]:.6f} (err: {best_gauge[2]:.2f}%) if best_gauge else ''

APPROACH 2: Regge Calculus
  Mean deficit angle: {np.degrees(deficit_angles.mean()):.4f} deg
  Total deficit: {total_deficit:.6f} rad
  Regge action: {S_regge:.6f}
  Lambda_Regge: {Lambda_regge:.6f}

APPROACH 3: Spectral Action
  a_0 (vertices): {a_0_plain}
  a_0 (E8):       {a_0_E8}
  zeta_D(1):      {zeta_D_1:.6f}
  zeta_D(1/2):    {zeta_D_half:.6f}

Target: Omega_Lambda = {OMEGA_LAMBDA_OBS}
""")

# Final honest assessment
n_good_matches = len([m for m in unique_matches if m[2] < 1.0]) if unique_matches else 0
n_close_matches = len([m for m in unique_matches if m[2] < 5.0]) if unique_matches else 0

if n_good_matches > 0:
    print(f"RESULT: Found {n_good_matches} combination(s) matching Omega_Lambda to < 1%.")
    print("However, with ~{} quantities x ~{} constants^2 = ~{} combinations tested,".format(
        len(quantities), len(constants), len(quantities) * len(constants)**2))
    print("finding a match by chance is expected (look-elsewhere effect).")
    print("A genuine derivation requires a PHYSICAL justification for the normalization.")
elif n_close_matches > 0:
    print(f"RESULT: Found {n_close_matches} combination(s) within 5%, but none below 1%.")
    print("No clean derivation of Omega_Lambda from these approaches.")
else:
    print("RESULT: No simple combination of lattice quantities reproduces Omega_Lambda.")

print("""
HONEST ASSESSMENT:
  The three approaches (gauge Casimir, Regge calculus, spectral action)
  produce well-defined geometric quantities from the 600-cell, but none
  yields Omega_Lambda = 0.6889 from a natural, physically motivated
  normalization. Any match found in the comprehensive scan must be
  evaluated for look-elsewhere effect: with hundreds of trial
  combinations, a ~1% match is statistically expected by chance.

  The phi-power formula for Omega_Lambda may require:
  (a) A different geometric construction (not just the symmetric 600-cell)
  (b) Additional physical input (running couplings, threshold corrections)
  (c) The full E8 lattice structure, not just its H4 projection
  (d) An entirely different derivation pathway
""")
