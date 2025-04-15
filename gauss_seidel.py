import numpy as np

def gauss_seidel(A, b, x0=None, tol=1e-6, max_iter=100):
    """
    Método de Gauss-Seidel para resolver sistemas de ecuaciones lineales.
    
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
    
    # Verificar que las dimensiones son compatibles
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
    for iteracion in range(max_iter):
        x_anterior = x.copy()
        
        for i in range(n):
            # Verificar que no hay división por cero
            if A[i, i] == 0:
                raise ValueError(f"División por cero encontrada en la fila {i}. Considere reordenar las ecuaciones.")
            
            # Sumatoria de a_ij * x_j para j < i (términos ya actualizados)
            suma1 = np.dot(A[i, :i], x[:i])
            
            # Sumatoria de a_ij * x_j para j > i (términos de la iteración anterior)
            suma2 = np.dot(A[i, i+1:], x_anterior[i+1:])
            
            # Actualizar x_i
            x[i] = (b[i] - suma1 - suma2) / A[i, i]
        
        # Guardar la aproximación actual
        aproximaciones.append(x.copy())
        
        # Verificar convergencia
        if np.linalg.norm(x - x_anterior, np.inf) < tol:
            return x, iteracion + 1, aproximaciones
    
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
    solucion, iteraciones, aproximaciones = gauss_seidel(A, b, x0)
    
    print(f"Solución: {solucion}")
    print(f"Iteraciones realizadas: {iteraciones}")
    print(f"Aproximación final: {aproximaciones[-1]}")
    
    # Verificar la solución
    print(f"Verificación (Ax - b): {np.dot(A, solucion) - b}")
    
    # Mostrar algunas aproximaciones intermedias
    if len(aproximaciones) > 5:
        print("\nAlgunas aproximaciones intermedias:")
        for i, aprox in enumerate(aproximaciones[:5]):
            print(f"Iteración {i}: {aprox}")
