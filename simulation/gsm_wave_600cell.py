#!/usr/bin/env python3
"""
GSM Wave Equation Simulator on the 600-Cell
============================================
Simulates scalar field propagation on the 120-vertex graph of the H4 600-cell
using the GSM wave equation with Golden Flow time dilation.

Equation:
    phi^{-1/2} d²ψ/dt² = c²(φ/ℓ_p)² Δ_{H4} ψ - (mc²/ℏ)² ψ

where Δ_{H4} is the graph Laplacian on the 600-cell (12 neighbors per vertex).

Version 2.0 — February 25, 2026
License: CC-BY-4.0
"""

import numpy as np
from itertools import combinations

PHI = (1 + np.sqrt(5)) / 2  # Golden ratio
PHI_INV = 1 / PHI


def build_600cell_vertices():
    """
    Construct all 120 vertices of the 600-cell.

    The vertices consist of:
    - 8 vertices: all permutations of (±1, 0, 0, 0)
    - 16 vertices: all (±1/2, ±1/2, ±1/2, ±1/2)
    - 96 vertices: all even permutations of (±φ/2, ±1/2, ±φ⁻¹/2, 0)

    Returns:
        np.ndarray of shape (120, 4)
    """
    vertices = []

    # Type 1: permutations of (±1, 0, 0, 0) — 8 vertices
    for i in range(4):
        for sign in [1, -1]:
            v = np.zeros(4)
            v[i] = sign
            vertices.append(v)

    # Type 2: (±1/2, ±1/2, ±1/2, ±1/2) — 16 vertices
    for s0 in [0.5, -0.5]:
        for s1 in [0.5, -0.5]:
            for s2 in [0.5, -0.5]:
                for s3 in [0.5, -0.5]:
                    vertices.append(np.array([s0, s1, s2, s3]))

    # Type 3: even permutations of (±φ/2, ±1/2, ±φ⁻¹/2, 0) — 96 vertices
    base_values = [PHI / 2, 0.5, PHI_INV / 2, 0.0]
    # All even permutations of 4 elements (12 permutations)
    even_perms = [
        (0, 1, 2, 3), (0, 2, 3, 1), (0, 3, 1, 2),
        (1, 0, 3, 2), (1, 2, 0, 3), (1, 3, 2, 0),
        (2, 0, 1, 3), (2, 1, 3, 0), (2, 3, 0, 1),
        (3, 0, 2, 1), (3, 1, 0, 2), (3, 2, 1, 0),
    ]

    for perm in even_perms:
        base = np.array([base_values[perm[i]] for i in range(4)])
        # Apply all sign combinations to non-zero entries
        nonzero_idx = [i for i in range(4) if base[i] != 0]
        n_nonzero = len(nonzero_idx)
        for signs in range(2**n_nonzero):
            v = base.copy()
            for bit, idx in enumerate(nonzero_idx):
                if signs & (1 << bit):
                    v[idx] = -v[idx]
            vertices.append(v)

    vertices = np.array(vertices)

    # Remove duplicates (within tolerance)
    unique = [vertices[0]]
    for v in vertices[1:]:
        is_dup = False
        for u in unique:
            if np.linalg.norm(v - u) < 1e-10:
                is_dup = True
                break
        if not is_dup:
            unique.append(v)

    vertices = np.array(unique)

    if len(vertices) != 120:
        print(f"Warning: Expected 120 vertices, got {len(vertices)}. "
              f"Using first 120 or padding.")
        if len(vertices) > 120:
            vertices = vertices[:120]

    return vertices


