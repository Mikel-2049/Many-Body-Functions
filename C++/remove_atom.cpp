#include <iostream>
#include <vector>
#include <map>
#include <tuple>
#include <set>
#include <algorithm>

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


void update_triplet_energies(map<tuple<int, int, int>, double>& triplet_energies, const vector<tuple<int, int, int>>& triplets_to_remove) {
    for (const auto& triplet : triplets_to_remove) {
        triplet_energies.erase(triplet);
    }
}

void update_atoms_and_coord_to_index(vector<vector<float>>& atoms, map<vector<float>, int>& coord_to_index, int atom_to_remove) {
    //cout << "Atoms Before: " << atoms.size() << endl;
    //cout << "Coord to Index Before: " << coord_to_index.size() << endl;

    //cout << "[Before Removal] Atoms Size: " << atoms.size() << ", Coord to Index Size: " << coord_to_index.size() << endl;

    
    if (atom_to_remove < atoms.size()) {
        atoms.erase(atoms.begin() + atom_to_remove);
    }
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

    //cout << "[After Removal] Atoms Size: " << atoms.size() << ", Coord to Index Size: " << coord_to_index.size() << ", Removed Atom Index: " << atom_to_remove << endl;

    //cout << "Atoms After: " << atoms.size() << endl;
    //cout << "Coord to Index After: " << coord_to_index.size() << endl;
}

void update_distance_map(map<pair<int, int>, double>& distance_map, int atom_to_remove) {
    for (auto it = distance_map.begin(); it != distance_map.end(); ) {
        const auto& atom_pair = it->first;
        if (atom_pair.first == atom_to_remove || atom_pair.second == atom_to_remove) {
            it = distance_map.erase(it); // Remove distances involving the removed atom
        } else {
            ++it;
        }
    }
}
