# Literature record

Every source searched, fetched, and read for this study, with near-misses called
out. Primary sources only: no news articles, blog posts, or secondary summaries
are used for mathematical content. Where a source could not be obtained, that is
stated rather than papered over.

Tags follow the anti-fabrication protocol: `[READ]` = full text obtained and the
relevant statement extracted; `[ABSTRACT]` = only the abstract obtained;
`[CITED-ONLY]` = bibliographic data verified but text not obtained.

---

## 1. Sources read, with the statements extracted

### Sarnak, *Class numbers of indefinite binary quadratic forms* `[CITED-ONLY → statement READ via Hashimoto]`

> P. Sarnak, J. Number Theory **15** (1982), no. 2, 229–247.
> Sequel: *Class numbers of indefinite binary quadratic forms II*,
> J. Number Theory **21** (1985), no. 3, 333–346.

The journal text is behind ScienceDirect (HTTP 403 from this environment;
attempt recorded in §4). The theorem statement was instead obtained verbatim
from a primary research paper that quotes it in displayed form:

> Y. Hashimoto, *Asymptotic formulas for class number sums of indefinite binary
> quadratic forms in arithmetic progressions*, arXiv:1003.3716, §1, eqns (1.2),
> (1.3) `[READ]`:
>
> "For an integer D, let h(D) be the class number of D **in the narrow sense**.
> … On the other hand, Sarnak [Sa1] obtained the following asymptotic formula.
>
>     sum_{D>0, eps(D)<x} h(D) log eps(D) ~ (1/2) x^2   as x → ∞.       (1.2)
>
> This yields that
>
>     sum_{D>0, eps(D)<x} h(D) ~ li(x^2)   as x → ∞,                    (1.3)
>
> where li(x) := int_2^x (log t)^{-1} dt."

Also quoted there, and used in this study for the geodesic normalisation:

> "#{[γ]: the primitive hyperbolic conjugacy classes of SL2(Z), the larger
> eigenvalue of γ is less than x} ~ li(x²) as x → ∞"

**Two things this pins down that the sponsoring brief did not state.**
(i) Sarnak's `h(D)` is the **narrow** class number and his `eps(D)` is the
**narrow** fundamental unit — so "the regulator ordering" means ordering by
`eps⁺_D`, not by `eps_D`. This study therefore reports both orderings separately
(`preregistration.md` §2). (ii) The prime geodesic theorem is normalised by the
*larger eigenvalue* λ, and geodesic length is `2 log λ` — which is what makes the
modular systole `4 log φ` and not `2 log φ` (`EXTREMALITY_NOTE.md` E4).

### Landesman & Levy, *The Cohen–Lenstra moments over function fields via the stable homology of non-splitting Hurwitz spaces* `[READ]`

> A. Landesman and I. Levy, arXiv:2410.22210v2 (3 March 2025).
> MSC 11R29 primary. Obtained as PDF and read directly.

Abstract, verbatim: *"We compute the average number of surjections from class
groups of quadratic function fields over 𝔽_q(t) onto finite odd order groups H,
once q is sufficiently large. These yield the first known moments of these class
groups, as predicted by the Cohen–Lenstra heuristics, apart from the case
H = ℤ/3ℤ. The key input to this result is a topological one, where we compute the
stable rational homology groups of Hurwitz spaces associated to non-splitting
conjugacy classes."*

Theorem 1.1.1, verbatim: *"Suppose H is a finite abelian group of odd order. Let
q be an odd prime power with gcd(|H|, q(q−1)) = 1. There is an integer C,
depending only on H, so that if q > C and i ∈ {0,1},*

    lim_{n→∞, n ≡ i mod 2}  [ Σ_{K ∈ MH_{n,q}} |Surj(Cl(O_K), H)| ]
                            / [ Σ_{K ∈ MH_{n,q}} 1 ]
      =  1        if i = 1
      =  1/|H|    if i = 0."

where `MH_{n,q}` is the set of function fields of monic smooth hyperelliptic
curves `y² = f(x)` with `f` monic squarefree of degree `n` over `𝔽_q`.

Hypotheses recorded exactly, in my own words, for the H2 refutation:
* the setting is **function fields over 𝔽_q(t)**, not number fields;
* `H` is **finite abelian of odd order** (Theorem 1.1.1; the non-abelian results
  are separate, §1.3);
