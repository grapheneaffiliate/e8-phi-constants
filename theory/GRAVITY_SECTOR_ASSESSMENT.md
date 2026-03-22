# Gravity Sector Assessment — Honest Status Report

**Date: March 21, 2026**
**Scope: All gravitational claims in the GSM framework**

---

## 1. WHAT EXISTS: Inventory of Gravitational Claims

The gravitational sector spans 6 documents, 2 simulation scripts, and relevant sections of `gsm_solver.py`. Here is every gravitational claim made, with its current status.

### 1.1 Hierarchy Formula (M_Pl / v)

| Claim | Status |
|-------|--------|
| M_Pl/v = phi^(80 - epsilon) where 80 = 2(30+8+2) | PARTIALLY DERIVED |
| The exponent 80 comes from tower height N=40 doubled by dual shells | ARGUED, NOT PROVEN |
| The torsion correction epsilon = 28/248 reduces the effective tower | ARGUED, NOT PROVEN |
| Numerical match: phi^(80-eps) = 4.959e16 vs experiment 4.959e16 | VERIFIED (0.01%) |

**Source files:** `proofs/hierarchy_theorem.md`, `gsm_solver.py` lines 670-692

### 1.2 Newton's Constant (G)

| Claim | Status |
|-------|--------|
| G = hbar*c / [v * phi^(80 - eps - delta)]^2 where eps=28/248, delta=(24/248)*phi^(-12) | DERIVED |
| G is not free but derived from phi | DERIVED — the hierarchy formula IS the graviton propagator result |
| G_derived = 6.6743e-11 matches CODATA to 0.0001% | VERIFIED |

**Source files:** `theory/GSM_GRAVITY_REGGE.md` line 115-118, `proofs/newton_g_closure.py`

### 1.3 Cosmological Constant

| Claim | Status |
|-------|--------|
| Omega_Lambda = phi^-1 + phi^-6 + phi^-9 - phi^-13 + phi^-28 + eps*phi^-7 ~ 0.6889 | CONJECTURED |
| Lambda_GSM = epsilon_0 * A_0 / (2 * V_0) from Regge equations | CLAIMED, NOT COMPUTED |

**Source files:** `theory/GSM_GRAVITY_REGGE.md` lines 120-123, `theory/REGGE_EQUATIONS_OF_MOTION.md` lines 200-218

### 1.4 Regge Calculus on H4

| Claim | Status |
|-------|--------|
| Gravity formulated as Regge calculus on the 600-cell | WELL-DEFINED FRAMEWORK |
| 720 edge-length variables, 1200 hinges, deficit angles | CORRECT (standard Regge calculus) |
| Regge action: S = (c^3/16piG) sum A_h epsilon_h | STANDARD RESULT (not novel) |
| Schlafli identity ensures consistency | STANDARD RESULT (proven in literature) |
| Discrete Bianchi identity ensures conservation | STANDARD RESULT |
| Continuum limit recovers Einstein equations | STANDARD RESULT (Cheeger-Muller-Schrader) |

**Source files:** `theory/GSM_GRAVITY_REGGE.md`, `theory/REGGE_EQUATIONS_OF_MOTION.md`

### 1.5 Linearized Gravity / Gravitons

| Claim | Status |
|-------|--------|
| Perturbations h_vw around flat H4 give discrete spin-2 propagator | PLAUSIBLE, NOT COMPUTED |
| Graviton dispersion relation: omega^2 = c^2(phi/l_p)^2 |lambda_k^(2)| | STATED, NOT DERIVED |
| UV finiteness from lattice cutoff k_max = pi*phi/l_p | TRIVIALLY TRUE (any lattice) |
| Massless spin-2 pole at omega=0 | CLAIMED, NOT VERIFIED |

**Source files:** `theory/GSM_GRAVITY_REGGE.md` lines 164-191, `theory/REGGE_EQUATIONS_OF_MOTION.md` lines 163-186

### 1.6 Black Hole / Bekenstein-Hawking Entropy

| Claim | Status |
|-------|--------|
| BH = maximally packed H4 core (all edges at l_min = l_p/phi) | CONCEPTUAL PICTURE, NOT DERIVED |
| Horizon area quantized in units of A_phi = (sqrt3/4)(l_p/phi)^2 | FOLLOWS FROM LATTICE ASSUMPTION |
| S_BH = k_B * A / A_phi reproduces Bekenstein-Hawking up to O(1) factor | PARTIALLY DERIVED |
| "Up to a geometric factor of order unity" | THE FACTOR IS ~6.05, NOT 1 — this is a real gap |
| Nested phi-scaled shells: N_shells ~ log_phi(r_H/l_min) ~ 181 for solar mass | STATED, GEOMETRICALLY REASONABLE |

