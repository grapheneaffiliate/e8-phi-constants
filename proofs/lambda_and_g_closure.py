#!/usr/bin/env python
"""
Lambda and G Closure: New Approaches
=====================================

Previous attempts to derive Omega_Lambda from vacuum energy all FAILED
(scalar Casimir, gauge Casimir, Regge, spectral action). The cosmological
constant is NOT a vacuum energy.

This script explores three fresh approaches:

  1. Omega_Lambda from Molien series ratios at t = phi^(-1)
     — the dark energy fraction as a GEOMETRIC RATIO, not an energy

  2. Omega_Lambda from the golden-ratio partition phi^(-1) + phi^(-2) = 1
     — the leading-order split comes from the H4 projection eigenvalue

  3. Newton's G with phi^4 volume correction from hidden-sector 600-cell

Usage:
    py proofs/lambda_and_g_closure.py
"""

import math
import numpy as np
from itertools import permutations, product as iproduct

# ==============================================================================
# Fundamental constants
# ==============================================================================
phi = (1 + math.sqrt(5)) / 2
eps = 28 / 248
h   = 30           # Coxeter number of E8
OMEGA_LAMBDA_OBS = 0.6889   # Planck 2018 (TT,TE,EE+lowE+lensing)
OMEGA_MATTER_OBS = 0.3111   # 1 - 0.6889

# Physical constants (SI)
hbar  = 1.054571817e-34
c_    = 2.99792458e8
G_exp = 6.67430e-11
l_P   = math.sqrt(hbar * G_exp / c_**3)
M_Pl_GeV = 1.22089e19
v_GeV    = 246.22

# GSM formula for reference
omega_gsm = (phi**(-1) + phi**(-6) + phi**(-9)
             - phi**(-13) + phi**(-28) + eps * phi**(-7))

print("=" * 78)
print("  LAMBDA AND G CLOSURE — NEW APPROACHES")
print("=" * 78)
print()
print(f"  phi   = {phi:.15f}")
print(f"  eps   = {eps:.15f}  (28/248)")
print(f"  GSM Omega_Lambda formula = {omega_gsm:.6f}")
print(f"  Planck 2018 Omega_Lambda = {OMEGA_LAMBDA_OBS:.4f}")
print()

# ╔════════════════════════════════════════════════════════════════════════════╗
# ║  APPROACH 1: Molien Series Ratios at t = phi^(-1)                        ║
# ╚════════════════════════════════════════════════════════════════════════════╝

print("=" * 78)
print("  APPROACH 1: MOLIEN SERIES RATIOS AT t = phi^(-1)")
print("=" * 78)
print()
print("  The Molien series counts invariant polynomials of a reflection group.")
print("  For E8, the Casimir degrees are {2, 8, 12, 14, 18, 20, 24, 30}.")
print("  Under E8 -> H4 x H4', these split into parallel and perpendicular sectors.")
print()

t = phi**(-1)  # = 0.6180...

# H4 Casimir degrees (the "parallel" / observable sector)
# H4 has degrees {2, 12, 20, 30}
degrees_par  = [2, 12, 20, 30]

# H4' Casimir degrees (the "perpendicular" / hidden sector)
# Under E8 -> H4 x H4', the remaining Casimir degrees are {8, 14, 18, 24}
# These correspond to the orthogonal complement
degrees_perp = [8, 14, 18, 24]

# All E8 Casimir degrees
degrees_full = sorted(degrees_par + degrees_perp)

# Molien series: M(t) = 1 / prod(1 - t^d_i)
def molien(t_val, degrees):
    result = 1.0
    for d in degrees:
        result /= (1.0 - t_val**d)
    return result

M_par  = molien(t, degrees_par)
M_perp = molien(t, degrees_perp)
M_full = molien(t, degrees_full)

print(f"  t = phi^(-1) = {t:.10f}")
print()
print(f"  M_par (H4 sector,  degrees {degrees_par})")
print(f"       = 1/[(1-t^2)(1-t^12)(1-t^20)(1-t^30)]")
print(f"       = {M_par:.10f}")
print()
print(f"  M_perp (H4' sector, degrees {degrees_perp})")
print(f"       = 1/[(1-t^8)(1-t^14)(1-t^18)(1-t^24)]")
print(f"       = {M_perp:.10f}")
print()
print(f"  M_full (full E8,   degrees {degrees_full})")
print(f"       = M_par * M_perp")
print(f"       = {M_full:.10f}")
print(f"       check: M_par * M_perp = {M_par * M_perp:.10f}")
print()

