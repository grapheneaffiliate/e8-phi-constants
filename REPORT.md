# ℚ(√5) extremality and regulator-ordered class group statistics

Tags: `[COMPUTED]` (script + bound given, re-runnable) · `[CLASSICAL]` (author,
year, venue, specific result) · `[CONJECTURAL]` (believed, unproved, phrased as a
question) · `[UNVERIFIED]` (not checked; may not support any other claim).

---

## 1. Verdict table

| # | Statement | Verdict | Evidence | Reference / script |
|---|---|---|---|---|
| E1 | 5 is the smallest fundamental discriminant of a real quadratic field | **KNOWN** | `[COMPUTED]` + definition | `data/verify_extremality.gp`; `EXTREMALITY_NOTE.md` E1 |
| E2 | `R(ℚ(√5)) = log φ` is the smallest regulator of any real quadratic field/order | **KNOWN** | `[COMPUTED]` + complete elementary proof | `data/verify_extremality.gp`; `EXTREMALITY_NOTE.md` E2 |
| E3 | √5 is optimal in Hurwitz's theorem; φ is the worst-approximable irrational; min of the Lagrange spectrum is √5 | **KNOWN** | `[CLASSICAL]` + `[COMPUTED]` numerics | Hurwitz, Math. Ann. 39 (1891), 279–284; Markoff, Math. Ann. 15/17 (1879/80); Cusick–Flahive (1989) ch. 1 |
| E4 | ℚ(√5) gives the shortest primitive closed geodesic on ℍ/PSL₂(ℤ) | **KNOWN** | `[COMPUTED]` + complete elementary derivation | `data/verify_extremality.gp`; `EXTREMALITY_NOTE.md` E4 |
| E4′ | …**of length `2 log φ ≈ 0.9624`** (as asserted in the brief) | **FALSE** | `[COMPUTED]` | length is `4 log φ = 2 arccosh(3/2) = 1.92485`; `2 log φ` is the half-length |
| K1 | `h(ℚ(√5)) = 1` carries no class-group information | **KNOWN** (true) | `[COMPUTED]` | Minkowski bound `√5/2 ≈ 1.118 < 2` |
| K1a | `h = 1` distinguishes ℚ(√5) among real quadratic fields | **FALSE** | `[COMPUTED]` | D ∈ {5, 8, 12, 13} all have Minkowski bound < 2, so all have h = 1 forced |
| H1 | ℚ(√5) is distinguished by its position in the Cohen–Lenstra distribution | **FALSE** | `[COMPUTED]` + `[CLASSICAL]` | §3.1 — it sits at the *mode*, and shares its class group with the first 11 discriminants |
| H2 | Landesman–Levy says something about an individual field | **FALSE** | `[CLASSICAL]`, verbatim hypotheses | §3.2 — arXiv:2410.22210 Thm 1.1.1 |
| H3 | `h(ℚ(√5)) = 1` is evidence beyond D = 5 being small | **FALSE** | `[COMPUTED]` | §3.3, = K1a |
| H4 | Being the first term of Sarnak's regulator-ordered asymptotic is a distinguishing property | **FALSE** | argument, §3.4 | Sarnak, J. Number Theory 15 (1982), 229–247 |
| H5 | Hurwitz-space topology (Landesman–Levy) and modular-surface geometry (Sarnak) constitute a mathematical link | **FALSE** | argument, §3.5 | §3.5 states what would be required and shows none of it holds |
| Q1 | Under regulator ordering, the odd p-part of `Cl` follows the **real** quadratic Cohen–Lenstra measure `μ^r_CL` (the same as under discriminant ordering) | **FALSE** | `[COMPUTED]`, n = 3 996 897 | §4.2; `analysis/compare.py` |
| Q2 | Under regulator ordering, it follows the **imaginary** quadratic measure `μ_CL` instead | **NOVEL** (empirical only — *not a theorem*, see §4.7) | `[COMPUTED]`, 12 moments (4 primes × 3 groups) all converging, 4 bounds, 5 controls | §4.2–§4.6a |
| Q3 | The difference is a D-size effect rather than a regulator effect | **FALSE** | `[COMPUTED]`, n = 250 000 at D ≈ 10¹² | §4.3 |
| Q4 | The regulator-ordered behaviour is just "h is large, so `p ∣ h` with probability ≈ 1/p" | **FALSE** | `[COMPUTED]` | §4.5 |
| S1 | Sarnak's asymptotic `Σ_{ε(D)<x} h(D) ~ li(x²)` | **KNOWN** (true, and stated for the **narrow** class number and **narrow** unit) | `[CLASSICAL]` | verbatim in Hashimoto arXiv:1003.3716 §1 eqns (1.2)–(1.3) |
| S3 | Landesman–Levy does not reach ℚ(√5) | **KNOWN** (true) | `[CLASSICAL]` | §3.2 |

---

## 2. Headline

**Nothing in the ℚ(√5) extremality cluster is novel — E1–E4 are entirely
classical, the class-number argument that the sponsoring framework rests on is
refuted outright, and all five hypotheses H1–H5 are false.** One thing that is
not about ℚ(√5) did come out of the primary research question, and it is an
empirical finding rather than a theorem: when real quadratic fields are ordered
by regulator instead of by discriminant, the odd part of the class group appears
to follow the Cohen–Lenstra measure for **imaginary** quadratic fields,
`μ_CL(A) ∝ 1/|Aut A|`, and not the measure `μ^r_CL(A) ∝ 1/(|A||Aut A|)` that the
same fields obey when ordered by discriminant. Over a complete enumeration of the
3 996 897 real quadratic fields with `ε_D ≤ 2·10⁶` (reaching `D ≈ 4·10¹²`), the
proportion with `p ∣ h` is 0.43497, 0.23787, 0.16178, 0.09807 for
p = 3, 5, 7, 11, against the imaginary Cohen–Lenstra values 0.43987, 0.23967,
0.16320, 0.09917 — and against the real-quadratic values 0.15981, 0.04958,
0.02374, 0.00908, which are wrong by factors of 2.7 to 10.8. The residuals shrink
monotonically as the bound grows (roughly like `T^{-1/2}`), while the residuals
against the real-quadratic measure grow. Testing two further moments — `H = ℤ/p²`
and `H = (ℤ/p)²`, where the two hypotheses differ by a factor `p²` rather than
`p` — gives twelve independent statistics in all, and **all twelve converge
monotonically to the imaginary prediction** while excluding the real one at z
between 17 and 935 (§4.6a); since moments determine the distribution
(Wood–Wood), that is qualitatively stronger than the single-moment test. Five controls survive, including the
decisive one: a discriminant-ordered sample of 250 000 fields at the *same*
`D ≈ 10¹²` scale reproduces the **real** measure to within about 2%, so the effect is
caused by the regulator condition and not by the size of D. I found no statement
of this in the literature, but it is not deep: it follows in a few lines from an
analogy that Cohen and Lenstra themselves record, credited to Gross. It is not
proved here, and `THEOREM_STATEMENT.md` has deliberately not been created (§4.7).

