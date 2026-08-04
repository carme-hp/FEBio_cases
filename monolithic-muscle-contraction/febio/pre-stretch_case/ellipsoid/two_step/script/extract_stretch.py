import csv

# Define the names of your files relative to your main two_step directory
input_filename = 'jobs/stretch_values.txt'
output_filename = 'jobs/final_stretch_values.csv'

# This list will act as our temporary storage bucket
final_step_data = []

print(f"Reading data from {input_filename}...")

with open(input_filename, 'r') as infile:
    for line in infile:
        # Remove any extra whitespace or hidden newline characters
        line = line.strip()

        # Skip empty lines
        if not line:
            continue

        # The Basic Concept: When a new time step begins, empty the bucket.
        # By the end of the file, it will only contain the final step!
        if line.startswith('*Step'):
            final_step_data = []
            continue

        # Skip the other header lines (*Time, *Data)
        if line.startswith('*'):
            continue

        # Split the line into Element ID and the Stretch Value.
        # .split() automatically handles spaces. 
        parts = line.replace(',', ' ').split()

        if len(parts) >= 2:
            elem_id = parts[0]
            stretch_val = parts[1]
            final_step_data.append([elem_id, stretch_val])

# Now, write the final block to a standard CSV file
print(f"Writing final time step data to {output_filename}...")

with open(output_filename, 'w', newline='') as outfile:
    writer = csv.writer(outfile)
    
    # Write the column headers first
    writer.writerow(['Element_ID', 'Stretch_Value'])
    
    # Write all the extracted element data
    writer.writerows(final_step_data)

print(f"Success! Extracted {len(final_step_data)} elements.")