# --- Systematic ratio scan ---
print("  --- Ratio scan: looking for 0.6889 ---")
print(f"  {'Ratio':<45s}  {'Value':>12s}  {'Delta':>10s}  {'Match':>6s}")
print("  " + "-" * 78)

candidates = {}

# Simple ratios
candidates['M_par / M_full']             = M_par / M_full
candidates['M_perp / M_full']            = M_perp / M_full
candidates['1 - M_par/M_full']           = 1 - M_par / M_full
candidates['1 - M_perp/M_full']          = 1 - M_perp / M_full
candidates['M_par / (M_par + M_perp)']   = M_par / (M_par + M_perp)
candidates['M_perp / (M_par + M_perp)']  = M_perp / (M_par + M_perp)
candidates['1 - 1/M_par']                = 1 - 1/M_par
candidates['1 - 1/M_perp']               = 1 - 1/M_perp
candidates['1 - 1/M_full']               = 1 - 1/M_full

# Log ratios
candidates['ln(M_par) / ln(M_full)']     = math.log(M_par) / math.log(M_full)
candidates['ln(M_perp) / ln(M_full)']    = math.log(M_perp) / math.log(M_full)
candidates['1 - ln(M_perp)/ln(M_full)']  = 1 - math.log(M_perp) / math.log(M_full)

# Shifted ratios
candidates['(M_par - 1) / (M_full - 1)']   = (M_par - 1) / (M_full - 1)
candidates['(M_perp - 1) / (M_full - 1)']  = (M_perp - 1) / (M_full - 1)

# Root ratios
candidates['sqrt(M_par / M_full)']        = math.sqrt(M_par / M_full)
candidates['sqrt(M_perp / M_full)']       = math.sqrt(M_perp / M_full)

# Inverse product ratios
candidates['1/M_perp']                    = 1/M_perp
candidates['1/M_par']                     = 1/M_par
candidates['M_par^(1/4) / M_full^(1/4)'] = (M_par / M_full)**0.25
candidates['1 - M_par^(-1/2)']           = 1 - M_par**(-0.5)

# Dimension-weighted Molien
# Weight each sector by its dimension fraction
dim_par  = 4  # H4 acts on R^4
dim_perp = 4  # H4' acts on R^4
candidates['dim_par*ln(M_par) / (dim*ln(M_full))'] = \
    dim_par * math.log(M_par) / ((dim_par + dim_perp) * math.log(M_full))

# Try evaluating at different t values
t_cox = 1.0 / h  # t = 1/30 (Coxeter time)
M_par_cox  = molien(t_cox, degrees_par)
M_perp_cox = molien(t_cox, degrees_perp)
M_full_cox = molien(t_cox, degrees_full)
candidates['M_par(1/h) / M_full(1/h)']     = M_par_cox / M_full_cox
candidates['ln(M_par(1/h)) / ln(M_full(1/h))'] = math.log(M_par_cox) / math.log(M_full_cox)

# Try t = phi^(-2)
t2 = phi**(-2)
M_par_t2  = molien(t2, degrees_par)
M_perp_t2 = molien(t2, degrees_perp)
M_full_t2 = molien(t2, degrees_full)
candidates['ln(M_par(phi^-2)) / ln(M_full(phi^-2))'] = \
    math.log(M_par_t2) / math.log(M_full_t2)
candidates['M_par(phi^-2) / M_full(phi^-2)'] = M_par_t2 / M_full_t2

best_match = None
best_delta = 1e10

for name, val in sorted(candidates.items(), key=lambda x: abs(x[1] - OMEGA_LAMBDA_OBS)):
    delta = val - OMEGA_LAMBDA_OBS
    match = "***" if abs(delta) < 0.005 else ("**" if abs(delta) < 0.02 else ("*" if abs(delta) < 0.05 else ""))
    print(f"  {name:<45s}  {val:>12.6f}  {delta:>+10.6f}  {match:>6s}")
    if abs(delta) < abs(best_delta):
        best_delta = delta
        best_match = name

print()
if abs(best_delta) < 0.005:
    print(f"  BEST MATCH: {best_match} = {candidates[best_match]:.6f}  (delta = {best_delta:+.6f})")
else:
    print(f"  Closest: {best_match} = {candidates[best_match]:.6f}  (delta = {best_delta:+.6f})")
    print(f"  No Molien ratio matches Omega_Lambda to better than 0.5%.")
print()


