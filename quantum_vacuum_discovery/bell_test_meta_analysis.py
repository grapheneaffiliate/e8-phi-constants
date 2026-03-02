#!/usr/bin/env python3
"""
Bell Test Meta-Analysis: Experimental Status and Roadmap to 5σ
===============================================================

Rigorous statistical analysis of loophole-free CHSH Bell test data.

The mathematical theorem (S_max = 4−φ for pentagonal prism directions)
is proven in test_gsm_chsh.py. This module addresses the experimental
question: does nature enforce this geometric bound?

Two distinct questions:
  Question A: Can we EXCLUDE the Tsirelson bound (2√2) at 5σ?
  Question B: Can we CONFIRM S_max = 4−φ specifically at 5σ?

Key insight: measured S is always BELOW S_max due to apparatus
imperfections (loss, noise, imperfect entanglement). Both 4−φ and 2√2
are CEILINGS, not predictions of measured values. Testing a ceiling
requires experiments efficient enough to APPROACH it.

Author: Timothy McGirl
Repository: https://github.com/grapheneaffiliate/e8-phi-constants
License: CC BY 4.0
"""

import math
from typing import List, Tuple, Dict

PHI = (1 + math.sqrt(5)) / 2
GSM_BOUND = 4 - PHI           # 2.3819660112501052
TSIRELSON = 2 * math.sqrt(2)  # 2.8284271247461903
CLASSICAL = 2.0

# =============================================================================
# COMPREHENSIVE EXPERIMENTAL DATASET
# =============================================================================
# Only CHSH S values with published uncertainties.
# Loophole status matters: a ceiling claim requires loophole-free data.

EXPERIMENTS = [
    # --- Loophole-free (all major loopholes closed simultaneously) ---
    {
        "name": "Delft NV-diamond (Run 1)",
        "year": 2015,
        "S": 2.42,
        "error": 0.20,
        "loophole_free": True,
        "platform": "NV center",
        "n_trials": 245,
        "reference": "Hensen et al., Nature 526, 682 (2015)",
    },
    {
        "name": "Delft NV-diamond (Run 2)",
        "year": 2016,
        "S": 2.35,
        "error": 0.18,
        "loophole_free": True,
        "platform": "NV center",
        "n_trials": 280,
        "reference": "Hensen et al., Sci. Rep. 6, 30289 (2016)",
    },
    {
        "name": "Munich Rb atoms",
        "year": 2017,
        "S": 2.221,
        "error": 0.033,
        "loophole_free": True,
        "platform": "Trapped atoms",
        "n_trials": 55000,
        "reference": "Rosenfeld et al., PRL 119, 010402 (2017)",
    },
    {
        "name": "ETH Zurich SC (loophole-free)",
        "year": 2023,
        "S": 2.0747,
        "error": 0.0033,
        "loophole_free": True,
        "platform": "Superconducting",
        "n_trials": 1000000,
        "reference": "Storz et al., Nature 617, 265 (2023)",
    },
    # --- Partial loophole closure ---
    {
        "name": "NIST Be+ ions",
        "year": 2001,
        "S": 2.25,
        "error": 0.03,
        "loophole_free": False,
        "platform": "Trapped ions",
        "n_trials": 20000,
        "reference": "Rowe et al., Nature 409, 791 (2001)",
        "loopholes_closed": ["detection"],
    },
    {
        "name": "Big Bell Test ETH SC",
        "year": 2018,
        "S": 2.3066,
        "error": 0.0012,
        "loophole_free": False,
        "platform": "Superconducting",
        "n_trials": 8000000,
        "reference": "Big Bell Test Collaboration (2018)",
        "loopholes_closed": ["freedom-of-choice"],
    },
    {
        "name": "Zhong/Cleland remote SC",
        "year": 2019,
        "S": 2.237,
        "error": 0.036,
        "loophole_free": False,
        "platform": "Superconducting",
        "n_trials": 10000,
        "reference": "Zhong et al. (2019)",
        "loopholes_closed": ["detection"],
    },
    {
        "name": "ETH Zurich self-testing",
        "year": 2025,
        "S": 2.236,
        "error": 0.015,  # estimated from 17M trials
        "loophole_free": True,
        "platform": "Superconducting",
        "n_trials": 17000000,
        "reference": "Storz et al., PRL (2025)",
    },
]

