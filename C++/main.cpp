#include <iostream>
#include <tuple>
#include <vector>
#include <map>
#include <set>
#include <cmath>
#include <algorithm>
#include <array> 
#include <fstream>


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

// Forward declaration for atom_triplets
map<int, vector<tuple<int, int, int>>> atom_triplets;

// Forward declaration for triplet energies
map<tuple<int, int, int>, double> triplet_energies;

// Forward declaration for calculating and storing energies
tuple<map<tuple<int, int, int>, double>, double> calculate_and_store_energies(
    const map<tuple<int, int, int>, tuple<array<double, 3>, tuple<double, double, double>>>& triplet_data, 
    const vector<vector<float>>& atoms, 
    const map<vector<float>, int>& coord_to_index, 
    const string& selected_potential,
    map<int, vector<tuple<int, int, int>>>& atom_triplets);

void update_atom_triplets(map<int, vector<tuple<int, int, int>>>& atom_triplets, int atom_to_remove);

void update_triplet_energies(map<tuple<int, int, int>, double>& triplet_energies, const vector<tuple<int, int, int>>& triplets_to_remove);

void update_atoms_and_coord_to_index(vector<vector<float>>& atoms, map<vector<float>, int>& coord_to_index, int atom_to_remove);


int find_most_contributing_atom(const map<int, vector<tuple<int, int, int>>>& atom_triplets, 
                                const map<tuple<int, int, int>, double>& triplet_energies) {
    double max_energy_diff = -numeric_limits<double>::infinity();
    int most_contributing_atom = -1;

    // Iterate over each atom and its associated triplets
    for (const auto& [atom, triplets] : atom_triplets) {
        double total_energy_for_atom = 0.0;

        // Sum the energies of all triplets that the atom is part of
        for (const auto& triplet : triplets) {
            total_energy_for_atom += triplet_energies.at(triplet);
        }

        // Update if this atom contributes more energy than the current max
        if (total_energy_for_atom > max_energy_diff) {
            max_energy_diff = total_energy_for_atom;
            most_contributing_atom = atom;
            //cout << "    Updated most contributing atom to: " << atom << ", Total Energy: " << max_energy_diff << endl;
        }
    }

    //cout << "Most contributing atom after loop: " << most_contributing_atom << endl;
    return most_contributing_atom;
}

void save_atoms_to_pof(const vector<vector<float>>& atoms, const string& filename) {
    ofstream outfile(filename);
    if (outfile.is_open()) {
        for (const auto& atom : atoms) {
            // Assuming each atom's data is a vector of floats (e.g., x, y, z coordinates)
            for (const auto& coord : atom) {
                outfile << coord << " ";
            }
            outfile << endl;
        }
        outfile.close();
    } else {
        cerr << "Unable to open file " << filename << endl;
    }
}




int main() {


    double total_energy;

    string file_path = "test_geometries/Sampled/VIE1_03D_sampled.pof"; 

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

    map<int, vector<tuple<int, int, int>>> atom_triplets;

    vector<int> milestones = {100, 75, 50, 25};
    set<int> milestones_set(milestones.begin(), milestones.end());

    while (atoms.size() > 24) {
        auto [current_triplet_energies, current_total_energy] = calculate_and_store_energies(
            triplet_data, atoms, coord_to_index, selected_potential, atom_triplets);

        double max_energy_diff;

        // Now use the updated global atom_triplets directly
        int most_contributing_atom = find_most_contributing_atom(atom_triplets, current_triplet_energies);

        //cout << "Most contributing atom: " << most_contributing_atom << endl;

        //cout << "Number of atoms before removing: " << atoms.size() << endl;
        // After finding the most contributing atom

        //cout << "Size of atom_triplets: " << atom_triplets.size() << endl;
        //for (const auto& pair : atom_triplets) {
            //cout << "Atomxd: " << pair.first << ", Number of Triplets: " << pair.second.size() << endl;
        //}

        vector<tuple<int, int, int>> triplets_to_remove = atom_triplets[most_contributing_atom];
        //cout << "Number of triplets to remove: " << triplets_to_remove.size() << endl;

        // Update the data structures
        update_atom_triplets(atom_triplets, most_contributing_atom);
        update_triplet_energies(current_triplet_energies, atom_triplets[most_contributing_atom]);
        update_atoms_and_coord_to_index(atoms, coord_to_index, most_contributing_atom);

        // Assign updated structures back to global variables
        triplet_energies = current_triplet_energies;
        total_energy = current_total_energy;

        cout << "Atoms: " << atoms.size() << endl;

        // Check if the current atom count is a milestone and save to a .pof file
        if (milestones_set.find(atoms.size()) != milestones_set.end()) {
            string filename = "output_at_" + to_string(atoms.size()) + "_atoms.pof";
            save_atoms_to_pof(atoms, filename);
        }
    }


    return 0;
}
