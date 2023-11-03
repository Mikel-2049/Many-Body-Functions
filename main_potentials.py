import numpy as np
import matplotlib.pyplot as plt

from read_pof_file import read_pof_file
from unique_triplets_m2 import find_unique_triplets
from calculate_distances_and_angles import calculate_distances_and_angles
from calculate_energies import calculate_and_store_energies
from find_most_contributing_atom import find_most_contributing_atom  
from remove_atom import remove_atom_and_update_triplets


def main():

    # Ask the user to select a potential
    print("Select a potential to use:")
    print("1. Stillinger-Weber")
    print("2. Axilrod-Teller")
    choice = input("Enter the number of your choice: ")
    
    # Map the user choice to the potential name
    if choice == '1':
        selected_potential = 'Stillinger-Weber'
    elif choice == '2':
        selected_potential = 'Axilrod-Teller'
    else:
        print("Invalid choice. Exiting.")
        return
    

    # Define the file paths for the POF files
    pof_file_paths = [
        'geometries\WFG3_02D_Sampled.pof'
    ]

    iteration_counter = 0

    # Loop through each POF file
    for file_path in pof_file_paths:
        print(f"Processing {file_path}...")
        
        # Read the POF file
        dimensionality, atoms, coord_to_index = read_pof_file(file_path)

        print(f"Number of atoms: {len(atoms)}")
        print(f"Dimensionality: {dimensionality}")

        # Initialize the list to store unique triplets
        atomsTuple = [tuple(inner_list) for inner_list in atoms]
        found_triplets = set()
        
        # Define the number of atoms you want to keep
        num_atoms_to_keep = 10  # Or any other number you choose

        # Start the iterative loop
        while len(atoms) > num_atoms_to_keep:
            # Find unique triplets from the list of atoms
            find_unique_triplets(atomsTuple, found_triplets)
            print(f"Number of unique triplets: {len(found_triplets)}")

            # Calculate distances and angles
            triplet_data = calculate_distances_and_angles(atoms, found_triplets, dimensionality)

            # Calculate and store energies
            triplet_energies, atom_triplets, total_energy = calculate_and_store_energies(triplet_data, atoms, coord_to_index, selected_potential)

            # Find the most contributing atom
            most_contributing_atom, energy_after_removal = find_most_contributing_atom(triplet_energies, atom_triplets, total_energy)

            print(f"Most contributing atom = {most_contributing_atom}")

            # Remove the atom and update triplets and energies
            new_total_energy, found_triplets, triplet_energies, new_atom_triplets, coord_to_index = remove_atom_and_update_triplets(most_contributing_atom, found_triplets, atom_triplets, triplet_energies, total_energy, coord_to_index)
            

            # Update atoms and atomsTuple
            atoms.pop(most_contributing_atom)
            atomsTuple.pop(most_contributing_atom)


            # Increment the iteration counter
            iteration_counter += 1

            # Only plot every 10 iterations
            if iteration_counter % 10 == 0:
                # After you've processed your atoms, convert the list of atoms to an array
                atoms_array = np.array(atoms)  # Assume 'atoms' is a list of lists or list of tuples

                # Plot depending on the dimensionality
                if dimensionality == 2:
                    # Create a 2D scatter plot using the first two dimensions of the atoms' coordinates
                    plt.scatter(atoms_array[:, 0], atoms_array[:, 1])
                    plt.xlabel("X-coordinate")
                    plt.ylabel("Y-coordinate")
                    plt.title("Atoms Plot in 2D")
                    plt.show()

                elif dimensionality == 3:
                    # Create a new figure for 3D plot
                    fig = plt.figure()
                    ax = fig.add_subplot(111, projection='3d')
                    # Create a 3D scatter plot using the coordinates of the atoms
                    ax.scatter(atoms_array[:, 0], atoms_array[:, 1], atoms_array[:, 2])
                    ax.set_xlabel("X-coordinate")
                    ax.set_ylabel("Y-coordinate")
                    ax.set_zlabel("Z-coordinate")
                    ax.set_title("3D Plot of Atoms")
                    plt.show()
        

if __name__ == "__main__":
    main()
