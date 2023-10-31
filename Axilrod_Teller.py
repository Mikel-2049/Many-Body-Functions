import numpy as np

def axilrod_teller_potential(distances, nu=0.4):
    """
    Calculate the Axilrod-Teller potential using pre-calculated distances.
    
    Parameters:
    - distances: A dictionary containing the distances 'rij', 'rik', and 'rjk' between the atoms in the triplet.
    - nu: The nu parameter in the Axilrod-Teller formula.
    
    Returns:
    - The calculated Axilrod-Teller potential.
    """
    
    rij, rik, rjk = distances
    
    # Calculate magnitudes of the distances
    rij_mag = np.linalg.norm(rij)
    rik_mag = np.linalg.norm(rik)
    rjk_mag = np.linalg.norm(rjk)
    
    # Calculate unit vectors
    rij_hat = rij / rij_mag
    rik_hat = rik / rik_mag
    rjk_hat = rjk / rjk_mag
    
    # Axilrod-Teller potential formula
    dot_product_term = np.dot(rij_hat, rik_hat) * np.dot(-rij_hat, rjk_hat) * np.dot(-rik_hat, -rjk_hat)
    potential = nu * (1 + 3 * dot_product_term) / (rij_mag**3 * rik_mag**3 * rjk_mag**3)
    
    return potential