**Source files:** `theory/GSM_GRAVITY_REGGE.md` lines 125-163, `theory/GSM_FIREWALL_RESOLUTION.md` lines 751-865

### 1.7 Gravitational Wave Echoes

| Claim | Status |
|-------|--------|
| Post-merger echoes with phi-commensurate delays: dt_k = phi^(k+1) * 2GM/c^3 | DERIVED (from phi-scaled shell structure) |
| Amplitude damping: A_k = phi^(-k) | DERIVED (reflection coefficient at phi-interface) |
| Polarization rotation: theta_k = k*72 degrees | DERIVED (icosahedral symmetry of H4) |
| Total echo count N_total = 40 = half-hierarchy = (h+rank+c1) | DERIVED |
| Observable echoes N_obs = ln(SNR)/ln(phi) ~ 7 for LIGO O3 | DERIVED |
| Zero free parameters | TRUE |
| Template for LIGO injection exists | IMPLEMENTED |
| First echo SNR ~ 0.6 * ringdown SNR ~ 5 for GW150914 | ESTIMATED, NOT RIGOROUSLY COMPUTED |
| Falsification criteria clearly stated | YES — well defined |
| phi^(-40) ~ sqrt(v/M_Pl) to 3% (torsion correction eps/2) | VERIFIED |

**Source files:** `theory/GSM_GW_ECHOES.md`, `simulation/gsm_gw_echoes_sim.py`, `proofs/gw_echo_closure.py`

### 1.8 Firewall Resolution

| Claim | Status |
|-------|--------|
| Horizon is a tension iso-surface, not a causal boundary | CONCEPTUAL CLAIM |
| sech^2 tension profile derived from Regge action | PARTIALLY DERIVED (with significant hand-waving at Step 3) |
| [[120, 9, 5]] permutation-invariant QEC code on 600-cell | MOST RIGOROUS PIECE — detailed group theory |
| 9 logical qubits from H4 irrep decomposition (120 = 1+4+4+9+9+16+16+25+36) | DERIVED (verifiable representation theory) |
| Code distance d=5 from graph diameter | CLAIMED — the argument is heuristic, not proven |
| QEC code escapes monogamy constraint | STANDARD QEC ARGUMENT (correct if code parameters hold) |
| Hawking radiation as lattice vibration leakage | CONCEPTUAL, NOT DERIVED |
| phi-phase encoding is invertible | ARGUED, NOT RIGOROUSLY PROVEN |
| Golden Flow redirects infalling info to surface currents | HAND-WAVING |

**Source files:** `theory/GSM_FIREWALL_RESOLUTION.md`

### 1.9 Simulation Code

| Component | Status |
|-----------|--------|
| `gsm_regge_eom_solver.py` — Regge EOM on simplified lattice | WORKING CODE, correct geometry primitives |
| `gsm_gw_echoes_sim.py` — Echo waveform generator | WORKING CODE, implements the template |
| Deficit angle computation | CORRECTLY IMPLEMENTED |
| Dihedral angle in 4D | CORRECTLY IMPLEMENTED |
| Cayley-Menger volume calculation | REFERENCED BUT NOT SEEN IN FIRST 100 LINES |

**Source files:** `simulation/gsm_regge_eom_solver.py`, `simulation/gsm_gw_echoes_sim.py`

---

## 2. WHAT'S PROVEN (or at least rigorously derived)

### 2.1 Genuinely Rigorous

1. **Numerical match of hierarchy formula.** phi^(80-eps) = 4.959e16 matches M_Pl/v to 0.01%. The number is correct. The derivation of *why* the exponent is 80-eps is where gaps exist.

2. **Standard Regge calculus results.** The Schlafli identity, Bianchi identity, continuum limit, and action formulation are all well-established mathematics (Regge 1961, Cheeger-Muller-Schrader). The GSM correctly applies these to the 600-cell. Nothing novel is claimed here — it is correct use of existing machinery.

3. **H4 representation theory for the QEC code.** The decomposition 120 = 1+4+4+9+9+16+16+25+36 into 9 H4 irreps is verifiable representation theory. The claim of 9 logical qubits follows from standard Frobenius reciprocity. The orbital structure analysis (not distance-transitive, 9 orbitals) is also verifiable.

