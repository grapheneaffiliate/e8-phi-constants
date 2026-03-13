# CLAUDE.md — GSM Theory of Everything

## Project Overview
The **Geometric Standard Model (GSM)** derives **58 fundamental constants** of nature —
plus a complete dynamical framework, quantum gravity, and resolutions to physics' greatest
open problems — from a single geometric principle: **Physics ≡ Geometry(E₈ → H₄)**.

Zero free parameters. Median deviation < 0.05%. Independent experimental confirmation.

## What Already Exists (Do Not Recreate)
- **gsm_solver.py** (110K) — Self-sustaining solver: all 58 constants, validation, discovery, predictions
- **verification/** (24 scripts) — Per-sector derivation scripts, Bell tests, uniqueness tests
- **theory/** (11 docs) — Wave equation, Lagrangians, Regge gravity, GW echoes, cosmic birefringence, firewall resolution, ten great problems
- **simulation/** (7 scripts) — 600-cell wave, fermion Dirac, Higgs, Regge EOM, GW echoes, LIGO templates
- **quantum_vacuum_discovery/** — E₈ Hum (22.80σ), CHSH proofs (3 algebraic + brute force), Bell meta-analysis
- **appendices/** (7 docs) — Formal proofs, formalization, Casimir proofs, uniqueness, alpha derivation, critic response, E₈→SM embedding
- **pentagonal_prism_bell_bound.md/.tex/.pdf** — Publication-ready Bell bound paper

## Key Mathematical Objects
- **φ** = (1+√5)/2, **ε** = 28/248, **h** = 30, **rank** = 8, **dim(E₈)** = 248
- Casimir degrees: {2, 8, 12, 14, 18, 20, 24, 30}
- E₈ exponents: {1, 7, 11, 13, 17, 19, 23, 29}
- "φ-Lucas" L_n = φⁿ + φ⁻ⁿ (real-valued) — L₃² = 20 exactly
- Master equation: α⁻¹ = 137 + φ⁻⁷ + φ⁻¹⁴ + φ⁻¹⁶ - φ⁻⁸/248
- See FORMULAS.md for complete reference of all 58 formulas

## Commands
```bash
python3 gsm_solver.py                              # All 58 constants + full pipeline
python3 gsm_solver.py --all                         # + dynamics + unification
python3 verification/verify_all.py                  # Original 26 constants
python3 quantum_vacuum_discovery/test_gsm_chsh.py --test  # Bell theorem (29 tests)
python3 verification/firewall_validation.py         # Firewall paradox (8 checks)
python3 verification/ten_problems_validation.py     # Ten great problems (25 checks)
python3 verification/lucas_periodicity_test.py      # E₈ Hum replication
```

## Development Principles
1. **Zero free parameters** — every number traces to E₈/H₄ geometry
2. **No numerology** — null hypothesis p < 0.001 required for every formula
3. **Honest classification** — FULLY_DERIVED, PARTIALLY_DERIVED, or CONJECTURED
4. **Test everything** — all verification scripts must pass before any commit
5. **One task per run** — focused, complete, validated, committed
6. **Preserve what works** — do not rewrite solid derivations
7. **Brutal honesty** — if a derivation has gaps, flag them, don't hide them

## Current Priority
Check the priority matrix in the prompt. Roughly:
Fix errors > null hypothesis tests > audit formulas > formal proofs > Lagrangian consistency >
dependency graph > upgrade Framework→Resolved > extend theory > comparisons > packaging
