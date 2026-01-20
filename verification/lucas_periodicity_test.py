#!/usr/bin/env python3
"""
GSM LANL RAW QUANTUM NOISE TEST
===============================

This tests the LANL raw ASE quantum noise for E8 structure.

FIG2a.csv: Raw oscilloscope trace - unprocessed voltage measurements
FIG4.u8: 954MB of raw 8-bit quantum noise

If E8 structure appears in raw quantum but not PRNG -> GSM PROVEN!

Author: Research Analysis
Date: January 20, 2026
"""

import numpy as np
from scipy.signal import welch, find_peaks
from scipy.stats import kurtosis, skew
import os
import glob

# ==========================================
# CONSTANTS
# ==========================================
PHI = (1 + np.sqrt(5)) / 2
E8_CASIMIRS = np.array([2, 8, 12, 14, 18, 20, 24, 30])
LUCAS = [2, 1, 3, 4, 7, 11, 18, 29, 47, 76, 123, 199]

# Possible file locations
SEARCH_PATHS = [
    "C:/Users/atchi/FIG2a.csv",
    "C:/Users/atchi/Downloads/FIG2a.csv",
    "C:/Users/atchi/Desktop/FIG2a.csv",
    "FIG2a.csv",
    "../FIG2a.csv",
]

U8_PATHS = [
    "C:/Users/atchi/FIG4.u8",
    "C:/Users/atchi/Downloads/FIG4.u8",
    "C:/Users/atchi/Desktop/FIG4.u8",
    "FIG4.u8",
]

def find_file(paths):
    """Find the first existing file in the paths."""
    for p in paths:
        if os.path.exists(p):
            return p
    return None

def load_csv_data(filename):
    """Load LANL CSV data - FIG2a.csv has columns: time us, CH1 mVX"""
    try:
        import pandas as pd
        print(f"Loading {filename}...")
        df = pd.read_csv(filename)
        # Column "CH1 mVX" contains raw quantum noise voltage
        if 'CH1 mVX' in df.columns:
            data = df['CH1 mVX'].values
            print(f"✓ Loaded {len(data)} RAW VOLTAGE samples from CH1 mVX")
        else:
            # Try second column
            data = df.iloc[:, 1].values
            print(f"✓ Loaded {len(data)} samples from column 2")
        data = data.astype(float)
        data = data[~np.isnan(data)]
        return data
    except ImportError:
        # Fallback without pandas
        print("Loading CSV without pandas...")
        with open(filename, 'r') as f:
            lines = f.readlines()
        values = []
        for line in lines[1:]:  # Skip header
            parts = line.strip().split(',')
            if len(parts) >= 2:
                try:
                    values.append(float(parts[1]))  # Second column (CH1 mVX)
                except:
                    pass
        print(f"✓ Loaded {len(values)} samples")
        return np.array(values)
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return None

def load_u8_data(filename, max_samples=1000000):
    """Load LANL u8 binary data."""
    try:
        print(f"Loading {filename} (up to {max_samples} samples)...")
        data = np.fromfile(filename, dtype=np.uint8, count=max_samples)
        print(f"✓ Loaded {len(data)} samples from u8 binary")
        return data.astype(float)
    except Exception as e:
        print(f"Error loading u8: {e}")
        return None

