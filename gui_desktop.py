
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sympy import Symbol, sympify

from metodos_raices import biseccion, regula_falsi, newton, secante
from metodos_sistemas import gauss_seidel, jacobi, gauss_jordan
import Validar_txt as vt

class AplicacionMetodosNumericos:
    def __init__(self, master):
        self.master = master
        master.title("MathWorks 2025 - Métodos Numéricos")
        master.geometry("1000x700")
        master.configure(bg="#f0f0f0")
        
        # Crear un marco principal con padding
        main_frame = tk.Frame(master, bg="#f0f0f0", padx=15, pady=15)
        main_frame.pack(fill='both', expand=True)
        
        # Título de la aplicación
        titulo_frame = tk.Frame(main_frame, bg="#f0f0f0")
        titulo_frame.pack(fill="x", pady=(0, 15))
        
        titulo_label = tk.Label(
            titulo_frame,
            text="Aplicación de Métodos Numéricos",
            font=("Arial", 18, "bold"),
            bg="#f0f0f0",
            fg="#2c3e50"
        )
        titulo_label.pack()
        
        subtitulo_label = tk.Label(
            titulo_frame,
            text="Sistemas de ecuaciones y búsqueda de raíces",
            font=("Arial", 12),
            bg="#f0f0f0",
            fg="#7f8c8d"
        )
        subtitulo_label.pack()
        
        # Crear notebook para las pestañas
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Pestaña para métodos de raíces
        self.tab_raices = tk.Frame(self.notebook, bg="#f5f5f5")
        self.notebook.add(self.tab_raices, text="Búsqueda de Raíces")
        
        # Pestaña para sistemas de ecuaciones
        self.tab_sistemas = tk.Frame(self.notebook, bg="#f5f5f5")
        self.notebook.add(self.tab_sistemas, text="Sistemas de Ecuaciones")
        
        # Pestaña de información
        self.tab_info = tk.Frame(self.notebook, bg="#f5f5f5")
        self.notebook.add(self.tab_info, text="Información")
        
        # Configurar las pestañas
        self.setup_tab_raices()
        self.setup_tab_sistemas()
        self.setup_tab_info()
        
        # Barra de estado
        self.status_bar = tk.Label(
            master, 
            text="Listo", 
            bd=1, 
            relief=tk.SUNKEN, 
            anchor=tk.W,
            bg="#e0e0e0",
            padx=10
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def setup_tab_raices(self):
        """Configura la pestaña de búsqueda de raíces"""
        # Panel principal dividido en dos
        panel_frame = tk.Frame(self.tab_raices, bg="#f5f5f5")
        panel_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Panel izquierdo para entrada de datos
        panel_izquierdo = tk.Frame(panel_frame, bg="#f5f5f5")
        panel_izquierdo.pack(side=tk.LEFT, fill='both', expand=True, padx=(0, 5))
        
        # Panel derecho para resultados
        panel_derecho = tk.Frame(panel_frame, bg="#f5f5f5")
        panel_derecho.pack(side=tk.RIGHT, fill='both', expand=True, padx=(5, 0))
        
        # ===== PANEL IZQUIERDO =====
        # Frame para selección de método
        metodo_frame = tk.LabelFrame(
            panel_izquierdo,
            text="Método",
            bg="#f5f5f5",
            fg="#2c3e50",
            font=("Arial", 11, "bold"),
            padx=10,
            pady=10
        )
        metodo_frame.pack(fill='x', pady=(0, 10))
        
        tk.Label(
            metodo_frame,
            text="Seleccionar método:",
            bg="#f5f5f5",
            fg="#2c3e50",
            font=("Arial", 10)
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        self.metodo_raices_var = tk.StringVar()
        metodos = ["Bisección", "Regula Falsi", "Newton", "Secante"]
        
        self.combo_metodo_raices = ttk.Combobox(
            metodo_frame,
            textvariable=self.metodo_raices_var,
            values=metodos,
            state="readonly",
            width=15,
            font=("Arial", 10)
        )
        self.combo_metodo_raices.pack(side=tk.LEFT, padx=5)
        self.combo_metodo_raices.current(0)
        
        # Vincular cambio de método
        self.combo_metodo_raices.bind("<<ComboboxSelected>>", self.actualizar_entradas_raices)
        
        # Frame para entrada de función
        funcion_frame = tk.LabelFrame(
            panel_izquierdo,
            text="Función",
            bg="#f5f5f5",
            fg="#2c3e50",
            font=("Arial", 11, "bold"),
            padx=10,
            pady=10
        )
        funcion_frame.pack(fill='x', pady=10)
        
        tk.Label(
            funcion_frame,
            text="Función f(x):",
            bg="#f5f5f5",
            fg="#2c3e50",
            font=("Arial", 10),
            anchor="w"
        ).pack(fill='x', pady=(0, 5))
        
        self.entry_funcion = tk.Entry(
            funcion_frame,
            font=("Courier New", 10),
            bg="white",
            fg="#2c3e50",
            relief="solid",
            bd=1
        )
        self.entry_funcion.pack(fill='x', pady=(0, 10))
        self.entry_funcion.insert(0, "x**3 - x - 2")  # Función de ejemplo
        
        # Frame para parámetros
        self.params_raices_frame = tk.LabelFrame(
            panel_izquierdo,
            text="Parámetros",
            bg="#f5f5f5",
            fg="#2c3e50",
            font=("Arial", 11, "bold"),
            padx=10,
            pady=10
        )
        self.params_raices_frame.pack(fill='x', pady=10)
        
        # Parámetro a
        self.lbl_a_frame = tk.Frame(self.params_raices_frame, bg="#f5f5f5")
        self.lbl_a_frame.pack(fill='x', pady=5)
        
        self.lbl_a = tk.Label(
            self.lbl_a_frame,
            text="a (extremo izquierdo):",
            bg="#f5f5f5",
            fg="#2c3e50",
            font=("Arial", 10),
            anchor="w"
        )
        self.lbl_a.pack(fill='x')
        
        self.entry_a = tk.Entry(
            self.lbl_a_frame,
            font=("Courier New", 10),
            bg="white",
            fg="#2c3e50",
            relief="solid",
            bd=1
        )
        self.entry_a.pack(fill='x', pady=(0, 5))
        self.entry_a.insert(0, "1")
        
        # Parámetro b
        self.lbl_b_frame = tk.Frame(self.params_raices_frame, bg="#f5f5f5")
        self.lbl_b_frame.pack(fill='x', pady=5)
        
        self.lbl_b = tk.Label(
            self.lbl_b_frame,
            text="b (extremo derecho):",
            bg="#f5f5f5",
            fg="#2c3e50",
            font=("Arial", 10),
            anchor="w"
        )
        self.lbl_b.pack(fill='x')
        
        self.entry_b = tk.Entry(
            self.lbl_b_frame,
            font=("Courier New", 10),
            bg="white",
            fg="#2c3e50",
            relief="solid",
            bd=1
        )
        self.entry_b.pack(fill='x', pady=(0, 5))
        self.entry_b.insert(0, "2")
        
        # Parámetros adicionales
        param_adicionales_frame = tk.Frame(self.params_raices_frame, bg="#f5f5f5")
        param_adicionales_frame.pack(fill='x', pady=5)
        
        tk.Label(
            param_adicionales_frame,
            text="Tolerancia:",
            bg="#f5f5f5",
            fg="#2c3e50",
            font=("Arial", 10)
        ).grid(row=0, column=0, padx=(0, 5), sticky="w")
        
        self.entry_tol_raices = tk.Entry(
            param_adicionales_frame,
            width=10,
            font=("Courier New", 10),
            bg="white",
            fg="#2c3e50",
            relief="solid",
            bd=1
        )
        self.entry_tol_raices.grid(row=0, column=1, padx=(0, 15))
        self.entry_tol_raices.insert(0, "1e-6")
        
        tk.Label(
            param_adicionales_frame,
            text="Máx. iteraciones:",
            bg="#f5f5f5",
            fg="#2c3e50",
            font=("Arial", 10)
        ).grid(row=0, column=2, padx=(0, 5), sticky="w")
        
        self.entry_max_iter_raices = tk.Entry(
            param_adicionales_frame,
            width=10,
            font=("Courier New", 10),
            bg="white",
            fg="#2c3e50",
            relief="solid",
            bd=1
        )
        self.entry_max_iter_raices.grid(row=0, column=3)
        self.entry_max_iter_raices.insert(0, "100")
        
        # Botón para resolver
        btn_frame = tk.Frame(panel_izquierdo, bg="#f5f5f5")
        btn_frame.pack(fill='x', pady=10)
        
        self.btn_resolver_raices = tk.Button(
            btn_frame,
            text="Calcular Raíz",
            command=self.resolver_raices,
            bg="#3498db",
            fg="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            padx=10,
            pady=5,
            cursor="hand2"
        )
        self.btn_resolver_raices.pack(side=tk.RIGHT)
        
        # Botones de ejemplo
        ejemplos_frame = tk.LabelFrame(
            panel_izquierdo,
            text="Ejemplos",
            bg="#f5f5f5",
            fg="#2c3e50",
            font=("Arial", 11, "bold"),
            padx=10,
            pady=3
        )
        ejemplos_frame.pack(fill='x', pady=10)
        
        tk.Button(
            ejemplos_frame,
            text="Función Polinómica",
            command=lambda: self.cargar_ejemplo_raiz(1),
            bg="#2ecc71",
            fg="white",
            font=("Arial", 9),
            relief="flat",
            padx=5,
            pady=1,
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=(0, 10), pady=2)
        
        tk.Button(
            ejemplos_frame,
            text="Función Trigonométrica",
            command=lambda: self.cargar_ejemplo_raiz(2),
            bg="#2ecc71",
            fg="white",
            font=("Arial", 9),
            relief="flat",
            padx=5,
            pady=1,
            cursor="hand2"
        ).pack(side=tk.LEFT, pady=2)
        
        # ===== PANEL DERECHO =====
        # Frame para resultados

        # Crear un frame contenedor para resultados y gráfico
        contenedor_frames = tk.Frame(panel_derecho, bg="#f5f5f5")
        contenedor_frames.pack(fill='both', expand=True)
        
        # Frame para resultados (mitad superior)
        resultados_frame = tk.LabelFrame(
            contenedor_frames,
            text="Resultados",
            bg="#f5f5f5",
            fg="#2c3e50",
            font=("Arial", 11, "bold"),
            padx=10,
            pady=10
        )
        resultados_frame.pack(fill='both', expand=True, pady=(0, 5))
        
        # Área de texto para mostrar resultados
        self.txt_resultados_raices = scrolledtext.ScrolledText(
            resultados_frame,
            width=45,
            height=10,  # Reducido para equilibrar con el gráfico
            font=("Courier New", 10),
            bg="white",
            fg="#2c3e50"
        )
        self.txt_resultados_raices.pack(fill='both', expand=True)
        
        # Frame para gráfico (mitad inferior)
        grafico_frame = tk.LabelFrame(
            contenedor_frames,
            text="Gráfico",
            bg="#f5f5f5",
            fg="#2c3e50",
            font=("Arial", 11, "bold"),
            padx=10,
            pady=10
        )
        grafico_frame.pack(fill='both', expand=True, pady=(5, 0))
        
        # Contenedor para el gráfico de matplotlib
        self.fig_raices = plt.Figure(dpi=100)
        self.ax_raices = self.fig_raices.add_subplot(111)
        self.canvas_raices = FigureCanvasTkAgg(self.fig_raices, grafico_frame)
        self.canvas_raices.get_tk_widget().pack(fill='both', expand=True)
        
        # Inicializar la interfaz
        self.actualizar_entradas_raices(None)

    def setup_tab_sistemas(self):
        """Configura la pestaña de sistemas de ecuaciones"""
        # Dividir en dos paneles
        panel_izquierdo = tk.Frame(self.tab_sistemas, bg="#f5f5f5")
        panel_izquierdo.pack(side=tk.LEFT, fill='both', expand=True, padx=10, pady=10)
        
        panel_derecho = tk.Frame(self.tab_sistemas, bg="#f5f5f5")
        panel_derecho.pack(side=tk.RIGHT, fill='both', expand=True, padx=10, pady=10)
        
        # Panel izquierdo: entrada de datos
        entrada_frame = tk.LabelFrame(
            panel_izquierdo, 
            text="Entrada de datos", 
            bg="#f5f5f5",
            fg="#2c3e50",
            font=("Arial", 11, "bold"),
            padx=10,
            pady=10
        )
        entrada_frame.pack(fill='both', expand=True)
        
        # Matriz A
        tk.Label(
            entrada_frame, 
            text="Matriz A (filas separadas por ; y elementos por espacios o comas):",
            bg="#f5f5f5",
            fg="#2c3e50",
            font=("Arial", 10),
            anchor="w"
        ).pack(fill='x', pady=(10, 5))
        
        self.txt_matriz_a = scrolledtext.ScrolledText(
            entrada_frame, 
            width=40, 
            height=6,
            font=("Courier New", 10),
            bg="white",
            fg="#2c3e50"
        )
        self.txt_matriz_a.pack(fill='x', pady=(0, 10))
        
        # Vector b
        tk.Label(
            entrada_frame, 
            text="Vector b (elementos separados por espacios o comas):",
            bg="#f5f5f5",
            fg="#2c3e50",
            font=("Arial", 10),
            anchor="w"
        ).pack(fill='x', pady=(5, 5))
        
        self.txt_vector_b = tk.Entry(
            entrada_frame, 
            font=("Courier New", 10),
            bg="white",
            fg="#2c3e50",
            relief="solid",
            bd=1
        )
        self.txt_vector_b.pack(fill='x', pady=(0, 10))
        
        # Vector inicial x0
        tk.Label(
            entrada_frame, 
            text="Vector inicial x0 (opcional):",
            bg="#f5f5f5",
            fg="#2c3e50",
            font=("Arial", 10),
            anchor="w"
        ).pack(fill='x', pady=(5, 5))
        
        self.txt_vector_x0 = tk.Entry(
            entrada_frame, 
            font=("Courier New", 10),
            bg="white",
            fg="#2c3e50",
            relief="solid",
            bd=1
        )
        self.txt_vector_x0.pack(fill='x', pady=(0, 10))
        
        # Parámetros
        param_frame = tk.Frame(entrada_frame, bg="#f5f5f5")
        param_frame.pack(fill='x', pady=5)
        
        tk.Label(
            param_frame, 
            text="Tolerancia:",
            bg="#f5f5f5",
            fg="#2c3e50",
            font=("Arial", 10)
        ).grid(row=0, column=0, padx=(0, 5), sticky="w")
        
        self.txt_tolerancia = tk.Entry(
            param_frame, 
            width=10, 
            font=("Courier New", 10),
            bg="white",
            fg="#2c3e50",
            relief="solid",
            bd=1
        )
        self.txt_tolerancia.grid(row=0, column=1, padx=(0, 15))
        self.txt_tolerancia.insert(0, "1e-5")
        
        tk.Label(
            param_frame, 
            text="Máx. iteraciones:",
            bg="#f5f5f5",
            fg="#2c3e50",
            font=("Arial", 10)
        ).grid(row=0, column=2, padx=(0, 5), sticky="w")
        
        self.txt_max_iter = tk.Entry(
            param_frame, 
            width=10, 
            font=("Courier New", 10),
            bg="white",
            fg="#2c3e50",
            relief="solid",
            bd=1
        )
        self.txt_max_iter.grid(row=0, column=3)
        self.txt_max_iter.insert(0, "100")
        
        # Selección de método
        method_frame = tk.Frame(entrada_frame, bg="#f5f5f5")
        method_frame.pack(fill='x', pady=10)
        
        tk.Label(
            method_frame, 
            text="Método:",
            bg="#f5f5f5",
            fg="#2c3e50",
            font=("Arial", 10)
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        self.metodo_var = tk.StringVar()
        metodos = ["Gauss-Jordan", "Gauss-Seidel", "Jacobi"]
        
        self.combo_metodo = ttk.Combobox(
            method_frame, 
            textvariable=self.metodo_var,
            values=metodos, 
            state="readonly", 
            width=15,
            font=("Arial", 10)
        )
        self.combo_metodo.pack(side=tk.LEFT, padx=5)
        self.combo_metodo.current(0)
        
        # Botón para resolver
        self.btn_resolver = tk.Button(
            method_frame, 
            text="Resolver Sistema",
            command=self.resolver_sistema,
            bg="#3498db",  # Azul
            fg="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            padx=10,
            pady=5,
            cursor="hand2"
        )
        self.btn_resolver.pack(side=tk.RIGHT, padx=5)
        
        # Botones de ejemplo
        ejemplos_frame = tk.LabelFrame(
            panel_izquierdo, 
            text="Ejemplos",
            bg="#f5f5f5", 
            fg="#2c3e50",
            font=("Arial", 11, "bold"),
            padx=10,
            pady=5
        )
        ejemplos_frame.pack(fill='x', pady=10)
        
        tk.Button(
            ejemplos_frame,
            text="Ejemplo 1: Sistema 3x3",
            command=self.cargar_ejemplo1,
            bg="#2ecc71",  # Verde
            fg="white",
            font=("Arial", 9),
            relief="flat",
            padx=5,
            pady=3,
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=(0, 10), pady=5)
        
        tk.Button(
            ejemplos_frame,
            text="Ejemplo 2: Para Métodos Iterativos",
            command=self.cargar_ejemplo2,
            bg="#2ecc71",  # Verde
            fg="white",
            font=("Arial", 9),
            relief="flat",
            padx=5,
            pady=3,
            cursor="hand2"
        ).pack(side=tk.LEFT, pady=5)
        
        # Panel derecho: resultados
        resultados_frame = tk.LabelFrame(
            panel_derecho, 
            text="Resultados", 
            bg="#f5f5f5",
            fg="#2c3e50",
            font=("Arial", 11, "bold"),
            padx=10,
            pady=10
        )
        resultados_frame.pack(fill='both', expand=True)
        
        # Área de texto para mostrar resultados
        self.txt_resultados = scrolledtext.ScrolledText(
            resultados_frame, 
            width=45, 
            height=25,
            font=("Courier New", 10),
            bg="white",
            fg="#2c3e50"
        )
        self.txt_resultados.pack(fill='both', expand=True, pady=5)
    
    def setup_tab_info(self):
        # Frame principal
        main_frame = tk.Frame(self.tab_info, bg="#f5f5f5")
        main_frame.pack(fill='both', expand=True)
        
        # Crear un canvas con scrollbar
        canvas = tk.Canvas(main_frame, bg="#f5f5f5", highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#f5f5f5")
        
        # Configurar el frame para que actualice el scrollregion cuando cambie su tamaño
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        # Crear ventana dentro del canvas que contendrá el frame scrollable
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Empaquetar canvas y scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Permitir scroll con la rueda del mouse
        canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(int(-1*(event.delta/120)), "units"))
        
        # Configurar el canvas para expandirse con la ventana
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)
        
        # Contenedor centrado para el contenido
        contenedor_centrado = tk.Frame(scrollable_frame, bg="#f5f5f5")
        contenedor_centrado.pack(fill='both', expand=True, padx=50)  # Padding horizontal para centrar
        
        # Contenido de la pestaña (ahora dentro del contenedor centrado)
        info_frame = tk.Frame(contenedor_centrado, bg="#f5f5f5", padx=20, pady=20)
        info_frame.pack(fill='both', expand=True)
        
        # Título
        titulo_frame = tk.Frame(info_frame, bg="#f5f5f5")
        titulo_frame.pack(fill='x', expand=True)
        
        tk.Label(
            titulo_frame,
            text="MathWorks 2025",
            font=("Arial", 18, "bold"),
            bg="#f5f5f5",
            fg="#2c3e50"
        ).pack(pady=(0, 5))
        
        tk.Label(
            titulo_frame,
            text="Aplicación de Métodos Numéricos",
            font=("Arial", 14, "bold"),
            bg="#f5f5f5",
            fg="#2c3e50"
        ).pack(pady=(0, 15))
        
        # Descripción general
        descripcion_frame = tk.LabelFrame(
            info_frame,
            text="Descripción",
            bg="#f5f5f5",
            fg="#2c3e50",
            font=("Arial", 11, "bold"),
            padx=15,
            pady=10
        )
        descripcion_frame.pack(fill='x', pady=5)
        
        descripcion_texto = """
Esta aplicación implementa diversos métodos numéricos para la resolución de problemas matemáticos:

• Búsqueda de raíces de funciones: Bisección, Regula Falsi, Newton y Secante
• Resolución de sistemas de ecuaciones lineales: Gauss-Jordan, Gauss-Seidel y Jacobi

Cada método posee características particulares que los hacen más adecuados para distintos tipos de problemas.
        """
        
        tk.Label(
            descripcion_frame,
            text=descripcion_texto,
            font=("Arial", 10),
            bg="#f5f5f5",
            fg="#2c3e50",
            justify="left",
            anchor="w"
        ).pack(fill='x')
        
        # Descripción de métodos de raíces
        metodos_raices_frame = tk.LabelFrame(
            info_frame,
            text="Métodos para búsqueda de raíces",
            bg="#f5f5f5",
            fg="#2c3e50",
            font=("Arial", 11, "bold"),
            padx=15,
            pady=10
        )
        metodos_raices_frame.pack(fill='x', pady=10)
        
        # Configurar grid para que se expanda
        metodos_raices_frame.columnconfigure(1, weight=1)
        
        metodos_raices_info = [
            ("Bisección", "Divide repetidamente el intervalo a la mitad y selecciona el subintervalo donde la función cambia de signo."),
            ("Regula Falsi", "Similar a bisección, pero usa interpolación lineal para estimar la raíz."),
            ("Newton", "Utiliza la derivada de la función para aproximarse rápidamente a la raíz."),
            ("Secante", "Similar a Newton, pero aproxima la derivada usando dos puntos anteriores.")
        ]
        
        for i, (nombre, desc) in enumerate(metodos_raices_info):
            tk.Label(
                metodos_raices_frame,
                text=nombre,
                font=("Arial", 10, "bold"),
                bg="#f5f5f5",
                fg="#2c3e50",
                anchor="w"
            ).grid(row=i, column=0, sticky="w", pady=5)
            
            tk.Label(
                metodos_raices_frame,
                text=desc,
                font=("Arial", 10),
                bg="#f5f5f5",
                fg="#2c3e50",
                anchor="w",
                justify="left",
                wraplength=600  # Aumentado para mejor adaptación
            ).grid(row=i, column=1, sticky="ew", padx=10, pady=5)
        
        # Descripción de métodos de sistemas
        metodos_sistemas_frame = tk.LabelFrame(
            info_frame,
            text="Métodos para sistemas de ecuaciones",
            bg="#f5f5f5",
            fg="#2c3e50",
            font=("Arial", 11, "bold"),
            padx=15,
            pady=10
        )
        metodos_sistemas_frame.pack(fill='x', pady=10)
        
        # Configurar grid para que se expanda
        metodos_sistemas_frame.columnconfigure(1, weight=1)
        
        metodos_sistemas_info = [
            ("Gauss-Jordan", "Método directo que transforma la matriz aumentada en una forma escalonada reducida."),
            ("Gauss-Seidel", "Método iterativo que actualiza cada componente usando los valores más recientes."),
            ("Jacobi", "Método iterativo que calcula nuevos valores basados en los valores de la iteración anterior.")
        ]
        
        for i, (nombre, desc) in enumerate(metodos_sistemas_info):
            tk.Label(
                metodos_sistemas_frame,
                text=nombre,
                font=("Arial", 10, "bold"),
                bg="#f5f5f5",
                fg="#2c3e50",
                anchor="w"
            ).grid(row=i, column=0, sticky="w", pady=5)
            
            tk.Label(
                metodos_sistemas_frame,
                text=desc,
                font=("Arial", 10),
                bg="#f5f5f5",
                fg="#2c3e50",
                anchor="w",
                justify="left",
                wraplength=600  # Aumentado para mejor adaptación
            ).grid(row=i, column=1, sticky="ew", padx=10, pady=5)
        
        # Pie de página
        footer_frame = tk.Frame(info_frame, bg="#f5f5f5")
        footer_frame.pack(fill='x', pady=10)
        
        tk.Label(
            footer_frame,
            text="Desarrollado para el curso de Análisis Numérico",
            font=("Arial", 10, "italic"),
            bg="#f5f5f5",
            fg="#7f8c8d"
        ).pack()    # ===== MÉTODOS PARA BÚSQUEDA DE RAÍCES =====
    def actualizar_entradas_raices(self, event):
        """Actualiza la interfaz de parámetros según el método seleccionado"""
        metodo = self.metodo_raices_var.get()
        
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
    

    def cargar_ejemplo_raiz(self, num_ejemplo):
        """Carga ejemplos predefinidos para búsqueda de raíces"""
        if num_ejemplo == 1:
        # Ejemplo de función polinómica
            self.entry_funcion.delete(0, tk.END)
            self.entry_funcion.insert(0, "x**3 - x - 2")
            self.entry_a.delete(0, tk.END)
            self.entry_a.insert(0, "1")
            self.entry_b.delete(0, tk.END)
            self.entry_b.insert(0, "2")
            self.combo_metodo_raices.set("Bisección")
            self.actualizar_entradas_raices(None)
            self.status_bar.config(text="Ejemplo polinómico cargado: f(x) = x³ - x - 2")
        
        elif num_ejemplo == 2:
        # Ejemplo de función trigonométrica
            self.entry_funcion.delete(0, tk.END)
            self.entry_funcion.insert(0, "sin(x) - x/2")
            self.entry_a.delete(0, tk.END)
            self.entry_a.insert(0, "0")
            self.entry_b.delete(0, tk.END)
            self.entry_b.insert(0, "2")
            self.combo_metodo_raices.set("Regula Falsi")
            self.actualizar_entradas_raices(None)
            self.status_bar.config(text="Ejemplo trigonométrico cargado: f(x) = sin(x) - x/2")

    def cargar_ejemplo1(self):
        """Carga un ejemplo básico de sistema 3x3"""
        self.txt_matriz_a.delete("1.0", tk.END)
        self.txt_vector_b.delete(0, tk.END)
        self.txt_vector_x0.delete(0, tk.END)
        
        self.txt_matriz_a.insert("1.0", "2 1 -1;\n-3 -1 2;\n-2 1 2")
        self.txt_vector_b.insert(0, "8 -11 -3")
        self.metodo_var.set("Gauss-Jordan")
        
        self.status_bar.config(text="Ejemplo 1 cargado: Sistema 3x3 para Gauss-Jordan")
        
    def cargar_ejemplo2(self):
        """Carga un ejemplo adecuado para métodos iterativos"""
        self.txt_matriz_a.delete("1.0", tk.END)
        self.txt_vector_b.delete(0, tk.END)
        self.txt_vector_x0.delete(0, tk.END)
        
        self.txt_matriz_a.insert("1.0", "10 -1 2;\n-1 11 -1;\n2 -1 10")
        self.txt_vector_b.insert(0, "6 25 -11")
        self.txt_vector_x0.insert(0, "0 0 0")
        self.metodo_var.set("Gauss-Seidel")
        
        self.status_bar.config(text="Ejemplo 2 cargado: Sistema para métodos iterativos")

    def resolver_raices(self):
        """Resuelve una ecuación para encontrar sus raíces usando el método seleccionado"""
        try:
            self.status_bar.config(text="Calculando raíz...")
            self.master.update_idletasks()
            
            # Obtener función y convertirla a expresión simbólica
            f_str = self.entry_funcion.get().strip()
            if not f_str:
                messagebox.showerror("Error", "La función no puede estar vacía")
                self.status_bar.config(text="Error: Función vacía")
                return
            
            try:
                x = Symbol('x')
                f = sympify(f_str)
            except Exception as e:
                messagebox.showerror("Error", f"Error al analizar la función: {e}")
                self.status_bar.config(text="Error en la función")
                return
            
            # Obtener parámetros adicionales
            try:
                tol = float(self.entry_tol_raices.get())
                max_iter = int(self.entry_max_iter_raices.get())
            except ValueError:
                messagebox.showerror("Error", "La tolerancia y el máximo de iteraciones deben ser números")
                self.status_bar.config(text="Error en los parámetros")
                return
            
            # Obtener método y parámetros específicos
            metodo = self.metodo_raices_var.get()
            
            # Limpiar resultados anteriores
            self.txt_resultados_raices.delete("1.0", tk.END)
            self.ax_raices.clear()
            
            # Resolver según el método seleccionado
            if metodo == "Bisección":
                try:
                    a = float(self.entry_a.get())
                    b = float(self.entry_b.get())
                    
                    self.txt_resultados_raices.insert(tk.END, f"Método de Bisección\n")
                    self.txt_resultados_raices.insert(tk.END, f"Función: {f_str}\n")
                    self.txt_resultados_raices.insert(tk.END, f"Intervalo: [{a}, {b}]\n")
                    self.txt_resultados_raices.insert(tk.END, f"Tolerancia: {tol}\n")
                    self.txt_resultados_raices.insert(tk.END, f"Máximo de iteraciones: {max_iter}\n\n")
                    
                    raiz, pasos = biseccion(f, a, b, tol, max_iter)
                    self._mostrar_resultados_raiz(raiz, pasos, f)
                except Exception as e:
                    messagebox.showerror("Error", f"Error al ejecutar el método: {e}")
                    self.status_bar.config(text=f"Error: {str(e)}")
            
            elif metodo == "Regula Falsi":
                try:
                    a = float(self.entry_a.get())
                    b = float(self.entry_b.get())
                    
                    self.txt_resultados_raices.insert(tk.END, f"Método de Regula Falsi\n")
                    self.txt_resultados_raices.insert(tk.END, f"Función: {f_str}\n")
                    self.txt_resultados_raices.insert(tk.END, f"Intervalo: [{a}, {b}]\n")
                    self.txt_resultados_raices.insert(tk.END, f"Tolerancia: {tol}\n")
                    self.txt_resultados_raices.insert(tk.END, f"Máximo de iteraciones: {max_iter}\n\n")
                    
                    raiz, pasos = regula_falsi(f, a, b, tol, max_iter)
                    self._mostrar_resultados_raiz(raiz, pasos, f)
                except Exception as e:
                    messagebox.showerror("Error", f"Error al ejecutar el método: {e}")
                    self.status_bar.config(text=f"Error: {str(e)}")
            
            elif metodo == "Newton":
                try:
                    x0 = float(self.entry_a.get())
                    
                    self.txt_resultados_raices.insert(tk.END, f"Método de Newton\n")
                    self.txt_resultados_raices.insert(tk.END, f"Función: {f_str}\n")
                    self.txt_resultados_raices.insert(tk.END, f"Aproximación inicial: {x0}\n")
                    self.txt_resultados_raices.insert(tk.END, f"Tolerancia: {tol}\n")
                    self.txt_resultados_raices.insert(tk.END, f"Máximo de iteraciones: {max_iter}\n\n")
                    
                    raiz, pasos = newton(f, x0, tol, max_iter)
                    self._mostrar_resultados_raiz(raiz, pasos, f)
                except Exception as e:
                    messagebox.showerror("Error", f"Error al ejecutar el método: {e}")
                    self.status_bar.config(text=f"Error: {str(e)}")
            
            elif metodo == "Secante":
                try:
                    x0 = float(self.entry_a.get())
                    x1 = float(self.entry_b.get())
                    
                    self.txt_resultados_raices.insert(tk.END, f"Método de la Secante\n")
                    self.txt_resultados_raices.insert(tk.END, f"Función: {f_str}\n")
                    self.txt_resultados_raices.insert(tk.END, f"Primera aproximación: {x0}\n")
                    self.txt_resultados_raices.insert(tk.END, f"Segunda aproximación: {x1}\n")
                    self.txt_resultados_raices.insert(tk.END, f"Tolerancia: {tol}\n")
                    self.txt_resultados_raices.insert(tk.END, f"Máximo de iteraciones: {max_iter}\n\n")
                    
                    raiz, pasos = secante(f, x0, x1, tol, max_iter)
                    self._mostrar_resultados_raiz(raiz, pasos, f)
                except Exception as e:
                    messagebox.showerror("Error", f"Error al ejecutar el método: {e}")
                    self.status_bar.config(text=f"Error: {str(e)}")
        
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {e}")
            self.status_bar.config(text="Error inesperado")

    def _mostrar_resultados_raiz(self, raiz, pasos, f):
        """Muestra los resultados de los métodos de búsqueda de raíces"""
        if raiz is None:
            self.txt_resultados_raices.insert(tk.END, "El método no pudo encontrar una raíz.\n")
            self.status_bar.config(text="No se encontró raíz")
            return
        
        # Mostrar pasos
        self.txt_resultados_raices.insert(tk.END, "ITERACIONES:\n")
        for i, paso in enumerate(pasos):
            self.txt_resultados_raices.insert(tk.END, f"Iteración {i+1}: x = {paso:.8f}\n")
        
        # Mostrar resultado final
        self.txt_resultados_raices.insert(tk.END, "\nRESULTADO FINAL:\n")
        self.txt_resultados_raices.insert(tk.END, f"Raíz aproximada: {raiz:.8f}\n")
        
        x = Symbol('x')
        f_val = float(f.subs(x, raiz))
        self.txt_resultados_raices.insert(tk.END, f"f({raiz:.8f}) = {f_val:.8e}\n")
        self.txt_resultados_raices.insert(tk.END, f"Número de iteraciones: {len(pasos)}\n")
        
        # Graficar la función y la raíz
        self._graficar_funcion(f, raiz, pasos)
        
        self.status_bar.config(text=f"Raíz encontrada: {raiz:.8f}")

    def _graficar_funcion(self, f, raiz, pasos):
        """Grafica la función y la raíz encontrada"""
        try:
            # Limpiar gráfico anterior
            self.ax_raices.clear()
            
            # Definir rango para graficar
            margen = max(1.0, abs(raiz) * 0.5)
            x_min = raiz - margen
            x_max = raiz + margen
            
            # Crear puntos para la gráfica
            x = Symbol('x')
            x_vals = np.linspace(x_min, x_max, 100)
            f_num = lambda val: float(f.subs(x, val))
            y_vals = [f_num(val) for val in x_vals]
            
            # Graficar función
            self.ax_raices.plot(x_vals, y_vals, 'b-', label='f(x)')
            
            # Graficar eje x
            self.ax_raices.axhline(y=0, color='k', linestyle='-', alpha=0.3)
            
            # Marcar la raíz
            self.ax_raices.plot([raiz], [0], 'ro', markersize=8, label=f'Raíz: {raiz:.6f}')
            
            # Graficar evolución de las aproximaciones
            if len(pasos) > 0:
                pasos_x = list(range(1, len(pasos) + 1))
                pasos_y = pasos
                
                # Crear un segundo eje para las iteraciones
                ax2 = self.ax_raices.twinx()
                ax2.plot(pasos_x, pasos_y, 'g-o', alpha=0.7, label='Convergencia')
                ax2.set_ylabel('Valor de x')
                ax2.tick_params(axis='y', labelcolor='g')
            
            # Configurar gráfico
            self.ax_raices.set_xlabel('x')
            self.ax_raices.set_ylabel('f(x)')
            self.ax_raices.set_title('Gráfica de la función y su raíz')
            self.ax_raices.grid(True, alpha=0.3)
            self.ax_raices.legend(loc='best')
            
            # Actualizar gráfico
            self.fig_raices.tight_layout()
            self.canvas_raices.draw()
            
        except Exception as e:
            print(f"Error al graficar: {e}")

    def resolver_sistema(self):
        """Resuelve el sistema de ecuaciones según el método seleccionado"""
        try:
            self.status_bar.config(text="Resolviendo sistema...")
            self.master.update_idletasks()
            
            # Validar y obtener la matriz A
            valido_a, matriz_a = vt.validar_matriz_texto(self.txt_matriz_a.get("1.0", "end-1c"))
            if not valido_a:
                self.status_bar.config(text="Error en el formato de la matriz A")
                return
            
            # Validar y obtener el vector b
            valido_b, vector_b = vt.validar_vector_texto(self.txt_vector_b.get())
            if not valido_b:
                self.status_bar.config(text="Error en el formato del vector b")
                return
            
            # Validar sistema
            valido_sistema, A, b = vt.validar_sistema_ecuaciones(matriz_a, vector_b)
            if not valido_sistema:
                self.status_bar.config(text="Error en el sistema de ecuaciones")
                return
            
            # Obtener parámetros adicionales
            valido_tol, tolerancia = vt.validar_numero(self.txt_tolerancia.get(), "La tolerancia debe ser un número")
            if not valido_tol:
                self.status_bar.config(text="Error en el valor de tolerancia")
                return
                
            valido_iter, max_iter = vt.validar_entero(self.txt_max_iter.get(), "El máximo de iteraciones debe ser un entero")
            if not valido_iter:
                self.status_bar.config(text="Error en el número máximo de iteraciones")
                return
            
            # Vector inicial (opcional)
            x0 = None
            if self.txt_vector_x0.get().strip():
                valido_x0, x0 = vt.validar_vector_texto(self.txt_vector_x0.get())
                if not valido_x0:
                    self.status_bar.config(text="Error en el formato del vector inicial x0")
                    return
                
                # Verificar dimensiones de x0
                if len(x0) != A.shape[1]:
                    messagebox.showwarning("Advertencia", 
                                        f"Dimensiones incompatibles: x0 tiene {len(x0)} elementos pero debería tener {A.shape[1]}")
                    self.status_bar.config(text="Error: dimensiones incompatibles del vector x0")
                    return
            
            # Resolver según el método seleccionado
            metodo = self.metodo_var.get()
            
            self.txt_resultados.delete("1.0", tk.END)
            self.txt_resultados.insert(tk.END, f"MÉTODO: {metodo}\n")
            self.txt_resultados.insert(tk.END, "="*45 + "\n\n")
            self.txt_resultados.insert(tk.END, f"Matriz A:\n{A}\n\n")
            self.txt_resultados.insert(tk.END, f"Vector b:\n{b}\n\n")
            self.txt_resultados.insert(tk.END, "="*45 + "\n\n")
            
            if metodo == "Gauss-Jordan":
                solucion, pasos = gauss_jordan(A, b)
                if solucion is not None:
                    self.mostrar_resultados_gauss_jordan(solucion, pasos)
                    self.status_bar.config(text=f"Sistema resuelto con el método de {metodo}")
            
            elif metodo == "Gauss-Seidel":
                solucion, pasos = gauss_seidel(A, b, x0, tolerancia, max_iter)
                if solucion is not None:
                    self.mostrar_resultados_iterativos(solucion, pasos, "Gauss-Seidel")
                    self.status_bar.config(text=f"Sistema resuelto con el método de {metodo} en {len(pasos)-1} iteraciones")
            
            elif metodo == "Jacobi":
                solucion, pasos = jacobi(A, b, x0, tolerancia, max_iter)
                if solucion is not None:
                    self.mostrar_resultados_iterativos(solucion, pasos, "Jacobi")
                    self.status_bar.config(text=f"Sistema resuelto con el método de {metodo} en {len(pasos)-1} iteraciones")
        
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")
            self.status_bar.config(text=f"Error: {str(e)}")
            
    def mostrar_resultados_gauss_jordan(self, solucion, pasos):
        """Muestra los resultados del método de Gauss-Jordan"""
        self.txt_resultados.insert(tk.END, "PASOS DEL MÉTODO DE GAUSS-JORDAN:\n\n")
        
        for i, paso in enumerate(pasos):
            self.txt_resultados.insert(tk.END, f"Paso {i+1}:\n")
            # Formatear matriz para mejor visualización
            self.txt_resultados.insert(tk.END, f"{paso}\n\n")
        
        self.txt_resultados.insert(tk.END, "="*45 + "\n\n")
        self.txt_resultados.insert(tk.END, "SOLUCIÓN FINAL:\n")
        
        for i, val in enumerate(solucion):
            self.txt_resultados.insert(tk.END, f"x{i+1} = {val:.8f}\n")

    def mostrar_resultados_iterativos(self, solucion, pasos, metodo):
        """Muestra los resultados de métodos iterativos (Gauss-Seidel, Jacobi)"""
        self.txt_resultados.insert(tk.END, f"ITERACIONES DEL MÉTODO DE {metodo.upper()}:\n\n")
        
        for i, paso in enumerate(pasos):
            self.txt_resultados.insert(tk.END, f"Iteración {i}:\n")
            self.txt_resultados.insert(tk.END, f"{paso}\n\n")
        
        self.txt_resultados.insert(tk.END, "="*45 + "\n\n")
        self.txt_resultados.insert(tk.END, "SOLUCIÓN FINAL:\n")
        
        for i, val in enumerate(solucion):
            self.txt_resultados.insert(tk.END, f"x{i+1} = {val:.8f}\n")
        
        self.txt_resultados.insert(tk.END, f"\nConvergencia alcanzada en {len(pasos)-1} iteraciones")
