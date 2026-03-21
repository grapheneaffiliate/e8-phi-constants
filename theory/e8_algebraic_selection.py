#!/usr/bin/env python
"""
E8 Algebraic Selection Rules — Deriving GSM exponents from Lie algebra structure.

Five independent approaches:
  1. Coxeter element in H4 basis (trace analysis)
  2. Molien series for E8/H4
  3. E8 theta function at q = phi^{-1}
  4. Weight lattice projection and phi-adic structure
  5. Combined Feynman-rule test

Statistical validation via hypergeometric p-values.
"""

import os, sys, csv, warnings
import numpy as np
from numpy.linalg import eig, matrix_power, det, inv
import sympy as sp
from sympy import sqrt as Sqrt, Rational, cos, pi, GoldenRatio, simplify, nsimplify
from scipy.special import comb as scipy_comb
from scipy.stats import hypergeom
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore")

OUT = os.path.dirname(os.path.abspath(__file__))
phi_num = (1 + np.sqrt(5)) / 2          # golden ratio ≈ 1.618
phi_inv = 1.0 / phi_num                  # ≈ 0.618

GSM_EXPONENTS = sorted({1,2,3,4,5,6,7,8,9,10,12,13,14,15,16,17,18,20,24,26,27,33,34})
GSM_SET = set(GSM_EXPONENTS)
N_MAX = 40    # scan range

# ─────────────────────────────────────────────────────────────────────
# E8 Cartan matrix
# ─────────────────────────────────────────────────────────────────────
C_E8 = np.array([
    [ 2,-1, 0, 0, 0, 0, 0, 0],
    [-1, 2,-1, 0, 0, 0, 0, 0],
    [ 0,-1, 2,-1, 0, 0, 0,-1],
    [ 0, 0,-1, 2,-1, 0, 0, 0],
    [ 0, 0, 0,-1, 2,-1, 0, 0],
    [ 0, 0, 0, 0,-1, 2,-1, 0],
    [ 0, 0, 0, 0, 0,-1, 2, 0],
    [ 0, 0,-1, 0, 0, 0, 0, 2]
], dtype=float)

# Simple roots in the standard basis (rows of identity — we work in root-space
# where the inner product is given by the Cartan matrix inverse).
# For reflections we need <α_i, α_j> = C_ij  (since all roots long, <α,α>=2).

def simple_reflection(i, C):
    """Reflection matrix s_i in root-coordinate basis."""
    n = C.shape[0]
    S = np.eye(n)
    for j in range(n):
        S[j, i] = S[j, i] - C[i, j]   # s_i(e_j) = e_j - C_{ij} e_i
    return S

# ─────────────────────────────────────────────────────────────────────
# APPROACH 1 — Coxeter element
# ─────────────────────────────────────────────────────────────────────
print("=" * 72)
print("APPROACH 1: Coxeter Element in H4 Basis")
print("=" * 72)

# Build Coxeter element w = s1 s2 ... s8
w = np.eye(8)
for i in range(8):
    w = w @ simple_reflection(i, C_E8)

evals_w = np.linalg.eigvals(w)
# Sort by argument
args = np.angle(evals_w)
order = np.argsort(args)
evals_w = evals_w[order]

coxeter_exponents = sorted({1, 7, 11, 13, 17, 19, 23, 29})
expected_args = sorted([2 * np.pi * m / 30 for m in coxeter_exponents]
                       + [-2 * np.pi * m / 30 for m in coxeter_exponents])[:8]

print("Coxeter element eigenvalues (argument × 30/2π):")
computed_ms = sorted(set(round(abs(np.angle(e)) * 30 / (2*np.pi)) for e in evals_w))
print(f"  Computed exponents: {computed_ms}")
print(f"  Expected:           {coxeter_exponents}")

# Eigenvectors — split into parallel (H4) and perpendicular subspaces
evals_full, evecs_full = np.linalg.eig(w)
# Identify parallel indices: m in {1, 11, 19, 29}
parallel_ms = {1, 11, 19, 29}
perp_ms     = {7, 13, 17, 23}

par_idx = []
perp_idx = []
for k, ev in enumerate(evals_full):
    m = round(abs(np.angle(ev)) * 30 / (2*np.pi))
    if m in parallel_ms:
        par_idx.append(k)
    elif m in perp_ms:
        perp_idx.append(k)

# Build change-of-basis: columns = parallel eigenvectors, then perpendicular
T = np.column_stack([evecs_full[:, k] for k in par_idx + perp_idx])

# w in block-diagonal basis
w_block = np.linalg.inv(T) @ w @ T
w_par  = w_block[:4, :4]
w_perp = w_block[4:, 4:]

# Verify traces
print(f"\nTr(w_par)  = {np.trace(w_par):.6f}")
print(f"Tr(w_perp) = {np.trace(w_perp):.6f}")

# Powers of w — Coxeter selection function
coxeter_traces = {}
n_range = np.arange(1, N_MAX+1)
tr_par  = np.zeros(N_MAX)
tr_perp = np.zeros(N_MAX)
tr_diff = np.zeros(N_MAX)
tr_full = np.zeros(N_MAX)

for idx, n in enumerate(n_range):
    wp_n = matrix_power(w_par,  int(n)) if n <= 100 else np.linalg.matrix_power(w_par, int(n))
    wq_n = matrix_power(w_perp, int(n)) if n <= 100 else np.linalg.matrix_power(w_perp, int(n))
    tp = np.real(np.trace(wp_n))
    tq = np.real(np.trace(wq_n))
    tr_par[idx]  = tp
    tr_perp[idx] = tq
    tr_diff[idx] = tp - tq
    tr_full[idx] = tp + tq
    coxeter_traces[n] = {"par": tp, "perp": tq, "diff": tp - tq}

