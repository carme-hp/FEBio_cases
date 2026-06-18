#!/usr/bin/env python3
"""
Compute convergence errors by comparing FEBio simulation results to a reference solution.
Creates plots of L2 error and relative error vs number of cells.
"""

import math
import matplotlib.pyplot as plt
import numpy as np


def read_vtk_file(file_path: str):
    """
    Read a VTU or VTK file and return the VTK dataset object.

    Args:
        file_path: Path to the VTU or VTK file

    Returns:
        VTK dataset object
    """
    try:
        import vtk
    except ImportError:
        raise ImportError("VTK library required. Install with: pip install vtk")

    # Suppress VTK error/warning messages
    vtk.vtkLogger.SetStderrVerbosity(vtk.vtkLogger.VERBOSITY_OFF)

    # Determine file format and use appropriate reader
    if file_path.endswith('.vtu'):
        reader = vtk.vtkXMLUnstructuredGridReader()
    elif file_path.endswith('.vtk'):
        reader = vtk.vtkDataSetReader()
    else:
        raise ValueError(f"Unsupported file format: {file_path}")

    reader.SetFileName(file_path)
    reader.Update()

    output = reader.GetOutput()
    num_points = output.GetNumberOfPoints()

    if num_points == 0:
        raise ValueError(f"Failed to read file '{file_path}' - file may be corrupted or empty")

    return output


def get_data_values(data_name: str, vtk_dataset) -> list[float]:
    """
    Extract data values from a VTK dataset.

    Args:
        data_name: Name of the data array to read
        vtk_dataset: VTK dataset object

    Returns:
        List of float values from the data array
    """
    try:
        from vtk.util.numpy_support import vtk_to_numpy
    except ImportError:
        raise ImportError("VTK library required. Install with: pip install vtk")

    point_data = vtk_dataset.GetPointData()
    array = point_data.GetArray(data_name)

    if array is None:
        available = [point_data.GetArrayName(i) for i in range(point_data.GetNumberOfArrays())]
        raise ValueError(f"Data array '{data_name}' not found in dataset. "
                         f"Available arrays: {available}")

    # Handle vector data by flattening
    num_tuples = array.GetNumberOfTuples()
    num_components = array.GetNumberOfComponents()
    
    if num_components == 1:
        return vtk_to_numpy(array).tolist()
    else:
        # For vector data, return as flat list
        return vtk_to_numpy(array).flatten().tolist()


def interpolate_data(source_dataset, target_dataset, data_name: str):
    """
    Interpolate data from source mesh to target mesh.

    Args:
        source_dataset: Source VTK dataset with data to interpolate
        target_dataset: Target VTK dataset (mesh to interpolate to)
        data_name: Name of the data array to interpolate

    Returns:
        List of interpolated values at target dataset points
    """
    try:
        import vtk
        from vtk.util.numpy_support import vtk_to_numpy
    except ImportError:
        raise ImportError("VTK library required. Install with: pip install vtk")

    vtk.vtkLogger.SetStderrVerbosity(vtk.vtkLogger.VERBOSITY_OFF)

    # Use vtkProbeFilter to interpolate source data to target points
    probe = vtk.vtkProbeFilter()
    probe.SetSourceData(source_dataset)
    probe.SetInputData(target_dataset)
    probe.Update()

    output = probe.GetOutput()
    point_data = output.GetPointData()
    array = point_data.GetArray(data_name)

    if array is None:
        raise ValueError(f"Interpolation failed for data array '{data_name}'")

    num_components = array.GetNumberOfComponents()
    if num_components == 1:
        return vtk_to_numpy(array).tolist()
    else:
        # For vector data, return as flat list
        return vtk_to_numpy(array).flatten().tolist()


def compute_l2_error(reference_values: list[float], simulation_values: list[float]) -> float:
    """
    Compute L2 error norm.

    Args:
        reference_values: Reference solution values
        simulation_values: Simulation solution values

    Returns:
        L2 error
    """
    if len(reference_values) != len(simulation_values):
        raise ValueError(f"Array size mismatch: {len(reference_values)} vs {len(simulation_values)}")

    l2_error = math.sqrt(sum((v1 - v2) ** 2 for v1, v2 in zip(simulation_values, reference_values)))
    return l2_error


def compute_relative_error(reference_values: list[float], simulation_values: list[float]) -> float:
    """
    Compute relative L2 error.

    Args:
        reference_values: Reference solution values
        simulation_values: Simulation solution values

    Returns:
        Relative L2 error
    """
    l2_error = compute_l2_error(reference_values, simulation_values)
    reference_norm = math.sqrt(sum(v ** 2 for v in reference_values))
    rel_error = l2_error / reference_norm if reference_norm > 0 else 0
    return rel_error


# ------------------------------------------------------------------
# CONFIGURATION
# ------------------------------------------------------------------

# Define mesh configurations: (folder_name, num_elements, timestep_file, grid_type)
MESH_CONFIGS = [
    ("results_2x2x8/results-opendihu-muscle", 2 * 2 * 8, "muscle_0000299.vtu", "NN"),
    ("results_4x4x16/results-opendihu-muscle", 4 * 4 * 16, "muscle_0000299.vtu", "NN"),
    ("results_8x8x32/results-opendihu-muscle", 8 * 8 * 32, "muscle_0000299.vtu", "NN"),
    ("results_16x16x64/results-opendihu-muscle", 16 * 16 * 64, "muscle_0000299.vtu", "NN"),
]

# Reference mesh (finest resolution)
REFERENCE_FOLDER = "results_16x16x64/results-opendihu-muscle"
REFERENCE_FILE = "results_16x16x64/results-opendihu-muscle/muscle_0000299.vtu"
REFERENCE_NUM_CELLS = 16 * 16 * 64