---

## 3. Negative results

Every refutation attempted, including the ones that refute claims in the
sponsoring framework and in the brief that commissioned this work.

### 3.0 Two errors in the brief itself

**(a) The modular systole is `4 log φ`, not `2 log φ`.** `[COMPUTED]` The brief's
E4 asserts "the shortest such geodesic, of length `2 log φ ≈ 0.9624`". A
hyperbolic `γ ∈ SL₂(ℤ)` with larger eigenvalue `λ` translates by `ℓ = 2 log λ`,
and `λ + λ⁻¹ = |tr γ|` with `|tr γ| ≥ 3` an integer; `|tr γ| = 3` gives
`λ = (3+√5)/2 = φ²` and

    ℓ = 2 log φ² = 4 log φ = 2 arccosh(3/2) = 1.9248473002384137899…

The brief's number, `2 log φ = arccosh(3/2) = 0.9624236501…`, is exactly half of
this. The error has a specific arithmetic source worth naming: the geodesic
length is `2 log ε⁺_D` in the **narrow** (totally positive) fundamental unit, and
`N(φ) = −1`, so `ε⁺_5 = φ² ≠ φ`. Substituting the wide unit into a formula that
calls for the narrow one loses exactly a factor 2. Corroboration of the
normalisation: the prime geodesic theorem for SL₂(ℤ) is stated as counting
primitive hyperbolic classes with *larger eigenvalue* `< x`, asymptotically
`li(x²)` (Hashimoto arXiv:1003.3716 §1) — i.e. length `< 2 log x`.

**(b) Sarnak's theorem is about the narrow class number and the narrow unit.**
`[CLASSICAL]` The brief states S1 without this qualification. The source is
explicit: *"let h(D) be the class number of D in the narrow sense … ε(D) is the
fundamental unit of D in the narrow sense"* (Hashimoto arXiv:1003.3716 §1). This
matters here, because ordering by `ε⁺_D` is genuinely a different ordering from
ordering by `ε_D`: they differ by a square exactly on the fields with
`N(ε_D) = −1`. This study therefore computes **both** orderings separately
(`preregistration.md` §2). It does not matter for the Cohen–Lenstra comparison
itself, since for odd p the narrow and wide class groups have the same Sylow
p-subgroup.

### 3.1 H1 — "ℚ(√5) is distinguished by its position in the Cohen–Lenstra distribution" — REFUTED

Two independent refutations.

**Categorical.** Cohen–Lenstra is a probability measure on isomorphism classes of
finite abelian p-groups, describing a limiting frequency over an infinite family.
A single field is one member of that family and carries limiting frequency zero.
There is no operation "position of a field in the distribution": the measure's
arguments are groups, not fields. To make H1 even type-check one must read it as
"the CL probability of ℚ(√5)'s class group", which is the next refutation.

**Quantitative, granting the charitable reading.** `[COMPUTED]` `Cl(ℚ(√5))` is
trivial. Under the real-quadratic measure `μ^r_CL`, the trivial group is the most
probable outcome for every p — `P = 0.8402, 0.9504, 0.9763, 0.9909` for
p = 3, 5, 7, 11 respectively (`analysis/cl.py`). So ℚ(√5) sits exactly at the
**mode** of the distribution. Under the charitable reading, H1 asserts that being
the single most typical possible value is distinguishing. It is the opposite.

Moreover the value is not even locally unique: `[COMPUTED]` the smallest positive
fundamental discriminant with `h > 1` is D = 40, so the **first eleven** real
quadratic fields (D = 5, 8, 12, 13, 17, 21, 24, 28, 29, 33, 37) all have trivial
class group and are indistinguishable from ℚ(√5) by any class-group statistic.

### 3.2 H2 — "Landesman–Levy says something about an individual field" — REFUTED

The theorem, quoted verbatim in `literature.md`, is

    lim_{n→∞, n≡i (2)}  Σ_{K ∈ MH_{n,q}} |Surj(Cl(O_K), H)| / Σ_{K ∈ MH_{n,q}} 1
      = 1 (i=1),   1/|H| (i=0)

for `H` finite abelian of odd order, `q` an odd prime power with
`gcd(|H|, q(q−1)) = 1`, and `q > C(H)`.

Four independent reasons it cannot constrain any individual field, in increasing
order of decisiveness:

1. **Wrong category of field.** `MH_{n,q}` consists of function fields of
   hyperelliptic curves over `𝔽_q`. ℚ(√5) is a number field. The paper states no
   transfer to number fields, and none is known.
2. **Wrong ordering.** The family is ordered by the degree `n` of the defining
   polynomial — what the paper calls the log discriminant degree (Remark 1.1.4).
   This is a discriminant ordering, not a regulator ordering.
3. **Large-`q` hypothesis.** The conclusion holds only for `q > C(H)`, so it says
   nothing at all about any fixed small `q`, let alone about ℚ.
4. **A limit of averages is blind to any finite set.** This is decisive and needs
   no reference to the specifics. The statement is a limit of a ratio whose
   denominator `Σ_{K ∈ MH_{n,q}} 1 → ∞`. Alter `Cl(O_K)` arbitrarily for any
   finite set of `K` — or delete them — and both sums change by `O(1)` while the
   denominator diverges, so the limit is unchanged. No individual field can be
   constrained by a statement that is invariant under changing it.

