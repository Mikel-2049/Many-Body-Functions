import numpy as np

def calculate_angle(rij, rik, rjk):
    cos_theta = (rij**2 + rik**2 - rjk**2) / (2 * rij * rik)
    cos_theta = np.clip(cos_theta, -1.0, 1.0)
    return np.arccos(cos_theta)

def calculate_angles_for_triplet(triplet, distance_map):
    i, j, k = triplet
    rij = distance_map[(i, j)]
    rik = distance_map[(i, k)]
    rjk = distance_map[(j, k)]
    
    theta_jik = calculate_angle(rij, rik, rjk)
    theta_ijk = calculate_angle(rij, rjk, rik)  # Note the order of distances
    theta_ikj = calculate_angle(rik, rjk, rij)  # Note the order of distances
    
    return theta_jik, theta_ijk, theta_ikj  # Return all three angles for the triplet
