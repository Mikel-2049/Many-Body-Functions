import random
import math
import numpy as np
import matplotlib.pyplot as plt

# Constants
rho = 5.4307  # Atomic density for silicon in Å⁻³
alpha = 5.5  # Parameter α for the EAM potential
step_size = 0.1  # Step size for placing atoms along the line

def line_function(x):
    return -x + 4

def pair_potential(R_ij):
    epsilon = 2.4  
    sigma = 0.22  
    return 4 * epsilon * ((sigma / R_ij) ** 12 - (sigma / R_ij) ** 6)

def calculate_host_density(x, y):
    host_density = 0.0
    for xi in range(-3, 4):
        if xi * step_size != x:
            rij = math.sqrt((xi * step_size - x)**2 + (line_function(xi * step_size) - y)**2)
            host_density += (rho ** alpha) / rij
    return host_density

def calculate_embedding_energy(x, y):
    host_density = calculate_host_density(x, y)
    embedding_energy = alpha * math.sqrt(host_density)
    return embedding_energy

def calculate_pair_potential_energy(atoms):
    pair_potential_energy = 0.0
    for i in range(len(atoms)):
        for j in range(i + 1, len(atoms)):
            xi, yi = atoms[i]
            xj, yj = atoms[j]
            rij = math.sqrt((xi - xj)**2 + (yi - yj)**2)
            
            if rij < 1e-6:  
                continue
            
            phi_ij = pair_potential(rij) 
            pair_potential_energy += phi_ij
    return pair_potential_energy

#def calculate_total_energy_for_atom(atoms, index):
    x, y = atoms[index]
    embedding_energy = calculate_embedding_energy(x, y)
    pair_potential_energy = calculate_pair_potential_energy(np.delete(atoms, index, axis=0))
    return embedding_energy + (0.5 * pair_potential_energy)

#def plot_atoms(atoms):
    x, y = atoms[:, 0], atoms[:, 1]
    plt.scatter(x, y, s=100, cmap='viridis', edgecolors='k')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Atom Positions')
    plt.show()

def given_atoms():
    atoms = np.array([
        (0, 1),
        (0.1, 0.9),
        (0.2, 0.8),
        (0.25, 0.75),
        (0.3, 0.7),
        (0.4, 0.6),
        (0.5, 0.5),
        (0.6, 0.4),
        (0.7, 0.3),
        (0.8, 0.2),
        (0.9, 0.1),
        (0.93, 0.07),
        (0.97, 0.03),
        (1, 0)
    ])
    return atoms

def calculate_total_energy_for_atom(atoms, i):
    x, y = atoms[i]
    embedding_energy = calculate_embedding_energy(x, y)
    pair_potential_energy = calculate_pair_potential_energy(np.delete(atoms, i, axis=0))
    total_energy = embedding_energy + (0.5 * pair_potential_energy)
    return total_energy

def main():
    atoms = given_atoms()
    while len(atoms) > 11:
        energies = []
        for i in range(len(atoms)):
            energy = calculate_total_energy_for_atom(atoms, i)
            energies.append(energy)

        # Normalize energies for plotting (Optional)
        norm_energies = [e / max(energies) for e in energies]

        # Plot the system
        x, y = atoms[:, 0], atoms[:, 1]
        plt.scatter(x, y, s=100, c=norm_energies, cmap='viridis', edgecolors='k')
        plt.colorbar()
        plt.show()

        # Identify the atom with the highest energy and remove it
        max_energy_index = np.argmax(energies)
        print(f"Removing atom at index {max_energy_index} with energy {energies[max_energy_index]:.4f} eV")
        atoms = np.delete(atoms, max_energy_index, axis=0)

    # For the final plot with only 11 atoms
    energies = [calculate_total_energy_for_atom(atoms, i) for i in range(len(atoms))]
    norm_energies = [e / max(energies) for e in energies]  # Normalize for plotting (Optional)
    x, y = atoms[:, 0], atoms[:, 1]
    plt.scatter(x, y, s=100, c=norm_energies, cmap='viridis', edgecolors='k')
    plt.colorbar()
    plt.show()

if __name__ == "__main__":
    main()