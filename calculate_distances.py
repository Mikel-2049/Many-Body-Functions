import numpy as np

def calculate_angle(r1, r2, r3):
    r12 = r2 - r1
    r13 = r3 - r1
    cos_theta = np.dot(r12, r13) / (np.linalg.norm(r12) * np.linalg.norm(r13))
    return np.arccos(cos_theta)

def calculate_distances_and_angles(atom_coordinates, unique_triplets):
    result = {}
    for triplet in unique_triplets:
        i, j, k = triplet
        ri, rj, rk = atom_coordinates[i], atom_coordinates[j], atom_coordinates[k]

        # Calculate distances
        rij = np.linalg.norm(ri - rj)
        rik = np.linalg.norm(ri - rk)
        rjk = np.linalg.norm(rj - rk)
        
        # Calculate angles
        theta_jik = calculate_angle(ri, rj, rk)
        theta_ijk = calculate_angle(rj, ri, rk)
        theta_ikj = calculate_angle(rk, ri, rj)
        
        result[triplet] = {'distances': (rij, rik, rjk), 'angles': (theta_jik, theta_ijk, theta_ikj)}
    return result