The paper is also explicit about what it does not prove (Remark 1.1.2, quoted in
`literature.md`): it does **not** establish the Cohen–Lenstra heuristics, only
finitely many moments for `H` small relative to `q`.

So S3 in the brief ("Landesman–Levy does not reach the number field ℚ(√5)"),
which I was asked to try to refute, **survives**: I could not refute it, and
reasons 1–4 above are the argument that it is correct.

### 3.3 H3 / K1a — "`h(ℚ(√5)) = 1` is evidence of anything" — REFUTED

`[COMPUTED]` The Minkowski bound for a real quadratic field of discriminant D is
`√D/2`. If `√D/2 < 2` then no prime ideal of norm ≥ 2 need be considered and
`h = 1` follows from the bound alone. `√D/2 < 2 ⟺ D < 16`. The complete set of
positive fundamental discriminants with `D < 16` (task K1.a):

| D | field | Minkowski bound | h |
|---|---|---|---|
| **5** | ℚ(√5) | 1.11803 | 1 |
| **8** | ℚ(√2) | 1.41421 | 1 |
| **12** | ℚ(√3) | 1.73205 | 1 |
| **13** | ℚ(√13) | 1.80278 | 1 |

**Four** fields, not one. Their class numbers are equal and forced, so `h = 1`
separates none of them, and any argument that leans on `h(ℚ(√5)) = 1` for
distinguishing purposes is refuted. The first discriminant whose Minkowski bound
reaches 2 is D = 17 (which also has h = 1, though now for a reason requiring an
actual computation); the first with `h > 1` is D = 40.

**Consequence for the sponsoring framework, stated explicitly as required.** A
claim of the form *"ℚ(√5) has unique minimal absolute discriminant among
class-number-one real quadratic fields"* is true but empty: 5 is the minimal real
quadratic fundamental discriminant outright, and the class-number-one qualifier
excludes nothing because every competitor below 17 has h = 1 for free. The
qualifier makes a statement about the ordering of discriminants look like a
theorem about class groups. The correct statement is E1, with the qualifier
deleted.

### 3.4 H4 — "first term of Sarnak's asymptotic" — REFUTED, but the refutation has content

H4 is the one the brief expected to be interesting. It is refutable, and the
refutation is worth stating precisely because it isolates what is real here.

**The refutation.** Sarnak's theorem is
`Σ_{D>0, ε(D)<x} h(D) log ε(D) ~ x²/2`, a statement about a limit as `x → ∞`.
Delete `D = 5` from the family, or replace `h(5)` by any other value: the left
side changes by a bounded amount, and the asymptotic is unchanged. An asymptotic
law is invariant under modification of any finite initial segment, so it cannot
confer a property on any member of that segment. In fact an asymptotic law has no
"first term" at all — it is a statement about a limit, not a series with an
indexed leading term. H4 attributes to the *theorem* what belongs to the
*ordering*.

**Does that fully dispose of it?** Not quite, and the residue is worth naming.
The ordering does have a least element, and identifying it is a genuine fact:

* `[COMPUTED]` the counting function `π(x) = #{primitive hyperbolic classes with
  larger eigenvalue < x}`, whose asymptotic is `li(x²)`, is identically 0 for
  `x ≤ φ²` and jumps to 1 at `x = φ²`. So ℚ(√5) does determine where the support
  of the counting function begins.

But that statement *is* E2/E4 — smallest regulator, shortest geodesic — restated.
It is classical, it is proved in `EXTREMALITY_NOTE.md` in four lines, and it owes
nothing to Sarnak. The correct decomposition is:

* **the ordering** has a minimum, and the minimum is ℚ(√5) — real, classical, E2;
* **the asymptotic law** confers nothing on the minimum — H4, refuted.

Anything that feels like content in H4 is E2 wearing a borrowed coat. This is the
same defect as K1a: a true elementary statement dressed in the vocabulary of a
deeper theorem so that it sounds like a consequence of it.

### 3.5 H5 — "moduli-space topology in both is a link" — REFUTED

**What would have to be true**, stated before checking:

1. *A correspondence of moduli problems* — the modular surface would have to
   arise as (or map to/from) a Hurwitz space in a way that carries the arithmetic
   content of both theorems; or
2. *A transfer of counts* — Sarnak's regulator-ordered geodesic count would have
   to be an instance of, or deducible from, the Hurwitz-space point count, or
   conversely; or
3. *A dictionary of orderings* — since Landesman–Levy order by degree
   (discriminant) and Sarnak orders by regulator, a link would need a translation
   between the two orderings.

**What is actually the case.**

*On (1) — and this is the one genuine connection, which is why it is worth being
precise about.* Landesman–Levy's family `MH_{n,q}` consists of hyperelliptic
curves `y² = f(x)`, i.e. double covers of `P¹` branched at `n` points — which is
literally a Hurwitz space for `ℤ/2`. For `n = 4` these are elliptic curves, and
the coarse moduli space of elliptic curves is `Y(1) = ℍ/PSL₂(ℤ)`, the modular
surface. So the two spaces do meet. But the meeting point is inert for both
theorems: Landesman–Levy's statement is a limit as `n → ∞`, so `n = 4`
contributes nothing to it; and Sarnak does not use the modular surface as a
moduli space of elliptic curves at all — he uses it as a hyperbolic orbifold, via
the correspondence between its closed geodesics and classes of indefinite binary
quadratic forms. The elliptic-curve interpretation of `Y(1)` plays no role in the
prime geodesic theorem. A shared object used for two unrelated purposes is not a
link between the purposes.

*On (2).* The mechanisms are different in kind. Sarnak's count is a dynamical one:
the Selberg trace formula and the prime geodesic theorem, governed by the length
spectrum and the spectrum of the Laplacian. Landesman–Levy's count is a
cohomological one: stable rational homology of Hurwitz spaces plus the
Grothendieck–Lefschetz trace formula over `𝔽_q`, governed by Frobenius
eigenvalues. Neither count is stated in terms of the other, and no transfer
appears in either paper or in anything found in the search (`literature.md` §3).

*On (3).* No such dictionary exists in the literature searched. The regulator
does have a function-field avatar — the order of `[∞₁ − ∞₂]` in `Pic⁰`
(Wood, arXiv:1710.01350 §1) — but Landesman–Levy do not order by it, and I found
no paper that does.