# Data array to compare (e.g., displacement)
DATA_ARRAY = "u"

# ------------------------------------------------------------------
# DEBUG: INSPECT FILES
# ------------------------------------------------------------------

print("=" * 60)
print("Inspecting VTK files")
print("=" * 60)
print()

def inspect_vtk_file(file_path: str):
    """Print available data arrays in a VTK file."""
    try:
        dataset = read_vtk_file(file_path)
        
        print(f"File: {file_path}")
        print(f"  Number of points: {dataset.GetNumberOfPoints()}")
        print(f"  Number of cells: {dataset.GetNumberOfCells()}")
        
        point_data = dataset.GetPointData()
        print(f"  Point data arrays:")
        for i in range(point_data.GetNumberOfArrays()):
            arr = point_data.GetArray(i)
            arr_name = point_data.GetArrayName(i)
            num_components = arr.GetNumberOfComponents()
            num_tuples = arr.GetNumberOfTuples()
            print(f"    - {arr_name}: {num_tuples} points × {num_components} components")
        print()
    except Exception as e:
        print(f"  Error: {e}")
        print()

for folder, num_cells, filename, grid_type in MESH_CONFIGS:
    file_path = f"{folder}/{filename}"
    inspect_vtk_file(file_path)

# ------------------------------------------------------------------
# COMPUTATION
# ------------------------------------------------------------------

print("=" * 60)
print("Computing convergence errors (with interpolation)")
print("=" * 60)
print()

# Load reference solution dataset
print(f"Loading reference solution from: {REFERENCE_FILE}")
reference_dataset = read_vtk_file(REFERENCE_FILE)
reference_values = get_data_values(DATA_ARRAY, reference_dataset)
print(f"✓ Reference mesh has {reference_dataset.GetNumberOfPoints()} points")
print(f"✓ Reference data has {len(reference_values)} values")
print()

# Storage for results
num_cells_list = []
l2_errors = []
relative_errors = []
grid_types = []

# Compute errors for each mesh configuration (excluding reference)
for folder, num_cells, filename, grid_type in MESH_CONFIGS:
    if num_cells == REFERENCE_NUM_CELLS:
        # Skip reference mesh itself
        print(f"Skipping reference mesh: {folder} ({num_cells} cells)")
        continue

    file_path = f"{folder}/{filename}"
    print(f"Processing: {folder}")
    print(f"  File: {file_path}")
    print(f"  Cells: {num_cells}")
    print(f"  Type: {grid_type}")

    try:
        # Load coarse simulation dataset
        coarse_dataset = read_vtk_file(file_path)
        print(f"  ✓ Coarse mesh has {coarse_dataset.GetNumberOfPoints()} points")

        # Interpolate coarse solution to reference mesh
        print(f"  Interpolating to reference mesh...")
        sim_values = interpolate_data(coarse_dataset, reference_dataset, DATA_ARRAY)
        print(f"  ✓ Interpolated to {len(sim_values)} values")

        # Compute errors
        l2_error = compute_l2_error(reference_values, sim_values)
        rel_error = compute_relative_error(reference_values, sim_values)

        num_cells_list.append(num_cells)
        l2_errors.append(l2_error)
        relative_errors.append(rel_error)
        grid_types.append(grid_type)

        print(f"  L2 error: {l2_error:.6e}")
        print(f"  Relative error: {rel_error:.6e}")
        print()

    except Exception as e:
        print(f"  ✗ Error: {e}")
        print()

# ------------------------------------------------------------------
# PLOTTING
# ------------------------------------------------------------------

print("=" * 60)
print("Creating plots")
print("=" * 60)
print()

if len(num_cells_list) == 0:
    print("✗ No data to plot. Check errors above.")
    exit(1)

# Create figure with two subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Convert to arrays for plotting
num_cells_array = np.array(num_cells_list)
l2_errors_array = np.array(l2_errors)
relative_errors_array = np.array(relative_errors)

print(f"Plotting {len(num_cells_list)} data points...")
print()

# Plot both L2 and relative error for all data
# Plot 1: L2 Error vs Number of Cells
ax1.loglog(num_cells_array, l2_errors_array, 'bo-', linewidth=2, markersize=8, label='L2 Error')
ax1.set_xlabel('Number of Cells', fontsize=12)
ax1.set_ylabel('L2 Error', fontsize=12)
ax1.set_title('L2 Error vs Number of Cells', fontsize=13)
ax1.grid(True, which='both', alpha=0.3)
ax1.legend(fontsize=11)

# Plot 2: Relative Error vs Number of Cells
ax2.loglog(num_cells_array, relative_errors_array, 'rs-', linewidth=2, markersize=8, label='Relative L2 Error')
ax2.set_xlabel('Number of Cells', fontsize=12)
ax2.set_ylabel('Relative L2 Error', fontsize=12)
ax2.set_title('Relative L2 Error vs Number of Cells', fontsize=13)
ax2.grid(True, which='both', alpha=0.3)
ax2.legend(fontsize=11)

plt.tight_layout()
plt.savefig('convergence_errors.png', dpi=150, bbox_inches='tight')
print("✓ Saved plot to: convergence_errors.png")

plt.show()

print()
print("=" * 60)
print("Summary")
print("=" * 60)
print(f"Reference mesh: {REFERENCE_FOLDER} ({REFERENCE_NUM_CELLS} cells)")
print(f"Compared meshes: {len(num_cells_list)}")
print()
for cells, l2_err, rel_err, gtype in zip(num_cells_list, l2_errors, relative_errors, grid_types):
    print(f"Cells: {cells:6d} | Type: {gtype:12s} | L2 Error: {l2_err:.6e} | Relative Error: {rel_err:.6e}")