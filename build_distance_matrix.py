import numpy as np

def build_distance_matrix(coordinates, dimensions):
    """
    Builds an n-dimensional distance matrix based on the coordinates and dimensions.
    
    Parameters:
        coordinates (list): List of tuples containing coordinates.
        dimensions (int): Number of dimensions (2, 3, 4, etc.).
        
    Returns:
        ndarray: An n-dimensional Numpy array containing distances.
    """
    num_atoms = len(coordinates)
    shape = [num_atoms] * dimensions  # Create shape dynamically based on dimensions
    distance_matrix = np.zeros(shape)
    
    # Your distance computation logic here
    
    return distance_matrix

# Example usage:
coordinates_3D = [(0, 0, 0), (1, 1, 1), (2, 2, 2)]
dimensions_3D = 3
matrix_3D = build_distance_matrix(coordinates_3D, dimensions_3D)

coordinates_2D = [(0, 0), (1, 1), (2, 2)]
dimensions_2D = 2
matrix_2D = build_distance_matrix(coordinates_2D, dimensions_2D)

print("3D Matrix shape:", matrix_3D)
print("2D Matrix shape:", matrix_2D.shape)