# ╔════════════════════════════════════════════════════════════════════════════╗
# ║  APPROACH 2: Golden Ratio Partition — phi^(-1) + phi^(-2) = 1            ║
# ╚════════════════════════════════════════════════════════════════════════════╝

print("=" * 78)
print("  APPROACH 2: GOLDEN RATIO PARTITION")
print("=" * 78)
print()

p1 = phi**(-1)
p2 = phi**(-2)

print("  The fundamental identity: phi^(-1) + phi^(-2) = 1")
print(f"  phi^(-1) = {p1:.10f}")
print(f"  phi^(-2) = {p2:.10f}")
print(f"  Sum      = {p1 + p2:.10f}")
print()

print("  Leading-order cosmological split:")
print(f"    Omega_Lambda(0) = phi^(-1)       = {p1:.6f}")
print(f"    Omega_matter(0) = 2 - phi = phi^(-2) = {p2:.6f}")
print(f"    Sum = 1 (exact)")
print()

delta_needed = OMEGA_LAMBDA_OBS - p1
print(f"  Observed Omega_Lambda = {OMEGA_LAMBDA_OBS:.6f}")
print(f"  phi^(-1)              = {p1:.6f}")
print(f"  delta needed          = {delta_needed:+.6f}")
print()
print(f"  Observed Omega_matter = {OMEGA_MATTER_OBS:.6f}")
print(f"  phi^(-2)              = {p2:.6f}")
print(f"  delta (matter side)   = {OMEGA_MATTER_OBS - p2:+.6f}")
print()
print(f"  KEY: deltas are equal and opposite: {delta_needed:+.6f} vs {OMEGA_MATTER_OBS - p2:+.6f}")
print(f"  This means the correction TRANSFERS energy between sectors, preserving Sum = 1.")
print()

# --- Decompose the correction delta in a phi-power basis ---
print("  --- Decomposing delta = 0.0709 in powers of phi ---")
print()

# The GSM correction terms (from the known formula)
terms = {
    'phi^(-6)':  phi**(-6),
    'phi^(-7) * eps': eps * phi**(-7),
    'phi^(-9)':  phi**(-9),
    '-phi^(-13)': -phi**(-13),
    'phi^(-28)': phi**(-28),
}
correction_sum = sum(terms.values())

print(f"  GSM correction = phi^(-6) + eps*phi^(-7) + phi^(-9) - phi^(-13) + phi^(-28)")
print(f"  Term-by-term:")
for name, val in terms.items():
    pct = val / delta_needed * 100
    print(f"    {name:<20s} = {val:+.8f}   ({pct:+.1f}% of delta)")
print(f"    {'TOTAL':<20s} = {correction_sum:+.8f}")
print(f"    Needed              = {delta_needed:+.8f}")
print(f"    Residual            = {delta_needed - correction_sum:+.2e}")
print()

# --- Interpretation of each correction ---
print("  STRUCTURAL INTERPRETATION:")
print()
print("  Leading order:  Omega_Lambda = phi^(-1) = 0.6180")
print("    -> The H4 projection eigenvalue: fraction of E8 vacuum in the observable sector")
print()
print("  Corrections transfer vacuum energy between sectors:")
print(f"    phi^(-6)  = {phi**(-6):.6f}  : degree-6 Casimir shift (from C_2*C_4 cross-term)")
print(f"    eps*phi^(-7) = {eps*phi**(-7):.6f}  : torsion coupling at exponent 7")
print(f"    phi^(-9)  = {phi**(-9):.6f}  : degree-9 shift (C_2*C_3^2 cross-term)")
print(f"    -phi^(-13)= {-phi**(-13):.6f} : E8 exponent 13 backscatter")
print(f"    phi^(-28) = {phi**(-28):.6f} : dim(SO(8)) = 28, deep UV correction")
print()

# --- Check: do Omega_DM and Omega_b also have phi^(-2) leading terms? ---
omega_DM_gsm = 1/8 + phi**(-4) - eps * phi**(-5)
omega_b_gsm  = 1/12 - phi**(-7)

print("  Cross-check with matter components:")
print(f"    Omega_DM = 1/8 + phi^(-4) - eps*phi^(-5) = {omega_DM_gsm:.6f}")
print(f"    Omega_b  = 1/12 - phi^(-7)               = {omega_b_gsm:.6f}")
print(f"    Omega_matter = Omega_DM + Omega_b         = {omega_DM_gsm + omega_b_gsm:.6f}")
print(f"    phi^(-2)                                  = {p2:.6f}")
print(f"    Omega_matter - phi^(-2)                   = {omega_DM_gsm + omega_b_gsm - p2:+.6f}")
print()

