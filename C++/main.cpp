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
    map<pair<int, int>, double>& distance_map,
    map<int, vector<tuple<int, int, int>>>& atom_triplets);


void update_atom_triplets(map<int, vector<tuple<int, int, int>>>& atom_triplets, int atom_to_remove);

void update_triplet_energies(map<tuple<int, int, int>, double>& triplet_energies, const vector<tuple<int, int, int>>& triplets_to_remove);

void update_atoms_and_coord_to_index(vector<vector<float>>& atoms, map<vector<float>, int>& coord_to_index, int atom_to_remove);

void update_distance_map(map<pair<int, int>, double>& distance_map, int atom_to_remove);


int find_most_contributing_atom(const map<int, vector<tuple<int, int, int>>>& atom_triplets, 
                                const map<tuple<int, int, int>, double>& triplet_energies) {
    double max_energy_diff = -numeric_limits<double>::infinity();
    int most_contributing_atom = -1;

    for (const auto& [atom, triplets] : atom_triplets) {
        double total_energy_for_atom = 0.0;

        for (const auto& triplet : triplets) {
            if (triplet_energies.find(triplet) == triplet_energies.end()) {
                cout << "Triplet not found in triplet_energies: (" 
                     << get<0>(triplet) << ", " << get<1>(triplet) << ", " << get<2>(triplet) << ")" << endl;
            } else {
                total_energy_for_atom += triplet_energies.at(triplet);
            }
        }

        if (total_energy_for_atom > max_energy_diff) {
            max_energy_diff = total_energy_for_atom;
            most_contributing_atom = atom;
        }
    }

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
        pair<int, int> key1 = make_pair(get<0>(triplet), get<1>(triplet));
        pair<int, int> key2 = make_pair(get<0>(triplet), get<2>(triplet));
        pair<int, int> key3 = make_pair(get<1>(triplet), get<2>(triplet));

        if (distance_map.find(key1) != distance_map.end() &&
            distance_map.find(key2) != distance_map.end() &&
            distance_map.find(key3) != distance_map.end()) {
            // Safe to access distance_map
            array<double, 3> distances = {distance_map.at(key1), distance_map.at(key2), distance_map.at(key3)};
            auto angles = calculate_angles_for_triplet(triplet, distance_map);
            triplet_data[triplet] = make_tuple(distances, angles);
        }
    }


    string selected_potential = select_potential();

    map<int, vector<tuple<int, int, int>>> atom_triplets;

    vector<int> milestones = {100, 75, 50, 25};
    set<int> milestones_set(milestones.begin(), milestones.end());

    // Place this just before the while loop starts in main
    cout << "[Main] Initial Atom Triplets Size: " << atom_triplets.size() << endl;

    while (atoms.size() > 24) {

        //cout << "\n[Start of Cycle Debugging]" << endl;
        //cout << "Atoms Size: " << atoms.size() << endl;
        //cout << "Coord to Index Size: " << coord_to_index.size() << endl;
        //cout << "Atom Triplets Size: " << atom_triplets.size() << endl;
        //cout << "Distance Map Size: " << distance_map.size() << endl;
        //cout << "Triplet Data Size: " << triplet_data.size() << endl;
        //cout << "Triplet Energies Size: " << triplet_energies.size() << endl;


        // Place this at the beginning of the while loop
        //cout << "[Main Loop Start] Atom Triplets Size: " << atom_triplets.size() << endl;

        // Place these around the calculate_and_store_energies call in main
        //cout << "[Before calculate_and_store_energies] Atom Triplets Size: " << atom_triplets.size() << endl;

        auto [current_triplet_energies, current_total_energy] = calculate_and_store_energies(
            triplet_data, atoms, coord_to_index, selected_potential, distance_map, atom_triplets);

        //cout << "[After calculate_and_store_energies] Atom Triplets Size: " << atom_triplets.size() << endl;

        //cout << "[After calculate_and_store_energies] Triplet Energies Size: " << triplet_energies.size() << endl;


        double max_energy_diff;

        // Now use the updated global atom_triplets directly
        int most_contributing_atom = find_most_contributing_atom(atom_triplets, current_triplet_energies);

        vector<tuple<int, int, int>> triplets_to_remove = atom_triplets[most_contributing_atom];

        // Update the data structures
        //cout << "[Main Loop before first function call] Atom Triplets Size: " << atom_triplets.size() << endl;
        update_atom_triplets(atom_triplets, most_contributing_atom);
        //cout << "[Main Loop after first function call] Atom Triplets Size: " << atom_triplets.size() << endl;

        // Debug: Log the triplets to be removed
        //cout << "[triplets_to_remove] Size: " << triplets_to_remove.size() << endl;


        update_triplet_energies(current_triplet_energies, triplets_to_remove);
        //cout << "[Main Loop after second function call] Atom Triplets Size: " << atom_triplets.size() << endl;


        update_atoms_and_coord_to_index(atoms, coord_to_index, most_contributing_atom);
        //cout << "[Main Loop after third function call] Atom Triplets Size: " << atom_triplets.size() << endl;

        // Update distance_map
        update_distance_map(distance_map, most_contributing_atom);

        for (auto it = triplet_data.begin(); it != triplet_data.end(); ) {
            const auto& triplet = it->first;
            if (get<0>(triplet) == most_contributing_atom || get<1>(triplet) == most_contributing_atom || get<2>(triplet) == most_contributing_atom) {
                it = triplet_data.erase(it); // Remove triplets involving the removed atom
            } else {
                ++it;
            }
        }

        // Assign updated structures back to global variables
        triplet_energies = current_triplet_energies;
        total_energy = current_total_energy;

        cout << "Atoms: " << atoms.size() << endl;

        // Place this at the ending of the while loop
        cout << "[Main Loop Ends] Atom Triplets Size: " << atom_triplets.size() << endl;


        // Add debug statements at the end of each cycle
            //cout << "\n[End of Cycle Debugging]" << endl;
            //cout << "Atoms Size: " << atoms.size() << endl;
            //cout << "Coord to Index Size: " << coord_to_index.size() << endl;
            //cout << "Atom Triplets Size: " << atom_triplets.size() << endl;
            //cout << "Distance Map Size: " << distance_map.size() << endl;
            //cout << "Triplet Data Size: " << triplet_data.size() << endl;
            //cout << "Triplet Energies Size: " << triplet_energies.size() << endl;

            // Iterate through each atom_triplet pair and print the size of each vector
            //for (const auto& pair : atom_triplets) {
                //cout << "Atom " << pair.first << " - Number of Triplets: " << pair.second.size() << endl;
            //}

        // Check if the current atom count is a milestone and save to a .pof file
        if (milestones_set.find(atoms.size()) != milestones_set.end()) {
            string filename = "output_at_" + to_string(atoms.size()) + "_atoms.pof";
            save_atoms_to_pof(atoms, filename);
        }
    }


    return 0;
}
