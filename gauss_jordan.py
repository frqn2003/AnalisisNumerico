import numpy as np

def gauss_jordan(A, b):
    """
    Solve a system of linear equations Ax = b using Gauss-Jordan elimination.
    
    Parameters:
    -----------
    A : numpy.ndarray
        Coefficient matrix (n x n)
    b : numpy.ndarray
        Right-hand side vector (n)
    
    Returns:
    --------
    numpy.ndarray
        The solution vector
    """
    n = len(b)
    
    # Check if A is a square matrix
    if A.shape[0] != A.shape[1]:
        raise ValueError("Matrix A must be square")
    
    # Check if A and b have compatible dimensions
    if A.shape[0] != len(b):
        raise ValueError("Dimensions of A and b are not compatible")
    
    # Create the augmented matrix [A|b]
    aug = np.column_stack((A, b))
    
    # Gauss-Jordan elimination
    for i in range(n):
        # Find the pivot row
        max_row = i + np.argmax(abs(aug[i:, i]))
        
        # Swap the current row with the pivot row
        if max_row != i:
            aug[[i, max_row]] = aug[[max_row, i]]
        
        # Check for singular matrix
        if abs(aug[i, i]) < 1e-10:
            raise ValueError("Matrix is singular or nearly singular")
        
        # Scale the pivot row to make the pivot element 1
        aug[i] = aug[i] / aug[i, i]
        
        # Eliminate other rows
        for j in range(n):
            if j != i:
                aug[j] = aug[j] - aug[j, i] * aug[i]
    
    # Extract the solution
    x = aug[:, n]
    
    return x

# Example usage
if __name__ == "__main__":
    # Example system:
    # 2x + y - z = 8
    # -3x - y + 2z = -11
    # -2x + y + 2z = -3
    
    A = np.array([
        [2, 1, -1],
        [-3, -1, 2],
        [-2, 1, 2]
    ])
    
    b = np.array([8, -11, -3])
    
    solution = gauss_jordan(A, b)
    
    print(f"Solution: {solution}")
    
    # Verify the solution
    print(f"Verification (Ax - b): {np.dot(A, solution) - b}")