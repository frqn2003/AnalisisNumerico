import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, diff, lambdify, sympify

# Definición de la variable simbólica x para las funciones matemáticas
x = symbols('x')

# ================= MÉTODOS NUMÉRICOS ====================

def biseccion(f, a, b, tol=1e-5, max_iter=100):
    """
    Método de Bisección para encontrar raíces de una función.
    
    Parámetros:
    - f: Función simbólica a evaluar
    - a, b: Extremos del intervalo inicial [a, b]
    - tol: Tolerancia para el criterio de parada
    - max_iter: Número máximo de iteraciones
    
    Retorna:
    - c: Aproximación de la raíz
    - pasos: Lista con las aproximaciones en cada iteración
    """
    fx = lambdify(x, f)  # Convierte la función simbólica a una función numérica
    pasos = []
    if fx(a) * fx(b) >= 0:
        raise ValueError("No hay cambio de signo en el intervalo")
    for i in range(max_iter):
        c = (a + b) / 2  # Punto medio del intervalo
        pasos.append(c)
        if abs(fx(c)) < tol or (b - a) / 2 < tol:
            return c, pasos  # Retorna si se alcanza la tolerancia
        if fx(a) * fx(c) < 0:
            b = c  # La raíz está en [a, c]
        else:
            a = c  # La raíz está en [c, b]
    return c, pasos

def regula_falsi(f, a, b, tol=1e-5, max_iter=100):
    """
    Método de Regula Falsi (Falsa Posición) para encontrar raíces.
    
    Parámetros:
    - f: Función simbólica a evaluar
    - a, b: Extremos del intervalo inicial [a, b]
    - tol: Tolerancia para el criterio de parada
    - max_iter: Número máximo de iteraciones
    
    Retorna:
    - c: Aproximación de la raíz
    - pasos: Lista con las aproximaciones en cada iteración
    """
    fx = lambdify(x, f)
    pasos = []
    if fx(a) * fx(b) >= 0:
        raise ValueError("No hay cambio de signo en el intervalo")
    for i in range(max_iter):
        # Cálculo del punto de intersección con el eje x
        c = b - fx(b)*(b - a)/(fx(b) - fx(a))
        pasos.append(c)
        if abs(fx(c)) < tol:
            return c, pasos
        if fx(a) * fx(c) < 0:
            b = c  # La raíz está en [a, c]
        else:
            a = c  # La raíz está en [c, b]
    return c, pasos

def newton(f, x0, tol=1e-5, max_iter=100):
    """
    Método de Newton-Raphson para encontrar raíces.
    
    Parámetros:
    - f: Función simbólica a evaluar
    - x0: Aproximación inicial
    - tol: Tolerancia para el criterio de parada
    - max_iter: Número máximo de iteraciones
    
    Retorna:
    - x1: Aproximación de la raíz
    - pasos: Lista con las aproximaciones en cada iteración
    """
    df = diff(f, x)  # Calcula la derivada de f respecto a x
    f_func = lambdify(x, f)  # Convierte la función simbólica a numérica
    df_func = lambdify(x, df)  # Convierte la derivada a función numérica
    pasos = [x0]
    for _ in range(max_iter):
        fx_val = f_func(x0)
        dfx_val = df_func(x0)
        if dfx_val == 0:
            raise ValueError("Derivada cero")
        # Fórmula de Newton: x_{n+1} = x_n - f(x_n)/f'(x_n)
        x1 = x0 - fx_val / dfx_val
        pasos.append(x1)
        if abs(x1 - x0) < tol:
            return x1, pasos
        x0 = x1
    return x0, pasos

def secante(f, x0, x1, tol=1e-5, max_iter=100):
    """
    Método de la Secante para encontrar raíces.
    
    Parámetros:
    - f: Función simbólica a evaluar
    - x0, x1: Dos aproximaciones iniciales
    - tol: Tolerancia para el criterio de parada
    - max_iter: Número máximo de iteraciones
    
    Retorna:
    - x2: Aproximación de la raíz
    - pasos: Lista con las aproximaciones en cada iteración
    """
    f_func = lambdify(x, f)
    pasos = [x0, x1]
    for _ in range(max_iter):
        if f_func(x1) - f_func(x0) == 0:
            raise ValueError("División por cero")
        # Fórmula del método de la secante
        x2 = x1 - f_func(x1)*(x1 - x0)/(f_func(x1) - f_func(x0))
        pasos.append(x2)
        if abs(x2 - x1) < tol:
            return x2, pasos
        x0, x1 = x1, x2  # Actualiza los valores para la siguiente iteración
    return x1, pasos

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
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    n = len(b)
    x = np.zeros(n) if x0 is None else np.array(x0, dtype=float)
    pasos = [x.copy()]
    
    # Verificar si la matriz es diagonalmente dominante
    for i in range(n):
        if abs(A[i, i]) <= sum(abs(A[i, j]) for j in range(n) if j != i):
            messagebox.showwarning("Advertencia", "La matriz no es diagonalmente dominante. El método puede no converger.")
            break
    
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
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    n = len(b)
    x = np.zeros(n) if x0 is None else np.array(x0, dtype=float)
    pasos = [x.copy()]
    
    # Verificar si la matriz es diagonalmente dominante
    for i in range(n):
        if abs(A[i, i]) <= sum(abs(A[i, j]) for j in range(n) if j != i):
            messagebox.showwarning("Advertencia", "La matriz no es diagonalmente dominante. El método puede no converger.")
            break
    
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
        if pivot == 0:
            raise ValueError("La matriz es singular, no se puede resolver con Gauss-Jordan")
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

