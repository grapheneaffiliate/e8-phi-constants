#!/usr/bin/env python3
"""
Hierarchy Uniqueness Proof — Shows that exponent 80 = 2(h + rank + 2) is the
unique integer exponent giving M_Pl/v within 1% of experiment.

The hierarchy formula is:
    M_Pl / v = phi^(exponent - eps - sub_torsion)

where:
    phi = (1+sqrt(5))/2
    eps = 28/248 = dim(SO(8))/dim(E8)
    sub_torsion = (24/248) * phi^(-12)   [sub-leading torsion from C_4 Casimir]

We scan exponent = 2(30 + 8 + k) for k in {-5, ..., 15} and show that only
k = 2 (exponent = 80) reproduces the experimental ratio to within 1%.

Usage:
    py proofs/hierarchy_uniqueness.py
"""

import math

# ─── Constants ───
phi = (1 + math.sqrt(5)) / 2
h = 30            # E8 Coxeter number
rank = 8          # E8 rank
eps = 28 / 248    # dim(SO(8)) / dim(E8), primary torsion correction
M_Pl = 1.22089e19   # Planck mass in GeV
v_exp = 246.22       # Electroweak VEV in GeV (experimental)

ratio_exp = M_Pl / v_exp  # Experimental M_Pl / v

# Sub-leading torsion from the degree-12 Casimir (C_4)
sub_torsion = (24 / 248) * phi**(-12)

# ─── Scan ───
print("=" * 78)
print("Hierarchy Uniqueness: scanning exponent = 2(h + rank + k) = 2(30 + 8 + k)")
print(f"  phi = {phi:.10f}")
print(f"  eps = 28/248 = {eps:.6f}")
print(f"  sub_torsion = (24/248)*phi^(-12) = {sub_torsion:.6e}")
print(f"  M_Pl = {M_Pl:.5e} GeV")
print(f"  v_exp = {v_exp} GeV")
print(f"  (M_Pl/v)_exp = {ratio_exp:.6e}")
print("=" * 78)
print()
print(f"{'k':>4s}  {'exponent':>8s}  {'eff_exp':>12s}  {'phi^eff':>14s}  "
      f"{'v_pred (GeV)':>14s}  {'dev (%)':>10s}  {'<1%?':>5s}")
print("-" * 78)

unique_count = 0
unique_k = None

for k in range(-5, 16):
    exponent = 2 * (h + rank + k)
    eff_exp = exponent - eps - sub_torsion
    ratio_pred = phi ** eff_exp
    v_pred = M_Pl / ratio_pred
    deviation = abs(ratio_pred - ratio_exp) / ratio_exp * 100

    within = deviation < 1.0
    if within:
        unique_count += 1
        unique_k = k
        marker = " <=="
    else:
        marker = ""

    print(f"{k:4d}  {exponent:8d}  {eff_exp:12.6f}  {ratio_pred:14.6e}  "
          f"{v_pred:14.4f}  {deviation:10.4f}  {'YES' if within else 'no':>5s}{marker}")

print("-" * 78)
print()

# ─── Verdict ───
if unique_count == 1:
    exp_unique = 2 * (h + rank + unique_k)
    print(f"RESULT: Exactly 1 exponent within 1% of experiment.")
    print(f"  k = {unique_k}  =>  exponent = 2({h}+{rank}+{unique_k}) = {exp_unique}")
    print(f"  This is 2(h + rank + c_1) = 2(30 + 8 + 2) = 80.")
    print()
    eff = exp_unique - eps - sub_torsion
    ratio = phi ** eff
    v = M_Pl / ratio
    dev = abs(ratio - ratio_exp) / ratio_exp * 100
    print(f"  phi^({exp_unique} - eps - sub_torsion) = phi^{eff:.6f} = {ratio:.6e}")
    print(f"  v_predicted = {M_Pl:.5e} / {ratio:.6e} = {v:.4f} GeV")
    print(f"  v_experiment = {v_exp} GeV")
    print(f"  deviation = {dev:.4f}%")
    print()
    print("UNIQUENESS PROVEN: exponent 80 is the unique member of the family")
    print("  2(h + rank + k) that reproduces M_Pl/v within 1%.")
else:
    print(f"WARNING: {unique_count} exponents found within 1% (expected exactly 1).")
    print("Uniqueness NOT established at the 1% level.")

print()
print("=" * 78)
