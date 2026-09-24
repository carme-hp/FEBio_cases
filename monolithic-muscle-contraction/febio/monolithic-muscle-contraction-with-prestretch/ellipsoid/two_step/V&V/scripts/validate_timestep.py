import math

# Define the file paths
file_30_steps = 'jobs/stretch_values_30.txt'
file_15_steps = 'jobs/stretch_values_15.txt'

def extract_final_step_to_dict(filename):
    """
    Reads the FEBio log file and returns a dictionary of the final step's stretch values.
    Keys are Element IDs, Values are the Stretch (Fzz).
    """
    final_data = {}
    
    with open(filename, 'r') as infile:
        for line in infile:
            line = line.strip()
            
            # Skip empty lines
            if not line:
                continue
                
            # The Bucket Concept: Empty dictionary when a new step starts
            if line.startswith('*Step'):
                final_data = {} 
                continue
                
            # Skip header lines
            if line.startswith('*'):
                continue
                
            # Split into ID and Value
            parts = line.replace(',', ' ').split()
            if len(parts) >= 2:
                elem_id = parts[0]
                stretch_val = float(parts[1]) # Convert to float for math!
                final_data[elem_id] = stretch_val
                
    return final_data

print("Extracting data from 30-step simulation...")
data_30 = extract_final_step_to_dict(file_30_steps)

print("Extracting data from 15-step simulation...")
data_15 = extract_final_step_to_dict(file_15_steps)

# Validation: Compare the two dictionaries
print("\n--- Performing Verification & Validation ---")

max_difference = 0.0
element_with_max_diff = None

for elem_id in data_30:
    if elem_id in data_15:
        # Calculate the absolute mathematical difference
        diff = abs(data_30[elem_id] - data_15[elem_id])
        
        if diff > max_difference:
            max_difference = diff
            element_with_max_diff = elem_id

print(f"Total elements compared: {len(data_30)}")
print(f"Maximum difference found: {max_difference:.10f} (at Element ID: {element_with_max_diff})")

# Check if the difference is practically zero (accounting for minor floating-point rounding)
tolerance = 1e-6
if max_difference < tolerance:
    print("\nSUCCESS: The time step size does not influence the final stretch.")
    print("Subtask 1 V&V mathematically proven for your supervisors!")
else:
    print("\nWARNING: The differences are larger than expected. Check the solver tolerances.")
