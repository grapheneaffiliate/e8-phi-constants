#!/usr/bin/env python3
"""Check the closed forms of the E8 root projection fractions quoted in the documents.

Two projections R^8 -> R^4 appear in this repository and they are NOT the same map:

  (a) the coordinate-pairing map of proofs/e8_oneloop_calculation.py,
          P_par,k = (a_2k + phi * a_2k+1) / sqrt(2 + phi),   k = 0..3,
      whose parallel fractions p = |P_par r|^2 / 2 take FIVE values on the 240 roots,
          p = 1/2 + k / (2 sqrt5),  k = -2..2   (0.0528, 0.2764, 0.5, 0.7236, 0.9472)
      with multiplicities 24, 24, 144, 24, 24 — quoted in GSM_COMPLETE_BUNDLE.md section 1.5;

  (b) the H4-symmetric projection: V_par is the sum of the E8 Coxeter element's eigenplanes with the
      H4 exponents {1, 29} and {11, 19}. Under it the 240 roots land on TWO 600-cells of 120 roots
      with fractions (5 -+ sqrt5)/10 — quoted in proofs/h4_cancellation_proof.md section 5.2.

Both tables carried wrong closed forms until 2026-09-18 ((3 -+ sqrt5)/8, (3 - phi^-1)/5 and
(3 -+ sqrt5)/4, which evaluate to 0.0955/0.6545, 0.4764 and 0.191/1.309). This script recomputes
every quoted value from the roots and the stated formulas, so the documents cannot drift again.
Exit 0 = every quoted closed form evaluates to the value beside it AND matches the computed spectrum.
"""
import itertools
import math
import sys

import numpy as np

PHI = (1 + math.sqrt(5)) / 2
S5 = math.sqrt(5)


def e8_roots():
    roots = []
    for i, j in itertools.combinations(range(8), 2):
        for si in (1, -1):
            for sj in (1, -1):
                v = np.zeros(8); v[i] = si; v[j] = sj
                roots.append(v)
    for signs in itertools.product((1, -1), repeat=8):
        if signs.count(-1) % 2 == 0:
            roots.append(np.array(signs) / 2)
    return np.array(roots)


def reflection(v):
    v = v / np.linalg.norm(v)
    return np.eye(len(v)) - 2 * np.outer(v, v)


def coxeter_parallel_basis():
    a = np.zeros((8, 8))
    a[0] = [0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, 0.5]
    a[1] = [1, 1, 0, 0, 0, 0, 0, 0]
    for k in range(2, 8):
        a[k, k - 2] = -1; a[k, k - 1] = 1
    c = np.eye(8)
    for r in a:
        c = c @ reflection(r)
    vals, vecs = np.linalg.eig(c)
    m = np.angle(vals) / (2 * math.pi) * 30
    cols = []
    for target in (1, 11):
        k = int(np.argmin(np.abs(m - target)))
        assert abs(m[k] - target) < 1e-6
        cols += [vecs[:, k].real, vecs[:, k].imag]
    B, _ = np.linalg.qr(np.stack(cols, axis=1))
    return B


def spectrum(fractions):
    vals, counts = np.unique(np.round(fractions, 7), return_counts=True)
    return dict(zip(vals.tolist(), counts.tolist()))


def main():
    R = e8_roots()
    assert R.shape == (240, 8)
    ok = True

    # (a) coordinate-pairing map and the bundle's table
    Bc = np.zeros((8, 4))
    for k in range(4):
        Bc[2 * k, k] = 1 / math.sqrt(2 + PHI)
        Bc[2 * k + 1, k] = PHI / math.sqrt(2 + PHI)
    spec_a = spectrum(((R @ Bc) ** 2).sum(1) / 2)
    table_a = [("1/2 - 1/sqrt5 = (7-4phi)/10", 0.5 - 1 / S5, (7 - 4 * PHI) / 10, 24),
               ("1/2 - 1/(2 sqrt5) = (5-sqrt5)/10", 0.5 - 1 / (2 * S5), (5 - S5) / 10, 24),
               ("1/2", 0.5, 0.5, 144),
               ("1/2 + 1/(2 sqrt5) = (5+sqrt5)/10", 0.5 + 1 / (2 * S5), (5 + S5) / 10, 24),
               ("1/2 + 1/sqrt5 = (3+4phi)/10", 0.5 + 1 / S5, (3 + 4 * PHI) / 10, 24)]
    print("(a) coordinate-pairing map (GSM_COMPLETE_BUNDLE.md 1.5):")
    for name, f1, f2, n in table_a:
        got = spec_a.get(round(f1, 7))
        good = abs(f1 - f2) < 1e-12 and got == n
        ok &= good
        print("    %-36s = %.7f   roots %-4s (table says %d)   %s" % (name, f1, got, n, "ok" if good else "FAIL"))
    old = [("(3-sqrt5)/8", (3 - S5) / 8), ("(3-phi^-1)/5", (3 - 1 / PHI) / 5), ("(3+sqrt5)/8", (3 + S5) / 8)]
    for name, v in old:
        in_spec = round(v, 7) in spec_a
        ok &= not in_spec
        print("    old closed form %-14s = %.7f  -> in the spectrum: %s (must be False)" % (name, v, in_spec))

    # (b) the H4-symmetric projection and the cancellation proof's table
    B = coxeter_parallel_basis()
    spec_b = spectrum(((R @ B) ** 2).sum(1) / 2)
    print("(b) H4-symmetric Coxeter-eigenplane projection (proofs/h4_cancellation_proof.md 5.2):")
    table_b = [("(5-sqrt5)/10 = 1/(2+phi)", (5 - S5) / 10, 1 / (2 + PHI), 120),
               ("(5+sqrt5)/10 = (1+phi)/(2+phi)", (5 + S5) / 10, (1 + PHI) / (2 + PHI), 120)]
    for name, f1, f2, n in table_b:
        got = spec_b.get(round(f1, 7))
        good = abs(f1 - f2) < 1e-12 and got == n
        ok &= good
        print("    %-36s = %.7f   roots %-4s (60 positive + 60 negative)   %s" % (name, f1, got, "ok" if good else "FAIL"))
    two_shells = sorted(spec_b.values()) == [120, 120]
    ok &= two_shells
    print("    exactly two shells of 120: %s" % two_shells)
    for name, v in (("(3-sqrt5)/4", (3 - S5) / 4), ("(3+sqrt5)/4", (3 + S5) / 4)):
        in_spec = round(v, 7) in spec_b
        ok &= not in_spec
        print("    old closed form %-14s = %.7f  -> in the spectrum: %s (must be False)" % (name, v, in_spec))
    print("RESULT: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