# ================= INTERFAZ GRÁFICA ====================

def actualizar_interfaz(*args):
    """
    Actualiza la interfaz según el método seleccionado
    """
    metodo = metodo_var.get()
    
    # Ocultar todos los frames primero
    frame_funcion.pack_forget()
    frame_sistema.pack_forget()
    
    # Mostrar el frame correspondiente según el método
    if metodo in ["Bisección", "Regula Falsi", "Newton", "Secante"]:
        frame_funcion.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Actualizar etiquetas según el método
        if metodo in ["Bisección", "Regula Falsi"]:
            lbl_a.config(text="a (extremo izquierdo):")
            lbl_b.config(text="b (extremo derecho):")
            entry_b.config(state="normal")
        elif metodo == "Newton":
            lbl_a.config(text="x0 (aproximación inicial):")
            lbl_b.config(text="No se usa:")
            entry_b.config(state="disabled")
        elif metodo == "Secante":
            lbl_a.config(text="x0 (primera aproximación):")
            lbl_b.config(text="x1 (segunda aproximación):")
            entry_b.config(state="normal")
    
    elif metodo in ["Gauss-Seidel", "Jacobi", "Gauss-Jordan"]:
        frame_sistema.pack(fill="both", expand=True, padx=10, pady=10)

def resolver():
    """
    Función principal que se ejecuta al hacer clic en el botón "Resolver".
    Determina qué método usar según la selección del usuario y procesa los datos.
    """
    metodo = metodo_var.get()  # Obtiene el método seleccionado
    try:
        # Métodos para encontrar raíces de funciones
        if metodo in ["Bisección", "Regula Falsi", "Newton", "Secante"]:
            f = sympify(entry_func.get())  # Convierte el texto a una expresión simbólica
            
            if metodo == "Bisección":
                a = float(entry_a.get())
                b = float(entry_b.get())
                res, pasos = biseccion(f, a, b)
            elif metodo == "Regula Falsi":
                a = float(entry_a.get())
                b = float(entry_b.get())
                res, pasos = regula_falsi(f, a, b)
            elif metodo == "Newton":
                x0 = float(entry_a.get())
                res, pasos = newton(f, x0)
            elif metodo == "Secante":
                x0 = float(entry_a.get())
                x1 = float(entry_b.get())
                res, pasos = secante(f, x0, x1)
                
            # Visualización de la convergencia
            plt.figure(figsize=(8, 6))
            plt.plot(pasos, marker='o')
            plt.title(f"{metodo} - Convergencia")
            plt.xlabel("Iteración")
            plt.ylabel("Aproximación")
            plt.grid()
            plt.show()
            
            # Mostrar resultado
            messagebox.showinfo("Resultado", f"Raíz aproximada: {res:.6f}")

        # Métodos para resolver sistemas de ecuaciones lineales
        elif metodo in ["Gauss-Seidel", "Jacobi", "Gauss-Jordan"]:
            # Obtener matriz A y vector b del texto ingresado
            try:
                A_text = txt_matriz.get("1.0", "end-1c").strip()
                b_text = txt_vector.get("1.0", "end-1c").strip()
                
                # Convertir texto a matrices numpy
                A = np.array([list(map(float, row.split())) for row in A_text.strip().split('\n')])
                b = np.array([float(val) for val in b_text.strip().split()])
                
                # Verificar dimensiones
                if A.shape[0] != len(b):
                    raise ValueError(f"Dimensiones incompatibles: A es {A.shape[0]}x{A.shape[1]} pero b tiene {len(b)} elementos")
                
                if metodo == "Gauss-Seidel":
                    res, pasos = gauss_seidel(A, b)
                elif metodo == "Jacobi":
                    res, pasos = jacobi(A, b)
                elif metodo == "Gauss-Jordan":
                    res, pasos = gauss_jordan(A, b)
                
                # Mostrar resultado
                resultado = "Solución aproximada:\n"
                for i, val in enumerate(res):
                    resultado += f"x{i+1} = {val:.6f}\n"
                
                messagebox.showinfo("Resultado", resultado)
                
                # Para Gauss-Jordan, mostrar los pasos
                if metodo == "Gauss-Jordan":
                    ventana_pasos = tk.Toplevel(root)
                    ventana_pasos.title("Pasos del método Gauss-Jordan")
                    ventana_pasos.geometry("600x400")
                    
                    txt_pasos = scrolledtext.ScrolledText(ventana_pasos, width=60, height=20)
                    txt_pasos.pack(padx=10, pady=10, fill="both", expand=True)
                    
                    txt_pasos.insert(tk.END, "Pasos del método Gauss-Jordan:\n\n")
                    for i, paso in enumerate(pasos):
                        txt_pasos.insert(tk.END, f"Paso {i+1}:\n")
                        txt_pasos.insert(tk.END, str(paso) + "\n\n")
                    
                    txt_pasos.config(state="disabled")  # Hacer el texto de solo lectura
                
            except Exception as e:
                messagebox.showerror("Error en formato", f"Error al procesar la matriz o vector: {str(e)}\n\n"
                                    "Asegúrate de ingresar la matriz A como filas separadas por saltos de línea, "
                                    "con los elementos de cada fila separados por espacios.\n\n"
                                    "El vector b debe ser una lista de números separados por espacios.")
                return

    except Exception as e:
        # Captura y muestra cualquier error que ocurra
        messagebox.showerror("Error", str(e))

