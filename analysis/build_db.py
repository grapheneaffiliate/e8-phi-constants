"""Load the two generated CSVs into a single SQLite artifact.

    python3 analysis/build_db.py

Reads   data/disc_ordered.csv, data/reg_ordered.csv
Writes  data/quadratic_fields.sqlite

Schema (one table per ordering; same columns except for the unit column):

  disc_ordered(D INTEGER PRIMARY KEY, h INTEGER, s INTEGER, R REAL, cyc TEXT)
  reg_ordered (D INTEGER PRIMARY KEY, h INTEGER, s INTEGER, t INTEGER, cyc TEXT)

  s   = N(eps_D) in {+1,-1}
  R   = log eps_D               (disc_ordered; 12 decimals as generated)
  t   = Tr(eps_D)               (reg_ordered; exact, so R is exact downstream)
  cyc = invariant factors of Cl(D), decreasing, '|'-separated, '' when h = 1

For reg_ordered two derived columns are added, since the whole point of the
dataset is that it supports both regulator orderings:

  eps  = (t + sqrt(t^2 - 4 s))/2         the wide fundamental unit
  epsp = eps if s = +1 else eps^2        the narrow (totally positive) one,
                                         which is Sarnak's eps(D)

Integrity checks run at load time and abort the build on failure:
  * D is a fundamental discriminant  (spot-checked, see verify_db.py)
  * h equals the product of the invariant factors
  * t^2 - 4 s is D times a perfect square      (reg_ordered)
  * D and cyc parse, h > 0, s in {+1,-1}
"""

import csv
import math
import os
import sqlite3
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data")
DB = os.path.join(DATA, "quadratic_fields.sqlite")


def parse_cyc(text):
    if not text:
        return []
    return [int(x) for x in text.split("|")]


def isqrt(n):
    return math.isqrt(n)


def load_disc(con, path):
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS disc_ordered")
    cur.execute("CREATE TABLE disc_ordered "
                "(D INTEGER PRIMARY KEY, h INTEGER, s INTEGER, R REAL, cyc TEXT)")
    n = 0
    rows = []
    with open(path) as f:
        rd = csv.reader(f)
        header = next(rd)
        assert header == ["D", "h", "s", "R", "cyc"], header
        for D, h, s, R, cyc in rd:
            D, h, s, R = int(D), int(h), int(s), float(R)
            iv = parse_cyc(cyc)
            prod = 1
            for x in iv:
                prod *= x
            if prod != h:
                raise SystemExit(f"disc_ordered: h != prod(cyc) at D={D}")
            if s not in (1, -1) or h < 1 or R <= 0:
                raise SystemExit(f"disc_ordered: bad row at D={D}")
            rows.append((D, h, s, R, cyc))
            n += 1
            if len(rows) >= 200000:
                cur.executemany("INSERT INTO disc_ordered VALUES (?,?,?,?,?)", rows)
                rows = []
    if rows:
        cur.executemany("INSERT INTO disc_ordered VALUES (?,?,?,?,?)", rows)
    con.commit()
    return n


def load_reg(con, path):
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS reg_ordered")
    cur.execute("CREATE TABLE reg_ordered "
                "(D INTEGER PRIMARY KEY, h INTEGER, s INTEGER, t INTEGER, "
                " u INTEGER, eps REAL, epsp REAL, cyc TEXT)")
    n = 0
    rows = []
    with open(path) as f:
        rd = csv.reader(f)
        header = next(rd)
        assert header == ["D", "h", "s", "t", "cyc"], header
        for D, h, s, t, cyc in rd:
            D, h, s, t = int(D), int(h), int(s), int(t)
            iv = parse_cyc(cyc)
            prod = 1
            for x in iv:
                prod *= x
            if prod != h:
                raise SystemExit(f"reg_ordered: h != prod(cyc) at D={D}")
            m = t * t - 4 * s
            if m <= 0 or m % D != 0:
                raise SystemExit(f"reg_ordered: t^2-4s not divisible by D at D={D}")
            u2 = m // D
            u = isqrt(u2)
            if u * u != u2:
                raise SystemExit(f"reg_ordered: (t^2-4s)/D not a square at D={D}")
            eps = (t + math.sqrt(float(m))) / 2.0
            epsp = eps if s == 1 else eps * eps
            rows.append((D, h, s, t, u, eps, epsp, cyc))
            n += 1
            if len(rows) >= 200000:
                cur.executemany(
                    "INSERT INTO reg_ordered VALUES (?,?,?,?,?,?,?,?)", rows)
                rows = []
    if rows:
        cur.executemany("INSERT INTO reg_ordered VALUES (?,?,?,?,?,?,?,?)", rows)
    con.commit()
    return n


def main():
    if os.path.exists(DB):
        os.remove(DB)
    con = sqlite3.connect(DB)
    con.execute("PRAGMA journal_mode=OFF")
    con.execute("PRAGMA synchronous=OFF")

    dpath = os.path.join(DATA, "disc_ordered.csv")
    rpath = os.path.join(DATA, "reg_ordered.csv")

    if os.path.exists(dpath):
        n = load_disc(con, dpath)
        print(f"disc_ordered: {n} rows")
        con.execute("CREATE INDEX idx_disc_D ON disc_ordered(D)")
    else:
        print("disc_ordered.csv missing", file=sys.stderr)

    if os.path.exists(rpath):
        n = load_reg(con, rpath)
        print(f"reg_ordered : {n} rows")
        con.execute("CREATE INDEX idx_reg_eps  ON reg_ordered(eps)")
        con.execute("CREATE INDEX idx_reg_epsp ON reg_ordered(epsp)")
    else:
        print("reg_ordered.csv missing", file=sys.stderr)

    con.commit()
    con.close()
    print(f"wrote {DB} ({os.path.getsize(DB)/1e6:.1f} MB)")


if __name__ == "__main__":
    main()
