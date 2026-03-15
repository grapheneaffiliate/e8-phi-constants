# Instructions: Download O3 LIGO Data and Run Echo Search

## What This Is

The GSM theory predicts gravitational wave echoes with specific phi-ratio timing.
We need real O3 LIGO strain data to test these predictions against actual observations.

## Step 1: Download Data Files

Download these 8 HDF5 files from GWOSC (Gravitational Wave Open Science Center).

Go to: https://gwosc.org/eventapi/html/GWTC/

For each event below, click the event name, then download the **4 KHz, 32-second**
strain files for both H1 (Hanford) and L1 (Livingston).

### GW200129 (O3b)
```
https://gwosc.org/eventapi/html/GWTC-3-confident/GW200129_065458/
```
- H1: `H-H1_GWOSC_O3b_4KHZ_R1-1264316100-32.hdf5`
- L1: `L-L1_GWOSC_O3b_4KHZ_R1-1264316100-32.hdf5`

### GW190521_074359 (O3a)
```
https://gwosc.org/eventapi/html/GWTC-2.1-confident/GW190521_074359/
```
- H1: `H-H1_GWOSC_O3a_4KHZ_R1-1242459841-32.hdf5`
- L1: `L-L1_GWOSC_O3a_4KHZ_R1-1242459841-32.hdf5`

### GW190412 (O3a)
```
https://gwosc.org/eventapi/html/GWTC-2.1-confident/GW190412/
```
- H1: `H-H1_GWOSC_O3a_4KHZ_R1-1239082246-32.hdf5`
- L1: `L-L1_GWOSC_O3a_4KHZ_R1-1239082246-32.hdf5`

### GW190814 (O3a)
```
https://gwosc.org/eventapi/html/GWTC-2.1-confident/GW190814/
```
- H1: `H-H1_GWOSC_O3a_4KHZ_R1-1249852241-32.hdf5`
- L1: `L-L1_GWOSC_O3a_4KHZ_R1-1249852241-32.hdf5`

### GW150914 (O1) — also needed as baseline
```
https://gwosc.org/eventapi/html/GWTC-1-confident/GW150914/
```
- H1: `H-H1_LOSC_4_V1-1126259446-32.hdf5`
- L1: `L-L1_LOSC_4_V1-1126259446-32.hdf5`

## Step 2: Place the Files

Put ALL downloaded files in `/tmp/`:

```bash
# Move all downloaded HDF5 files to /tmp/
mv ~/Downloads/*.hdf5 /tmp/
```

## Step 3: Install Dependencies

```bash
pip install numpy scipy h5py matplotlib
```

## Step 4: Run the Tests

From the repo root (`e8-phi-constants/`):

```bash
# Test 1: O3 benchmark (noise-scaled injection-recovery)
# Uses GW150914 O1 noise, scales it to O3/O4/O5 sensitivity
python3 simulation/gsm_echo_o3_benchmark.py

# Test 2: Real data echo search on GW150914
python3 simulation/gsm_echo_ligo_search.py

# Test 3: Improved search with ringdown subtraction + multi-event stacking
python3 simulation/gsm_echo_improved_search.py
```

## Step 5: (Optional) Run with Real O3 Data

The current `gsm_echo_o3_benchmark.py` uses noise-scaled O1 data.
To run on actual O3 strain data, the script needs to be modified to
load the O3 event files directly instead of scaling O1 noise. The key
changes would be:

1. Add O3 file paths (the files you downloaded in Step 1)
2. Load each event's actual strain data
3. Identify the merger time in each file
4. Extract post-merger data and run the phi-comb search

The event parameters are already defined in the script's `O3_EVENTS` dict.

## Key Repo Files

| File | Purpose |
|------|---------|
| `simulation/gsm_echo_o3_benchmark.py` | Main O3 benchmark (noise-scaled) |
| `simulation/gsm_echo_ligo_search.py` | GW150914 real-data search |
| `simulation/gsm_echo_improved_search.py` | Multi-event stacking search |
| `simulation/gsm_echo_injection_test.py` | Injection-recovery validation |
| `simulation/gsm_echo_o3_forecast.py` | Detection probability forecast |
| `simulation/gsm_ligo_template_generator.py` | Echo template generator |
| `simulation/gsm_gw_echoes_sim.py` | Echo simulation core |

## What the Tests Produce

- **Console output**: z-scores, p-values, detection status per event
- **PNG plots**: Saved to repo root (e.g., `gsm_echo_o3_benchmark.png`)
- **Markdown reports**: Saved to repo root (e.g., `GSM_ECHO_O3_BENCHMARK.md`)

## Expected Results

- **GW150914 (O1)**: Null result expected (echoes below noise floor)
- **O3 events (noise-scaled)**: Marginal-to-strong detection depending on event SNR
- **GW250114 projection**: Strong detection expected at O4+ sensitivity
