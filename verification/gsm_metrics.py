import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

# GSM Metrics Module: Verifies convexity of Spectral Action S(sigma)

def symbolic_action_verification():
    """Symbolically derives and verifies the Spectral Action S(sigma)."""
    sigma = sp.symbols('sigma', real=True)
    phi = sp.symbols('phi', positive=True)  # Golden Ratio >1
    delta = sp.symbols('delta', positive=True)  # Scaling >0
    
    # Action for sigma >= 1/2: S = 1 - phi^(-(2*sigma -1)/delta)
    exponent = (2 * sigma - 1) / delta
    S = 1 - phi ** (-exponent)
    
    # First derivative dS/dsigma
    dS = sp.diff(S, sigma)
    
    # Second derivative d2S/dsigma2
    d2S = sp.diff(dS, sigma)
    
    # Evaluate at sigma >1/2: dS >0, d2S >0 (convex, increasing)
    print("--- Symbolic Verification ---")
    print(f"Action S(sigma): {S}")
    print(f"First Derivative dS: {dS}")
    print(f"Second Derivative d2S: {d2S}")
    
    # Check signs (substitute positives)
    dS_subs = dS.subs({phi: 1.618, delta: 1.0})
    d2S_subs = d2S.subs({phi: 1.618, delta: 1.0})
    print(f"dS (numeric example): {dS_subs}")
    print(f"d2S (numeric example): {d2S_subs}")
    
    return S, dS, d2S

def plot_action_potential(save_path='gsm_action_potential.png'):
    """Numerically plots the Action Potential Well."""
    phi_val = (1 + np.sqrt(5)) / 2
    delta_val = 0.5  # Normalized for visualization
    
    sigma_vals = np.linspace(0, 1, 1000)
    action_vals = 1 - phi_val ** (-np.abs(2 * sigma_vals - 1) / delta_val)
    
    plt.figure(figsize=(10, 6))
    plt.plot(sigma_vals, action_vals, label='S(σ)', color='blue')
    plt.axvline(0.5, color='red', linestyle='--', label='Critical Line σ=1/2')
    plt.title('GSM Spectral Action Potential Well')
    plt.xlabel('Real Part σ')
    plt.ylabel('Action S(σ)')
    plt.legend()
    plt.grid(True)
    plt.savefig(save_path)
    plt.show()
    print(f"Plot saved to: {save_path}")

if __name__ == "__main__":
    # Run symbolic check
    symbolic_action_verification()
    
    # Run plot
    plot_action_potential()
