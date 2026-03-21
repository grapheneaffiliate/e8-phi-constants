#!/usr/bin/env python3
"""
Automated Validation Pipeline for GSM Solver
=============================================
Compares all derived constants against experimental values.
Produces: summary table, aggregate statistics, CSV, deviation plot.
"""

import sys
import os
import csv
import numpy as np

# Add repo root to path so we can import gsm_solver
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, REPO_ROOT)

from gsm_solver import derive_all, EXPERIMENT

# ---------------------------------------------------------------------------
# Sector classification (mirrors gsm_solver.analyze sector_map)
# ---------------------------------------------------------------------------
SECTOR_MAP = {
    'alpha_inv': 'gauge', 'sin2_theta_w': 'gauge', 'alpha_s': 'gauge',
    'mu_e_ratio': 'lepton', 'tau_mu_ratio': 'lepton',
    'm_e_GeV': 'lepton', 'm_mu_GeV': 'lepton', 'm_tau_GeV': 'lepton',
    'ms_md_ratio': 'quark', 'mc_ms_ratio': 'quark', 'mb_mc_ratio': 'quark',
    'm_u_GeV': 'quark', 'm_d_GeV': 'quark', 'm_s_GeV': 'quark',
    'm_c_GeV': 'quark', 'm_b_GeV': 'quark',
    'mp_me_ratio': 'composite', 'n_p_mass_diff': 'composite',
    'r_p_fm': 'composite', 'mpi_me': 'composite', 'Bd_mp': 'composite',
    'Rydberg_eV': 'composite',
    'y_t': 'electroweak', 'mH_v': 'electroweak', 'mW_v': 'electroweak',
    'mt_v': 'electroweak', 'mZ_v': 'electroweak',
    'm_t_GeV': 'electroweak', 'm_W_GeV': 'electroweak',
    'm_Z_GeV': 'electroweak', 'm_H_GeV': 'electroweak',
    'mW_mZ': 'electroweak', 'G_F_GeV2': 'electroweak',
    'sin_theta_C': 'CKM', 'J_CKM': 'CKM', 'V_cb': 'CKM', 'V_ub': 'CKM',
    'theta_12': 'PMNS', 'theta_23': 'PMNS', 'theta_13': 'PMNS',
    'delta_CP': 'PMNS',
    'Sigma_m_nu': 'neutrino', 'dm21_sq': 'neutrino', 'dm32_sq': 'neutrino',
    'N_eff': 'neutrino',
    'Omega_Lambda': 'cosmology', 'z_CMB': 'cosmology', 'H0': 'cosmology',
    'n_s': 'cosmology', 'Omega_b': 'cosmology', 'Omega_DM': 'cosmology',
    'T_CMB': 'cosmology', 'eta_B': 'cosmology',
    'r_tensor': 'cosmology', 'sigma_8': 'cosmology',
    'M_Pl_v': 'hierarchy', 'v_GeV': 'hierarchy',
    'S_CHSH': 'prediction',
}


def classify(sigma_abs):
    """Classify by sigma tension."""
    if sigma_abs < 2.0:
        return "PASS"
    elif sigma_abs <= 3.0:
        return "WARN"
    else:
        return "FAIL"


def fmt_sci(x, sig=6):
    """Format a number in a readable way, choosing fixed or scientific."""
    ax = abs(x)
    if ax == 0:
        return "0"
    if 1e-3 <= ax < 1e6:
        return f"{x:.{sig}g}"
    return f"{x:.{sig-1}e}"


