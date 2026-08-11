"""Higher Cohen-Lenstra moments in each ordering.

    python3 analysis/moments2.py

NOT PRE-REGISTERED.  preregistration.md fixed three statistics: the first moment
E[#Surj(Cl, Z/p)], the p-rank distribution, and a chi-square on isomorphism types
up to order p^3.  This script adds two further moments,

    H = Z/p^2      and      H = (Z/p)^2 ,

which the pre-registration did not name.  They are reported as confirmatory, not
as a search: the predictions are fixed by theory before looking, being 1 under
mu_CL and 1/|H| under mu_CL^r for every H (Landesman-Levy arXiv:2410.22210
Thm 1.1.1 proves exactly these two values over function fields), and all six
predictions are checked in analysis/cl.py::selftest.  Nothing here chooses a
threshold or a cell.

Why bother: Wood-Wood (quoted in Landesman-Levy Sec. 1) show the Cohen-Lenstra
distribution is determined by its moments, so agreement on several H is
substantially stronger evidence than agreement on one.  For H = Z/p the two
hypotheses differ by a factor p; for the two H of order p^2 they differ by p^2,
so these are sharper discriminations as well as independent ones.

Caveat recorded up front: #Surj(A, H) grows like p^{2 rank}, so these estimators
have heavy tails and their standard errors are dominated by rare high-rank
fields.  The printed SE is the plain sample SE; where the effective sample of
rank >= 2 fields is small the estimate is reported but should not be read as
precise.  That is flagged per row.
"""

import math
import os
import sqlite3
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cl  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB = os.path.join(ROOT, "data", "quadratic_fields.sqlite")
OUT = os.path.join(ROOT, "data", "summary", "higher_moments.csv")

PRIMES = (3, 5, 7, 11)
HS = ("Zp", "Zp2", "ZpZp")


def p_part(cyc, p):
    out = []
    for c in cyc:
        v = 0
        while c % p == 0:
            c //= p
            v += 1
        if v:
            out.append(v)
    return tuple(out)


def surj_count(lam, p, H):
    if H == "Zp":
        return cl.n_surj_to_Zp(lam, p)
    if H == "Zp2":
        return cl.n_surj_to_Zpk(lam, p, 2)
    return cl.n_surj_to_ZpZp(lam, p)


def load_parts(table, order_col, bound):
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute(f"SELECT cyc FROM {table} WHERE {order_col} <= ?", (bound,))
    parts = {p: [] for p in PRIMES}
    n = 0
    for (cyc,) in cur:
        iv = [int(x) for x in cyc.split("|")] if cyc else []
        for p in PRIMES:
            parts[p].append(p_part(iv, p))
        n += 1
    con.close()
    return parts, n


def run(label, table, order_col, bound, writer):
    parts, n = load_parts(table, order_col, bound)
    print(f"\n{'='*100}\n{label}   n = {n:,}\n{'='*100}")
    print(f"{'p':>3} {'H':>6} {'|H|':>5} {'E[#Surj] obs':>14} {'SE':>11} "
          f"{'mu_CL=1':>9} {'mu_CL^r':>9} {'z vs CL':>9} {'z vs CL^r':>10}  n(rank>=2)")
    for p in PRIMES:
        pl = parts[p]
        ranks = np.fromiter((len(t) for t in pl), dtype=np.int64, count=n)
        n_hi = int((ranks >= 2).sum())
        for H in HS:
            vals = np.fromiter((surj_count(t, p, H) for t in pl),
                               dtype=np.float64, count=n)
            m = float(vals.mean())
            se = float(vals.std(ddof=1) / math.sqrt(n))
            pred_r = 1.0 / cl.H_ORDER[H](p)
            z0 = (m - 1.0) / se if se > 0 else float("nan")
            z1 = (m - pred_r) / se if se > 0 else float("nan")
            flag = "" if (H == "Zp" or n_hi >= 200) else "   <-- thin"
            print(f"{p:>3} {H:>6} {cl.H_ORDER[H](p):>5} {m:>14.5f} {se:>11.5f} "
                  f"{1.0:>9.5f} {pred_r:>9.5f} {z0:>9.1f} {z1:>10.1f}  "
                  f"{n_hi:>9,}{flag}")
            writer.write(f"{label},{n},{p},{H},{cl.H_ORDER[H](p)},{m:.8f},"
                         f"{se:.8f},1.0,{pred_r:.8f},{z0:.4f},{z1:.4f},{n_hi}\n")


def main():
    con = sqlite3.connect(DB)
    tables = {r[0] for r in con.execute(
        "SELECT name FROM sqlite_master WHERE type='table'")}
    con.close()

    print("Predicted E[#Surj(Cl,H)]  (verified in analysis/cl.py::selftest):")
    print("   mu_CL   (imaginary, u=0):  1        for every H")
    print("   mu_CL^r (real,      u=1):  1/|H|    for every H")

    f = open(OUT, "w")
    f.write("ordering,n,p,H,absH,obs,SE,pred_imag,pred_real,z_imag,z_real,n_rank_ge2\n")

    if "disc_ordered" in tables:
        run("disc  (D <= 1e7)", "disc_ordered", "D", 10**7, f)
    if "disc_window" in tables:
        run("disc-window (D ~ 1e12)", "disc_window", "D", 10**14, f)
    if "reg_ordered" in tables:
        for b in (10**5, 10**6, 2 * 10**6):
            run(f"reg-wide (eps <= {b:.0e})", "reg_ordered", "eps", b, f)
        run("reg-narrow (eps+ <= 2e6)", "reg_ordered", "epsp", 2 * 10**6, f)
    f.close()
    print(f"\nwrote {OUT}")


if __name__ == "__main__":
    main()
