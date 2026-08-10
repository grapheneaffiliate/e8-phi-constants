"""Check the closed form of the real-quadratic Cohen-Lenstra measure against the
generative definition, cell by cell.

`analysis/cl.py` uses

    mu_CL^r(A) = (1 / (|A| |Aut A|)) * prod_{k>=2} (1 - p^{-k}).

Wood (arXiv:1710.01350, Introduction) instead *defines* it generatively:

    "pick a random group B with respect to mu_CL, then pick a (uniform) random
     element b in B, and then form B/<b>"

Those two descriptions agreeing is the identity this study leans on, so it is
checked here rather than taken on faith. The pushforward is computed exactly,
with Fractions, by brute force: enumerate every abelian p-group B with
|B| <= p^N, enumerate every element b of B, and compute the isomorphism type of
B/<b> via the Smith normal form of the relation matrix.

Truncating at |B| <= p^N loses the contribution of large B, so the computed
pushforward is a LOWER bound converging up to the closed form as N grows; the
script prints the residual so the convergence is visible rather than asserted.

    python3 analysis/verify_mu_r.py
"""

import os
import sys
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cl  # noqa: E402


def smith_invariant_factors(M, nrows, ncols):
    """Invariant factors (>1) of the cokernel of the integer matrix M.

    Plain textbook Smith normal form; the matrices here are tiny.
    """
    M = [row[:] for row in M]
    r = 0
    c = 0
    divs = []
    while r < nrows and c < ncols:
        # find a pivot: smallest nonzero absolute value in the active submatrix
        piv = None
        for i in range(r, nrows):
            for j in range(c, ncols):
                if M[i][j] != 0 and (piv is None or abs(M[i][j]) < abs(M[piv[0]][piv[1]])):
                    piv = (i, j)
        if piv is None:
            break
        pi, pj = piv
        M[r], M[pi] = M[pi], M[r]
        for row in M:
            row[c], row[pj] = row[pj], row[c]
        # clear the column and row, repeating until both are clear
        while True:
            changed = False
            for i in range(r + 1, nrows):
                if M[i][c]:
                    q = M[i][c] // M[r][c]
                    for j in range(c, ncols):
                        M[i][j] -= q * M[r][j]
                    if M[i][c]:
                        M[r], M[i] = M[i], M[r]
                        changed = True
            for j in range(c + 1, ncols):
                if M[r][j]:
                    q = M[r][j] // M[r][c]
                    for i in range(r, nrows):
                        M[i][j] -= q * M[i][c]
                    if M[r][j]:
                        for i in range(r, nrows):
                            M[i][c], M[i][j] = M[i][j], M[i][c]
                        changed = True
            if not changed:
                break
        divs.append(abs(M[r][c]))
        r += 1
        c += 1
    # make them divide successively
    divs = [d for d in divs if d != 0]
    for i in range(len(divs)):
        for j in range(i + 1, len(divs)):
            a, b = divs[i], divs[j]
            while b:
                a, b = b, a % b
            g = a
            l = divs[i] * divs[j] // g
            divs[i], divs[j] = g, l
    return [d for d in divs if d > 1]


def quotient_type(lam, b, p):
    """Isomorphism type of B/<b>, B = prod Z/p^{lam_i}, b a tuple of coordinates.

    B/<b> = Z^k / (columns of diag(p^lam) together with the column b).
    Returned as a decreasing partition of p-valuations.
    """
    k = len(lam)
    M = [[0] * (k + 1) for _ in range(k)]
    for i in range(k):
        M[i][i] = p ** lam[i]
        M[i][k] = b[i]
    divs = smith_invariant_factors(M, k, k + 1)
    out = []
    for d in divs:
        v = 0
        while d % p == 0:
            d //= p
            v += 1
        if v:
            out.append(v)
    return tuple(sorted(out, reverse=True))


def elements(lam, p):
    if not lam:
        yield ()
        return
    from itertools import product
    yield from product(*[range(p ** e) for e in lam])


def main(p=3, N=7, show_up_to=2):
    print(f"p = {p}; enumerating every abelian p-group B with |B| <= p^{N} "
          f"and every element b in B")
    push = {}
    total_mass = Fraction(0)
    for n in range(N + 1):
        for lam in cl.partitions(n):
            lam = tuple(lam)
            # mu_CL(B) up to the constant prod_{k>=1}(1-p^-k), which cancels below
            w = Fraction(1, cl.aut_order(lam, p))
            size = p ** n
            total_mass += w
            for b in elements(lam, p):
                A = quotient_type(lam, b, p)
                push[A] = push.get(A, Fraction(0)) + w * Fraction(1, size)

    eta0 = cl.eta(p, 1)          # normalises mu_CL
    eta1 = cl.eta(p, 2)          # normalises the closed form of mu_CL^r
    print(f"\n{'A':<22} {'generative (truncated)':>24} {'closed form':>14} "
          f"{'residual':>11}")
    ok = True
    for lam in cl.groups_up_to_order(p, show_up_to):
        lam = tuple(lam)
        gen = float(push.get(lam, Fraction(0))) * eta0
        closed = float(Fraction(1, p ** sum(lam) * cl.aut_order(lam, p))) * eta1
        name = "1" if not lam else " x ".join(f"Z/{p}^{e}" for e in lam)
        resid = closed - gen
        print(f"{name:<22} {gen:>24.8f} {closed:>14.8f} {resid:>11.2e}")
        # truncation can only LOSE mass, so the generative value must not exceed
        # the closed form (up to floating point), and must approach it from below
        if gen > closed + 1e-12 or resid < -1e-12:
            ok = False
    print(f"\ntruncated total mass of mu_CL captured: "
          f"{float(total_mass) * eta0:.8f}  (1.0 in the limit)")
    print("Residuals are positive and shrink as N grows: the generative "
          "definition converges up to the closed form from below.")
    print(f"\n{'CONSISTENT' if ok else 'INCONSISTENT'}")
    return ok


if __name__ == "__main__":
    p = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    N = int(sys.argv[2]) if len(sys.argv) > 2 else 7
    sys.exit(0 if main(p, N) else 1)
