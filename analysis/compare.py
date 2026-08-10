"""Run the pre-registered comparison (preregistration.md) of empirical p-part
distributions against the two named Cohen-Lenstra hypotheses.

    python3 analysis/compare.py

Reads   data/quadratic_fields.sqlite
Writes  data/summary/*.csv   and a text report on stdout.

Nothing here chooses a prime, a truncation bound, a cell merge, or a decision
threshold: all of those are fixed in preregistration.md sections 2, 4 and 5.
"""

import csv
import math
import os
import sqlite3
import sys

import numpy as np
from scipy import stats

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cl  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DB = os.path.join(ROOT, "data", "quadratic_fields.sqlite")
OUT = os.path.join(ROOT, "data", "summary")

PRIMES = (3, 5, 7, 11)
BOOT_SEED = 20260810           # fixed in preregistration.md section 4
BOOT_N = 1000
ZACC, ZREJ = 3.0, 5.0          # preregistration.md section 5
CHI2_REJECT = 1e-3

DISC_BOUNDS = (10**5, 10**6, 10**7)
REG_BOUNDS = (10**4, 10**5, 10**6, 2 * 10**6)

HYPS = (("H_real", 1), ("H_imag", 0))


# ------------------------------------------------------------------ p-parts

def p_part(cyc, p):
    """Partition (decreasing valuations) of the Sylow p-subgroup.

    cyc is the list of invariant factors of Cl, decreasing with c_{i+1} | c_i;
    the Sylow p-subgroup is prod_i Z/p^{v_p(c_i)}.
    """
    out = []
    for c in cyc:
        v = 0
        while c % p == 0:
            c //= p
            v += 1
        if v:
            out.append(v)
    return tuple(out)          # already decreasing since c_{i+1} | c_i


def parse_cyc(text):
    return [int(x) for x in text.split("|")] if text else []


# ------------------------------------------------------------------ loading

def load(table, order_col, bounds):
    """Stream rows sorted by order_col; return per-bound arrays of p-part data.

    Returns dict bound -> dict with
        'n'      : sample size
        p        : list of partitions (one per field) for each p in PRIMES
        'h','R','D','u' : auxiliary arrays for the confounder checks
    """
    con = sqlite3.connect(DB)
    cur = con.cursor()
    has_u = table == "reg_ordered"
    cols = f"D,h,cyc,{order_col}" + (",u,s,t" if has_u else ",R")
    cur.execute(f"SELECT {cols} FROM {table} ORDER BY {order_col}")

    snaps = {}
    parts = {p: [] for p in PRIMES}
    Ds, hs, keys, us, Rs = [], [], [], [], []
    bi = 0
    bounds = sorted(bounds)

    def snapshot(b):
        snaps[b] = {
            "n": len(Ds),
            "parts": {p: list(parts[p]) for p in PRIMES},
            "D": np.array(Ds, dtype=np.int64),
            "h": np.array(hs, dtype=np.int64),
            "R": np.array(Rs, dtype=np.float64),
            "u": np.array(us, dtype=np.int64) if has_u else None,
        }

    for row in cur:
        D, h, cyc, key = row[0], row[1], row[2], row[3]
        if has_u:
            u, s, t = row[4], row[5], row[6]
            R = math.log((t + math.sqrt(t * t - 4.0 * s)) / 2.0)
        else:
            u, R = 0, row[4]
        while bi < len(bounds) and key > bounds[bi]:
            snapshot(bounds[bi])
            bi += 1
        if bi >= len(bounds):
            break
        iv = parse_cyc(cyc)
        for p in PRIMES:
            parts[p].append(p_part(iv, p))
        Ds.append(D)
        hs.append(h)
        Rs.append(R)
        if has_u:
            us.append(u)
    while bi < len(bounds):
        snapshot(bounds[bi])
        bi += 1
    con.close()
    return snaps


# ------------------------------------------------------------------- tests