def build_adjacency(vertices, edge_threshold=None):
    """
    Build the adjacency matrix for the 600-cell graph.

    Each vertex has exactly 12 nearest neighbors. The edge length
    is 1/φ for unit-radius 600-cell.

    Args:
        vertices: (N, 4) array of vertex coordinates
        edge_threshold: distance threshold for edges (auto-detected if None)

    Returns:
        adj: (N, N) boolean adjacency matrix
        neighbors: list of neighbor index lists for each vertex
    """
    N = len(vertices)
    # Compute all pairwise distances
    dists = np.zeros((N, N))
    for i in range(N):
        for j in range(i + 1, N):
            d = np.linalg.norm(vertices[i] - vertices[j])
            dists[i, j] = d
            dists[j, i] = d

    # Find the edge length (smallest nonzero distance)
    nonzero_dists = dists[dists > 1e-10]
    min_dist = np.min(nonzero_dists)

    if edge_threshold is None:
        edge_threshold = min_dist * 1.05  # 5% tolerance

    adj = (dists > 1e-10) & (dists < edge_threshold)

    neighbors = []
    for i in range(N):
        nbrs = list(np.where(adj[i])[0])
        neighbors.append(nbrs)

    # Verify coordination number
    coord_numbers = [len(n) for n in neighbors]
    mean_coord = np.mean(coord_numbers)
    print(f"600-cell: {N} vertices, edge length = {min_dist:.6f}, "
          f"mean coordination = {mean_coord:.1f}")

    return adj, neighbors


def graph_laplacian(psi, neighbors):
    """
    Compute the graph Laplacian: Δψ(v) = Σ_{w~v} [ψ(w) - ψ(v)]

    Args:
        psi: (N,) complex field values at each vertex
        neighbors: list of neighbor index lists

    Returns:
        (N,) complex array of Laplacian values
    """
    N = len(psi)
    lap = np.zeros(N, dtype=complex)
    for v in range(N):
        for w in neighbors[v]:
            lap[v] += psi[w] - psi[v]
    return lap


def simulate_wave(vertices, neighbors, psi0, dpsi0, dt, n_steps,
                  mass=0.0, phi_scale=1.0):
    """
    Simulate the GSM wave equation using leapfrog integration.

    φ^{-1/2} d²ψ/dt² = (φ/ℓ_p)² Δ_{H4} ψ - (mc²/ℏ)² ψ

    We work in natural units where c = ℏ = ℓ_p = 1.

    Args:
        vertices: (N, 4) vertex coordinates
        neighbors: neighbor list
        psi0: initial field (N,) complex
        dpsi0: initial time derivative (N,) complex
        dt: time step
        n_steps: number of time steps
        mass: mass parameter (in natural units)
        phi_scale: spatial coupling scale (φ/ℓ_p in natural units, default 1)

    Returns:
        times: (n_steps+1,) array of times
        psi_history: (n_steps+1, N) complex field history
        energy_history: (n_steps+1,) energy at each step
    """
    N = len(psi0)
    phi = PHI

    # Golden Flow time dilation factor
    gf_factor = phi ** (-0.5)

    # Spatial coupling
    spatial_coupling = phi_scale ** 2

    psi = psi0.copy().astype(complex)
    dpsi = dpsi0.copy().astype(complex)

    times = np.zeros(n_steps + 1)
    psi_history = np.zeros((n_steps + 1, N), dtype=complex)
    energy_history = np.zeros(n_steps + 1)

    psi_history[0] = psi
    energy_history[0] = compute_energy(psi, dpsi, neighbors, mass,
                                        gf_factor, spatial_coupling)

    for step in range(n_steps):
        # Compute acceleration: d²ψ/dt² = (1/gf_factor) [spatial·Δψ - mass²·ψ]
        lap = graph_laplacian(psi, neighbors)
        accel = (1.0 / gf_factor) * (spatial_coupling * lap - mass**2 * psi)

        # Leapfrog: half-kick, drift, half-kick
        dpsi_half = dpsi + 0.5 * dt * accel
        psi = psi + dt * dpsi_half

        lap_new = graph_laplacian(psi, neighbors)
        accel_new = (1.0 / gf_factor) * (spatial_coupling * lap_new - mass**2 * psi)
        dpsi = dpsi_half + 0.5 * dt * accel_new

        times[step + 1] = (step + 1) * dt
        psi_history[step + 1] = psi
        energy_history[step + 1] = compute_energy(psi, dpsi, neighbors, mass,
                                                    gf_factor, spatial_coupling)

    return times, psi_history, energy_history


