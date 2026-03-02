#!/usr/bin/env python3
"""
Multi-Party Bell Inequality Bounds — GSM Predictions
=====================================================

STATUS:
  [PROVEN]      n=2 (CHSH): The pentagonal prism theorem establishes
                S_max = 4−φ for measurement directions drawn from an
                H4-geometric prism. See test_gsm_chsh.py for three
                algebraic proofs and brute-force verification.

  [CONJECTURED] n≥3: If H4 geometry constrains 2-party correlations,
                the suppression should propagate through the tensor
                product structure of multi-party Bell operators.
                The conjectured n-party suppression factor is:

                    η(n) = [(4−φ)/(2√2)]^(n/2)

                Each n-party prediction is independently falsifiable.

Author: Timothy McGirl
Repository: https://github.com/grapheneaffiliate/e8-phi-constants
License: CC BY 4.0
"""

import math
from typing import List, Dict
from dataclasses import dataclass


# =============================================================================
# FUNDAMENTAL CONSTANTS
# =============================================================================

PHI = (1 + math.sqrt(5)) / 2    # Golden ratio
GSM_BOUND = 4 - PHI              # 2-party CHSH bound (proven)
TSIRELSON = 2 * math.sqrt(2)     # Standard QM Tsirelson bound
GSM_SUPPRESSION = GSM_BOUND / TSIRELSON  # ≈ 0.8422


# =============================================================================
# STANDARD QM BOUNDS (established theory)
# =============================================================================

def standard_qm_bound(n: int) -> float:
    """
    Standard QM maximum for n-party MABK Bell inequality.

    n=2 (CHSH): 2√2 ≈ 2.828
    n≥3 (MABK): 2^(n/2)

    Reference: Mermin, PRL 65, 1838 (1990).
    """
    if n < 2:
        raise ValueError("Need at least 2 parties")
    if n == 2:
        return TSIRELSON
    return 2 ** (n / 2)


def classical_bound(n: int) -> float:
    """
    Classical (local hidden variable) bound for n-party Bell inequality.

    n=2 (CHSH): 2
    n≥3 (MABK): 2^((n-1)/2)

    Reference: Clauser et al., PRL 23, 880 (1969).
    """
    if n == 2:
        return 2.0
    return 2 ** ((n - 1) / 2)


# =============================================================================
# GSM BOUNDS
# =============================================================================
#
# STATUS KEY:
#   [P] PROVEN       — mathematical theorem (test_gsm_chsh.py)
#   [C] CONJECTURED  — extension requiring experimental confirmation
#

def gsm_suppression_factor(n: int) -> float:
    """
    GSM suppression factor η(n) for n-party inequalities.

    The 2-party suppression ratio (4−φ)/(2√2) ≈ 0.8422 is the ratio
    of the proven pentagonal prism bound to the Tsirelson bound.

    For n ≥ 3 parties, the CONJECTURE is that this suppression
    compounds through the recursive Mermin operator structure:

        η(n) = [(4−φ)/(2√2)]^(n/2)

    Physical reasoning: The n-party Mermin operator is built from
    pairwise correlations. Each pair contributes one factor of the
    base suppression. The exponent n/2 counts the number of
    independent pair correlations in the tensor product structure.

    STATUS:
        n=2: η = 0.8422 [PROVEN — pentagonal prism theorem]
        n≥3: η(n) = 0.8422^(n/2) [CONJECTURED]
    """
    return GSM_SUPPRESSION ** (n / 2)


def gsm_bound(n: int) -> float:
    """
    GSM maximum for n-party Bell inequality.

    n=2: 4 − φ ≈ 2.382 [PROVEN]
    n≥3: standard_qm_bound(n) × η(n) [CONJECTURED]
    """
    if n == 2:
        return GSM_BOUND  # Exact, proven
    return standard_qm_bound(n) * gsm_suppression_factor(n)


def gsm_svetlichny_bound(n: int) -> float:
    """
    GSM bound for Svetlichny inequality (genuine n-party nonlocality).

    Standard QM max = 2^((n+1)/2) for GHZ states.
    GSM applies the same geometric suppression.

    STATUS: CONJECTURED for all n ≥ 3.
    """
    if n < 3:
        raise ValueError("Svetlichny inequality requires n ≥ 3")
    qm_bound = 2 ** ((n + 1) / 2)
    return qm_bound * gsm_suppression_factor(n)


