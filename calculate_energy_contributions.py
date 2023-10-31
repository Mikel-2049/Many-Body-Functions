def calculate_energy_contributions(triplet_energies, atom_triplets):
    energy_contributions = {}
    for atom, associated_triplets in atom_triplets.items():
        for triplet in associated_triplets:
            if triplet not in triplet_energies:
                print(f"Debug: Triplet {triplet} not found in triplet_energies.")

    return energy_contributions
