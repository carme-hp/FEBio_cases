import pyvista as pv
import numpy as np

# Updated file paths reflecting the jobs/VTK_files/ directory
file_step_0 = 'jobs/VTK_files/ellipsoid_prestrain_ready.t00.vtk'
file_step_1 = 'jobs/VTK_files/ellipsoid_prestrain_ready.t01.vtk'

def inspect_vtk_step(filename, step_name):
    print(f"\n--- Inspecting {step_name} ---")
    try:
        # Load the mesh using PyVista
        mesh = pv.read(filename)
        
        # Check what data arrays FEBio actually saved into this VTK
        print(f"Available Point Data (Nodes): {list(mesh.point_data.keys())}")
        print(f"Available Cell Data (Elements): {list(mesh.cell_data.keys())}")
        
        # We are looking for the stretch or displacement data. 
        for array_name in mesh.cell_data.keys():
            if 'stretch' in array_name.lower() or 'strain' in array_name.lower():
                data = mesh.cell_data[array_name]
                print(f"Found Cell Array '{array_name}': Min = {np.min(data):.6f}, Max = {np.max(data):.6f}")
                
        for array_name in mesh.point_data.keys():
            if 'displacement' in array_name.lower():
                data = mesh.point_data[array_name]
                # Calculate the magnitude of the displacement vectors
                magnitudes = np.linalg.norm(data, axis=1)
                print(f"Found Point Array '{array_name}': Max Displacement Magnitude = {np.max(magnitudes):.6f}")
                
    except FileNotFoundError:
        print(f"ERROR: Could not find {filename}. Did FEBio export this step?")
    except Exception as e:
        print(f"An error occurred while reading {filename}: {e}")

# Run the inspection
inspect_vtk_step(file_step_0, "Time Step 0 (Initial State)")
inspect_vtk_step(file_step_1, "Time Step 1 (First Load Step)")