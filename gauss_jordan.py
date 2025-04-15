import numpy as np

def gauss_jordan(A, b):
    """
    Método de Gauss-Jordan para resolver sistemas de ecuaciones lineales.
    
    Parámetros:
    -----------
    A : numpy.ndarray
        Matriz de coeficientes
    b : numpy.ndarray
        Vector de términos independientes
        
    Retorna:
    --------
    numpy.ndarray
        Vector solución
    """
    # Convertir las entradas a arrays de numpy y asegurar que son de tipo float
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
    
    # Crear la matriz aumentada [A|b]
    Ab = np.column_stack((A, b))
    
    # Aplicar eliminación de Gauss-Jordan
    for i in range(n):
        # Pivoteo parcial: encontrar el pivote máximo en la columna i
        max_index = i + np.argmax(abs(Ab[i:, i]))
        
        # Intercambiar filas si es necesario
        if max_index != i:
            Ab[[i, max_index]] = Ab[[max_index, i]]
        
        # Verificar si la matriz es singular
        pivot = Ab[i, i]
        if abs(pivot) < 1e-10:
            raise ValueError("La matriz es singular o casi singular")
        
        # Dividir la fila i por el pivot para obtener un 1 en la posición (i,i)
        Ab[i] = Ab[i] / pivot
        
        # Hacer ceros por encima y por debajo del pivote
        for j in range(n):
            if j != i:
                factor = Ab[j, i]
                Ab[j] = Ab[j] - factor * Ab[i]
    
    # Extraer la solución (última columna de la matriz aumentada)
    x = Ab[:, -1]
    
    return x

# Ejemplo de uso
if __name__ == "__main__":
    # Sistema de ecuaciones:
    # 2x + y - z = 8
    # -3x - y + 2z = -11
    # -2x + y + 2z = -3
    
    A = np.array([
        [2, 1, -1],
        [-3, -1, 2],
        [-2, 1, 2]
    ])
    
    b = np.array([8, -11, -3])
    
    # Resolver el sistema
    solucion = gauss_jordan(A, b)
    
    print(f"Solución: {solucion}")
    
    # Verificar la solución
    print(f"Verificación (A·x): {np.dot(A, solucion)}")
    print(f"Vector b original: {b}")
    print(f"Diferencia (A·x - b): {np.dot(A, solucion) - b}")
