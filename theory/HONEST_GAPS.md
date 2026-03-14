# GSM Honest Gaps: Derivation Chain Analysis

**Version 1.0 — March 14, 2026**
**License: CC-BY-4.0**

## Purpose

This document catalogues the **7 honest gaps** in the GSM derivation chain.
The Lagrangian is structurally complete — every constant has an identified sector.
The gaps are in the **derivation chain**: explicitly computing the φ-formulas from
the lattice action's equations of motion, rather than postulating them independently.

These gaps are distinct from (and complementary to) the per-formula audit in
`verification/audit/SUMMARY.md`, which classifies individual terms. Here we focus
on the logical path from the lattice action to the final formulas.

---

## Gap Summary

| ID | Severity | Gap | Core Issue |
|----|----------|-----|------------|
| GAP-1 | MINOR | λ_geom vs m_H/v consistency | Two independent formulas; RG running needed to connect them |
| GAP-2 | MINOR | EW triangle tree-level tension | sin²θ_W, m_W/v, m_Z/v don't close at tree level |
| GAP-3 | MODERATE | QCD running not derived from lattice | α_s(M_Z) uses standard β-function, not lattice EOM |
| GAP-4 | MODERATE | m_u/m_d ratio lacks M_geom derivation | φ⁻¹ − φ⁻⁵ postulated, not computed from mass matrix |
| GAP-5 | MODERATE | Composites are phenomenological fits | m_p, m_π, r_p formulas not derived from QCD bound states |
| GAP-6 | MODERATE | Cosmological formulas not from Regge EOM | Ω_Λ, H₀, n_s postulated rather than solved from Regge action |
| GAP-7 | MINOR | Continuum limit Lorentz recovery unproven | Argued heuristically, no rigorous proof |

---

## Detailed Analysis

### GAP-1: Higgs Self-Coupling vs Mass Ratio (MINOR)

**The issue:**
The Higgs sector provides two independent geometric formulas:

1. Self-coupling from Coxeter number: λ_geom = φ²/(4h²) = φ²/3600
2. Mass-to-VEV ratio: m_H/v = 1/2 + φ⁻⁵/10 = 0.5090

In the Standard Model, these are related by m_H = v√(2λ). Substituting:

```
m_H/v = √(2λ_geom) = √(2φ²/3600) = φ√(2/3600) ≈ 0.0302
```

This does **not** match m_H/v = 0.5090. The discrepancy is expected: the
tree-level relation m_H = v√(2λ) receives large radiative corrections from
the top quark loop. But the GSM currently does not derive the RG running
from the lattice — it simply provides both formulas independently.

**What would close it:**
Compute the one-loop effective potential on the H₄ lattice, showing that
the lattice UV cutoff k_max = πφ/ℓ_p produces precisely the running that
connects λ_geom at the Planck scale to (m_H/v)² at the EW scale.

**Affected constants:** #11 (m_H/v), indirectly #48 (m_H)

**Current status:** Both formulas independently match experiment. The gap is
in showing they are two limits of the same lattice computation.

---

### GAP-2: Electroweak Triangle Tree-Level Tension (MINOR)

**The issue:**
Three EW quantities are derived independently:

| Constant | Formula | Value |
|----------|---------|-------|
| sin²θ_W | 3/13 + φ⁻¹⁶ | 0.23122 |
| m_W/v | (1 − φ⁻⁸)/3 | 0.32619 |
| m_Z/v | 78/248 + φ⁻⁶ | 0.37024 |

The SM tree-level relation is:

```
sin²θ_W = 1 − (m_W/m_Z)² = 1 − (m_W/v)²/(m_Z/v)²
```

Computing from the GSM formulas:

```
1 − (0.32619/0.37024)² = 1 − 0.7763 = 0.2237
```

This gives 0.2237 vs the GSM value 0.23122. The ~3% discrepancy is
consistent with the known radiative corrections to the ρ parameter
(ρ = m_W²/(m_Z²cos²θ_W) ≠ 1 at one loop).

**What would close it:**
Show that the H₄ lattice regulator produces exactly the radiative
corrections (primarily the top-quark loop contribution to the W/Z
self-energies) that shift the tree-level relation by the observed amount.

**Affected constants:** #2 (sin²θ_W), #12 (m_W/v), #30 (m_Z/v)

**Current status:** Expected from standard physics. The gap is that the
GSM provides corrected values without deriving the corrections from the lattice.

---

### GAP-3: QCD Running Not Derived from Lattice (MODERATE)

**The issue:**
The strong coupling formula:

```
α_s(M_Z) = 1/[2φ³(1 + φ⁻¹⁴)(1 + 8φ⁻⁵/14400)]
```

