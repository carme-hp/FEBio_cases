#!/usr/bin/env python3
"""
Combined convergence analysis: Compare FEBio structured grids and OpenDiHu grids
against both FEBio and OpenDiHu reference solutions.

Creates a single plot with three lines:
1. FEBio structured grids vs FEBio reference (16x16x64)
2. OpenDiHu NN grids vs OpenDiHu reference (16x16x64)
3. OpenDiHu NN grids vs FEBio reference (16x16x64)
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

# FEBio structured grid configurations
FEBIO_CONFIGS = [
    ("results_febio_2x2x8", 2 * 2 * 8, "fusiform-muscle-2x2x8.t300.vtk"),
    ("results_febio_4x4x16", 4 * 4 * 16, "fusiform-muscle-4x4x16.t300.vtk"),
    ("results_febio_8x8x32", 8 * 8 * 32, "fusiform-muscle-8x8x32.t300.vtk"),
    ("results_febio_16x16x64", 16 * 16 * 64, "fusiform-muscle-16x16x64.t300.vtk"),
]

# OpenDiHu configurations
OPENDIHU_CONFIGS = [
    ("results_2x2x8/results-opendihu-muscle", 2 * 2 * 8, "muscle_0000299.vtu"),
    ("results_4x4x16/results-opendihu-muscle", 4 * 4 * 16, "muscle_0000299.vtu"),
    ("results_8x8x32/results-opendihu-muscle", 8 * 8 * 32, "muscle_0000299.vtu"),
    ("results_16x16x64/results-opendihu-muscle", 16 * 16 * 64, "muscle_0000299.vtu"),
]

# Reference files
FEBIO_REFERENCE_FILE = "results_febio_16x16x64/fusiform-muscle-16x16x64.t300.vtk"
FEBIO_REFERENCE_NUM_CELLS = 16 * 16 * 64

OPENDIHU_REFERENCE_FILE = "results_16x16x64/results-opendihu-muscle/muscle_0000299.vtu"
OPENDIHU_REFERENCE_NUM_CELLS = 16 * 16 * 64

# Data arrays
FEBIO_DATA_ARRAY = "displacement"
OPENDIHU_DATA_ARRAY = "u"

# ------------------------------------------------------------------
# LOAD REFERENCE SOLUTIONS
# ------------------------------------------------------------------

print("=" * 60)
print("Loading reference solutions")
print("=" * 60)
print()

print(f"Loading FEBio reference from: {FEBIO_REFERENCE_FILE}")
febio_ref_dataset = read_vtk_file(FEBIO_REFERENCE_FILE)
febio_ref_values = get_data_values(FEBIO_DATA_ARRAY, febio_ref_dataset)
print(f"✓ FEBio reference mesh has {febio_ref_dataset.GetNumberOfPoints()} points")
print()

print(f"Loading OpenDiHu reference from: {OPENDIHU_REFERENCE_FILE}")
opendihu_ref_dataset = read_vtk_file(OPENDIHU_REFERENCE_FILE)
opendihu_ref_values = get_data_values(OPENDIHU_DATA_ARRAY, opendihu_ref_dataset)
print(f"✓ OpenDiHu reference mesh has {opendihu_ref_dataset.GetNumberOfPoints()} points")
print()

# ------------------------------------------------------------------
# COMPUTE ERRORS
# ------------------------------------------------------------------

print("=" * 60)
print("Computing convergence errors")
print("=" * 60)
print()

# Storage for results
febio_cells = []
febio_rel_errors = []

opendihu_cells = []
opendihu_vs_opendihu_errors = []
opendihu_vs_febio_errors = []

# --- FEBio structured grids vs FEBio reference ---
print("FEBio structured grids vs FEBio reference (16x16x64):")
print()

for folder, num_cells, filename in FEBIO_CONFIGS:
    if num_cells == FEBIO_REFERENCE_NUM_CELLS:
        print(f"Skipping reference mesh: {folder} ({num_cells} cells)")
        continue

    file_path = f"{folder}/{filename}"
    print(f"  {folder}: {num_cells} cells")

    try:
        coarse_dataset = read_vtk_file(file_path)
        sim_values = interpolate_data(coarse_dataset, febio_ref_dataset, FEBIO_DATA_ARRAY)
        rel_error = compute_relative_error(febio_ref_values, sim_values)

        febio_cells.append(num_cells)
        febio_rel_errors.append(rel_error)

        print(f"    ✓ Relative error: {rel_error:.6e}")

    except Exception as e:
        print(f"    ✗ Error: {e}")

print()

# --- OpenDiHu NN grids vs OpenDiHu reference ---
print("OpenDiHu NN grids vs OpenDiHu reference (16x16x64):")
print()

for folder, num_cells, filename in OPENDIHU_CONFIGS:
    if num_cells == OPENDIHU_REFERENCE_NUM_CELLS:
        print(f"Skipping reference mesh: {folder} ({num_cells} cells)")
        continue

    file_path = f"{folder}/{filename}"
    print(f"  {folder}: {num_cells} cells")

    try:
        coarse_dataset = read_vtk_file(file_path)
        
        # Compute error vs OpenDiHu reference
        sim_values_opendihu = interpolate_data(coarse_dataset, opendihu_ref_dataset, OPENDIHU_DATA_ARRAY)
        rel_error_opendihu = compute_relative_error(opendihu_ref_values, sim_values_opendihu)
        
        # Compute error vs FEBio reference
        sim_values_febio = interpolate_data(coarse_dataset, febio_ref_dataset, OPENDIHU_DATA_ARRAY)
        rel_error_febio = compute_relative_error(febio_ref_values, sim_values_febio)

        opendihu_cells.append(num_cells)
        opendihu_vs_opendihu_errors.append(rel_error_opendihu)
        opendihu_vs_febio_errors.append(rel_error_febio)

        print(f"    ✓ Relative error (vs OpenDiHu ref): {rel_error_opendihu:.6e}")
        print(f"    ✓ Relative error (vs FEBio ref):    {rel_error_febio:.6e}")

    except Exception as e:
        print(f"    ✗ Error: {e}")

print()

# ------------------------------------------------------------------
# PLOTTING
# ------------------------------------------------------------------

print("=" * 60)
print("Creating plot")
print("=" * 60)
print()

if len(febio_cells) == 0 or len(opendihu_cells) == 0:
    print("✗ No data to plot. Check errors above.")
    exit(1)

# Create figure
fig, ax = plt.subplots(figsize=(7,5))

# Convert to arrays for plotting
febio_cells_array = np.array(febio_cells)
febio_rel_errors_array = np.array(febio_rel_errors)

opendihu_cells_array = np.array(opendihu_cells)
opendihu_vs_opendihu_array = np.array(opendihu_vs_opendihu_errors)
opendihu_vs_febio_array = np.array(opendihu_vs_febio_errors)

# Plot all three lines
ax.loglog(febio_cells_array, febio_rel_errors_array, 
          'ro-', linewidth=2.5, markersize=10, label='FEBio mechanics', zorder=3)

ax.loglog(opendihu_cells_array, opendihu_vs_opendihu_array, 
          'gs-', linewidth=2.5, markersize=10, label='OpenDiHu mechanics', zorder=3)

# ax.loglog(opendihu_cells_array, opendihu_vs_febio_array, 
#           'r^--', linewidth=2.5, markersize=10, label='OpenDiHu (vs FEBio 16×16×64)', zorder=3)

ax.set_xlabel('Number of Elements')
ax.set_ylabel('Relative L2 Error')
# ax.set_title('Convergence Comparison: FEBio vs OpenDiHu', fontsize=15, fontweight='bold')
ax.grid(True, which='both', alpha=0.3, linestyle='--', linewidth=0.7)
ax.legend(fontsize=12, loc='upper right', framealpha=0.95)

plt.tight_layout()
plt.savefig('combined_convergence_comparison.png', dpi=150, bbox_inches='tight')
print("✓ Saved plot to: combined_convergence_comparison.png")

plt.show()

print()
print("=" * 60)
print("Summary")
print("=" * 60)
print()
print("FEBio Structured Grids (vs FEBio 16×16×64):")
for cells, err in zip(febio_cells, febio_rel_errors):
    print(f"  Cells: {cells:6d} | Relative Error: {err:.6e}")

print()
print("OpenDiHu NN Grids (vs OpenDiHu 16×16×64):")
for cells, err in zip(opendihu_cells, opendihu_vs_opendihu_errors):
    print(f"  Cells: {cells:6d} | Relative Error: {err:.6e}")

print()
print("OpenDiHu NN Grids (vs FEBio 16×16×64):")
for cells, err in zip(opendihu_cells, opendihu_vs_febio_errors):
    print(f"  Cells: {cells:6d} | Relative Error: {err:.6e}")
