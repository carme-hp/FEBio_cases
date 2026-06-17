import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# ------------------------------------------------------------------
# INPUTS
# ------------------------------------------------------------------

# Configuration tags and corresponding number of elements
configs = [
    {"tag": "2x2x8", "num_elements": 2*2*8},
    {"tag": "4x4x16", "num_elements": 4*4*16},
    {"tag": "8x8x32", "num_elements": 8*8*32},
]

num_runs = 5

# ------------------------------------------------------------------
# STORAGE - averaged values
# ------------------------------------------------------------------

# For each config, store averaged values across 5 runs
mapping_M_values = []
mapping_F_values = []

advance_mapping_M_values = []
advance_mapping_F_values = []

global_M_values = []
global_F_values = []

advance_M_values = []
advance_F_values = []

solverAdvance_M_values = []
solverAdvance_F_values = []

num_elements_list = []
config_labels = []

# ------------------------------------------------------------------
# PROCESS EACH CONFIGURATION
# ------------------------------------------------------------------

for config in configs:
    tag = config["tag"]
    num_elements = config["num_elements"]
    
    # Storage for values from this config's runs
    mapping_M_runs = []
    mapping_F_runs = []
    advance_mapping_M_runs = []
    advance_mapping_F_runs = []
    global_M_runs = []
    global_F_runs = []
    advance_M_runs = []
    advance_F_runs = []
    solverAdvance_M_runs = []
    solverAdvance_F_runs = []
    
    print(f"Processing configuration: {tag}")
    
    # Process each of the 5 runs
    for run_num in range(1, num_runs + 1):
        results_dir = f"results_{tag}_{run_num}"
        csv_file = os.path.join(results_dir, "profiling.csv")
        
        if not os.path.exists(csv_file):
            print(f"  ✗ Warning: {csv_file} not found, skipping run {run_num}")
            continue
        
        print(f"  Reading {csv_file}")
        
        try:
            df = pd.read_csv(csv_file)
            
            # Mapping
            mapping_M = df[(df["participant"] == "Muscle") & (df["rank"] == 0) & (df["event"] == "initialize/mapping")]["duration"]
            mapping_F = df[(df["participant"] == "Fibers") & (df["rank"] == 0) & (df["event"] == "initialize/mapping")]["duration"]
            
            if len(mapping_M) > 0 and len(mapping_F) > 0:
                mapping_M_runs.append(mapping_M.iloc[0])
                mapping_F_runs.append(mapping_F.iloc[0])
            
            # Advance mapping
            advance_mapping_M_array = df[(df["participant"] == "Muscle") & (df["rank"] == 0) & (df["event"] == "advance/mapping")]["duration"].values
            advance_mapping_F_array = df[(df["participant"] == "Fibers") & (df["rank"] == 0) & (df["event"] == "advance/mapping")]["duration"].values
            
            if len(advance_mapping_M_array) > 0 and len(advance_mapping_F_array) > 0:
                advance_mapping_M_runs.append(advance_mapping_M_array.mean())
                advance_mapping_F_runs.append(advance_mapping_F_array.mean())
            
            # Global
            global_M = df[(df["participant"] == "Muscle") & (df["rank"] == 0) & (df["event"] == "_GLOBAL")]["duration"]
            global_F = df[(df["participant"] == "Fibers") & (df["rank"] == 0) & (df["event"] == "_GLOBAL")]["duration"]
            
            if len(global_M) > 0 and len(global_F) > 0:
                global_M_runs.append(global_M.iloc[0])
                global_F_runs.append(global_F.iloc[0])
            
            # Solver advance
            solverAdvance_M_array = df[(df["participant"] == "Muscle") & (df["rank"] == 0) & (df["event"] == "solver.advance")]["duration"].values
            solverAdvance_F_array = df[(df["participant"] == "Fibers") & (df["rank"] == 0) & (df["event"] == "solver.advance")]["duration"].values
            
            if len(solverAdvance_M_array) > 0 and len(solverAdvance_F_array) > 0:
                solverAdvance_M_runs.append(solverAdvance_M_array.sum())
                solverAdvance_F_runs.append(solverAdvance_F_array.sum())
            
            # Advance
            advance_M_array = df[(df["participant"] == "Muscle") & (df["rank"] == 0) & (df["event"] == "advance")]["duration"].values
            advance_F_array = df[(df["participant"] == "Fibers") & (df["rank"] == 0) & (df["event"] == "advance")]["duration"].values
            
            if len(advance_M_array) > 0 and len(advance_F_array) > 0:
                advance_M_runs.append(advance_M_array.sum())
                advance_F_runs.append(advance_F_array.sum())
        
        except Exception as e:
            print(f"  ✗ Error reading {csv_file}: {e}")
            continue
    
    # Calculate averages for this configuration
    if len(mapping_M_runs) > 0:
        mapping_M_values.append(np.mean(mapping_M_runs))
        mapping_F_values.append(np.mean(mapping_F_runs))
    
    if len(advance_mapping_M_runs) > 0:
        advance_mapping_M_values.append(np.mean(advance_mapping_M_runs))
        advance_mapping_F_values.append(np.mean(advance_mapping_F_runs))
    
    if len(global_M_runs) > 0:
        global_M_values.append(np.mean(global_M_runs))
        global_F_values.append(np.mean(global_F_runs))
    
    if len(solverAdvance_M_runs) > 0:
        solverAdvance_M_values.append(np.mean(solverAdvance_M_runs))
        solverAdvance_F_values.append(np.mean(solverAdvance_F_runs))
    
    if len(advance_M_runs) > 0:
        advance_M_values.append(np.mean(advance_M_runs))
        advance_F_values.append(np.mean(advance_F_runs))
    
    num_elements_list.append(num_elements)
    config_labels.append(tag)
    
    print(f"  ✓ Processed {len(mapping_M_runs)} runs successfully")

