#include <vector>
#include <set>
#include <algorithm>  // For std::sort
using namespace std;

set<tuple<int, int, int>> find_unique_triplets(int number_of_atoms) {
    set<tuple<int, int, int>> found_triplets;
    for (int i = 0; i < number_of_atoms; ++i) {
        for (int j = i + 1; j < number_of_atoms; ++j) {
            for (int k = j + 1; k < number_of_atoms; ++k) {
                // Create a triplet and add it to the set
                vector<int> triplet = {i, j, k};
                sort(triplet.begin(), triplet.end());  // Ensure the triplet is sorted
                found_triplets.insert(make_tuple(triplet[0], triplet[1], triplet[2]));
            }
        }
    }
    return found_triplets;
}
