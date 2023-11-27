#include <cmath>  // For std::acos
#include <array>
#include <algorithm>  // For std::min and std::max
#include <iostream>
#include <tuple>
#include <vector>
#include <map>
#include <set>
#include <iostream>

using namespace std;

// Forward declare potential functions
double f3(const array<double, 3>& distances, const array<double, 3>& angles);
double axilrod_teller_potential(const array<double, 3>& distances, double nu = -4);

// Function to calculate and store energies
tuple<map<tuple<int, int, int>, double>, double> calculate_and_store_energies(
    const map<tuple<int, int, int>, tuple<array<double, 3>, tuple<double, double, double>>>& triplet_data, 
    const vector<vector<float>>& atoms, 
    const map<vector<float>, int>& coord_to_index, 
    const string& selected_potential,
    map<pair<int, int>, double>& distance_map, // Added distance_map as a parameter
    map<int, vector<tuple<int, int, int>>>& atom_triplets) {

    //cout << "[calculate_energies beginning] Atom Triplets Size: " << atom_triplets.size() << endl;

    map<tuple<int, int, int>, double> triplet_energies;
    double total_energy = 0.0;

    for (const auto& item : triplet_data) {
        const auto& triplet = item.first;

        // Safety checks before accessing distance_map
        pair<int, int> key1 = make_pair(get<0>(triplet), get<1>(triplet));
        pair<int, int> key2 = make_pair(get<0>(triplet), get<2>(triplet));
        pair<int, int> key3 = make_pair(get<1>(triplet), get<2>(triplet));

        if (distance_map.find(key1) == distance_map.end() ||
            distance_map.find(key2) == distance_map.end() ||
            distance_map.find(key3) == distance_map.end()) {
            //cout << "Key not found in distance_map for triplet: (" << get<0>(triplet) << ", " << get<1>(triplet) << ", " << get<2>(triplet) << ")" << endl;
            continue;  // Skip this triplet if any key is missing
        }

        const auto& distances = get<0>(item.second);
        const auto& angles = get<1>(item.second);

        double energy = 0.0;
        if (selected_potential == "Stillinger-Weber") {
            array<double, 3> angle_array = {get<0>(angles), get<1>(angles), get<2>(angles)};
            energy = f3(distances, angle_array);
        } else if (selected_potential == "Axilrod-Teller") {
            energy = axilrod_teller_potential(distances);
        } else {
            cerr << "Warning: Unknown potential " << selected_potential << "." << endl;
            exit(1); // or handle this differently
        }

        triplet_energies[triplet] = energy;
        total_energy += energy;


        // Update atom_triplets map for each atom in the triplet
        for (int index : {get<0>(triplet), get<1>(triplet), get<2>(triplet)}) {
            atom_triplets[index].push_back(triplet);
        }
    }

    //cout << "[calculate_energies end] Atom Triplets Size: " << atom_triplets.size() << endl;

    return make_tuple(triplet_energies, total_energy);
}
