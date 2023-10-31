def read_coordinates(file_path):
    """
    Reads a file and extracts atom coordinates.
    
    Parameters:
        file_path (str): The path to the file containing the coordinates.
        
    Returns:
        tuple: A tuple containing a list of tuples for coordinates and the dimension.
    """
    coordinates = []
    dimensions = 0  # Initialize dimensions to zero
    
    try:
        with open(file_path, 'r') as file:
            # Check for optional header
            first_line = file.readline().strip()
            if first_line.startswith("#"):
                num_atoms, dimensions = map(int, first_line[1:].split())
                print(f"Header found: {num_atoms} atoms, {dimensions} dimensions")
            
            # If no header, reset file pointer
            else:
                file.seek(0)
                dimensions = len(file.readline().strip().split())  # Determine dimensions from first data line
                file.seek(0)  # Reset file pointer again
            
            # Read and parse each line for coordinates
            for line in file:
                coords = tuple(map(float, line.strip().split()))
                if len(coords) != dimensions:
                    print("Warning: Mismatch in dimensions and number of coordinates in a line.")
                    continue
                
                coordinates.append(coords)
                
        return coordinates, dimensions
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None

# Example usage:
if __name__ == "__main__":
    file_path_3D = "WFG3_03D.pof"  # Replace with your file path
    file_path_2D = "WFG3_02D.pof"  # Replace with your file path
    
    coordinates_3D, dimensions_3D = read_coordinates(file_path_3D)
    coordinates_2D, dimensions_2D = read_coordinates(file_path_2D)
    
    print("First 10 coordinates from 3D file:", coordinates_3D[:10])
    print("Dimensions of 3D file:", dimensions_3D)
    
    print("First 10 coordinates from 2D file:", coordinates_2D[:10])
    print("Dimensions of 2D file:", dimensions_2D)


