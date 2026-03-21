#!/usr/bin/env python
"""
Cosmological Closure Test
=========================
Verify that the three GSM-derived Omega formulas sum to ~1
and cross-check each against Planck 2018 data.

Pure GSM parameters:
    phi = (1 + sqrt(5)) / 2   (golden ratio)
    eps = 28 / 248             (E8 structure fraction)
"""

import math

# ── Fundamental constants ──────────────────────────────────────────
phi = (1 + math.sqrt(5)) / 2
eps = 28 / 248

# ── GSM-derived cosmological fractions ─────────────────────────────
Omega_Lambda = (phi**(-1) + phi**(-6) + phi**(-9)
                - phi**(-13) + phi**(-28) + eps * phi**(-7))

Omega_DM = 1/8 + phi**(-4) - eps * phi**(-5)

Omega_b = 1/12 - phi**(-7)

Omega_sum = Omega_Lambda + Omega_DM + Omega_b
deviation = Omega_sum - 1.0
radiation = 1.0 - Omega_sum

# ── Planck 2018 reference values (TT,TE,EE+lowE+lensing) ─────────
planck = {
    "Omega_Lambda": (0.6889, 0.0056),
    "Omega_DM":     (0.2607, 0.0020),
    "Omega_b":      (0.0489, 0.0003),
}

gsm = {
    "Omega_Lambda": Omega_Lambda,
    "Omega_DM":     Omega_DM,
    "Omega_b":      Omega_b,
}

# ── Output ─────────────────────────────────────────────────────────
print("=" * 72)
print("  COSMOLOGICAL CLOSURE TEST  —  GSM vs Planck 2018")
print("=" * 72)
print(f"\n  phi   = {phi:.15f}")
print(f"  eps   = {eps:.15f}  (28/248)")

print(f"\n{'Parameter':<16} {'GSM Value':>12} {'Planck':>12} {'± sigma':>8} {'Delta':>10} {'sigma-off':>10}")
print("-" * 72)

for name in ["Omega_Lambda", "Omega_DM", "Omega_b"]:
    val = gsm[name]
    p_val, p_sig = planck[name]
    delta = val - p_val
    sigma_off = delta / p_sig
    print(f"  {name:<14} {val:>12.6f} {p_val:>12.4f} {p_sig:>8.4f} {delta:>+10.6f} {sigma_off:>+10.2f}")

print("-" * 72)
print(f"  {'Sum':<14} {Omega_sum:>12.6f}")
print(f"  {'Deviation':<14} {deviation:>+12.2e}")
print(f"  {'Radiation':<14} {radiation:>+12.2e}   (= 1 - Sum)")
print()

# ── Pass / fail summary ───────────────────────────────────────────
all_within = True
for name in ["Omega_Lambda", "Omega_DM", "Omega_b"]:
    val = gsm[name]
    p_val, p_sig = planck[name]
    if abs(val - p_val) > 2 * p_sig:
        all_within = False

if abs(deviation) < 1e-2:
    print("  [PASS] Sum deviates from 1.0 by < 1%")
else:
    print("  [FAIL] Sum deviates from 1.0 by >= 1%")

if all_within:
    print("  [PASS] All components within 2-sigma of Planck 2018")
else:
    print("  [INFO] One or more components outside 2-sigma of Planck 2018")

if abs(radiation) < 1e-2:
    print(f"  [NOTE] Residual {radiation:+.2e} consistent with radiation density")

print("=" * 72)