# Configuración de la ventana principal
root = tk.Tk()
root.title("Métodos Numéricos - MathWorks 2025")
root.geometry("600x500")  # Tamaño inicial de la ventana

# Selector de método numérico
frame_selector = ttk.Frame(root, padding=10)
frame_selector.pack(fill="x")

ttk.Label(frame_selector, text="Seleccionar método:").pack(side="left")
metodo_var = tk.StringVar()  # Variable para almacenar el método seleccionado
metodo_menu = ttk.Combobox(frame_selector, textvariable=metodo_var, width=20)
metodo_menu['values'] = ["Bisección", "Regula Falsi", "Newton", "Secante", "Gauss-Seidel", "Jacobi", "Gauss-Jordan"]
metodo_menu.current(0)  # Selecciona el primer método por defecto
metodo_menu.pack(side="left", padx=5)

# Vincular el cambio de método con la actualización de la interfaz
metodo_var.trace_add("write", actualizar_interfaz)

# Frame para métodos de búsqueda de raíces
frame_funcion = ttk.LabelFrame(root, text="Búsqueda de Raíces", padding=10)

ttk.Label(frame_funcion, text="Función f(x):").pack(anchor="w")
entry_func = ttk.Entry(frame_funcion, width=50)
entry_func.insert(0, "x**3 - x - 2")  # Valor por defecto
entry_func.pack(fill="x", pady=5)

lbl_a = ttk.Label(frame_funcion, text="a (extremo izquierdo):")
lbl_a.pack(anchor="w")
entry_a = ttk.Entry(frame_funcion, width=50)
entry_a.insert(0, "1")  # Valor por defecto
entry_a.pack(fill="x", pady=5)

lbl_b = ttk.Label(frame_funcion, text="b (extremo derecho):")
lbl_b.pack(anchor="w")
entry_b = ttk.Entry(frame_funcion, width=50)
entry_b.insert(0, "2")  # Valor por defecto
entry_b.pack(fill="x", pady=5)

# Frame para métodos de sistemas de ecuaciones
frame_sistema = ttk.LabelFrame(root, text="Sistemas de Ecuaciones Lineales", padding=10)

ttk.Label(frame_sistema, text="Matriz A (una fila por línea, elementos separados por espacios):").pack(anchor="w")
txt_matriz = scrolledtext.ScrolledText(frame_sistema, width=50, height=6)
txt_matriz.insert("1.0", "4 -1 0\n-1 4 -1\n0 -1 4")  # Ejemplo de matriz
txt_matriz.pack(fill="x", pady=5)

ttk.Label(frame_sistema, text="Vector b (elementos separados por espacios):").pack(anchor="w")
txt_vector = scrolledtext.ScrolledText(frame_sistema, width=50, height=2)
txt_vector.insert("1.0", "15 10 15")  # Ejemplo de vector
txt_vector.pack(fill="x", pady=5)

# Botón para ejecutar el cálculo
ttk.Button(root, text="Resolver", command=resolver).pack(pady=20)

# Mostrar la interfaz inicial
actualizar_interfaz()

# Inicia el bucle principal de la interfaz gráfica
root.mainloop()