import pyvista as pv
import numpy as np

# --- HYPOTHESIS TEST: Phase 1 Final vs Phase 2 Step 1 ---
file_phase1 = 'jobs/VTK_files/ellipsoid_initialpull_30.t30.vtk'
file_phase2_t1 = 'jobs/VTK_files/ellipsoid_prestrain_ready.t01.vtk'

def check_hypothesis(file1, file2):
    print(f"Loading Phase 1 (t=30): {file1}")
    print(f"Loading Phase 2 (t=0.1): {file2}")
    
    try:
        mesh1 = pv.read(file1)
        mesh2 = pv.read(file2)
        
        print("\n--- Array Extraction at t=0.1 ---")
        
        # 1. Check Fiber Stretch
        if 'fiber_stretch' in mesh1.cell_data and 'fiber_stretch' in mesh2.cell_data:
            stretch1 = mesh1.cell_data['fiber_stretch']
            stretch2 = mesh2.cell_data['fiber_stretch']
            
            print(f"Phase 1 Max Fiber Stretch (t=30): {np.max(stretch1):.6f}")
            print(f"Phase 2 Max Fiber Stretch (t=0.1): {np.max(stretch2):.6f}")
            
            stretch_diff = np.max(np.abs(stretch1 - stretch2))
            print(f"Maximum difference in Fiber Stretch: {stretch_diff:.6f}")
        
        print("\n---------------------------------")
        
        # 2. Check Stress
        if 'stress' in mesh1.cell_data and 'stress' in mesh2.cell_data:
            stress1 = mesh1.cell_data['stress']
            stress2 = mesh2.cell_data['stress']
            stress_diff = np.max(np.abs(stress1 - stress2))
            print(f"Maximum difference in Cauchy Stress: {stress_diff:.6f}")
            
    except FileNotFoundError as e:
        print(f"ERROR: Could not find a file. {e}")

# Run the test
check_hypothesis(file_phase1, file_phase2_t1)
