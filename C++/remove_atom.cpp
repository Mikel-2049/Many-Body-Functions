#include <iostream>
#include <vector>
#include <map>
#include <tuple>
#include <set>
#include <algorithm>
#include <array>


using namespace std;

void update_atom_triplets(map<int, vector<tuple<int, int, int>>>& atom_triplets, int atom_to_remove) {
    // Remove the entry for the deleted atom
    atom_triplets.erase(atom_to_remove);

    // Iterate over all atoms and remove any triplets that include the deleted atom
    for (auto& [atom, triplets] : atom_triplets) {
        auto original_size = triplets.size();
        triplets.erase(
            remove_if(triplets.begin(), triplets.end(), 
                      [atom_to_remove](const tuple<int, int, int>& triplet) {
                          return get<0>(triplet) == atom_to_remove ||
                                 get<1>(triplet) == atom_to_remove ||
                                 get<2>(triplet) == atom_to_remove;
                      }), 
            triplets.end()
        );

        if (triplets.size() != original_size) {
            //cout << "Atom " << atom << ": Removed " << (original_size - triplets.size()) 
                 //<< " triplets involving atom " << atom_to_remove << endl;
        }
    }
}


void update_atoms_and_coord_to_index(vector<vector<float>>& atoms, 
                                     map<vector<float>, int>& coord_to_index, 
                                     map<int, vector<tuple<int, int, int>>>& atom_triplets,
                                     map<tuple<int, int, int>, double>& triplet_energies,
                                     map<tuple<int, int, int>, tuple<array<double, 3>, tuple<double, double, double>>>& triplet_data,
                                     int atom_to_remove) {
    
    atoms.erase(atoms.begin() + atom_to_remove);
    
    for (auto it = coord_to_index.begin(); it != coord_to_index.end(); ) {
        if (it->second == atom_to_remove) {
            it = coord_to_index.erase(it);
        } else {
            if (it->second > atom_to_remove) {
                it->second--;
            }
            ++it;
        }
    }
}


void update_distance_map(map<pair<int, int>, double>& distance_map, int atom_to_remove) {
    for (auto it = distance_map.begin(); it != distance_map.end(); ) {
        const auto& [atom1, atom2] = it->first;
        if (atom1 == atom_to_remove || atom2 == atom_to_remove) {
            it = distance_map.erase(it);
        } else {
            ++it;
        }
    }
}

void update_triplet_data(map<tuple<int, int, int>, tuple<array<double, 3>, tuple<double, double, double>>>& triplet_data, 
                         int atom_to_remove) {
    map<tuple<int, int, int>, tuple<array<double, 3>, tuple<double, double, double>>> updated_triplet_data;

    for (const auto& [triplet, data] : triplet_data) {
        auto [atom1, atom2, atom3] = triplet;

        if (atom1 == atom_to_remove || atom2 == atom_to_remove || atom3 == atom_to_remove) {
            continue;
        }

        if (atom1 > atom_to_remove) --atom1;
        if (atom2 > atom_to_remove) --atom2;
        if (atom3 > atom_to_remove) --atom3;

        updated_triplet_data.emplace(make_tuple(atom1, atom2, atom3), data);
    }

    triplet_data = std::move(updated_triplet_data);
}