# ------------------------------------------------------------------
# PLOT: GLOBAL
# ------------------------------------------------------------------

plt.figure(figsize=(7, 5))

plt.plot(num_elements_list, 1e-6*np.array(global_M_values), color='red', marker='o', linestyle='-', label='Muscle', linewidth=2, markersize=8)
plt.plot(num_elements_list, 1e-6*np.array(global_F_values), color='blue', marker='^', linestyle='-', label='Fibers', linewidth=2, markersize=8)

plt.xlabel("Number of Elements", fontsize=12)
plt.ylabel("Time [s]", fontsize=12)
plt.title("Global Timing (Averaged over 5 runs)", fontsize=14)
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3)
plt.xscale('log')

# ------------------------------------------------------------------
# PLOT: ADVANCE
# ------------------------------------------------------------------
print(solverAdvance_F_array)

plt.figure(figsize=(7, 5))

plt.plot(num_elements_list, 1e-6*np.array(solverAdvance_M_values), color='red', marker='o', linestyle='-', label='Mechanics:solver', linewidth=2, markersize=8)
plt.plot(num_elements_list, 1e-6*np.array(advance_M_values), color='red', marker='o', linestyle='--', label='Mechanics:precice', linewidth=2, markersize=8)

plt.plot(num_elements_list, 1e-6*np.array(solverAdvance_F_values), color='blue', marker='^', linestyle='-', label='Fibers:solver', linewidth=2, markersize=8)
plt.plot(num_elements_list, 1e-6*np.array(advance_F_values), color='blue', marker='^', linestyle='--', label='Fibers:precice', linewidth=2, markersize=8)

plt.xlabel("Number of Elements", fontsize=12)
plt.ylabel("Time [s]", fontsize=12)
plt.title("Time spent in solver vs in precice (Averaged over 5 runs)", fontsize=14)
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3)
plt.xscale('log')

# ------------------------------------------------------------------
# PLOT: MAPPING INITIALIZATION
# ------------------------------------------------------------------

plt.figure(figsize=(7, 5))

plt.plot(num_elements_list, 1e-6*np.array(mapping_M_values), color='red', marker='o', linestyle='-', label='Muscle', linewidth=2, markersize=8)
plt.plot(num_elements_list, 1e-6*np.array(mapping_F_values), color='blue', marker='^', linestyle='-', label='Fibers', linewidth=2, markersize=8)

plt.xlabel("Number of Elements", fontsize=12)
plt.ylabel("Time [s]", fontsize=12)
plt.title("Timing for \"initialize/mapping\" (Averaged over 5 runs)", fontsize=14)
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3)
plt.xscale('log')

# ------------------------------------------------------------------
# PLOT: MAPPING ADVANCE
# ------------------------------------------------------------------

plt.figure(figsize=(7, 5))

plt.plot(num_elements_list, 1e-6*np.array(advance_mapping_M_values), color='red', marker='o', linestyle='-', label='Muscle', linewidth=2, markersize=8)
plt.plot(num_elements_list, 1e-6*np.array(advance_mapping_F_values), color='blue', marker='^', linestyle='-', label='Fibers', linewidth=2, markersize=8)

plt.xlabel("Number of Elements", fontsize=12)
plt.ylabel("Time [s]", fontsize=12)
plt.title("Timing for \"advance/mapping\" (Averaged over 5 runs)", fontsize=14)
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3)
plt.xscale('log')

# ------------------------------------------------------------------
# SHOW ALL FIGURES
# ------------------------------------------------------------------

print("\nPlots generated successfully!")
print(f"Configurations: {config_labels}")
print(f"Number of elements: {num_elements_list}")

plt.show()
