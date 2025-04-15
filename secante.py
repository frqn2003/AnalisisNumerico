import numpy as np

def secante(f, x0, x1, tol=1e-6, max_iter=100):
    """
    Método de la Secante para encontrar raíces de ecuaciones.
    
    Parámetros:
    -----------
    f : función
        Función de la cual se busca la raíz
    x0 : float
        Primera aproximación inicial
    x1 : float
        Segunda aproximación inicial
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
    iteraciones = 0
    aproximaciones = [x0, x1]
    
    while iteraciones < max_iter:
        f_x0 = f(x0)
        f_x1 = f(x1)
        
        # Verificar que la diferencia entre f(x1) y f(x0) no sea cero
        if abs(f_x1 - f_x0) < 1e-10:
            raise ValueError(f"La diferencia entre f({x1}) y f({x0}) es casi cero. El método de la Secante no puede continuar.")
        
        # Calcular nueva aproximación
        x2 = x1 - f_x1 * (x1 - x0) / (f_x1 - f_x0)
        aproximaciones.append(x2)
        
        # Verificar convergencia
        if abs(x2 - x1) < tol:
            return x2, iteraciones + 1, aproximaciones
            
        # Actualizar valores para la siguiente iteración
        x0 = x1
        x1 = x2
        iteraciones += 1
    
    # Si se alcanza el máximo de iteraciones
    return x1, iteraciones, aproximaciones

# Ejemplo de uso
if __name__ == "__main__":
    # Definir una función de ejemplo: f(x) = x^3 - x - 2
    def funcion_ejemplo(x):
        return x**3 - x - 2
    
    # Aproximaciones iniciales x0 = 1.0, x1 = 2.0
    raiz, iteraciones, aproximaciones = secante(funcion_ejemplo, 1.0, 2.0)
    
    print(f"Raíz aproximada: {raiz}")
    print(f"Iteraciones realizadas: {iteraciones}")
    print(f"Aproximaciones intermedias: {aproximaciones}")