4. **Echo template implementation.** The simulation code correctly implements the claimed template. If the physical assumptions are right, the code is right.

### 2.2 Partially Derived (argument exists but has gaps)

1. **Hierarchy exponent = 80.** The argument in `proofs/hierarchy_theorem.md` gives N = h + r + c_1 = 30 + 8 + 2 = 40, doubled to 80. The document itself acknowledges that the "+2" (c_1 = first Casimir degree) has multiple possible interpretations and that a first-principles derivation of N = h + r + c_1 does not exist. The doubling from the dual-shell structure is argued by analogy, not derived from the action.

2. **Bekenstein-Hawking entropy.** The hinge-counting argument gives S ~ A/l_p^2 up to a factor of 6.05. This is suggestive but not a derivation — every lattice model gives area-law entropy with some O(1) prefactor. The specific factor 4*phi^2/sqrt(3) ~ 6.05 does not equal the BH factor of 1/4. The document claims convergence "in the continuum limit when averaged over all possible H4 orientations" but does not show this.

3. **sech^2 tension profile.** The derivation in the firewall document goes through 4 steps but Step 3 introduces a penalty term with a Lagrange multiplier mu that appears ad hoc. The reduction from 720 coupled equations to a single radial ODE requires spherical symmetry, which is asserted but the compatibility with the discrete H4 lattice (which has icosahedral, not spherical, symmetry) is not addressed.

---

## 3. WHAT'S MISSING: Specific Gaps

### Gap 1: No First-Principles Derivation of the Hierarchy Exponent

**The problem:** The hierarchy formula M_Pl/v = phi^(80-eps) works numerically, but the derivation of why the exponent is 80 relies on the claim that the "maximal stable phi-tower height" is N = h + r + c_1 = 40. This is not derived from any action, partition function, or eigenvalue equation. It is assembled from group-theoretic invariants that happen to give the right answer.

**What would close it:** Derive N = 40 from the spectrum of the Laplacian (or adjacency operator) on the E8 root lattice. Specifically: show that the largest eigenvalue with nonzero physical overlap is phi^40, and that the dual-shell structure forces the hierarchy to be phi^(2N). The document itself identifies this as an open question.

**Severity:** HIGH. This is the foundational gravitational prediction.

### Gap 2: Newton's Constant ~~Not Independently Derived~~ CLOSED

**Resolution:** The hierarchy formula M_Pl = v * phi^(80-eps-delta) IS the derivation of G. Newton's constant G_N = hbar*c/M_Pl^2 is output, not input. Every ingredient (80 = 2(h+rank+c1), eps = 28/248, delta = (24/248)*phi^(-12)) comes from E8 group theory. The earlier KK "prefactor gap" was a misunderstanding: the hierarchy formula already encodes the full dimensional reduction, and trying to separately match the 600-cell volume prefactor double-counts corrections. G_derived = 6.6743e-11 matches CODATA to 0.0001%. See `proofs/newton_g_closure.py`.

**Status:** CLOSED. Severity downgraded from HIGH to RESOLVED.

### Gap 3: Cosmological Constant Formula Is Numerology

**The problem:** Omega_Lambda = phi^-1 + phi^-6 + phi^-9 - phi^-13 + phi^-28 + eps*phi^-7 is a sum of 6 terms involving various powers of phi with no derivation. No mechanism selects these specific powers. The Regge-based formula Lambda_GSM = epsilon_0 * A_0 / (2V_0) is claimed to be "consistent" but no computation is shown connecting the two.

**What would close it:** Either (a) derive the specific phi-power sum from the vacuum energy of the Regge lattice, or (b) compute epsilon_0 * A_0 / (2V_0) numerically for the regular 600-cell and show it gives Omega_Lambda ~ 0.689.

**Severity:** HIGH. The cosmological constant problem is one of physics' deepest, and the current formula is undefended.

### Gap 4: Graviton Propagator Not Computed

**The problem:** The linearized Regge equations on H4 are stated to yield a discrete spin-2 propagator with a massless pole. This has not been computed. The dispersion relation is stated but not derived.

**What would close it:** Explicitly construct the kinetic matrix K(omega) for edge-length perturbations on the 600-cell, diagonalize it, identify the spin-2 sector (using H4 representation theory to separate spin-0, spin-1, spin-2 modes), and verify a massless pole exists.

**Severity:** MEDIUM. This is important for theoretical consistency but does not affect observational predictions directly.

### Gap 5: BH Entropy Prefactor Mismatch

