import random

file_path = 'geometries\DTLZ7_03D.pof'

# Output file path
output_file_path = 'geometries\DTLZ7_03D_250.pof'

# Number of points to sample
num_sampled_points = 250

# Read the original header to get the dimensionality
with open(file_path, 'r') as file:
    original_header = file.readline().strip()

# Extract dimensionality from the original header
_, total_points, dimensionality = original_header.split()

# Now, we create the new header with the correct number of points and dimensionality
new_header_corrected = f"# {num_sampled_points} {dimensionality}"

# Read all lines from the file after the header
with open(file_path, 'r') as file:
    # Skip the header line
    next(file)
    # Read the rest of the points
    data_points = [line.strip() for line in file]

# Randomly sample the specified number of points
sampled_points = random.sample(data_points, num_sampled_points)

# Write the sampled points to the new file with the corrected header
with open(output_file_path, 'w') as file:
    file.write(new_header_corrected + '\n')
    file.writelines('\n'.join(sampled_points) + '\n')
    
# Return the path to the new file
output_file_path
