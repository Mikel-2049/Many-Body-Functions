import numpy as np

def calculate_distances(r1, r2, dimensionality):
    r1_array = np.array(r1[:dimensionality])
    r2_array = np.array(r2[:dimensionality])
    return np.linalg.norm(r1_array - r2_array)

def calculate_all_distances(atom_coordinates, dimensionality):
    distance_map = {}
    number_of_points = len(atom_coordinates)
    for i in range(number_of_points):
        for j in range(i + 1, number_of_points):
            dist = calculate_distances(atom_coordinates[i], atom_coordinates[j], dimensionality)
            distance_map[(i, j)] = dist
            distance_map[(j, i)] = dist
    return distance_map