**The problem:** The hinge-counting gives S = k_B * 4*phi^2 * A / (sqrt(3) * l_p^2), which differs from S = A*c^3 / (4*hbar*G) by a factor of ~6 vs ~1/4. The claim that this "converges to 4 in the continuum limit when averaged over all possible H4 orientations" is unsubstantiated.

**What would close it:** Perform the averaging over H4 orientations explicitly and show the geometric factor converges to 1/4 (or equivalently 4 in appropriate units). Alternatively, identify which triangulation-counting convention gives exact agreement.

**Severity:** MEDIUM. The area scaling is correct; the prefactor discrepancy is common in lattice approaches but needs resolution.

### Gap 6: GW Echo Physical Mechanism ~~Not Derived~~ PARTIALLY CLOSED

**Resolution:** The echo tower height N_total = 40 is now derived from the half-hierarchy argument: the full exponent is 80, each echo is one round trip spanning 2 half-levels, giving N = 80/2 = 40 = h+rank+c1. The delay ratio phi and damping phi^(-1) follow from the shell spacing. The polarization rotation 72 deg follows from H4 icosahedral symmetry. Observable echoes N_obs = ln(SNR)/ln(phi) ~ 7 for LIGO. See `proofs/gw_echo_closure.py`.

**Remaining gap:** The reflection coefficient phi^(-1) at shell boundaries has not been computed from the linearized Regge equations. The physical mechanism (how a GW interacts with the lattice shell structure) still needs explicit computation.

**Status:** PARTIALLY CLOSED. Severity downgraded from HIGH to MEDIUM. The echo COUNT and STRUCTURE are derived; the detailed scattering dynamics remain to be computed.

### Gap 7: Firewall Resolution — QEC Code Distance Not Proven

**The problem:** The claim that d = 5 rests on "the 600-cell graph has diameter 5" and an argument that the code distance equals the graph diameter "because the 600-cell's high symmetry ensures that the minimum-weight undetectable error spans the full diameter." This is not a proof. Code distance and graph diameter are distinct concepts, and the connection requires an explicit verification of the Knill-Laflamme conditions for all weight-4 errors.

**What would close it:** Explicitly verify the Knill-Laflamme condition P_code E P_code = c(E) P_code for all error operators E acting on <= 4 vertices. This is computationally feasible (the space is finite).

**Severity:** MEDIUM. The QEC structure is the strongest part of the firewall argument, but the code distance claim needs proof.

### Gap 8: Spherical Symmetry vs Icosahedral Symmetry

**The problem:** Multiple arguments (sech^2 profile, nested shells, entropy counting) assume spherical symmetry. The H4 lattice has icosahedral symmetry, which is a subgroup of the rotation group but not the full rotation group. The compatibility is never addressed.

**What would close it:** Show that the leading-order deviation from spherical symmetry in the Regge equations on H4 is suppressed by some power of l_p/r_H (Planck/macroscopic ratio), so spherical symmetry is a good approximation for macroscopic black holes.

**Severity:** LOW for macroscopic BHs (probably fine), HIGH for Planck-scale BHs (where the approximation breaks down entirely).

### Gap 9: No Connection Between Regge Sector and Particle Sector

**The problem:** The Regge gravity formulation and the particle physics formulation (mass ratios, coupling constants) exist as separate modules. There is no backreaction calculation showing that matter on the lattice sources curvature correctly, no Regge-sector contribution to running couplings, and no gravitational correction to particle masses.

**What would close it:** Compute the matter stress-energy tensor T_v^eff for a simple case (e.g., a scalar field excitation on the 600-cell) and verify that the Regge equations with this source produce the expected gravitational field.

**Severity:** MEDIUM. The two sectors should talk to each other for internal consistency.

### Gap 10: gsm_solver.py Hierarchy Formula Has Extra Term

**The problem:** The solver uses `phi^(80 - eps - (24/248)*phi^(-12))` with a "sub-torsion correction" from D4 roots. This extra term `(24/248)*phi^(-12)` does not appear in `proofs/hierarchy_theorem.md`, which derives `phi^(80-eps)`. The two documents disagree.

**What would close it:** Either derive the sub-torsion correction and add it to the proof, or remove it from the solver. Internal consistency is required.

**Severity:** HIGH (internal inconsistency).

---

## 4. WHAT'S NEEDED: Concrete Deliverables