**Verdict.** What both theorems share is a *technique class*: "compute the
topology of a moduli space, deduce an arithmetic count". That is a resemblance at
the level of method, and it is a real and important one in modern arithmetic
statistics — but it relates the two proofs the way "both use Fourier analysis"
relates two analytic number theory papers. It is not a mathematical link between
the objects, and it transfers no statement from one setting to the other.

### 3.6 Refutation attempts against my own primary result

The primary result (§4) is that the regulator-ordered p-part distribution
follows the **imaginary** Cohen–Lenstra measure. Here is every attempt I made to
destroy it. Outcomes are in §4.1-§4.6; the attempts are listed here so that the list is
visible independently of whether they succeeded. **None of the eight overturned
the result**; attacks 1, 2 and 5 each had a clear chance to and did not.

1. **"The pipeline is wrong."** Attack: run the same code on a family whose
   answer is a theorem. The discriminant-ordered channel must reproduce
   Davenport–Heilbronn's `4/3`. → §4.1.
2. **"It is a D-size effect, not a regulator effect."** The regulator-ordered
   sample reaches `D ~ 4·10^12` while the discriminant-ordered one stops at
   `10^7`, so the two differ in D-scale as well as in ordering. Attack: generate
   a third dataset — 250 000 consecutive fundamental discriminants at `D ~ 10^12`,
   discriminant-ordered, no regulator condition — and see which of the two it
   matches (`data/gen_disc_window.gp`). → §4.3.
3. **"It is a truncation artefact."** Attack: the pre-registered convergence
   test. If the discrepancy from `μ_CL` shrinks as the bound grows, the limit is
   `μ_CL`; if it is stable or grows, it is not. → §4.2.
4. **"`quadclassunit` is wrong at large D with huge class numbers."** The
   regulator-ordered population has mean `h ≈ 51 000` at `t ~ 2·10^6`, far
   outside the regime where class-group tabulations are usually checked, and the
   computation is GRH-conditional. Attack: recompute a sample with
   `bnfinit` + `bnfcertify`, which is unconditional. → §4.4.
5. **"It is really `P(p | h) ≈ 1/p`, i.e. nothing but h being large."** If the
   only effect were that the regulator ordering makes `h` enormous, the natural
   null would be the naive divisibility value `1 − 1/p`, not the Cohen–Lenstra
   value `∏_{k≥1}(1 − p^{−k})`. These differ substantially (for p = 3: 0.6667 vs
   0.5601). Attack: check which one the data converges to. → §4.5.
6. **"It is the thin polynomial family `D = t² ± 4`, not the regulator."**
   Attack: split the sample by `u` (the index in `t² − 4s = D u²`) and by
   `N(ε_D)`, and check whether the sub-populations agree. → §4.5. But note the
   structural point in §4.6: this dichotomy is not a real one, because "small
   regulator" and "`u²D` within 4 of a perfect square" are the *same condition*.
7. **"Genus theory."** Excluded by construction (odd p only), and checked by
   restricting to prime D, where the genus group is trivial. → §4.5.
8. **"Someone has already done this."** Attack: the priority search in
   `literature.md` §3, plus a second search run after the result was known and
   its statement was therefore searchable. → §4.6.

---

## 4. The primary question: regulator-ordered p-part distribution

All numbers `[COMPUTED]` by `analysis/compare.py` from
`data/quadratic_fields.sqlite`, built by `analysis/build_db.py` from the three
enumerations in `data/`. Sizes, digests and bounds are pinned in
`data/MANIFEST.md`; the summary tables every number here is read from are in
`data/summary/`. The two hypotheses, the statistics, the truncation ladder, the
bootstrap seed and the decision rules were all fixed in `preregistration.md`
before any of this was computed.

The datasets:

| dataset | ordering | n | reaches |
|---|---|---:|---|
| `disc_ordered` | by discriminant, all `0 < D ≤ 10⁷` | 3 039 653 | `D = 10⁷` |
| `reg_ordered` | by regulator, all `ε_D ≤ 2·10⁶` | 3 996 898 | `D ≈ 4·10¹²` |
| `disc_window` | by discriminant, 250 000 consecutive `D` from `10¹²` | 250 000 | `D ≈ 1.0000008·10¹²` |

### 4.1 Calibration: the pipeline reproduces Davenport–Heilbronn

Mandatory before anything else (`preregistration.md` §6). In the discriminant
ordering the answer is a theorem: the average of `#Surj(Cl, ℤ/3)` must tend to
1/3. Observed `M_3` at bounds `10⁵, 10⁶, 10⁷`:

    0.21846      0.25370      0.27960        →  1/3 = 0.33333

The deficit is `−0.11487, −0.07963, −0.05374`, shrinking by factors 1.44 and 1.48
per decade. The pre-registered expectation, written down before the computation,
was that the `X^{5/6}` secondary term in cubic field counts (Roberts;
Bhargava–Shankar–Tsimerman; Taniguchi–Thorne) makes the residual decay like
`X^{-1/6}`, i.e. by a factor `10^{1/6} = 1.468` per decade. Observed 1.44 and
1.48. The same holds for p = 5, 7, 11 (ratios 1.70–2.04). Against the imaginary
measure the residual is instead flat (ratios 1.02–1.05) at a value near −0.72 to
−0.96.

**The pipeline is correct, and the discriminant ordering converges to `μ^r_CL`,
as it must.**

### 4.2 The result

Regulator ordering (`reg-wide`, ordering by `ε_D`), at the four pre-registered
bounds. `P(triv)` is the observed proportion with trivial Sylow p-subgroup:

| bound on ε | n | `M_3` | `M_5` | `M_7` | `M_11` |
|---:|---:|---:|---:|---:|---:|
| 10⁴ | 19 752 | 0.83465 | 0.87161 | 0.86574 | 0.77461 |
| 10⁵ | 199 262 | 0.92700 | 0.96000 | 0.95241 | 0.93982 |
| 10⁶ | 1 997 783 | 0.97259 | 0.98608 | 0.98548 | 0.98099 |
| 2·10⁶ | 3 996 897 | **0.98127** | **0.99091** | **0.99032** | **0.98860** |
| *predicted, `μ_CL` (imaginary)* | | *1* | *1* | *1* | *1* |
| *predicted, `μ^r_CL` (real)* | | *0.33333* | *0.20000* | *0.14286* | *0.09091* |