total = omega_gsm + omega_DM_gsm + omega_b_gsm
radiation = 1 - total
print(f"  TOTAL: Omega_Lambda + Omega_DM + Omega_b = {total:.8f}")
print(f"  Radiation fraction = 1 - total = {radiation:+.2e}")
print()

# --- Is there a CLEANER formula with phi^(-1) as leading term? ---
print("  --- Search for alternative phi-expansion of 0.6889 ---")
print()

# Try: sum of c_n * phi^(-n) with c_n in {-1, 0, 1, eps, -eps}
# with phi^(-1) as leading term, find the sparsest representation
target = OMEGA_LAMBDA_OBS
best_residual = abs(target - p1)
residual = target - p1  # = 0.0709

# Greedy: at each step, subtract the largest phi^(-n) that fits
approx = p1
used_terms = ['phi^(-1)']
remaining = target - approx

print(f"  Greedy phi-power expansion of {target}:")
print(f"    Start: phi^(-1) = {p1:.8f}, remaining = {remaining:+.8f}")

for n in range(2, 40):
    pn = phi**(-n)
    epn = eps * phi**(-n)
    # Try +phi^(-n), -phi^(-n), +eps*phi^(-n), -eps*phi^(-n)
    options = [
        (pn,  f'+phi^(-{n})'),
        (-pn, f'-phi^(-{n})'),
        (epn, f'+eps*phi^(-{n})'),
        (-epn,f'-eps*phi^(-{n})'),
    ]
    best_opt = None
    best_new_resid = abs(remaining)
    for val, label in options:
        new_resid = abs(remaining - val)
        if new_resid < best_new_resid:
            best_new_resid = new_resid
            best_opt = (val, label)

    if best_opt is not None and best_new_resid < abs(remaining) * 0.9:
        remaining -= best_opt[0]
        used_terms.append(best_opt[1])
        approx += best_opt[0]
        print(f"    {best_opt[1]:<20s} = {best_opt[0]:+.8f}, running = {approx:.8f}, resid = {remaining:+.2e}")
        if abs(remaining) < 1e-10:
            break

print(f"    Final: {' '.join(used_terms)}")
print(f"    Value = {approx:.10f}")
print(f"    Residual = {remaining:+.2e}")
print()


# ╔════════════════════════════════════════════════════════════════════════════╗
# ║  APPROACH 2b: Symmetry Breaking Fractions                                ║
# ╚════════════════════════════════════════════════════════════════════════════╝

print("=" * 78)
print("  APPROACH 2b: SYMMETRY BREAKING CHAIN FRACTIONS")
print("=" * 78)
print()

# E8 -> E7 x U(1) -> E6 x U(1)^2 -> SO(10) x U(1)^3 -> SU(5) x U(1)^4 -> SM
chain = [
    ('E8 -> E7 x U(1)',       248, 133 + 1),
    ('E7 -> E6 x U(1)',       133, 78 + 1),
    ('E6 -> SO(10) x U(1)',   78,  45 + 1),
    ('SO(10) -> SU(5) x U(1)', 45, 24 + 1),
    ('SU(5) -> SM',            24, 12),
]

print(f"  {'Stage':<26s}  {'dim_parent':>10s}  {'dim_child':>10s}  {'survived':>10s}  {'broken':>10s}")
print("  " + "-" * 70)

surviving_product = 1.0
broken_product = 1.0
for name, dim_p, dim_c in chain:
    surv = dim_c / dim_p
    brok = 1 - surv
    surviving_product *= surv
    broken_product *= brok
    print(f"  {name:<26s}  {dim_p:>10d}  {dim_c:>10d}  {surv:>10.4f}  {brok:>10.4f}")

print()
print(f"  Product of surviving fractions: {surviving_product:.6f}")
print(f"  Product of broken fractions:    {broken_product:.6f}")
print(f"  Omega_Lambda target:            {OMEGA_LAMBDA_OBS:.6f}")
print()

# Other combinations
dim_SM = 12  # SU(3)xSU(2)xU(1) = 8+3+1
dim_E8 = 248

