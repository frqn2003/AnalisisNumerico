def regula_falsi(f, a, b, tol=1e-6, max_iter=100):
    """
    Find the root of a function using the Regula Falsi (False Position) method.
    
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
    
    fa = f(a)
    fb = f(b)
    iter_count = 0
    
    while iter_count < max_iter:
        # Calculate the false position (weighted average based on function values)
        c = (a * fb - b * fa) / (fb - fa)
        fc = f(c)
        
        if abs(fc) < tol:  # If we're close enough to zero
            return c, iter_count
        
        if fa * fc < 0:  # Root is in [a, c]
            b = c
            fb = fc
        else:  # Root is in [c, b]
            a = c
            fa = fc
            
        # Check if the interval is small enough
        if abs(b - a) < tol:
            return c, iter_count
            
        iter_count += 1
    
    return c, iter_count  # Return the last approximation

# Example usage
if __name__ == "__main__":
    # Example function: f(x) = x^3 - x - 2
    def f(x):
        return x**3 - x - 2
    
    root, iterations = regula_falsi(f, 1, 2)
    print(f"Root found: {root}")
    print(f"Function value at root: {f(root)}")
    print(f"Iterations: {iterations}")