The pre-registered novelty test is condition 2 of `preregistration.md` §5: a
discrepancy that shrinks with the bound is a truncation artefact, not a finding.
Applying it to both hypotheses:

| | p=3 | p=5 | p=7 | p=11 |
|---|---|---|---|---|
| residual vs `μ_CL`, shrink factor per step | 2.27, 2.66, 1.46 | 3.21, 2.87, 1.53 | 2.82, 3.28, 1.50 | 3.75, 3.17, 1.67 |
| residual vs `μ^r_CL`, shrink factor per step | 0.84, 0.93, 0.99 | 0.88, 0.97, 0.99 | 0.89, 0.96, 0.99 | 0.81, 0.95, 0.99 |

The first three bounds differ by a decade each and the last by a factor 2; the
observed shrink factors against `μ_CL` are consistent with a `T^{-1/2}` law
(`10^{1/2} = 3.16`, `2^{1/2} = 1.41`). Against `μ^r_CL` every factor is `< 1`:
the discrepancy **grows**, saturating at the largest gap the statistic allows.

So by the pre-registered rule: the deviation from `μ_CL` is a truncation
artefact and may not be claimed; the deviation from `μ^r_CL` is not, and `μ^r_CL`
is excluded. **Q1 is FALSE; the data are consistent with `μ_CL`.**

**Sarnak's actual ordering gives the same answer.** Sarnak's theorem is stated
for the narrow fundamental unit (§3.0(b)), so `reg-narrow` orders by
`ε⁺_D`. At the largest bound (n = 1 998 450): `M_p = 0.96828, 0.98614, 0.98619,
0.98173`, with residuals against `μ_CL` again shrinking (factors 2.03–3.57 per
decade) and residuals against `μ^r_CL` again growing. The conclusion does not
depend on which of the two regulator orderings is used.

**A note on the literal verdict column.** The pre-registered z-test rejects *both*
hypotheses at every regulator bound and at every discriminant bound, printing
"neither" throughout, because at n ∈ [10⁶, 4·10⁶] a residual of 1% is still
tens of sigma. That rule is uninformative at these sample sizes — which is
exactly why the calibration channel was mandated, and it is why the calibration
channel prints "neither" too, at a bound where the answer is a *theorem*. The
informative pre-registered criterion is the convergence test above. Where n is
moderate enough for the z-test to be meaningful, it behaves correctly: at
n = 250 000 the `disc-window` control returns the verdict `H_real` outright for
p = 5, 7, 11 (§4.3).

### 4.3 The decisive control: it is not a D-size effect

The regulator dataset reaches `D ≈ 4·10¹²`; the discriminant dataset stops at
`10⁷`. The obvious objection is that the two differ in the size of D, not only in
the ordering. `data/gen_disc_window.gp` removes it: 250 000 consecutive
fundamental discriminants starting at `10¹²`, ordered by discriminant, with no
regulator condition — the same D-scale as the regulator-ordered population.

| | `M_3` | `M_5` | `M_7` | `M_11` |
|---|---:|---:|---:|---:|
| observed at `D ≈ 10¹²`, discriminant-ordered | 0.32631 | 0.19790 | 0.14522 | 0.09100 |
| `μ^r_CL` (real) | 0.33333 | 0.20000 | 0.14286 | 0.09091 |
| residual | −0.00702 | −0.00210 | **+0.00237** | **+0.00009** |
| `μ_CL` (imaginary) | 1 | 1 | 1 | 1 |

At the same D-scale where the regulator ordering gives ≈ 1, the discriminant
ordering gives the real-quadratic prediction to within 2.1%, 1.1%, 1.7% and 0.1%
respectively (residual as a fraction of the prediction). The formal verdict is `H_real` for p = 5, 7, 11 and "undecided" for
p = 3 at z = −4.4 — and the p = 3 residual, −0.00702, is −2.1% relative, which is
what the `X^{-1/6}` Davenport–Heilbronn secondary term predicts at `X = 10¹²`
(`10^{-2}` times the O(1) constant ≈ 2.4 fitted from §4.1, giving ≈ 2.4%).

**Q3 is FALSE.** D-size is not the operative variable; the regulator condition is.

### 4.4 GRH and computational correctness

`quadclassunit` uses Bach's bound and is conditional on GRH. `data/grh_spotcheck.gp`
recomputes samples with `bnfinit` + `bnfcertify`, which is unconditional:

* 265 discriminants across `D ~ 10¹ … 10⁶` plus `D = t²−4` near `t = 10⁵`:
  **0 mismatches, 0 certification failures**;
* an extended check over the whole `t` range actually used — `t ~ 10², 10³, 10⁴,
  10⁵, 5·10⁵, 10⁶, 2·10⁶`, 60 discriminants each, 420 total, with mean class
  number rising from 9.5 to **51 027**: **0 mismatches, 0 certification failures**.

This is a spot check, not a proof that all 7.3 million class groups are
unconditional; certifying them all costs far more than computing them. The honest
description of the datasets is *GRH-conditional, spot-checked unconditionally on
420 fields spanning the full range, including the large-class-number regime where
a failure would matter most*.

Independently, `analysis/build_db.py` rejects any row where `h` differs from the
product of the invariant factors, or where `t² − 4s` is not `D` times a perfect
square. All 7 286 551 rows passed.

### 4.5 Confounders

All at the largest regulator bound, n = 3 996 897 (`preregistration.md` §6).

**(1) Thinness / the algebraic family.** 57.80% of the sample has `u = 1`
(i.e. `D = t² ± 4` exactly), 42.20% has `u > 1`.

| | `M_3` | `M_5` | `M_7` | `M_11` | n |
|---|---:|---:|---:|---:|---:|
| `u = 1` | **1.00083** | 0.99519 | 0.99610 | 0.99656 | 2 310 188 |
| `u > 1` | 0.95449 | 0.98504 | 0.98240 | 0.97769 | 1 686 709 |