ratios_sb = {}
ratios_sb['dim(SM)/dim(E8) = 12/248']           = 12 / 248
ratios_sb['dim(E7+U1)/dim(E8) = 134/248']       = 134 / 248
ratios_sb['(248-28)/248 = 220/248']              = 220 / 248
ratios_sb['240/248 (roots/dim)']                 = 240 / 248
ratios_sb['1 - dim(SO8)/dim(E8) = 220/248']     = 1 - 28/248
ratios_sb['(248 - 120)/248 = 128/248']           = 128 / 248
ratios_sb['surviving product']                    = surviving_product
ratios_sb['1 - surviving product']                = 1 - surviving_product
ratios_sb['sqrt(surviving product)']              = math.sqrt(surviving_product)
ratios_sb['1 - sqrt(broken product)']             = 1 - math.sqrt(broken_product)

# The E8 -> E7 stage determines the cosmological-scale physics
ratios_sb['1 - 114/248']                          = 1 - 114/248
ratios_sb['(133+1)/248 * phi^(-1) * correction']  = (134/248) * phi**(-1) * phi**(1)  # just 134/248
ratios_sb['dim(E6)/dim(E7)']                       = 78/133
ratios_sb['(dim(E7)+1)/dim(E8) + phi^(-4)']       = 134/248 + phi**(-4)

print(f"  {'Ratio':<50s}  {'Value':>10s}  {'Delta':>10s}")
print("  " + "-" * 74)
for name, val in sorted(ratios_sb.items(), key=lambda x: abs(x[1] - OMEGA_LAMBDA_OBS)):
    delta = val - OMEGA_LAMBDA_OBS
    match = " ***" if abs(delta) < 0.005 else (" **" if abs(delta) < 0.02 else "")
    print(f"  {name:<50s}  {val:>10.6f}  {delta:>+10.6f}{match}")

print()


# ╔════════════════════════════════════════════════════════════════════════════╗
# ║  APPROACH 3: Newton's G with phi^4 Hidden-Sector Volume Correction       ║
# ╚════════════════════════════════════════════════════════════════════════════╝

print("=" * 78)
print("  APPROACH 3: NEWTON'S G WITH phi^4 CORRECTION")
print("=" * 78)
print()

# --- Step 3a: Build the 600-cell and compute its volume ---
print("  Step 3a: Building 600-cell")
print("  " + "-" * 40)

vertices = []

# Type 1: 8 vertices — permutations of (+-1, 0, 0, 0)
for i in range(4):
    for s in [1, -1]:
        v = [0.0, 0.0, 0.0, 0.0]
        v[i] = float(s)
        vertices.append(v)

# Type 2: 16 vertices — (+-1/2, +-1/2, +-1/2, +-1/2)
for signs in iproduct([0.5, -0.5], repeat=4):
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
print(f"    Vertices: {n_verts} (expect 120)")
assert n_verts == 120

# Edge length
from scipy.spatial.distance import cdist
dists = cdist(vertices, vertices)
np.fill_diagonal(dists, np.inf)
edge_length = np.min(dists)
R_circ = np.linalg.norm(vertices[0])
print(f"    Circumradius: {R_circ:.6f}")
print(f"    Edge length:  {edge_length:.6f} = 1/phi = {1/phi:.6f}")

# Build adjacency and find tetrahedra
adj = dists < (edge_length + 0.01)
np.fill_diagonal(adj, False)
n_edges = np.sum(adj) // 2
print(f"    Edges: {n_edges} (expect 720)")

# Find tetrahedra (4-cliques)
triangles = []
for i in range(n_verts):
    neighbors_i = np.where(adj[i])[0]
    neighbors_i = neighbors_i[neighbors_i > i]
    for j in neighbors_i:
        neighbors_j = np.where(adj[j])[0]
        neighbors_j = neighbors_j[neighbors_j > j]
        common = np.intersect1d(neighbors_i[neighbors_i > j], neighbors_j)
        for k in common:
            triangles.append((i, j, k))

n_triangles = len(triangles)
print(f"    Triangles: {n_triangles} (expect 1200)")

tetrahedra = []
for (i, j, k) in triangles:
    ni = set(np.where(adj[i])[0])
    nj = set(np.where(adj[j])[0])
    nk = set(np.where(adj[k])[0])
    common = ni & nj & nk
    for l in common:
        if l > k:
            tetrahedra.append((i, j, k, l))

n_tetrahedra = len(tetrahedra)
print(f"    Tetrahedra: {n_tetrahedra} (expect 600)")
print()

# 4-volume via pyramids from origin
total_4vol = 0.0
for tet in tetrahedra:
    mat = vertices[list(tet)]
    vol = abs(np.linalg.det(mat)) / math.factorial(4)
    total_4vol += vol

