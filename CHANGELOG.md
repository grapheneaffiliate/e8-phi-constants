# Changelog — The Geometric Standard Model

All notable changes to this project are documented in this file.
Format follows [Keep a Changelog](https://keepachangelog.com/).

---

## [2.0] — 2026-02-25

### Added — Full Dynamic Extension

**Theory (9 new documents in `theory/`):**
- `GSM_WAVE_EQUATION.md` — Discrete Klein-Gordon on 600-cell, Golden Flow τ = φ^{-1/4}t, continuum limit proof
- `GSM_FULL_LAGRANGIAN.md` — Complete variational action for all sectors (scalar, fermion, Higgs, gauge, gravity)
- `GSM_FERMION_LAGRANGIAN.md` — Dirac equation on doubled 600-cell, SO(8) triality generations, all mass ratios
- `GSM_HIGGS_LAGRANGIAN.md` — Geometric Higgs from inter-copy displacement, VEV ∝ φ⁻¹¹, naturalness
- `GSM_GRAVITY_REGGE.md` — Full Regge calculus on H₄ lattice, deficit angles, area law, UV finiteness
- `REGGE_EQUATIONS_OF_MOTION.md` — Discrete Einstein equations with Schläfli identity proof
- `GSM_GW_ECHOES.md` — GW echo template: Δt_k = φ^{k+1}×2M, A_k = φ⁻ᵏ, θ_k = k·72° + 36°/φᵏ
- `GSM_COSMIC_BIREFRINGENCE.md` — Isotropic β = arcsin(φ⁻³) ≈ 0.292°, redshift dependence
- `GSM_COSMIC_BIREFRINGENCE_ANISOTROPIC.md` — Quadrupole + 5-fold modulation from lattice strain
- `GSM_COMPLETE_THEORY_v2.0.md` — Master unified document merging all v1.0 + v2.0 content

**Simulation Code (7 new scripts in `simulation/`):**
- `gsm_wave_600cell.py` — Wave propagation on 600-cell with eigenmode analysis
- `gsm_full_lagrangian_sim.py` — All-sector Lagrangian verification
- `gsm_fermion_dirac_sim.py` — Dirac equation, mass ratios, CKM/PMNS from geometry
- `gsm_higgs_sim.py` — Symmetry breaking dynamics, mass spectrum, naturalness
- `gsm_regge_eom_solver.py` — Regge EOM solver with Schläfli identity verification
- `gsm_gw_echoes_sim.py` — GW echo waveform generator and detection forecasts
- `gsm_ligo_template_generator.py` — LIGO-compatible template bank generator (v2.4)

**Evidence & Predictions (new folders):**
- `evidence/EVIDENCE_SUMMARY.md` — Complete catalog of convergent experimental evidence
- `predictions/GSM_PREDICTIONS_v2.0.md` — All testable predictions with timeline and falsification criteria

### Changed
- `README.md` — Added Dynamic Extension v2.0 section
- `FORMULAS.md` — Added v2.0 dynamical formulas (wave equation, echoes, birefringence, Regge)

### Framework Upgrade
- Version bumped from 1.0 → **2.0**
- Repo transitions from "static constants + geometry" to **complete dynamical unified theory**
- All new content: zero free parameters, fully falsifiable, with running simulations

---

## [1.0] — 2026-01-20 through 2026-02-02

### Core Framework
- 26 fundamental constants derived from E₈ → H₄ geometry (median error 0.016%)
- α⁻¹ = 137 + φ⁻⁷ + φ⁻¹⁴ + φ⁻¹⁶ − φ⁻⁸/248 (0.027 ppm match)
- CHSH Bell bound S ≤ 4 − φ ≈ 2.382 (three independent algebraic derivations)
- Pentagonal prism Bell bound paper (Markdown + LaTeX + PDF)

### E8 Hum Discovery (January 20, 2026)
- 22.80σ Lucas periodicity detection in LANL quantum vacuum noise
- FIG2a.csv raw data from Los Alamos ASE experiment
- Pink noise control test (16.74σ confirms non-artifact)

### Verification Infrastructure
- 18 Python verification scripts covering all sectors
- Master verification suite (`verify_all.py`)
- GSM calculator class with high-precision arithmetic
- Casimir uniqueness exhaustive search

### Appendices (A through G)
- Formal proofs, complete formalization, Casimir proofs
- Uniqueness theorem, alpha derivation, critic response
- E₈ → Standard Model embedding with explicit EM couplings

### Publications
- GSM v1 Complete paper (Markdown + LaTeX + PDF)
- Riemann Hypothesis synthesis paper
- GSM Status Report with corrected δ_CP
