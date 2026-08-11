"""Cohen-Lenstra measures on finite abelian p-groups, and the group theory needed
to compare them with tabulated class groups.

Sources for the two measures (both quoted, not reconstructed):

  M. M. Wood, "Cohen-Lenstra heuristics and local conditions", Res. Number
  Theory 4 (2018), arXiv:1710.01350, Introduction, p.1:

      mu_CL(A) := (1/|Aut(A)|) * prod_{i>=1} (1 - p^{-i})

  is conjectured (Cohen-Lenstra [CL84]) to give the distribution of the Sylow
  p-subgroup of Cl(O_K) for K imaginary quadratic.  For K real quadratic, the
  conjectured measure mu_CL^r is defined there as the law of B/<b> where B is
  drawn from mu_CL and b is a uniform random element of B.

This module works with the closed form of mu_CL^r,

      mu_CL^r(A) = (1 / (|A| * |Aut(A)|)) * prod_{k>=2} (1 - p^{-k}),

and does NOT take that closed form on faith: `selftest()` checks the
normalisation of both measures against the Cohen-Lenstra/Hall identity

      sum_A 1/(|A|^u |Aut A|) = prod_{k >= u+1} (1 - p^{-k})^{-1},

and checks the first moments

      sum_A mu_CL(A)   * #Surj(A, Z/p) = 1        (imaginary, u=0)
      sum_A mu_CL^r(A) * #Surj(A, Z/p) = 1/p      (real,      u=1)

against the two independent external anchors:
  * Davenport-Heilbronn (1971): average of |Cl[3]| is 2 for imaginary and 4/3
    for real quadratic fields, i.e. average #Surj(Cl, Z/3) is 1 and 1/3.
  * Landesman-Levy (arXiv:2410.22210) Theorem 1.1.1: over F_q(t) the average of
    |Surj(Cl(O_K), H)| tends to 1 in the imaginary case and 1/|H| in the real
    case.

|Aut(A)| uses the Hillar-Rhea formula (Amer. Math. Monthly 114 (2007), 917-923,
Theorem 4.1); `selftest()` checks it against hand values.
"""

from fractions import Fraction
from functools import lru_cache
from itertools import count

# ---------------------------------------------------------------- partitions

def partitions(n, maxpart=None):
    """Partitions of n as weakly decreasing tuples."""
    if maxpart is None:
        maxpart = n
    if n == 0:
        yield ()
        return
    for first in range(min(n, maxpart), 0, -1):
        for rest in partitions(n - first, first):
            yield (first,) + rest


def groups_up_to_order(p, max_exp):
    """All finite abelian p-groups of order <= p**max_exp, as partitions.

    The partition (e_1 >= e_2 >= ...) denotes  Z/p^e_1 x Z/p^e_2 x ... ;
    the empty partition is the trivial group.
    """
    out = []
    for n in range(max_exp + 1):
        out.extend(partitions(n))
    return out


# ------------------------------------------------------------------ |Aut(A)|

@lru_cache(maxsize=None)
def aut_order(lam, p):
    """|Aut(A)| for A = prod Z/p^{lam_i}, via Hillar-Rhea Theorem 4.1.

    Hillar-Rhea state the formula for e_1 <= e_2 <= ... <= e_n, so the
    (decreasing) partition is reversed first.
    """
    e = sorted(lam)                      # increasing, as Hillar-Rhea require
    n = len(e)
    if n == 0:
        return 1
    d = [max(l for l in range(1, n + 1) if e[l - 1] == e[k - 1]) for k in range(1, n + 1)]
    c = [min(l for l in range(1, n + 1) if e[l - 1] == e[k - 1]) for k in range(1, n + 1)]
    res = 1
    for k in range(1, n + 1):
        res *= p ** d[k - 1] - p ** (k - 1)
    for j in range(1, n + 1):
        res *= p ** (e[j - 1] * (n - d[j - 1]))
    for i in range(1, n + 1):
        res *= p ** ((e[i - 1] - 1) * (n - c[i - 1] + 1))
    return res


def group_order(lam, p):
    return p ** sum(lam)


