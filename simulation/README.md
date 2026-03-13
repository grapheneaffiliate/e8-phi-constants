# GSM Simulation Scripts

Numerical simulations implementing the dynamical framework (v2.0) of the Geometric Standard Model. All scripts derive physics from E₈ → H₄ projection with zero free parameters.

## Scripts

| Script | Description | Output |
|--------|-------------|--------|
| `gsm_wave_600cell.py` | Scalar field propagation on the 120-vertex H₄ 600-cell using the Golden Flow wave equation | Eigenmode spectrum, field evolution |
| `gsm_full_lagrangian_sim.py` | All-sector GSM Lagrangian on the H₄ lattice (scalar, fermion, Higgs, gauge, gravity) | Verification of golden ratio identities |
| `gsm_fermion_dirac_sim.py` | Discrete Dirac equation on the H₄ 600-cell; verifies geometric mass ratios from two φ-scaled copies | Spinor fields, mass ratio checks |
| `gsm_gw_echoes_sim.py` | Gravitational wave echoes with φ-commensurate delays, φ⁻ᵏ damping, and 72° polarization rotations | Echo waveforms (strain data) |
| `gsm_regge_eom_solver.py` | Discrete Einstein-Regge equations on simplified H₄ lattice: deficit angles, Schläfli identity, graviton modes | Simplex geometry, gravitational modes |
| `gsm_higgs_sim.py` | Geometric Higgs mechanism via spontaneous symmetry breaking from relative displacement between two φ-scaled 600-cell copies | Higgs field evolution (leapfrog integration) |
| `gsm_ligo_template_generator.py` | LIGO-compatible GW echo templates with φ-commensurate delays for PyCBC / LALSuite / GWpy | Template banks (HDF5 / numpy arrays) |

## Quick Start

```bash
# Run any individual simulation
python3 simulation/gsm_wave_600cell.py
python3 simulation/gsm_higgs_sim.py

# Run the GW template generator
python3 simulation/gsm_ligo_template_generator.py
```

## Dependencies

- Python 3.8+
- NumPy
- SciPy (some scripts)
- JSON (template generator)

## Related Documents

- Theory: [`theory/GSM_COMPLETE_THEORY_v2.0.md`](../theory/GSM_COMPLETE_THEORY_v2.0.md)
- Wave equation: [`theory/GSM_WAVE_EQUATION.md`](../theory/GSM_WAVE_EQUATION.md)
- GW echoes: [`theory/GSM_GW_ECHOES.md`](../theory/GSM_GW_ECHOES.md)
- Regge gravity: [`theory/GSM_GRAVITY_REGGE.md`](../theory/GSM_GRAVITY_REGGE.md)
- Higgs sector: [`theory/GSM_HIGGS_LAGRANGIAN.md`](../theory/GSM_HIGGS_LAGRANGIAN.md)
