import numpy as np

def jacobi(A, b, x0=None, tol=1e-6, max_iter=100):
    """
    Método de Jacobi para resolver sistemas de ecuaciones lineales.
    
    Parámetros:
    -----------
    A : numpy.ndarray
        Matriz de coeficientes
    b : numpy.ndarray
        Vector de términos independientes
    x0 : numpy.ndarray, opcional
        Vector inicial de aproximación
    tol : float, opcional
        Tolerancia para el criterio de convergencia
    max_iter : int, opcional
        Número máximo de iteraciones
        
    Retorna:
    --------
    numpy.ndarray
        Vector solución
    int
        Número de iteraciones realizadas
    list
        Lista de aproximaciones intermedias
    """
    # Convertir las entradas a arrays de numpy
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    
    # Obtener dimensiones
    n = len(b)
    
    # Verificar que la matriz es cuadrada
    if A.shape[0] != A.shape[1]:
        raise ValueError("La matriz A debe ser cuadrada")
    
    # Verificar que A y b tienen dimensiones compatibles
    if A.shape[0] != len(b):
        raise ValueError("Las dimensiones de A y b no son compatibles")
    
    # Inicializar el vector de solución
    if x0 is None:
        x = np.zeros(n)
    else:
        x = np.array(x0, dtype=float)
    
    # Lista para almacenar aproximaciones
    aproximaciones = [x.copy()]
    
    # Iteraciones
    for iter_count in range(max_iter):
        x_nueva = np.zeros(n)
        
        for i in range(n):
            # Verificar división por cero
            if A[i, i] == 0:
                raise ValueError(f"División por cero encontrada en la fila {i}. Considere reordenar las ecuaciones.")
                
            # Suma de todos los términos excepto el término diagonal
            suma = np.dot(A[i, :], x) - A[i, i] * x[i]
            
            # Actualizar x_i
            x_nueva[i] = (b[i] - suma) / A[i, i]
        
        # Guardar la aproximación actual
        aproximaciones.append(x_nueva.copy())
        
        # Verificar convergencia
        if np.linalg.norm(x_nueva - x, np.inf) < tol:
            return x_nueva, iter_count + 1, aproximaciones
        
        # Actualizar x para la siguiente iteración
        x = x_nueva.copy()
    
    # Si se alcanza el máximo de iteraciones
    return x, max_iter, aproximaciones

# Ejemplo de uso
if __name__ == "__main__":
    # Sistema de ecuaciones:
    # 4x + y - z = 7
    # x + 5y + 2z = 8
    # 2x + y + 6z = 9
    
    A = np.array([
        [4, 1, -1],
        [1, 5, 2],
        [2, 1, 6]
    ])
    
    b = np.array([7, 8, 9])
    
    # Valor inicial
    x0 = np.zeros(3)
    
    # Resolver el sistema
    solucion, iteraciones, aproximaciones = jacobi(A, b, x0)
    
    print(f"Solución: {solucion}")
    print(f"Iteraciones realizadas: {iteraciones}")
    print(f"Aproximación final: {aproximaciones[-1]}")
    
    # Verificar la solución
    print(f"Verificación (Ax - b): {np.dot(A, solucion) - b}")
