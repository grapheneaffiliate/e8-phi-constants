# Pre-registration: p-part of class groups of real quadratic fields under regulator ordering

**Committed before any empirical class-group distribution was computed or inspected.**

At the time of writing, the two datasets (`data/gen_disc_ordered.gp`,
`data/gen_reg_ordered.gp`) were either running or complete as raw CSV, but **no
p-part statistic, rank tabulation, or comparison against any Cohen–Lenstra
prediction had been computed or looked at.** What had been inspected: row counts,
the largest discriminant reached, a benchmark of mean class number on ~60
discriminants near t = 10^4, 10^5, 10^6 (reported in the run log as 405, 3158,
26060 — used only to size the computation), and the arithmetic self-consistency
of the fundamental-unit columns.

Nothing below is conditioned on an observed p-rank frequency.

---

## 1. Question

Sarnak (J. Number Theory 14 (1982), 342–378) proved that the **average** class
number obeys a clean asymptotic law when indefinite binary quadratic forms are
ordered by the size of the fundamental unit rather than by discriminant:

    sum_{D>0, eps(D) < x} h(D) log eps(D)  ~  x^2 / 2
    sum_{D>0, eps(D) < x} h(D)             ~  li(x^2)

The **distribution** of the class group in that ordering is a separate question
and is what this study measures. Specifically: for odd primes p, what is the
distribution of the isomorphism class of the Sylow p-subgroup `Cl(D)_p` when real
quadratic fields are ordered by regulator?

## 2. Data

Two independently generated, complete enumerations:

| dataset | ordering | completeness criterion | truncation bounds to be used |
|---|---|---|---|
| `disc_ordered.csv` | by discriminant | every fundamental discriminant `0 < D <= 10^7` | `10^5, 10^6, 10^7` |
| `reg_ordered.csv` | by regulator | every fundamental discriminant with `eps_D <= 2*10^6` | `10^4, 10^5, 10^6, 2*10^6` |

The regulator dataset is a genuine regulator-ordered enumeration, not a re-sort
of the discriminant-ordered one: it reaches `D ~ 4*10^12`.

Two regulator orderings will be reported separately, because Sarnak's theorem is
stated for the **narrow** fundamental unit while `quadunit` returns the **wide**
one:

* `reg-wide`: order by `eps_D` (fundamental unit of the maximal order).
* `reg-narrow`: order by `eps_D^+` = `eps_D` if `N(eps_D) = +1`, else `eps_D^2`
  (the fundamental totally positive unit; the fundamental solution of the Pell
  equation `t^2 - D u^2 = 4`). This is Sarnak's `eps(D)`.

Since `eps_D^+ >= eps_D`, the set of fields with `eps_D <= 2*10^6` contains every
field with `eps_D^+ <= 2*10^6`, so both orderings are complete out to the same
cutoff.

Only **odd** p are studied: p ∈ {3, 5, 7, 11}. The 2-part is excluded because
genus theory determines it from the factorisation of D, and the regulator-ordered
family is dominated by `D = t^2 ± 4 = (t∓2)(t±2)`, which is a genus-theoretically
special factorisation. Any 2-part effect would be a known artefact, not a finding.

For odd p, the narrow and wide class groups have the same Sylow p-subgroup (they
differ by a 2-group), so the wide-class-group convention of `quadclassunit` is
immaterial.

## 3. Competing hypotheses

Both are fully specified point hypotheses; both were verified in
`analysis/cl.py::selftest` against Davenport–Heilbronn and Landesman–Levy before
this file was written.

