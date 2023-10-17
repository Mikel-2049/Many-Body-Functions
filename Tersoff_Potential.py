import numpy as np
import matplotlib.pyplot as plt

# Constants from your provided data:
A = 3264.7
B = 95.373
lambda_1 = 3.2394
lambda_2 = 1.3258
lambda_3 = lambda_2
R = 3.0
D = 0.2
beta = 0.33675
n = 22.956
c = 4.8381
d = 2.0417
h = 0.0000
m = 4.5
theta_0 = 0

def f_C(r):
    if r < R - D:
        return 1
    elif r <= R + D:
        return 0.5 - 0.5 * np.sin(np.pi / 2 * (r - R) / D)
    else:
        return 0

def V_A(r):
    return A * np.exp(-lambda_1 * r)

def V_R(r):
    return B * np.exp(-lambda_2 * r)

def g(theta):
    gamma = 1 + c**2/d**2 - c**2/(d**2 + (h - np.cos(theta))**2)
    return gamma + c**2/d**2 - gamma / (1 + np.exp(-d * (np.cos(theta) - np.cos(theta_0))))


def bond_order(i, j, atoms):
    rij = np.linalg.norm(atoms[i] - atoms[j])
    chi_ij = 0
    for k in range(len(atoms)):
        if k != i and k != j:
            rik = np.linalg.norm(atoms[i] - atoms[k])
            epsilon = 1e-10  # Small positive number to avoid division by zero
            cos_theta = np.dot(atoms[j] - atoms[i], atoms[k] - atoms[i]) / (rij * rik + epsilon)
            cos_theta = np.clip(cos_theta, -1, 1)  # Clipping cos_theta to avoid errors
            theta = np.arccos(cos_theta)
            power_val = abs(rij - rik)**m  # Using absolute value
            if -100 < power_val < 100:  # Adjust if needed
                chi_ij += f_C(rik) * g(theta) * np.exp(lambda_3**m * power_val)
    chi_ij = min(chi_ij, 10)  # Setting an upper limit to chi_ij
    power_result = chi_ij**n
    return (1 + beta**n * power_result)**(-0.5/n)

def energy_for_atom(atom_idx, atoms):
    energy = 0
    for j in range(len(atoms)):
        if atom_idx != j:
            energy += interaction_energy(atom_idx, j, atoms)
    return energy

def total_interaction_energy(atoms):
    energies = [energy_for_atom(i, atoms) for i in range(len(atoms))]
    return np.sum(energies), energies


def interaction_energy(i, j, atoms):
    rij = np.linalg.norm(atoms[i] - atoms[j])
    bij = bond_order(i, j, atoms)
    return f_C(rij) * (V_A(rij) - bij * V_R(rij))



def generate_atoms(num_atoms, step_size):
    random_values = np.random.uniform(0, 5, num_atoms) 
    x_values = np.round(random_values, 2)
    y_values = x_values **2 - (5*x_values) + 5
    atoms = np.column_stack((x_values, y_values))
    return atoms


def main():
    atoms = generate_atoms(50, 0.01)
    total_energy, individual_energies = total_interaction_energy(atoms)
    print(total_energy)
    print(individual_energies)

    # Extract x and y coordinates
    x_coords = atoms[:, 0]
    y_coords = atoms[:, 1]

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.scatter(x_coords, y_coords, s=100, c=individual_energies, cmap='viridis', edgecolors='k')
    plt.colorbar(label='Interaction Energy')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.title('Atoms Position and Interaction Energy')
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    main()