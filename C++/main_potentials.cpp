#include <vector>
#include <set>
#include <map>
#include <tuple>
#include <cmath>  // For std::sqrt, std::pow, std::acos
#include <algorithm>  // For std::max, std::min
#include <fstream>
#include <iostream>

using namespace std;

// Forward Declarations
tuple<int, vector<vector<float>>> read_pof_file(const string& file_path);
map<pair<int, int>, double> calculate_all_distances(const vector<vector<float>>& atoms);
set<tuple<int, int, int>> find_unique_triplets(const vector<vector<float>>& atoms);
double calculate_angle(double rij, double rik, double rjk);
tuple<double, double, double> calculate_angles_for_triplet(const tuple<int, int, int>& triplet, const map<pair<int, int>, double>& distance_map);

int main() {
    // Step 1: Read file
    string file_path = "path/to/your/pof_file.pof";  // Update with your actual file path
    auto [dimensionality, atoms] = read_pof_file(file_path);

    // Step 2: Calculate all distances
    auto distance_map = calculate_all_distances(atoms);

    // Step 3: Create all triplets
    auto triplets = find_unique_triplets(atoms);

    // Step 4: Iterate through all triplets and find the angles
    map<tuple<int, int, int>, tuple<double, double, double>> angle_map;
    for (const auto& triplet : triplets) {
        auto angles = calculate_angles_for_triplet(triplet, distance_map);
        angle_map[triplet] = angles;
    }

    return 0;
}

