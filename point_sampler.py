import os
import random

# Define the source and destination directories
source_dir = 'test_geometries\OG'
destination_dir = 'test_geometries\Sampled'

# Number of points to sample
num_sampled_points = 500

# Ensure the destination directory exists
if not os.path.exists(destination_dir):
    os.makedirs(destination_dir)

# Iterate over all files in the source directory
for filename in os.listdir(source_dir):
    if filename.endswith(".pof"):
        file_path = os.path.join(source_dir, filename)
        output_file_path = os.path.join(destination_dir, filename.rsplit('.', 1)[0] + '_sampled.pof')

        # Read the original header to get the dimensionality
        with open(file_path, 'r') as file:
            original_header = file.readline().strip()
            _, total_points, dimensionality = original_header.split()
            new_header_corrected = f"# {num_sampled_points} {dimensionality}"

        # Read all lines from the file after the header
        with open(file_path, 'r') as file:
            next(file)  # Skip the header line
            data_points = [line.strip() for line in file]

        # Randomly sample the specified number of points
        sampled_points = random.sample(data_points, min(num_sampled_points, len(data_points)))

        # Write the sampled points to the new file with the corrected header
        with open(output_file_path, 'w') as file:
            file.write(new_header_corrected + '\n')
            file.writelines('\n'.join(sampled_points) + '\n')

        print(f"Sampled file created: {output_file_path}")