**H_real (the null).** The p-part follows the Cohen–Lenstra measure for real
quadratic fields, `mu_CL^r`, the same measure conjectured for the discriminant
ordering:

    mu_CL^r(A) = (1/(|A| |Aut A|)) * prod_{k>=2} (1 - p^-k)
    E[#Surj(Cl, Z/p)] = 1/p

*Interpretation if accepted:* the regulator ordering changes the average class
number enormously but leaves the class-group distribution alone. No novelty.

**H_imag (the named alternative).** The p-part follows the Cohen–Lenstra measure
for **imaginary** quadratic fields, `mu_CL`:

    mu_CL(A) = (1/|Aut A|) * prod_{k>=1} (1 - p^-k)
    E[#Surj(Cl, Z/p)] = 1

*Why this is the alternative worth naming, stated in advance:*

1. **Function-field structure.** For a real quadratic function field,
   `Cl(O_K) = Pic^0(C_K)/<[inf_1 - inf_2]>`, and the regulator is the **order**
   of `[inf_1 - inf_2]` in `Pic^0`, so that `h(O_K) * R_K = |Pic^0(C_K)|`
   (M. M. Wood, arXiv:1710.01350, §1). The `1/|A|` factor distinguishing
   `mu_CL^r` from `mu_CL` is exactly the cost of quotienting by that one random
   element. Conditioning on a small regulator conditions that element to have
   small order; in the limiting case where p does not divide the regulator, the
   p-part of the quotient equals the p-part of `Pic^0`, which is `mu_CL`-distributed.
2. **A proved analogy for the class number.** Lamzouri (arXiv:1609.01630,
   abstract) proves that when discriminants are ordered by the size of `eps_d`,
   the tail of the distribution of large `h(d)` "has the same shape as that of
   class numbers of imaginary quadratic fields ordered by the size of their
   discriminants."
3. **Size heuristic.** `h R = sqrt(D) L(1,chi_D)`. In the discriminant ordering R
   is typically of size `D^{1/2+o(1)}` and h is O(1); in the regulator ordering R
   is bounded and `h = D^{1/2+o(1)}`, i.e. as large as in the imaginary case.

**H_neither.** Both rejected. Would require the interpretation discipline of §6
before being called anything.

The two hypotheses are far apart and easily separated at the available sample
sizes. Predicted `P(Cl_p = trivial)`:

| p | H_imag (u=0) | H_real (u=1) |
|---|---|---|
| 3 | 0.560126 | 0.840189 |
| 5 | 0.760333 | 0.950416 |
| 7 | 0.836795 | 0.976261 |
| 11 | 0.900833 | 0.990916 |

**Stated expectation (for the record, so it can be wrong):** I expect H_imag to
fit the regulator ordering better than H_real, on the strength of argument (1).
I expect H_real to fit the discriminant ordering.

## 4. Test statistics

For each (dataset, ordering, truncation bound X, prime p):

**T1 — first moment.** `M_p := mean over the sample of #Surj(Cl, Z/p) = p^{r_p} - 1`,
where `r_p = rank_p Cl`. Predicted `1/p` under H_real, `1` under H_imag. This is
the statistic that Landesman–Levy compute and that Wood–Wood (Theorem 1.3, quoted
in Landesman–Levy §1) show determines the distribution. Reported with a standard
error from the sample variance, and separately from a 1000-resample bootstrap
(seed 20260810, fixed here).

**T2 — rank distribution.** Empirical frequencies of `r_p = 0, 1, >= 2` against
both predictions.

**T3 — full isomorphism-type distribution.** Pearson chi-square of the empirical
counts of `Cl_p ≅ A` over cells `A` = every abelian p-group of order `<= p^3`,
plus one catch-all cell. Cells whose **expected** count under the null being
tested is `< 5` are merged into the catch-all before computing the statistic
(the merge is determined by n and the null only, never by observed counts).
Degrees of freedom = (number of surviving cells) − 1.

## 5. Decision rules

Fixed now:

* **z-scores.** `z = (M_p_hat − prediction)/SE`. A hypothesis is *rejected* at a
  given (ordering, p, X) if `|z| > 5`. It is *accepted* if `|z| < 3`. Between 3
  and 5: undecided.
* **chi-square.** A hypothesis is rejected if its p-value is `< 10^-3`.
* **Verdict per ordering.** H_real / H_imag / neither / undecided, required to be
  consistent across all four primes at the largest bound; inconsistency across
  primes is itself reported as "neither".
* **Novelty threshold.** A deviation from *both* named hypotheses will be called
  a real observation only if all four hold:
  1. `|z| > 5` against both, at the largest truncation bound;
  2. the deviation does **not** shrink as the truncation bound increases across
     the full ladder of bounds (§2) — a shrinking discrepancy is declared a
     truncation artefact and reported as such;
  3. the deviation exceeds, in absolute relative terms, the calibration
     deviation measured on the discriminant-ordered channel at comparable sample
     size (§6);
  4. it survives the confounder checks of §6.

## 6. Calibration channel and known confounders

**Calibration (mandatory).** The discriminant-ordered dataset is a control with a
*proved* answer: by Davenport–Heilbronn (1971), `M_3 -> 1/3` in that ordering.
If the pipeline does not reproduce this, the pipeline is wrong and no other
number in this study may be reported.

**Expected size of the calibration residual, stated in advance.** Convergence to
the Davenport–Heilbronn average is known to be slow. The count of cubic fields of
bounded discriminant has a secondary term of order `X^{5/6}` (conjectured by
Roberts; proved independently by Bhargava–Shankar–Tsimerman and by
Taniguchi–Thorne, 2013), which corresponds to a **relative correction of order
`X^{-1/6}`** to the average of `|Cl[3]|`. At `X = 10^7` that is `10^{-7/6} ≈ 0.068`,
so a residual of several percent in `M_3` in the discriminant ordering is
*expected* and must not be reported as a deviation. Any claim about the regulator
ordering must clear this scale by a wide margin.

**Confounders that must be ruled out before any deviation is called meaningful:**

1. **Thinness / algebraic family.** `#{D : eps_D <= x}` grows like a constant
   times `x`, versus a constant times `X` for `#{D <= X}` — but the regulator
   ordering reaches `D ~ x^2`, so it samples a set of density `~1/x` among
   discriminants of comparable size. It is dominated by `D = (t^2 ∓ 4)/u^2`,
   i.e. by values of a quadratic polynomial. To be reported: the fraction of the
   sample with `u = 1`, and the statistics restricted to `u = 1` and to `u > 1`
   separately. If the two sub-populations disagree, the effect is a property of
   the polynomial family, not of the regulator ordering as such.
2. **The `h R = sqrt(D) L` bias.** Conditioning on small R with D large forces h
   large. To be reported: the empirical distribution of `h` and of
   `L(1,chi_D) = 2 h R / sqrt(D)` in each ordering, and the statistics
   restricted to sub-bands of `h`.
3. **Genus theory / the 2-part.** Excluded by construction (odd p only). To be
   confirmed: results are unchanged when restricted to `D` prime (where genus
   theory contributes nothing).
4. **Sample size.** Report n for every cell. No verdict at any (ordering, p, X)
   where the expected count of the rarest retained cell under the null is `< 5`.

## 7. Prohibited moves

* No statistic reported without the null it is tested against being one of the
  two named in §3.
* No post-hoc choice of p, truncation bound, or cell merging.
* If the outcome is "the regulator ordering agrees with H_real, no novelty," that
  is reported as the headline exactly as plainly as any other outcome.
* If a computation contradicts a claim in this file, this file is wrong and the
  contradiction is reported.