def moment_test(partitions_list, p, rng):
    """T1: mean of #Surj(Cl, Z/p) = p^rank - 1, with analytic and bootstrap SE."""
    ranks = np.fromiter((len(t) for t in partitions_list), dtype=np.int64,
                        count=len(partitions_list))
    vals = np.power(float(p), ranks) - 1.0
    n = len(vals)
    m = float(vals.mean())
    se = float(vals.std(ddof=1) / math.sqrt(n)) if n > 1 else float("nan")
    # bootstrap by multinomial resampling of the rank histogram (exact
    # equivalent of resampling the values, since the value is a function of rank)
    rk, cnt = np.unique(ranks, return_counts=True)
    rvals = np.power(float(p), rk.astype(float)) - 1.0
    boots = rng.multinomial(n, cnt / cnt.sum(), size=BOOT_N) @ rvals / n
    return m, se, float(boots.std(ddof=1)), n


def rank_dist(partitions_list):
    ranks = np.fromiter((len(t) for t in partitions_list), dtype=np.int64,
                        count=len(partitions_list))
    n = len(ranks)
    return {0: float((ranks == 0).sum()) / n,
            1: float((ranks == 1).sum()) / n,
            2: float((ranks >= 2).sum()) / n}, n


def chi2_test(partitions_list, p, u):
    """T3: Pearson chi-square over abelian p-groups of order <= p^3 plus a
    catch-all; cells with expected count < 5 under THIS null are merged into
    the catch-all first (merge depends on n and the null only)."""
    n = len(partitions_list)
    cells = [tuple(lam) for lam in cl.groups_up_to_order(p, 3)]
    meas = cl.cl_measure(p, u, 40 if p == 3 else 24)
    probs = {c: meas[c] for c in cells}
    keep = [c for c in cells if n * probs[c] >= 5]
    obs = {c: 0 for c in keep}
    other = 0
    keepset = set(keep)
    for t in partitions_list:
        if t in keepset:
            obs[t] += 1
        else:
            other += 1
    p_other = 1.0 - sum(probs[c] for c in keep)
    observed = np.array([obs[c] for c in keep] + [other], dtype=float)
    expected = np.array([n * probs[c] for c in keep] + [n * p_other], dtype=float)
    if (expected < 5).any() or len(observed) < 2:
        return float("nan"), float("nan"), 0, keep, observed, expected
    chi2 = float(((observed - expected) ** 2 / expected).sum())
    df = len(observed) - 1
    return chi2, float(stats.chi2.sf(chi2, df)), df, keep, observed, expected


def verdict(z_real, z_imag, pv_real, pv_imag):
    def one(z, pv):
        if abs(z) > ZREJ or pv < CHI2_REJECT:
            return "reject"
        if abs(z) < ZACC and pv >= CHI2_REJECT:
            return "accept"
        return "undecided"
    vr, vi = one(z_real, pv_real), one(z_imag, pv_imag)
    if vr == "accept" and vi == "reject":
        return "H_real"
    if vi == "accept" and vr == "reject":
        return "H_imag"
    if vr == "reject" and vi == "reject":
        return "neither"
    return f"undecided(real={vr},imag={vi})"


# -------------------------------------------------------------------- main

