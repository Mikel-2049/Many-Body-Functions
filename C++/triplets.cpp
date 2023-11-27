#include <vector>
#include <set>
#include <tuple>

using namespace std;

set<tuple<int, int, int>> find_unique_triplets(const vector<vector<float>>& atoms) {
    int number_of_atoms = atoms.size();
    set<tuple<int, int, int>> found_triplets;

    for (int i = 0; i < number_of_atoms; ++i) {
        for (int j = i + 1; j < number_of_atoms; ++j) {
            for (int k = j + 1; k < number_of_atoms; ++k) {
                found_triplets.insert(make_tuple(i, j, k));
            }
        }
    }

    return found_triplets;
}
