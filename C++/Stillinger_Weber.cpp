#include <cmath>
#include <array>
using namespace std;

// Constants
const double a = 1.80;
const double lambda_ = 21.0;
const double alpha = 3.4723e-12;
const double gamma = 1.20;

// Function h
double h(double r1, double r2, double theta) {
    if (r1 < a && r2 < a) {
        double cos_term = cos(theta) + 1.0 / 3.0;
        double exp_term = exp(gamma * (1.0 / (r1 - a) + 1.0 / (r2 - a)));
        return lambda_ * exp_term * pow(cos_term, 2);
    } else {
        return 0.0;
    }
}

// Function f3
double f3(const array<double, 3>& distances, const array<double, 3>& angles) {
    double rij = distances[0], rik = distances[1], rjk = distances[2];
    double theta_jik = angles[0], theta_ijk = angles[1], theta_ikj = angles[2];

    double h1 = h(rij, rik, theta_jik);
    double h2 = h(rij, rjk, theta_ijk);
    double h3 = h(rik, rjk, theta_ikj);

    return h1 + h2 + h3;
}