* `gcd(|H|, q(q−1)) = 1`, i.e. odd characteristic prime to `|H|` and no roots of
  unity of order dividing `|H|` in `𝔽_q` (Theorem 1.2.1 removes the `q−1` part
  at the cost of a factor `|∧²H[h]|`, `h = gcd(|H|, q−1)`);
* `q > C(H)` — "q sufficiently large", with `C` depending only on `H`
  (Remark 1.1.3 says `C` can be made explicit, Remark 5.3.2);
* the family is ordered by **degree n**, i.e. by discriminant — the paper calls
  `n` the "log discriminant degree" (Remark 1.1.4);
* the conclusion is a **ratio of sums over an infinite family as n → ∞**.

Remark 1.1.2, verbatim, is the paper's own statement of what it does *not* prove:
*"Even though for any given H, we compute the H-moment of the class group of
quadratic fields over 𝔽_q(t) for sufficiently large q, we do not prove the
Cohen–Lenstra heuristics. Although it is true that knowledge of all moments do
determine the Cohen–Lenstra distribution, for a fixed value of q, we are only
able to compute moments associated to sufficiently small groups H relative to q."*

Also recorded, from §1: Wood–Wood ([WW21], Theorem 1.3) show the Cohen–Lenstra
distribution for imaginary or real quadratic fields is determined by its moments;
and *"since 1988, no additional odd order moments of class groups of quadratic
fields have been computed"* beyond `ℓ = 3` (Davenport–Heilbronn over ℚ,
Datskovsky–Wright over function fields).

The `i = 0` / `i = 1` split is the real / imaginary split, and the values `1/|H|`
and `1` are exactly the first moments of the two Cohen–Lenstra measures used in
`analysis/cl.py`; the self-test checks against them.

### Wood, *Cohen–Lenstra heuristics and local conditions* `[READ]`

> M. M. Wood, Res. Number Theory **4** (2018), art. 24; arXiv:1710.01350v2.

Used as the primary source for the two measures, since Cohen–Lenstra (1984) is
paywalled (§4). Introduction, p.1, verbatim:

> "if we consider the measure on finite abelian p-groups such that
>
>     mu_CL(A) := (1/|Aut(A)|) prod_{i≥1} (1 − p^{−i}),
>
> they conjectured that this measure gives the distribution of the Sylow
> p-subgroups of class groups of imaginary quadratic fields. For real quadratic
> fields, we make a probability measure mu^r_CL on finite abelian p-groups by
> producing a random group as follows: pick a random group B with respect to
> mu_CL, then pick a (uniform) random element b ∈ B, and then form B/⟨b⟩. Then
> mu^r_CL(A) is the probability that this process produces a group isomorphic to
> A. They then conjectured that mu^r_CL gives the distribution of the Sylow
> p-subgroups of class groups of real quadratic fields."

Also, the structural fact used to motivate the named alternative hypothesis
(`preregistration.md` §3):

> "when K/𝔽_q(t) is imaginary quadratic (i.e. ramified over ∞), then
> Cl(O_K) ≃ Pic⁰(C_K). However, when K/𝔽_q(t) is real quadratic (i.e. ∞ splits
> into ∞₁, ∞₂), then Cl(O_K) ≃ Pic⁰(C_K)/⟨∞₁ − ∞₂⟩."

This is what identifies the `1/|A|` factor as "the cost of quotienting by one
random element", and identifies the function-field regulator with the *order* of
that element.

### Lamzouri, *Large moments and extreme values of class numbers of indefinite binary quadratic forms* — **NEAR MISS** `[READ, intro]`

> Y. Lamzouri, arXiv:1609.01630v3; Mathematika (2017).

Abstract, verbatim: *"Let h(d) be the class number of indefinite binary quadratic
forms of discriminant d, and let ε_d be the corresponding fundamental unit. In
this paper, we obtain an asymptotic formula for the k-th moment of h(d) over
positive discriminants d with ε_d ≤ x, uniformly for real numbers k in the range
0 < k ≤ (log x)^{1−o(1)}. This improves upon the work of Raulf, who obtained such
an asymptotic for a fixed positive integer k. **We also investigate the
distribution of large values of h(d) when the d's are ordered according to the
size of their fundamental units ε_d. In particular, we show that the tail of this
distribution has the same shape as that of class numbers of imaginary quadratic
fields ordered by the size of their discriminants.**"*

