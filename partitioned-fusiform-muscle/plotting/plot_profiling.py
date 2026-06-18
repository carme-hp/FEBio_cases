
import pandas as pd
import matplotlib.pyplot as plt

# ------------------------------------------------------------------
# INPUTS
# ------------------------------------------------------------------

csv_files_NN = [
    "results_2x2x8/profiling.csv",
    "results_4x4x16/profiling.csv",
    "results_8x8x32/profiling.csv",
]

# Number of elements corresponding to each CSV file
num_elements_NN = [
    2*2*4,
    4*4*16,
    8*8*32,
]

csv_files_rbf = [
    "results_rbf2x2x8/profiling.csv",
    "results_rbf4x4x16/profiling.csv",
    "results_rbf8x8x32/profiling.csv",
]

# Number of elements corresponding to each CSV file
num_elements_rbf = [
    2*2*4,
    4*4*16,
    8*8*32,
]
# ------------------------------------------------------------------
# CONSTANT INDICES
# ------------------------------------------------------------------

indexInitializeMapping = 8
indexGlobal = 1811

indexFirstSolverAdvance = 10
indexAdvance = 15

# ------------------------------------------------------------------
# STORAGE
# ------------------------------------------------------------------

mapping_M_values_NN = []
mapping_F_values_NN = []

global_M_values_NN = []
global_F_values_NN = []

advance_M_values_NN = []
advance_F_values_NN = []

mapping_M_values_rbf = []
mapping_F_values_rbf = []

global_M_values_rbf = []
global_F_values_rbf = []

advance_M_values_rbf = []
advance_F_values_rbf = []

# ------------------------------------------------------------------
# PROCESS EACH CSV FILE
# ------------------------------------------------------------------

for csv_file in csv_files_NN:

    df = pd.read_csv(csv_file)

    # --------------------------------------------------------------
    # Mapping
    # --------------------------------------------------------------

    initializeMappingM = df.iloc[indexInitializeMapping, 5]
    initializeMappingF = df.iloc[indexInitializeMapping + indexGlobal + 1, 5]

    mapping_M_values_NN.append(initializeMappingM)
    mapping_F_values_NN.append(initializeMappingF)

    # --------------------------------------------------------------
    # Global
    # --------------------------------------------------------------

    globalM = df.iloc[indexGlobal, 5]
    globalF = df.iloc[indexGlobal + indexGlobal + 1, 5]

    global_M_values_NN.append(globalM)
    global_F_values_NN.append(globalF)

    # --------------------------------------------------------------
    # Advance
    # --------------------------------------------------------------

    solverAdvanceM = df.iloc[indexFirstSolverAdvance, 5]
    advanceM = 0

    for i in range(indexFirstSolverAdvance + 5, indexGlobal, 6):
        advanceM += df.iloc[i, 5]
        solverAdvanceM += df.iloc[i + 1, 5]

    solverAdvanceF = df.iloc[indexFirstSolverAdvance + indexGlobal, 5]
    advanceF = 0

    for i in range(indexFirstSolverAdvance + indexGlobal + 5,
                   indexGlobal + indexGlobal + 1,
                   6):
        advanceF += df.iloc[i, 5]
        solverAdvanceF += df.iloc[i + 1, 5]

    advance_M_values_NN.append(advanceM)
    advance_F_values_NN.append(advanceF)