gives the value at the Z-pole (M_Z ≈ 91.2 GeV). But the derivation of this
formula implicitly assumes standard QCD β-function running from the Planck
scale down to M_Z. The β-function coefficients b₀ = 7, b₁ = ... come from
counting active quark flavors and gluon loops — **not** from the H₄ lattice.

In a fully self-contained derivation, the β-function should emerge from the
lattice gauge action:

```
ℒ_gauge = −(1/4g²) Σ_{□} Tr[F_{□} F_{□}]
```

The lattice plaquette action on H₄ should produce asymptotic freedom with
the standard β-coefficients as a consequence of the E₈ → SU(3) branching
rules, but this computation has not been performed.

**What would close it:**
1. Compute the one-loop effective action for the H₄ lattice gauge theory
2. Show that the β-function coefficients match standard QCD
3. Derive the running from k_max = πφ/ℓ_p to M_Z
4. Recover α_s(M_Z) = 1/[2φ³(...)] as the result

**Affected constants:** #3 (α_s(M_Z))

**Current status:** The formula matches experiment to 0.09%. The geometric
content (φ³, 14400 = |W(H₄)|, 8φ⁻⁵) is fully traced. The gap is in the
derivation of the running itself.

---

### GAP-4: Light Quark Mass Ratio m_u/m_d (MODERATE)

**The issue:**
The up/down mass ratio is given as:

```
m_u/m_d = φ⁻¹ − φ⁻⁵ ≈ 0.527
```

(Experiment: m_u/m_d ≈ 0.47 ± 0.07, so this is within the large uncertainty.)

The fermion Lagrangian defines a geometric mass matrix M_geom that is diagonal
in the generation basis with entries from H₄ Casimir eigenvalues. For the
heavier quarks (m_s/m_d = L₃² = 20, m_c/m_s, m_b/m_c), the mass ratios are
derived from M_geom eigenvalue ratios.

But for m_u/m_d, the formula φ⁻¹ − φ⁻⁵ is **postulated** rather than computed.
The derivation would need to:

1. Diagonalize M_geom in the up-type sector
2. Show that the lightest two eigenvalues have ratio φ⁻¹ − φ⁻⁵
3. Explain why the up-type sector uses a subtraction (−) rather than the
   additions seen in other mass ratios

**What would close it:**
Explicit diagonalization of the 3×3 geometric mass matrix for up-type quarks,
showing the eigenvalue ratio emerges from E₈ → SU(3) branching.

**Affected constants:** #45 (m_u)

**Current status:** The experimental uncertainty on m_u/m_d is ~15%, so the
formula is consistent. But the derivation chain is incomplete.

---

### GAP-5: Composite Quantities Are Phenomenological Fits (MODERATE)

**The issue:**
Three quantities involving QCD bound states are derived from φ-formulas:

| Constant | Formula | Origin claim |
|----------|---------|-------------|
| m_p/m_e (#9) | 6π⁵(1 + φ⁻²⁴ + φ⁻¹³/240) | Proton as QCD bound state |
| m_π/m_e (#52) | 240 + 30 + φ² + φ⁻¹ − φ⁻⁷ | Pion mass from lattice |
| r_p (#53) | 4ℏc/m_p (4 = rank/2) | Proton charge radius |

These formulas match experiment beautifully (all within 0.1%). But they are
not derived from the QCD sector of the Lagrangian. Computing hadron masses
from first principles requires solving the non-perturbative lattice QCD
problem — even standard lattice QCD takes years of supercomputer time.

The GSM claim is that the H₄ lattice structure constrains the bound-state
spectrum through its discrete symmetries. But the actual computation
(evaluating the path integral of ℒ_gauge + ℒ_fermion for confined states)
has not been done.

**What would close it:**
1. Show that the H₄ lattice gauge theory confines (Wilson loop area law)
2. Compute the lightest baryon mass on the H₄ lattice
3. Demonstrate that 6π⁵ emerges from the lattice path integral
4. Similarly derive the pion mass and proton radius

**Affected constants:** #9 (m_p/m_e), #52 (m_π/m_e), #53 (r_p), #54 (B_d/m_p)

**Current status:** The formulas are compelling — the appearance of 6π⁵,
240 (kissing number), 30 (Coxeter number), and rank/2 strongly suggests
geometric origin. But the derivation from the lattice action is missing.

---

### GAP-6: Cosmological Formulas Not Derived from Regge EOM (MODERATE)

**The issue:**
The cosmological constants are expressed as φ-formulas:

| Constant | Formula |
|----------|---------|
| Ω_Λ (#22) | φ⁻¹ + φ⁻⁶ + φ⁻⁹ − φ⁻¹³ + φ⁻²⁸ + εφ⁻⁷ |
| H₀ (#24) | 100φ⁻¹(1 + φ⁻⁴ − 1/(30φ²)) |
| n_s (#25) | 1 − φ⁻⁷ |
| z_CMB (#23) | φ¹⁴ + 246 |

The theory document `GSM_GRAVITY_REGGE.md` defines a Regge calculus action
on the H₄ lattice with discrete Einstein equations. In principle, solving
these equations with cosmological boundary conditions should yield Ω_Λ, H₀,
and n_s as outputs.

But the current derivation does not solve the Regge equations of motion.
Instead, each cosmological formula is postulated independently and verified
against experiment. The connection to the Regge action is structural
("Ω_Λ comes from the lattice growth rate") but not computational.

**What would close it:**
1. Set up the Regge-Friedmann equations on the H₄ lattice
2. Solve for the late-time cosmological constant → derive Ω_Λ
3. Solve for the expansion rate → derive H₀
4. Compute primordial perturbation spectrum → derive n_s
5. Find the recombination surface → derive z_CMB

**Affected constants:** #22 (Ω_Λ), #23 (z_CMB), #24 (H₀), #25 (n_s),
#28 (Ω_b), #31 (Ω_DM), #55 (σ₈), #58 (r)

**Current status:** Individual terms in each formula trace to E₈/H₄
invariants. The formal proof in `proofs/cosmological_constant.md` proves
the Ω_Λ formula but notes an open question on the action principle origin.
The gap is in deriving these from the dynamical equations.

---

### GAP-7: Continuum Limit Lorentz Recovery (MINOR)

**The issue:**
The H₄ lattice has discrete H₄ symmetry (order 14400), not continuous
Lorentz symmetry SO(3,1). The theory claims that Lorentz invariance is
recovered in the continuum limit (wavelengths λ ≫ ℓ_p/φ), and this is
the standard expectation for any well-behaved lattice theory.

But the argument is heuristic:
- The 600-cell is the most isotropic regular polytope in 4D
- H₄ has 14400 symmetry elements → densely samples SO(4)
- Standard lattice QCD arguments apply

A rigorous proof would need to show:
1. The lattice propagator approaches the continuum propagator as k → 0
2. Rotational symmetry violation scales as (kℓ_p)^n for some n ≥ 2
3. The specific H₄ lattice artifacts (pentagonal anisotropy) are bounded

**What would close it:**
Compute the lattice dispersion relation on the 600-cell graph Laplacian
and show that deviations from ω² = k²c² + m²c⁴/ℏ² scale as O(k⁶ℓ_p⁴)
or higher, confirming rotational symmetry recovery.

**Affected constants:** All (foundational assumption)

**Current status:** This is a standard problem in lattice field theory.
The H₄ lattice is expected to behave well due to its high symmetry, but
a proof specific to the 600-cell geometry has not been published.

---

## Relationship to Existing Audit

The `verification/audit/SUMMARY.md` identifies 5 PARTIALLY_DERIVED constants
and 6 flagged issues. The overlap with this gap analysis:

| Audit Issue | Related Gap |
|-------------|-------------|
| Lepton sign patterns (#4, #5) | Related to GAP-4 (mass matrix diagonalization) |
| Electron exponent 27 (#37) | Independent (representation theory question) |
| Factor 6 in m_p/m_e (#9) | Contained in GAP-5 (composite derivation) |
| H₀ unit prefactor (#24) | Contained in GAP-6 (cosmological derivation) |
| V_cb combination (#15) | Independent (CKM computation) |
| T_CMB units (#32) | Contained in GAP-6 (cosmological derivation) |

The audit focuses on **individual formula terms**; this document focuses on
the **derivation chain** from the Lagrangian to the formulas.

---

## Bottom Line

The GSM Lagrangian (`theory/GSM_FULL_LAGRANGIAN.md`) is **structurally complete**:
every constant has an identified sector (gauge, fermion, Higgs, gravity, composite).
The 7 gaps are not in the framework itself but in the **derivation chain** —
explicitly computing the φ-formulas from the lattice action's equations of motion,
rather than postulating them independently.

**Priority ordering for closing gaps:**

1. **GAP-3** (QCD running) — Most tractable; standard lattice perturbation theory
2. **GAP-4** (m_u/m_d) — Requires explicit mass matrix computation
3. **GAP-6** (cosmology) — High impact; connects Regge gravity to observations
4. **GAP-1** (Higgs RG) — Standard one-loop computation on novel lattice
5. **GAP-2** (EW triangle) — Expected from radiative corrections
6. **GAP-5** (composites) — Hardest; requires non-perturbative lattice QCD
7. **GAP-7** (Lorentz) — Standard lattice theory argument, needs formalization