def main():
    # ------------------------------------------------------------------
    # 1. Derive all constants
    # ------------------------------------------------------------------
    derivations = derive_all()

    # ------------------------------------------------------------------
    # 2. Build comparison rows
    # ------------------------------------------------------------------
    rows = []  # (key, name, derived, experimental, unc, abs_dev, dev_ppm, sigma, tier, sector, status)

    for key, deriv in derivations.items():
        if key not in EXPERIMENT:
            continue
        exp = EXPERIMENT[key]
        d_val = deriv.value
        e_val = exp['value']
        unc = exp['unc']
        tier = exp['tier']
        name = exp['name']
        sector = SECTOR_MAP.get(key, 'other')

        abs_dev = abs(d_val - e_val)
        dev_ppm = abs_dev / abs(e_val) * 1e6 if e_val != 0 else float('inf')
        sigma = abs_dev / unc if unc > 0 else float('inf')
        status = classify(sigma)

        rows.append({
            'key': key,
            'name': name,
            'derived': d_val,
            'experimental': e_val,
            'unc': unc,
            'abs_dev': abs_dev,
            'dev_ppm': dev_ppm,
            'sigma': sigma,
            'tier': tier,
            'sector': sector,
            'status': status,
        })

    # Sort by sector then key for readability
    sector_order = ['gauge', 'lepton', 'quark', 'composite', 'electroweak',
                    'CKM', 'PMNS', 'neutrino', 'cosmology', 'hierarchy', 'prediction', 'other']
    sector_rank = {s: i for i, s in enumerate(sector_order)}
    rows.sort(key=lambda r: (sector_rank.get(r['sector'], 99), r['key']))

    # ------------------------------------------------------------------
    # 3. Print formatted summary table
    # ------------------------------------------------------------------
    hdr = f"{'Key':<18} {'Name':<38} {'Derived':>14} {'Experimental':>14} {'Dev_ppm':>10} {'Sigma':>8} {'Tier':>4} {'Status':>6}"
    sep = "-" * len(hdr)

    print("\n" + "=" * len(hdr))
    print("  GSM VALIDATION PIPELINE — FULL RESULTS")
    print("=" * len(hdr))
    print(hdr)
    print(sep)

    for r in rows:
        print(f"{r['key']:<18} {r['name']:<38} {fmt_sci(r['derived']):>14} {fmt_sci(r['experimental']):>14} "
              f"{r['dev_ppm']:>10.2f} {r['sigma']:>8.3f} {r['tier']:>4} {r['status']:>6}")

    print(sep)

    # ------------------------------------------------------------------
    # 4. Aggregate statistics
    # ------------------------------------------------------------------
    n_pass = sum(1 for r in rows if r['status'] == 'PASS')
    n_warn = sum(1 for r in rows if r['status'] == 'WARN')
    n_fail = sum(1 for r in rows if r['status'] == 'FAIL')
    n_total = len(rows)

    ppms = [r['dev_ppm'] for r in rows]
    median_ppm = np.median(ppms)
    mean_ppm = np.mean(ppms)

    sigmas = [r['sigma'] for r in rows]
    chi2 = sum(s ** 2 for s in sigmas)
    reduced_chi2 = chi2 / n_total if n_total > 0 else 0.0

    print(f"\n{'AGGREGATE STATISTICS':^{len(hdr)}}")
    print(sep)
    print(f"  Total constants validated : {n_total}")
    print(f"  PASS (< 2 sigma)          : {n_pass}")
    print(f"  WARN (2-3 sigma)          : {n_warn}")
    print(f"  FAIL (> 3 sigma)          : {n_fail}")
    print(f"  Pass rate                 : {100*n_pass/n_total:.1f}%")
    print(f"  Median deviation          : {median_ppm:.2f} ppm")
    print(f"  Mean deviation            : {mean_ppm:.2f} ppm")
    print(f"  Overall reduced chi^2     : {reduced_chi2:.4f}")

    # Sector-by-sector breakdown
    print(f"\n{'SECTOR BREAKDOWN':^{len(hdr)}}")
    print(sep)
    print(f"  {'Sector':<14} {'N':>3} {'Pass':>5} {'Warn':>5} {'Fail':>5} {'Med_ppm':>10} {'Mean_sig':>10}")
    print(f"  {'-'*14} {'---':>3} {'-----':>5} {'-----':>5} {'-----':>5} {'----------':>10} {'----------':>10}")

    for sec in sector_order:
        sec_rows = [r for r in rows if r['sector'] == sec]
        if not sec_rows:
            continue
        sn = len(sec_rows)
        sp = sum(1 for r in sec_rows if r['status'] == 'PASS')
        sw = sum(1 for r in sec_rows if r['status'] == 'WARN')
        sf = sum(1 for r in sec_rows if r['status'] == 'FAIL')
        smed = np.median([r['dev_ppm'] for r in sec_rows])
        smean_sig = np.mean([r['sigma'] for r in sec_rows])
        print(f"  {sec:<14} {sn:>3} {sp:>5} {sw:>5} {sf:>5} {smed:>10.2f} {smean_sig:>10.3f}")

    # ------------------------------------------------------------------
    # 5. Save CSV
    # ------------------------------------------------------------------
    csv_path = os.path.join(os.path.dirname(__file__), "validation_results.csv")
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            'key', 'name', 'derived', 'experimental', 'unc',
            'abs_dev', 'dev_ppm', 'sigma', 'tier', 'sector', 'status'])
        writer.writeheader()
        for r in rows:
            writer.writerow(r)
    print(f"\n  CSV saved to: {csv_path}")

    # ------------------------------------------------------------------
    # 6. Generate deviation plot
    # ------------------------------------------------------------------
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 12), gridspec_kw={'height_ratios': [2, 1]})

        # Top panel: sigma tension bar chart
        keys_plot = [r['key'] for r in rows]
        sigmas_plot = [r['sigma'] for r in rows]
        colors = []
        for r in rows:
            if r['status'] == 'PASS':
                colors.append('#2ecc71')
            elif r['status'] == 'WARN':
                colors.append('#f39c12')
            else:
                colors.append('#e74c3c')

        x_pos = np.arange(len(keys_plot))
        ax1.bar(x_pos, sigmas_plot, color=colors, edgecolor='black', linewidth=0.3)
        ax1.axhline(y=2.0, color='orange', linestyle='--', linewidth=1.2, label='2 sigma (WARN)')
        ax1.axhline(y=3.0, color='red', linestyle='--', linewidth=1.2, label='3 sigma (FAIL)')
        ax1.set_xticks(x_pos)
        ax1.set_xticklabels(keys_plot, rotation=90, fontsize=6)
        ax1.set_ylabel('Sigma tension |derived - exp| / unc')
        ax1.set_title(f'GSM Validation: {n_total} Constants  |  PASS={n_pass}  WARN={n_warn}  FAIL={n_fail}  |  Reduced chi^2={reduced_chi2:.4f}')
        ax1.legend(loc='upper right')
        ax1.set_xlim(-0.5, len(keys_plot) - 0.5)

        # Bottom panel: deviation in ppm (log scale)
        ax2.bar(x_pos, ppms, color=colors, edgecolor='black', linewidth=0.3)
        ax2.set_yscale('log')
        ax2.set_xticks(x_pos)
        ax2.set_xticklabels(keys_plot, rotation=90, fontsize=6)
        ax2.set_ylabel('Deviation (ppm, log scale)')
        ax2.set_xlabel('Constant')
        ax2.axhline(y=100, color='gray', linestyle=':', linewidth=0.8, label='100 ppm')
        ax2.axhline(y=10000, color='gray', linestyle=':', linewidth=0.8, label='10000 ppm (1%)')
        ax2.legend(loc='upper right', fontsize=8)
        ax2.set_xlim(-0.5, len(keys_plot) - 0.5)

        plt.tight_layout()
        plot_path = os.path.join(os.path.dirname(__file__), "validation_deviations.png")
        fig.savefig(plot_path, dpi=150)
        plt.close(fig)
        print(f"  Plot saved to: {plot_path}")

    except ImportError:
        print("  [WARN] matplotlib not available -- skipping plot generation.")

    print("\n  Pipeline complete.\n")


if __name__ == "__main__":
    main()
