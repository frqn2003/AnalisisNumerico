import numpy as np
import re
from sympy import Symbol, sympify, denom, solve
from tkinter import messagebox

def validar_numero(valor, mensaje="Valor inválido"):
    """
    Valida que un string represente un número válido.
    
    Parámetros:
    - valor: String a validar
    - mensaje: Mensaje de error personalizado
    
    Retorna:
    - (bool, float): Tupla con un booleano indicando si es válido y el valor convertido
    """
    try:
        if not valor.strip():
            messagebox.showwarning("Advertencia", "El campo no puede estar vacío")
            return False, None
        
        num = float(valor)
        return True, num
    except ValueError:
        messagebox.showwarning("Advertencia", mensaje)
        return False, None

def validar_entero(valor, mensaje="Debe ingresar un número entero"):
    """
    Valida que un string represente un número entero válido.
    
    Parámetros:
    - valor: String a validar
    - mensaje: Mensaje de error personalizado
    
    Retorna:
    - (bool, int): Tupla con un booleano indicando si es válido y el valor convertido
    """
    try:
        if not valor.strip():
            messagebox.showwarning("Advertencia", "El campo no puede estar vacío")
            return False, None
        
        num = int(valor)
        return True, num
    except ValueError:
        messagebox.showwarning("Advertencia", mensaje)
        return False, None

def validar_intervalo(a, b, mensaje="El intervalo no es válido"):
    """
    Valida que a < b para un intervalo [a, b].
    
    Parámetros:
    - a, b: Límites del intervalo
    - mensaje: Mensaje de error personalizado
    
    Retorna:
    - bool: True si el intervalo es válido, False en caso contrario
    """
    if a >= b:
        messagebox.showwarning("Advertencia", mensaje)
        return False
    return True

def validar_expresion(expr_str):
    """
    Valida que una expresión matemática sea sintácticamente correcta.
    
    Parámetros:
    - expr_str: Expresión matemática como string
    
    Retorna:
    - (bool, sympy.Expr): Tupla con un booleano indicando si es válida y la expresión convertida
    """
    try:
        if not expr_str.strip():
            messagebox.showwarning("Advertencia", "La expresión no puede estar vacía")
            return False, None
        
        # Reemplazar notación de potencia ^ por **
        expr_str = expr_str.replace('^', '**')
        
        # Validar sintaxis básica
        x = Symbol('x')
        expr = sympify(expr_str)
        
        # Intentar evaluar en un punto para verificar que es calculable
        try:
            float(expr.subs(x, 1.0))
        except:
            messagebox.showwarning("Advertencia", "La expresión no puede evaluarse numéricamente")
            return False, None
        
        return True, expr
    except Exception as e:
        messagebox.showwarning("Advertencia", f"Error en la expresión: {e}")
        return False, None

def divisiones_por_cero(expr_str):
    """
    Verifica si una expresión puede tener divisiones por cero.
    
    Parámetros:
    - expr_str: Expresión matemática como string
    
    Retorna:
    - (bool, str): Tupla con un booleano indicando si hay divisiones por cero y un mensaje
    """
    x = Symbol('x')
    
    try:
        # Reemplazar notación de potencia ^ por **
        expr_str = expr_str.replace('^', '**')
        
        expr = sympify(expr_str)  # Convierte a expresión simbólica
        denominador = denom(expr)  # Extrae el denominador
        ceros = solve(denominador, x)  # Encuentra valores de x que hacen que se anule el denominador
        
        if ceros:
            return True, f"División por cero potencial en x = {ceros}"
        else:
            return False, "No hay división por cero detectada"
        
    except Exception as e:
        return True, f"Error al analizar la expresión: {e}"

def validar_divisiones_por_cero(expr_str, a=None, b=None):
    """
    Verifica si una expresión puede tener divisiones por cero en el intervalo [a, b].
    
    Parámetros:
    - expr_str: Expresión matemática como string
    - a, b: Límites del intervalo (opcional)
    
    Retorna:
    - (bool, str): Tupla con un booleano indicando si es válida y un mensaje
    """
    try:
        # Reemplazar notación de potencia ^ por **
        expr_str = expr_str.replace('^', '**')
        
        x = Symbol('x')
        expr = sympify(expr_str)
        denominador = denom(expr)
        
        # Si el denominador es 1, no hay división
        if denominador == 1:
            return True, "No hay divisiones en la expresión"
        
        # Encontrar valores que anulan el denominador
        ceros = solve(denominador, x)
        
        if not ceros:
            return True, "No hay divisiones por cero"
        
        # Si se proporciona un intervalo, verificar si los ceros están en él
        if a is not None and b is not None:
            ceros_en_intervalo = [float(cero) for cero in ceros 
                                 if cero.is_real and a <= float(cero) <= b]
            
            if ceros_en_intervalo:
                mensaje = f"La función tiene divisiones por cero en x = {ceros_en_intervalo} dentro del intervalo [{a}, {b}]"
                messagebox.showwarning("Advertencia", mensaje)
                return False, mensaje
            else:
                return True, "No hay divisiones por cero en el intervalo"
        else:
            mensaje = f"La función tiene divisiones por cero en x = {ceros}"
            messagebox.showwarning("Advertencia", mensaje)
            return False, mensaje
            
    except Exception as e:
        messagebox.showwarning("Advertencia", f"Error al analizar divisiones por cero: {e}")
        return False, str(e)

