from typing import Tuple, List

def read_pof_file(file_path: str) -> Tuple[int, List[List[float]], dict[Tuple[float], int]]:
    atoms = []
    coord_to_index = {}  # Create a mapping from coordinates to index
    index = 0
    with open(file_path, 'r') as f:
        # Read the first line to get the dimensionality
        first_line = f.readline().strip()
        dimensionality = int(first_line.split()[-1])
        
        # Read the remaining lines to get the data points
        for line in f:
            coords = tuple(map(float, line.strip().split()))
            atoms.append(coords)
            coord_to_index[coords] = index  # Add the mapping from coordinates to index
            index += 1  # Increment the index
            
    return dimensionality, atoms, coord_to_index


# Example usage
#if __name__ == "__main__":
    file_path = "WFG3_03D.pof"
    dimensionality, atoms = read_pof_file(file_path)
    print(f"Dimensionality: {dimensionality}")
    print(f"Number of atoms: {len(atoms)}")
    print(f"First 5 atoms: {atoms[:5]}")