**Why this is the most important near-miss.** It is the closest thing in the
literature to the question of this study: it *is* about the regulator ordering,
and it *is* about a distribution. But the object whose distribution is described
is the class **number** `h(d)` as a real quantity — its moments and the tail of
its large values — not the isomorphism class of the class **group** or its Sylow
p-subgroups. Cohen–Lenstra is a statement about the latter, and Lamzouri makes no
Cohen–Lenstra statement. The emphasised sentence is nonetheless the strongest
published evidence for the alternative hypothesis registered in
`preregistration.md` §3, and was cited there before any comparison was run.

### Dousselin, *Complex moments of class numbers with fundamental unit restrictions* — **NEAR MISS** `[READ, intro]`

> J. Dousselin, arXiv:2408.01401v1 (2 August 2024).

Abstract, verbatim: *"We explore the distribution of class numbers h(d) of
indefinite binary quadratic forms, for discriminants d such that the
corresponding fundamental unit ε_d is lower than d^{1/2+α}, where 0 < α < 1/2. To
do so we find an asymptotic formula for z-th moments of such h(d)'s, over d ≤ x,
uniformly for a complex number z in a range of the form |z| ≤ (log x)^{1+o(1)},
ℜ(z) ≥ −1. This is achieved by constructing a probabilistic random model for
these values … As another application, we give an asymptotic formula for the
number of d's such that h(d) ≤ H and ε_d ≤ d^{1/2+α}."*

Same delineation as Lamzouri: a small-regulator condition, a probabilistic model,
a distribution — but of the class *number*, not the class *group*. Records
Gauss's conjecture (Disquisitiones, 1801) `Σ_{d≤x} h(d) log ε_d ~ π²x^{3/2}/(18ζ(3))`,
proved by Siegel (1944), and attributes to Hooley the still-open conjecture for
the unweighted sum.

### Hashimoto, *Asymptotic formulas for class number sums … in arithmetic progressions* `[READ, intro]`

> Y. Hashimoto, arXiv:1003.3716v2.

Used for the Sarnak statement (above). Notes that comparable asymptotics were
obtained earlier by Raulf by different methods.

### Deitmar, *Class numbers of orders in cubic fields* `[READ, partial]`

> A. Deitmar, arXiv:math/0005242. PDF obtained and searched.

The regulator ordering extended beyond the quadratic case: class number sums for
orders in cubic fields, ordered by regulator, via a prime-geodesic-type theorem.
The brief asked specifically whether the *distribution* question is raised there.
It is not: the paper is about sums and averages. The related
*Class Numbers of Orders in Quartic Fields* (arXiv:math/0602294) likewise states
an asymptotic law "as the bound on the regulators tends to infinity", again for
sums, not distributions.

### Ellenberg, *Recent progress around Cohen–Lenstra heuristics* — **the decisive context** `[READ, relevant sections]`

> J. Ellenberg, Séminaire Bourbaki, 78e année, n° 1251, March 2026;
> arXiv:2606.06024v1. Obtained as PDF and read.

Found late, by searching `abs:"Pell" AND abs:"Cohen-Lenstra"`. It is the most
important secondary source for this study — not for a result, but because it
settles three things that the earlier searches left open.

**(a) The number-field form of the mechanism, credited to Gross.** §"Even taking
this into account…", verbatim:

> "Numerical evidence suggests that, as K ranges over real quadratic extensions
> of Q, the probability that Cl_K[ℓ^∞] is isomorphic to A is proportional, not to
> |Aut(A)|^{−1}, but to |A|^{−1}|Aut(A)|^{−1}. … (Cohen and Lenstra, 1983)
> records the observation, credited to Gross, that when K is a real quadratic
> field, the ring O_K is in some sense analogous to the ring O_L[1/π], where L is
> a quadratic imaginary field and π is a factor of a prime p split in L. Both
> rings have two "missing" places: the two archimedean places in the case of O_K,
> and ∞ and π in the case of O_L[1/π]. The class group of O_L[1/π] is simply
> Cl_L/⟨π⟩. This suggests that Cl_K should be seen, not as a random abelian
> ℓ-group, but as the quotient of a random abelian ℓ-group (like Cl_L) modulo a
> random element (like π)."

