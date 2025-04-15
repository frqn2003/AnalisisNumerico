def bisection(f, a, b, tol=1e-6, max_iter=100):
    """
    Find the root of a function using the bisection method.
    
    Parameters:
    -----------
    f : function
        The function for which we want to find the root
    a, b : float
        The interval [a, b] where f(a) and f(b) have opposite signs
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
    # Check if f(a) and f(b) have opposite signs
    if f(a) * f(b) >= 0:
        raise ValueError("Function values at interval endpoints must have opposite signs")
    
    iter_count = 0
    
    while (b - a) / 2 > tol and iter_count < max_iter:
        c = (a + b) / 2  # Midpoint
        fc = f(c)
        
        if abs(fc) < tol:  # If we're close enough to zero
            return c, iter_count
        
        if f(a) * fc < 0:  # Root is in [a, c]
            b = c
        else:  # Root is in [c, b]
            a = c
            
        iter_count += 1
    
    return (a + b) / 2, iter_count

# Example usage
if __name__ == "__main__":
    # Example function: f(x) = x^3 - x - 2
    def f(x):
        return x**3 - x - 2
    
    root, iterations = bisection(f, 1, 2)
    print(f"Root found: {root}")
    print(f"Function value at root: {f(root)}")
    print(f"Iterations: {iterations}")