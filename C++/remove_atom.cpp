#include <iostream>
#include <vector>
#include <map>
#include <tuple>
#include <set>

using namespace std;

void update_atom_triplets(map<int, vector<tuple<int, int, int>>>& atom_triplets, int atom_to_remove) {
    //cout << "Atom Triplets Before: " << atom_triplets.size() << endl;
    atom_triplets.erase(atom_to_remove);
    //cout << "Atom Triplets After: " << atom_triplets.size() << endl;
}

void update_triplet_energies(map<tuple<int, int, int>, double>& triplet_energies, const vector<tuple<int, int, int>>& triplets_to_remove) {
    //cout << "Triplets to Remove: " << triplets_to_remove.size() << endl;
    //cout << "Triplet Energies Before: " << triplet_energies.size() << endl;
    for (const auto& triplet : triplets_to_remove) {
        triplet_energies.erase(triplet);
    }
    //cout << "Triplet Energies After: " << triplet_energies.size() << endl;
}

void update_atoms_and_coord_to_index(vector<vector<float>>& atoms, map<vector<float>, int>& coord_to_index, int atom_to_remove) {
    //cout << "Atoms Before: " << atoms.size() << endl;
    //cout << "Coord to Index Before: " << coord_to_index.size() << endl;
    
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

    //cout << "Atoms After: " << atoms.size() << endl;
    //cout << "Coord to Index After: " << coord_to_index.size() << endl;
}