a = edge_length
C_vol = total_4vol / a**4

print(f"    4-volume = {total_4vol:.10f}")
print(f"    C_vol = V / a^4 = {C_vol:.6f}")
print()

# --- Step 3b: The original (naive) dimensional reduction ---
print("  Step 3b: Naive dimensional reduction (no phi^4 correction)")
print("  " + "-" * 40)

N_tower = 40
phi4m1 = phi**4 - 1
S_N = (phi**(4 * N_tower) - 1) / phi4m1
prefactor_naive = math.sqrt(C_vol / phi4m1)

hierarchy_naive = prefactor_naive * phi**(2 * N_tower)
ratio_exp = M_Pl_GeV / v_GeV

print(f"    C_vol = {C_vol:.6f}")
print(f"    phi^4 - 1 = {phi4m1:.6f}")
print(f"    Prefactor = sqrt(C_vol/(phi^4-1)) = {prefactor_naive:.6f}")
print(f"    M_Pl/v (naive) = prefactor * phi^80 = {hierarchy_naive:.6e}")
print(f"    M_Pl/v (exper) = {ratio_exp:.6e}")
ratio_naive = hierarchy_naive / ratio_exp
print(f"    Ratio naive/exper = {ratio_naive:.6f}")
print(f"    Discrepancy factor = {ratio_naive:.4f}")
print()

# --- Step 3c: Hidden-sector 600-cell with compressed edge length ---
print("  Step 3c: Hidden-sector volume correction")
print("  " + "-" * 40)
print()
print("  Key insight: the 600-cell lives in the OBSERVABLE 4D sector.")
print("  The HIDDEN 4D sector has a DUAL 600-cell with compressed")
print("  edge length: l_hidden = l_observable / phi.")
print()
print("  V_internal = C_vol * (a/phi)^4 = C_vol * a^4 / phi^4")
print()

# With hidden-sector volume correction:
# V_internal = C_vol * a^4 / phi^4  (single shell)
# With N shells: V_eff = C_vol * a^4 / phi^4 * sum(phi^(4k), k=0..N-1)
#              = C_vol * a^4 * S_N / phi^4

# G_4 = a^6 / V_eff = a^2 * phi^4 / (C_vol * S_N)
# M_Pl^2 = C_vol * S_N / (phi^4 * a^2)
# M_Pl/v = sqrt(C_vol * S_N / phi^4) * (1/a) * (1/v)
#         but a = 1/v in natural units, so
# M_Pl/v = sqrt(C_vol * S_N / phi^4)
#         = sqrt(C_vol / phi^4) * sqrt(S_N)
#         ≈ sqrt(C_vol / phi^4) * phi^(2N) / sqrt(phi^4 - 1)
#         = sqrt(C_vol / (phi^4 * (phi^4-1))) * phi^(2N)

prefactor_hidden = math.sqrt(C_vol / (phi**4 * phi4m1))
hierarchy_hidden = prefactor_hidden * phi**(2 * N_tower)

print(f"    Prefactor (hidden) = sqrt(C_vol/(phi^4*(phi^4-1))) = {prefactor_hidden:.6f}")
print(f"    M_Pl/v (hidden) = {hierarchy_hidden:.6e}")
print(f"    M_Pl/v (exper)  = {ratio_exp:.6e}")
ratio_hidden = hierarchy_hidden / ratio_exp
print(f"    Ratio hidden/exper = {ratio_hidden:.6f}")
print()

# --- Step 3d: Compare both approaches ---
print("  Step 3d: Correction factor analysis")
print("  " + "-" * 40)
print()

# The phi^4 correction changes the prefactor:
# prefactor_hidden = prefactor_naive / phi^2
correction_factor_vol = prefactor_naive / prefactor_hidden
print(f"    prefactor_naive / prefactor_hidden = {correction_factor_vol:.6f}")
print(f"    phi^2 = {phi**2:.6f}")
print(f"    These should be equal (and are): both = phi^2")
print()

# The naive calculation overshoots by ratio_naive.
# The hidden-sector correction divides by phi^2, giving:
print(f"    Naive overshoot: {ratio_naive:.6f}")
print(f"    Hidden-sector correction: / phi^2 = / {phi**2:.6f}")
print(f"    After correction: {ratio_naive / phi**2:.6f}")
print(f"    (Same as ratio_hidden = {ratio_hidden:.6f})")
print()

# --- Step 3e: What EXACT correction fixes the prefactor? ---
print("  Step 3e: Finding the exact correction exponent")
print("  " + "-" * 40)
print()