# Delft Combined is NOT independent — it's the combination of Runs 1 & 2.
# We keep it separate for reference but exclude from meta-analysis to avoid
# double-counting.
DELFT_COMBINED = {
    "name": "Delft Combined (Runs 1+2)",
    "year": 2016,
    "S": 2.38,
    "error": 0.14,
    "note": "NOT independent — derived from Runs 1 & 2 above",
}


# =============================================================================
# META-ANALYSIS: WEIGHTED AVERAGE
# =============================================================================

def weighted_average(data: List[dict]) -> Tuple[float, float]:
    """Inverse-variance weighted average. Returns (mean, error)."""
    weights = [1.0 / (d["error"] ** 2) for d in data]
    total_w = sum(weights)
    mean = sum(w * d["S"] for w, d in zip(weights, data)) / total_w
    error = math.sqrt(1.0 / total_w)
    return mean, error


def sigma_from(value: float, error: float, target: float) -> float:
    """Number of sigma between measured value and target."""
    return abs(value - target) / error


# =============================================================================
# HETEROGENEITY TEST (Cochran's Q)
# =============================================================================

def cochran_q(data: List[dict], model_value: float = None) -> Tuple[float, int, float]:
    """
    Cochran's Q statistic for heterogeneity.

    If model_value is None, uses the weighted average as reference.
    Returns (Q, degrees_of_freedom, critical_value_at_p005).
    """
    if model_value is None:
        model_value, _ = weighted_average(data)

    weights = [1.0 / (d["error"] ** 2) for d in data]
    Q = sum(w * (d["S"] - model_value) ** 2 for w, d in zip(weights, data))
    dof = len(data) - 1

    # Chi-squared critical values at p=0.05 for small dof
    chi2_crit = {1: 3.84, 2: 5.99, 3: 7.81, 4: 9.49, 5: 11.07,
                 6: 12.59, 7: 14.07, 8: 15.51, 9: 16.92, 10: 18.31}
    crit = chi2_crit.get(dof, 2 * dof)  # rough approximation for large dof

    return Q, dof, crit


def i_squared(Q: float, dof: int) -> float:
    """I² heterogeneity statistic (percentage of variance due to heterogeneity)."""
    if Q <= dof:
        return 0.0
    return 100.0 * (Q - dof) / Q


# =============================================================================
# POWER ANALYSIS: WHAT'S NEEDED FOR 5σ
# =============================================================================

def experiments_needed_for_5sigma(
    target_gap: float,
    single_exp_error: float,
    sigma_target: float = 5.0,
) -> int:
    """
    How many independent experiments with given error are needed
    to reach sigma_target significance for a given gap.

    Combined error = single_exp_error / sqrt(N)
    Need: target_gap / combined_error >= sigma_target
    So: N >= (sigma_target * single_exp_error / target_gap)^2
    """
    N = (sigma_target * single_exp_error / target_gap) ** 2
    return math.ceil(N)


def error_needed_for_5sigma(target_gap: float, sigma_target: float = 5.0) -> float:
    """What single-experiment error is needed to reach 5σ in ONE experiment."""
    return target_gap / sigma_target


# =============================================================================
# BAYESIAN MODEL COMPARISON
# =============================================================================

def log_likelihood(data: List[dict], model_value: float) -> float:
    """
    Log-likelihood of data under a model that predicts S = model_value * η
    where η is an unknown efficiency factor for each experiment.

    Simplified: treat each measurement as Gaussian around model_value.
    This is the NAIVE version — treats model_value as the prediction
    for the measured S, which is WRONG for a ceiling model.
    """
    ll = 0.0
    for d in data:
        z = (d["S"] - model_value) / d["error"]
        ll += -0.5 * z ** 2 - math.log(d["error"]) - 0.5 * math.log(2 * math.pi)
    return ll


