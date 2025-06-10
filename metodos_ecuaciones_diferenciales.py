import numpy as np
from sympy import Symbol, sympify
from tkinter import messagebox

def validar_ecuacion_diferencial(f_expr, x0, y0, h, x_final):
    """
    Valida una ecuación diferencial para métodos numéricos.
    
    Parámetros:
    - f_expr: Expresión de la función f(x,y) donde dy/dx = f(x,y)
    - x0, y0: Condiciones iniciales
    - h: Tamaño del paso
    - x_final: Valor final de x
    
    Retorna:
    - bool: True si la ecuación es válida, False en caso contrario
    """
    x, y = Symbol('x'), Symbol('y')
    
    # Convertir a expresión simbólica si es string
    if isinstance(f_expr, str):
        f_expr = sympify(f_expr)
    
    try:
        # Convertir a función numérica y probar en el punto inicial
        f_num = lambda x_val, y_val: float(f_expr.subs([(x, x_val), (y, y_val)]))
        f_num(x0, y0)  # Intentar evaluar en el punto inicial
        
        return True
    except Exception as e:
        messagebox.showerror("Error", f"Error al evaluar la ecuación diferencial: {e}")
        return False

def runge_kutta_1er_orden(f, x0, y0, h, x_final):
    """
    Método de Runge-Kutta de 1er orden (Método de Euler) para resolver EDO.
    
    Parámetros:
    - f: Función f(x,y) donde dy/dx = f(x,y) (expresión simbólica)
    - x0, y0: Condiciones iniciales
    - h: Tamaño del paso
    - x_final: Valor final de x
    
    Retorna:
    - solucion: Lista de tuplas (x, y) con la solución
    - pasos: Información detallada del cálculo
    """
    x, y = Symbol('x'), Symbol('y')
    
    # Validar la ecuación diferencial
    if not validar_ecuacion_diferencial(f, x0, y0, h, x_final):
        return None, []
    
    # Convertir a función numérica
    f_num = lambda x_val, y_val: float(f.subs([(x, x_val), (y, y_val)]))
    
    # Inicializar variables
    x_vals = [x0]
    y_vals = [y0]
    x_current = x0
    y_current = y0
    
    pasos_detallados = []
    
    # Calcular número de pasos
    n_pasos = int((x_final - x0) / h)
    
    for i in range(n_pasos):
        # Método de Euler: y_{n+1} = y_n + h * f(x_n, y_n)
        k1 = f_num(x_current, y_current)
        
        y_next = y_current + h * k1
        x_next = x_current + h
        
        # Guardar información del paso
        paso_info = {
            'iteracion': i + 1,
            'x_n': x_current,
            'y_n': y_current,
            'k1': k1,
            'y_next': y_next,
            'x_next': x_next
        }
        pasos_detallados.append(paso_info)
        
        # Actualizar valores
        x_vals.append(x_next)
        y_vals.append(y_next)
        x_current = x_next
        y_current = y_next
    
    solucion = list(zip(x_vals, y_vals))
    
    pasos = {
        'metodo': 'Runge-Kutta 1er Orden (Euler)',
        'ecuacion': str(f),
        'condiciones_iniciales': (x0, y0),
        'h': h,
        'x_final': x_final,
        'n_pasos': n_pasos,
        'pasos_detallados': pasos_detallados,
        'solucion': solucion
    }
    
    return solucion, pasos