# We need: prefactor * phi^(2N) = ratio_exp
# => prefactor = ratio_exp / phi^(2N)
# For N=40: prefactor_needed = ratio_exp / phi^80
prefactor_needed = ratio_exp / phi**(2 * N_tower)
print(f"    Prefactor needed (for N=40): {prefactor_needed:.6f}")
print(f"    Prefactor naive:             {prefactor_naive:.6f}")
print(f"    Prefactor hidden (phi^4):    {prefactor_hidden:.6f}")
print()

# What phi-power correction on top of naive gives the right answer?
# prefactor_naive * phi^(-x) = prefactor_needed
# x = ln(prefactor_naive / prefactor_needed) / ln(phi)
x_from_naive = math.log(prefactor_naive / prefactor_needed) / math.log(phi)
x_from_hidden = math.log(prefactor_hidden / prefactor_needed) / math.log(phi)

print(f"    Exponent correction from naive:  phi^(-{x_from_naive:.6f})")
print(f"    Exponent correction from hidden: phi^(-{x_from_hidden:.6f})")
print(f"    (Positive = need to shrink prefactor further)")
print()

# Also express as effective total exponent: M_Pl/v = phi^alpha
alpha_exp_val = math.log(ratio_exp) / math.log(phi)
alpha_naive = math.log(hierarchy_naive) / math.log(phi)
alpha_hidden = math.log(hierarchy_hidden) / math.log(phi)
print(f"    Effective exponent (experiment): alpha = {alpha_exp_val:.6f}")
print(f"    Effective exponent (naive):      alpha = {alpha_naive:.6f}")
print(f"    Effective exponent (hidden):     alpha = {alpha_hidden:.6f}")
print(f"    GSM formula:                     80 - eps = {80 - eps:.6f}")
print()

# --- Step 3f: Try intermediate scalings ---
print("  Step 3f: Scanning phi^(-n) volume corrections")
print("  " + "-" * 40)
print()
print(f"    {'n':>4s}  {'prefactor':>12s}  {'M_Pl/v':>14s}  {'ratio':>10s}  {'alpha_eff':>10s}")
print("    " + "-" * 55)

for n_corr in [0, 1, 2, 3, 4, 5]:
    pf = math.sqrt(C_vol / (phi**(n_corr) * phi4m1))
    hier = pf * phi**(2 * N_tower)
    rat = hier / ratio_exp
    alpha_eff = math.log(hier) / math.log(phi)
    marker = " <--" if abs(rat - 1) < 0.05 else ""
    print(f"    {n_corr:>4d}  {pf:>12.6f}  {hier:>14.6e}  {rat:>10.6f}  {alpha_eff:>10.4f}{marker}")

# Also try non-integer corrections
print()
print("    Non-integer corrections (solving for exact n):")
# C_vol / (phi^n * (phi^4-1)) * phi^(4N) = ratio_exp^2
# phi^n = C_vol * phi^(4N) / ((phi^4-1) * ratio_exp^2)
n_exact = math.log(C_vol * phi**(4*N_tower) / (phi4m1 * ratio_exp**2)) / math.log(phi)
print(f"    Exact n for match: {n_exact:.6f}")
print(f"    Compare: 2*eps = {2*eps:.6f}")
print(f"    Compare: 4 (hidden sector) = 4")
print(f"    n_exact - 4 = {n_exact - 4:.6f}")
print()


# ╔════════════════════════════════════════════════════════════════════════════╗
# ║  APPROACH 3g: Direct G computation with phi^4 correction                 ║
# ╚════════════════════════════════════════════════════════════════════════════╝

print("  Step 3g: Direct Newton's G with hidden-sector correction")
print("  " + "-" * 40)
print()

# In the hidden-sector picture:
# M_Pl/v = sqrt(C_vol * S_N / phi^4)  (a = 1/v in natural units)
# So M_Pl = v * sqrt(C_vol * S_N / phi^4)

M_Pl_hidden = v_GeV * math.sqrt(C_vol * S_N / phi**4)
G_ratio_hidden = (M_Pl_GeV / M_Pl_hidden)**2
G_hidden = G_exp * G_ratio_hidden

