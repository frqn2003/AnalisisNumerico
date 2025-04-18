import numpy as np
from tkinter import messagebox

def validar_matriz(A, b):
    """
    Valida una matriz y un vector para resolver un sistema de ecuaciones.
    
    Parámetros:
    - A: Matriz de coeficientes
    - b: Vector de términos independientes
    
    Retorna:
    - bool: True si la matriz es válida, False en caso contrario
    """
    try:
        A = np.array(A, dtype=float)
        b = np.array(b, dtype=float)
        
        # Verificar dimensiones
        if A.shape[0] != len(b):
            messagebox.showwarning("Advertencia", 
                                  f"Dimensiones incompatibles: A es {A.shape[0]}x{A.shape[1]} pero b tiene {len(b)} elementos")
            return False
        
        # Verificar si la matriz es singular
        if np.linalg.det(A) == 0:
            messagebox.showwarning("Advertencia", 
                                  "La matriz es singular (determinante = 0). El sistema puede no tener solución única.")
            return False
        
        return True
    except Exception as e:
        messagebox.showwarning("Error", f"Error al validar la matriz: {e}")
        return False

def es_diagonalmente_dominante(A):
    """
    Verifica si una matriz es diagonalmente dominante.
    
    Parámetros:
    - A: Matriz a verificar
    
    Retorna:
    - bool: True si la matriz es diagonalmente dominante, False en caso contrario
    """
    n = A.shape[0]
    for i in range(n):
        if abs(A[i, i]) <= sum(abs(A[i, j]) for j in range(n) if j != i):
            return False
    return True

def gauss_seidel(A, b, x0=None, tol=1e-5, max_iter=100):
    """
    Método de Gauss-Seidel para resolver sistemas de ecuaciones lineales Ax = b.
    
    Parámetros:
    - A: Matriz de coeficientes
    - b: Vector de términos independientes
    - x0: Vector inicial (por defecto, vector de ceros)
    - tol: Tolerancia para el criterio de parada
    - max_iter: Número máximo de iteraciones
    
    Retorna:
    - x_new: Solución aproximada
    - pasos: Lista con las aproximaciones en cada iteración
    """
    # Validar la matriz y el vector
    if not validar_matriz(A, b):
        return None, []
    
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    n = len(b)
    x = np.zeros(n) if x0 is None else np.array(x0, dtype=float)
    pasos = [x.copy()]
    
    # Verificar si la matriz es diagonalmente dominante
    if not es_diagonalmente_dominante(A):
        messagebox.showwarning("Advertencia", 
                              "La matriz no es diagonalmente dominante. El método puede no converger.")
    
    # Verificar que no haya elementos diagonales nulos
    for i in range(n):
        if abs(A[i, i]) < 1e-10:
            messagebox.showwarning("Advertencia", 
                                  f"El elemento diagonal A[{i},{i}] es aproximadamente cero. El método no puede continuar.")
            return None, []
    
    for _ in range(max_iter):
        x_new = np.copy(x)
        for i in range(n):
            # Suma los productos A[i,j]*x_new[j] para j≠i (usa valores actualizados)
            s1 = sum(A[i, j] * x_new[j] for j in range(i))
            s2 = sum(A[i, j] * x[j] for j in range(i + 1, n))
            x_new[i] = (b[i] - s1 - s2) / A[i, i]
        
        pasos.append(x_new.copy())
        if np.linalg.norm(x_new - x) < tol:
            return x_new, pasos  # Converge si la norma es menor que la tolerancia
        x = x_new
    
    messagebox.showinfo("Información", 
                       f"El método alcanzó el número máximo de iteraciones ({max_iter}) sin converger.")
    return x, pasos

def jacobi(A, b, x0=None, tol=1e-5, max_iter=100):
    """
    Método de Jacobi para resolver sistemas de ecuaciones lineales Ax = b.
    
    Parámetros:
    - A: Matriz de coeficientes
    - b: Vector de términos independientes
    - x0: Vector inicial (por defecto, vector de ceros)
    - tol: Tolerancia para el criterio de parada
    - max_iter: Número máximo de iteraciones
    
    Retorna:
    - x_new: Solución aproximada
    - pasos: Lista con las aproximaciones en cada iteración
    """
    # Validar la matriz y el vector
    if not validar_matriz(A, b):
        return None, []
    
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    n = len(b)
    x = np.zeros(n) if x0 is None else np.array(x0, dtype=float)
    pasos = [x.copy()]
    
    # Verificar si la matriz es diagonalmente dominante
    if not es_diagonalmente_dominante(A):
        messagebox.showwarning("Advertencia", 
                              "La matriz no es diagonalmente dominante. El método puede no converger.")
    
    # Verificar que no haya elementos diagonales nulos
    for i in range(n):
        if abs(A[i, i]) < 1e-10:
            messagebox.showwarning("Advertencia", 
                                  f"El elemento diagonal A[{i},{i}] es aproximadamente cero. El método no puede continuar.")
            return None, []
    
    for _ in range(max_iter):
        x_new = np.zeros_like(x)
        for i in range(n):
            # Suma los productos A[i,j]*x[j] para j≠i (usa valores de la iteración anterior)
            s = sum(A[i, j] * x[j] for j in range(n) if j != i)
            x_new[i] = (b[i] - s) / A[i, i]
        
        pasos.append(x_new.copy())
        if np.linalg.norm(x_new - x) < tol:
            return x_new, pasos
        x = x_new
    
    messagebox.showinfo("Información", 
                       f"El método alcanzó el número máximo de iteraciones ({max_iter}) sin converger.")
    return x, pasos

def gauss_jordan(A, b):
    """
    Método de Gauss-Jordan para resolver sistemas de ecuaciones lineales Ax = b.
    
    Parámetros:
    - A: Matriz de coeficientes
    - b: Vector de términos independientes
    
    Retorna:
    - x: Solución exacta del sistema
    - pasos: Lista con las matrices aumentadas en cada paso
    """
    # Validar la matriz y el vector
    if not validar_matriz(A, b):
        return None, []
    
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float).reshape(-1, 1)  # Convertir b en vector columna
    n = len(b)
    
    # Crear matriz aumentada [A|b]
    Ab = np.hstack((A, b))
    pasos = [Ab.copy()]
    
    # Eliminación hacia adelante
    for i in range(n):
        # Pivoteo parcial (buscar el mayor elemento en la columna)
        max_row = i + np.argmax(abs(Ab[i:, i]))
        if max_row != i:
            Ab[[i, max_row]] = Ab[[max_row, i]]  # Intercambiar filas
            pasos.append(Ab.copy())
        
        # Hacer que el elemento diagonal sea 1
        pivot = Ab[i, i]
        if abs(pivot) < 1e-10:
            messagebox.showwarning("Advertencia", 
                                  "La matriz es singular, no se puede resolver con Gauss-Jordan")
            return None, pasos
        
        Ab[i] = Ab[i] / pivot
        pasos.append(Ab.copy())
        
        # Hacer ceros en la columna i
        for j in range(n):
            if j != i:
                factor = Ab[j, i]
                Ab[j] = Ab[j] - factor * Ab[i]
        pasos.append(Ab.copy())
    
    # Extraer la solución
    x = Ab[:, -1]
    return x, pasos