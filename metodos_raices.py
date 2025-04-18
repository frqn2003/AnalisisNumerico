import numpy as np
from sympy import Symbol, diff, sympify, denom, solve
from tkinter import messagebox

def divisiones_por_cero(expr_str):
    """
    Verifica si una expresión puede tener divisiones por cero.
    
    Parámetros:
    - expr_str: Expresión matemática como string
    
    Retorna:
    - (bool, str): Tupla con un booleano indicando si hay división por cero
                  y un mensaje descriptivo
    """
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

def validar_funcion(f_expr, a=None, b=None):
    """
    Valida una función para evitar divisiones por cero en el intervalo [a, b].
    
    Parámetros:
    - f_expr: Expresión simbólica de la función
    - a, b: Límites del intervalo (opcional)
    
    Retorna:
    - bool: True si la función es válida, False en caso contrario
    """
    x = Symbol('x')
    
    # Convertir a expresión simbólica si es string
    if isinstance(f_expr, str):
        f_expr = sympify(f_expr)
    
    # Verificar divisiones por cero
    hay_division, mensaje = divisiones_por_cero(str(f_expr))
    
    if hay_division:
        # Si se proporciona un intervalo, verificar si los puntos de división por cero están en él
        if a is not None and b is not None:
            denominador = denom(f_expr)
            ceros = solve(denominador, x)
            
            # Filtrar solo los ceros reales en el intervalo [a, b]
            ceros_en_intervalo = [float(cero) for cero in ceros 
                                 if cero.is_real and a <= float(cero) <= b]
            
            if ceros_en_intervalo:
                messagebox.showwarning("Advertencia", 
                                      f"La función tiene divisiones por cero en x = {ceros_en_intervalo} dentro del intervalo [{a}, {b}]")
                return False
            else:
                # Hay divisiones por cero pero no en el intervalo
                return True
        else:
            messagebox.showwarning("Advertencia", mensaje)
            return False
    
    return True

def biseccion(f, a, b, tol=1e-6, max_iter=100):
    """
    Método de bisección para encontrar raíces de una función.
    
    Parámetros:
    - f: Función a evaluar (expresión simbólica)
    - a, b: Límites del intervalo inicial
    - tol: Tolerancia para el criterio de parada
    - max_iter: Número máximo de iteraciones
    
    Retorna:
    - c: Aproximación de la raíz
    - pasos: Lista con las aproximaciones en cada iteración
    """
    x = Symbol('x')
    
    # Validar la función en el intervalo
    if not validar_funcion(f, a, b):
        return None, []
    
    # Convertir a función numérica
    f_num = lambda val: float(f.subs(x, val))
    
    # Verificar que f(a) y f(b) tienen signos opuestos
    if f_num(a) * f_num(b) >= 0:
        messagebox.showwarning("Advertencia", 
                              f"f({a}) y f({b}) deben tener signos opuestos para garantizar una raíz en el intervalo.")
        return None, []
    
    pasos = []
    c = a
    
    for i in range(max_iter):
        c = (a + b) / 2
        pasos.append(c)
        
        if abs(f_num(c)) < tol or (b - a) / 2 < tol:
            return c, pasos
        
        if f_num(c) * f_num(a) < 0:
            b = c
        else:
            a = c
    
    return c, pasos

def regula_falsi(f, a, b, tol=1e-6, max_iter=100):
    """
    Método de regula falsi (falsa posición) para encontrar raíces de una función.
    
    Parámetros:
    - f: Función a evaluar (expresión simbólica)
    - a, b: Límites del intervalo inicial
    - tol: Tolerancia para el criterio de parada
    - max_iter: Número máximo de iteraciones
    
    Retorna:
    - c: Aproximación de la raíz
    - pasos: Lista con las aproximaciones en cada iteración
    """
    x = Symbol('x')
    
    # Validar la función en el intervalo
    if not validar_funcion(f, a, b):
        return None, []
    
    # Convertir a función numérica
    f_num = lambda val: float(f.subs(x, val))
    
    # Verificar que f(a) y f(b) tienen signos opuestos
    if f_num(a) * f_num(b) >= 0:
        messagebox.showwarning("Advertencia", 
                              f"f({a}) y f({b}) deben tener signos opuestos para garantizar una raíz en el intervalo.")
        return None, []
    
    pasos = []
    c = a
    
    for i in range(max_iter):
        fa = f_num(a)
        fb = f_num(b)
        
        # Calcular el punto de intersección con el eje x
        c = (a * fb - b * fa) / (fb - fa)
        pasos.append(c)
        
        fc = f_num(c)
        
        if abs(fc) < tol or abs(b - a) < tol:
            return c, pasos
        
        if fc * fa < 0:
            b = c
        else:
            a = c
    
    return c, pasos

def newton(f, x0, tol=1e-6, max_iter=100):
    """
    Método de Newton-Raphson para encontrar raíces de una función.
    
    Parámetros:
    - f: Función a evaluar (expresión simbólica)
    - x0: Punto inicial
    - tol: Tolerancia para el criterio de parada
    - max_iter: Número máximo de iteraciones
    
    Retorna:
    - x: Aproximación de la raíz
    - pasos: Lista con las aproximaciones en cada iteración
    """
    x = Symbol('x')
    
    # Validar la función
    if not validar_funcion(f):
        return None, []
    
    # Calcular la derivada
    df = diff(f, x)
    
    # Convertir a funciones numéricas
    f_num = lambda val: float(f.subs(x, val))
    df_num = lambda val: float(df.subs(x, val))
    
    pasos = [x0]
    x_n = x0
    
    for i in range(max_iter):
        # Verificar que la derivada no sea cero
        if abs(df_num(x_n)) < 1e-10:
            messagebox.showwarning("Advertencia", 
                                  f"La derivada es aproximadamente cero en x = {x_n}. El método no puede continuar.")
            return x_n, pasos
        
        # Fórmula de Newton
        x_n1 = x_n - f_num(x_n) / df_num(x_n)
        pasos.append(x_n1)
        
        if abs(x_n1 - x_n) < tol:
            return x_n1, pasos
        
        x_n = x_n1
    
    return x_n, pasos

def secante(f, x0, x1, tol=1e-6, max_iter=100):
    """
    Método de la secante para encontrar raíces de una función.
    
    Parámetros:
    - f: Función a evaluar (expresión simbólica)
    - x0, x1: Puntos iniciales
    - tol: Tolerancia para el criterio de parada
    - max_iter: Número máximo de iteraciones
    
    Retorna:
    - x: Aproximación de la raíz
    - pasos: Lista con las aproximaciones en cada iteración
    """
    x = Symbol('x')
    
    # Validar la función
    if not validar_funcion(f):
        return None, []
    
    # Convertir a función numérica
    f_num = lambda val: float(f.subs(x, val))
    
    pasos = [x0, x1]
    
    for i in range(max_iter):
        f_x0 = f_num(x0)
        f_x1 = f_num(x1)
        
        # Verificar división por cero
        if abs(f_x1 - f_x0) < 1e-10:
            messagebox.showwarning("Advertencia", 
                                  "La pendiente de la secante es aproximadamente cero. El método no puede continuar.")
            return x1, pasos
        
        # Fórmula de la secante
        x2 = x1 - f_x1 * (x1 - x0) / (f_x1 - f_x0)
        pasos.append(x2)
        
        if abs(x2 - x1) < tol:
            return x2, pasos
        
        x0, x1 = x1, x2
    
    return x1, pasos