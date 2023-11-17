#include <cmath>  // For std::sqrt and std::pow
#include <vector>

using namespace std;

double calculate_distances(const vector<float>& r1, const vector<float>& r2, int dimensionality) {
    double sum = 0.0;
    for (int i = 0; i < dimensionality; ++i) {
        sum += pow(r1[i] - r2[i], 2);
    }
    return sqrt(sum);
}

#include <map>
#include <utility>  // For std::pair

map<pair<int, int>, double> calculate_all_distances(const vector<vector<float>>& atom_coordinates, int dimensionality) {
    map<pair<int, int>, double> distance_map;
    int number_of_points = atom_coordinates.size();
    for (int i = 0; i < number_of_points; ++i) {
        for (int j = i + 1; j < number_of_points; ++j) {
            double dist = calculate_distances(atom_coordinates[i], atom_coordinates[j], dimensionality);
            distance_map[make_pair(i, j)] = dist;
            distance_map[make_pair(j, i)] = dist;
        }
    }
    return distance_map;
}
