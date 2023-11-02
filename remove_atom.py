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