# =============================================================================
# BOUNDS TABLE
# =============================================================================

@dataclass
class BellBounds:
    """Container for n-party Bell inequality bounds."""
    n: int
    classical: float
    qm: float
    gsm: float
    suppression_pct: float
    status: str  # "PROVEN" or "CONJECTURED"


def compute_bounds_table(max_n: int = 10) -> List[BellBounds]:
    """Compute bounds for all party numbers from 2 to max_n."""
    results = []
    for n in range(2, max_n + 1):
        cl = classical_bound(n)
        qm = standard_qm_bound(n)
        gsm = gsm_bound(n)
        supp = (1 - gsm / qm) * 100
        status = "PROVEN" if n == 2 else "CONJECTURED"
        results.append(BellBounds(n, cl, qm, gsm, supp, status))
    return results


# =============================================================================
# CONSISTENCY CHECKS
# =============================================================================

def verify_bounds_ordering() -> List[Dict]:
    """
    Verify that for all n: classical < GSM < QM.

    This must hold for the framework to be internally consistent.
    A GSM bound below the classical limit would be unphysical — it
    would mean local hidden variable theories violate the bound.

    NOTE: The simple extrapolation η(n) = base^(n/2) breaks down at
    large n because the suppression compounds faster than the classical
    bound grows. This indicates the multi-party formula needs
    refinement for n ≥ 5, and marks the boundary of the conjecture's
    validity.
    """
    results = []
    for n in range(2, 11):
        cl = classical_bound(n)
        gsm = gsm_bound(n)
        qm = standard_qm_bound(n)
        results.append({
            "n": n,
            "classical": cl,
            "gsm": gsm,
            "qm": qm,
            "ordering_valid": cl < gsm < qm,
        })
    return results


def verify_suppression_increases() -> List[Dict]:
    """
    Verify that suppression percentage increases with n.

    The geometric constraints should become MORE restrictive as
    more parties are added, since each pair of parties contributes
    additional suppression.
    """
    bounds = compute_bounds_table(10)
    results = []
    for i in range(len(bounds) - 1):
        results.append({
            "n": bounds[i].n,
            "n_next": bounds[i + 1].n,
            "suppression": bounds[i].suppression_pct,
            "suppression_next": bounds[i + 1].suppression_pct,
            "increases": bounds[i + 1].suppression_pct > bounds[i].suppression_pct,
        })
    return results


# =============================================================================
# FALSIFICATION CRITERIA
# =============================================================================

def falsification_criteria() -> Dict[int, Dict]:
    """
    For each n, specify what loophole-free measurement would falsify
    the GSM prediction.

    A single loophole-free violation at ANY n would falsify the
    corresponding GSM bound. This is what makes the predictions
    scientifically meaningful — they are precise and refutable.

    We use a 3σ threshold: the measurement must exceed the GSM
    bound by at least 3 standard deviations to count as falsification.
    """
    criteria = {}
    for n in range(2, 9):
        gsm = gsm_bound(n)
        qm = standard_qm_bound(n)
        gap = qm - gsm
        criteria[n] = {
            "gsm_bound": gsm,
            "qm_bound": qm,
            "gap": gap,
            "gap_pct": gap / qm * 100,
            "falsified_if": f"loophole-free measurement exceeds {gsm:.4f} at 3σ",
            "status": "PROVEN" if n == 2 else "CONJECTURED",
        }
    return criteria


# =============================================================================
# REPORT
# =============================================================================

