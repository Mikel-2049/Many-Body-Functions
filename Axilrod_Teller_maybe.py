import numpy as np
import matplotlib.pyplot as plt

num_atoms = 50

def generate_atoms(num_atoms, step_size):
    
    random_values = np.random.uniform(0, 4, num_atoms) # Generate an array with 30 random values in the range from 0 to 4
    x_values = np.round(random_values, 2) # Round the values to two decimal places
    y_values = -x_values + 4  # Compute y values based on the function -x + 4
    atoms = np.column_stack((x_values, y_values))  # Combine x and y values to create atom coordinates
    return atoms



import numpy as np

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



def main():
    num_atoms = 50
    step_size=0.1
    atoms = generate_atoms(num_atoms, step_size)
    # Extract x and y coordinates from the atoms
    x_coords = atoms[:, 0]
    y_coords = atoms[:, 1]

    # Plotting
    plt.scatter(x_coords, y_coords, marker='o', color='blue')
    plt.title("Atoms Scatter Plot")
    plt.xlabel("X-values")
    plt.ylabel("Y-values")
    plt.grid(True)
    plt.show()


    interactions = []
    for i in range(1, num_atoms + 1):
        if i == 1:
            atom1, atom2, _ = atoms[i-1], atoms[i], None
        elif i == num_atoms:
            atom1, atom2, _ = atoms[i-2], atoms[i-1], None
        else:
            atom1, atom2, atom3 = atoms[i-2], atoms[i-1], atoms[i]
            interactions.append(interaction_value(atom1, atom2, atom3))

    print(interactions)


    # Identify the index of the atom with the highest interaction value
    index_highest_interaction = interactions.index(max(interactions))
    index_lowest_interaction = interactions.index(min(interactions))
    print(index_highest_interaction, max(interactions))
    print(index_lowest_interaction, min(interactions))

    # Extract x and y coordinates from the atoms
    x_coords = atoms[:, 0]
    y_coords = atoms[:, 1]

    # Plotting all atoms in blue
    plt.scatter(x_coords, y_coords, marker='o', color='blue')

    # Highlighting the atom with the highest interaction value in red
    plt.scatter(x_coords[index_highest_interaction], y_coords[index_highest_interaction], marker='o', color='red')

    # Highlighting the atom with the lowest interaction value in yellow
    plt.scatter(x_coords[index_lowest_interaction], y_coords[index_lowest_interaction], marker='o', color='yellow')

    plt.title("Atoms Scatter Plot with Atom of Highest Interaction Highlighted")
    plt.xlabel("X-values")
    plt.ylabel("Y-values")
    plt.grid(True)
    plt.show()
        


if __name__ == "__main__":
    main()