#include <iostream>
#include <tuple>
#include <vector>
#include <map>
#include <set>
#include <cmath>
#include <algorithm>
#include <array> 

using namespace std;

// Forward declare the read_pof_file function
tuple<int, vector<vector<float>>, map<vector<float>, int>> read_pof_file(const string& file_path);

// Forward declare the calculate_distances function
map<pair<int, int>, double> calculate_all_distances(const vector<vector<float>>& atom_coordinates, int dimensionality);

// Forward declaration for find_unique_triplets
set<tuple<int, int, int>> find_unique_triplets(int number_of_atoms);

//Forward declaration for calculate_angles_for_triplets
tuple<double, double, double> calculate_angles_for_triplet(const tuple<int, int, int>& triplet, const map<pair<int, int>, double>& distance_map);

// Forward declaration for selecting the potential
string select_potential();

// Forward declaration for find_most_contributing_atom
int find_most_contributing_atom(double& max_energy_diff);

// Forward declaration for triplet energies
map<tuple<int, int, int>, double> triplet_energies;

// Forward declaration for atom_triplets
map<int, vector<tuple<int, int, int>>> atom_triplets;

// Forward declaration for calculating and storing energies
tuple<map<tuple<int, int, int>, double>, 
           map<int, vector<tuple<int, int, int>>>, 
           double> calculate_and_store_energies(
               const map<tuple<int, int, int>, 
               tuple<array<double, 3>, tuple<double, double, double>>>& triplet_data, 
               const vector<vector<float>>& atoms, 
               const map<vector<float>, int>& coord_to_index, 
               const string& selected_potential);


int find_most_contributing_atom(double& max_energy_diff, map<int, vector<tuple<int, int, int>>>& atom_triplets) {
    max_energy_diff = -numeric_limits<double>::infinity();
    int most_contributing_atom = -1;

    // Debug: Check if entering the loop
    cout << "Entering loop. Size of atom_triplets: " << atom_triplets.size() << endl;

    //for(int i=0; i < atom_triplets.size() ; i++) {
    //for (const auto& [atom, triplets] : atom_triplets) {
    for (const auto& atom_triplet : atom_triplets) {

        int atom = atom_triplet.first;
        vector<tuple<int, int, int>> triplets = atom_triplet.second;

        double energy_to_remove = 0.0;


        // Debug: Check the triplets for each atom
        // cout << "Atom " << atom << " is part of " << triplets.size() << " triplets." << endl;

        for (const auto& triplet : triplets) {
            double triplet_energy = triplet_energies[triplet];
            energy_to_remove += triplet_energy;

            // Debug: Print each triplet's energy contribution
            //cout << "    Triplet: (" << get<0>(triplet) << ", " << get<1>(triplet) << ", " << get<2>(triplet) 
            //     << "), Energy: " << triplet_energy << endl;
        }

        cout << "Atom: " << atom << ", Total Energy to Remove: " << energy_to_remove << endl;

        if (energy_to_remove > max_energy_diff) {
            max_energy_diff = energy_to_remove;
            most_contributing_atom = atom;
            cout << "    Updated most contributing atom to: " << atom << ", Max Energy Diff: " << max_energy_diff << endl;
        }
    }

    cout << "Most contributing atom after loop: " << most_contributing_atom << endl;
    return most_contributing_atom;
}


int main() {
    string file_path = "geometries/DTLZ7_03D_350.pof"; 

    // Call the read_pof_file function
    auto [dimensionality, atoms, coord_to_index] = read_pof_file(file_path);

    // Call calculate_all_distances
    auto distance_map = calculate_all_distances(atoms, dimensionality);

    // Calculate the number of atoms
    int number_of_atoms = atoms.size();

    // Find unique triplets
    auto found_triplets = find_unique_triplets(number_of_atoms);

    //Declaration for triplet_data
    map<tuple<int, int, int>, tuple<array<double, 3>, tuple<double, double, double>>> triplet_data;

    for (const auto& triplet : found_triplets) {
        array<double, 3> distances = {
            distance_map.at(make_pair(get<0>(triplet), get<1>(triplet))),
            distance_map.at(make_pair(get<0>(triplet), get<2>(triplet))),
            distance_map.at(make_pair(get<1>(triplet), get<2>(triplet)))
        };

        auto angles = calculate_angles_for_triplet(triplet, distance_map);

        triplet_data[triplet] = make_tuple(distances, angles);
    }

    string selected_potential = select_potential();

    auto [triplet_energies, atom_triplets, total_energy] = calculate_and_store_energies(triplet_data, atoms, coord_to_index, selected_potential);

    cout << "Total Energy: " << total_energy <<endl;

    // Debugging print to check the size of atom_triplets
    cout << "Size of atom_triplets: " << atom_triplets.size() << endl;

    double max_energy_diff;

    int most_contributing_atom = find_most_contributing_atom(max_energy_diff, atom_triplets);

    cout << "Max Energy Difference: " << max_energy_diff << endl;
    cout << "Most contributing atom: " << most_contributing_atom << endl;


    return 0;
}