def rank(lam):
    """p-rank = dim_{F_p} A/pA = number of invariant factors."""
    return len(lam)


def n_surj_to_Zp(lam, p):
    """#Surj(A, Z/p) = |A/pA| - 1 = p^rank - 1."""
    return p ** len(lam) - 1


def n_hom_to_Zpk(lam, p, k):
    """#Hom(A, Z/p^k) = prod_i p^{min(lam_i, k)}."""
    e = 0
    for x in lam:
        e += min(x, k)
    return p ** e


def n_surj_to_Zpk(lam, p, k):
    """#Surj(A, Z/p^k).

    A homomorphism to Z/p^k fails to be surjective exactly when its image lies
    in the unique index-p subgroup, which is isomorphic to Z/p^{k-1}.  Hence
    #Surj = #Hom(A, Z/p^k) - #Hom(A, Z/p^{k-1}).
    """
    return n_hom_to_Zpk(lam, p, k) - n_hom_to_Zpk(lam, p, k - 1)


def n_surj_to_ZpZp(lam, p):
    """#Surj(A, (Z/p)^2).

    (Z/p)^2 is elementary abelian, so every hom factors through A/pA = (Z/p)^r;
    surjections correspond to rank-2 matrices in Hom(F_p^r, F_p^2), of which
    there are (p^r - 1)(p^r - p).  This is 0 for r < 2, as it must be.
    """
    r = len(lam)
    return (p ** r - 1) * (p ** r - p)


def cl_moment(p, u, H, max_exp=None):
    """Predicted E[#Surj(Cl, H)] under the CL measure of unit rank u.

    H is one of 'Zp', 'Zp2', 'ZpZp'.  The Cohen-Lenstra moments are 1 for u = 0
    and 1/|H| for u = 1 (Landesman-Levy arXiv:2410.22210 Thm 1.1.1 proves exactly
    these over function fields, i = 1 and i = 0 respectively).
    """
    if max_exp is None:
        max_exp = 34 if p == 3 else 22 if p == 5 else 18
    m = cl_measure(p, u, max_exp)
    f = {"Zp": lambda lam: n_surj_to_Zp(lam, p),
         "Zp2": lambda lam: n_surj_to_Zpk(lam, p, 2),
         "ZpZp": lambda lam: n_surj_to_ZpZp(lam, p)}[H]
    return sum(pr * f(lam) for lam, pr in m.items())


H_ORDER = {"Zp": lambda p: p, "Zp2": lambda p: p * p, "ZpZp": lambda p: p * p}


# ------------------------------------------------------------- the measures

def eta(p, start, terms=400):
    """prod_{k >= start} (1 - p^{-k}) as a float."""
    v = 1.0
    for k in range(start, start + terms):
        t = p ** (-k)
        if t < 1e-30:
            break
        v *= 1.0 - t
    return v


def cl_weight(lam, p, u):
    """Unnormalised Cohen-Lenstra weight 1/(|A|^u |Aut A|)."""
    return Fraction(1, group_order(lam, p) ** u * aut_order(tuple(lam), p))


def cl_measure(p, u, max_exp):
    """{partition: probability} for the CL measure with unit rank u.

    u = 0 -> mu_CL   (imaginary quadratic)
    u = 1 -> mu_CL^r (real quadratic)

    Normalisation uses the exact infinite product prod_{k >= u+1}(1-p^{-k}),
    NOT the finite sum, so the returned probabilities sum to slightly less
    than 1; the deficit is exactly the mass on groups of order > p^max_exp.
    """
    norm = eta(p, u + 1)
    return {tuple(lam): float(cl_weight(lam, p, u)) * norm
            for lam in groups_up_to_order(p, max_exp)}


def cl_rank_probs(p, u, max_exp=12):
    """Probability of each p-rank under the CL measure with unit rank u."""
    m = cl_measure(p, u, max_exp)
    out = {}
    for lam, pr in m.items():
        out[len(lam)] = out.get(len(lam), 0.0) + pr
    return out


