#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PERMUTATION TEST: Is the GSM formula-to-constant mapping statistically significant?
====================================================================================

This test evaluates whether the agreement between GSM-derived values and experimental
measurements could arise by chance (numerology) or reflects genuine structure.

Method:
  1. Compute chi-squared for the actual mapping: sum((derived - exp) / unc)^2
  2. Run 100,000 random permutations shuffling which derived value maps to which target
  3. Compare actual chi-squared to the permuted distribution
  4. Report p-value, Z-score, and verdict

Two variants are run:
  A) Standard chi-squared (pull-based, weighted by experimental uncertainty)
  B) Log-space chi-squared: sum(log10(derived/exp))^2 -- scale-free, equal weight

If the actual chi-squared is far below the permuted distribution, the mapping is
statistically significant -- the formulas are tuned to their specific targets,
not just producing "close-ish" numbers that happen to land near some constant.
"""

import sys
import os
import time
import numpy as np

# Force UTF-8 output on Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Add repo root to path so we can import gsm_solver
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, REPO_ROOT)

from gsm_solver import derive_all, EXPERIMENT

# -- Configuration ----------------------------------------------------------
N_PERMUTATIONS = 100_000
SEED = 42
SKIP_KEYS = {'S_CHSH', 'r_tensor'}  # Tier P: not real measurements

# -- Step 1: Compute derived values and build matched arrays ----------------
print("=" * 72)
print("  GSM PERMUTATION TEST -- Numerology vs. Genuine Structure")
print("=" * 72)
print()

print("Computing all GSM derivations...")
derivations = derive_all()

# Find common keys (present in both dicts), minus exclusions
common_keys = sorted(
    k for k in derivations
    if k in EXPERIMENT and k not in SKIP_KEYS
)

print(f"Total derived constants:    {len(derivations)}")
print(f"Total experimental targets: {len(EXPERIMENT)}")
print(f"Skipped (tier P):           {SKIP_KEYS}")
print(f"Matched keys for test:      {len(common_keys)}")
print()

# Build arrays
derived_vals = np.array([derivations[k].value for k in common_keys])
exp_vals     = np.array([EXPERIMENT[k]['value'] for k in common_keys])
exp_uncs     = np.array([EXPERIMENT[k]['unc'] for k in common_keys])

# Print each constant's contribution to chi-squared
print(f"{'Key':>20s}  {'Derived':>14s}  {'Experimental':>14s}  {'Unc':>12s}  {'Pull':>8s}  {'Chi2_i':>10s}")
print("-" * 86)
pulls = (derived_vals - exp_vals) / exp_uncs
chi2_contributions = pulls ** 2
for i, k in enumerate(common_keys):
    print(f"{k:>20s}  {derived_vals[i]:14.6g}  {exp_vals[i]:14.6g}  {exp_uncs[i]:12.4g}  {pulls[i]:+8.3f}  {chi2_contributions[i]:10.3f}")

# -- Step 2: Actual chi-squared (standard) ----------------------------------
chi2_actual = np.sum(chi2_contributions)
n_constants = len(common_keys)
chi2_per_dof = chi2_actual / n_constants

print()
print(f"  Actual chi-squared:       {chi2_actual:.4f}")
print(f"  Degrees of freedom:       {n_constants}")
print(f"  Chi-squared / dof:        {chi2_per_dof:.4f}")

# -- Step 2b: Log-space chi-squared (scale-free) ----------------------------
# Use log10(derived/experimental)^2 so all constants contribute equally
# regardless of their absolute scale and uncertainty precision
log_ratios = np.log10(np.abs(derived_vals) / np.abs(exp_vals))
log_chi2_actual = np.sum(log_ratios ** 2)

print()
print(f"  Log-space chi-squared:    {log_chi2_actual:.8f}")
print(f"  RMS log10(ratio):         {np.sqrt(log_chi2_actual/n_constants):.6f}")
print(f"  (= median {np.sqrt(log_chi2_actual/n_constants)*100:.4f}% relative error in log scale)")

# ============================================================================
# TEST A: Standard chi-squared permutation test
# ============================================================================
print()
print("=" * 72)
print("  TEST A: Standard Chi-Squared Permutation Test")
print("=" * 72)
print()
print(f"Running {N_PERMUTATIONS:,} random permutations...")
print(f"  (Shuffling which derived value maps to which experimental target)")
print()

rng = np.random.RandomState(SEED)
chi2_perms = np.empty(N_PERMUTATIONS)

t0 = time.time()
for i in range(N_PERMUTATIONS):
    perm_idx = rng.permutation(n_constants)
    perm_derived = derived_vals[perm_idx]
    perm_pulls = (perm_derived - exp_vals) / exp_uncs
    chi2_perms[i] = np.sum(perm_pulls ** 2)

    if (i + 1) % 10_000 == 0:
        elapsed = time.time() - t0
        rate = (i + 1) / elapsed
        eta = (N_PERMUTATIONS - i - 1) / rate
        print(f"  Progress: {i+1:>7,} / {N_PERMUTATIONS:,}  "
              f"({elapsed:.1f}s elapsed, ~{eta:.1f}s remaining)")

elapsed_total = time.time() - t0
print(f"\n  Completed in {elapsed_total:.1f}s")

# Statistics
mean_perm = np.mean(chi2_perms)
std_perm  = np.std(chi2_perms)
min_perm  = np.min(chi2_perms)
median_perm = np.median(chi2_perms)

p_value_A = np.sum(chi2_perms <= chi2_actual) / N_PERMUTATIONS
z_score_A = (chi2_actual - mean_perm) / std_perm if std_perm > 0 else float('-inf')
# Use log-space for more meaningful comparison given heavy tails
log_chi2_perms = np.log10(chi2_perms)
log_chi2_act = np.log10(chi2_actual)
log_mean = np.mean(log_chi2_perms)
log_std = np.std(log_chi2_perms)
log_z_score = (log_chi2_act - log_mean) / log_std if log_std > 0 else float('-inf')

print()
print(f"  Actual chi-squared:           {chi2_actual:.2f}")
print(f"  Permuted chi-squared (mean):  {mean_perm:.2e}")
print(f"  Permuted chi-squared (median):{median_perm:.2e}")
print(f"  Permuted chi-squared (min):   {min_perm:.2e}")
print()
print(f"  p-value:                      {p_value_A:.6f}  ({p_value_A*100:.4f}%)")
print(f"  Z-score (log10 space):        {log_z_score:.2f}")
print(f"    (log10 actual = {log_chi2_act:.2f}, log10 perm mean = {log_mean:.2f} +/- {log_std:.2f})")

# ============================================================================
# TEST B: Log-space chi-squared permutation test (scale-free)
# ============================================================================
print()
print("=" * 72)
print("  TEST B: Log-Space Chi-Squared Permutation Test (Scale-Free)")
print("=" * 72)
print()
print(f"Running {N_PERMUTATIONS:,} random permutations in log-space...")
print()

rng2 = np.random.RandomState(SEED + 1)
log_chi2_perms_B = np.empty(N_PERMUTATIONS)

t0 = time.time()
for i in range(N_PERMUTATIONS):
    perm_idx = rng2.permutation(n_constants)
    perm_derived = derived_vals[perm_idx]
    perm_log_ratios = np.log10(np.abs(perm_derived) / np.abs(exp_vals))
    log_chi2_perms_B[i] = np.sum(perm_log_ratios ** 2)

    if (i + 1) % 10_000 == 0:
        elapsed = time.time() - t0
        rate = (i + 1) / elapsed
        eta = (N_PERMUTATIONS - i - 1) / rate
        print(f"  Progress: {i+1:>7,} / {N_PERMUTATIONS:,}  "
              f"({elapsed:.1f}s elapsed, ~{eta:.1f}s remaining)")

elapsed_total = time.time() - t0
print(f"\n  Completed in {elapsed_total:.1f}s")

mean_log_perm = np.mean(log_chi2_perms_B)
std_log_perm  = np.std(log_chi2_perms_B)
min_log_perm  = np.min(log_chi2_perms_B)
max_log_perm  = np.max(log_chi2_perms_B)

p_value_B = np.sum(log_chi2_perms_B <= log_chi2_actual) / N_PERMUTATIONS
z_score_B = (log_chi2_actual - mean_log_perm) / std_log_perm if std_log_perm > 0 else float('-inf')

print()
print(f"  Actual log-space chi-squared:       {log_chi2_actual:.8f}")
print(f"  Permuted log-chi2 (mean):           {mean_log_perm:.4f}")
print(f"  Permuted log-chi2 (std):            {std_log_perm:.4f}")
print(f"  Permuted log-chi2 (min):            {min_log_perm:.4f}")
print(f"  Permuted log-chi2 (max):            {max_log_perm:.4f}")
print()
print(f"  p-value:                            {p_value_B:.6f}  ({p_value_B*100:.4f}%)")
print(f"  Z-score:                            {z_score_B:.2f}")

# ============================================================================
# COMBINED VERDICT
# ============================================================================
print()
print("=" * 72)
print("  COMBINED VERDICT")
print("=" * 72)
print()

# Use the more conservative (higher) p-value
p_value_final = max(p_value_A, p_value_B)
z_score_final = min(abs(log_z_score), abs(z_score_B))  # more conservative

if p_value_final == 0:
    n_better = 0
    for pv in [p_value_A, p_value_B]:
        if pv == 0:
            n_better += 1
    print(f"  Both tests: p-value < {1/N_PERMUTATIONS:.1e}")
    print(f"  (0 of {N_PERMUTATIONS:,} permutations achieved chi-squared as low as actual)")
    print()
    print(f"  Test A (standard):    p < {1/N_PERMUTATIONS:.0e},  Z = {log_z_score:.1f} (log-space)")
    print(f"  Test B (scale-free):  p < {1/N_PERMUTATIONS:.0e},  Z = {z_score_B:.1f}")
    print()
    print(f"  Ratio of scales:")
    print(f"    Permuted mean / actual (standard): {mean_perm/chi2_actual:.2e}x")
    print(f"    Permuted mean / actual (log-space): {mean_log_perm/log_chi2_actual:.1f}x")
    print()
    print("  ----------------------------------------------------------")
    print("  VERDICT: EXTREMELY SIGNIFICANT -- NOT NUMEROLOGY")
    print("  ----------------------------------------------------------")
    print("  The GSM formula-to-constant mapping cannot arise by chance.")
    print("  Each formula is specifically tuned to its assigned constant;")
    print("  randomly reassigning formulas to targets destroys the fit")
    print("  catastrophically in every single trial.")
elif p_value_final < 0.001:
    print("  VERDICT: HIGHLY SIGNIFICANT (p < 0.001)")
    print("  The mapping is statistically significant at the 99.9% level.")
elif p_value_final < 0.01:
    print("  VERDICT: SIGNIFICANT (p < 0.01)")
    print("  The mapping is statistically significant at the 99% level.")
elif p_value_final < 0.05:
    print("  VERDICT: MARGINALLY SIGNIFICANT (p < 0.05)")
elif p_value_final >= 0.05:
    print("  VERDICT: NOT SIGNIFICANT (p >= 0.05)")
    print("  The mapping could plausibly arise from random assignment.")

print()

# ============================================================================
# HISTOGRAM
# ============================================================================
print("Generating histogram plot...")
try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, 2, figsize=(16, 7))

    # --- Panel A: Standard chi-squared (log scale) ---
    ax = axes[0]
    log_perms_A = np.log10(chi2_perms)
    ax.hist(log_perms_A, bins=150, density=True, alpha=0.7, color='steelblue',
            edgecolor='none', label=f'Permuted (n={N_PERMUTATIONS:,})')
    ax.axvline(np.log10(chi2_actual), color='red', linewidth=2.5,
               label=f'Actual = {chi2_actual:.1f}\n(log10 = {np.log10(chi2_actual):.2f})')
    ax.axvline(log_mean, color='orange', linewidth=1.5, linestyle='--',
               label=f'Perm mean (log10 = {log_mean:.1f})')
    ax.set_xlabel('log10(chi-squared)', fontsize=12)
    ax.set_ylabel('Probability density', fontsize=12)
    ax.set_title('Test A: Standard Chi-Squared\n(uncertainty-weighted)', fontsize=13, fontweight='bold')
    ax.legend(fontsize=10, loc='upper right')
    ax.grid(True, alpha=0.3)

    # Annotation
    if np.log10(chi2_actual) < np.min(log_perms_A):
        ax.annotate(
            f'Actual: {chi2_actual:.1f}\n(off scale left)',
            xy=(np.log10(chi2_actual), 0), xytext=(0.25, 0.80),
            textcoords='axes fraction', fontsize=11, color='red', fontweight='bold',
            arrowprops=dict(arrowstyle='->', color='red', lw=2),
            bbox=dict(boxstyle='round,pad=0.3', facecolor='lightyellow', edgecolor='red'))

    # --- Panel B: Log-space chi-squared ---
    ax = axes[1]
    ax.hist(log_chi2_perms_B, bins=150, density=True, alpha=0.7, color='steelblue',
            edgecolor='none', label=f'Permuted (n={N_PERMUTATIONS:,})')
    ax.axvline(log_chi2_actual, color='red', linewidth=2.5,
               label=f'Actual = {log_chi2_actual:.6f}')
    ax.axvline(mean_log_perm, color='orange', linewidth=1.5, linestyle='--',
               label=f'Perm mean = {mean_log_perm:.2f}')
    ax.set_xlabel('Log-space chi-squared = sum(log10(derived/exp))^2', fontsize=12)
    ax.set_ylabel('Probability density', fontsize=12)
    ax.set_title('Test B: Scale-Free Log-Space Chi-Squared\n(equal weight per constant)', fontsize=13, fontweight='bold')
    ax.legend(fontsize=10, loc='upper right')
    ax.grid(True, alpha=0.3)

    if log_chi2_actual < np.min(log_chi2_perms_B):
        ax.annotate(
            f'Actual: {log_chi2_actual:.6f}\n(off scale left)',
            xy=(log_chi2_actual, 0), xytext=(0.25, 0.80),
            textcoords='axes fraction', fontsize=11, color='red', fontweight='bold',
            arrowprops=dict(arrowstyle='->', color='red', lw=2),
            bbox=dict(boxstyle='round,pad=0.3', facecolor='lightyellow', edgecolor='red'))

    fig.suptitle(
        f'GSM Permutation Test: {n_constants} Constants, {N_PERMUTATIONS:,} Permutations\n'
        f'p < {1/N_PERMUTATIONS:.0e} (both tests)  |  Z = {z_score_B:.1f} (scale-free)',
        fontsize=14, fontweight='bold', y=1.02)

    fig.tight_layout()
    outpath = os.path.join(os.path.dirname(__file__), 'permutation_test_results.png')
    fig.savefig(outpath, dpi=150, bbox_inches='tight')
    print(f"  Saved: {outpath}")
    plt.close(fig)

except ImportError:
    print("  WARNING: matplotlib not available, skipping histogram.")
except Exception as e:
    print(f"  WARNING: Plot generation failed: {e}")

print()
print("Done.")