The two sub-populations do differ, which by the letter of my own pre-registered
criterion means the effect cannot be cleanly attributed to "the regulator
ordering as such" rather than to the family. But the difference is one of degree,
not of kind: both are near 1 and neither is remotely near `1/p`. And the `u = 1`
sub-population — 2.3 million fields — agrees with `μ_CL` to
`M_3 = 1.00083` against a predicted 1, which at SE ≈ 0.0016 is **0.5σ**.
See §4.6 for why the "family vs regulator" dichotomy is not a real one.

**(2) The `hR = √D·L` bias.** Mean `h = 1.963·10⁴`, median `1.406·10⁴`; mean
`L(1,χ_D) = 0.8396`. Split by class-number quartile, `M_3` = 0.94045, 0.98488,
0.99972, 1.00004 — the agreement with `μ_CL` is *better* for larger h, i.e. the
residual is concentrated in the small-h (less extremal) tail, not created by it.

**(3) Genus theory.** Odd p only by construction. Restricting further to
D prime (n = 183 386), where the genus group is trivial: `M_p` = 1.00783,
1.00479, 0.99400, 0.99391 — all consistent with 1.

**(4) Norm of the fundamental unit.** `N(ε_D) = −1` for 50.03% of the sample.
`M_3` = 0.99409 (`N = −1`) versus 0.96844 (`N = +1`); both near 1.

**(5) "It is just `P(p ∣ h) ≈ 1/p` because h is huge."** This is the sharpest
alternative, and it is cleanly excluded, because Cohen–Lenstra's prediction is
*not* the naive one — that was Cohen and Lenstra's original observation. Observed
proportion of the sample with `p ∣ h`, against three nulls:

| p | observed (reg) | `μ_CL` (imaginary) | `μ^r_CL` (real) | naive `1/p` |
|---|---:|---:|---:|---:|
| 3 | **0.43497** | 0.43987 | 0.15981 | 0.33333 |
| 5 | **0.23787** | 0.23967 | 0.04958 | 0.20000 |
| 7 | **0.16178** | 0.16320 | 0.02374 | 0.14286 |
| 11 | **0.09807** | 0.09917 | 0.00908 | 0.09091 |

and for the `D ≈ 10¹²` discriminant-ordered control: 0.15675, 0.04916, 0.02415,
0.00906 — matching the *real* column.

The observation exceeds the naive value by 30% at p = 3 and by 19% at p = 5,
whereas it differs from the imaginary Cohen–Lenstra value by 1.1% and 0.8%. **Q4 is FALSE.** It is specifically
Cohen–Lenstra, not divisibility of a large random integer.

There is a pleasing way to say this. Ellenberg's survey opens by quoting
Cohen and Lenstra's own founding observation: *"If p is a small odd prime, the
proportion of imaginary quadratic fields whose class number is divisible by p
seems to be significantly greater than 1/p (for instance 43% for p = 3, 23.5% for
p = 5)."* The regulator-ordered **real** quadratic fields give 43.50% and 23.79%.

**(6) Post-hoc mechanism probe (not pre-registered, labelled as such).** Let
`ρ := 2R/log D`. Since `ε_D ≥ (1+√D)/2` forces `R ≥ log√D − log 2`, `ρ ≈ 1` is
the *floor* of the regulator range and larger `ρ` means a less extreme field.
Split by `ρ` quartile (edges 1.0000, 1.0000, 1.0844; range 0.5980–5.2214):

| p | `ρ` q1 (floor) | q2 | q3 | q4 (least extreme) |
|---|---:|---:|---:|---:|
| 3 | **1.00641** | 1.00185 | 0.98161 | 0.93521 |
| 5 | 0.99721 | 0.99747 | 0.99086 | 0.97810 |
| 7 | 0.99588 | 0.99731 | 0.99273 | 0.97534 |
| 11 | 0.99887 | 0.99641 | 0.99270 | 0.96641 |

`M_p` decreases monotonically as the regulator becomes less extremal, for every
p, and at the floor it sits on `μ_CL` essentially exactly. This is the signature
the mechanism of §4.7 predicts, and it also explains the `u = 1` vs `u > 1` gap
in confounder (1): `u = 1` forces `ρ ≈ 1`, while `u > 1` gives
`ρ = log t/(log t − log u) > 1`, so `u` is a proxy for `ρ`.

### 4.6a Higher moments (added after the pre-registered analysis; confirmatory)

**Not pre-registered.** `preregistration.md` fixed three statistics, all built on
`H = ℤ/p`. This section adds `H = ℤ/p²` and `H = (ℤ/p)²`, run afterwards on the
same data by `analysis/moments2.py`. They are reported as confirmation rather
than as a search, for a specific reason: the predictions are fixed by theory
before looking and admit no tuning — `E[#Surj(Cl,H)] = 1` under `μ_CL` and
`1/|H|` under `μ^r_CL`, for *every* `H`. All six predictions are checked in
`analysis/cl.py::selftest`. Wood–Wood (quoted in Landesman–Levy §1) show the
Cohen–Lenstra distribution is determined by its moments, so agreement across
several `H` is qualitatively stronger evidence than agreement on one; and for the
two groups of order `p²` the two hypotheses differ by a factor `p²` rather than
`p`, making them sharper discriminations as well as independent ones.

Regulator ordering at the largest bound, n = 3 996 897:

| p | H | \|H\| | observed | `μ_CL` = 1 | `μ^r_CL` = 1/\|H\| | z vs `μ_CL` | z vs `μ^r_CL` |
|---|---|---:|---:|---:|---:|---:|---:|
| 3 | ℤ/3 | 3 | 0.98127 | 1 | 0.33333 | −27.0 | +935.4 |
| 3 | ℤ/9 | 9 | 0.97740 | 1 | 0.11111 | −16.4 | +628.6 |
| 3 | (ℤ/3)² | 9 | 0.91827 | 1 | 0.11111 | −20.1 | +198.2 |
| 5 | ℤ/5 | 5 | 0.99091 | 1 | 0.20000 | −9.2 | +797.2 |
| 5 | ℤ/25 | 25 | 0.97678 | 1 | 0.04000 | −9.6 | +386.6 |
| 5 | (ℤ/5)² | 25 | 0.95246 | 1 | 0.04000 | −4.0 | +76.8 |
| 7 | ℤ/7 | 7 | 0.99032 | 1 | 0.14286 | −8.0 | +697.3 |
| 7 | ℤ/49 | 49 | 0.95974 | 1 | 0.02041 | −12.1 | +281.4 |
| 7 | (ℤ/7)² | 49 | 0.94220 | 1 | 0.02041 | −2.7 | +42.3 |
| 11 | ℤ/11 | 11 | 0.98860 | 1 | 0.09091 | −7.3 | +571.6 |
| 11 | ℤ/121 | 121 | 0.91269 | 1 | 0.00826 | −17.1 | +176.8 |
| 11 | (ℤ/11)² | 121 | 0.94784 | 1 | 0.00826 | −0.9 | +16.8 |