# Symbolic trace computation using exact eigenvalues
print("\nSymbolic trace analysis (mod 30 arithmetic):")
print(f"  {'n':>3}  {'Tr_par':>10}  {'Tr_perp':>10}  {'|Diff|':>10}")
print("  " + "-"*40)
for n in range(1, N_MAX+1):
    # Exact: Tr(w_par^n) = sum_{m in {1,11,19,29}} 2cos(2πmn/30)
    tp_exact = sum(2*np.cos(2*np.pi*m*n/30) for m in [1,11,19,29])
    tq_exact = sum(2*np.cos(2*np.pi*m*n/30) for m in [7,13,17,23])
    diff = abs(tp_exact - tq_exact)
    coxeter_traces[n]["diff_exact"] = diff
    if diff > 1e-6:
        # Check if diff is a recognizable phi expression
        phi_power = np.log(abs(diff)) / np.log(phi_num) if diff > 0.01 else -99
        tag = ""
        if abs(phi_power - round(phi_power)) < 0.05 and abs(round(phi_power)) <= 10:
            tag = f"  ~ phi^{int(round(phi_power))}"
        elif abs(diff - round(diff)) < 1e-6:
            tag = f"  = {int(round(diff))}"
        print(f"  {n:3d}  {tp_exact:10.4f}  {tq_exact:10.4f}  {diff:10.4f}{tag}")

C_n = np.array([abs(coxeter_traces[n]["diff_exact"]) for n in range(1, N_MAX+1)])

# ── Coxeter plot ─────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(12, 5))
ax.bar(n_range, C_n, color="steelblue", alpha=0.7, label="|Tr(w_par^n) - Tr(w_perp^n)|")
for g in GSM_EXPONENTS:
    if g <= N_MAX:
        ax.axvline(g, color="red", ls="--", alpha=0.5, lw=0.8)
ax.set_xlabel("n")
ax.set_ylabel("C(n)")
ax.set_title("Approach 1: Coxeter Selection Function")
ax.legend()
fig.tight_layout()
fig.savefig(os.path.join(OUT, "e8_coxeter_traces.png"), dpi=150)
plt.close(fig)
print(f"\n  → Saved e8_coxeter_traces.png")

# Determine which n are "selected" by Coxeter (C(n) > threshold)
coxeter_threshold = 0.5
coxeter_selected = set(n for n in range(1, N_MAX+1) if C_n[n-1] > coxeter_threshold)
print(f"  Coxeter selected (|diff| > {coxeter_threshold}): {sorted(coxeter_selected)}")

# ─────────────────────────────────────────────────────────────────────
# APPROACH 2 — Molien Series E8/H4
# ─────────────────────────────────────────────────────────────────────
print("\n" + "=" * 72)
print("APPROACH 2: Molien Series for E8/H4")
print("=" * 72)

# E8 degrees: {2,8,12,14,18,20,24,30}
# H4 degrees: {2,12,20,30}
# Complementary degrees: {8,14,18,24}
comp_degrees = [8, 14, 18, 24]
print(f"Complementary degrees (E8 \\ H4): {comp_degrees}")

# M_{E8/H4}(t) = 1/[(1-t^8)(1-t^14)(1-t^18)(1-t^24)]
# Expand as power series: sum a_n t^n

# Compute by polynomial multiplication up to degree N_MAX
# Start with 1, then multiply by 1/(1-t^d) = 1 + t^d + t^{2d} + ...
max_deg = N_MAX + 10
molien_coeffs = np.zeros(max_deg + 1)
molien_coeffs[0] = 1.0

for d in comp_degrees:
    new_coeffs = np.zeros(max_deg + 1)
    for k in range(max_deg + 1):
        # accumulate: new_coeffs[k] = sum_{j=0}^{k//d} molien_coeffs[k - j*d]
        j = 0
        while j * d <= k:
            new_coeffs[k] += molien_coeffs[k - j * d]
            j += 1
    molien_coeffs = new_coeffs

print(f"\nMolien coefficients a_n for n=0..{N_MAX}:")
print(f"  {'n':>3}  {'a_n':>6}  {'a_n·phi^(-n)':>14}")
print("  " + "-" * 30)
molien_weighted = np.zeros(N_MAX + 1)
for n in range(N_MAX + 1):
    a_n = int(round(molien_coeffs[n]))
    w_n = a_n * phi_inv**n
    molien_weighted[n] = w_n
    if a_n > 0:
        print(f"  {n:3d}  {a_n:6d}  {w_n:14.8f}")

# Evaluate at t = phi^{-1}
M_val = 1.0
for d in comp_degrees:
    M_val /= (1 - phi_inv**d)
print(f"\nM_{{E8/H4}}(phi^{{-1}}) = {M_val:.10f}")
print(f"Sum of series (check):  {sum(molien_weighted):.10f}")

# Nonzero Molien exponents
molien_selected = set(n for n in range(1, N_MAX+1) if molien_coeffs[n] > 0.5)
print(f"Nonzero Molien exponents (n=1..{N_MAX}): {sorted(molien_selected)}")

# ── Molien plot ──────────────────────────────────────────────────────
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

ns_plot = np.arange(1, N_MAX+1)
an_plot = [molien_coeffs[n] for n in ns_plot]
ax1.bar(ns_plot, an_plot, color="darkgreen", alpha=0.7)
for g in GSM_EXPONENTS:
    if g <= N_MAX:
        ax1.axvline(g, color="red", ls="--", alpha=0.5, lw=0.8)
ax1.set_xlabel("n")
ax1.set_ylabel("a_n")
ax1.set_title("Molien coefficients a_n")

aw_plot = [molien_weighted[n] for n in ns_plot]
ax2.bar(ns_plot, aw_plot, color="teal", alpha=0.7)
for g in GSM_EXPONENTS:
    if g <= N_MAX:
        ax2.axvline(g, color="red", ls="--", alpha=0.5, lw=0.8)
ax2.set_xlabel("n")
ax2.set_ylabel("a_n · φ^{-n}")
ax2.set_title("Molien coefficients weighted by φ^{-n}")

fig.suptitle("Approach 2: Molien Series E8/H4", fontsize=13)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "e8_molien_coefficients.png"), dpi=150)
plt.close(fig)
print(f"  → Saved e8_molien_coefficients.png")

# ─────────────────────────────────────────────────────────────────────
# APPROACH 3 — E8 Theta Function
# ─────────────────────────────────────────────────────────────────────
print("\n" + "=" * 72)
print("APPROACH 3: E8 Theta Function at q = φ^{-1}")
print("=" * 72)

