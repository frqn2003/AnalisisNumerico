def newton(f, df, x0, tol=1e-6, max_iter=100):
    """
    Find the root of a function using Newton's method.
    
    Parameters:
    -----------
    f : function
        The function for which we want to find the root
    df : function
        The derivative of the function f
    x0 : float
        Initial guess for the root
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
    x = x0
    iter_count = 0
    
    while iter_count < max_iter:
        fx = f(x)
        
        if abs(fx) < tol:  # If we're close enough to zero
            return x, iter_count
        
        dfx = df(x)
        
        if dfx == 0:
            raise ValueError("Derivative is zero. Newton's method fails.")
        
        # Newton's formula
        x_new = x - fx / dfx
        
        # Check for convergence
        if abs(x_new - x) < tol:
            return x_new, iter_count
        
        x = x_new
        iter_count += 1
    
    return x, iter_count  # Return the last approximation

# Example usage
if __name__ == "__main__":
    import math
    
    # Example function: f(x) = x^3 - x - 2
    def f(x):
        return x**3 - x - 2
    
    # Derivative of f(x)
    def df(x):
        return 3*x**2 - 1
    
    root, iterations = newton(f, df, 1.5)
    print(f"Root found: {root}")
    print(f"Function value at root: {f(root)}")
    print(f"Iterations: {iterations}")