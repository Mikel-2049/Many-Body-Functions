def find_most_contributing_atom(triplet_energies, atom_triplets, total_energy):
    max_energy_diff = 0
    most_contributing_atom = None
    
    for atom, associated_triplets in atom_triplets.items():
        energy_to_remove = sum(triplet_energies[t] for t in associated_triplets)
        remaining_energy = total_energy - energy_to_remove
        
        if remaining_energy > max_energy_diff:
            energy_after_removal = remaining_energy
            most_contributing_atom = atom

            
    return most_contributing_atom, energy_after_removal