def sigma3(n):
    """Sum of cubes of divisors of n."""
    s = 0
    for d in range(1, int(n**0.5) + 1):
        if n % d == 0:
            s += d**3
            if d != n // d:
                s += (n // d)**3
    return s

N_THETA = 200
# Compute terms
theta_terms = np.zeros(N_THETA + 1)
theta_terms[0] = 1.0
for n in range(1, N_THETA + 1):
    theta_terms[n] = 240 * sigma3(n) * phi_inv**n

Theta_total = np.sum(theta_terms)
print(f"Theta_E8(phi^{{-1}}) = {Theta_total:.6f}")
print(f"  (first term = 1, remaining = {Theta_total - 1:.6f})")

# Information content
I_n = np.zeros(N_THETA + 1)
for n in range(1, N_THETA + 1):
    I_n[n] = theta_terms[n] / Theta_total

# Cumulative convergence
cumsum = np.cumsum(theta_terms) / Theta_total
n99 = np.searchsorted(cumsum, 0.99)
n999 = np.searchsorted(cumsum, 0.999)
print(f"  99% convergence at n = {n99}")
print(f"  99.9% convergence at n = {n999}")

# Top contributing terms
print(f"\nTop 30 terms by information content I(n) = 240·σ₃(n)·φ^{{-n}} / Θ:")
print(f"  {'n':>3}  {'σ₃(n)':>10}  {'240·σ₃(n)':>12}  {'term':>14}  {'I(n)':>12}  {'GSM?':>5}")
print("  " + "-" * 62)
top_idx = np.argsort(I_n[1:])[::-1] + 1
theta_selected_1pct = set()
theta_selected_01pct = set()
for rank, n in enumerate(top_idx[:30]):
    s3 = sigma3(n)
    gsm_flag = "***" if n in GSM_SET else ""
    print(f"  {n:3d}  {s3:10d}  {240*s3:12d}  {theta_terms[n]:14.6f}  {I_n[n]:12.8f}  {gsm_flag:>5}")
    if I_n[n] > 0.01:
        theta_selected_1pct.add(n)
    if I_n[n] > 0.001:
        theta_selected_01pct.add(n)

print(f"\n  Terms with I(n) > 1%:  {sorted(theta_selected_1pct)}")
print(f"  Terms with I(n) > 0.1%: {sorted(theta_selected_01pct)}")

# Logarithmic derivative
print("\nLogarithmic derivative Θ'/Θ analysis:")
# Θ'(q) = sum n · 240 · σ₃(n) · q^{n-1}
# q·Θ'(q)/Θ(q) = sum n · 240 · σ₃(n) · q^n / Θ(q)
log_deriv_terms = np.zeros(N_THETA + 1)
for n in range(1, N_THETA + 1):
    log_deriv_terms[n] = n * 240 * sigma3(n) * phi_inv**n / Theta_total

print(f"  q·Θ'/Θ = {np.sum(log_deriv_terms):.6f}")
# Which n dominate the log derivative?
top_ld = np.argsort(log_deriv_terms[1:])[::-1] + 1
print(f"  Top 10 terms in log derivative:")
for n in top_ld[:10]:
    gsm_flag = "***" if n in GSM_SET else ""
    print(f"    n={n:3d}  contribution={log_deriv_terms[n]:.8f}  {gsm_flag}")

# ── Theta plot ───────────────────────────────────────────────────────
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

ns_th = np.arange(1, min(N_MAX+1, N_THETA+1))
In_plot = [I_n[n] for n in ns_th]
colors_th = ["red" if n in GSM_SET else "steelblue" for n in ns_th]
ax1.bar(ns_th, In_plot, color=colors_th, alpha=0.7)
ax1.set_xlabel("n")
ax1.set_ylabel("I(n)")
ax1.set_title("Theta function information content I(n)")
ax1.axhline(0.01, color="gray", ls=":", lw=0.8, label="1% threshold")
ax1.legend()

# Cumulative
ax2.plot(np.arange(N_THETA+1), cumsum, "b-", lw=1.5)
ax2.axhline(0.99, color="gray", ls=":", lw=0.8)
ax2.axhline(0.999, color="gray", ls=":", lw=0.8)
ax2.set_xlabel("n")
ax2.set_ylabel("Cumulative fraction")
ax2.set_title("Theta function cumulative convergence")
ax2.set_xlim(0, 50)

fig.suptitle("Approach 3: E8 Theta Function at q = φ^{-1}", fontsize=13)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "e8_theta_information.png"), dpi=150)
plt.close(fig)
print(f"  → Saved e8_theta_information.png")

# ─────────────────────────────────────────────────────────────────────
# APPROACH 4 — Weight Lattice Projection & phi-adic Products
# ─────────────────────────────────────────────────────────────────────
print("\n" + "=" * 72)
print("APPROACH 4: Weight Lattice Projection & phi-adic Structure")
print("=" * 72)

# Build the 240 E8 roots in root-coordinate basis (α_1..α_8 basis)
# Positive roots of E8: use the Cartan matrix to enumerate
# Instead, use the standard realization in R^8.
# E8 roots (all 240) in the "even coordinate" form:
# Type 1: ±e_i ± e_j  (i<j), i,j in 1..8  → 2*C(8,2)*4 = 224 ... no,
# Actually the standard E8 root system in R^8:
# - All permutations of (±1, ±1, 0, 0, 0, 0, 0, 0): C(8,2)*4 = 112
# - All (±1/2, ..., ±1/2) with even number of minus signs: 2^7 = 128
# Total: 240. ✓

roots_e8 = []

# Type 1: ±e_i ± e_j
for i in range(8):
    for j in range(i+1, 8):
        for si in [1, -1]:
            for sj in [1, -1]:
                v = np.zeros(8)
                v[i] = si
                v[j] = sj
                roots_e8.append(v)

# Type 2: (±1/2)^8 with even number of minus signs
import itertools
for signs in itertools.product([0.5, -0.5], repeat=8):
    if sum(1 for s in signs if s < 0) % 2 == 0:
        roots_e8.append(np.array(signs))

roots_e8 = np.array(roots_e8)
print(f"Number of E8 roots: {len(roots_e8)}")

