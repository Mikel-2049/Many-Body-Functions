import numpy as np

def calculate_distances(r1, r2, dimensionality):
    r1_array = np.array(r1[:dimensionality])
    r2_array = np.array(r2[:dimensionality])
    return np.linalg.norm(r1_array - r2_array)

def calculate_angle(r1, r2, r3, dimensionality):
    r12 = np.array(r1[:dimensionality]) - np.array(r2[:dimensionality])
    r13 = np.array(r1[:dimensionality]) - np.array(r3[:dimensionality])
    cos_theta = np.dot(r12, r13) / (np.linalg.norm(r12) * np.linalg.norm(r13))
    cos_theta = np.clip(cos_theta, -1.0, 1.0)
    return np.arccos(cos_theta)

def calculate_distances_and_angles(atom_coordinates, unique_triplets, dimensionality):
    result = {}
    for triplet in unique_triplets:
        ri, rj, rk = triplet  # Now these are coordinates directly
        
        # Calculate distances
        rij = calculate_distances(ri, rj, dimensionality)
        rik = calculate_distances(ri, rk, dimensionality)
        rjk = calculate_distances(rj, rk, dimensionality)
        
        # Calculate angles
        theta_jik = calculate_angle(ri, rj, rk, dimensionality)
        theta_ijk = calculate_angle(rj, ri, rk, dimensionality)
        theta_ikj = calculate_angle(rk, ri, rj, dimensionality)
        
        result[triplet] = {'distances': (rij, rik, rjk), 'angles': (theta_jik, theta_ijk, theta_ikj)}
    return result

'''
def calculate_distances_and_angles(atom_coordinates, unique_triplets, dimensionality):
    result = {}
    for triplet in unique_triplets:
        i, j, k = triplet

        ri = np.array(atom_coordinates[i][:dimensionality])
        rj = np.array(atom_coordinates[j][:dimensionality])
        rk = np.array(atom_coordinates[k][:dimensionality])
        
        rij = calculate_distances(ri, rj, dimensionality)
        rik = calculate_distances(ri, rk, dimensionality)
        rjk = calculate_distances(rj, rk, dimensionality)

        theta_jik = calculate_angle(ri, rj, rk, dimensionality)
        theta_ijk = calculate_angle(rj, ri, rk, dimensionality)
        theta_ikj = calculate_angle(rk, ri, rj, dimensionality)
        
        result[triplet] = ((rij, rik, rjk), (theta_jik, theta_ijk, theta_ikj))
    return result
'''

