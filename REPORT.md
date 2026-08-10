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
| Q | Under regulator ordering, does the p-part of `Cl` (odd p) follow Cohen–Lenstra? | *(see §4)* | `[COMPUTED]` | `analysis/compare.py`, `preregistration.md` |
| S1 | Sarnak's asymptotic `Σ_{ε(D)<x} h(D) ~ li(x²)` | **KNOWN** (true, and stated for the **narrow** class number and **narrow** unit) | `[CLASSICAL]` | verbatim in Hashimoto arXiv:1003.3716 §1 eqns (1.2)–(1.3) |
| S3 | Landesman–Levy does not reach ℚ(√5) | **KNOWN** (true) | `[CLASSICAL]` | §3.2 |

---

## 2. Headline

*(filled in §4)*

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
destroy it. Outcomes are in §4.5; the attempts are listed here so that the list
is visible independently of whether they succeeded.

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

*(filled in below)*

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

**Q1 / Q2 (the primary question)** — see §4.6.
