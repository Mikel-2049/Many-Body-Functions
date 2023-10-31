import numpy as np
import matplotlib.pyplot as plt


def interaction_value(r1, r2, r3, nu = 0.4):
    # Compute vectors pointing from point i to point j
    r12 = r2 - r1
    r21 = -r12
    r23 = r3 - r2
    r32 = -r23
    r31 = r1 - r3
    r13 = -r31
    
    # Compute magnitudes
    r12_mag = np.linalg.norm(r12)
    r23_mag = np.linalg.norm(r23)
    r31_mag = np.linalg.norm(r31)

    # Avoid division by 0
    r12_mag = r12_mag if r12_mag != 0 else 1e-10
    r23_mag = r23_mag if r23_mag != 0 else 1e-10
    r31_mag = r12_mag if r31_mag != 0 else 1e-10
    
    # Compute unit vectors
    r12_hat = r12 / r12_mag
    r21_hat = r21 / r12_mag
    r23_hat = r23 / r23_mag
    r32_hat = r32 / r23_mag
    r31_hat = r31 / r31_mag
    r13_hat = r13 / r31_mag
    
    # Compute the function
    numerator = 1 + 3 * (np.dot(r12_hat, r13_hat) * np.dot(r21_hat, r23_hat) * np.dot(r31_hat, r32_hat))
    denominator = r12_mag**3 * r23_mag**3 * r31_mag**3
    
    return nu * numerator / denominator


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
    atoms = given_atoms()

    while len(atoms) > 10:
        potentials = [0]*len(atoms)  # Initialize a list of zeros with the same length as the number of atoms
        for i in range(len(atoms)):
            atom_i = atoms[i]
            for j in range(len(atoms)):
                if i == j:
                    continue
                atom_j = atoms[j]
                for k in range(len(atoms)):
                    if i == k or j == k:
                        continue
                    atom_k = atoms[k]
                    potentials[j] += interaction_value(atom_i, atom_j, atom_k)  # Add potential to the middle atom


        # Plot the atoms and their potentials
        plt.scatter(atoms[:, 0], atoms[:, 1], c=potentials, cmap='viridis')
        plt.colorbar(label='Potential')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Axilrod-Teller Potential for Atoms')
        plt.show()

        # Remove the atom with the highest potential
        index_highest_potential = np.argmin(potentials)
        atoms = np.delete(atoms, index_highest_potential, axis=0)

    print("Remaining atoms:", atoms)

if __name__ == "__main__":
    main()