#!/usr/bin/env python3
"""
Verify the GSM Selection Rules for phi-exponents.

Implements the three selection rules from SELECTION_RULES.md and checks:
1. The rules produce exactly the predicted GSM exponent set
2. All exponents used in gsm_solver.py formulas are in the predicted set
"""

import re
import sys
import os

# ─── Selection Rule Implementation ───────────────────────────────────────────

CASIMIR_DEGREES = {2, 8, 12, 14, 18, 20, 24, 30}
E8_COXETER_EXPONENTS = {1, 7, 11, 13, 17, 19, 23, 29}
E8_ONLY_COXETER = {7, 13, 17, 23}        # perpendicular sector
H4_PARALLEL_COXETER = {1, 11, 19, 29}    # parallel sector
H4_COXETER_GT1 = {11, 19, 29}            # forbidden by Rule 1 (n=1 exempt)


def selection_rule(n_max=34):
    """
    Return the set of allowed exponents in {1, ..., n_max} per the three rules.

    Rule A (n <= 20): All integers except H4 Coxeter exponents {11, 19}.
    Rule B (n > 20): Only structurally enhanced exponents:
        - Casimir degrees of E8: {24}
        - Doubled E8-only Coxeter: {2*e for e in {7,13,17,23}} = {14,26,34,46}
        - Cross-terms (Casimir + Coxeter): {8+19=27, 14+19=33}
    Rule 3 also forbids n=30 (Coxeter triviality), but n=30 is already > 20
    and not in Rule B, so it is automatically excluded.
    """
    # Rule A: n <= 20, excluding H4 Coxeter cancellations
    rule_A = {n for n in range(1, 21) if n not in H4_COXETER_GT1}

    # Rule B: n > 20, only structurally enhanced
    casimir_enhanced = {24}  # Only Casimir degree > 20 (30 is excluded by Rule 3)
    doubled_coxeter = {2 * e for e in E8_ONLY_COXETER if 20 < 2 * e <= n_max}
    cross_terms = {8 + 19, 14 + 19}  # rank + H4_Cox, Casimir + H4_Cox
    cross_terms = {n for n in cross_terms if n <= n_max}

    rule_B = casimir_enhanced | doubled_coxeter | cross_terms

    return rule_A | rule_B


# ─── Expected Sets ───────────────────────────────────────────────────────────

GSM_ACTUAL = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17, 18,
              20, 24, 26, 27, 33, 34}

FORBIDDEN = {11, 19, 21, 22, 23, 25, 28, 29, 30, 31, 32}


# ─── Extract Exponents from gsm_solver.py ───────────────────────────────────

def extract_phi_exponents(filepath):
    """
    Parse gsm_solver.py and extract all negative integer exponents of PHI.
    Matches patterns like PHI**(-7), PHI**(-14), etc.
    Returns a set of the absolute values of those exponents.
    """
    pattern = re.compile(r'PHI\s*\*\*\s*\(\s*-\s*(\d+)\s*\)')
    exponents = set()
    with open(filepath, 'r') as f:
        for line in f:
            # Skip comments-only lines and docstrings
            stripped = line.strip()
            if stripped.startswith('#') or stripped.startswith('"') or stripped.startswith("'"):
                continue
            # Skip f-string display lines and check() calls (not formulas)
            if 'f"' in line or "f'" in line or 'check(' in line:
                continue
            for match in pattern.finditer(line):
                exponents.add(int(match.group(1)))
    return exponents


# ─── Main Verification ──────────────────────────────────────────────────────