This matters because the alternative hypothesis registered in
`preregistration.md` §3 was motivated by the *function field* picture
(`Cl(O_K) = Pic⁰/⟨∞₁−∞₂⟩`). The Gross analogy is the same mechanism stated
directly for number fields, and it goes back to Cohen–Lenstra themselves. Under
it, the element quotiented by is the class of π, and the quantity playing the
role of the regulator is the **order of that class**. So "condition on a small
regulator" reads as "condition on the quotiented element having small order",
and in the limit the quotient disappears and the imaginary measure is recovered.
This is recorded here rather than in `preregistration.md` because it was found
after that file was committed; it changes no hypothesis, only the strength of
the motivation for one already registered.

**(b) It is already known that the ordering matters for Cohen–Lenstra-type
conjectures, and the known mechanism is subfields.** §"Another change is the
order in which the K are counted", verbatim: *"it has come to be seen that this
ordering [by discriminant] is problematic for Cohen-Lenstra heuristics. Roughly
speaking, the problem is subfields. If one counts Z/4Z-extensions K of Q in order
of discriminant, for example, and L is a fixed quadratic field, then a positive
proportion of K contain L, and so any unexpected behavior of a single Cl_L can
bias the distribution of Cl_K over all K. (Bartel and Lenstra, 2020, §6) shows
that indeed this phenomenon produces counterexamples to the original
[Cohen–Lenstra–Martinet] conjectures."*

So "ordering changes the answer" is not itself new. The known mechanism requires
intermediate subfields, which do not exist for quadratic K/ℚ.

**(c) The survey does not treat regulator-ordered distributions.** Its only
mention of the regulator is a footnote: *"it is the combination of h_K and the
regulator which has an analytic meaning; it is natural to consider these
together, and there is another line of work in which one considers not only the
class group but an 'Arakelov class group' whose component group is Cl_K and whose
identity component manifests the regulator; **we will not explore this further
here**, but see e.g. (Bartel, Johnston, and Lenstra, 2024)."*

### Sawin & Wood, *Conjectures for distributions of class groups …* — **NEAR MISS on the ordering question** `[READ, Remark 1.3]`

> W. Sawin and M. M. Wood, *Conjectures for distributions of class groups of
> extensions of number fields containing roots of unity*, arXiv:2301.00791.

Remark 1.3, verbatim (line breaks normalised):

> "Conjecture 1.1 is not precise, in that it does not specify an ordering on E so
> that the distribution of class groups is well-defined. Cohen and Martinet
> [CM90] order fields by Nm Disc K, but this is known to not work in general,
> even when there are not relevant roots of unity in the base field [BL20,
> p. 929]. One possible ordering, as suggested by Bartel and Lenstra in [BL20]
> and also by Theorem 3.1, is by Nm √Disc(K/K₀), where √ denotes the radical. We
> certainly imagine the conjecture only holding for orderings such that the
> proportion of fields in E containing any fixed field K₁ ⊄ K₀ is 0."

**Read the last sentence carefully.** It states a *necessary* condition — "only
holding for orderings such that…" — not a sufficient one. Ellenberg's survey
paraphrases it as *"any natural ordering on extensions K/F will do as long as no
intermediate subfield occurs a positive proportion of the time"*, which is the
converse and is stronger than what Sawin–Wood wrote. The distinction is load
bearing for how the present result may be stated, and is handled in `REPORT.md`
§4.6: under the paraphrase the regulator ordering would be a counterexample;
under the actual remark it is only evidence that the subfield condition is not
sufficient. Note also that Conjecture 1.1 concerns extensions containing roots of
unity, a different family from real quadratic fields over ℚ.

### Bartel, Johnston & Lenstra, *Arakelov class groups of random number fields* `[READ, introduction]`

> A. Bartel, H. Johnston, H. W. Lenstra Jr., arXiv:2005.11533v3 (27 March 2024).

The reference Ellenberg points to for treating `Cl_F` and the units together.
Introduction, verbatim: *"we make the case that, in this context, Cl_F and O_F^×
are most naturally studied in combination, since their distributions need, by all
appearances, not be independent. Their dependence is best expressed by means of
the Arakelov class group. … **For number fields it plays the rôle that the
Jacobian of a curve plays for function fields over finite fields.** It can be
broken up into two pieces, one being Cl_F and the other coming from O_F^×."*

This supplies the correct number-field name for the object my heuristic treats as
"the thing being quotiented": the Arakelov class group is the number-field
analogue of `Pic⁰(C)`, with `Cl_F` as its component group and the regulator as
the covolume of its identity component.

