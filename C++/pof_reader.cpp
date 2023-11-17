#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <map>
#include <tuple>

using namespace std;

tuple<int, vector<vector<float>>, map<vector<float>, int>> read_pof_file(const string& file_path) {
    vector<vector<float>> atoms;
    map<vector<float>, int> coord_to_index;
    int index = 0;
    int dimensionality;
    int num_points; // To store the number of points, though not used directly
    ifstream file(file_path);

    if (!file.is_open()) {
        cerr << "Error opening file" << endl;
        exit(1); // or handle the error as appropriate
    }

    string line;
    getline(file, line);
    stringstream first_line(line);

    char hash; // To consume the '#' character
    first_line >> hash >> num_points >> dimensionality;

    while (getline(file, line)) {
        stringstream ss(line);
        vector<float> coords(dimensionality);
        for (int i = 0; i < dimensionality; ++i) {
            ss >> coords[i];
        }
        atoms.push_back(coords);
        coord_to_index[coords] = index;
        index++;
    }

    cout << "Dimensionality read: " << dimensionality << endl;
    cout << "Number of points read: " << atoms.size() << endl;

    file.close();
    return make_tuple(dimensionality, atoms, coord_to_index);
}
