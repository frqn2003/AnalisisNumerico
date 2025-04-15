from sympy import sympify, Symbol, solve, denom


def divisiones_por_cero(expr_str):
    x = Symbol('x')
    
    try:
        expr = sympify(expr_str)  # Convierte a expresión simbólica
        denominador = denom(expr)  # Extrae el denominador
        ceros = solve(denominador, x)  # Encuentra valores de x que hacen que se anule el denominador
        
        if ceros:
            return True, f"División por cero potencial en x = {ceros}"
        else:
            return False, "No hay división por cero detectada"
        
    except Exception as e:
        return True, f"Error al analizar la expresión: {e}"