**Why it is nevertheless not my result.** Their paper's subject is the *Galois
module* structure of oriented Arakelov class groups, Chinburg's Ω(3) conjecture,
and a new series of counterexamples to Cohen–Lenstra–Martinet with non-abelian
Galois groups. Searching the text for "regulator", "ordering", "ordered by" and
"by discriminant" returns nothing relevant: the paper does not order families by
regulator and makes no statement about real quadratic fields ordered that way.
It is the right conceptual framework for the question and does not answer it.

---

## 2. Sources located and used bibliographically

* A. Hurwitz, *Ueber die angenäherte Darstellung der Irrationalzahlen durch
  rationale Brüche*, Math. Ann. **39** (1891), 279–284. `[CITED-ONLY]` — the
  optimality of √5. The statement is standard and is additionally verified
  numerically in `data/verify_extremality.gp` (convergence of `q·|qφ−p|` to
  `1/√5`).
* A. A. Markoff, *Sur les formes quadratiques binaires indéfinies*,
  Math. Ann. **15** (1879), 381–406; **17** (1880), 379–399. `[CITED-ONLY]`
* T. W. Cusick and M. E. Flahive, *The Markoff and Lagrange Spectra*,
  Math. Surveys and Monographs **30**, AMS, 1989. `[CITED-ONLY]` — Lagrange
  spectrum minimum √5.
* C. Series, *The modular surface and continued fractions*, J. London Math. Soc.
  (2) **31** (1985), 69–80. `[CITED-ONLY]` — geodesic ↔ continued fraction
  correspondence.
* H. Davenport and H. Heilbronn, *On the density of discriminants of cubic
  fields II*, Proc. Roy. Soc. London A **322** (1971), 405–420. `[CITED-ONLY]` —
  average `|Cl[3]|` = 2 (imaginary) and 4/3 (real). Used as the calibration
  anchor; encoded and checked in `analysis/cl.py::selftest`.
* M. Bhargava, A. Shankar, J. Tsimerman, *On the Davenport–Heilbronn theorems
  and second order terms*, Invent. Math. **193** (2013), 439–499; and
  T. Taniguchi, F. Thorne, *Secondary terms in counting functions for cubic
  fields*, Duke Math. J. **162** (2013), 2451–2508. `[CITED-ONLY]` — the `X^{5/6}`
  secondary term, used in `preregistration.md` §6 to set the expected size of the
  calibration residual (relative `X^{−1/6}`) *before* looking at the data.
* B. Hillar, D. Rhea, *Automorphisms of finite abelian groups*, Amer. Math.
  Monthly **114** (2007), 917–923. `[CITED-ONLY]` — `|Aut(A)|` formula,
  implemented and unit-tested against hand values in `analysis/cl.py`.
* C. Hooley, *On the Pellian equation and the class number of indefinite binary
  quadratic forms*, J. Reine Angew. Math. **353** (1984), 98–131. `[CITED-ONLY]` —
  located via Dousselin §1, which records Hooley's (still open) conjecture for
  `Σ_{d≤x} h(d)`. Full text not obtained.
* C. L. Siegel, *The average measure of quadratic forms with given determinant
  and signature*, Ann. of Math. **45** (1944), 667–685. `[CITED-ONLY]` — proof of
  Gauss's `x^{3/2}` law in the discriminant ordering.

---

## 3. Searches run, and what came back

arXiv API (`https://export.arxiv.org/api/query`), plus web search. The arXiv API
indexes **metadata only**, not full text, so quoted-phrase queries against `all:`
return loose matches; this is noted because it limits how strong a negative
conclusion the arXiv searches can support.