def runge_kutta_4to_orden(f, x0, y0, h, x_final):
    """
    Método de Runge-Kutta de 4to orden para resolver EDO.
    
    Parámetros:
    - f: Función f(x,y) donde dy/dx = f(x,y) (expresión simbólica)
    - x0, y0: Condiciones iniciales
    - h: Tamaño del paso
    - x_final: Valor final de x
    
    Retorna:
    - solucion: Lista de tuplas (x, y) con la solución
    - pasos: Información detallada del cálculo
    """
    x, y = Symbol('x'), Symbol('y')
    
    # Validar la ecuación diferencial
    if not validar_ecuacion_diferencial(f, x0, y0, h, x_final):
        return None, []
    
    # Convertir a función numérica
    f_num = lambda x_val, y_val: float(f.subs([(x, x_val), (y, y_val)]))
    
    # Inicializar variables
    x_vals = [x0]
    y_vals = [y0]
    x_current = x0
    y_current = y0
    
    pasos_detallados = []
    
    # Calcular número de pasos
    n_pasos = int((x_final - x0) / h)
    
    for i in range(n_pasos):
        # Calcular k1, k2, k3, k4
        k1 = f_num(x_current, y_current)
        k2 = f_num(x_current + h/2, y_current + h*k1/2)
        k3 = f_num(x_current + h/2, y_current + h*k2/2)
        k4 = f_num(x_current + h, y_current + h*k3)
        
        # Calcular y_{n+1}
        y_next = y_current + (h/6) * (k1 + 2*k2 + 2*k3 + k4)
        x_next = x_current + h
        
        # Guardar información del paso
        paso_info = {
            'iteracion': i + 1,
            'x_n': x_current,
            'y_n': y_current,
            'k1': k1,
            'k2': k2,
            'k3': k3,
            'k4': k4,
            'y_next': y_next,
            'x_next': x_next
        }
        pasos_detallados.append(paso_info)
        
        # Actualizar valores
        x_vals.append(x_next)
        y_vals.append(y_next)
        x_current = x_next
        y_current = y_next
    
    solucion = list(zip(x_vals, y_vals))
    
    pasos = {
        'metodo': 'Runge-Kutta 4to Orden',
        'ecuacion': str(f),
        'condiciones_iniciales': (x0, y0),
        'h': h,
        'x_final': x_final,
        'n_pasos': n_pasos,
        'pasos_detallados': pasos_detallados,
        'solucion': solucion
    }
    
    return solucion, pasos

def calcular_k_values(f, x_n, y_n, h):
    """
    Calcula los valores k1, k2, k3, k4 para el método de Runge-Kutta de 4to orden.
    
    Parámetros:
    - f: Función f(x,y) (expresión simbólica)
    - x_n, y_n: Valores actuales de x e y
    - h: Tamaño del paso
    
    Retorna:
    - dict: Diccionario con los valores k1, k2, k3, k4
    """
    x, y = Symbol('x'), Symbol('y')
    
    # Convertir a función numérica
    f_num = lambda x_val, y_val: float(f.subs([(x, x_val), (y, y_val)]))
    
    # Calcular k1, k2, k3, k4
    k1 = f_num(x_n, y_n)
    k2 = f_num(x_n + h/2, y_n + h*k1/2)
    k3 = f_num(x_n + h/2, y_n + h*k2/2)
    k4 = f_num(x_n + h, y_n + h*k3)
    
    return {
        'k1': k1,
        'k2': k2,
        'k3': k3,
        'k4': k4
    }

def mostrar_k_values_detallado(f, x_n, y_n, h):
    """
    Muestra el cálculo detallado de los valores k para fines educativos.
    
    Parámetros:
    - f: Función f(x,y) (expresión simbólica)
    - x_n, y_n: Valores actuales de x e y
    - h: Tamaño del paso
    
    Retorna:
    - str: Descripción detallada del cálculo
    """
    k_vals = calcular_k_values(f, x_n, y_n, h)
    
    descripcion = f"""
Cálculo de valores k para Runge-Kutta 4to orden:

Punto actual: (x_n, y_n) = ({x_n:.6f}, {y_n:.6f})
Tamaño de paso: h = {h}

k1 = f(x_n, y_n) = f({x_n:.6f}, {y_n:.6f}) = {k_vals['k1']:.6f}

k2 = f(x_n + h/2, y_n + h*k1/2)
   = f({x_n:.6f} + {h}/2, {y_n:.6f} + {h}*{k_vals['k1']:.6f}/2)
   = f({x_n + h/2:.6f}, {y_n + h*k_vals['k1']/2:.6f})
   = {k_vals['k2']:.6f}

k3 = f(x_n + h/2, y_n + h*k2/2)
   = f({x_n:.6f} + {h}/2, {y_n:.6f} + {h}*{k_vals['k2']:.6f}/2)
   = f({x_n + h/2:.6f}, {y_n + h*k_vals['k2']/2:.6f})
   = {k_vals['k3']:.6f}

k4 = f(x_n + h, y_n + h*k3)
   = f({x_n:.6f} + {h}, {y_n:.6f} + {h}*{k_vals['k3']:.6f})
   = f({x_n + h:.6f}, {y_n + h*k_vals['k3']:.6f})
   = {k_vals['k4']:.6f}

y_{{n+1}} = y_n + (h/6)(k1 + 2k2 + 2k3 + k4)
         = {y_n:.6f} + ({h}/6)({k_vals['k1']:.6f} + 2*{k_vals['k2']:.6f} + 2*{k_vals['k3']:.6f} + {k_vals['k4']:.6f})
         = {y_n + (h/6)*(k_vals['k1'] + 2*k_vals['k2'] + 2*k_vals['k3'] + k_vals['k4']):.6f}
"""
    
    return descripcion