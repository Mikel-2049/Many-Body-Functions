#include <iostream>
#include <tuple>
#include <vector>
#include <map>

using namespace std;

// Forward declare the read_pof_file function
tuple<int, vector<vector<float>>, map<vector<float>, int>> read_pof_file(const string& file_path);

int main() {
    string file_path = "geometries/DTLZ7_03D_350.pof"; 

    // Call the read_pof_file function
    auto [dimensionality, atoms, coord_to_index] = read_pof_file(file_path);

    // Print the dimensionality and number of points
    cout << "Dimensionality: " << dimensionality << endl;
    cout << "Number of points: " << atoms.size() << endl;


    cout << "Dimensionality: " << dimensionality << endl;
    cout << "Atoms:" << endl;
    for (const auto& atom : atoms) {
        for (float coord : atom) {
            cout << coord << " ";
        }
        cout << endl;
    }
    cout << "Coordinate to Index Mapping:" << endl;
    for (const auto& pair : coord_to_index) {
        const auto& coords = pair.first;
        cout << "(";
        for (float coord : coords) {
            cout << coord << ",";
        }
        cout << ") -> " << pair.second << endl;
    }

    return 0;
}