for csv_file in csv_files_rbf:

    df = pd.read_csv(csv_file)

    # --------------------------------------------------------------
    # Mapping
    # --------------------------------------------------------------

    initializeMappingM = df.iloc[indexInitializeMapping, 5]
    initializeMappingF = df.iloc[indexInitializeMapping + indexGlobal + 1, 5]

    mapping_M_values_rbf.append(initializeMappingM)
    mapping_F_values_rbf.append(initializeMappingF)

    # --------------------------------------------------------------
    # Global
    # --------------------------------------------------------------

    globalM = df.iloc[indexGlobal, 5]
    globalF = df.iloc[indexGlobal + indexGlobal + 1, 5]

    global_M_values_rbf.append(globalM)
    global_F_values_rbf.append(globalF)

    # --------------------------------------------------------------
    # Advance
    # --------------------------------------------------------------

    solverAdvanceM = df.iloc[indexFirstSolverAdvance, 5]
    advanceM = 0

    for i in range(indexFirstSolverAdvance + 5, indexGlobal, 6):
        advanceM += df.iloc[i, 5]
        solverAdvanceM += df.iloc[i + 1, 5]

    solverAdvanceF = df.iloc[indexFirstSolverAdvance + indexGlobal, 5]
    advanceF = 0

    for i in range(indexFirstSolverAdvance + indexGlobal + 5,
                   indexGlobal + indexGlobal + 1,
                   6):
        advanceF += df.iloc[i, 5]
        solverAdvanceF += df.iloc[i + 1, 5]

    advance_M_values_rbf.append(advanceM)
    advance_F_values_rbf.append(advanceF)

# ------------------------------------------------------------------
# PLOT: GLOBAL
# ------------------------------------------------------------------

plt.figure(figsize=(7, 5))

plt.plot(num_elements_NN, global_M_values_NN, color='blue', marker='o', linestyle='-', label='M - NN')
plt.plot(num_elements_NN, global_F_values_NN, color='blue', marker='o', linestyle='--', label='F - NN')
plt.plot(num_elements_rbf, global_M_values_rbf, color='red', marker='^', linestyle='-', label='M - RBF')
plt.plot(num_elements_rbf, global_F_values_rbf, color='red', marker='^', linestyle='--', label='F - RBF')

plt.xlabel("Number of Elements")
plt.ylabel("Time [ms]")
plt.title("Global Timing")
plt.legend()
plt.grid(True)

# ------------------------------------------------------------------
# PLOT: ADVANCE
# ------------------------------------------------------------------

plt.figure(figsize=(7, 5))

plt.plot(num_elements_NN, advance_M_values_NN, color='blue', marker='o', linestyle='-', label='M - NN')
plt.plot(num_elements_NN, advance_F_values_NN, color='blue', marker='o', linestyle='--', label='F - NN')
plt.plot(num_elements_rbf, advance_M_values_rbf, color='red', marker='^', linestyle='-', label='M - RBF')
plt.plot(num_elements_rbf, advance_F_values_rbf, color='red', marker='^', linestyle='--', label='F - RBF')

plt.xlabel("Number of Elements")
plt.ylabel("Time [ms]")
plt.title("Advance Timing")
plt.legend()
plt.grid(True)

# ------------------------------------------------------------------
# PLOT: MAPPING
# ------------------------------------------------------------------
print("NN", mapping_M_values_NN)
print("rbf", mapping_M_values_rbf)

mapping_M_values_NN = [10390, 14745, 16516]
mapping_M_values_rbf = [61597, 39864, 147860]

print("NN", mapping_M_values_NN)
print("rbf", mapping_M_values_rbf)

plt.figure(figsize=(7, 5))

plt.plot(num_elements_NN, mapping_M_values_NN, color='red', marker='o', linestyle='-', label='M - NN')
plt.plot(num_elements_rbf, mapping_M_values_rbf, color='red', marker='o', linestyle='--', label='M - RBF')



# plt.plot(num_elements_NN, mapping_F_values_NN, color='blue', marker='^', linestyle='-', label='F - NN')
# plt.plot(num_elements_rbf, mapping_F_values_rbf, color='blue', marker='^', linestyle='--', label='F - RBF')

plt.xlabel("Number of Elements")
plt.title("Mapping Timing")
plt.legend()
plt.grid(True)

# ------------------------------------------------------------------
# SHOW ALL FIGURES
# ------------------------------------------------------------------

plt.show()
