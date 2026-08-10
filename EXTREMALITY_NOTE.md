# The extremality of ℚ(√5): a clean statement

This note states, with correct attributions, the sense in which ℚ(√5) is
extremal among real quadratic fields. It contains **no class-number claim** —
see §6 for why any such claim is empty — and no application to anything outside
algebraic number theory.

Every claim carries one tag: `[COMPUTED]` (script given, re-runnable),
`[CLASSICAL]` (author, year, venue, specific result), or `[CONJECTURAL]`.
All `[COMPUTED]` numbers below come from `data/verify_extremality.gp`, run with
PARI/GP 2.15.4 at 40 significant digits:

    gp -q data/verify_extremality.gp

Throughout, φ = (1+√5)/2 = 1.6180339887498948482…, and for a positive
fundamental discriminant D, ε_D denotes the fundamental unit > 1 of the maximal
order of ℚ(√D) and R(D) = log ε_D its regulator.

---

## The statement

> **ℚ(√5) is simultaneously extremal in four distinct senses: it has the
> smallest discriminant, the smallest regulator, the worst rational
> approximability of its generator, and the shortest associated closed geodesic
> on the modular surface. These four are not four coincidences — the last three
> are the same fact seen through three standard equivalences (§5).**

---

## E1. Smallest discriminant `[COMPUTED]` `[CLASSICAL]`

The positive fundamental discriminants begin

    5, 8, 12, 13, 17, 21, 24, 28, 29, 33, 37, 40, …

so `D = 5` is the smallest, and ℚ(√5) is the real quadratic field of smallest
discriminant.

This is immediate from the definition (a fundamental discriminant is a
squarefree `m ≡ 1 (mod 4)` or `4m` with squarefree `m ≡ 2, 3 (mod 4)`; the
smallest such positive non-square is 5). It is a fact about the *list of
discriminants*, and nothing more should be read into it.

*Caveat on the enumeration:* `D = 1` is a fundamental discriminant — that of ℚ
itself — and PARI's `isfundamental(1)` returns true. It is excluded above because
ℚ is not a quadratic field.

## E2. Smallest regulator `[COMPUTED]` + complete elementary proof

    R(5) = log φ = 0.4812118250596034474977589134243684231352…

is the smallest regulator of any real quadratic field. The ten smallest, computed
over `0 < D ≤ 5000`:

| R(D) | D | ε_D | N(ε_D) |
|---|---|---|---|
| 0.4812118251 | 5 | φ | −1 |
| 0.8813735870 | 8 | 1+√2 | −1 |
| 1.1947632173 | 13 | (3+√13)/2 | −1 |
| 1.3169578969 | 12 | 2+√3 | +1 |
| 1.5667992370 | 21 | (5+√21)/2 | +1 |
| 1.6472311464 | 29 | (5+√29)/2 | −1 |
| 1.8184464592 | 40 | 3+√10 | −1 |
| 1.9657204716 | 53 | (7+√53)/2 | −1 |
| 2.0634370689 | 60 | 4+√15 | +1 |
| 2.0947125473 | 17 | 4+√17 | −1 |

**Proof (complete, elementary).** Write ε_D = (t + u√D)/2 with `t, u` positive
rational integers satisfying `t² − D u² = ±4`. That `t ≥ 1` and `u ≥ 1` is forced:
`u = 0` would make ε_D = ±1, not a unit > 1 of infinite order, and `t = 0` would
give `−D u² = ±4`, impossible for `D ≥ 5`. Hence

    ε_D = (t + u√D)/2 ≥ (1 + √D)/2 ≥ (1 + √5)/2 = φ,

using `D ≥ 5` from E1. Equality forces `t = u = 1` and `D = 5`, i.e. ℚ(√5).
Since `log` is increasing, `R(D) ≥ log φ` with equality only at `D = 5`. ∎

Two remarks the proof makes free:

* The bound holds for every real quadratic **order**, not just maximal ones: the
  fundamental unit of a non-maximal order is a power of that of the maximal
  order, hence at least as large.
* φ is therefore the smallest unit > 1 in any real quadratic order. `[COMPUTED]`
  confirms no counterexample for `D ≤ 20000`.

## E3. Worst rational approximability `[CLASSICAL]`

> **Hurwitz's theorem.** For every irrational α there are infinitely many
> rationals `p/q` with `|α − p/q| < 1/(√5 q²)`, and the constant √5 cannot be
> replaced by any larger one — it fails already for α = φ.
>
> A. Hurwitz, *Ueber die angenäherte Darstellung der Irrationalzahlen durch
> rationale Brüche*, Math. Ann. **39** (1891), 279–284.

Equivalently `liminf_{q→∞} q·‖qφ‖ = 1/√5`, where ‖·‖ is distance to the nearest
integer. `[COMPUTED]`, along the convergents `p/q` of φ (Fibonacci ratios), the
quantity `q·|qφ − p|` oscillates and converges to `1/√5 = 0.4472135955…`:

    q = 3    0.4376941013        q = 34   0.4472909949
    q = 5    0.4508497187        q = 55   0.4471840316
    q = 8    0.4458247200        q = 89   0.4472248879
    q = 13   0.4477440987        q = 144  0.4472092822
    q = 21   0.4470109613        q = 233  0.4472152430

The reason is visible in the continued fraction: `φ = [1; 1, 1, 1, …]`, all
partial quotients minimal, so the convergents advance as slowly as possible.

√5 is also the smallest element of the Lagrange spectrum, whose discrete initial
part `√5, √8, √221/5, …` is indexed by the Markov triples:

> A. A. Markoff, *Sur les formes quadratiques binaires indéfinies*,
> Math. Ann. **15** (1879), 381–406, and **17** (1880), 379–399.
>
> T. W. Cusick and M. E. Flahive, *The Markoff and Lagrange Spectra*,
> Math. Surveys and Monographs **30**, Amer. Math. Soc., 1989 — Ch. 1 for the
> minimum √5 and the Markov correspondence.

## E4. Shortest closed geodesic on the modular surface `[COMPUTED]` `[CLASSICAL]`

**Corrected statement.** Under the correspondence between classes of indefinite
binary quadratic forms and primitive closed geodesics on the modular surface
ℍ/PSL₂(ℤ), the discriminant `D = 5` gives the **shortest** primitive closed
geodesic, of length

    ℓ_min = 4 log φ = 2 log((3+√5)/2) = 2 arccosh(3/2) = 1.9248473002384137899…

**Derivation (complete, elementary).** Primitive closed geodesics on ℍ/PSL₂(ℤ)
correspond to primitive hyperbolic conjugacy classes in PSL₂(ℤ); a hyperbolic
`γ` with larger eigenvalue `λ` has translation length `ℓ = 2 log λ`, and
`λ + λ^{-1} = |tr γ|`, so `ℓ = 2 arccosh(|tr γ|/2)`. Hyperbolicity requires
`|tr γ| > 2`, and the trace is a rational integer, so `|tr γ| ≥ 3`; the value 3 is
attained, e.g. by `[[2,1],[1,1]]`. For `|tr γ| = 3` the larger eigenvalue is
`(3+√5)/2 = φ²`, giving `ℓ = 2 log φ² = 4 log φ`. The associated discriminant is
`t² − 4 = 3² − 4 = 5`. ∎

Corroboration that the normalisation `ℓ = 2 log λ` is the standard one: the prime
geodesic theorem for SL₂(ℤ) is stated as counting primitive hyperbolic classes
whose *larger eigenvalue* is `< x`, with asymptotic `li(x²)` — i.e. geodesics of
length `< 2 log x`, so that the topological entropy is 1 (Y. Hashimoto,
arXiv:1003.3716, §1, quoting Selberg and Hejhal).

For the correspondence itself:

> C. Series, *The modular surface and continued fractions*,
> J. London Math. Soc. (2) **31** (1985), 69–80.

**A factor-of-2 trap, stated because it is easy to fall into.** The number

    2 log φ = arccosh(3/2) = 0.9624236501192068950…

is *not* the length of the geodesic; it is half of it. It is often quoted as the
length by mistake. The confusion has a specific arithmetic source, which is worth
naming (§5): the geodesic length is `2 log ε⁺_D` in terms of the **narrow**
(totally positive) fundamental unit, and for `D = 5` we have `N(φ) = −1`, so
`ε⁺_5 = φ² ≠ φ = ε_5`. Using the wide unit ε_5 in a formula that calls for the
narrow one ε⁺_5 loses exactly a factor of 2.

## 5. The four are not independent

E2, E3, E4 are three faces of one fact; only E1 is genuinely separate (and E1 is
what makes E2's proof work).

* **E2 ⟺ E4.** For discriminant D, the associated primitive closed geodesic has
  length `2 log ε⁺_D`, where `ε⁺_D` is the fundamental solution of the Pell
  equation `t² − Du² = 4` — the fundamental *totally positive* unit, equal to
  `ε_D` when `N(ε_D) = +1` and to `ε_D²` when `N(ε_D) = −1`. Minimising the
  regulator and minimising the geodesic length are therefore the same problem up
  to that norm-dependent factor of 2. `[COMPUTED]`: for `D = 5`, `N(ε_5) = −1`,
  `ε⁺_5 = φ²`, and `2 log ε⁺_5 = 4 log φ`, matching E4 exactly.
* **E3 ⟺ E2/E4.** The continued fraction of a quadratic irrational is periodic,
  its period encodes the fundamental unit, and by the Series correspondence the
  cutting sequence of the geodesic *is* the continued fraction expansion. φ has
  the slowest-growing continued fraction `[1;1,1,…]`, the smallest unit, and the
  shortest geodesic, for one reason expressed three ways.

So the honest headline is: **ℚ(√5) has the smallest discriminant among real
quadratic fields, and — as a consequence of that plus the Pell equation — the
smallest fundamental unit, from which its Diophantine and geometric extremality
follow by standard equivalences.** All of this is classical.

## 6. What must not be claimed: the class number

`h(ℚ(√5)) = 1` carries **no** class-group information, and cannot be used to
distinguish ℚ(√5) from anything.

The Minkowski bound for a real quadratic field of discriminant D is `√D/2`. If
`√D/2 < 2`, no prime ideal of norm ≥ 2 needs to be tested and `h = 1` follows
from the bound alone. `√D/2 < 2 ⟺ D < 16`, and `[COMPUTED]` the positive
fundamental discriminants below 16 are

| D | field | Minkowski bound | h |
|---|---|---|---|
| 5 | ℚ(√5) | 1.1180 | 1 |
| 8 | ℚ(√2) | 1.4142 | 1 |
| 12 | ℚ(√3) | 1.7321 | 1 |
| 13 | ℚ(√13) | 1.8028 | 1 |

**Four** fields, not one. Their class numbers are equal and forced, so `h = 1`
separates none of them. The first discriminant whose Minkowski bound reaches 2 is
`D = 17`; the smallest positive fundamental discriminant with `h > 1` at all is
`D = 40`.

It follows that a statement of the form *"ℚ(√5) has the unique minimal absolute
discriminant among class-number-one real quadratic fields"* is true but empty:
5 is the minimal real quadratic fundamental discriminant outright (E1), and the
class-number-one qualifier excludes nothing, since every candidate smaller than
17 has `h = 1` for free. The qualifier makes the sentence sound like a theorem
about class groups while adding no content. The correct statement is E1, with no
qualifier.