| query | result |
|---|---|
| `all:"ordered by regulator"` | no relevant hits (matches were physics/CS noise — confirms the field is not full-text indexed) |
| `all:"regulator ordering"` | 1 hit, *Regulators of rank one quadratic twists* (0707.0772) — elliptic curve regulators, unrelated |
| `abs:"Cohen-Lenstra" AND abs:"regulator"` | 1 hit, *Numerical verification of the Cohen–Lenstra–Martinet heuristics …* (1706.04847) — discriminant ordering, p-rationality; not the regulator ordering |
| `abs:"Cohen-Lenstra" AND abs:"real quadratic" AND cat:math.NT` | 4 hits: Wood 1710.01350 (used); 2509.20185 ray class groups; 2104.08561 class numbers of ℚ(√p) by prime discriminant; 1302.3099 p-ramified modules. None uses a regulator ordering |
| `abs:"fundamental unit" AND abs:"class number" AND abs:"distribution" AND cat:math.NT` | Lamzouri 1609.01630 and Dousselin 2408.01401 — the two near-misses; both class **number**, not class **group** |
| `ti:"class numbers" AND abs:"prime geodesic theorem"` | Hashimoto 0807.0056 and 1003.3716; Deitmar math/0005242 and math/0602294 — all sums/averages in a regulator ordering, no distributions |
| `all:"class numbers of indefinite binary quadratic forms"` | 0807.0056, 1609.01630, 1208.6086 |
| `au:Fouvry AND au:Jouve AND abs:"regulator"` | no results |
| `au:Fouvry AND au:Kluners AND abs:"negative Pell"` | no results (their papers predate/are indexed differently); reached instead via 1908.01752 |
| `abs:"negative Pell equation" AND abs:"density"` | Koymans–Pagano 1908.01752 (improves Fouvry–Klüners toward Stevenhagen's 58.1%, via the 8-rank of narrow class groups), 1907.13105, 1806.06250 — all about the **2-power** rank, excluded here by design |
| web: `"Cohen-Lenstra" class group distribution "ordered by regulator" real quadratic` | no paper; returned general CL material and Wood's `mu^r_CL` description |
| web: `class group 3-rank real quadratic Richaud–Degert "n²+4" Cohen–Lenstra thin family` | criteria for `h = 1, 2, 3` in Richaud–Degert families; no distributional/CL statement in a regulator ordering |
| web: Sarnak bibliography (IAS) | confirmed J. Number Theory **15** (1982), 229–247 — corrected a wrong volume in the first commit of `preregistration.md` |
| web: modular surface systole / `2 arccosh(3/2)` | no clean primary citation surfaced; E4 is therefore given a complete elementary derivation in `EXTREMALITY_NOTE.md` rather than being asserted |

**Conclusion of the priority search.** No source found states, conjectures, or
tests the distribution of the p-part of class groups of real quadratic fields
under a regulator ordering. The closest published work (Lamzouri, Dousselin,
Raulf, Sarnak, Hooley, Deitmar) studies **sums, averages, moments and value
distribution of the class number** in that ordering, which is a different object.
This is a negative result about the literature and is bounded by the search
limitation noted above: arXiv full text is not searchable through the API, and
pre-arXiv journal literature (Hooley 1984, Raulf's thesis work) was reached only
through citations in later papers.

---

## 4. Sources sought but not obtained

Recorded so that nothing is silently treated as read.

* **Cohen & Lenstra, *Heuristics on class groups of number fields*, in Number
  Theory Noordwijkerhout 1983, Lecture Notes in Math. 1068, Springer (1984),
  33–62.** Springer returns a 303 redirect to an identity-provider login;
  ResearchGate returns HTML, not the PDF. **Not read.** The brief asked for the
  real-quadratic prediction to be taken "from Cohen–Lenstra (1984) directly";
  that was not possible here. The measure used in this study is instead quoted
  verbatim from Wood 2018 (§1 above), which attributes it to [CL84], and is
  independently pinned down by two external checks that do not depend on the CL84
  text at all: the Davenport–Heilbronn value 4/3 and Landesman–Levy Theorem 1.1.1
  (`i = 0` moment `1/|H|`). Both checks are executed in `analysis/cl.py::selftest`.
  **Consequence:** CL84's own discussion of the regulator's role in producing the
  `1/|G|` factor is `[UNVERIFIED]` here and is not used to support any claim.
* **Sarnak (1982), journal text.** ScienceDirect HTTP 403. Statement obtained
  verbatim from Hashimoto instead (§1). Sarnak's *Acta Math.* 151 paper
  (*The arithmetic and geometry of some hyperbolic Bianchi groups*, §§5–7 in the
  brief's description) was **not obtained**; no claim here rests on it.
* **Hooley (1984), J. Reine Angew. Math. 353.** Not obtained; used only as a
  bibliographic pointer via Dousselin.
* **Fouvry & Jouve on regulator sizes.** No arXiv record found under that author
  pair with "regulator" in the abstract. Not obtained. No claim rests on it.
* **Raulf**, whose fixed-`k` moment results Lamzouri improves. Reached only
  through citations. Not obtained.