def analyse(label, snaps, bounds, writer):
    rng = np.random.default_rng(BOOT_SEED)
    print(f"\n{'='*94}\nORDERING: {label}\n{'='*94}")
    for b in bounds:
        s = snaps[b]
        n = s["n"]
        if n == 0:
            continue
        print(f"\n-- bound {b:>12,}   n = {n:,}   "
              f"max D = {int(s['D'].max()):,}   "
              f"mean h = {s['h'].mean():.4g}   "
              f"median R = {np.median(s['R']):.4g}")
        print(f"   {'p':>3} {'M_p':>10} {'SE':>10} {'bootSE':>10} "
              f"{'z(H_real)':>11} {'z(H_imag)':>11} "
              f"{'chi2p(real)':>12} {'chi2p(imag)':>12}  verdict")
        for p in PRIMES:
            pl = s["parts"][p]
            m, se, bse, nn = moment_test(pl, p, rng)
            z_real = (m - 1.0 / p) / se if se > 0 else float("nan")
            z_imag = (m - 1.0) / se if se > 0 else float("nan")
            c_r, pv_r, df_r, keep_r, ob_r, ex_r = chi2_test(pl, p, 1)
            c_i, pv_i, df_i, keep_i, ob_i, ex_i = chi2_test(pl, p, 0)
            rd, _ = rank_dist(pl)
            v = verdict(z_real, z_imag, pv_r, pv_i)
            print(f"   {p:>3} {m:>10.5f} {se:>10.5f} {bse:>10.5f} "
                  f"{z_real:>11.2f} {z_imag:>11.2f} "
                  f"{pv_r:>12.3e} {pv_i:>12.3e}  {v}")
            writer.writerow({
                "ordering": label, "bound": b, "n": n, "p": p,
                "M_p": f"{m:.8f}", "SE": f"{se:.8f}", "bootSE": f"{bse:.8f}",
                "pred_real": f"{1.0/p:.8f}", "pred_imag": "1.0",
                "z_real": f"{z_real:.4f}", "z_imag": f"{z_imag:.4f}",
                "chi2_real": f"{c_r:.4f}", "chi2p_real": f"{pv_r:.6e}", "df_real": df_r,
                "chi2_imag": f"{c_i:.4f}", "chi2p_imag": f"{pv_i:.6e}", "df_imag": df_i,
                "rank0": f"{rd[0]:.6f}", "rank1": f"{rd[1]:.6f}", "rank2plus": f"{rd[2]:.6f}",
                "pred_rank0_real": f"{cl.eta(p,2):.6f}",
                "pred_rank0_imag": f"{cl.eta(p,1):.6f}",
                "verdict": v,
            })


def dump_cells(label, snaps, bound):
    """Full isomorphism-type contingency tables at the largest bound."""
    s = snaps[bound]
    path = os.path.join(OUT, f"celltable_{label}.csv")
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["ordering", "bound", "n", "p", "group", "observed",
                    "expected_real", "expected_imag"])
        for p in PRIMES:
            pl = s["parts"][p]
            n = len(pl)
            cells = [tuple(lam) for lam in cl.groups_up_to_order(p, 3)]
            mr = cl.cl_measure(p, 1, 40 if p == 3 else 24)
            mi = cl.cl_measure(p, 0, 40 if p == 3 else 24)
            obs = {c: 0 for c in cells}
            other = 0
            cs = set(cells)
            for t in pl:
                if t in cs:
                    obs[t] += 1
                else:
                    other += 1
            for c in cells:
                name = "1" if not c else " x ".join(f"Z/{p}^{e}" for e in c)
                w.writerow([label, bound, n, p, name, obs[c],
                            f"{n*mr[c]:.2f}", f"{n*mi[c]:.2f}"])
            w.writerow([label, bound, n, p, f"other(|A|>{p}^3)", other,
                        f"{n*(1-sum(mr[c] for c in cells)):.2f}",
                        f"{n*(1-sum(mi[c] for c in cells)):.2f}"])
    print(f"   wrote {path}")


