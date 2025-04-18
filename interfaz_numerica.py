import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sympy import Symbol, sympify

# Importar los módulos de métodos numéricos
import metodos_sistemas as ms
import Validar_txt as vt

class AplicacionNumerica(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Métodos Numéricos")
        self.geometry("900x700")
        
        # Crear pestañas
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Pestaña para sistemas de ecuaciones
        self.tab_sistemas = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_sistemas, text="Sistemas de Ecuaciones")
        self.setup_tab_sistemas()
        
        # Aquí se pueden agregar más pestañas para otros métodos numéricos
        
    def setup_tab_sistemas(self):
        """Configura la pestaña de sistemas de ecuaciones"""
        frame = ttk.Frame(self.tab_sistemas, padding="10")
        frame.pack(fill='both', expand=True)
        
        # Frame para entrada de datos
        input_frame = ttk.LabelFrame(frame, text="Entrada de datos", padding="10")
        input_frame.pack(fill='x', pady=5)
        
        # Matriz A
        ttk.Label(input_frame, text="Matriz A (filas separadas por ; y elementos por espacios o comas):").grid(row=0, column=0, sticky='w', pady=5)
        self.txt_matriz_a = scrolledtext.ScrolledText(input_frame, width=40, height=5)
        self.txt_matriz_a.grid(row=1, column=0, padx=5, pady=5, sticky='w')
        
        # Vector b
        ttk.Label(input_frame, text="Vector b (elementos separados por espacios o comas):").grid(row=2, column=0, sticky='w', pady=5)
        self.txt_vector_b = ttk.Entry(input_frame, width=40)
        self.txt_vector_b.grid(row=3, column=0, padx=5, pady=5, sticky='w')
        
        # Vector inicial x0 (opcional)
        ttk.Label(input_frame, text="Vector inicial x0 (opcional):").grid(row=4, column=0, sticky='w', pady=5)
        self.txt_vector_x0 = ttk.Entry(input_frame, width=40)
        self.txt_vector_x0.grid(row=5, column=0, padx=5, pady=5, sticky='w')
        
        # Parámetros
        param_frame = ttk.Frame(input_frame)
        param_frame.grid(row=6, column=0, sticky='w', pady=5)
        
        ttk.Label(param_frame, text="Tolerancia:").grid(row=0, column=0, padx=5)
        self.txt_tolerancia = ttk.Entry(param_frame, width=10)
        self.txt_tolerancia.grid(row=0, column=1, padx=5)
        self.txt_tolerancia.insert(0, "1e-5")
        
        ttk.Label(param_frame, text="Máx. iteraciones:").grid(row=0, column=2, padx=5)
        self.txt_max_iter = ttk.Entry(param_frame, width=10)
        self.txt_max_iter.grid(row=0, column=3, padx=5)
        self.txt_max_iter.insert(0, "100")
        
        # Selección de método
        method_frame = ttk.Frame(input_frame)
        method_frame.grid(row=7, column=0, sticky='w', pady=10)
        
        ttk.Label(method_frame, text="Método:").grid(row=0, column=0, padx=5)
        self.metodo_var = tk.StringVar()
        metodos = ["Gauss-Jordan", "Gauss-Seidel", "Jacobi"]
        self.combo_metodo = ttk.Combobox(method_frame, textvariable=self.metodo_var, values=metodos, state="readonly", width=15)
        self.combo_metodo.grid(row=0, column=1, padx=5)
        self.combo_metodo.current(0)
        
        # Botón para resolver
        self.btn_resolver = ttk.Button(method_frame, text="Resolver", command=self.resolver_sistema)
        self.btn_resolver.grid(row=0, column=2, padx=20)
        
        # Frame para resultados
        result_frame = ttk.LabelFrame(frame, text="Resultados", padding="10")
        result_frame.pack(fill='both', expand=True, pady=10)
        
        # Área de texto para mostrar resultados
        self.txt_resultados = scrolledtext.ScrolledText(result_frame, width=80, height=15)
        self.txt_resultados.pack(fill='both', expand=True, padx=5, pady=5)
        
    def resolver_sistema(self):
        """Resuelve el sistema de ecuaciones según el método seleccionado"""
        try:
            # Validar y obtener la matriz A
            valido_a, matriz_a = vt.validar_matriz_texto(self.txt_matriz_a.get("1.0", "end-1c"))
            if not valido_a:
                return
            
            # Validar y obtener el vector b
            valido_b, vector_b = vt.validar_vector_texto(self.txt_vector_b.get())
            if not valido_b:
                return
            
            # Validar sistema
            valido_sistema, A, b = vt.validar_sistema_ecuaciones(matriz_a, vector_b)
            if not valido_sistema:
                return
            
            # Obtener parámetros adicionales
            valido_tol, tolerancia = vt.validar_numero(self.txt_tolerancia.get(), "La tolerancia debe ser un número")
            if not valido_tol:
                return
                
            valido_iter, max_iter = vt.validar_entero(self.txt_max_iter.get(), "El máximo de iteraciones debe ser un entero")
            if not valido_iter:
                return
            
            # Vector inicial (opcional)
            x0 = None
            if self.txt_vector_x0.get().strip():
                valido_x0, x0 = vt.validar_vector_texto(self.txt_vector_x0.get())
                if not valido_x0:
                    return
                
                # Verificar dimensiones de x0
                if len(x0) != A.shape[1]:
                    messagebox.showwarning("Advertencia", 
                                          f"Dimensiones incompatibles: x0 tiene {len(x0)} elementos pero debería tener {A.shape[1]}")
                    return
            
            # Resolver según el método seleccionado
            metodo = self.metodo_var.get()
            
            self.txt_resultados.delete("1.0", tk.END)
            self.txt_resultados.insert(tk.END, f"Resolviendo sistema con método: {metodo}\n\n")
            self.txt_resultados.insert(tk.END, f"Matriz A:\n{A}\n\n")
            self.txt_resultados.insert(tk.END, f"Vector b:\n{b}\n\n")
            
            if metodo == "Gauss-Jordan":
                solucion, pasos = ms.gauss_jordan(A, b)
                if solucion is not None:
                    self.mostrar_resultados_gauss_jordan(solucion, pasos)
            
            elif metodo == "Gauss-Seidel":
                solucion, pasos = ms.gauss_seidel(A, b, x0, tolerancia, max_iter)
                if solucion is not None:
                    self.mostrar_resultados_iterativos(solucion, pasos, "Gauss-Seidel")
            
            elif metodo == "Jacobi":
                solucion, pasos = ms.jacobi(A, b, x0, tolerancia, max_iter)
                if solucion is not None:
                    self.mostrar_resultados_iterativos(solucion, pasos, "Jacobi")
        
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")
            
    def mostrar_resultados_gauss_jordan(self, solucion, pasos):
        """Muestra los resultados del método de Gauss-Jordan"""
        self.txt_resultados.insert(tk.END, "Pasos del método de Gauss-Jordan:\n\n")
        
        for i, paso in enumerate(pasos):
            self.txt_resultados.insert(tk.END, f"Paso {i+1}:\n")
            self.txt_resultados.insert(tk.END, f"{paso}\n\n")
        
        self.txt_resultados.insert(tk.END, "Solución:\n")
        for i, val in enumerate(solucion):
            self.txt_resultados.insert(tk.END, f"x{i+1} = {val:.6f}\n")
    
    def mostrar_resultados_iterativos(self, solucion, pasos, metodo):
        """Muestra los resultados de métodos iterativos (Gauss-Seidel, Jacobi)"""
        self.txt_resultados.insert(tk.END, f"Iteraciones del método de {metodo}:\n\n")
        
        for i, paso in enumerate(pasos):
            self.txt_resultados.insert(tk.END, f"Iteración {i}:\n")
            self.txt_resultados.insert(tk.END, f"{paso}\n\n")
        
        self.txt_resultados.insert(tk.END, "Solución final:\n")
        for i, val in enumerate(solucion):
            self.txt_resultados.insert(tk.END, f"x{i+1} = {val:.6f}\n")
        
        self.txt_resultados.insert(tk.END, f"\nConvergencia alcanzada en {len(pasos)-1} iteraciones")

if __name__ == "__main__":
    app = AplicacionNumerica()
    app.mainloop()