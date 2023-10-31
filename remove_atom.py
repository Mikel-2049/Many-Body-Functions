def remove_atom_and_update_triplets(atom_to_remove, found_triplets, atom_triplets, triplet_energies, total_energy):
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

        
    return new_total_energy, found_triplets, triplet_energies
