import csv
import re

# Define your file paths based on your directory structure
csv_filename = 'jobs/final_stretch_values.csv'
template_filename = 'ellipsoid_prestrain.feb'
output_filename = 'ellipsoid_prestrain_ready.feb'

# 1. Load the stretch values from the CSV into a dictionary
stretch_data = {}
print(f"Loading stretch values from {csv_filename}...")
with open(csv_filename, 'r') as f:
    reader = csv.reader(f)
    next(reader)  # Skip the header row
    for row in reader:
        # row[0] is Element_ID, row[1] is Stretch_Value
        stretch_data[row[0]] = row[1]

# 2. Read the template and inject the values into a new file
print(f"Injecting values into {template_filename}...")
with open(template_filename, 'r') as infile, open(output_filename, 'w') as outfile:
    for line in infile:
        # Look for the line containing the element ID, e.g., <e lid="1">0</e>
        match = re.search(r'<e lid="(\d+)">', line)
        
        if match:
            lid = match.group(1)
            # If we have a stretch value for this element, replace the line
            if lid in stretch_data:
                # Grab the whitespace at the start of the line to keep indentation neat
                indent = line.split('<')[0]
                new_line = f'{indent}<e lid="{lid}">{stretch_data[lid]}</e>\n'
                outfile.write(new_line)
            else:
                outfile.write(line) # Fallback if ID is missing
        else:
            outfile.write(line) # Write all normal XML lines exactly as they are

print(f"Success! Your ready-to-run file is saved as: {output_filename}")
