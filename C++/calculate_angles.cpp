#include <cmath>  // For std::acos
#include <algorithm>  // For std::min and std::max
#include <iostream>
#include <tuple>
#include <vector>
#include <map>
#include <set>
using namespace std;

double calculate_angle(double rij, double rik, double rjk) {
    // Clip cos_theta to the range [-1, 1]
    double cos_theta = (pow(rij, 2) + pow(rik, 2) - pow(rjk, 2)) / (2.0 * rij * rik);
    cos_theta = max(-1.0, min(cos_theta, 1.0));
    return acos(cos_theta);
}

tuple<double, double, double> calculate_angles_for_triplet(const tuple<int, int, int>& triplet, const map<pair<int, int>, double>& distance_map) {
    auto [i, j, k] = triplet;

    double rij = distance_map.at(make_pair(i, j));
    double rik = distance_map.at(make_pair(i, k));
    double rjk = distance_map.at(make_pair(j, k));

    double theta_jik = calculate_angle(rij, rik, rjk);
    double theta_ijk = calculate_angle(rij, rjk, rik);  // Note the order of distances
    double theta_ikj = calculate_angle(rik, rjk, rij);  // Note the order of distances

    return make_tuple(theta_jik, theta_ijk, theta_ikj);
}
