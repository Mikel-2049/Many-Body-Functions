import numpy as np
import matplotlib.pyplot as plt

# Given parameters
A = 7.049556277
B = 0.6022245584
p = 4
a = 1.80
sigma = 0.20951  # in nm
lambda_ = 21.0
epsilon = 50.0  # in kcal/mol
alpha = 3.4723e-12
epsilon_dist = 1e-10  # A very small distance to avoid division by zero

# Function to calculate pairwise potential between two atoms
def phi_2(r):
    r = max(r, epsilon_dist)  # Replace zero with epsilon_dist
    if r >= a:
        return 0.0
    else:
        return A * ((B / r) ** p - 1) * np.exp(sigma / (r - a))

# Function to calculate three-body potential between three atoms
def phi_3(r_ij, r_ik, cos_theta_ijk):
    return lambda_ * epsilon * (cos_theta_ijk + 1/3)**2 * np.exp(alpha / (r_ij - a)) * np.exp(alpha / (r_ik - a))

# Function to generate atoms
def generate_atoms(num_atoms):
    random_values = np.random.uniform(0, 5, num_atoms)
    x_values = np.round(random_values, 2)
    y_values = x_values ** 2 - (5 * x_values) + 5
    atoms = np.column_stack((x_values, y_values))
    return atoms

# Function to calculate individual interaction energy for each atom
def individual_interaction_energy(atoms):
    num_atoms = len(atoms)
    interaction_energy = np.zeros(num_atoms)
    
    for i in range(num_atoms):
        for j in range(num_atoms):
            if i == j:
                continue
            
            r_ij = np.linalg.norm(atoms[i] - atoms[j])
            r_ij = max(r_ij, epsilon_dist)  # Replace zero with epsilon_dist
            
            interaction_energy[i] += phi_2(r_ij)
            
            for k in range(num_atoms):
                if k == i or k == j:
                    continue
                
                r_ik = np.linalg.norm(atoms[i] - atoms[k])
                r_ik = max(r_ik, epsilon_dist)  # Replace zero with epsilon_dist
                
                # Ensure we're not dividing by zero
                cos_theta_ijk = np.dot(atoms[i] - atoms[j], atoms[i] - atoms[k]) / (r_ij * r_ik)
                
                interaction_energy[i] += phi_3(r_ij, r_ik, cos_theta_ijk)
    
    return interaction_energy


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


def main():
    # Generate atoms
    #num_atoms = 50  # for example
    #atoms = generate_atoms(num_atoms)

    atoms = given_atoms()

    while len(atoms) > 11:

        # Calculate individual interaction energy for each atom
        individual_energy = individual_interaction_energy(atoms)

        print("Individual interaction energy for each atom:", individual_energy)

        # Extract x and y coordinates
        x_coords = atoms[:, 0]
        y_coords = atoms[:, 1]

        # Plotting
        plt.figure(figsize=(10, 6))
        plt.scatter(x_coords, y_coords, s=100, c=individual_energy, cmap='viridis', edgecolors='k')
        plt.colorbar(label='Interaction Energy')
        plt.xlabel('X Coordinate')
        plt.ylabel('Y Coordinate')
        plt.title('Atoms Position and Interaction Energy')
        plt.grid(True)
        plt.show()

         # Find the index of the atom with the highest energy
        max_energy_idx = np.argmax(individual_energy)
        
        # Remove that atom
        atoms = np.delete(atoms, max_energy_idx, axis=0)


    # Finally, plot the remaining 11 atoms
    individual_energies = individual_interaction_energy(atoms)
    x_coords = atoms[:, 0]
    y_coords = atoms[:, 1]
    plt.figure(figsize=(10, 6))
    plt.scatter(x_coords, y_coords, s=100, c=individual_energies, cmap='viridis', edgecolors='k')
    plt.colorbar(label='Interaction Energy')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.title('Final 11 Atoms Position and Interaction Energy')
    plt.grid(True)
    plt.show()




if __name__ == "__main__":
    main()