import random
import math

# Constants
rho = 5.4307  # Atomic density for silicon in Å⁻³
alpha = 5.5  # Parameter α for the EAM potential
step_size = 0.1  # Step size for placing atoms along the line

# Define the line function y = -x + 4
def line_function(x):
    return -x + 4

def pair_potential(R_ij):
    epsilon = 2.4  # Energy scale parameter (adjust as needed)
    sigma = 0.22    # Length scale parameter (adjust as needed)
    return 4 * epsilon * ((sigma / R_ij) ** 12 - (sigma / R_ij) ** 6)

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
    embedding_energy = alpha * math.sqrt(host_density) # negative = attractive || positive = repulsive
    return embedding_energy

# Calculate the pair potential energy for all pairs of atoms
def calculate_pair_potential_energy(atoms):
    pair_potential_energy = 0.0
    for i in range(len(atoms)):
        for j in range(i + 1, len(atoms)):
            xi, yi = atoms[i]
            xj, yj = atoms[j]
            rij = math.sqrt((xi - xj)**2 + (yi - yj)**2)
            
            # Check if rij is very close to zero, and if so, skip the division
            if rij < 1e-6:  # You can adjust this threshold as needed
                continue
            
            phi_ij = pair_potential(rij)   # Example Lennard-Jones-like potential
            pair_potential_energy += phi_ij
    return pair_potential_energy


# Generate random positions for the atoms along the line with one decimal place precision
random_x_values = [round(random.uniform(0, 4), 1) for _ in range(4)]
#random_x_values.sort()  # Sort the values for clarity

# Create a list of atom positions along the line with random x values
atoms = [(x, line_function(x)) for x in random_x_values]

# Calculate the energy for each atom
energies = {}
for i, (x, y) in enumerate(atoms):
    embedding_energy = calculate_embedding_energy(x, y)
    pair_potential_energy = calculate_pair_potential_energy(atoms[:i] + atoms[i + 1:])
    total_energy = embedding_energy + (0.5 * pair_potential_energy)
    energies[f'Atom {chr(65 + i)}'] = total_energy

# Print the calculated energies for all atoms
for atom, energy in energies.items():
    print(f'{atom}: Energy = {energy:.4f} eV')
