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
tuple<map<tuple<int, int, int>, double>, map<int, vector<tuple<int, int, int>>>, double> calculate_and_store_energies(
    const map<tuple<int, int, int>, tuple<array<double, 3>, tuple<double, double, double>>>& triplet_data, 
    const vector<vector<float>>& atoms, 
    const map<vector<float>, int>& coord_to_index, 
    const string& selected_potential) {

    map<tuple<int, int, int>, double> triplet_energies;
    map<int, vector<tuple<int, int, int>>> atom_triplets;
    double total_energy = 0.0;

    for (const auto& item : triplet_data) {
        const auto& triplet = item.first;
        const auto& data = item.second;
        const auto& distances = get<0>(data);
        const auto& angles = get<1>(data);

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


        for (int index : {get<0>(triplet), get<1>(triplet), get<2>(triplet)}) {
            atom_triplets[index].push_back(triplet);
        }
    }
    
    cout << "Total_energy: " << total_energy << endl;

    return make_tuple(triplet_energies, atom_triplets, total_energy);
}
