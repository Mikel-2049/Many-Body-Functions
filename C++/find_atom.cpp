#include <map>
#include <vector>
#include <tuple>
#include <limits>  // For numeric_limits
#include <iostream>
using namespace std;

// Triplet_energies and atom_triplets are defined in main.cpp
extern map<tuple<int, int, int>, double> triplet_energies;
extern map<int, vector<tuple<int, int, int>>> atom_triplets;

int find_most_contributing_atom(double& max_energy_diff) {
    max_energy_diff = -numeric_limits<double>::infinity();
    int most_contributing_atom = -1;

    // Debug: Check if entering the loop
    cout << "Entering loop. Size of atom_triplets: " << atom_triplets.size() << endl;

    for (const auto& [atom, triplets] : atom_triplets) {
        double energy_to_remove = 0.0;

        // Debug: Check the triplets for each atom
        cout << "Atom " << atom << " is part of " << triplets.size() << " triplets." << endl;

        for (const auto& triplet : triplets) {
            double triplet_energy = triplet_energies[triplet];
            energy_to_remove += triplet_energy;

            // Debug: Print each triplet's energy contribution
            cout << "    Triplet: (" << get<0>(triplet) << ", " << get<1>(triplet) << ", " << get<2>(triplet) 
                 << "), Energy: " << triplet_energy << endl;
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

