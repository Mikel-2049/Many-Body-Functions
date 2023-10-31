from Stillinger_Weber import f3  # Import the Stillinger Weber function

def calculate_and_store_energies(triplet_data, atoms, coord_to_index):
    triplet_energies = {}
    atom_triplets = {index: [] for index in range(len(atoms))}
    
    total_energy = 0.0
    
    for triplet, data in triplet_data.items():
        distances = data['distances']
        angles = data['angles']

        energy = f3(distances, angles)
        triplet_energies[triplet] = energy
        total_energy += energy
        #print(f"Debug: total_energy calculated in calculate_and_store_energies = {total_energy}")

        
        for coord in triplet:
            index = coord_to_index[coord]
            atom_triplets[index].append(triplet)
            
    return triplet_energies, atom_triplets, total_energy

