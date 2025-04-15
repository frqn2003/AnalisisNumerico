import numpy as np

def newton(f, df, x0, tol=1e-6, max_iter=100):
    """
    Método de Newton-Raphson para encontrar raíces de ecuaciones.
    
    Parámetros:
    -----------
    f : función
        Función de la cual se busca la raíz
    df : función
        Derivada de la función f
    x0 : float
        Aproximación inicial de la raíz
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
    x = x0
    iteraciones = 0
    aproximaciones = [x0]
    
    while iteraciones < max_iter:
        # Calcular el valor de la función en el punto actual
        fx = f(x)
        
        if abs(fx) < tol:  # Si estamos suficientemente cerca de cero
            return x, iteraciones, aproximaciones
        
        # Calcular derivada en el punto actual
        derivada = df(x)
        
        # Verificar que la derivada no sea cero
        if abs(derivada) < 1e-10:
            raise ValueError(f"Derivada casi cero en x = {x}. El método de Newton no puede continuar.")
        
        # Calcular nueva aproximación
        x_nueva = x - fx / derivada
        aproximaciones.append(x_nueva)
        
        # Verificar convergencia
        if abs(x_nueva - x) < tol:
            return x_nueva, iteraciones + 1, aproximaciones
            
        x = x_nueva
        iteraciones += 1
    
    # Si se alcanza el máximo de iteraciones
    return x, iteraciones, aproximaciones

# Ejemplo de uso
if __name__ == "__main__":
    # Definir una función de ejemplo: f(x) = x^3 - x - 2
    def funcion_ejemplo(x):
        return x**3 - x - 2
    
    # Derivada de la función: f'(x) = 3x^2 - 1
    def derivada_ejemplo(x):
        return 3*x**2 - 1
    
    # Aproximación inicial x0 = 1.5
    raiz, iteraciones, aproximaciones = newton(funcion_ejemplo, derivada_ejemplo, 1.5)
    
    print(f"Raíz aproximada: {raiz}")
    print(f"Valor de la función en la raíz: {funcion_ejemplo(raiz)}")
    print(f"Iteraciones realizadas: {iteraciones}")
    print(f"Aproximaciones intermedias:")
    for i, aprox in enumerate(aproximaciones):
        print(f"  Iteración {i}: {aprox}")