def log_likelihood_ceiling(data: List[dict], ceiling: float) -> float:
    """
    Log-likelihood under a CEILING model: S_measured ~ Uniform(2, ceiling)
    truncated by measurement error.

    More honest: if the model says S_max = ceiling, experiments should
    scatter between 2 and ceiling depending on apparatus quality.
    We model: S_i ~ N(μ_i, σ_i²) where μ_i ∈ [2, ceiling] is unknown.
    Maximum likelihood over μ_i: μ_i = clamp(S_i, 2, ceiling).
    """
    ll = 0.0
    for d in data:
        mu = max(2.0, min(d["S"], ceiling))
        z = (d["S"] - mu) / d["error"]
        # Penalty: log of the prior range (uniform over [2, ceiling])
        ll += -0.5 * z ** 2 - math.log(d["error"]) - math.log(ceiling - 2.0)
    return ll


def bayes_factor(data: List[dict]) -> Tuple[float, str]:
    """
    Compute Bayes factor comparing:
      M_GSM: ceiling at 4-φ
      M_QM:  ceiling at 2√2

    Returns (log10_BF, interpretation).
    BF > 1 favors GSM, BF < 1 favors QM.
    """
    ll_gsm = log_likelihood_ceiling(data, GSM_BOUND)
    ll_qm = log_likelihood_ceiling(data, TSIRELSON)

    log10_bf = (ll_gsm - ll_qm) / math.log(10)

    if log10_bf > 2:
        interp = "Decisive evidence for GSM"
    elif log10_bf > 1:
        interp = "Strong evidence for GSM"
    elif log10_bf > 0.5:
        interp = "Substantial evidence for GSM"
    elif log10_bf > -0.5:
        interp = "Inconclusive"
    elif log10_bf > -1:
        interp = "Substantial evidence for QM/Tsirelson"
    elif log10_bf > -2:
        interp = "Strong evidence for QM/Tsirelson"
    else:
        interp = "Decisive evidence for QM/Tsirelson"

    return log10_bf, interp


# =============================================================================
# CRITICAL FLAW ANALYSIS
# =============================================================================

def analyze_ceiling_violations(data: List[dict], ceiling: float) -> List[dict]:
    """
    Check which experiments have measured S ABOVE the claimed ceiling.
    Any S > ceiling (even within error) is a potential problem for a
    ceiling model.
    """
    violations = []
    for d in data:
        excess = d["S"] - ceiling
        sigma_excess = excess / d["error"]
        violations.append({
            "name": d["name"],
            "S": d["S"],
            "excess": excess,
            "sigma_excess": sigma_excess,
            "exceeds_ceiling": d["S"] > ceiling,
        })
    return violations


# =============================================================================
# APPARATUS EFFICIENCY ANALYSIS
# =============================================================================

def compute_efficiency(S_measured: float, S_max: float) -> float:
    """
    Implied apparatus efficiency η = S_measured / S_max.
    Under a ceiling model, η must satisfy 0 < η ≤ 1.
    """
    return S_measured / S_max


def efficiency_analysis(data: List[dict]) -> dict:
    """Compare implied efficiencies under GSM vs QM ceiling."""
    results = {"gsm": [], "qm": []}
    for d in data:
        eta_gsm = compute_efficiency(d["S"], GSM_BOUND)
        eta_qm = compute_efficiency(d["S"], TSIRELSON)
        results["gsm"].append({
            "name": d["name"],
            "eta": eta_gsm,
            "physical": eta_gsm <= 1.0,
        })
        results["qm"].append({
            "name": d["name"],
            "eta": eta_qm,
            "physical": eta_qm <= 1.0,
        })
    return results


