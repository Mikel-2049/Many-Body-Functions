import numpy as np

# Given parameters
a = 1.80 + 4
lambda_ = 21.0
alpha = 3.4723e-12
gamma = 1.20 

# Generalized function to calculate h
def h(r1, r2, theta):
    if r1 < a and r2 < a:
        cos_term = np.cos(theta) + 1.0 / 3.0
        exp_term = np.exp(gamma * (1.0 / (r1 - a) + 1.0 / (r2 - a)))
        return lambda_ * exp_term * (cos_term ** 2)
    else:
        return 0

# Function to calculate f3(ri, rj, rk)
def f3(distances, angles):
    #print(f"Debug: distances = {distances}")
    rij, rik, rjk = distances
    theta_jik, theta_ijk, theta_ikj = angles
    
    h1 = h(rij, rik, theta_jik)
    h2 = h(rij, rjk, theta_ijk)
    h3 = h(rik, rjk, theta_ikj)

    return h1 + h2 + h3