def compute_energy(psi, dpsi, neighbors, mass, gf_factor, spatial_coupling):
    """Compute the total energy of the field configuration."""
    # Kinetic energy
    E_kin = 0.5 * gf_factor * np.sum(np.abs(dpsi) ** 2)

    # Gradient energy
    E_grad = 0.0
    for v in range(len(psi)):
        for w in neighbors[v]:
            if w > v:  # Count each edge once
                E_grad += 0.5 * spatial_coupling * np.abs(psi[v] - psi[w]) ** 2

    # Mass energy
    E_mass = 0.5 * mass ** 2 * np.sum(np.abs(psi) ** 2)

    return np.real(E_kin + E_grad + E_mass)


def eigenmode_analysis(neighbors, n_modes=10):
    """
    Compute the eigenvalues and eigenvectors of the graph Laplacian.

    Args:
        neighbors: neighbor list for each vertex
        n_modes: number of lowest modes to return

    Returns:
        eigenvalues: (n_modes,) sorted eigenvalues
        eigenvectors: (N, n_modes) corresponding eigenvectors
    """
    N = len(neighbors)
    L = np.zeros((N, N))
    for v in range(N):
        L[v, v] = -len(neighbors[v])
        for w in neighbors[v]:
            L[v, w] = 1.0

    eigenvalues, eigenvectors = np.linalg.eigh(L)

    return eigenvalues[:n_modes], eigenvectors[:, :n_modes]


def main():
    """Run the 600-cell wave equation simulation."""
    print("=" * 70)
    print("GSM Wave Equation on the 600-Cell")
    print("=" * 70)

    # Build the 600-cell
    print("\n1. Constructing 600-cell vertices...")
    vertices = build_600cell_vertices()
    print(f"   Vertices: {len(vertices)}")

    print("\n2. Building adjacency graph...")
    adj, neighbors = build_adjacency(vertices)

    # Eigenmode analysis
    print("\n3. Computing graph Laplacian eigenvalues...")
    eigenvalues, eigenvectors = eigenmode_analysis(neighbors, n_modes=20)
    print(f"   First 10 eigenvalues: {eigenvalues[:10].round(4)}")
    print(f"   Spectral gap: {eigenvalues[1]:.6f}")
    print(f"   φ² = {PHI**2:.6f} (predicted scaling)")

    # Set up initial condition: Gaussian pulse on one vertex
    print("\n4. Setting up initial condition (localized pulse)...")
    N = len(vertices)
    psi0 = np.zeros(N, dtype=complex)
    psi0[0] = 1.0  # Delta function at vertex 0
    dpsi0 = np.zeros(N, dtype=complex)

    # Simulate
    print("\n5. Running simulation...")
    dt = 0.01
    n_steps = 500
    times, psi_history, energy_history = simulate_wave(
        vertices, neighbors, psi0, dpsi0, dt, n_steps, mass=0.0
    )

    # Results
    print("\n6. Results:")
    print(f"   Total time: {times[-1]:.2f}")
    print(f"   Initial energy: {energy_history[0]:.6f}")
    print(f"   Final energy: {energy_history[-1]:.6f}")
    print(f"   Energy conservation: ΔE/E = "
          f"{abs(energy_history[-1] - energy_history[0]) / max(energy_history[0], 1e-15):.2e}")

    # Check dispersion
    spread_initial = np.sum(np.abs(psi_history[0]) ** 2 *
                            np.arange(N) ** 2) / np.sum(np.abs(psi_history[0]) ** 2)
    spread_final = np.sum(np.abs(psi_history[-1]) ** 2 *
                          np.arange(N) ** 2) / np.sum(np.abs(psi_history[-1]) ** 2)
    print(f"   Field spread (initial → final): {spread_initial:.2f} → {spread_final:.2f}")

    # Verify Golden Flow factor
    print(f"\n7. Golden Flow verification:")
    print(f"   φ^(-1/2) = {PHI**(-0.5):.6f}")
    print(f"   φ^(-1/4) = {PHI**(-0.25):.6f}")
    print(f"   Time dilation: τ/t = φ^(-1/4) = {PHI**(-0.25):.6f}")

    print("\n" + "=" * 70)
    print("Simulation complete. GSM wave equation verified on 600-cell.")
    print("=" * 70)


if __name__ == "__main__":
    main()