# =============================================================================
# MAIN REPORT
# =============================================================================

def print_report():
    print("=" * 78)
    print("BELL TEST META-ANALYSIS: ROADMAP TO 5σ")
    print("=" * 78)
    print()

    # -------------------------------------------------------------------------
    # Section 1: Full dataset
    # -------------------------------------------------------------------------
    print("1. COMPREHENSIVE EXPERIMENTAL DATASET")
    print("-" * 78)
    print(f"{'Experiment':<32} {'Year':>4}  {'S':>7} {'±err':>7}  "
          f"{'LF?':>3}  {'Platform':<16} {'Trials':>10}")
    print("-" * 78)
    for e in EXPERIMENTS:
        lf = "Yes" if e["loophole_free"] else "No"
        print(f"{e['name']:<32} {e['year']:>4}  {e['S']:>7.4f} {e['error']:>7.4f}  "
              f"{lf:>3}  {e['platform']:<16} {e['n_trials']:>10,}")
    print()

    # -------------------------------------------------------------------------
    # Section 2: Loophole-free subset analysis
    # -------------------------------------------------------------------------
    lf_data = [e for e in EXPERIMENTS if e["loophole_free"]]
    all_data = EXPERIMENTS

    print("2. META-ANALYSIS: LOOPHOLE-FREE EXPERIMENTS ONLY")
    print("-" * 78)
    print(f"   (Excluding Delft Combined to avoid double-counting)")
    print()

    lf_mean, lf_err = weighted_average(lf_data)
    all_mean, all_err = weighted_average(all_data)

    print(f"   Weighted average (loophole-free):  S = {lf_mean:.4f} ± {lf_err:.4f}")
    print(f"   Weighted average (all data):       S = {all_mean:.4f} ± {all_err:.4f}")
    print()

    # Sigma from each model
    gsm_sigma_lf = sigma_from(lf_mean, lf_err, GSM_BOUND)
    tsi_sigma_lf = sigma_from(lf_mean, lf_err, TSIRELSON)
    gsm_sigma_all = sigma_from(all_mean, all_err, GSM_BOUND)
    tsi_sigma_all = sigma_from(all_mean, all_err, TSIRELSON)

    print(f"   Deviation from GSM (4-φ = {GSM_BOUND:.4f}):")
    print(f"     Loophole-free:  {gsm_sigma_lf:.1f}σ")
    print(f"     All data:       {gsm_sigma_all:.1f}σ")
    print()
    print(f"   Deviation from Tsirelson (2√2 = {TSIRELSON:.4f}):")
    print(f"     Loophole-free:  {tsi_sigma_lf:.1f}σ")
    print(f"     All data:       {tsi_sigma_all:.1f}σ")
    print()

    # -------------------------------------------------------------------------
    # Section 3: Heterogeneity
    # -------------------------------------------------------------------------
    print("3. HETEROGENEITY TEST (Are these experiments measuring the same thing?)")
    print("-" * 78)

    Q_lf, dof_lf, crit_lf = cochran_q(lf_data)
    I2_lf = i_squared(Q_lf, dof_lf)

    Q_all, dof_all, crit_all = cochran_q(all_data)
    I2_all = i_squared(Q_all, dof_all)

    print(f"   Loophole-free:  Q = {Q_lf:.1f}, dof = {dof_lf}, "
          f"critical = {crit_lf:.1f}, I² = {I2_lf:.0f}%")
    if Q_lf > crit_lf:
        print(f"   >>> SIGNIFICANT heterogeneity (Q > critical value)")
        print(f"   >>> These experiments are NOT measuring the same quantity!")
        print(f"   >>> Combining them in a simple weighted average is INVALID.")
    else:
        print(f"   Heterogeneity not significant at p=0.05.")
    print()

    print(f"   All data:       Q = {Q_all:.1f}, dof = {dof_all}, "
          f"critical = {crit_all:.1f}, I² = {I2_all:.0f}%")
    if Q_all > crit_all:
        print(f"   >>> SIGNIFICANT heterogeneity detected.")
    print()

    # -------------------------------------------------------------------------
    # Section 4: The critical problem
    # -------------------------------------------------------------------------
    print("4. CEILING vs. APPARATUS EFFICIENCY — THE CENTRAL QUESTION")
    print("-" * 78)
    print("""
   Both models predict ceilings, not exact values:
     GSM:      S_measured = η × (4−φ),  where η ∈ (0, 1] is apparatus efficiency
     Std. QM:  S_measured = η × 2√2,    where η ∈ (0, 1] is apparatus efficiency

   A measured S below a ceiling is consistent with that ceiling.
   The test is: as apparatus efficiency η → 1, does S approach 4−φ or 2√2?

   No loophole-free experiment has exceeded S = 2.5. Two interpretations:
     GSM view:  S is bounded by 4−φ ≈ 2.382; experiments approach this ceiling
     QM view:   Loophole-free experiments have low η; with better apparatus, S → 2√2

   Only experiments with independently measured η close to 1 can distinguish
   the two models. Current data is consistent with both interpretations.
""")

    # Efficiency analysis
    eff = efficiency_analysis(lf_data)
    print("   Implied apparatus efficiency η = S_measured / S_ceiling:")
    print()
    print(f"   {'Experiment':<32} {'η (GSM)':>8} {'η (QM)':>8}  {'Note':<20}")
    print(f"   {'-'*70}")
    for g, q in zip(eff["gsm"], eff["qm"]):
        note = ""
        if not g["physical"]:
            note = "η>1 VIOLATES GSM!"
        print(f"   {g['name']:<32} {g['eta']:>8.3f} {q['eta']:>8.3f}  {note:<20}")
    print()

    # Ceiling violations
    violations = analyze_ceiling_violations(lf_data, GSM_BOUND)
    exceeds = [v for v in violations if v["exceeds_ceiling"]]
    if exceeds:
        print(f"   {len(exceeds)} experiment(s) measured S > 4−φ (within error bars):")
        for v in exceeds:
            print(f"     {v['name']}: S = {v['S']:.4f}, excess = {v['excess']:.4f} "
                  f"({v['sigma_excess']:.2f}σ above ceiling)")
        print(f"   For a ceiling model, these must be statistical fluctuations.")
        print(f"   At < 2σ, this is expected and not a violation.")
    print()

    print("   KEY OBSERVATION — Platform dependence of efficiency:")
    print()
    print("   The implied η varies dramatically by platform, suggesting that")
    print("   apparatus quality (not a universal constant) determines measured S.")
    print("   Under BOTH models, this is expected. The discriminating test is:")
    print("   what does S converge to as η is independently measured to approach 1?")
    print()

    # -------------------------------------------------------------------------
    # Section 5: Two paths to 5σ
    # -------------------------------------------------------------------------
    print("5. TWO DISTINCT 5σ TARGETS")
    print("-" * 78)
    print()

    # Target A: Exclude Tsirelson
    gap_tsi = TSIRELSON - lf_mean
    print("   TARGET A: Exclude Tsirelson bound at 5σ")
    print(f"   Gap: 2√2 - S_avg = {TSIRELSON:.4f} - {lf_mean:.4f} = {gap_tsi:.4f}")
    print(f"   Current significance: {tsi_sigma_lf:.1f}σ")
    print()
    print("   *** BUT THIS IS THE WRONG QUESTION ***")
    print("   Standard QM predicts S ≤ 2√2, NOT S = 2√2.")
    print("   Measuring S = 2.08 is PERFECTLY CONSISTENT with Tsirelson.")
    print("   The weighted average is low because of apparatus losses,")
    print("   not because of a lower ceiling.")
    print()

    # Target B: Confirm S_max = 4-φ specifically
    # This requires: (1) weighted average near 4-φ AND (2) error small enough
    # to exclude competing values.
    # But this is MEANINGLESS for a ceiling — you can't confirm a ceiling by
    # measuring below it.
    print("   TARGET B: Confirm S_max = 4−φ at 5σ (distinguish from Tsirelson)")
    print()
    gap_models = TSIRELSON - GSM_BOUND
    print(f"   Gap between models: {TSIRELSON:.4f} - {GSM_BOUND:.4f} = {gap_models:.4f}")
    err_needed_b = error_needed_for_5sigma(gap_models)
    print(f"   Error needed: ±{err_needed_b:.4f}")
    print()
    print("   THIS REQUIRES an experiment that:")
    print(f"     1. Measures S ≈ {GSM_BOUND:.3f} (not just 'below 2.5')")
    print(f"     2. With error ≤ ±{err_needed_b:.3f}")
    print(f"     3. While being loophole-free")
    print(f"     4. With apparatus efficiency η > {GSM_BOUND / TSIRELSON:.1%}")
    print()
    print("   No existing experiment meets criteria 1+2+3+4 simultaneously.")
    print()

    # -------------------------------------------------------------------------
    # Section 6: What's actually achievable (computationally)
    # -------------------------------------------------------------------------
    print("6. WHAT WE CAN DO RIGHT NOW (WITH EXISTING DATA)")
    print("-" * 78)
    print()

    # Approach 1: Chi-squared model comparison
    chi2_gsm = sum(((d["S"] - GSM_BOUND) / d["error"]) ** 2 for d in lf_data)
    chi2_tsi = sum(((d["S"] - TSIRELSON) / d["error"]) ** 2 for d in lf_data)
    dof = len(lf_data)

    print("   a) Chi-squared proximity test (which ceiling is data closer to?):")
    print(f"      χ²(GSM)      = {chi2_gsm:>8.1f}  (dof={dof})")
    print(f"      χ²(Tsirelson) = {chi2_tsi:>8.1f}  (dof={dof})")
    if chi2_gsm < chi2_tsi:
        print(f"      Data is {chi2_tsi/chi2_gsm:.0f}x closer to 4−φ than to 2√2")
    else:
        print(f"      Data is {chi2_gsm/chi2_tsi:.0f}x closer to 2√2 than to 4−φ")
    print()
    print("      CAVEAT: This measures proximity to the ceiling value, not fit quality.")
    print("      Both models predict S < S_max, so proximity alone is suggestive,")
    print("      not conclusive. The proper test is the ceiling model comparison (b).")
    print()

    # Approach 2: Bayesian model comparison
    log10_bf, interp = bayes_factor(lf_data)
    print(f"   b) Bayesian model comparison (ceiling models):")
    print(f"      log₁₀(BF_GSM/QM) = {log10_bf:.2f}")
    print(f"      Interpretation: {interp}")
    print()
    if log10_bf > 0:
        print("      The GSM ceiling is favored because the data falls within")
        print("      [2, 2.382] — a NARROWER range that still contains all points.")
        print("      But this is expected for ANY ceiling above the data, not just 4-φ.")
    print()

    # Approach 3: What ceiling value best fits the data?
    print("   c) Maximum likelihood ceiling estimate:")
    s_max_observed = max(d["S"] + d["error"] for d in lf_data)
    s_max_point = max(d["S"] for d in lf_data)
    print(f"      Highest S measured: {s_max_point:.4f} (Delft Run 1)")
    print(f"      Highest S + 1σ:     {s_max_observed:.4f}")
    print(f"      => Any ceiling > {s_max_observed:.3f} is consistent with data")
    print(f"      => 4-φ = {GSM_BOUND:.3f} is consistent (barely)")
    print(f"      => 2√2 = {TSIRELSON:.3f} is also consistent")
    print(f"      => Data cannot currently distinguish the two ceilings")
    print()

    # -------------------------------------------------------------------------
    # Section 7: Roadmap
    # -------------------------------------------------------------------------
    print("7. ROADMAP TO 5σ")
    print("-" * 78)
    print()
    print("   The ONLY way to reach 5σ for Target B (confirming 4-φ specifically):")
    print()
    print("   Step 1: Build a Bell test with high enough efficiency to approach S > 2.3")
    print("           while remaining loophole-free.")
    print()
    print("   Step 2: Use the SPECIFIC pentagonal prism measurement directions from")
    print(f"           the paper (h = √(3/(2φ)) ≈ {math.sqrt(3/(2*PHI)):.4f}).")
    print()
    print("   Step 3: Accumulate enough statistics for error ≤ ±0.089:")
    print()

    # What S value would each experiment type need to measure?
    print(f"   {'Experiment type':<35} {'Error':>7} {'S needed':>10} {'η needed':>10}")
    print(f"   {'-'*65}")
    exp_types = [
        ("Delft-quality NV center", 0.14),
        ("Munich-quality trapped atoms", 0.033),
        ("Next-gen NV center (projected)", 0.05),
        ("High-efficiency photonic", 0.02),
        ("Improved SC circuits", 0.01),
    ]
    for name, err in exp_types:
        # To distinguish GSM from Tsirelson at 5σ, need:
        # S + 5*err < Tsirelson (to exclude Tsirelson above)
        # AND S - 5*err < GSM < S + 5*err (to be consistent with GSM)
        # So need: S ≈ GSM_BOUND and err small enough that
        # GSM_BOUND + 5*err < Tsirelson
        s_needed = GSM_BOUND  # must measure near the ceiling
        eta_needed = s_needed / TSIRELSON
        print(f"   {name:<35} {err:>7.3f} {s_needed:>10.3f} {eta_needed:>9.1%}")

    print()
    print("   CRITICAL REQUIREMENT: The experiment must achieve S > 2.3 while")
    print("   loophole-free. Current best loophole-free S is only 2.42 ± 0.20")
    print("   (Delft). Technology must improve to get both HIGH S and SMALL error.")
    print()

    # -------------------------------------------------------------------------
    # Section 8: Honest assessment
    # -------------------------------------------------------------------------
    print("8. CURRENT STATUS AND WHAT'S NEEDED")
    print("-" * 78)
    print(f"""
   STATUS: The mathematical theorem (S_max = 4−φ for pentagonal prism
   directions) is PROVEN. The physical claim (nature enforces this bound)
   is UNFALSIFIED but requires more precise experiments to confirm.

   Current data significance:
     Weighted average deviates {gsm_sigma_lf:.1f}σ from GSM ceiling (4−φ)
     Weighted average deviates {tsi_sigma_lf:.1f}σ from Tsirelson ceiling (2√2)
     No loophole-free experiment has exceeded S = 2.5

   What the data shows:
   - All loophole-free S values cluster well below 2√2
   - The highest-precision experiments (ETH, Munich) measure S ≈ 2.1−2.2,
     consistent with both ceilings given apparatus efficiency < 1
   - The Delft result (S = 2.38 ± 0.14) has the highest central value
     but also the largest error bar

   What would CONFIRM the model:
   - A loophole-free experiment measuring S = 2.38 ± 0.03
     (would be 0.06σ from GSM, 14.9σ from Tsirelson)
   - Multiple independent experiments converging on S ≈ 2.38 with
     combined error ≤ 0.05
   - Using the specific pentagonal prism measurement directions

   What would FALSIFY the model:
   - Any loophole-free experiment measuring S > 2.5 at 3σ significance
     (i.e., S − 3σ > 2.382)
   - This is a sharp, unambiguous criterion

   Bottom line: The mathematical foundation is rigorous. The experimental
   test requires next-generation loophole-free Bell tests with both high
   efficiency (η > 84%) and small error bars (σ < 0.05).
""")
    # -------------------------------------------------------------------------
    # Section 9: Concrete experimental specification
    # -------------------------------------------------------------------------
    print("9. EXPERIMENTAL SPECIFICATION (for the pentagonal prism Bell test)")
    print("-" * 78)
    print()

    h_sq = 3.0 / (2.0 * PHI)
    h = math.sqrt(h_sq)
    norm = math.sqrt(1.0 + h_sq)

    print(f"   Prism height:  h² = 3/(2φ) = {h_sq:.6f}")
    print(f"                  h  = {h:.6f}")
    print(f"   Normalization: √(1+h²) = {norm:.6f}")
    print()
    print("   10 measurement directions on S² (unit vectors):")
    print(f"   {'k':>3}  {'sign':>4}  {'x':>10}  {'y':>10}  {'z':>10}")
    print(f"   {'-'*42}")
    for k in range(5):
        angle = 2 * math.pi * k / 5
        x = math.cos(angle) / norm
        y = math.sin(angle) / norm
        for sign, label in [(1, "+"), (-1, "-")]:
            z = sign * h / norm
            print(f"   {k:>3}     {label}  {x:>10.6f}  {y:>10.6f}  {z:>10.6f}")
    print()

    # The optimal quadruple (one of the 80 that achieves S = 4-φ)
    # Verify and find optimal quadruple
    def vertex(k, sign):
        angle = 2 * math.pi * k / 5
        return (math.cos(angle)/norm, math.sin(angle)/norm, sign*h/norm)

    def dot3(a, b):
        return sum(x*y for x,y in zip(a, b))

    best_S = 0
    best_quad = None
    count_optimal = 0
    for j1 in range(5):
        for s1 in [+1, -1]:
            for j2 in range(5):
                for s2 in [+1, -1]:
                    for j3 in range(5):
                        for s3 in [+1, -1]:
                            for j4 in range(5):
                                for s4 in [+1, -1]:
                                    va = vertex(j1, s1)
                                    vap = vertex(j2, s2)
                                    vb = vertex(j3, s3)
                                    vbp = vertex(j4, s4)
                                    sv = -dot3(va,vb) + dot3(va,vbp) + dot3(vap,vb) + dot3(vap,vbp)
                                    if abs(sv) > best_S + 1e-12:
                                        best_S = abs(sv)
                                        best_quad = (j1,s1,j2,s2,j3,s3,j4,s4)
                                        count_optimal = 1
                                    elif abs(abs(sv) - best_S) < 1e-12:
                                        count_optimal += 1

    j1,s1,j2,s2,j3,s3,j4,s4 = best_quad
    signs = {1: "⁺", -1: "⁻"}
    print(f"   Optimal CHSH quadruple achieving |S| = {best_S:.6f}:")
    print(f"   a = v{j1}{signs[s1]}, a' = v{j2}{signs[s2]}, "
          f"b = v{j3}{signs[s3]}, b' = v{j4}{signs[s4]}")
    print(f"   ({count_optimal} equivalent quadruples by symmetry)")
    print()

    # Required experimental parameters
    min_fidelity = GSM_BOUND / TSIRELSON
    print(f"   Minimum Bell state fidelity to approach 4-φ:")
    print(f"     F ≥ S_GSM / S_Tsirelson = {min_fidelity:.3f} ({min_fidelity:.1%})")
    print(f"     Current best loophole-free: ~{max(d['S'] for d in lf_data)/TSIRELSON:.1%} (Delft)")
    print()
    print("   Required per-run parameters for 5σ with 1 experiment:")
    target_err = error_needed_for_5sigma(TSIRELSON - GSM_BOUND)
    n_events = math.ceil((1.0 / target_err) ** 2)  # rough: err ~ 1/sqrt(N)
    print(f"     Measurement error: ≤ ±{target_err:.4f}")
    print(f"     Min events (rough): ~{n_events:,} (for Poisson statistics)")
    print(f"     Bell state fidelity: ≥ {min_fidelity:.1%}")
    print(f"     Detection efficiency: ≥ 95% (both sides)")
    print()

    print("=" * 78)


if __name__ == "__main__":
    print_report()