Every one of the twelve sits near 1 and nowhere near `1/|H|`; `μ^r_CL` is
excluded at z between 17 and 935. And the pre-registered convergence criterion,
applied to all twelve, gives the same answer as it did for the first moment —
**all twelve residuals against `μ_CL` shrink monotonically** across bounds
`10⁵ → 10⁶ → 2·10⁶`, with shrink factors 2.2–3.6 per decade and 1.46–1.90 per
doubling, against the `T^{-1/2}` reference values 3.16 and 1.41:

| p | H | resid @10⁵ | @10⁶ | @2·10⁶ | ratios |
|---|---|---:|---:|---:|---|
| 3 | ℤ/9 | −0.10540 | −0.03461 | −0.02260 | 3.05, 1.53 |
| 3 | (ℤ/3)² | −0.28769 | −0.11930 | −0.08173 | 2.41, 1.46 |
| 5 | ℤ/25 | −0.13009 | −0.03626 | −0.02322 | 3.59, 1.56 |
| 5 | (ℤ/5)² | −0.20266 | −0.09035 | −0.04754 | 2.24, 1.90 |
| 7 | ℤ/49 | −0.20811 | −0.06478 | −0.04026 | 3.21, 1.61 |
| 7 | (ℤ/7)² | −0.15014 | −0.10794 | −0.05780 | 1.39, 1.87 |
| 11 | ℤ/121 | −0.36737 | −0.13070 | −0.08731 | 2.81, 1.50 |
| 11 | (ℤ/11)² | −0.13882 | −0.09480 | −0.05216 | 1.46, 1.82 |

