import numpy as np

def regula_falsi(f, a, b, tol=1e-6, max_iter=100):
    """
    Método de Regula Falsi (Falsa Posición) para encontrar raíces de ecuaciones.
    
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
    
    fa = f(a)
    fb = f(b)
    iteraciones = 0
    aproximaciones = []
    
    while iteraciones < max_iter:
        # Calcular el punto de intersección con el eje x
        c = (a * fb - b * fa) / (fb - fa)
        aproximaciones.append(c)
        fc = f(c)
        
        if abs(fc) < tol:  # Convergencia alcanzada
            return c, iteraciones, aproximaciones
        
        if fa * fc < 0:  # Raíz está en [a, c]
            b = c
            fb = fc
        else:  # Raíz está en [c, b]
            a = c
            fa = fc
            
        # Verificar si el intervalo es suficientemente pequeño
        if abs(b - a) < tol:
            return c, iteraciones, aproximaciones
            
        iteraciones += 1
    
    # Retornar la última aproximación si se alcanza el máximo de iteraciones
    return c, iteraciones, aproximaciones

# Ejemplo de uso
if __name__ == "__main__":
    # Definir una función de ejemplo: f(x) = x^3 - x - 2
    def funcion_ejemplo(x):
        return x**3 - x - 2
    
    # Intervalo inicial [1, 2]
    raiz, iteraciones, aproximaciones = regula_falsi(funcion_ejemplo, 1, 2)
    
    print(f"Raíz aproximada: {raiz}")
    print(f"Valor de la función en la raíz: {funcion_ejemplo(raiz)}")
    print(f"Iteraciones realizadas: {iteraciones}")
    print(f"Aproximaciones intermedias: {aproximaciones}")
