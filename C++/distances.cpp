#include <cmath>
#include <vector>
#include <map>
#include <utility>

using namespace std;

double calculate_distance(const vector<float>& r1, const vector<float>& r2, int dimensionality) {
    double sum = 0.0;
    for (int i = 0; i < dimensionality; ++i) {
        sum += pow(r1[i] - r2[i], 2);
    }
    return sqrt(sum);
}

map<pair<int, int>, double> calculate_all_distances(const vector<vector<float>>& atom_coordinates, int dimensionality) {
    map<pair<int, int>, double> distance_map;
    int number_of_atoms = atom_coordinates.size();

    for (int i = 0; i < number_of_atoms; ++i) {
        for (int j = i + 1; j < number_of_atoms; ++j) {
            double dist = calculate_distance(atom_coordinates[i], atom_coordinates[j], dimensionality);
            distance_map[make_pair(i, j)] = dist;
            distance_map[make_pair(j, i)] = dist;  // Optional due to symmetric nature of distance
        }
    }

    return distance_map;
}
