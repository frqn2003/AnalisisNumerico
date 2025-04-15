import numpy as np

def bisection(f, a, b, tol=1e-6, max_iter=100):
    """
    Método de Bisección para encontrar raíces de ecuaciones.
    
    Parámetros:
    -----------
    f : función
        Función de la cual se busca la raíz
    a : float
        Límite inferior del intervalo inicial
    b : float
        Límite superior del intervalo inicial
    tol : float, opcional
        Tolerancia para el criterio de convergencia
    max_iter : int, opcional
        Número máximo de iteraciones
        
    Retorna:
    --------
    float
        La aproximación de la raíz encontrada
    int
        Número de iteraciones realizadas
    list
        Lista de aproximaciones intermedias
    """
    # Verificar que f(a) y f(b) tengan signos opuestos
    if f(a) * f(b) >= 0:
        raise ValueError("La función debe tener signos opuestos en los extremos del intervalo")
    
    iteraciones = 0
    aproximaciones = []
    
    while (b - a) > tol and iteraciones < max_iter:
        c = (a + b) / 2  # Punto medio
        aproximaciones.append(c)
        
        if f(c) == 0:
            return c, iteraciones, aproximaciones  # Raíz exacta encontrada
        
        if f(a) * f(c) < 0:
            b = c  # La raíz está en [a, c]
        else:
            a = c  # La raíz está en [c, b]
            
        iteraciones += 1
    
    raiz = (a + b) / 2  # Aproximación final
    return raiz, iteraciones, aproximaciones

# Ejemplo de uso
if __name__ == "__main__":
    # Definir una función de ejemplo: f(x) = x^3 - x - 2
    def funcion_ejemplo(x):
        return x**3 - x - 2
    
    # Intervalo inicial [1, 2]
    raiz, iteraciones, aproximaciones = bisection(funcion_ejemplo, 1, 2)
    
    print(f"Raíz aproximada: {raiz}")
    print(f"Valor de la función en la raíz: {funcion_ejemplo(raiz)}")
    print(f"Iteraciones realizadas: {iteraciones}")
    print(f"Aproximaciones intermedias: {aproximaciones}")
