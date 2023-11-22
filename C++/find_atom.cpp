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


    for (const auto& [atom, triplets] : atom_triplets) {
        double energy_to_remove = 0.0;


        for (const auto& triplet : triplets) {
            double triplet_energy = triplet_energies[triplet];
            energy_to_remove += triplet_energy;

        }


        if (energy_to_remove > max_energy_diff) {
            max_energy_diff = energy_to_remove;
            most_contributing_atom = atom;
        }
    }

    return most_contributing_atom;
}

