#!/usr/bin/env python3
"""
Bell Test Angle Calculator — Experimental Protocol for S = 4 − φ
=================================================================

Computes all measurement angles, expected correlations, and required
statistics for an experimental Bell test of the GSM prediction S = 4 − φ.

Provides output in formats useful for different experimental platforms:
  - Photonic (polarizer angles in degrees)
  - NV center / trapped ion (Bloch sphere polar + azimuthal angles)
  - General (Cartesian unit vectors on S²)

Also computes:
  - Expected coincidence rates for each setting combination
  - Statistical error as a function of event count
  - Required run time for 3σ and 5σ significance
  - Comparison with standard CHSH-optimal angles

Author: Timothy McGirl
Repository: https://github.com/grapheneaffiliate/e8-phi-constants
License: CC BY 4.0
"""

import math
from typing import List, Tuple, Dict

PHI = (1 + math.sqrt(5)) / 2
GSM_BOUND = 4 - PHI
TSIRELSON = 2 * math.sqrt(2)
CLASSICAL = 2.0

# =============================================================================
# PENTAGONAL PRISM GEOMETRY
# =============================================================================

H_SQ = 3.0 / (2.0 * PHI)   # h² = 3/(2φ) ≈ 0.9271
H = math.sqrt(H_SQ)          # h ≈ 0.9628
NORM = math.sqrt(1.0 + H_SQ) # R = √(1+h²) ≈ 1.3882
Z0 = H / NORM                # z₀ = h/R ≈ 0.6935


def prism_vertex(k: int, sign: int) -> Tuple[float, float, float]:
    """
    Compute unit vector for vertex k (0-4) on ring sign (+1 or -1).

    Returns (x, y, z) on S².
    """
    angle = 2 * math.pi * k / 5
    x = math.cos(angle) / NORM
    y = math.sin(angle) / NORM
    z = sign * H / NORM
    return (x, y, z)


def all_vertices() -> List[Tuple[int, int, Tuple[float, float, float]]]:
    """All 10 prism vertices as (k, sign, (x,y,z))."""
    verts = []
    for k in range(5):
        for sign in [+1, -1]:
            verts.append((k, sign, prism_vertex(k, sign)))
    return verts


def dot3(a: Tuple, b: Tuple) -> float:
    return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]


def to_spherical(v: Tuple[float, float, float]) -> Tuple[float, float]:
    """Convert Cartesian (x,y,z) to spherical (θ, ϕ) in degrees."""
    x, y, z = v
    theta = math.degrees(math.acos(z))
    phi = math.degrees(math.atan2(y, x))
    if phi < 0:
        phi += 360
    return theta, phi


def to_polarizer_angle(v: Tuple[float, float, float]) -> float:
    """
    For photonic Bell test: extract polarizer angle from xy-plane azimuth.
    Polarizer angle = half the azimuthal angle (for linear polarization).
    """
    x, y, _ = v
    phi = math.degrees(math.atan2(y, x))
    if phi < 0:
        phi += 360
    return phi / 2  # half-angle for polarization


# =============================================================================
# OPTIMAL QUADRUPLE SEARCH
# =============================================================================

def find_optimal_quadruples() -> Dict:
    """
    Brute-force search over all vertex quadruples to find those achieving
    |S| = 4 − φ. Returns the best quadruple and statistics.
    """
    best_S = 0.0
    best_quad = None
    optimal_quads = []
    total = 0

    for k_a in range(5):
        for s_a in [+1, -1]:
            va = prism_vertex(k_a, s_a)
            for k_ap in range(5):
                for s_ap in [+1, -1]:
                    if k_a == k_ap and s_a == s_ap:
                        continue
                    vap = prism_vertex(k_ap, s_ap)
                    for k_b in range(5):
                        for s_b in [+1, -1]:
                            vb = prism_vertex(k_b, s_b)
                            for k_bp in range(5):
                                for s_bp in [+1, -1]:
                                    if k_b == k_bp and s_b == s_bp:
                                        continue
                                    total += 1
                                    vbp = prism_vertex(k_bp, s_bp)

                                    S = (-dot3(va, vb) + dot3(va, vbp)
                                         + dot3(vap, vb) + dot3(vap, vbp))
                                    absS = abs(S)

                                    if absS > best_S + 1e-12:
                                        best_S = absS
                                        best_quad = (k_a, s_a, k_ap, s_ap,
                                                     k_b, s_b, k_bp, s_bp)
                                        optimal_quads = [best_quad]
                                    elif abs(absS - best_S) < 1e-12:
                                        optimal_quads.append(
                                            (k_a, s_a, k_ap, s_ap,
                                             k_b, s_b, k_bp, s_bp))

    return {
        "best_S": best_S,
        "best_quad": best_quad,
        "n_optimal": len(optimal_quads),
        "n_total": total,
        "target": GSM_BOUND,
        "match": math.isclose(best_S, GSM_BOUND, rel_tol=1e-10),
    }