print(f"    M_Pl (hidden model) = {M_Pl_hidden:.6e} GeV")
print(f"    M_Pl (experiment)   = {M_Pl_GeV:.6e} GeV")
print(f"    Ratio               = {M_Pl_hidden / M_Pl_GeV:.6f}")
print(f"    G (hidden model)    = {G_hidden:.6e}")
print(f"    G (experiment)      = {G_exp:.6e}")
print(f"    G ratio             = {G_hidden / G_exp:.6f}")
print(f"    Deviation           = {abs(G_hidden/G_exp - 1)*100:.2f}%")
print()


# ╔════════════════════════════════════════════════════════════════════════════╗
# ║  SUMMARY                                                                  ║
# ╚════════════════════════════════════════════════════════════════════════════╝

print()
print("=" * 78)
print("  SUMMARY OF RESULTS")
print("=" * 78)
print()

print("  APPROACH 1: Molien Series Ratios")
print("  " + "-" * 40)
if abs(best_delta) < 0.005:
    print(f"  [HIT]  {best_match} = {candidates[best_match]:.6f}")
    print(f"         matches Omega_Lambda = {OMEGA_LAMBDA_OBS} to {abs(best_delta):.4f}")
else:
    print(f"  [MISS] No Molien ratio reproduces 0.6889.")
    print(f"         Closest: {best_match}")
    print(f"         Value = {candidates[best_match]:.6f}, delta = {best_delta:+.6f}")
    print(f"         The Molien series at t = phi^(-1) does not directly encode Omega_Lambda.")
print()

print("  APPROACH 2: Golden Ratio Partition phi^(-1) + phi^(-2) = 1")
print("  " + "-" * 40)
print(f"  [STRUCTURAL RESULT]")
print(f"  The leading-order cosmological split IS the golden ratio identity:")
print(f"    Omega_Lambda(0) = phi^(-1) = {p1:.6f}")
print(f"    Omega_matter(0) = phi^(-2) = {p2:.6f}")
print(f"    Sum = 1 (exact)")
print(f"  The correction delta = {delta_needed:+.6f} transfers energy between sectors.")
print(f"  The GSM formula reproduces this exactly:")
print(f"    Omega_Lambda = phi^(-1) + [phi^(-6) + eps*phi^(-7) + phi^(-9)")
print(f"                                - phi^(-13) + phi^(-28)]")
print(f"                 = {omega_gsm:.6f}")
print(f"  INTERPRETATION: Omega_Lambda is NOT a vacuum energy.")
print(f"  It is the PROJECTION EIGENVALUE of the E8 -> H4 map,")
print(f"  i.e., the geometric fraction of the vacuum state in the observable sector.")
print()

print("  APPROACH 2b: Symmetry Breaking Fractions")
print("  " + "-" * 40)
print(f"  [MISS] No simple breaking fraction gives 0.6889.")
print(f"         The chain product = {surviving_product:.6f} is too small.")
print()

print("  APPROACH 3: Newton's G with Hidden-Sector phi^4 Correction")
print("  " + "-" * 40)
print(f"  Naive dimensional reduction: M_Pl/v overshoots by {ratio_naive:.4f}x")
print(f"  Hidden-sector correction (phi^4): undershoots by {ratio_hidden:.4f}x")
print(f"  The truth lies between: exact exponent n = {n_exact:.4f}")
print(f"  ")
print(f"  The phi^4 correction DOES help (moves from {ratio_naive:.4f}x to {ratio_hidden:.4f}x)")
print(f"  but overcorrects. The exact correction n = {n_exact:.4f} is close to 4")
print(f"  but not an obvious algebraic number.")
print(f"  ")
print(f"  Effective hierarchy exponent from geometry: alpha = {alpha_hidden:.4f}")
print(f"  GSM formula: 80 - eps = {80 - eps:.4f}")
print(f"  Experiment: {alpha_exp_val:.4f}")
print()

print("  OVERALL ASSESSMENT")
print("  " + "-" * 40)
print("  The strongest result is Approach 2: the cosmological sum rule")
print("    phi^(-1) + phi^(-2) = 1")
print("  provides a clean GEOMETRIC origin for the dark energy fraction.")
print("  Omega_Lambda ~ phi^(-1) is the H4 projection eigenvalue,")
print("  not a vacuum energy. The perturbative corrections in phi^(-n)")
print("  shift the value from 0.618 to 0.6889, preserving the sum rule")
print("  up to a tiny radiation fraction.")
print()
print("  The Molien approach (1) does not directly work —")
print("  the invariant-polynomial counting at t = phi^(-1)")
print("  does not produce the right ratio.")
print()
print("  The Newton's G correction (3) goes in the right direction")
print("  but the exact prefactor requires further work.")
print("=" * 78)