# Build projection matrix from E8 → H4 (parallel) and E8 → H4_perp
# Use the Coxeter element eigenvectors computed in Approach 1.
# The eigenvectors in root-coordinate basis need to be converted to R^8.
# Actually, we built w in root-coordinates. We need the E8 roots in those
# coordinates too — but we have them in the standard R^8 embedding.
# The eigenvectors of w (built from Cartan matrix reflections) live in
# root-coordinate space. We need the projection in the SAME space as the roots.

# Simpler: diagonalize w in the standard R^8 realization.
# First build w in the standard R^8 basis using the standard root coordinates.
# Simple roots in standard R^8:
alpha = np.zeros((8, 8))
# Standard E8 simple roots (Bourbaki numbering matching our Cartan matrix):
# α_1 = e_1 - e_2
# α_2 = e_2 - e_3
# α_3 = e_3 - e_4
# α_4 = e_4 - e_5
# α_5 = e_5 - e_6
# α_6 = e_6 - e_7
# α_7 = e_7 + e_8   ... wait, need to be careful.

# For the Cartan matrix with node 8 connected to node 3:
# Use a known set of simple roots for E8:
# α_1 = (1,-1,0,0,0,0,0,0)
# α_2 = (0,1,-1,0,0,0,0,0)
# α_3 = (0,0,1,-1,0,0,0,0)
# α_4 = (0,0,0,1,-1,0,0,0)
# α_5 = (0,0,0,0,1,-1,0,0)
# α_6 = (0,0,0,0,0,1,-1,0)
# α_7 = (0,0,0,0,0,1,1,0)
# α_8 = (-1/2,-1/2,-1/2,-1/2,-1/2,-1/2,-1/2,1/2) ... but check Cartan.

# Let me verify: <α_i, α_j> should give C_{ij}/2... no, for simply-laced,
# <α_i, α_j> = C_{ij} since all roots have <α,α> = 2.

# Actually let's just verify the Cartan matrix. C_{ij} = 2<α_i,α_j>/<α_i,α_i>.
# For simply-laced (ADE), <α_i,α_i>=2, so C_{ij} = <α_i,α_j>.

# Standard E8 simple roots that give our Cartan matrix (node 8 → node 3):
alpha[0] = [1,-1, 0, 0, 0, 0, 0, 0]
alpha[1] = [0, 1,-1, 0, 0, 0, 0, 0]
alpha[2] = [0, 0, 1,-1, 0, 0, 0, 0]
alpha[3] = [0, 0, 0, 1,-1, 0, 0, 0]
alpha[4] = [0, 0, 0, 0, 1,-1, 0, 0]
alpha[5] = [0, 0, 0, 0, 0, 1,-1, 0]
alpha[6] = [0, 0, 0, 0, 0, 1, 1, 0]
alpha[7] = [-0.5,-0.5,-0.5,-0.5,-0.5,-0.5,-0.5, 0.5]

# Verify Cartan matrix
C_check = np.zeros((8,8))
for i in range(8):
    for j in range(8):
        C_check[i,j] = round(2 * np.dot(alpha[i], alpha[j]) / np.dot(alpha[i], alpha[i]))

# Check which entry mismatches
mismatch = np.abs(C_check - C_E8)
if np.max(mismatch) > 0.01:
    print(f"  WARNING: Cartan matrix mismatch (max diff = {np.max(mismatch):.4f})")
    print(f"  C_check =\n{C_check}")
    # Try alternative: α_7 = (0,0,0,0,0,1,1,0), α_8 = (-1/2,...,-1/2,1/2)
    # Node 8 connects to node 4 in our numbering.
    # Let me try: node 8 connects to node 3 means C[2,7] = C[7,2] = -1.
    # <α_3, α_8> should be -1.
    # α_3 = (0,0,1,-1,0,0,0,0), α_8 = (-1/2,-1/2,-1/2,-1/2,-1/2,-1/2,-1/2,1/2)
    # <α_3,α_8> = 0+0+(-1/2)-(-1/2)+0+0+0+0 = 0. Not -1.
    #
    # Need: C[7,2] = -1, i.e. node 8 connects to node 3.
    # <α_8, α_3> = -1.
    # Try α_8 = (-1/2,-1/2,-1/2,1/2,1/2,1/2,1/2,-1/2)?
    # Check <α_8,α_8> = 8*(1/4) = 2. ✓
    # <α_3,α_8> = 0+0+(-1/2)+(−1)(1/2)+0+0+0+0 = -1/2 - 1/2 = -1? No.
    # α_3=(0,0,1,-1,0,0,0,0), α_8=(-1/2,-1/2,-1/2,1/2,1/2,1/2,1/2,-1/2)
    # <> = 0+0+1*(-1/2)+(-1)*(1/2)+0+0+0+0 = -1/2-1/2 = -1 ✓
    # Now check <α_8, α_4> where α_4=(0,0,0,1,-1,0,0,0):
    # <> = 0+0+0+1/2+(-1)(1/2)+0+0+0 = 0. Good, C[7,3]=0 ✓ (in 0-indexed C[7,3])
    # Check C[7,k] for all k:
    # <α_8,α_1>: (1)(-1/2)+(-1)(-1/2) = -1/2+1/2 = 0 ✓
    # <α_8,α_2>: (1)(-1/2)+(-1)(-1/2) = 0 ✓ (wait: α_2=(0,1,-1,0,...))
    # = 0+1*(-1/2)+(-1)(-1/2)+0+... = -1/2+1/2 = 0 ✓
    # <α_8,α_5>: α_5=(0,0,0,0,1,-1,0,0) → 0+0+0+0+1/2+(-1)(1/2)+0+0=0 ✓
    # <α_8,α_6>: α_6=(0,0,0,0,0,1,-1,0) → 0+0+0+0+0+1/2+(-1)(1/2)+0=0 ✓
    # <α_8,α_7>: α_7=(0,0,0,0,0,1,1,0) → 0+0+0+0+0+1/2+1/2+0=1 ... should be 0.
    # Hmm, <α_8,α_7> = 1, but C[7,6]=0. That's wrong.
    # Try α_8 with different sign pattern.
    pass

# Let me use a more systematic approach: build w directly in R^8
# using reflections from the simple roots, then eigendecompose.

