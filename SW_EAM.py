import math
import numpy as np
import matplotlib.pyplot as plt

# EAM parameters (arbitrary values for demonstration)
alpha = 1.0
rho = 1.0
step_size = 1.0

# Function to represent the position of atoms along the line
def line_function(x):
    return -x + 4


# Stillinger-Weber parameters (arbitrary values for demonstration)
lambda_sw = 21.0  # eV
gamma_sw = 1.2  # Å⁻¹
a_sw = 2.7  # Å (cutoff distance)

# Function to calculate angle between two vectors
def angle_between_vectors(v1, v2):
    dot_product = sum(a * b for a, b in zip(v1, v2))
    magnitude_v1 = math.sqrt(sum(a * a for a in v1))
    magnitude_v2 = math.sqrt(sum(a * a for a in v2))
    
    # Handle ZeroDivisionError
    if magnitude_v1 == 0 or magnitude_v2 == 0:
        return 0.0  # or whatever value is appropriate in your context
    
    cos_theta = dot_product / (magnitude_v1 * magnitude_v2)
    
    # Handle math domain error
    if cos_theta > 1.0:
        cos_theta = 1.0
    elif cos_theta < -1.0:
        cos_theta = -1.0
    
    return math.acos(cos_theta)


# Function to calculate the Stillinger-Weber three-body term
def calculate_three_body_term(atom_i, atom_j, atom_k):
    r_ij = math.sqrt((atom_i[0] - atom_j[0])**2 + (atom_i[1] - atom_j[1])**2)
    r_ik = math.sqrt((atom_i[0] - atom_k[0])**2 + (atom_i[1] - atom_k[1])**2)
    
    if r_ij > a_sw or r_ik > a_sw:
        return 0.0  # Beyond cutoff distance
    
    vector_ij = [atom_j[0] - atom_i[0], atom_j[1] - atom_i[1]]
    vector_ik = [atom_k[0] - atom_i[0], atom_k[1] - atom_i[1]]
    theta_ijk = angle_between_vectors(vector_ij, vector_ik)
    
    V3 = lambda_sw * (math.cos(theta_ijk) + 1/3)**2 * \
         math.exp(gamma_sw / (r_ij - a_sw)) * \
         math.exp(gamma_sw / (r_ik - a_sw))
    
    return V3


# Calculate the host density for an atom at position (x, y)
def calculate_host_density(x, y):
    host_density = 0.0
    for xi in range(-3, 4):
        if xi * step_size != x:
            rij = math.sqrt((xi * step_size - x)**2 + (line_function(xi * step_size) - y)**2)
            host_density += (rho ** alpha) / rij
    return host_density

# Calculate the embedding energy for an atom at position (x, y)
def calculate_embedding_energy(x, y):
    host_density = calculate_host_density(x, y)
    embedding_energy = alpha * math.sqrt(host_density)  # negative = attractive || positive = repulsive
    return embedding_energy



# Generate random positions for the atoms along the line with one decimal place precision
random_x_values = [round(np.random.uniform(0, 4), 1) for _ in range(4)]
#random_x_values.sort()  # Sort the values for clarity

# Create a list of atom positions along the line with random x values
atoms = [(x, line_function(x)) for x in random_x_values]

# Initialize a dictionary to store the energy for each atom
atom_energies = {}

# Calculate total energy incorporating EAM and Stillinger-Weber three-body term
def calculate_total_energy_hybrid(atoms):
    total_energy = 0.0
    
    # Calculate pair potential and embedding energy using EAM
    for atom in atoms:
        x, y = atom
        embedding_energy = calculate_embedding_energy(x, y)
        total_energy += embedding_energy
        
        # Initialize the energy for this atom
        atom_energies[atom] = embedding_energy
    
    # Add the three-body term from Stillinger-Weber
    for i in range(len(atoms)):
        for j in range(i+1, len(atoms)):
            for k in range(j+1, len(atoms)):
                three_body_energy = calculate_three_body_term(atoms[i], atoms[j], atoms[k])
                total_energy += three_body_energy
                
                # Distribute the three-body energy equally among the involved atoms
                atom_energies[atoms[i]] += three_body_energy / 3
                atom_energies[atoms[j]] += three_body_energy / 3
                atom_energies[atoms[k]] += three_body_energy / 3
                
    return total_energy



# After generating atoms, calculate the total energy
total_energy = calculate_total_energy_hybrid(atoms)

# Now, atom_energies will contain the energy for each atom
# You can print or otherwise use this data as needed
print(f"Total Energy: {total_energy}")
for atom, energy in atom_energies.items():
    print(f"Energy for atom at {atom}: {energy}")