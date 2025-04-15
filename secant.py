def secant(f, x0, x1, tol=1e-6, max_iter=100):
    """
    Find the root of a function using the Secant method.
    
    Parameters:
    -----------
    f : function
        The function for which we want to find the root
    x0, x1 : float
        Two initial guesses close to the root
    tol : float, optional
        Tolerance for convergence (default: 1e-6)
    max_iter : int, optional
        Maximum number of iterations (default: 100)
    
    Returns:
    --------
    float
        The approximate root of the function
    int
        Number of iterations performed
    """
    f0 = f(x0)
    f1 = f(x1)
    iter_count = 0
    
    while iter_count < max_iter:
        if abs(f1) < tol:  # If we're close enough to zero
            return x1, iter_count
        
        if f1 == f0:
            raise ValueError("Division by zero in Secant method. Try different initial points.")
        
        # Secant formula
        x_new = x1 - f1 * (x1 - x0) / (f1 - f0)
        
        # Check for convergence
        if abs(x_new - x1) < tol:
            return x_new, iter_count
        
        # Update values for next iteration
        x0, x1 = x1, x_new
        f0, f1 = f1, f(x_new)
        
        iter_count += 1
    
    return x1, iter_count  # Return the last approximation

# Example usage
if __name__ == "__main__":
    # Example function: f(x) = x^3 - x - 2
    def f(x):
        return x**3 - x - 2
    
    root, iterations = secant(f, 1.0, 2.0)
    print(f"Root found: {root}")
    print(f"Function value at root: {f(root)}")
    print(f"Iterations: {iterations}")