# =============================================================================
# EXPECTED CORRELATIONS
# =============================================================================

def expected_correlations(quad: Tuple) -> Dict:
    """
    Compute expected correlations E(a,b), E(a,b'), E(a',b), E(a',b')
    for a singlet state with measurement directions from the given quadruple.
    """
    k_a, s_a, k_ap, s_ap, k_b, s_b, k_bp, s_bp = quad
    va = prism_vertex(k_a, s_a)
    vap = prism_vertex(k_ap, s_ap)
    vb = prism_vertex(k_b, s_b)
    vbp = prism_vertex(k_bp, s_bp)

    # Singlet correlation: E(x,y) = -x·y
    E_ab = -dot3(va, vb)
    E_abp = -dot3(va, vbp)
    E_apb = -dot3(vap, vb)
    E_apbp = -dot3(vap, vbp)

    # CHSH parameter matching brute-force convention:
    # S = -a·b + a·b' + a'·b + a'·b' = E(a,b) - E(a,b') - E(a',b) - E(a',b')
    # We compute |S| from dot products directly (same as brute force)
    S_dots = -dot3(va, vb) + dot3(va, vbp) + dot3(vap, vb) + dot3(vap, vbp)

    return {
        "E_ab": E_ab,
        "E_abp": E_abp,
        "E_apb": E_apb,
        "E_apbp": E_apbp,
        "S": S_dots,
        "directions": {
            "a": va, "a'": vap, "b": vb, "b'": vbp,
        }
    }


def coincidence_probabilities(E: float) -> Dict[str, float]:
    """
    From correlation E, compute coincidence probabilities.
    For singlet: P(++) = P(--) = (1-E)/4, P(+-) = P(-+) = (1+E)/4
    """
    return {
        "P_++": (1 - E) / 4,
        "P_--": (1 - E) / 4,
        "P_+-": (1 + E) / 4,
        "P_-+": (1 + E) / 4,
    }


# =============================================================================
# STATISTICAL ANALYSIS
# =============================================================================

def chsh_error(N_per_setting: int) -> float:
    """
    Statistical error on S for N events per setting combination.
    σ_S ≈ √(8/N) for 4 equiprobable settings (Poisson statistics).
    """
    return math.sqrt(8.0 / N_per_setting)


def events_for_sigma(target_sigma: float, gap: float) -> int:
    """
    How many events per setting are needed to achieve target_sigma
    significance for a given gap.
    N = 8 × (target_sigma / gap)²
    """
    return math.ceil(8 * (target_sigma / gap) ** 2)


def run_time(N_events: int, rate_hz: float) -> float:
    """Run time in hours for N total events at given rate."""
    return N_events / rate_hz / 3600


# =============================================================================
# COMPARISON WITH STANDARD CHSH ANGLES
# =============================================================================

def standard_chsh_angles() -> Dict:
    """
    Standard CHSH-optimal angles (maximizing S for Tsirelson bound).
    These are the textbook angles: 0°, 22.5°, 45°, 67.5°.
    """
    return {
        "Alice_1": 0.0,
        "Alice_2": 45.0,
        "Bob_1": 22.5,
        "Bob_2": 67.5,
        "S_max": TSIRELSON,
        "source": "Tsirelson-optimal (continuous S²)",
    }


def gsm_chsh_angles() -> Dict:
    """
    GSM pentagonal prism angles (maximizing S for H₄-constrained geometry).
    """
    result = find_optimal_quadruples()
    quad = result["best_quad"]
    corr = expected_correlations(quad)

    angles = {}
    for label, v in corr["directions"].items():
        theta, phi = to_spherical(v)
        pol = to_polarizer_angle(v)
        angles[label] = {
            "cartesian": v,
            "theta_deg": theta,
            "phi_deg": phi,
            "polarizer_deg": pol,
        }

    return {
        "angles": angles,
        "S_max": result["best_S"],
        "quad": quad,
        "source": "H₄-constrained pentagonal prism",
    }


# =============================================================================
# REPORT
# =============================================================================

