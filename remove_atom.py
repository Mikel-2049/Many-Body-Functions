def remove_atom_and_update_triplets(atom_to_remove, found_triplets, atom_triplets, triplet_energies, total_energy, coord_to_index):
    # Remove triplets associated with the atom
    triplets_to_remove = atom_triplets[atom_to_remove]
    
    # Update the set of found triplets
    found_triplets -= set(triplets_to_remove)
    
    # Update the total energy
    energy_to_remove = sum(triplet_energies[t] for t in triplets_to_remove)
    new_total_energy = total_energy - energy_to_remove
    
    # Remove the entries for these triplets from triplet_energies
    for triplet in triplets_to_remove:
        del triplet_energies[triplet]

    # Remove the entries for the atom from atom_triplets
    del atom_triplets[atom_to_remove]
    
    # Update coord_to_index mapping and indices in atom_triplets
    for coord, index in coord_to_index.items():
        if index > atom_to_remove:
            coord_to_index[coord] -= 1

    new_atom_triplets = {}
    for index, triplets in atom_triplets.items():
        new_index = index - 1 if index > atom_to_remove else index
        new_atom_triplets[new_index] = triplets
    
    return new_total_energy, found_triplets, triplet_energies, new_atom_triplets, coord_to_index

def remove_atom_from_triplets(atom_to_remove, found_triplets):
    # Create a set to hold triplets that need to be removed
    triplets_to_remove = set()

    # Identify triplets that include the atom to remove
    for triplet in found_triplets:
        if atom_to_remove in triplet:
            triplets_to_remove.add(triplet)

    # Remove identified triplets from found_triplets
    found_triplets.difference_update(triplets_to_remove)

    return found_triplets


def update_triplet_data(triplet_data, atom_to_remove):
    new_triplet_data = {}

    for triplet, data in triplet_data.items():
        # Check if the current triplet includes the removed atom
        if atom_to_remove not in triplet:
            # Adjust indices in the triplet
            adjusted_triplet = tuple(index - 1 if index > atom_to_remove else index for index in triplet)
            
            # Transfer valid data to new_triplet_data
            new_triplet_data[adjusted_triplet] = data

    return new_triplet_data
