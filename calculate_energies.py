from Stillinger_Weber import f3
from Axilrod_Teller import axilrod_teller_potential

def calculate_and_store_energies(triplet_data, atoms, coord_to_index, selected_potential):

    triplet_energies = {}
    atom_triplets = {index: [] for index in range(len(atoms))}
    
    total_energy = 0.0
    
    for triplet, data in triplet_data.items():
        distances = data['distances']
        angles = data['angles']

        if selected_potential == 'Stillinger-Weber':
            energy = f3(distances, angles)
        elif selected_potential == 'Axilrod-Teller':
            energy = axilrod_teller_potential(distances)
        else:
            print(f"Warning: Unknown potential {selected_potential}.")
        
        triplet_energies[triplet] = energy
        total_energy += energy
    
        for index in triplet:
            atom_triplets[index].append(triplet)
            
    return triplet_energies, atom_triplets, total_energy