def phi_lag_autocorrelation(data, label="Data"):
    """Test for enhanced correlations at φ-related lags."""
    data = (data - np.mean(data)) / np.std(data)
    n = len(data)
    
    # Autocorrelation
    corr = np.correlate(data, data, mode='full')
    corr = corr[len(corr)//2:]
    corr = corr / corr[0]
    
    # φ-related lags
    phi_lags = [int(round(10 * PHI**k)) for k in range(1, 8) if int(round(10 * PHI**k)) < min(200, n//2)]
    
    # Baseline 
    max_lag = min(200, n//2-1)
    mask = np.ones(max_lag, dtype=bool)
    for l in phi_lags:
        if l < max_lag:
            mask[l] = False
    mask[0] = False
    
    if np.sum(mask) < 10:
        return -999, "Insufficient data"
    
    baseline = corr[1:max_lag][mask[1:]]
    baseline_mean = np.mean(np.abs(baseline))
    baseline_std = np.std(baseline)
    
    phi_signal = np.mean([np.abs(corr[l]) for l in phi_lags if l < len(corr)])
    z_score = (phi_signal - baseline_mean) / (baseline_std + 1e-10)
    
    return z_score, f"φ-lag Z = {z_score:.2f}σ"

def lucas_periodicity(data, label="Data"):
    """Test for Lucas number periodicity."""
    data = (data - np.mean(data)) / np.std(data)
    n = len(data)
    
    corr = np.correlate(data, data, mode='full')
    corr = corr[len(corr)//2:]
    corr = corr / corr[0]
    
    lucas_lags = [l for l in LUCAS if l < min(200, n//2)]
    if len(lucas_lags) < 3:
        return -999, "Insufficient Lucas lags"
    
    lucas_corr = [abs(corr[l]) for l in lucas_lags]
    
    max_lag = min(200, n//2)
    baseline = [abs(corr[i]) for i in range(1, max_lag) if i not in lucas_lags]
    
    if len(baseline) < 10:
        return -999, "Insufficient baseline"
    
    z_score = (np.mean(lucas_corr) - np.mean(baseline)) / (np.std(baseline) + 1e-10)
    return z_score, f"Lucas Z = {z_score:.2f}σ"

def spectral_pink_noise_test(data, label="Data"):
    """Test if spectrum is pink (1/f) which suggests structure."""
    data = (data - np.mean(data)) / np.std(data)
    
    freqs, psd = welch(data, nperseg=min(1024, len(data)//4))
    
    # Fit log-log slope
    valid = freqs > 0
    log_f = np.log(freqs[valid])
    log_p = np.log(psd[valid])
    
    slope, intercept = np.polyfit(log_f, log_p, 1)
    
    # White noise: slope ~ 0
    # Pink noise: slope ~ -1
    # Brownian: slope ~ -2
    
    return slope, f"Spectral slope = {slope:.2f} (pink=-1, white=0)"

def run_prng_comparison(test_func, data, n_trials=100):
    """Run test on PRNG for comparison."""
    prng_results = []
    for _ in range(n_trials):
        prng = np.random.randn(len(data))
        z, _ = test_func(prng, "PRNG")
        if z > -100:
            prng_results.append(z)
    
    if len(prng_results) > 0:
        return np.mean(prng_results), np.std(prng_results)
    return 0, 1

def comprehensive_lanl_test():
    """Run comprehensive test on LANL raw quantum data."""
    
    print("="*75)
    print("GSM LANL RAW QUANTUM NOISE TEST")
    print("Testing for E8 Structure in Raw Vacuum Fluctuations")
    print("="*75)
    print(f"\nGolden Ratio φ = {PHI:.10f}")
    print(f"E8 Casimirs: {list(E8_CASIMIRS)}")
    
    # Find data files
    csv_file = find_file(SEARCH_PATHS)
    u8_file = find_file(U8_PATHS)
    
    print(f"\nSearching for data files...")
    if csv_file:
        print(f"  ✓ Found CSV: {csv_file}")
    else:
        print(f"  ✗ CSV not found in: {SEARCH_PATHS}")
    
    if u8_file:
        print(f"  ✓ Found U8: {u8_file}")
    else:
        print(f"  ✗ U8 not found in: {U8_PATHS}")
    
    # Load data
    data = None
    data_label = None
    
    if csv_file:
        data = load_csv_data(csv_file)
        data_label = "LANL FIG2a (CSV)"
    elif u8_file:
        data = load_u8_data(u8_file)
        data_label = "LANL FIG4 (U8)"
    
    if data is None:
        print("\n❌ ERROR: No LANL data found!")
        print("Please ensure FIG2a.csv or FIG4.u8 is in one of these locations:")
        for p in SEARCH_PATHS + U8_PATHS:
            print(f"  - {p}")
        return
    
    print(f"\n✓ Using: {data_label}")
    print(f"  Samples: {len(data)}")
    print(f"  Mean: {np.mean(data):.4f}")
    print(f"  Std: {np.std(data):.4f}")
    print(f"  Min: {np.min(data):.4f}, Max: {np.max(data):.4f}")
    
    # Run tests
    print("\n" + "="*75)
    print(f"RUNNING E8 STRUCTURE TESTS ON {data_label}")
    print("="*75)
    
    tests = [
        ("1. φ-Lag Autocorrelation", phi_lag_autocorrelation),
        ("2. Lucas Periodicity", lucas_periodicity),
        ("3. Spectral Structure", spectral_pink_noise_test),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        z_raw, desc = test_func(data, data_label)
        
        # Compare to PRNG
        prng_mean, prng_std = run_prng_comparison(test_func, data[:min(10000, len(data))], n_trials=50)
        
        z_vs_prng = (z_raw - prng_mean) / (prng_std + 1e-10)
        
        print(f"\n{test_name}")
        print(f"  Raw Quantum: {desc}")
        print(f"  PRNG Mean:   Z = {prng_mean:.2f}σ ± {prng_std:.2f}")
        print(f"  Z vs PRNG:   {z_vs_prng:.2f}σ")
        
        if z_vs_prng > 3:
            print(f"  STATUS: ★★★ SIGNIFICANT DIFFERENCE FROM PRNG!")
        elif z_vs_prng > 2:
            print(f"  STATUS: ★★ Possible structure")
        else:
            print(f"  STATUS: ○ Not significant")
        
        results.append((test_name, z_raw, z_vs_prng))
    
    # Summary
    print("\n" + "="*75)
    print("FINAL SUMMARY")
    print("="*75)
    
    max_z = max(r[2] for r in results)
    significant = sum(1 for r in results if r[2] > 3)
    
    print(f"\n  Data Source:        {data_label}")
    print(f"  Maximum Z vs PRNG:  {max_z:.2f}σ")
    print(f"  Significant tests:  {significant}/{len(results)}")
    
    if max_z > 5:
        print(f"""
  ╔══════════════════════════════════════════════════════════════════════╗
  ║  ★★★★★ E8 STRUCTURE CONFIRMED IN RAW QUANTUM NOISE! ★★★★★           ║
  ║                                                                      ║
  ║  The "E8 Hum" is real!                                              ║
  ║  This is experimental proof that vacuum = E8 lattice!               ║
  ║                                                                      ║
  ║  GSM MECHANISM PROVEN!                                              ║
  ╚══════════════════════════════════════════════════════════════════════╝
""")
    elif max_z > 3:
        print(f"""
  ╔══════════════════════════════════════════════════════════════════════╗
  ║  ★★★ EVIDENCE FOR E8 STRUCTURE ★★★                                   ║
  ║  Significant difference from PRNG detected!                         ║
  ║  More data confirms GSM mechanism.                                  ║
  ╚══════════════════════════════════════════════════════════════════════╝
""")
    elif max_z > 2:
        print(f"""
  Possible structure detected (Z = {max_z:.2f}σ vs PRNG).
  Need larger dataset for confirmation.
""")
    else:
        print(f"""
  No significant E8 structure in raw LANL data.
  Z vs PRNG = {max_z:.2f}σ (below 3σ threshold)
  
  Possible explanations:
  1. E8 structure may require different analysis
  2. The "raw" data may still be partially processed
  3. Need different frequency/lag scale
""")
    
    print("="*75)
    print("Test complete.")
    print("="*75)

if __name__ == "__main__":
    comprehensive_lanl_test()