# Try the standard E8 root system with the Bourbaki labeling:
# The E8 Dynkin diagram: 1-2-3-4-5-6-7 with 8 branching from 3 (our convention)
# But standard Bourbaki has branch at node 4 (or 5 depending on convention).
# Our Cartan matrix has C[2,7]=C[7,2]=-1, meaning node 3 connects to node 8.

# Let's use a different well-known set of simple roots for E8.
# From the D8 sub-root-system approach:
# First 7 roots span a D7 = so(14) sub-system, 8th extends to E8.
# α_i = e_i - e_{i+1} for i=1..6
# α_7 = e_6 + e_7   (this makes D7 with α_1..α_7)
# α_8 = ... for E8 extension

# Actually, let's just be more careful. Our Cartan matrix:
# Row 8 (index 7): only C[7,2]=-1 (and C[7,7]=2)
# So α_8 is connected only to α_3 (index 2).

# Try: keep α_1..α_7 as a D7 system, with α_8 connected to α_3.
# α_1 = e_1-e_2, α_2 = e_2-e_3, ..., α_6 = e_6-e_7
# α_7 = e_6+e_7 (this creates D7)
# Check: <α_6,α_7> = <e_6-e_7, e_6+e_7> = 1-1 = 0. But C[5,6]=-1. ❌

# OK, α_7 should connect to α_6. Standard D_n:
# α_i = e_i - e_{i+1} for i=1..n-1, α_n = e_{n-1}+e_n
# For D7: α_1=e_1-e_2,...,α_6=e_6-e_7, α_7=e_6+e_7
# <α_5,α_6> = <e_5-e_6, e_6-e_7> = 0-1-0 = -1 ✓
# <α_6,α_7> = <e_6-e_7, e_6+e_7> = 1-1 = 0 ❌ but C[5,6]=-1...
# Our Cartan: C[5,6]=-1, C[6,5]=-1. That means α_6 and α_7 ARE connected.
# With α_6=e_6-e_7, α_7=e_6+e_7: <α_6,α_7>=0. Not -1.

# Standard D_n numbering: the LAST root α_n connects to α_{n-2}, not α_{n-1}.
# D7 Dynkin: 1-2-3-4-5<6,7 (fork at node 5).
# But our first 7 nodes are a straight chain: 1-2-3-4-5-6-7.
# That's A7, not D7!

# OK so nodes 1-2-3-4-5-6-7 form an A7 chain, and node 8 branches from node 3.
# This is the E8 Dynkin diagram in standard form where the branch is at node 3.

# For A7: α_i = e_i - e_{i+1}, i=1..7. These give <α_i,α_{i+1}>=-1, rest 0. ✓
# For α_8 connected only to α_3: <α_8, α_3>=-1, <α_8, α_k>=0 for k≠3, <α_8,α_8>=2.
# α_3 = e_3-e_4. So α_8 must have <α_8, e_3-e_4>=-1 and <α_8, e_k-e_{k+1}>=0 for k≠3.
# Also <α_8,α_8>=2.

# Constraints on α_8 = (a_1,...,a_8):
# <α_8, α_1> = a_1 - a_2 = 0
# <α_8, α_2> = a_2 - a_3 = 0
# <α_8, α_3> = a_3 - a_4 = -1
# <α_8, α_4> = a_4 - a_5 = 0
# <α_8, α_5> = a_5 - a_6 = 0
# <α_8, α_6> = a_6 - a_7 = 0
# <α_8, α_7> = a_7 - a_8 = 0
# So: a_1=a_2=a_3, a_4=a_5=a_6=a_7=a_8, a_3-a_4=-1.
# And sum(a_i^2) = 2.
# Let a_1=a_2=a_3=c, a_4=...=a_8=c+1 (since a_3-a_4=-1 → a_4=a_3+1).
# Wait: a_3-a_4=-1 means a_4=a_3+1.
# 3c^2 + 5(c+1)^2 = 2
# 3c^2 + 5c^2 + 10c + 5 = 2
# 8c^2 + 10c + 3 = 0
# c = (-10 ± sqrt(100-96))/16 = (-10 ± 2)/16
# c = -1/2 or c = -3/4

# c=-1/2: α_8 = (-1/2,-1/2,-1/2, 1/2, 1/2, 1/2, 1/2, 1/2)
# Check: <α_8,α_8> = 3/4 + 5/4 = 2 ✓
# <α_8,α_3> = <(-1/2,-1/2,-1/2,1/2,...), (0,0,1,-1,0,0,0,0)> = -1/2-1/2 = -1 ✓

alpha[0] = [1,-1, 0, 0, 0, 0, 0, 0]
alpha[1] = [0, 1,-1, 0, 0, 0, 0, 0]
alpha[2] = [0, 0, 1,-1, 0, 0, 0, 0]
alpha[3] = [0, 0, 0, 1,-1, 0, 0, 0]
alpha[4] = [0, 0, 0, 0, 1,-1, 0, 0]
alpha[5] = [0, 0, 0, 0, 0, 1,-1, 0]
alpha[6] = [0, 0, 0, 0, 0, 0, 1,-1]
alpha[7] = [-0.5,-0.5,-0.5, 0.5, 0.5, 0.5, 0.5, 0.5]

# Verify Cartan matrix
C_check2 = np.zeros((8,8))
for i in range(8):
    for j in range(8):
        C_check2[i,j] = round(2 * np.dot(alpha[i], alpha[j]) / np.dot(alpha[i], alpha[i]))

mismatch2 = np.abs(C_check2 - C_E8)
if np.max(mismatch2) < 0.01:
    print(f"  Cartan matrix verified ✓")
else:
    print(f"  WARNING: Cartan matrix mismatch! max diff = {np.max(mismatch2)}")
    print(f"  C_check2 =\n{C_check2.astype(int)}")

# Build Coxeter element in R^8
def reflection_R8(alpha_vec, x):
    """Reflect x through hyperplane perp to alpha_vec."""
    return x - 2 * np.dot(x, alpha_vec) / np.dot(alpha_vec, alpha_vec) * alpha_vec

def reflection_matrix_R8(alpha_vec):
    """Reflection matrix for simple root alpha_vec."""
    n = len(alpha_vec)
    a = alpha_vec.reshape(-1,1)
    return np.eye(n) - 2 * (a @ a.T) / np.dot(alpha_vec, alpha_vec)