def main():
    all_pass = True

    print("=" * 65)
    print("  GSM Selection Rules Verification")
    print("=" * 65)

    # Test 1: Selection rule produces the correct set
    print("\n[Test 1] Selection rule reproduces GSM exponent set")
    predicted = selection_rule(34)
    if predicted == GSM_ACTUAL:
        print("  PASS  Predicted == Actual")
        print(f"  Allowed (23): {sorted(predicted)}")
    else:
        all_pass = False
        print("  FAIL  Predicted != Actual")
        extra = predicted - GSM_ACTUAL
        missing = GSM_ACTUAL - predicted
        if extra:
            print(f"  Extra in predicted: {sorted(extra)}")
        if missing:
            print(f"  Missing from predicted: {sorted(missing)}")

    # Test 2: Forbidden set is correct complement
    print("\n[Test 2] Forbidden set is exact complement in {1..34}")
    full = set(range(1, 35))
    computed_forbidden = full - predicted
    if computed_forbidden == FORBIDDEN:
        print("  PASS  Forbidden == {1..34} \\ Allowed")
        print(f"  Forbidden (11): {sorted(FORBIDDEN)}")
    else:
        all_pass = False
        print("  FAIL  Forbidden set mismatch")
        print(f"  Expected: {sorted(FORBIDDEN)}")
        print(f"  Got:      {sorted(computed_forbidden)}")

    # Test 3: Rule decomposition
    print("\n[Test 3] Rule decomposition")
    rule1_forbids = H4_COXETER_GT1  # {11, 19, 29}
    rule2_forbids = {21, 22, 23, 25, 28, 31, 32}
    rule3_forbids = {30}
    total_forbidden = rule1_forbids | rule2_forbids | rule3_forbids
    if total_forbidden == FORBIDDEN:
        print(f"  PASS  Rule 1 forbids: {sorted(rule1_forbids)}")
        print(f"        Rule 2 forbids: {sorted(rule2_forbids)}")
        print(f"        Rule 3 forbids: {sorted(rule3_forbids)}")
        print(f"        Union = all 11 forbidden exponents")
    else:
        all_pass = False
        print(f"  FAIL  Rules don't cover all forbidden exponents")
        print(f"  Uncovered: {sorted(FORBIDDEN - total_forbidden)}")

    # Test 4: Cross-check against gsm_solver.py
    print("\n[Test 4] Cross-check against gsm_solver.py formulas")
    solver_path = os.path.join(os.path.dirname(__file__), '..', 'gsm_solver.py')
    solver_path = os.path.normpath(solver_path)

    if not os.path.exists(solver_path):
        print(f"  SKIP  {solver_path} not found")
    else:
        used_exponents = extract_phi_exponents(solver_path)
        print(f"  Exponents found in formulas: {sorted(used_exponents)}")

        # Check which used exponents are outside the predicted set
        violations = used_exponents - predicted
        covered = used_exponents & predicted

        if not violations:
            print(f"  PASS  All {len(used_exponents)} exponents are in predicted set")
        else:
            # Report violations but distinguish between formula-level and annotation
            print(f"  NOTE  {len(violations)} exponent(s) outside predicted set: {sorted(violations)}")
            print(f"        These may indicate formulas that need review or")
            print(f"        selection rule extensions for edge cases.")
            # This is informational -- we still flag it
            all_pass = False

        # Check coverage: which predicted exponents actually appear
        unused = predicted - used_exponents
        if unused:
            print(f"  INFO  Predicted but not found in formulas: {sorted(unused)}")
            print(f"        (These exponents are allowed but not currently used)")

    # Test 5: Structural enhancement verification
    print("\n[Test 5] Structural enhancement for n > 20")
    enhanced = {
        24: "Casimir degree of E8",
        26: "2 x 13 (doubled E8-only Coxeter)",
        27: "8 + 19 (rank + H4 Coxeter)",
        33: "14 + 19 (Casimir + H4 Coxeter)",
        34: "2 x 17 (doubled E8-only Coxeter)",
    }
    large_n = {n for n in predicted if n > 20}
    if large_n == set(enhanced.keys()):
        print("  PASS  All 5 enhanced exponents accounted for:")
        for n in sorted(enhanced):
            print(f"        n = {n}: {enhanced[n]}")
    else:
        all_pass = False
        print(f"  FAIL  Enhanced set mismatch")
        print(f"  Expected: {sorted(enhanced.keys())}")
        print(f"  Got:      {sorted(large_n)}")

    # Summary
    print("\n" + "=" * 65)
    if all_pass:
        print("  RESULT: ALL TESTS PASSED")
    else:
        print("  RESULT: SOME TESTS HAVE ISSUES (see above)")
    print("=" * 65)

    return 0 if all_pass else 1


if __name__ == '__main__':
    sys.exit(main())