def print_report():
    print("=" * 74)
    print("BELL TEST ANGLE CALCULATOR — EXPERIMENTAL PROTOCOL FOR S = 4 − φ")
    print("=" * 74)
    print()

    # --- Prism geometry ---
    print("1. PENTAGONAL PRISM GEOMETRY")
    print("-" * 74)
    print(f"  Height parameter:  h² = 3/(2φ) = {H_SQ:.10f}")
    print(f"                     h  = √(3/(2φ)) = {H:.10f}")
    print(f"  Normalization:     R  = √(1+h²) = {NORM:.10f}")
    print(f"  z-coordinate:     z₀ = h/R = {Z0:.10f}")
    print(f"  Polar angle:       θ  = arccos(z₀) = {math.degrees(math.acos(Z0)):.4f}°")
    print()

    # --- All 10 vertices ---
    print("2. ALL 10 MEASUREMENT DIRECTIONS")
    print("-" * 74)
    print(f"  {'k':>2} {'±':>2}  {'x':>10} {'y':>10} {'z':>10}  "
          f"{'θ(°)':>7} {'ϕ(°)':>7}  {'Pol(°)':>7}")
    print(f"  {'-'*68}")
    for k, sign, v in all_vertices():
        theta, phi = to_spherical(v)
        pol = to_polarizer_angle(v)
        s = "+" if sign > 0 else "−"
        print(f"  {k:>2} {s:>2}  {v[0]:>10.6f} {v[1]:>10.6f} {v[2]:>10.6f}  "
              f"{theta:>7.2f} {phi:>7.2f}  {pol:>7.2f}")
    print()

    # --- Optimal quadruple ---
    print("3. OPTIMAL CHSH QUADRUPLE")
    print("-" * 74)
    result = find_optimal_quadruples()
    print(f"  Total quadruples tested: {result['n_total']:,}")
    print(f"  Optimal quadruples:      {result['n_optimal']}")
    print(f"  Maximum |S|:             {result['best_S']:.15f}")
    print(f"  Target (4−φ):            {result['target']:.15f}")
    print(f"  Match:                   {'YES' if result['match'] else 'NO'}")
    print()

    quad = result["best_quad"]
    corr = expected_correlations(quad)
    signs = {1: "⁺", -1: "⁻"}

    k_a, s_a, k_ap, s_ap, k_b, s_b, k_bp, s_bp = quad
    print(f"  Representative optimal quadruple:")
    print(f"    a  = v{k_a}{signs[s_a]}   a' = v{k_ap}{signs[s_ap]}   "
          f"b  = v{k_b}{signs[s_b]}   b' = v{k_bp}{signs[s_bp]}")
    print()

    for label in ["a", "a'", "b", "b'"]:
        v = corr["directions"][label]
        theta, phi = to_spherical(v)
        pol = to_polarizer_angle(v)
        print(f"    {label:>2} = ({v[0]:>8.5f}, {v[1]:>8.5f}, {v[2]:>8.5f})  "
              f"θ={theta:>7.2f}° ϕ={phi:>7.2f}° pol={pol:>7.2f}°")
    print()

    # --- Expected correlations ---
    print("4. EXPECTED CORRELATIONS (singlet state)")
    print("-" * 74)
    print(f"  E(a,b)   = −a·b   = {corr['E_ab']:>+.10f}")
    print(f"  E(a,b')  = −a·b'  = {corr['E_abp']:>+.10f}")
    print(f"  E(a',b)  = −a'·b  = {corr['E_apb']:>+.10f}")
    print(f"  E(a',b') = −a'·b' = {corr['E_apbp']:>+.10f}")
    print()
    print(f"  S = −a·b + a·b' + a'·b + a'·b'  (dot product convention)")
    va, vap, vb, vbp = [corr["directions"][k] for k in ["a", "a'", "b", "b'"]]
    d_ab = dot3(va, vb)
    d_abp = dot3(va, vbp)
    d_apb = dot3(vap, vb)
    d_apbp = dot3(vap, vbp)
    print(f"    = −({d_ab:.6f}) + ({d_abp:.6f}) "
          f"+ ({d_apb:.6f}) + ({d_apbp:.6f})")
    print(f"    = {corr['S']:>+.15f}")
    print(f"    = 4 − φ ✓" if math.isclose(abs(corr['S']), GSM_BOUND, rel_tol=1e-10)
          else f"    ≠ 4 − φ ✗")
    print()

    # --- Coincidence probabilities ---
    print("5. EXPECTED COINCIDENCE PROBABILITIES")
    print("-" * 74)
    for label, E_val in [("E(a,b)", corr["E_ab"]),
                          ("E(a,b')", corr["E_abp"]),
                          ("E(a',b)", corr["E_apb"]),
                          ("E(a',b')", corr["E_apbp"])]:
        probs = coincidence_probabilities(E_val)
        print(f"  {label:>10}  P(++)={probs['P_++']:.4f}  P(--)={probs['P_--']:.4f}  "
              f"P(+-)={probs['P_+-']:.4f}  P(-+)={probs['P_-+']:.4f}")
    print()

    # --- Comparison with standard angles ---
    print("6. COMPARISON: STANDARD vs GSM ANGLES")
    print("-" * 74)
    std = standard_chsh_angles()
    print(f"  {'Setting':<16} {'Standard (°)':>14} {'GSM (°)':>14}")
    print(f"  {'-'*46}")

    gsm = gsm_chsh_angles()
    gsm_labels = {"a": "Alice 1", "a'": "Alice 2", "b": "Bob 1", "b'": "Bob 2"}
    std_vals = {"Alice 1": std["Alice_1"], "Alice 2": std["Alice_2"],
                "Bob 1": std["Bob_1"], "Bob 2": std["Bob_2"]}

    for key, label in gsm_labels.items():
        gsm_pol = gsm["angles"][key]["polarizer_deg"]
        std_val = std_vals[label]
        print(f"  {label:<16} {std_val:>14.2f} {gsm_pol:>14.2f}")

    print()
    print(f"  S_max (Standard):  {std['S_max']:.10f}  (Tsirelson 2√2)")
    print(f"  S_max (GSM):       {gsm['S_max']:.10f}  (4 − φ)")
    print(f"  Suppression:       {100*(1 - gsm['S_max']/std['S_max']):.1f}%")
    print()

    # --- Statistical requirements ---
    print("7. STATISTICAL REQUIREMENTS")
    print("-" * 74)
    gap = TSIRELSON - GSM_BOUND
    print(f"  Gap (2√2 − (4−φ)):  {gap:.6f}")
    print()

    for sigma in [3, 5, 10]:
        N = events_for_sigma(sigma, gap)
        total = 4 * N  # 4 setting combinations
        print(f"  For {sigma}σ exclusion of Tsirelson:")
        print(f"    Events per setting:  {N:>10,}")
        print(f"    Total events:        {total:>10,}")
        print(f"    σ_S:                 {chsh_error(N):.6f}")

        for rate in [10, 100, 1000]:
            t = run_time(total, rate)
            unit = "hours" if t < 24 else "days"
            val = t if t < 24 else t / 24
            print(f"    Run time ({rate:>4} Hz):  {val:>8.1f} {unit}")
        print()

    # --- Falsification criteria ---
    print("8. FALSIFICATION CRITERIA")
    print("-" * 74)
    print(f"""
  GSM FALSIFIED if:
    Any loophole-free experiment measures S > {GSM_BOUND + 3*0.05:.3f}
    (i.e., S − 3σ > {GSM_BOUND:.4f})
    with error σ_S < 0.05

  GSM CONFIRMED if:
    S = {GSM_BOUND:.3f} ± 0.03  (0σ from GSM, {gap/0.03:.0f}σ from Tsirelson)
    Multiple independent experiments converge

  INCONCLUSIVE if:
    Measured S in range [2.2, 2.5] with σ_S > 0.1
    (Cannot distinguish apparatus inefficiency from geometric bound)
""")

    # --- Summary for experimentalists ---
    print("9. QUICK REFERENCE FOR EXPERIMENTALISTS")
    print("-" * 74)
    print(f"""
  ┌─────────────────────────────────────────────────────────────────────┐
  │ PENTAGONAL PRISM BELL TEST — QUICK REFERENCE                       │
  ├─────────────────────────────────────────────────────────────────────┤
  │                                                                     │
  │ Prediction:    S_max = 4 − φ = {GSM_BOUND:.10f}              │
  │ Tsirelson:     S_max = 2√2  = {TSIRELSON:.10f}              │
  │ Gap:           Δ = {gap:.10f}                                │
  │                                                                     │
  │ Prism height:  h = √(3/(2φ)) = {H:.6f}                        │
  │ Polar angle:   θ = {math.degrees(math.acos(Z0)):.2f}° from z-axis                           │
  │ Azimuthal:     ϕ = 0°, 72°, 144°, 216°, 288°                      │
  │                                                                     │
  │ PHOTONIC SETUP (polarizer angles):                                  │
  │   Alice 1:  0.00°    Bob 1:  0.00°                                 │
  │   Alice 2: 36.00°    Bob 2: 72.00°                                 │
  │                                                                     │
  │ SPIN SETUP (Bloch sphere):                                          │
  │   θ = {math.degrees(math.acos(Z0)):.2f}° (upper) or {180-math.degrees(math.acos(Z0)):.2f}° (lower)                  │
  │   ϕ = k × 72° for k = 0,1,2,3,4                                   │
  │                                                                     │
  │ Required:  η > 84%,  >4000 events,  all loopholes closed           │
  │ Falsified: S > 2.5 at 3σ loophole-free                             │
  └─────────────────────────────────────────────────────────────────────┘
""")

    print("=" * 74)


if __name__ == "__main__":
    print_report()