def confounders(snaps, bound):
    """preregistration.md section 6 checks, regulator ordering only."""
    s = snaps[bound]
    print(f"\n{'='*94}\nCONFOUNDER CHECKS (regulator ordering, bound {bound:,})\n{'='*94}")
    rng = np.random.default_rng(BOOT_SEED)
    u = s["u"]
    print(f"\n[C1] thinness / algebraic family: fraction with u = 1 is "
          f"{float((u==1).sum())/len(u):.4f}  (u>1: {float((u>1).sum())/len(u):.4f})")
    print(f"   {'p':>3} {'M_p(u=1)':>11} {'n(u=1)':>10} {'M_p(u>1)':>11} {'n(u>1)':>10}")
    for p in PRIMES:
        pl = s["parts"][p]
        arr = np.array([len(t) for t in pl])
        for name, mask in (("u1", u == 1), ("ug", u > 1)):
            pass
        v1 = np.power(float(p), arr[u == 1]) - 1.0
        v2 = np.power(float(p), arr[u > 1]) - 1.0
        print(f"   {p:>3} {v1.mean():>11.5f} {len(v1):>10,} "
              f"{(v2.mean() if len(v2) else float('nan')):>11.5f} {len(v2):>10,}")

    print(f"\n[C2] h R = sqrt(D) L bias: statistics by class-number band")
    h = s["h"].astype(float)
    D = s["D"].astype(float)
    R = s["R"]
    L = 2.0 * h * R / np.sqrt(D)
    print(f"   mean h = {h.mean():.4g}   median h = {np.median(h):.4g}   "
          f"mean L(1,chi) = {L.mean():.4f}   median L = {np.median(L):.4f}")
    qs = np.quantile(h, [0.25, 0.5, 0.75])
    bands = [(0, qs[0]), (qs[0], qs[1]), (qs[1], qs[2]), (qs[2], np.inf)]
    print(f"   {'p':>3} " + " ".join(f"{'M_p[q%d]'%(i+1):>10}" for i in range(4)))
    for p in PRIMES:
        arr = np.array([len(t) for t in s["parts"][p]])
        vals = np.power(float(p), arr) - 1.0
        cells = []
        for lo, hi in bands:
            m = (h > lo) & (h <= hi)
            cells.append(vals[m].mean() if m.sum() else float("nan"))
        print(f"   {p:>3} " + " ".join(f"{c:>10.5f}" for c in cells))

    print(f"\n[C3] genus theory control: restrict to D prime "
          f"(genus group trivial, so no 2-part artefact)")
    Dl = s["D"]
    isp = np.array([_isprime(int(x)) for x in Dl])
    print(f"   n(D prime) = {int(isp.sum()):,} of {len(Dl):,}")
    print(f"   {'p':>3} {'M_p(D prime)':>14} {'M_p(all)':>12}")
    for p in PRIMES:
        arr = np.array([len(t) for t in s["parts"][p]])
        vals = np.power(float(p), arr) - 1.0
        print(f"   {p:>3} {vals[isp].mean():>14.5f} {vals.mean():>12.5f}")


def _isprime(n):
    if n < 2:
        return False
    for q in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % q == 0:
            return n == q
    d, r = n - 1, 0
    while d % 2 == 0:
        d //= 2
        r += 1
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(r - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def main():
    os.makedirs(OUT, exist_ok=True)
    fields = ["ordering", "bound", "n", "p", "M_p", "SE", "bootSE",
              "pred_real", "pred_imag", "z_real", "z_imag",
              "chi2_real", "chi2p_real", "df_real",
              "chi2_imag", "chi2p_imag", "df_imag",
              "rank0", "rank1", "rank2plus",
              "pred_rank0_real", "pred_rank0_imag", "verdict"]
    f = open(os.path.join(OUT, "moments.csv"), "w", newline="")
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader()

    print("Cohen-Lenstra predictions (verified in analysis/cl.py::selftest):")
    print(f"   {'p':>3} {'E[#Surj] real':>15} {'E[#Surj] imag':>15} "
          f"{'P(triv) real':>14} {'P(triv) imag':>14}")
    for p in PRIMES:
        print(f"   {p:>3} {1.0/p:>15.6f} {1.0:>15.6f} "
              f"{cl.eta(p,2):>14.6f} {cl.eta(p,1):>14.6f}")

    con = sqlite3.connect(DB)
    tables = {r[0] for r in con.execute(
        "SELECT name FROM sqlite_master WHERE type='table'")}
    con.close()

    if "disc_ordered" in tables:
        snaps = load("disc_ordered", "D", DISC_BOUNDS)
        analyse("disc", snaps, DISC_BOUNDS, w)
        dump_cells("disc", snaps, DISC_BOUNDS[-1])
        del snaps
    if "reg_ordered" in tables:
        snaps = load("reg_ordered", "eps", REG_BOUNDS)
        analyse("reg-wide", snaps, REG_BOUNDS, w)
        dump_cells("reg-wide", snaps, REG_BOUNDS[-1])
        confounders(snaps, REG_BOUNDS[-1])
        del snaps
        snaps = load("reg_ordered", "epsp", REG_BOUNDS)
        analyse("reg-narrow", snaps, REG_BOUNDS, w)
        dump_cells("reg-narrow", snaps, REG_BOUNDS[-1])
        del snaps

    f.close()
    print(f"\nwrote {os.path.join(OUT, 'moments.csv')}")


if __name__ == "__main__":
    main()