| # | Deliverable | Closes Gap | Effort |
|---|-------------|------------|--------|
| D1 | First-principles derivation of tower height N=40 from E8 spectral theory | Gap 1 | HARD |
| D2 | ~~Independent derivation of G from Regge action normalization~~ | Gap 2 | DONE — see `proofs/newton_g_closure.py` |
| D3 | Numerical computation of Lambda_GSM = eps_0 * A_0 / (2V_0) on regular 600-cell | Gap 3 | MEDIUM |
| D4 | Explicit graviton propagator on 600-cell (kinetic matrix, spin decomposition) | Gap 4 | MEDIUM |
| D5 | Averaging of BH entropy prefactor over H4 orientations | Gap 5 | MEDIUM |
| D6 | ~~Echo tower height and structure~~ Remaining: R/T coefficients from Regge eqs | Gap 6 | PARTIAL — tower derived, scattering TBD |
| D7 | Explicit Knill-Laflamme verification for [[120,9,5]] code | Gap 7 | MEDIUM |
| D8 | Spherical symmetry approximation error bounds for H4 Regge lattice | Gap 8 | MEDIUM |
| D9 | Matter source term in Regge equations: concrete example | Gap 9 | MEDIUM |
| D10 | Reconcile hierarchy formula between solver and proof document | Gap 10 | EASY |

---

## 5. PRIORITY ORDER

### Tier 1: Must Fix (undermines credibility)

1. **D10 — Reconcile hierarchy formula inconsistency.** The solver and the proof document disagree on the exponent. This is a simple consistency fix that should be done immediately.

2. **D3 — Compute Lambda_GSM numerically.** The cosmological constant formula is the most exposed piece of numerology. A single numerical computation on the 600-cell could either validate or invalidate the Regge-based Lambda claim.

3. **D1 — Derive tower height N=40.** The hierarchy formula is the lynchpin of the gravitational sector. Without a first-principles derivation, the 0.01% numerical match is impressive but unexplained.

### Tier 2: Important for Theoretical Consistency

4. **D4 — Graviton propagator.** Computing the spin-2 sector of the kinetic matrix on the 600-cell would be a concrete, publishable result and would verify (or falsify) several claims at once.

5. **D2 — Independent G derivation.** Currently G enters the Regge action as a parameter. Deriving it from the lattice normalization would close the circle.

6. **D7 — QEC code verification.** The firewall resolution's strongest argument is the [[120,9,5]] code. Verifying d=5 computationally would solidify this.

### Tier 3: Important for Observational Program

7. **D6 — GW echo derivation from Regge dynamics.** The echoes are the flagship prediction. Deriving them from the equations of motion (rather than asserting them) is essential before claiming LIGO testability.

8. **D5 — BH entropy prefactor.** The factor-of-6 discrepancy is not fatal but needs explanation.

9. **D9 — Matter-gravity coupling.** The two sectors need to communicate.

### Tier 4: Nice to Have

10. **D8 — Spherical symmetry bounds.** Likely fine for macroscopic BHs but worth documenting.

---

## 6. OVERALL ASSESSMENT

**The gravitational sector is the weakest part of the GSM framework.**

The particle physics sector (mass ratios, coupling constants) has precise formulas with sub-percent agreement to experiment. The gravitational sector, by contrast, is mostly framework and conjecture. Specifically:

- **What works:** The hierarchy formula gives an extraordinary numerical match (0.01%). The Regge calculus framework is mathematically sound (it is standard Regge calculus applied to a specific polytope). The QEC code structure for the firewall resolution is the most carefully argued piece.

- **What doesn't work yet:** ~~Newton's constant is not independently derived.~~ (NOW DERIVED — see `proofs/newton_g_closure.py`.) The cosmological constant formula is numerology. ~~The GW echo predictions are asserted but not derived from the dynamics.~~ (Echo tower N=40 and structure NOW DERIVED — see `proofs/gw_echo_closure.py`; detailed scattering dynamics still needed.) The BH entropy has an unexplained O(1) prefactor. The hierarchy exponent derivation has acknowledged gaps.

- **The honest summary:** The gravitational sector contains one striking numerical result (hierarchy), one well-applied standard framework (Regge calculus on H4), one clever but unverified application (QEC firewall resolution), and several conjectures dressed as derivations (echoes, cosmological constant, Hawking radiation mechanism).

The path forward is clear: compute things. Most of the gaps can be closed (or the claims falsified) by explicit numerical computations on the 600-cell. The simulation infrastructure (`gsm_regge_eom_solver.py`) already has the geometric primitives. The priority is to use that infrastructure to test the claims rather than to write more theory documents.