def print_report():
    """Print multi-party bounds analysis."""

    print("=" * 72)
    print("MULTI-PARTY BELL INEQUALITY BOUNDS — GSM PREDICTIONS")
    print("=" * 72)
    print()
    print("  STATUS KEY:")
    print("    [P] PROVEN      — pentagonal prism theorem (test_gsm_chsh.py)")
    print("    [C] CONJECTURED — extension requiring experimental test")
    print()

    # Bounds table
    print("─" * 72)
    print("n-PARTY BOUNDS TABLE")
    print("─" * 72)
    print(f"  {'n':<3} {'Status':<5} {'Classical':>10} {'QM Max':>10} "
          f"{'GSM Max':>10} {'Suppression':>12}")
    print(f"  {'─' * 55}")

    for b in compute_bounds_table(8):
        tag = "[P]" if b.status == "PROVEN" else "[C]"
        note = ""
        if b.gsm <= b.classical:
            note = " ** below classical — formula needs refinement"
        print(f"  {b.n:<3} {tag:<5} {b.classical:>10.4f} {b.qm:>10.4f} "
              f"{b.gsm:>10.4f} {b.suppression_pct:>11.1f}%{note}")
    print()

    # Suppression formula
    print("─" * 72)
    print("SUPPRESSION FORMULA")
    print("─" * 72)
    print(f"  Base ratio: (4−φ)/(2√2) = {GSM_SUPPRESSION:.10f}")
    print(f"  n-party: η(n) = {GSM_SUPPRESSION:.4f}^(n/2)")
    print()
    print("  n=2 (CHSH):    η = 0.842 → S_max = 4−φ ≈ 2.382     [PROVEN]")
    print(f"  n=3 (Mermin):  η = {gsm_suppression_factor(3):.3f} → "
          f"M₃ ≈ {gsm_bound(3):.3f}     [CONJECTURED]")
    print(f"  n=4 (Mermin):  η = {gsm_suppression_factor(4):.3f} → "
          f"M₄ ≈ {gsm_bound(4):.3f}     [CONJECTURED]")
    print()

    # Svetlichny bounds
    print("─" * 72)
    print("SVETLICHNY BOUNDS (genuine multipartite nonlocality)")
    print("─" * 72)
    for n in range(3, 7):
        qm_sv = 2 ** ((n + 1) / 2)
        gsm_sv = gsm_svetlichny_bound(n)
        print(f"  n={n}: QM = {qm_sv:.4f}, GSM = {gsm_sv:.4f} "
              f"({(1 - gsm_sv / qm_sv) * 100:.1f}% suppression)  [CONJECTURED]")
    print()

    # Consistency checks
    print("─" * 72)
    print("INTERNAL CONSISTENCY CHECKS")
    print("─" * 72)

    ordering = verify_bounds_ordering()
    valid_n = [r["n"] for r in ordering if r["ordering_valid"]]
    invalid_n = [r["n"] for r in ordering if not r["ordering_valid"]]
    print(f"  Ordering (classical < GSM < QM):")
    print(f"    Valid for n = {valid_n}")
    if invalid_n:
        print(f"    FAILS for n = {invalid_n}")
        print(f"    At these n, the simple suppression formula compounds")
        print(f"    faster than the classical bound grows. This marks the")
        print(f"    boundary where the extrapolation needs refinement.")

    monotonic = verify_suppression_increases()
    all_increasing = all(r["increases"] for r in monotonic)
    print(f"  Suppression monotonically increasing:  "
          f"{'YES' if all_increasing else 'NO'}")
    print()

    # Falsification criteria
    print("─" * 72)
    print("FALSIFICATION CRITERIA")
    print("─" * 72)
    print()
    print("  Each prediction below is independently testable.")
    print("  A single loophole-free violation at ANY n falsifies that bound.")
    print()

    for n, crit in falsification_criteria().items():
        tag = "[P]" if crit["status"] == "PROVEN" else "[C]"
        print(f"  n={n} {tag}: GSM bound = {crit['gsm_bound']:.4f}  "
              f"(gap to QM: {crit['gap']:.4f} = {crit['gap_pct']:.1f}%)")
        print(f"         Falsified if: {crit['falsified_if']}")
    print()

    # Derivation status
    print("─" * 72)
    print("STATUS OF THE MULTI-PARTY EXTENSION")
    print("─" * 72)
    print("""
  The n=2 (CHSH) bound S ≤ 4−φ is a mathematical theorem:
    - Three independent algebraic proofs from H4 Coxeter invariants
    - Brute-force verified over all 8,100 vertex quadruples
    - Zero free parameters

  The extension to n ≥ 3 is a CONJECTURE based on:
    - The recursive Mermin operator structure M_n = f(M_{n-1})
    - Each recursion step adding one pair-correlation factor
    - The pair suppression being the proven (4−φ)/(2√2)

  This conjecture is falsifiable: each n gives a specific numerical
  bound that can be tested independently. The suppression increases
  with n (reaching ~50% for n=8), which means higher-n tests are
  EASIER to distinguish from standard QM predictions.

  Experimental priority:
    1. n=2: Achieve loophole-free S > 2.38 with error < ±0.05
    2. n=3: First loophole-free 3-party Mermin test (compare to 2.186)
    3. n=4: First loophole-free 4-party test (29% suppression gap)
""")

    print("=" * 72)


if __name__ == "__main__":
    print_report()