def validar_matriz_texto(texto_matriz):
    """
    Valida y convierte una matriz ingresada como texto.
    Formato esperado: filas separadas por punto y coma (;) y elementos por espacios o comas.
    
    Parámetros:
    - texto_matriz: String con la matriz
    
    Retorna:
    - (bool, numpy.ndarray): Tupla con un booleano indicando si es válida y la matriz convertida
    """
    try:
        if not texto_matriz.strip():
            messagebox.showwarning("Advertencia", "La matriz no puede estar vacía")
            return False, None
        
        # Dividir por filas (separadas por punto y coma)
        filas = texto_matriz.strip().split(';')
        matriz = []
        
        for fila in filas:
            # Reemplazar comas por espacios y dividir por espacios
            fila = fila.replace(',', ' ')
            elementos = re.split(r'\s+', fila.strip())
            
            # Filtrar elementos vacíos
            elementos = [e for e in elementos if e]
            
            if not elementos:
                continue
                
            # Convertir a números
            try:
                fila_numerica = [float(e) for e in elementos]
                matriz.append(fila_numerica)
            except ValueError:
                messagebox.showwarning("Advertencia", f"Valor no numérico en la fila: {fila}")
                return False, None
        
        if not matriz:
            messagebox.showwarning("Advertencia", "La matriz está vacía después de procesar")
            return False, None
            
        # Verificar que todas las filas tengan la misma longitud
        longitud = len(matriz[0])
        if not all(len(fila) == longitud for fila in matriz):
            messagebox.showwarning("Advertencia", "Todas las filas deben tener el mismo número de elementos")
            return False, None
            
        return True, np.array(matriz)
    except Exception as e:
        messagebox.showwarning("Advertencia", f"Error al procesar la matriz: {e}")
        return False, None

def validar_vector_texto(texto_vector):
    """
    Valida y convierte un vector ingresado como texto.
    Formato esperado: elementos separados por espacios o comas.
    
    Parámetros:
    - texto_vector: String con el vector
    
    Retorna:
    - (bool, numpy.ndarray): Tupla con un booleano indicando si es válido y el vector convertido
    """
    try:
        if not texto_vector.strip():
            messagebox.showwarning("Advertencia", "El vector no puede estar vacío")
            return False, None
        
        # Reemplazar comas por espacios y dividir
        texto_vector = texto_vector.replace(',', ' ')
        elementos = re.split(r'\s+', texto_vector.strip())
        
        # Filtrar elementos vacíos
        elementos = [e for e in elementos if e]
        
        if not elementos:
            messagebox.showwarning("Advertencia", "El vector está vacío después de procesar")
            return False, None
            
        # Convertir a números
        try:
            vector = np.array([float(e) for e in elementos])
            return True, vector
        except ValueError:
            messagebox.showwarning("Advertencia", "El vector contiene valores no numéricos")
            return False, None
    except Exception as e:
        messagebox.showwarning("Advertencia", f"Error al procesar el vector: {e}")
        return False, None

def validar_sistema_ecuaciones(A, b):
    """
    Valida un sistema de ecuaciones Ax = b.
    
    Parámetros:
    - A: Matriz de coeficientes (texto o numpy.ndarray)
    - b: Vector de términos independientes (texto o numpy.ndarray)
    
    Retorna:
    - (bool, numpy.ndarray, numpy.ndarray): Tupla con un booleano indicando si es válido, 
                                           la matriz A y el vector b convertidos
    """
    # Si A es texto, convertirlo a matriz
    if isinstance(A, str):
        valido, A = validar_matriz_texto(A)
        if not valido:
            return False, None, None
    
    # Si b es texto, convertirlo a vector
    if isinstance(b, str):
        valido, b = validar_vector_texto(b)
        if not valido:
            return False, None, None
    
    # Verificar dimensiones
    if A.shape[0] != len(b):
        messagebox.showwarning("Advertencia", 
                              f"Dimensiones incompatibles: A es {A.shape[0]}x{A.shape[1]} pero b tiene {len(b)} elementos")
        return False, None, None
    
    # Verificar si la matriz es singular
    try:
        if np.linalg.det(A) == 0:
            messagebox.showwarning("Advertencia", 
                                  "La matriz es singular (determinante = 0). El sistema puede no tener solución única.")
            return False, None, None
    except:
        messagebox.showwarning("Advertencia", "No se pudo calcular el determinante de la matriz")
        return False, None, None
    
    return True, A, b
