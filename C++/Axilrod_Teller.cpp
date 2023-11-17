#include <cmath>  // For std::acos
#include <array>

using namespace std;

// Axilrod-Teller potential function
double axilrod_teller_potential(const array<double, 3>& distances, double nu = -4) {
    double rij = distances[0], rik = distances[1], rjk = distances[2];

    // Ensure non-zero distances to avoid division by zero
    rij = (rij != 0) ? rij : 1e-10;
    rik = (rik != 0) ? rik : 1e-10;
    rjk = (rjk != 0) ? rjk : 1e-10;

    // Axilrod-Teller potential formula
    // Since the unit vectors and dot products are not needed due to the distances being scalar magnitudes,
    // the formula simplifies greatly:
    double potential = nu / (pow(rij, 3) * pow(rik, 3) * pow(rjk, 3));
    return potential;
}