def cl_moment_Zp(p, u, max_exp=14):
    """Predicted average of #Surj(Cl, Z/p): should be p^{-u}."""
    m = cl_measure(p, u, max_exp)
    return sum(pr * n_surj_to_Zp(lam, p) for lam, pr in m.items())


# ----------------------------------------------------------------- self test

def selftest(verbose=True):
    ok = True

    def chk(name, got, want, tol=0.0):
        nonlocal ok
        good = (abs(got - want) <= tol) if tol else (got == want)
        ok = ok and good
        if verbose:
            print(f"  [{'ok ' if good else 'FAIL'}] {name}: got {got}, want {want}")

    if verbose:
        print("|Aut(A)| (Hillar-Rhea) against hand computation:")
    chk("|Aut(Z/3)|",            aut_order((1,), 3),     2)
    chk("|Aut(Z/9)|",            aut_order((2,), 3),     6)
    chk("|Aut(Z/3 x Z/3)|",      aut_order((1, 1), 3),   48)     # |GL_2(F_3)|
    chk("|Aut(Z/2 x Z/4)|",      aut_order((2, 1), 2),   8)
    chk("|Aut(Z/3 x Z/9)|",      aut_order((2, 1), 3),   3**3 * 2**2)
    chk("|Aut(Z/5 x Z/5 x Z/5)|", aut_order((1, 1, 1), 5),
        (5**3 - 1) * (5**3 - 5) * (5**3 - 5**2))

    # Truncating at order p^E omits mass; the omitted mass is largest for the
    # smallest p and for u=0 (lighter 1/|A|^u damping), so E is chosen per p.
    EXP = {3: 34, 5: 22, 7: 18, 11: 16}
    TOL = 1e-7

    if verbose:
        print("\nCohen-Lenstra/Hall normalisation "
              "sum_A 1/(|A|^u |Aut A|) = prod_{k>u} (1-p^-k)^-1")
        print("  (finite sums over |A| <= p^E; deficit shown is pure truncation)")
    for p in (3, 5, 7, 11):
        for u in (0, 1):
            s = sum(float(cl_weight(lam, p, u))
                    for lam in groups_up_to_order(p, EXP[p]))
            want = 1.0 / eta(p, u + 1)
            if verbose:
                print(f"      p={p:2d} u={u} E={EXP[p]}  deficit = {want - s:.3e}")
            chk(f"p={p} u={u}", s, want, TOL)

    if verbose:
        print("\nFirst moment  E[#Surj(Cl, Z/p)]  (want p^-u):")
    for p in (3, 5, 7, 11):
        for u in (0, 1):
            chk(f"p={p} u={u}", cl_moment_Zp(p, u, EXP[p]), float(p ** -u), TOL)

    if verbose:
        print("\nHigher moments E[#Surj(Cl,H)] (want 1 for u=0, 1/|H| for u=1):")
    for p in (3, 5, 7):
        for H in ("Zp", "Zp2", "ZpZp"):
            for u in (0, 1):
                want = 1.0 if u == 0 else 1.0 / H_ORDER[H](p)
                chk(f"p={p} H={H} u={u}", cl_moment(p, u, H, EXP[p]), want, TOL)

    if verbose:
        print("\nExternal anchors:")
    # Davenport-Heilbronn: average |Cl[3]| = 1 + E[#Surj(.,Z/3)]
    chk("avg |Cl[3]| imaginary (Davenport-Heilbronn 1971)",
        1 + cl_moment_Zp(3, 0, EXP[3]), 2.0, TOL)
    chk("avg |Cl[3]| real      (Davenport-Heilbronn 1971)",
        1 + cl_moment_Zp(3, 1, EXP[3]), 4 / 3, TOL)

    if verbose:
        print("\nP(Sylow p-subgroup trivial):")
        for p in (3, 5, 7, 11):
            print(f"  p={p:2d}  u=0 (imaginary) {eta(p,1):.6f}   "
                  f"u=1 (real) {eta(p,2):.6f}")

    if verbose:
        print(f"\nSELFTEST {'PASSED' if ok else 'FAILED'}")
    return ok


if __name__ == "__main__":
    import sys
    sys.exit(0 if selftest() else 1)