`reg-narrow` (Sarnak's own ordering, by `ε⁺_D`) gives the same twelve-for-twelve
picture. The discriminant-ordered channel and the `D ≈ 10¹²` control both go the
other way, to `1/|H|`, as they must.

**Honest caveat.** `#Surj(A,H)` grows like `p^{2·rank}`, so these estimators have
heavy tails and their standard errors are dominated by rare high-rank fields. At
the smaller bounds the `(ℤ/p)²` rows for p = 7, 11 rest on fewer than 200
rank-≥2 fields and are flagged `<-- thin` in the script output; they are reported
for completeness, not as precise. The p = 3 and p = 5 rows, and all rows at the
largest bound, rest on thousands to tens of thousands.

### 4.6 Interpretation, and what this is not

**"Small regulator" and "D near a square" are the same condition, not two.**
`ε_D ≤ T` means `t² − Du² = ±4` with `t ≤ T + 1`, i.e. `u²D` lies within 4 of a
perfect square. There is no way to separate "the regulator ordering" from "the
family `D = (t² ∓ 4)/u²`", because they are logically equivalent — a real
quadratic field whose maximal order is generated by a unit is precisely one of
narrow Richaud–Degert type (arXiv:2512.11311, abstract). So confounder (1) above
cannot be "ruled out" in the sense of separating two causes; there is one
condition with two descriptions. What confounder (6) shows is that the operative
variable within that family is *how extremal the regulator is*, which is the
regulator-side description.

**The ordering is extremely thin.** `#{D : ε_D ≤ T} ≈ 2T` `[COMPUTED]`: the ratio
`#/T` is 1.9160, 1.9753, 1.9926, 1.9984 at `T = 10³, 10⁴, 10⁵, 2·10⁶`. Among
discriminants up to `T²` this is a set of density `≈ 2/T → 0`. Any statement here
is about a density-zero family, and carries no implication for the discriminant
ordering.

**Was it already known?** Two search rounds, the second run after the result was
known and therefore searchable (`literature.md` §3). No source states, conjectures
or tests this. The nearest work:

* **Lamzouri** (arXiv:1609.01630) proves that in the regulator ordering the tail
  of large `h(d)` "has the same shape as that of class numbers of imaginary
  quadratic fields ordered by the size of their discriminants" — the same
  imaginary-like behaviour, but for the *size* of `h`, not the structure of `Cl`.
* **Dousselin** (arXiv:2408.01401), same delineation, for `ε_d ≤ d^{1/2+α}`.
* **arXiv:2512.11311** studies exactly the discriminants `n² ∓ 4`, but the class
  groups of the *orders* `ℤ[ε]`, and only class-number size and the 2-part.
* **Bartel–Johnston–Lenstra** (arXiv:2005.11533) supply the right framework — the
  Arakelov class group, "for number fields it plays the rôle that the Jacobian of
  a curve plays for function fields", with `Cl` as component group and the
  regulator as identity component — but do not order by regulator.

**Relation to what is known about orderings.** That the ordering can change a
Cohen–Lenstra answer is *not* new: Bartel–Lenstra (2020) produced counterexamples
to Cohen–Lenstra–Martinet in the discriminant ordering, and the mechanism there is
subfield contamination (Ellenberg, Bourbaki 1251). That mechanism is unavailable
for quadratic `K/ℚ`, which has no intermediate field. Sawin–Wood
(arXiv:2301.00791) Remark 1.3 writes: *"We certainly imagine the conjecture only
holding for orderings such that the proportion of fields in E containing any
fixed field K₁ ⊄ K₀ is 0."* **That is a necessary condition, not a sufficient
one** — Ellenberg's survey paraphrases it as the stronger converse ("any natural
ordering will do as long as…"). The regulator ordering satisfies the condition
vacuously and still, numerically, changes the answer. So the present observation
is evidence that a subfield criterion alone cannot characterise the good
orderings; it is **not** a counterexample to Sawin–Wood as written, and their
Conjecture 1.1 concerns a different family anyway.

### 4.7 The conjecture, and why there is no `THEOREM_STATEMENT.md`

`[CONJECTURAL]` — stated as a question, with no proof, per the anti-fabrication
protocol:

> **Question.** Let `p` be an odd prime. As `T → ∞`, does the Sylow p-subgroup of
> `Cl(ℚ(√D))`, taken over the real quadratic fields with `ε_D ≤ T` ordered by
> `ε_D`, become distributed according to the *imaginary* quadratic Cohen–Lenstra
> measure `μ_CL(A) = |Aut A|^{-1} ∏_{k≥1}(1 − p^{-k})`, rather than the
> real-quadratic `μ^r_CL`? The data above are consistent with yes, with residuals
> decaying roughly like `T^{-1/2}`.

`[CONJECTURAL]` **Why one should expect it, in a few lines.** Cohen and Lenstra
record an observation credited to Gross (quoted in Ellenberg, Bourbaki 1251):
for `K` real quadratic, `O_K` behaves like `O_L[1/π]` with `L` imaginary
quadratic and `π` a prime above a split `p`, both rings having two "missing"
places; and `Cl(O_L[1/π]) = Cl_L/⟨π⟩`. That is exactly why `Cl_K` is modelled as
a random group **modulo a random element**, which is what produces the `1/|A|`
factor. In that dictionary the regulator corresponds to the *order* of the
element being quotiented by. Ordering by regulator and truncating conditions that
element to have small order; in the limit the quotient does nothing and `μ_CL` is
recovered. The function-field form is the same statement with
`Cl(O_K) = Pic⁰(C_K)/⟨∞₁−∞₂⟩` and the regulator equal to the order of
`[∞₁−∞₂]`.

This is a heuristic, not a derivation, and it has a visible gap: the number-field
regulator `log ε_D` is a real number with no p-part, so "the order of the
quotiented element is prime to p" has no literal number-field meaning. Closing
that gap is what a proof would have to do.

**No `THEOREM_STATEMENT.md` is created.** The brief specifies that that file
requires a full statement *and a full proof*. I have a numerical result over
7.3 million fields with five controls, and a heuristic that predicts it. That is
not a theorem, and writing it into a theorem environment is precisely the failure
mode the brief warns against. Verdict `NOVEL` on row Q2 attaches to the empirical
observation and to nothing more; my honest expectation is that it is folklore
among people who think about Arakelov class groups, rather than new.

---

## 5. What would change the verdict

**E1, E2, E3** — settled. E1 and E2 have complete elementary proofs in
`EXTREMALITY_NOTE.md`; E3 is Hurwitz's theorem. Nothing short of an error in
those proofs would change them.

**E4** — settled, given the standard normalisation `ℓ = 2 log λ` for the
translation length of a hyperbolic isometry with larger eigenvalue `λ`. What
would change the verdict on E4′ (the brief's version): a primary source using a
convention in which the translation length is `log λ` rather than `2 log λ`.
I did not find one, and the prime geodesic theorem's `li(x²)` normalisation is
inconsistent with such a convention — under `ℓ = log λ` the geodesic counting
function would be `li(e^{2ℓ})`, i.e. topological entropy 2, which is wrong for a
hyperbolic surface of curvature −1.

**K1, K1a, H1, H3** — settled by finite computation. To change them one would
have to produce a positive fundamental discriminant `D < 16` other than
5, 8, 12, 13, or exhibit a class-group statistic separating those four fields.
Neither exists.

**H2** — settled. Would change only if someone proved a transfer of
Landesman–Levy to number fields *and* a statement about individual members of the
family. The second is impossible for a limit of averages (§3.2, reason 4).

**H4** — settled as stated. The residue that survives (that the ordering has a
least element, and it is ℚ(√5)) is E2/E4 and is already proved.

**H5** — the verdict would change if someone exhibited (i) a correspondence
carrying Sarnak's geodesic count to a Hurwitz-space point count or conversely,
or (ii) a Hurwitz-space model for the *regulator* ordering, i.e. a moduli
interpretation of ordering real quadratic function fields by the order of
`[∞₁ − ∞₂]` in `Pic⁰`. (ii) is a well-posed and, as far as I can tell,
unaddressed question; it is the one place in H5 where something could be built.

**Q1, Q3, Q4** — settled numerically, with the controls in §4.3–§4.5. Q1 would
change only if the residual against `μ^r_CL` began to shrink at larger bounds; it
grows at every bound tested and is already within 3% of the largest gap the
statistic permits.

**Q2 — the only genuinely open item.** What would resolve it, in increasing order
of difficulty:

1. *Push the truncation.* `T = 10⁷` would give ≈ 2·10⁷ fields with `D ≈ 10¹⁴`
   and, on the observed `T^{-1/2}` trend, a residual of about 0.008 for p = 3. If
   the residual instead stalls, the limit is not `μ_CL` and Q2 is FALSE. This is
   the cheapest decisive test: it is the same script with `TMAX` changed, and the
   cost is roughly 15 core-hours.
2. *Test a second moment.* This study tests `E[#Surj(Cl, ℤ/p)]` and the
   isomorphism-type distribution up to order `p³`. The `H = (ℤ/p)²` moment
   (predicted `1` under `μ_CL`, `p^{-3}`… under `μ^r_CL`) would discriminate
   again and independently. Wood–Wood guarantees the moments determine the
   distribution, so agreement across a range of `H` is the strongest available
   numerical evidence short of proof.
3. *Close the heuristic's gap.* Give the number-field regulator a p-adic
   avatar — presumably via the Arakelov class group (Bartel–Johnston–Lenstra),
   where `Cl_F` is the component group and the regulator the covolume of the
   identity component — so that "the quotiented element has order prime to p"
   becomes a statement one can condition on. This is what would turn the
   heuristic of §4.7 into a conjecture with a mechanism.
4. *Prove it in the function field setting*, where the regulator genuinely is
   the integer `ord([∞₁−∞₂])` and "prime to p" is literal. The Landesman–Levy
   machinery computes moments for `MH_{n,q}` ordered by degree; the question is
   whether a Hurwitz-space model exists for the regulator ordering. That is also
   the one place where H5 could become true (§5, H5), which is a reason to think
   the two loose ends are the same loose end.