w_R8 = np.eye(8)
for i in range(8):
    w_R8 = w_R8 @ reflection_matrix_R8(alpha[i])

evals_R8 = np.linalg.eigvals(w_R8)
computed_ms_R8 = sorted(set(round(abs(np.angle(e)) * 30 / (2*np.pi)) for e in evals_R8 if abs(e) > 0.5))
print(f"  Coxeter exponents from R^8 realization: {computed_ms_R8}")

# Eigendecompose w_R8
evals_R8, evecs_R8 = np.linalg.eig(w_R8)
par_idx_R8 = []
perp_idx_R8 = []
for k, ev in enumerate(evals_R8):
    m = round(abs(np.angle(ev)) * 30 / (2*np.pi))
    if m in parallel_ms:
        par_idx_R8.append(k)
    elif m in perp_ms:
        perp_idx_R8.append(k)

# Build projection matrices
# We need REAL subspaces. Eigenvectors come in conjugate pairs.
# For real projection, take Re and Im parts of eigenvectors for the parallel space.
par_evecs = evecs_R8[:, par_idx_R8]  # 8x4 complex
# Build real 4D basis for parallel subspace
# Take pairs: if v, v* are conjugate eigenvectors, use Re(v) and Im(v)
real_par_basis = []
used = set()
for k in par_idx_R8:
    if k in used:
        continue
    v = evecs_R8[:, k]
    # Find conjugate
    for k2 in par_idx_R8:
        if k2 != k and k2 not in used:
            if np.allclose(evecs_R8[:, k2], np.conj(v)):
                real_par_basis.append(np.real(v))
                real_par_basis.append(np.imag(v))
                used.add(k)
                used.add(k2)
                break
    if k not in used:
        # Real eigenvector (eigenvalue ±1)
        real_par_basis.append(np.real(v))
        used.add(k)

real_perp_basis = []
used2 = set()
for k in perp_idx_R8:
    if k in used2:
        continue
    v = evecs_R8[:, k]
    for k2 in perp_idx_R8:
        if k2 != k and k2 not in used2:
            if np.allclose(evecs_R8[:, k2], np.conj(v)):
                real_perp_basis.append(np.real(v))
                real_perp_basis.append(np.imag(v))
                used2.add(k)
                used2.add(k2)
                break
    if k not in used2:
        real_perp_basis.append(np.real(v))
        used2.add(k)

P_par_basis = np.array(real_par_basis).T   # 8 x 4
P_perp_basis = np.array(real_perp_basis).T  # 8 x 4

# Orthonormalize each basis
from numpy.linalg import qr
P_par_basis, _ = qr(P_par_basis, mode='reduced')   # 8x4 orthonormal
P_perp_basis, _ = qr(P_perp_basis, mode='reduced')

# Projection matrices (8x8)
P_par  = P_par_basis @ P_par_basis.T
P_perp = P_perp_basis @ P_perp_basis.T

# Project all 240 roots to 4D parallel space
roots_proj = roots_e8 @ P_par_basis  # 240 x 4

# Squared norms
sq_norms = np.sum(roots_proj**2, axis=1)

# Find distinct values
unique_norms = sorted(set(round(x, 6) for x in sq_norms))
print(f"\n  Distinct projected squared norms: {len(unique_norms)} values")
for un in unique_norms:
    count = sum(1 for x in sq_norms if abs(x - un) < 1e-4)
    # Express in terms of phi
    # Try: un = a + b*phi for rational a,b
    # phi = (1+sqrt(5))/2, so a + b*(1+sqrt(5))/2 = a + b/2 + b*sqrt(5)/2
    # un ≈ a + b/2 + b*0.5*2.236
    # Let's try sympy
    un_sym = nsimplify(un, [sp.GoldenRatio], rational=False, tolerance=1e-4)
    print(f"    ||P(r)||² = {un:.6f}  (count={count:3d})  = {un_sym}")

# Pairwise products for nearest neighbors
print("\n  Pairwise products of projected norms (nearest-neighbor roots):")
product_set = set()
for i in range(len(roots_e8)):
    for j in range(i+1, len(roots_e8)):
        # Check if <r_i, r_j> = 1 (nearest neighbor in root system)
        ip = np.dot(roots_e8[i], roots_e8[j])
        if abs(ip - 1.0) < 1e-6:
            prod = sq_norms[i] * sq_norms[j]
            product_set.add(round(prod, 6))

unique_products = sorted(product_set)
print(f"  Distinct pairwise products: {len(unique_products)}")
for up in unique_products[:20]:
    up_sym = nsimplify(up, [sp.GoldenRatio], rational=False, tolerance=1e-4)
    print(f"    {up:.6f}  = {up_sym}")

# phi-adic expansion of the projected norms
# Express norm values as polynomials in phi^{-1}
print("\n  phi-adic structure of projected norms:")
# phi^(-1) = phi - 1 = (sqrt(5)-1)/2
# Unique norm values in terms of phi:
phi_sym = sp.GoldenRatio
for un in unique_norms:
    un_sym = nsimplify(un, [sp.GoldenRatio], rational=False, tolerance=1e-4)
    # Try to expand as sum of phi^(-k) terms
    val = float(un_sym.subs(sp.GoldenRatio, phi_num))
    residual = val
    expansion = {}
    for k in range(-3, 20):
        coeff = round(residual * phi_num**k)
        if abs(coeff) > 0 and abs(coeff) <= 10:
            expansion[k] = coeff
            residual -= coeff * phi_inv**k
            if abs(residual) < 1e-8:
                break
    exp_str = " + ".join(f"{c}·φ^(-{k})" for k, c in sorted(expansion.items()))
    print(f"    {un:.6f} = {un_sym} ≈ {exp_str}")

# Approach 4 exponent generation via Z[phi] multiplication
print("\n  Z[φ] multiplication table for projected norm groups:")
# Each distinct norm = a + b·φ for integer a,b (or half-integer)
# Product of (a1+b1·φ)(a2+b2·φ) = a1a2 + (a1b2+a2b1)φ + b1b2·φ²
#                                 = a1a2+b1b2 + (a1b2+a2b1+b1b2)φ
# (using φ² = φ+1)

