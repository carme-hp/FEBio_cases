#!/usr/bin/env python3
"""
Read and compare VTU files to compute relative errors.
Supports both ASCII and binary VTU formats.
"""
import math
import xml.etree.ElementTree as ET


def read_data_values(data_name: str, file_path: str) -> list[float]:
    """
    Read data values from a VTU file.

    Args:
        data_name: Name of the data array to read
        file_path: Path to the VTU file

    Returns:
        List of float values from the data array
    """
    tree = ET.parse(file_path)
    root = tree.getroot()

    for data_array in root.findall(f".//DataArray[@Name='{data_name}']"):
        # ASCII format: data is in text content
        if data_array.text and data_array.text.strip():
            return [float(value) for value in data_array.text.strip().split()]

        # Binary/appended format: use VTK library
        data_format = data_array.get('format', 'ascii')
        if data_format in ['appended', 'binary']:
            try:
                import vtk
                from vtk.util.numpy_support import vtk_to_numpy

                # Suppress VTK error/warning messages
                vtk.vtkLogger.SetStderrVerbosity(vtk.vtkLogger.VERBOSITY_OFF)

                # Read the VTU file using VTK
                reader = vtk.vtkXMLUnstructuredGridReader()
                reader.SetFileName(file_path)
                reader.Update()

                output = reader.GetOutput()
                num_points = output.GetNumberOfPoints()

                if num_points == 0:
                    raise ValueError(f"Failed to read VTU file '{file_path}' - file may be corrupted")

                point_data = output.GetPointData()
                array = point_data.GetArray(data_name)

                if array is None:
                    available = [point_data.GetArrayName(i) for i in range(point_data.GetNumberOfArrays())]
                    raise ValueError(f"Data array '{data_name}' not found in {file_path}. "
                                     f"Available arrays: {available}")

                return vtk_to_numpy(array).tolist()

            except ImportError:
                raise ImportError(
                    f"VTU file '{file_path}' uses binary format. "
                    f"Install VTK library: pip install vtk"
                )

    raise ValueError(f"Data array '{data_name}' not found in {file_path}")


def get_relative_error(reference_file: str, simulation_file: str, data_name: str) -> float:
    """
    Compute relative L2 error between two VTU files.

    Args:
        reference_file: Path to reference VTU file
        simulation_file: Path to simulation VTU file
        data_name: Name of the data array to compare

    Returns:
        Relative L2 error
    """
    reference_values = read_data_values(data_name, reference_file)
    simulation_values = read_data_values(data_name, simulation_file)

    abs_error = math.sqrt(sum((v1 - v2) ** 2 for v1, v2 in zip(simulation_values, reference_values)))
    reference_norm = math.sqrt(sum(v ** 2 for v in reference_values))
    rel_error = abs_error / reference_norm if reference_norm > 0 else 0

    print(f"Reference: {reference_file}")
    print(f"Simulation: {simulation_file}")
    print(f"Relative error: {rel_error}")

    return rel_error
