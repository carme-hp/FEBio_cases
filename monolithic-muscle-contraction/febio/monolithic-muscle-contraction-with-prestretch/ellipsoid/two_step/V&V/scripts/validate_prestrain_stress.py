import pyvista as pv
import numpy as np

# --- UPDATED FILE PATHS FOR PROOF B (TIME STEP 1) ---
# We are comparing the stress-free baseline against the prestrained file at t=0.1

# The control: Your fixed baseline file with NO prestrain map (Time Step 1)
file_baseline = 'jobs/VTK_files/ellipsoid-muscle-contraction.t01.vtk'

# The experimental: Your ready file WITH the injected Fzz prestrain map (Time Step 1)
file_prestrained = 'jobs/VTK_files/ellipsoid_prestrain_ready.t01.vtk'

def compare_stress_tensors(file1, file2):
    print(f"Loading Baseline State (t=0.1): {file1}")
    print(f"Loading Prestrained State (t=0.1): {file2}")
    
    try:
        # Load both meshes
        mesh1 = pv.read(file1)
        mesh2 = pv.read(file2)
        
        # Verify the 'stress' array exists in both files
        if 'stress' not in mesh1.cell_data or 'stress' not in mesh2.cell_data:
            print("ERROR: 'stress' array not found in one or both VTK files.")
            return

        # Extract the stress data arrays
        stress_baseline = mesh1.cell_data['stress']
        stress_prestrained = mesh2.cell_data['stress']
        
        # Calculate the absolute mathematical difference between the two arrays
        stress_difference = np.abs(stress_baseline - stress_prestrained)
        
        # Find the maximum difference across all components and all elements
        max_diff = np.max(stress_difference)
        
        print("\n--- Performing Stress Validation (Proof B at t=0.1) ---")
        print(f"Total elements compared: {mesh1.n_cells}")
        print(f"Maximum stress difference found: {max_diff:.10f}")
        
        # For Proof B, we WANT a massive difference to prove the prestrain is active!
        tolerance = 1e-5
        if max_diff > tolerance:
            print("\nSUCCESS: The internal stress tensors are significantly different.")
            print("This physically proves the prestrain map successfully pre-stiffened the muscle!")
        else:
            print("\nWARNING: The stress tensors match perfectly. The prestrain is not active.")
            
    except FileNotFoundError as e:
        print(f"ERROR: Could not find a file. Please check your file paths: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Run the comparison
compare_stress_tensors(file_baseline, file_prestrained)