norm_phi_coeffs = []
for un in unique_norms:
    un_sym = nsimplify(un, [sp.GoldenRatio], rational=False, tolerance=1e-4)
    # Extract a, b where un_sym = a + b*GoldenRatio
    expanded = sp.expand(un_sym)
    a_coeff = expanded.subs(sp.GoldenRatio, 0)
    b_coeff = sp.simplify((expanded - a_coeff) / sp.GoldenRatio) if expanded != a_coeff else 0
    norm_phi_coeffs.append((float(a_coeff), float(b_coeff)))
    print(f"    {un:.6f} = {a_coeff} + {b_coeff}·φ")

# Generate all products up to order 4
from itertools import combinations_with_replacement

product_exponents = set()

def phi_power_decompose(val, max_k=40):
    """Find which phi^(-k) terms appear in a value."""
    exps = set()
    residual = val
    for k in range(0, max_k+1):
        pk = phi_inv**k
        if pk < 1e-15:
            break
        c = round(residual / pk)
        if abs(c) >= 1 and abs(c) <= 100:
            exps.add(k)
            residual -= c * pk
            if abs(residual) < 1e-8:
                break
    return exps

for order in range(1, 5):
    order_exps = set()
    for combo in combinations_with_replacement(range(len(unique_norms)), order):
        prod = 1.0
        for idx in combo:
            prod *= unique_norms[idx]
        exps = phi_power_decompose(prod)
        order_exps.update(exps)
        product_exponents.update(exps)
    print(f"  Order {order} products generate exponents: {sorted(order_exps & set(range(1,N_MAX+1)))}")

product_selected = product_exponents & set(range(1, N_MAX+1))
print(f"\n  All product exponents (orders 1-4): {sorted(product_selected)}")

# ─────────────────────────────────────────────────────────────────────
# APPROACH 5 — Combined Feynman Rules
# ─────────────────────────────────────────────────────────────────────
print("\n" + "=" * 72)
print("APPROACH 5: Combined Selection Function (Feynman Rules on E8/H4)")
print("=" * 72)

# Build individual signals for n = 1..N_MAX
signal_coxeter = np.zeros(N_MAX)
signal_molien  = np.zeros(N_MAX)
signal_theta   = np.zeros(N_MAX)
signal_product = np.zeros(N_MAX)

for n in range(1, N_MAX + 1):
    idx = n - 1
    # Coxeter: |Tr_par - Tr_perp|, normalized
    signal_coxeter[idx] = C_n[idx]
    # Molien: coefficient a_n
    signal_molien[idx] = molien_coeffs[n]
    # Theta: I(n) (information content)
    signal_theta[idx] = I_n[n] if n <= N_THETA else 0
    # Product: 1 if n in product exponents, 0 otherwise
    signal_product[idx] = 1.0 if n in product_selected else 0.0

# Normalize each signal to [0,1]
def norm01(x):
    mn, mx = x.min(), x.max()
    if mx - mn < 1e-15:
        return np.zeros_like(x)
    return (x - mn) / (mx - mn)

sc = norm01(signal_coxeter)
sm = norm01(signal_molien)
st = norm01(signal_theta)
sp_sig = signal_product  # already 0/1

# Combined: multiplicative where possible, additive as fallback
# g(n) = (1 + sc) * (1 + sm) * (1 + st) * (1 + sp) - 1  (so 0 when all zero)
combined = (1 + sc) * (1 + sm) * (1 + st) * (1 + sp_sig) - 1

print(f"  {'n':>3}  {'Coxeter':>8}  {'Molien':>8}  {'Theta':>8}  {'Product':>8}  {'Combined':>10}  {'GSM?':>5}")
print("  " + "-" * 60)
for n in range(1, N_MAX + 1):
    idx = n - 1
    gsm_flag = "***" if n in GSM_SET else ""
    if combined[idx] > 0.01 or n in GSM_SET:
        print(f"  {n:3d}  {sc[idx]:8.4f}  {sm[idx]:8.4f}  {st[idx]:8.4f}  {sp_sig[idx]:8.1f}  {combined[idx]:10.4f}  {gsm_flag:>5}")

# ── Combined plot ────────────────────────────────────────────────────
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
ns = np.arange(1, N_MAX + 1)

colors_gsm = ["red" if n in GSM_SET else "steelblue" for n in ns]

axes[0,0].bar(ns, sc, color=colors_gsm, alpha=0.7)
axes[0,0].set_title("Coxeter Selection C(n) [normalized]")
axes[0,0].set_xlabel("n")

axes[0,1].bar(ns, sm, color=colors_gsm, alpha=0.7)
axes[0,1].set_title("Molien Coefficients [normalized]")
axes[0,1].set_xlabel("n")

axes[1,0].bar(ns, st, color=colors_gsm, alpha=0.7)
axes[1,0].set_title("Theta Information I(n) [normalized]")
axes[1,0].set_xlabel("n")

axes[1,1].bar(ns, combined, color=colors_gsm, alpha=0.7)
axes[1,1].set_title("COMBINED Selection Function")
axes[1,1].set_xlabel("n")
# Mark GSM exponents
for g in GSM_EXPONENTS:
    if g <= N_MAX:
        axes[1,1].axvline(g, color="red", ls="--", alpha=0.3, lw=0.8)

fig.suptitle("E8/H4 Algebraic Selection Rules — All Four Approaches", fontsize=14)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "e8_combined_selection.png"), dpi=150)
plt.close(fig)
print(f"\n  → Saved e8_combined_selection.png")

# ─────────────────────────────────────────────────────────────────────
# STATISTICAL ANALYSIS
# ─────────────────────────────────────────────────────────────────────
print("\n" + "=" * 72)
print("STATISTICAL ANALYSIS")
print("=" * 72)

def hypergeom_pvalue(S, G, N=N_MAX):
    """P-value for overlap between S and G drawn from {1..N}."""
    overlap = len(S & G)
    # P(X >= overlap) where X ~ Hypergeometric(N, |G|, |S|)
    pval = hypergeom.sf(overlap - 1, N, len(G), len(S))
    return overlap, pval

approaches = {}

# 1. Coxeter
approaches["Coxeter (|diff|>0.5)"] = coxeter_selected & set(range(1, N_MAX+1))

