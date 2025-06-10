import numpy as np
from sympy import Symbol, sympify
from tkinter import messagebox

def validar_funcion_integracion(f_expr, a, b):
    """
    Valida una función para integración numérica.
    
    Parámetros:
    - f_expr: Expresión simbólica de la función
    - a, b: Límites de integración
    
    Retorna:
    - bool: True si la función es válida, False en caso contrario
    """
    x = Symbol('x')
    
    # Convertir a expresión simbólica si es string
    if isinstance(f_expr, str):
        f_expr = sympify(f_expr)
    
    try:
        # Convertir a función numérica y probar en algunos puntos
        f_num = lambda val: float(f_expr.subs(x, val))
        test_points = np.linspace(a, b, 10)
        
        for point in test_points:
            f_num(point)  # Intentar evaluar
        
        return True
    except Exception as e:
        messagebox.showerror("Error", f"Error al evaluar la función: {e}")
        return False

def regla_trapecios(f, a, b, n=100):
    """
    Método de integración por regla de los trapecios.
    
    Parámetros:
    - f: Función a integrar (expresión simbólica)
    - a, b: Límites de integración
    - n: Número de subintervalos
    
    Retorna:
    - integral: Valor aproximado de la integral
    - pasos: Información detallada del cálculo
    """
    x = Symbol('x')
    
    # Validar la función
    if not validar_funcion_integracion(f, a, b):
        return None, []
    
    # Convertir a función numérica
    f_num = lambda val: float(f.subs(x, val))
    
    # Calcular el paso
    h = (b - a) / n
    
    # Calcular los puntos
    x_vals = np.linspace(a, b, n + 1)
    y_vals = [f_num(x_val) for x_val in x_vals]
    
    # Aplicar la regla de los trapecios
    integral = h * (y_vals[0] + 2 * sum(y_vals[1:-1]) + y_vals[-1]) / 2
    
    # Información detallada
    pasos = {
        'metodo': 'Regla de los Trapecios',
        'funcion': str(f),
        'limites': [a, b],
        'n_intervalos': n,
        'h': h,
        'puntos_x': x_vals.tolist(),
        'puntos_y': y_vals,
        'integral': integral
    }
    
    return integral, pasos

def simpson_1_3(f, a, b, n=100):
    """
    Método de integración por regla de Simpson 1/3.
    
    Parámetros:
    - f: Función a integrar (expresión simbólica)
    - a, b: Límites de integración
    - n: Número de subintervalos (debe ser par)
    
    Retorna:
    - integral: Valor aproximado de la integral
    - pasos: Información detallada del cálculo
    """
    x = Symbol('x')
    
    # Validar la función
    if not validar_funcion_integracion(f, a, b):
        return None, []
    
    # Asegurar que n sea par
    if n % 2 != 0:
        n += 1
        messagebox.showinfo("Información", f"n debe ser par. Se ajustó a n = {n}")
    
    # Convertir a función numérica
    f_num = lambda val: float(f.subs(x, val))
    
    # Calcular el paso
    h = (b - a) / n
    
    # Calcular los puntos
    x_vals = np.linspace(a, b, n + 1)
    y_vals = [f_num(x_val) for x_val in x_vals]
    
    # Aplicar la regla de Simpson 1/3
    integral = h * (y_vals[0] + 4 * sum(y_vals[1::2]) + 2 * sum(y_vals[2:-1:2]) + y_vals[-1]) / 3
    
    # Información detallada
    pasos = {
        'metodo': 'Regla de Simpson 1/3',
        'funcion': str(f),
        'limites': [a, b],
        'n_intervalos': n,
        'h': h,
        'puntos_x': x_vals.tolist(),
        'puntos_y': y_vals,
        'integral': integral
    }
    
    return integral, pasos

def simpson_3_8(f, a, b, n=99):
    """
    Método de integración por regla de Simpson 3/8.
    
    Parámetros:
    - f: Función a integrar (expresión simbólica)
    - a, b: Límites de integración
    - n: Número de subintervalos (debe ser múltiplo de 3)
    
    Retorna:
    - integral: Valor aproximado de la integral
    - pasos: Información detallada del cálculo
    """
    x = Symbol('x')
    
    # Validar la función
    if not validar_funcion_integracion(f, a, b):
        return None, []
    
    # Asegurar que n sea múltiplo de 3
    if n % 3 != 0:
        n = ((n // 3) + 1) * 3
        messagebox.showinfo("Información", f"n debe ser múltiplo de 3. Se ajustó a n = {n}")
    
    # Convertir a función numérica
    f_num = lambda val: float(f.subs(x, val))
    
    # Calcular el paso
    h = (b - a) / n
    
    # Calcular los puntos
    x_vals = np.linspace(a, b, n + 1)
    y_vals = [f_num(x_val) for x_val in x_vals]
    
    # Aplicar la regla de Simpson 3/8
    integral = 0
    for i in range(0, n, 3):
        integral += (3 * h / 8) * (y_vals[i] + 3 * y_vals[i + 1] + 3 * y_vals[i + 2] + y_vals[i + 3])
    
    # Información detallada
    pasos = {
        'metodo': 'Regla de Simpson 3/8',
        'funcion': str(f),
        'limites': [a, b],
        'n_intervalos': n,
        'h': h,
        'puntos_x': x_vals.tolist(),
        'puntos_y': y_vals,
        'integral': integral
    }
    
    return integral, pasos