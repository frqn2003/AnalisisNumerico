import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import numpy as np
import matplotlib.pyplot as plt
from sympy import sympify

from metodos_raices import biseccion, regula_falsi, newton, secante
from metodos_sistemas import gauss_seidel, jacobi, gauss_jordan

class AplicacionMetodosNumericos:
    def __init__(self, master):
        self.master = master
        master.title("Métodos Numéricos - MathWorks 2025")
        master.geometry("600x500")  # Tamaño inicial de la ventana

        # Selector de método numérico
        self.frame_selector = ttk.Frame(master, padding=10)
        self.frame_selector.pack(fill="x")

        ttk.Label(self.frame_selector, text="Seleccionar método:").pack(side="left")
        self.metodo_var = tk.StringVar()  # Variable para almacenar el método seleccionado
        self.metodo_menu = ttk.Combobox(self.frame_selector, textvariable=self.metodo_var, width=20)
        self.metodo_menu['values'] = ["Bisección", "Regula Falsi", "Newton", "Secante", 
                                       "Gauss-Seidel", "Jacobi", "Gauss-Jordan"]
        self.metodo_menu.current(0)  # Selecciona el primer método por defecto
        self.metodo_menu.pack(side="left", padx=5)

        # Vincular el cambio de método con la actualización de la interfaz
        self.metodo_var.trace_add("write", self.actualizar_interfaz)

        # Frame para métodos de búsqueda de raíces
        self.frame_funcion = ttk.LabelFrame(master, text="Búsqueda de Raíces", padding=10)

        ttk.Label(self.frame_funcion, text="Función f(x):").pack(anchor="w")
        self.entry_func = ttk.Entry(self.frame_funcion, width=50)
        self.entry_func.insert(0, "x**3 - x - 2")  # Valor por defecto
        self.entry_func.pack(fill="x", pady=5)

        self.lbl_a = ttk.Label(self.frame_funcion, text="a (extremo izquierdo):")
        self.lbl_a.pack(anchor="w")
        self.entry_a = ttk.Entry(self.frame_funcion, width=50)
        self.entry_a.insert(0, "1")  # Valor por defecto
        self.entry_a.pack(fill="x", pady=5)

        self.lbl_b = ttk.Label(self.frame_funcion, text="b (extremo derecho):")
        self.lbl_b.pack(anchor="w")
        self.entry_b = ttk.Entry(self.frame_funcion, width=50)
        self.entry_b.insert(0, "2")  # Valor por defecto
        self.entry_b.pack(fill="x", pady=5)

        # Frame para métodos de sistemas de ecuaciones
        self.frame_sistema = ttk.LabelFrame(master, text="Sistemas de Ecuaciones Lineales", padding=10)

        ttk.Label(self.frame_sistema, text="Matriz A (una fila por línea, elementos separados por espacios):").pack(anchor="w")
        self.txt_matriz = scrolledtext.ScrolledText(self.frame_sistema, width=50, height=6)
        self.txt_matriz.insert("1.0", "4 -1 0\n-1 4 -1\n0 -1 4")  # Ejemplo de matriz
        self.txt_matriz.pack(fill="x", pady=5)

        ttk.Label(self.frame_sistema, text="Vector b (elementos separados por espacios):").pack(anchor="w")
        self.txt_vector = scrolledtext.ScrolledText(self.frame_sistema, width=50, height=2)
        self.txt_vector.insert("1.0", "15 10 15")  # Ejemplo de vector
        self.txt_vector.pack(fill="x", pady=5)

        # Botón para ejecutar el cálculo
        ttk.Button(master, text="Resolver", command=self.resolver).pack(pady=20)

        # Mostrar la interfaz inicial
        self.actualizar_interfaz()

    def actualizar_interfaz(self, *args):
        """
        Actualiza la interfaz según el método seleccionado
        """
        metodo = self.metodo_var.get()
        
        # Ocultar todos los frames primero
        self.frame_funcion.pack_forget()
        self.frame_sistema.pack_forget()
        
        # Mostrar el frame correspondiente según el método
        if metodo in ["Bisección", "Regula Falsi", "Newton", "Secante"]:
            self.frame_funcion.pack(fill="both", expand=True, padx=10, pady=10)
            
            # Actualizar etiquetas según el método
            if metodo in ["Bisección", "Regula Falsi"]:
                self.lbl_a.config(text="a (extremo izquierdo):")
                self.lbl_b.config(text="b (extremo derecho):")
                self.entry_b.config(state="normal")
            elif metodo == "Newton":
                self.lbl_a.config(text="x0 (aproximación inicial):")
                self.lbl_b.config(text="No se usa:")
                self.entry_b.config(state="disabled")
            elif metodo == "Secante":
                self.lbl_a.config(text="x0 (primera aproximación):")
                self.lbl_b.config(text="x1 (segunda aproximación):")
                self.entry_b.config(state="normal")
        
        elif metodo in ["Gauss-Seidel", "Jacobi", "Gauss-Jordan"]:
            self.frame_sistema.pack(fill="both", expand=True, padx=10, pady=10)

    def resolver(self):
        """
        Función principal que se ejecuta al hacer clic en el botón "Resolver".
        Determina qué método usar según la selección del usuario y procesa los datos.
        """
        metodo = self.metodo_var.get()  # Obtiene el método seleccionado
        try:
            # Métodos para encontrar raíces de funciones
            if metodo in ["Bisección", "Regula Falsi", "Newton", "Secante"]:
                f = sympify(self.entry_func.get())  # Convierte el texto a una expresión simbólica
                
                if metodo == "Bisección":
                    a = float(self.entry_a.get())
                    b = float(self.entry_b.get())
                    res, pasos = biseccion(f, a, b)
                elif metodo == "Regula Falsi":
                    a = float(self.entry_a.get())
                    b = float(self.entry_b.get())
                    res, pasos = regula_falsi(f, a, b)
                elif metodo == "Newton":
                    x0 = float(self.entry_a.get())
                    res, pasos = newton(f, x0)
                elif metodo == "Secante":
                    x0 = float(self.entry_a.get())
                    x1 = float(self.entry_b.get())
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
                    A_text = self.txt_matriz.get("1.0", "end-1c").strip()
                    b_text = self.txt_vector.get("1.0", "end-1c").strip()
                    
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
                        ventana_pasos = tk.Toplevel(self.master)
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