# 2. Molien
approaches["Molien (a_n > 0)"] = molien_selected & set(range(1, N_MAX+1))

# 3. Theta (1% threshold)
approaches["Theta (I>1%)"] = theta_selected_1pct & set(range(1, N_MAX+1))
approaches["Theta (I>0.1%)"] = theta_selected_01pct & set(range(1, N_MAX+1))

# 4. Products
approaches["Products (order<=4)"] = product_selected

# 5. Combined — threshold at median
med = np.median(combined[combined > 0]) if np.any(combined > 0) else 0.1
combined_selected = set(n for n in range(1, N_MAX+1) if combined[n-1] > med)
approaches["Combined (>median)"] = combined_selected

# Also try: top-23 by combined score (same size as GSM set)
top23_idx = np.argsort(combined)[::-1][:23]
combined_top23 = set(n_range[i] for i in top23_idx)
approaches["Combined (top 23)"] = combined_top23

print(f"\nGSM exponents ({len(GSM_SET)} elements): {GSM_EXPONENTS}")
print(f"Universe: {{1, ..., {N_MAX}}}\n")

print(f"  {'Approach':<30}  {'|S|':>4}  {'|S∩G|':>6}  {'Cover':>7}  {'Precis':>7}  {'p-value':>12}")
print("  " + "-" * 75)

results_rows = []
for name, S in approaches.items():
    overlap, pval = hypergeom_pvalue(S, GSM_SET, N_MAX)
    coverage = overlap / len(GSM_SET) if len(GSM_SET) > 0 else 0
    precision = overlap / len(S) if len(S) > 0 else 0
    print(f"  {name:<30}  {len(S):4d}  {overlap:6d}  {coverage:7.1%}  {precision:7.1%}  {pval:12.2e}")
    missing = sorted(GSM_SET - S)
    extra = sorted(S - GSM_SET)
    if missing:
        print(f"    Missing GSM: {missing}")
    if extra and len(extra) <= 15:
        print(f"    Extra:       {extra}")
    results_rows.append({
        "approach": name, "S_size": len(S), "overlap": overlap,
        "coverage": f"{coverage:.3f}", "precision": f"{precision:.3f}",
        "p_value": f"{pval:.2e}",
        "selected": str(sorted(S)),
        "missing_gsm": str(missing),
        "extra": str(extra)
    })

# ─────────────────────────────────────────────────────────────────────
# Save CSV
# ─────────────────────────────────────────────────────────────────────
csv_path = os.path.join(OUT, "e8_algebraic_results.csv")
with open(csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=results_rows[0].keys())
    writer.writeheader()
    writer.writerows(results_rows)
print(f"\n  → Saved e8_algebraic_results.csv")

# ─────────────────────────────────────────────────────────────────────
# FINAL VERDICT
# ─────────────────────────────────────────────────────────────────────
print("\n" + "=" * 72)
print("FINAL VERDICT")
print("=" * 72)

print("""
Summary of the five algebraic approaches to deriving GSM exponents from E8:

APPROACH 1 (Coxeter Element):
  The Coxeter selection function C(n) = |Tr(w_par^n) - Tr(w_perp^n)| is
  periodic with period 30 (the Coxeter number). It peaks at specific n values
  determined by the Coxeter exponents mod 30. This provides a COARSE filter
  that selects roughly half the integers — necessary but far from sufficient.

APPROACH 2 (Molien Series):
  The quotient Molien series M_{E8/H4}(t) = 1/[(1-t^8)(1-t^14)(1-t^18)(1-t^24)]
  has nonzero coefficients at n = 0, 8, 14, 16, 18, 22, 24, 26, 28, 30, 32, ...
  These are the degrees at which NEW H4-breaking invariants appear. This is a
  strong structural signal: the "complementary degrees" {8,14,18,24} and their
  sums generate the allowed exponents. Coverage of GSM is PARTIAL — it captures
  the larger exponents well but misses many small ones.

APPROACH 3 (Theta Function):
  The E8 theta function at q=φ^{-1} is dominated by low-n terms (since φ^{-n}
  decays exponentially). The "information content" I(n) selects n=1,2,3,...
  monotonically — there is NO non-trivial selection mechanism here. The theta
  function at the specific point q=φ^{-1} does not distinguish GSM exponents
  from non-GSM exponents. This approach FAILS to provide selection rules.

APPROACH 4 (phi-adic Products):
  The projected root norms in Z[φ] generate specific exponents through
  multiplication. Products up to order 4 generate a LIMITED set of exponents.
  The coverage depends on how many distinct norm groups exist and how they
  combine. This approach provides ALGEBRAIC constraints from the ring structure
  of Z[φ], but the generated set tends to be either too small or too large.

APPROACH 5 (Combined):
  Combining all four signals multiplicatively gives a richer selection function.
  However, since Approach 3 is essentially monotone and Approach 4 is binary,
  the combined signal is dominated by Approaches 1 and 2.

HONEST ASSESSMENT:
  None of the five approaches, individually or combined, cleanly DERIVES the
  full set of 23 GSM exponents from E8 algebraic structure alone. The Coxeter
  and Molien approaches provide genuine structural constraints, but they are
  either too coarse (Coxeter: selects ~20 of 40) or too sparse (Molien: misses
  low exponents). The theta function provides no selection at all.

  The fundamental issue is: the GSM exponents {1,2,3,...,10,12,...,34} are
  ALMOST a complete set of small integers (with only a few gaps: 11,19,21,22,
  23,25,28,29,30,31,32,35,...). Deriving "most small integers" from E8 is not
  a strong constraint — any approach that selects "small numbers" will have
  high apparent coverage.

  The Molien series approach is the most STRUCTURALLY motivated: the
  complementary degrees {8,14,18,24} of E8 relative to H4 are the genuine
  algebraic signature of the E8→H4 symmetry breaking. But their power series
  expansion generates ALL sufficiently large integers eventually, so the
  selection is really about WHICH SMALL integers are missing.

  BOTTOM LINE: E8 algebraic structure provides necessary conditions (Coxeter
  periodicity, Molien degree constraints) but not sufficient conditions to
  uniquely determine the GSM exponents. The selection rules likely require
  ADDITIONAL physical input beyond pure E8/H4 representation theory.
""")
