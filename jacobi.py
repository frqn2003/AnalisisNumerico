import numpy as np

def jacobi(A, b, x0=None, tol=1e-6, max_iter=100):
    """
    Solve a system of linear equations Ax = b using the Jacobi method.
    
    Parameters:
    -----------
    A : numpy.ndarray
        Coefficient matrix (n x n)
    b : numpy.ndarray
        Right-hand side vector (n)
    x0 : numpy.ndarray, optional
        Initial guess for the solution (default: zeros)
    tol : float, optional
        Tolerance for convergence (default: 1e-6)
    max_iter : int, optional
        Maximum number of iterations (default: 100)
    
    Returns:
    --------
    numpy.ndarray
        The approximate solution vector
    int
        Number of iterations performed
    bool
        Whether the method converged
    """
    n = len(b)
    
    # Check if A is a square matrix
    if A.shape[0] != A.shape[1]:
        raise ValueError("Matrix A must be square")
    
    # Check if A and b have compatible dimensions
    if A.shape[0] != len(b):
        raise ValueError("Dimensions of A and b are not compatible")
    
    # Initialize x if not provided
    if x0 is None:
        x = np.zeros(n)
    else:
        x = x0.copy()
    
    # Iterate until convergence or max iterations
    for iter_count in range(max_iter):
        x_new = np.zeros(n)
        
        # Update each component of x
        for i in range(n):
            # Calculate the sum of known terms
            sum_terms = sum(A[i, j] * x[j] for j in range(n) if j != i)
            
            # Check for division by zero
            if A[i, i] == 0:
                raise ValueError(f"Division by zero encountered at row {i}. Consider reordering the equations.")
            
            # Update x_new[i]
            x_new[i] = (b[i] - sum_terms) / A[i, i]
        
        # Check for convergence
        if np.linalg.norm(x_new - x, np.inf) < tol:
            return x_new, iter_count + 1, True
        
        # Update x for next iteration
        x = x_new.copy()
    
    # If we've reached max_iter without converging
    return x, max_iter, False

# Example usage
if __name__ == "__main__":
    # Example system:
    # 4x + y - z = 7
    # x + 5y + 2z = 8
    # 2x + y + 6z = 9
    
    A = np.array([
        [4, 1, -1],
        [1, 5, 2],
        [2, 1, 6]
    ])
    
    b = np.array([7, 8, 9])
    
    solution, iterations, converged = jacobi(A, b)
    
    print(f"Solution: {solution}")
    print(f"Iterations: {iterations}")
    print(f"Converged: {converged}")
    
    # Verify the solution
    print(f"Verification (Ax - b): {np.dot(A, solution) - b}")