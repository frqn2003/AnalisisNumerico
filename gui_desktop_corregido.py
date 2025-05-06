
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sympy import Symbol, sympify
import json
import os
from tkinter import simpledialog

from favoritos import GestorFavoritos
from metodos_raices import biseccion, regula_falsi, newton, secante
from metodos_sistemas import gauss_seidel, jacobi, gauss_jordan
import Validar_txt as vt
from idiomas import GestorIdiomas

class AplicacionMetodosNumericos:
    def __init__(self, master):
        self.master = master
        
        # Inicializar el gestor de idiomas primero
        self.gestor_idiomas = GestorIdiomas(idioma_inicial="es")
        
        # Usar el gestor para configurar el título
        master.title(self.gestor_idiomas.obtener_texto("app_title"))
        master.geometry("1000x700")
        master.configure(bg="#f0f0f0")
        
        # Crear un marco principal con padding
        main_frame = tk.Frame(master, bg="#f0f0f0", padx=15, pady=15)
        main_frame.pack(fill='both', expand=True)
        
        # Título de la aplicación usando el gestor de idiomas
        titulo_frame = tk.Frame(main_frame, bg="#f0f0f0")
        titulo_frame.pack(fill="x", pady=(0, 15))
        
        self.titulo_label = tk.Label(
            titulo_frame,
            text=self.gestor_idiomas.obtener_texto("app_title"),
            font=("Arial", 18, "bold"),
            bg="#f0f0f0",
            fg="#2c3e50"
        )
        self.titulo_label.pack()
        
        self.subtitulo_label = tk.Label(
            titulo_frame,
            text=self.gestor_idiomas.obtener_texto("app_subtitle"),
            font=("Arial", 12),
            bg="#f0f0f0",
            fg="#7f8c8d"
        )
        self.subtitulo_label.pack()
        # Botón para cambiar idioma
        self.idioma_frame = tk.Frame(titulo_frame, bg="#f0f0f0")
        self.idioma_frame.pack(pady=5)
        
        self.idioma_label = tk.Label(
            self.idioma_frame,
            text=self.gestor_idiomas.obtener_texto("language") + ":",
            bg="#f0f0f0",
            fg="#2c3e50",
            font=("Arial", 10)
        )
        self.idioma_label.pack(side=tk.LEFT, padx=(0, 5))
        
        self.idioma_var = tk.StringVar()
        self.idioma_var.set(self.gestor_idiomas.obtener_texto("language_spanish") if self.gestor_idiomas.idioma_actual == "es" else self.gestor_idiomas.obtener_texto("language_english"))
        
        idiomas = [self.gestor_idiomas.obtener_texto("language_spanish"), self.gestor_idiomas.obtener_texto("language_english")]
        
        self.combo_idioma = ttk.Combobox(
            self.idioma_frame,
            textvariable=self.idioma_var,
            values=idiomas,
            state="readonly",
            width=10,
            font=("Arial", 10)
        )
        self.combo_idioma.pack(side=tk.LEFT)
        self.combo_idioma.current(0 if self.gestor_idiomas.idioma_actual == "es" else 1)
        
        # Vincular cambio de idioma
        self.combo_idioma.bind("<<ComboboxSelected>>", self.cambiar_idioma)
        
        # Crear notebook para las pestañas
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Pestaña para métodos de raíces
        self.tab_raices = tk.Frame(self.notebook, bg="#f5f5f5")
        self.notebook.add(self.tab_raices, text=self.gestor_idiomas.obtener_texto("tab_roots"))
        
        # Pestaña para sistemas de ecuaciones
        self.tab_sistemas = tk.Frame(self.notebook, bg="#f5f5f5")
        self.notebook.add(self.tab_sistemas, text=self.gestor_idiomas.obtener_texto("tab_systems"))
        
        # Pestaña de información
        self.tab_info = tk.Frame(self.notebook, bg="#f5f5f5")
        self.notebook.add(self.tab_info, text=self.gestor_idiomas.obtener_texto("tab_info"))
        
        self.tab_favoritos = tk.Frame(self.notebook, bg="#f5f5f5")
        self.notebook.add(self.tab_favoritos, text=self.gestor_idiomas.obtener_texto("tab_favorites"))
        
        # Configurar las pestañas
        self.setup_tab_raices()
        self.setup_tab_sistemas()
        self.setup_tab_info()
        self.setup_tab_favoritos()

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
        
    def cambiar_idioma(self, event=None):
        # Determinar el nuevo idioma basado en la selección
        nuevo_idioma = "es" if self.idioma_var.get() == self.gestor_idiomas.obtener_texto("language_spanish") else "en"
        
        # Si el idioma no cambió, no hacer nada
        if nuevo_idioma == self.gestor_idiomas.idioma_actual:
            return
        
        # Cambiar el idioma
        if self.gestor_idiomas.cambiar_idioma(nuevo_idioma):
            # Actualizar la interfaz con el nuevo idioma
            self.actualizar_interfaz()
            # Mostrar mensaje de confirmación
            messagebox.showinfo(
                self.gestor_idiomas.obtener_texto("success"),
                self.gestor_idiomas.obtener_texto("change_language")
            )
        
    def actualizar_interfaz(self):
        """Actualiza todos los textos de la interfaz al idioma actual"""
        # Actualizar título y subtítulo
        self.master.title(self.gestor_idiomas.obtener_texto("app_title"))
        self.titulo_label.config(text=self.gestor_idiomas.obtener_texto("app_title"))
        self.subtitulo_label.config(text=self.gestor_idiomas.obtener_texto("app_subtitle"))
        
        # Actualizar etiqueta de idioma
        self.idioma_label.config(text=self.gestor_idiomas.obtener_texto("language") + ":")
        
        # Actualizar combobox de idioma
        idiomas = [self.gestor_idiomas.obtener_texto("language_spanish"), self.gestor_idiomas.obtener_texto("language_english")]
        self.combo_idioma.config(values=idiomas)
        self.idioma_var.set(self.gestor_idiomas.obtener_texto("language_spanish") if self.gestor_idiomas.idioma_actual == "es" else self.gestor_idiomas.obtener_texto("language_english"))
        
        # Actualizar pestañas
        self.notebook.tab(0, text=self.gestor_idiomas.obtener_texto("tab_roots"))
        self.notebook.tab(1, text=self.gestor_idiomas.obtener_texto("tab_systems"))
        self.notebook.tab(2, text=self.gestor_idiomas.obtener_texto("tab_info"))
        self.notebook.tab(3, text=self.gestor_idiomas.obtener_texto("tab_favorites"))
        
        # Actualizar barra de estado
        self.status_bar.config(text=self.gestor_idiomas.obtener_texto("ready_status"))
        
        # Actualizar contenido de las pestañas
        self.actualizar_tab_raices()
        self.actualizar_tab_sistemas()
        self.actualizar_tab_info()
        self.actualizar_tab_favoritos()
    def actualizar_tab_raices(self):
        """Actualiza los textos de la pestaña de raíces"""
        # Actualizar botones principales
        if hasattr(self, 'btn_resolver_raices'):
            self.btn_resolver_raices.config(text=self.gestor_idiomas.obtener_texto("calculate_root"))
        
        if hasattr(self, 'btn_guardar_favorito_raices'):
            self.btn_guardar_favorito_raices.config(text=self.gestor_idiomas.obtener_texto("save_as_favorite"))
        
        # Actualizar etiquetas de método
        if hasattr(self, 'metodo_label'):
            self.metodo_label.config(text=self.gestor_idiomas.obtener_texto("method") + ":")
        
        if hasattr(self, 'metodo_frame'):
            self.metodo_frame.config(text=self.gestor_idiomas.obtener_texto("select_method"))
        
        # Actualizar etiquetas de función
        if hasattr(self, 'funcion_label'):
            self.funcion_label.config(text=self.gestor_idiomas.obtener_texto("function") + ":")
        
        if hasattr(self, 'funcion_frame'):
            self.funcion_frame.config(text=self.gestor_idiomas.obtener_texto("function_fx"))
        
        # Actualizar etiquetas de parámetros
        if hasattr(self, 'parametros_frame'):
            self.parametros_frame.config(text=self.gestor_idiomas.obtener_texto("parameters"))
        
        if hasattr(self, 'a_label'):
            self.a_label.config(text=self.gestor_idiomas.obtener_texto("a_left"))
        
        if hasattr(self, 'b_label'):
            self.b_label.config(text=self.gestor_idiomas.obtener_texto("b_right"))
        
        if hasattr(self, 'x0_label'):
            self.x0_label.config(text=self.gestor_idiomas.obtener_texto("x0_approx"))
        
        if hasattr(self, 'x1_label'):
            self.x1_label.config(text=self.gestor_idiomas.obtener_texto("x1_second"))
        
        if hasattr(self, 'not_used_label'):
            self.not_used_label.config(text=self.gestor_idiomas.obtener_texto("not_used"))
        
        if hasattr(self, 'tolerancia_label'):
            self.tolerancia_label.config(text=self.gestor_idiomas.obtener_texto("tolerance"))
        
        if hasattr(self, 'max_iter_label'):
            self.max_iter_label.config(text=self.gestor_idiomas.obtener_texto("max_iterations"))
        
        # Actualizar frame de ejemplos
        if hasattr(self, 'ejemplos_frame'):
            self.ejemplos_frame.config(text=self.gestor_idiomas.obtener_texto("examples"))
        
        if hasattr(self, 'btn_ejemplo_polinomico'):
            self.btn_ejemplo_polinomico.config(text=self.gestor_idiomas.obtener_texto("polynomial_function"))
        
        if hasattr(self, 'btn_ejemplo_trigonometrico'):
            self.btn_ejemplo_trigonometrico.config(text=self.gestor_idiomas.obtener_texto("trigonometric_function"))
        
        # Actualizar resultados
        if hasattr(self, 'resultados_frame'):
            self.resultados_frame.config(text=self.gestor_idiomas.obtener_texto("results"))
        
        if hasattr(self, 'grafico_frame'):
            self.grafico_frame.config(text=self.gestor_idiomas.obtener_texto("graph"))

    def actualizar_tab_sistemas(self):
        """Actualiza los textos de la pestaña de sistemas"""
        # Actualizar etiquetas y frames principales
        if hasattr(self, 'datos_frame'):
            self.datos_frame.config(text=self.gestor_idiomas.obtener_texto("data_input"))
        
        if hasattr(self, 'matriz_a_label'):
            self.matriz_a_label.config(text=self.gestor_idiomas.obtener_texto("matrix_A"))
        
        if hasattr(self, 'vector_b_label'):
            self.vector_b_label.config(text=self.gestor_idiomas.obtener_texto("vector_b"))
        
        if hasattr(self, 'vector_x0_label'):
            self.vector_x0_label.config(text=self.gestor_idiomas.obtener_texto("vector_x0"))
        
        # Actualizar botones
        if hasattr(self, 'btn_resolver_sistema'):
            self.btn_resolver_sistema.config(text=self.gestor_idiomas.obtener_texto("solve_system"))
        
        if hasattr(self, 'btn_guardar_favorito_sistemas'):
            self.btn_guardar_favorito_sistemas.config(text=self.gestor_idiomas.obtener_texto("save_as_favorite"))
        
        # Actualizar ejemplos
        if hasattr(self, 'ejemplos_sistemas_frame'):
            self.ejemplos_sistemas_frame.config(text=self.gestor_idiomas.obtener_texto("examples"))
        
        if hasattr(self, 'btn_ejemplo_sistema1'):
            self.btn_ejemplo_sistema1.config(text=self.gestor_idiomas.obtener_texto("example_1"))
        
        if hasattr(self, 'btn_ejemplo_sistema2'):
            self.btn_ejemplo_sistema2.config(text=self.gestor_idiomas.obtener_texto("example_2"))
        
        # Actualizar resultados
        if hasattr(self, 'resultados_sistemas_frame'):
            self.resultados_sistemas_frame.config(text=self.gestor_idiomas.obtener_texto("results"))
        
        # Actualizar método
        if hasattr(self, 'metodo_sistemas_label'):
            self.metodo_sistemas_label.config(text=self.gestor_idiomas.obtener_texto("method") + ":")
        
        if hasattr(self, 'metodo_sistemas_frame'):
            self.metodo_sistemas_frame.config(text=self.gestor_idiomas.obtener_texto("select_method"))

    def actualizar_tab_info(self):
        """Actualiza los textos de la pestaña de información"""
        # Actualizar título y descripción
        if hasattr(self, 'info_titulo_label'):
            self.info_titulo_label.config(text=self.gestor_idiomas.obtener_texto("app_name"))
        
        if hasattr(self, 'info_descripcion_text'):
            self.info_descripcion_text.config(state='normal')
            self.info_descripcion_text.delete(1.0, tk.END)
            self.info_descripcion_text.insert(tk.END, self.gestor_idiomas.obtener_texto("app_description"))
            self.info_descripcion_text.config(state='disabled')
        
        # Actualizar secciones de métodos
        if hasattr(self, 'metodos_raices_label'):
            self.metodos_raices_label.config(text=self.gestor_idiomas.obtener_texto("root_methods"))
        
        if hasattr(self, 'metodos_sistemas_label'):
            self.metodos_sistemas_label.config(text=self.gestor_idiomas.obtener_texto("system_methods"))
        
        # Actualizar nombres y descripciones de métodos
        if hasattr(self, 'biseccion_nombre_label'):
            self.biseccion_nombre_label.config(text=self.gestor_idiomas.obtener_texto("bisection_name"))
        
        if hasattr(self, 'biseccion_desc_label'):
            self.biseccion_desc_label.config(text=self.gestor_idiomas.obtener_texto("bisection_desc"))
        
        if hasattr(self, 'regula_falsi_nombre_label'):
            self.regula_falsi_nombre_label.config(text=self.gestor_idiomas.obtener_texto("regula_falsi_name"))
        
        if hasattr(self, 'regula_falsi_desc_label'):
            self.regula_falsi_desc_label.config(text=self.gestor_idiomas.obtener_texto("regula_falsi_desc"))
        
        if hasattr(self, 'newton_nombre_label'):
            self.newton_nombre_label.config(text=self.gestor_idiomas.obtener_texto("newton_name"))
        
        if hasattr(self, 'newton_desc_label'):
            self.newton_desc_label.config(text=self.gestor_idiomas.obtener_texto("newton_desc"))
        
        if hasattr(self, 'secante_nombre_label'):
            self.secante_nombre_label.config(text=self.gestor_idiomas.obtener_texto("secant_name"))
        
        if hasattr(self, 'secante_desc_label'):
            self.secante_desc_label.config(text=self.gestor_idiomas.obtener_texto("secant_desc"))
        
        if hasattr(self, 'gauss_jordan_nombre_label'):
            self.gauss_jordan_nombre_label.config(text=self.gestor_idiomas.obtener_texto("gauss_jordan_name"))
        
        if hasattr(self, 'gauss_jordan_desc_label'):
            self.gauss_jordan_desc_label.config(text=self.gestor_idiomas.obtener_texto("gauss_jordan_desc"))
        
        if hasattr(self, 'gauss_seidel_nombre_label'):
            self.gauss_seidel_nombre_label.config(text=self.gestor_idiomas.obtener_texto("gauss_seidel_name"))
        
        if hasattr(self, 'gauss_seidel_desc_label'):
            self.gauss_seidel_desc_label.config(text=self.gestor_idiomas.obtener_texto("gauss_seidel_desc"))
        
        if hasattr(self, 'jacobi_nombre_label'):
            self.jacobi_nombre_label.config(text=self.gestor_idiomas.obtener_texto("jacobi_name"))
        
        if hasattr(self, 'jacobi_desc_label'):
            self.jacobi_desc_label.config(text=self.gestor_idiomas.obtener_texto("jacobi_desc"))
        
        # Actualizar pie de página
        if hasattr(self, 'footer_label'):
            self.footer_label.config(text=self.gestor_idiomas.obtener_texto("footer_text"))

    def actualizar_tab_favoritos(self):
        """Actualiza los textos de la pestaña de favoritos"""
        # Actualizar título y etiquetas principales
        if hasattr(self, 'favoritos_titulo_label'):
            self.favoritos_titulo_label.config(text=self.gestor_idiomas.obtener_texto("my_favorites"))
        
        # Actualizar frame de detalles
        if hasattr(self, 'detalles_frame'):
            self.detalles_frame.config(text=self.gestor_idiomas.obtener_texto("details"))
        
        # Actualizar etiquetas de detalles
        if hasattr(self, 'nombre_favorito_label'):
            self.nombre_favorito_label.config(text=self.gestor_idiomas.obtener_texto("name"))
        
        if hasattr(self, 'expresion_favorito_label'):
            self.expresion_favorito_label.config(text=self.gestor_idiomas.obtener_texto("expression"))
        
        if hasattr(self, 'descripcion_favorito_label'):
            self.descripcion_favorito_label.config(text=self.gestor_idiomas.obtener_texto("description"))
        
        if hasattr(self, 'fecha_favorito_label'):
            self.fecha_favorito_label.config(text=self.gestor_idiomas.obtener_texto("creation_date"))
        
        # Actualizar botones
        if hasattr(self, 'btn_cargar_favorito'):
            self.btn_cargar_favorito.config(text=self.gestor_idiomas.obtener_texto("load_calculator"))
        
        if hasattr(self, 'btn_eliminar_favorito'):
            self.btn_eliminar_favorito.config(text=self.gestor_idiomas.obtener_texto("delete"))
        
        # Actualizar encabezados de lista si existe un Treeview
        if hasattr(self, 'favoritos_tree'):
            self.favoritos_tree.heading('nombre', text=self.gestor_idiomas.obtener_texto("name"))
            self.favoritos_tree.heading('tipo', text=self.gestor_idiomas.obtener_texto("function"))
            self.favoritos_tree.heading('fecha', text=self.gestor_idiomas.obtener_texto("creation_date"))

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
        self.metodo_frame = tk.LabelFrame(
            panel_izquierdo,
            text=self.gestor_idiomas.obtener_texto("method"),
            bg="#f5f5f5",
            fg="#2c3e50",
            font=("Arial", 11, "bold"),
            padx=10,
            pady=10
        )
        self.metodo_frame.pack(fill='x', pady=(0, 10))
        
        self.metodo_label = tk.Label(
            self.metodo_frame,
            text=self.gestor_idiomas.obtener_texto("select_method"),
            bg="#f5f5f5",
            fg="#2c3e50",
            font=("Arial", 10)
        )
        self.metodo_label.pack(side=tk.LEFT, padx=(0, 5))
        
        self.metodo_raices_var = tk.StringVar()
        metodos = ["Bisección", "Regula Falsi", "Newton", "Secante"]
        
        self.combo_metodo_raices = ttk.Combobox(
            self.metodo_frame,
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
        self.funcion_frame = tk.LabelFrame(
            panel_izquierdo,
            text=self.gestor_idiomas.obtener_texto("function"),
            bg="#f5f5f5",
            fg="#2c3e50",
            font=("Arial", 11, "bold"),
            padx=10,
            pady=10
        )
        self.funcion_frame.pack(fill='x', pady=10)
        
        self.funcion_label = tk.Label(
            self.funcion_frame,
            text=self.gestor_idiomas.obtener_texto("function_fx"),
            bg="#f5f5f5",
            fg="#2c3e50",
            font=("Arial", 10),
            anchor="w"
        )
        self.funcion_label.pack(fill='x', pady=(0, 5))
        
        self.entry_funcion = tk.Entry(
            self.funcion_frame,
            font=("Courier New", 10),
            bg="white",
            fg="#2c3e50",
            relief="solid",
            bd=1
        )
        self.entry_funcion.pack(fill='x', pady=(0, 10))
        self.entry_funcion.insert(0, "x**3 - x - 2")  # Función de ejemplo
        
        # Frame para parámetros
        self.parametros_frame = tk.LabelFrame(
            panel_izquierdo,
            text=self.gestor_idiomas.obtener_texto("parameters"),
            bg="#f5f5f5",
            fg="#2c3e50",
            font=("Arial", 11, "bold"),
            padx=10,
            pady=10
        )
        self.parametros_frame.pack(fill='x', pady=10)
        
        # Parámetro a
        self.lbl_a_frame = tk.Frame(self.parametros_frame, bg="#f5f5f5")
        self.lbl_a_frame.pack(fill='x', pady=5)
        
        self.a_label = tk.Label(
            self.lbl_a_frame,
            text=self.gestor_idiomas.obtener_texto("a_left"),
            bg="#f5f5f5",
            fg="#2c3e50",
            font=("Arial", 10),
            anchor="w"
        )
        self.a_label.pack(fill='x')
        
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
        self.lbl_b_frame = tk.Frame(self.parametros_frame, bg="#f5f5f5")
        self.lbl_b_frame.pack(fill='x', pady=5)
        
        self.b_label = tk.Label(
            self.lbl_b_frame,
            text=self.gestor_idiomas.obtener_texto("b_right"),
            bg="#f5f5f5",
            fg="#2c3e50",
            font=("Arial", 10),
            anchor="w"
        )
        self.b_label.pack(fill='x')
        
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
        param_adicionales_frame = tk.Frame(self.parametros_frame, bg="#f5f5f5")
        param_adicionales_frame.pack(fill='x', pady=5)
        
        self.tolerancia_label = tk.Label(
            param_adicionales_frame,
            text=self.gestor_idiomas.obtener_texto("tolerance"),
            bg="#f5f5f5",
            fg="#2c3e50",
            font=("Arial", 10)
        )
        self.tolerancia_label.grid(row=0, column=0, padx=(0, 5), sticky="w")
        
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
        
        self.max_iter_label = tk.Label(
            param_adicionales_frame,
            text=self.gestor_idiomas.obtener_texto("max_iterations"),
            bg="#f5f5f5",
            fg="#2c3e50",
            font=("Arial", 10)
        )
        self.max_iter_label.grid(row=0, column=2, padx=(0, 5), sticky="w")
        
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
            text=self.gestor_idiomas.obtener_texto("calculate_root"),
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
        self.ejemplos_frame = tk.LabelFrame(
            panel_izquierdo,
            text=self.gestor_idiomas.obtener_texto("examples"),
            bg="#f5f5f5",
            fg="#2c3e50",
            font=("Arial", 11, "bold"),
            padx=10,
            pady=3
        )
        self.ejemplos_frame.pack(fill='x', pady=10)
        
        self.btn_ejemplo_polinomico = tk.Button(
            self.ejemplos_frame,
            text=self.gestor_idiomas.obtener_texto("polynomial_function"),
            command=lambda: self.cargar_ejemplo_raiz(1),
            bg="#2ecc71",
            fg="white",
            font=("Arial", 9),
            relief="flat",
            padx=5,
            pady=1,
            cursor="hand2"
        )
        self.btn_ejemplo_polinomico.pack(side=tk.LEFT, padx=(0, 10), pady=2)
        
        self.btn_ejemplo_trigonometrico = tk.Button(
            self.ejemplos_frame,
            text=self.gestor_idiomas.obtener_texto("trigonometric_function"),
            command=lambda: self.cargar_ejemplo_raiz(2),
            bg="#2ecc71",
            fg="white",
            font=("Arial", 9),
            relief="flat",
            padx=5,
            pady=1,
            cursor="hand2"
        )
        self.btn_ejemplo_trigonometrico.pack(side=tk.LEFT, pady=2)
        
        self.btn_guardar_favorito_raices = tk.Button(
            btn_frame,
            text=self.gestor_idiomas.obtener_texto("save_as_favorite"),
            command=self.guardar_favorito_raices,
            bg="#2ecc71",
            fg="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            padx=10,
            pady=5,
            cursor="hand2"
        )
        self.btn_guardar_favorito_raices.pack(side=tk.LEFT)

        # ===== PANEL DERECHO =====
        # Crear un frame contenedor para resultados y gráfico
        contenedor_frames = tk.Frame(panel_derecho, bg="#f5f5f5")
        contenedor_frames.pack(fill='both', expand=True)
        
        # Frame para resultados (mitad superior)
        self.resultados_frame = tk.LabelFrame(
            contenedor_frames,
            text=self.gestor_idiomas.obtener_texto("results"),
            bg="#f5f5f5",
            fg="#2c3e50",
            font=("Arial", 11, "bold"),
            padx=10,
            pady=10
        )
        self.resultados_frame.pack(fill='both', expand=True, pady=(0, 5))
        
        # Área de texto para mostrar resultados
        self.txt_resultados_raices = scrolledtext.ScrolledText(
            self.resultados_frame,
            width=45,
            height=10,
            font=("Courier New", 10),
            bg="white",
            fg="#2c3e50"
        )
        self.txt_resultados_raices.pack(fill='both', expand=True)
        
        # Frame para gráfico (mitad inferior)
        self.grafico_frame = tk.LabelFrame(
            contenedor_frames,
            text=self.gestor_idiomas.obtener_texto("graph"),
            bg="#f5f5f5",
            fg="#2c3e50",
            font=("Arial", 11, "bold"),
            padx=10,
            pady=10
        )
        self.grafico_frame.pack(fill='both', expand=True, pady=(5, 0))
        
        # Contenedor para el gráfico de matplotlib
        self.fig_raices = plt.Figure(dpi=100)
        self.ax_raices = self.fig_raices.add_subplot(111)
        self.canvas_raices = FigureCanvasTkAgg(self.fig_raices, self.grafico_frame)
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
        
        self.btn_guardar_favorito_sistemas = tk.Button(
            method_frame,
            text="Guardar como Favorito",
            command=self.guardar_favorito_sistemas,
            bg="#2ecc71",  # Verde
            fg="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            padx=10,
            pady=5,
            cursor="hand2"
        )
        self.btn_guardar_favorito_sistemas.pack(side=tk.RIGHT, padx=(5, 0))
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
            self.a_label.config(text=self.gestor_idiomas.obtener_texto("a_left"))
            self.b_label.config(text=self.gestor_idiomas.obtener_texto("b_right"))
            self.entry_b.config(state="normal")
        elif metodo == "Newton":
            self.a_label.config(text=self.gestor_idiomas.obtener_texto("x0_approx"))
            self.b_label.config(text=self.gestor_idiomas.obtener_texto("not_used"))
            self.entry_b.config(state="disabled")
        elif metodo == "Secante":
            self.a_label.config(text=self.gestor_idiomas.obtener_texto("x0_first"))
            self.b_label.config(text=self.gestor_idiomas.obtener_texto("x1_second"))
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
            self.status_bar.config(text=f"{self.gestor_idiomas.obtener_texto('polynomial_function')} f(x) = x³ - x - 2")
        
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
            self.status_bar.config(text=f"{self.gestor_idiomas.obtener_texto('trigonometric_function')} f(x) = sin(x) - x/2")
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
            self.status_bar.config(text=self.gestor_idiomas.obtener_texto("calculating_root"))
            self.master.update_idletasks()
            
            # Obtener función y convertirla a expresión simbólica
            f_str = self.entry_funcion.get().strip()
            if not f_str:
                messagebox.showerror(self.gestor_idiomas.obtener_texto("error"), 
                                    self.gestor_idiomas.obtener_texto("function_empty"))
                self.status_bar.config(text=self.gestor_idiomas.obtener_texto("error_empty_function"))
                return
            
            try:
                x = Symbol('x')
                f = sympify(f_str)
            except Exception as e:
                messagebox.showerror(self.gestor_idiomas.obtener_texto("error"), 
                                    f"{self.gestor_idiomas.obtener_texto('error_parsing_function')}: {e}")
                self.status_bar.config(text=self.gestor_idiomas.obtener_texto("error_in_function"))
                return
            
            # Obtener parámetros adicionales
            try:
                tol = float(self.entry_tol_raices.get())
                max_iter = int(self.entry_max_iter_raices.get())
            except ValueError:
                messagebox.showerror(self.gestor_idiomas.obtener_texto("error"), 
                                    self.gestor_idiomas.obtener_texto("error_tolerance_iterations"))
                self.status_bar.config(text=self.gestor_idiomas.obtener_texto("error_in_parameters"))
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
                    
                    self.txt_resultados_raices.insert(tk.END, f"{self.gestor_idiomas.obtener_texto('bisection method')}\n")
                    self.txt_resultados_raices.insert(tk.END, f"{self.gestor_idiomas.obtener_texto('function')}: {f_str}\n")
                    self.txt_resultados_raices.insert(tk.END, f"{self.gestor_idiomas.obtener_texto('interval')}: [{a}, {b}]\n")
                    self.txt_resultados_raices.insert(tk.END, f"{self.gestor_idiomas.obtener_texto('tolerance')}: {tol}\n")
                    self.txt_resultados_raices.insert(tk.END, f"{self.gestor_idiomas.obtener_texto('max iterations')}: {max_iter}\n\n")
                    
                    raiz, pasos = biseccion(f, a, b, tol, max_iter)
                    self._mostrar_resultados_raiz(raiz, pasos, f)
                except Exception as e:
                    messagebox.showerror(self.gestor_idiomas.obtener_texto("error"), 
                                        f"{self.gestor_idiomas.obtener_texto('error_executing_method')}: {e}")
                    self.status_bar.config(text=f"{self.gestor_idiomas.obtener_texto('error')}: {str(e)}")
            
            elif metodo == "Regula Falsi":
                try:
                    a = float(self.entry_a.get())
                    b = float(self.entry_b.get())
                    
                    self.txt_resultados_raices.insert(tk.END, f"{self.gestor_idiomas.obtener_texto('regula falsi method')}\n")
                    self.txt_resultados_raices.insert(tk.END, f"{self.gestor_idiomas.obtener_texto('function')}: {f_str}\n")
                    self.txt_resultados_raices.insert(tk.END, f"{self.gestor_idiomas.obtener_texto('interval')}: [{a}, {b}]\n")
                    self.txt_resultados_raices.insert(tk.END, f"{self.gestor_idiomas.obtener_texto('tolerance')}: {tol}\n")
                    self.txt_resultados_raices.insert(tk.END, f"{self.gestor_idiomas.obtener_texto('max iterations')}: {max_iter}\n\n")
                    
                    raiz, pasos = regula_falsi(f, a, b, tol, max_iter)
                    self._mostrar_resultados_raiz(raiz, pasos, f)
                except Exception as e:
                    messagebox.showerror(self.gestor_idiomas.obtener_texto("error"), 
                                        f"{self.gestor_idiomas.obtener_texto('error_executing_method')}: {e}")
                    self.status_bar.config(text=f"{self.gestor_idiomas.obtener_texto('error')}: {str(e)}")
            
            elif metodo == "Newton":
                try:
                    x0 = float(self.entry_a.get())
                    
                    self.txt_resultados_raices.insert(tk.END, f"{self.gestor_idiomas.obtener_texto('newton method')}\n")
                    self.txt_resultados_raices.insert(tk.END, f"{self.gestor_idiomas.obtener_texto('function')}: {f_str}\n")
                    self.txt_resultados_raices.insert(tk.END, f"{self.gestor_idiomas.obtener_texto('initial approximation')}: {x0}\n")
                    self.txt_resultados_raices.insert(tk.END, f"{self.gestor_idiomas.obtener_texto('tolerance')}: {tol}\n")
                    self.txt_resultados_raices.insert(tk.END, f"{self.gestor_idiomas.obtener_texto('max iterations')}: {max_iter}\n\n")
                    
                    raiz, pasos = newton(f, x0, tol, max_iter)
                    self._mostrar_resultados_raiz(raiz, pasos, f)
                except Exception as e:
                    messagebox.showerror(self.gestor_idiomas.obtener_texto("error"), 
                                        f"{self.gestor_idiomas.obtener_texto('error_executing_method')}: {e}")
                    self.status_bar.config(text=f"{self.gestor_idiomas.obtener_texto('error')}: {str(e)}")
            
            elif metodo == "Secante":
                try:
                    x0 = float(self.entry_a.get())
                    x1 = float(self.entry_b.get())
                    
                    self.txt_resultados_raices.insert(tk.END, f"{self.gestor_idiomas.obtener_texto('secant method')}\n")
                    self.txt_resultados_raices.insert(tk.END, f"{self.gestor_idiomas.obtener_texto('function')}: {f_str}\n")
                    self.txt_resultados_raices.insert(tk.END, f"{self.gestor_idiomas.obtener_texto('first approximation')}: {x0}\n")
                    self.txt_resultados_raices.insert(tk.END, f"{self.gestor_idiomas.obtener_texto('second approximation')}: {x1}\n")
                    self.txt_resultados_raices.insert(tk.END, f"{self.gestor_idiomas.obtener_texto('tolerance')}: {tol}\n")
                    self.txt_resultados_raices.insert(tk.END, f"{self.gestor_idiomas.obtener_texto('max iterations')}: {max_iter}\n\n")
                    
                    raiz, pasos = secante(f, x0, x1, tol, max_iter)
                    self._mostrar_resultados_raiz(raiz, pasos, f)
                except Exception as e:
                    messagebox.showerror(self.gestor_idiomas.obtener_texto("error"), 
                                        f"{self.gestor_idiomas.obtener_texto('error_executing_method')}: {e}")
                    self.status_bar.config(text=f"{self.gestor_idiomas.obtener_texto('error')}: {str(e)}")
        
        except Exception as e:
            messagebox.showerror(self.gestor_idiomas.obtener_texto("error"), 
                                f"{self.gestor_idiomas.obtener_texto('unexpected_error')}: {e}")
            self.status_bar.config(text=self.gestor_idiomas.obtener_texto("unexpected_error"))
    def _mostrar_resultados_raiz(self, raiz, pasos, f):
        """Muestra los resultados de los métodos de búsqueda de raíces"""
        if raiz is None:
            self.txt_resultados_raices.insert(tk.END, f"{self.gestor_idiomas.obtener_texto('method_no_root')}\n")
            self.status_bar.config(text=self.gestor_idiomas.obtener_texto("no_root_found"))
            return
        
        # Mostrar pasos
        self.txt_resultados_raices.insert(tk.END, f"{self.gestor_idiomas.obtener_texto('iterations').upper()}:\n")
        for i, paso in enumerate(pasos):
            self.txt_resultados_raices.insert(tk.END, f"{self.gestor_idiomas.obtener_texto('iteration')} {i+1}: x = {paso:.8f}\n")
        
        # Mostrar resultado final
        self.txt_resultados_raices.insert(tk.END, f"\n{self.gestor_idiomas.obtener_texto('final_result').upper()}:\n")
        self.txt_resultados_raices.insert(tk.END, f"{self.gestor_idiomas.obtener_texto('approximate_root')}: {raiz:.8f}\n")
        
        x = Symbol('x')
        f_val = float(f.subs(x, raiz))
        self.txt_resultados_raices.insert(tk.END, f"f({raiz:.8f}) = {f_val:.8e}\n")
        self.txt_resultados_raices.insert(tk.END, f"{self.gestor_idiomas.obtener_texto('number_of_iterations')}: {len(pasos)}\n")
        
        # Graficar la función y la raíz
        self._graficar_funcion(f, raiz, pasos)
        
        self.status_bar.config(text=f"{self.gestor_idiomas.obtener_texto('root_found')}: {raiz:.8f}")
    def _graficar_funcion(self, f, raiz, pasos):
        """Grafica la función y la raíz encontrada"""
        try:
            # Limpiar gráfico anterior completamente
            self.ax_raices.clear()
            self.fig_raices.clf()  # Limpiar toda la figura
            self.ax_raices = self.fig_raices.add_subplot(111)  # Recrear el eje principal
            
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
            root_label = f"{self.gestor_idiomas.obtener_texto('root')}: {raiz:.6f}"
            self.ax_raices.plot([raiz], [0], 'ro', markersize=8, label=root_label)
            
            # Graficar evolución de las aproximaciones
            if len(pasos) > 0:
                pasos_x = list(range(1, len(pasos) + 1))
                pasos_y = pasos
                
                # Crear un segundo eje para las iteraciones
                ax2 = self.ax_raices.twinx()
                ax2.plot(pasos_x, pasos_y, 'g-o', alpha=0.7, label=self.gestor_idiomas.obtener_texto('convergence'))
                ax2.set_ylabel(self.gestor_idiomas.obtener_texto('x_value'))
                ax2.tick_params(axis='y', labelcolor='g')
                
                # Añadir leyenda para el segundo eje
                lines1, labels1 = self.ax_raices.get_legend_handles_labels()
                lines2, labels2 = ax2.get_legend_handles_labels()
                ax2.legend(lines1 + lines2, labels1 + labels2, loc='best')
            else:
                self.ax_raices.legend(loc='best')
            
            # Configurar gráfico
            self.ax_raices.set_xlabel('x')
            self.ax_raices.set_ylabel('f(x)')
            self.ax_raices.set_title(self.gestor_idiomas.obtener_texto('function_graph_and_root'))
            self.ax_raices.grid(True, alpha=0.3)
            
            # Actualizar gráfico
            self.fig_raices.tight_layout()
            self.canvas_raices.draw()
            self.canvas_raices.flush_events()  # Forzar actualización del canvas
            
        except Exception as e:
            print(f"Error al graficar: {e}")
            # Mostrar el error en la interfaz para mejor depuración
            messagebox.showerror(self.gestor_idiomas.obtener_texto("graph_error"), 
                                f"{self.gestor_idiomas.obtener_texto('error_graphing')}: {e}")
    def resolver_sistema(self):
        """Resuelve el sistema de ecuaciones según el método seleccionado"""
        try:
            self.status_bar.config(text=self.gestor_idiomas.obtener_texto("solving_system"))
            self.master.update_idletasks()
            
            # Validar y obtener la matriz A
            valido_a, matriz_a = vt.validar_matriz_texto(self.txt_matriz_a.get("1.0", "end-1c"))
            if not valido_a:
                self.status_bar.config(text=self.gestor_idiomas.obtener_texto("error_matrix_a_format"))
                return
            
            # Validar y obtener el vector b
            valido_b, vector_b = vt.validar_vector_texto(self.txt_vector_b.get())
            if not valido_b:
                self.status_bar.config(text=self.gestor_idiomas.obtener_texto("error_vector_b_format"))
                return
            
            # Validar sistema
            valido_sistema, A, b = vt.validar_sistema_ecuaciones(matriz_a, vector_b)
            if not valido_sistema:
                self.status_bar.config(text=self.gestor_idiomas.obtener_texto("error_equation_system"))
                return
            
            # Obtener parámetros adicionales
            valido_tol, tolerancia = vt.validar_numero(self.txt_tolerancia.get(), 
                                                    self.gestor_idiomas.obtener_texto("tolerance_must_be_number"))
            if not valido_tol:
                self.status_bar.config(text=self.gestor_idiomas.obtener_texto("error_tolerance_value"))
                return
                
            valido_iter, max_iter = vt.validar_entero(self.txt_max_iter.get(), 
                                                    self.gestor_idiomas.obtener_texto("max_iter_must_be_integer"))
            if not valido_iter:
                self.status_bar.config(text=self.gestor_idiomas.obtener_texto("error_max_iterations"))
                return
            
            # Vector inicial (opcional)
            x0 = None
            if self.txt_vector_x0.get().strip():
                valido_x0, x0 = vt.validar_vector_texto(self.txt_vector_x0.get())
                if not valido_x0:
                    self.status_bar.config(text=self.gestor_idiomas.obtener_texto("error_x0_vector_format"))
                    return
                
                # Verificar dimensiones de x0
                if len(x0) != A.shape[1]:
                    messagebox.showwarning(self.gestor_idiomas.obtener_texto("warning"), 
                                        f"{self.gestor_idiomas.obtener_texto('incompatible_dimensions')}: x0 {self.gestor_idiomas.obtener_texto('has')} {len(x0)} {self.gestor_idiomas.obtener_texto('elements_but_should_have')} {A.shape[1]}")
                    self.status_bar.config(text=self.gestor_idiomas.obtener_texto("error_incompatible_dimensions_x0"))
                    return
            
            # Resolver según el método seleccionado
            metodo = self.metodo_var.get()
            
            self.txt_resultados.delete("1.0", tk.END)
            self.txt_resultados.insert(tk.END, f"{self.gestor_idiomas.obtener_texto('method')}: {metodo}\n")
            self.txt_resultados.insert(tk.END, "="*45 + "\n\n")
            self.txt_resultados.insert(tk.END, f"{self.gestor_idiomas.obtener_texto('matrix_A')}:\n{A}\n\n")
            self.txt_resultados.insert(tk.END, f"{self.gestor_idiomas.obtener_texto('vector_b')}:\n{b}\n\n")
            self.txt_resultados.insert(tk.END, "="*45 + "\n\n")
            
            if metodo == "Gauss-Jordan":
                solucion, pasos = gauss_jordan(A, b)
                if solucion is not None:
                    self.mostrar_resultados_gauss_jordan(solucion, pasos)
                    self.status_bar.config(text=f"{self.gestor_idiomas.obtener_texto('system_solved_with')} {metodo}")
            
            elif metodo == "Gauss-Seidel":
                solucion, pasos = gauss_seidel(A, b, x0, tolerancia, max_iter)
                if solucion is not None:
                    self.mostrar_resultados_iterativos(solucion, pasos, "Gauss-Seidel")
                    self.status_bar.config(text=f"{self.gestor_idiomas.obtener_texto('system_solved_with')} {metodo} {self.gestor_idiomas.obtener_texto('in')} {len(pasos)-1} {self.gestor_idiomas.obtener_texto('iterations')}")
            
            elif metodo == "Jacobi":
                solucion, pasos = jacobi(A, b, x0, tolerancia, max_iter)
                if solucion is not None:
                    self.mostrar_resultados_iterativos(solucion, pasos, "Jacobi")
                    self.status_bar.config(text=f"{self.gestor_idiomas.obtener_texto('system_solved_with')} {metodo} {self.gestor_idiomas.obtener_texto('in')} {len(pasos)-1} {self.gestor_idiomas.obtener_texto('iterations')}")
        
        except Exception as e:
            messagebox.showerror(self.gestor_idiomas.obtener_texto("error"), 
                                f"{self.gestor_idiomas.obtener_texto('error_occurred')}: {e}")
            self.status_bar.config(text=f"{self.gestor_idiomas.obtener_texto('error')}: {str(e)}")
    def setup_tab_favoritos(self):
        """Configura la pestaña de favoritos"""
        # Panel principal
        panel_frame = tk.Frame(self.tab_favoritos, bg="#f5f5f5")
        panel_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Inicializar gestor de favoritos si aún no existe
        if not hasattr(self, 'gestor_favoritos'):
            self.gestor_favoritos = GestorFavoritos()
        
        # Panel izquierdo para lista de favoritos
        panel_izquierdo = tk.Frame(panel_frame, bg="#f5f5f5")
        panel_izquierdo.pack(side=tk.LEFT, fill='both', expand=True, padx=(0, 5))
        
        # Panel derecho para detalles y acciones
        panel_derecho = tk.Frame(panel_frame, bg="#f5f5f5")
        panel_derecho.pack(side=tk.RIGHT, fill='both', expand=True, padx=(5, 0))
        
        # Lista de favoritos
        self.lista_frame = tk.LabelFrame(
            panel_izquierdo,
            text=self.gestor_idiomas.obtener_texto("my_favorites"),
            bg="#f5f5f5",
            fg="#2c3e50",
            font=("Arial", 11, "bold"),
            padx=10,
            pady=10
        )
        self.lista_frame.pack(fill='both', expand=True)
        
        # Lista con scrollbar
        scrollbar = tk.Scrollbar(self.lista_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.lista_favoritos = tk.Listbox(
            self.lista_frame,
            bg="white",
            fg="#2c3e50",
            font=("Arial", 10),
            selectbackground="#3498db",
            selectforeground="white",
            height=20,
            bd=1,
            relief="solid",
            yscrollcommand=scrollbar.set
        )
        self.lista_favoritos.pack(side=tk.LEFT, fill='both', expand=True, padx=5, pady=5)
        scrollbar.config(command=self.lista_favoritos.yview)
        
        # Cargar favoritos en la lista
        self.cargar_lista_favoritos()
        
        # Vincular selección de la lista
        self.lista_favoritos.bind('<<ListboxSelect>>', self.mostrar_detalles_favorito)
        
        # Panel de detalles
        self.detalles_frame = tk.LabelFrame(
            panel_derecho,
            text=self.gestor_idiomas.obtener_texto("details"),
            bg="#f5f5f5",
            fg="#2c3e50",
            font=("Arial", 11, "bold"),
            padx=10,
            pady=10
        )
        self.detalles_frame.pack(fill='both', expand=True)
        
        # Nombre
        self.nombre_favorito_label = tk.Label(
            self.detalles_frame,
            text=self.gestor_idiomas.obtener_texto("name") + ":",
            bg="#f5f5f5",
            fg="#2c3e50",
            font=("Arial", 10, "bold"),
            anchor="w"
        )
        self.nombre_favorito_label.pack(fill='x', pady=(10, 0))
        
        self.lbl_nombre_fav = tk.Label(
            self.detalles_frame,
            text="",
            bg="#f5f5f5",
            fg="#2c3e50",
            font=("Arial", 10),
            anchor="w"
        )
        self.lbl_nombre_fav.pack(fill='x', pady=(0, 10))
        
        # Expresión
        self.expresion_favorito_label = tk.Label(
            self.detalles_frame,
            text=self.gestor_idiomas.obtener_texto("expression") + ":",
            bg="#f5f5f5",
            fg="#2c3e50",
            font=("Arial", 10, "bold"),
            anchor="w"
        )
        self.expresion_favorito_label.pack(fill='x', pady=(0, 0))
        
        self.lbl_expresion_fav = tk.Label(
            self.detalles_frame,
            text="",
            bg="#f5f5f5",
            fg="#2c3e50",
            font=("Arial", 10),
            anchor="w"
        )
        self.lbl_expresion_fav.pack(fill='x', pady=(0, 10))
        
        # Descripción
        self.descripcion_favorito_label = tk.Label(
            self.detalles_frame,
            text=self.gestor_idiomas.obtener_texto("description") + ":",
            bg="#f5f5f5",
            fg="#2c3e50",
            font=("Arial", 10, "bold"),
            anchor="w"
        )
        self.descripcion_favorito_label.pack(fill='x', pady=(0, 0))
        
        self.lbl_descripcion_fav = tk.Label(
            self.detalles_frame,
            text="",
            bg="#f5f5f5",
            fg="#2c3e50",
            font=("Arial", 10),
            anchor="w",
            wraplength=300
        )
        self.lbl_descripcion_fav.pack(fill='x', pady=(0, 10))
        
        # Fecha
        self.fecha_favorito_label = tk.Label(
            self.detalles_frame,
            text=self.gestor_idiomas.obtener_texto("creation_date") + ":",
            bg="#f5f5f5",
            fg="#2c3e50",
            font=("Arial", 10, "bold"),
            anchor="w"
        )
        self.fecha_favorito_label.pack(fill='x', pady=(0, 0))
        
        self.lbl_fecha_fav = tk.Label(
            self.detalles_frame,
            text="",
            bg="#f5f5f5",
            fg="#2c3e50",
            font=("Arial", 10),
            anchor="w"
        )
        self.lbl_fecha_fav.pack(fill='x', pady=(0, 10))
        
        # Botones de acción
        botones_frame = tk.Frame(self.detalles_frame, bg="#f5f5f5")
        botones_frame.pack(fill='x', pady=10)
        
        self.btn_cargar_favorito = tk.Button(
            botones_frame,
            text=self.gestor_idiomas.obtener_texto("load_calculator"),
            command=self.cargar_favorito_seleccionado,
            bg="#3498db",
            fg="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            padx=10,
            pady=5,
            cursor="hand2",
            state="disabled"
        )
        self.btn_cargar_favorito.pack(side=tk.LEFT, padx=(0, 10))
        
        self.btn_eliminar_favorito = tk.Button(
            botones_frame,
            text=self.gestor_idiomas.obtener_texto("delete"),
            command=self.eliminar_favorito,
            bg="#e74c3c",
            fg="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            padx=10,
            pady=5,
            cursor="hand2",
            state="disabled"
        )
        self.btn_eliminar_favorito.pack(side=tk.LEFT)
    def cargar_lista_favoritos(self):
        """Carga la lista de favoritos desde el gestor"""
        # Comprobar si la lista existe
        if not hasattr(self, 'lista_favoritos'):
            print("Lista de favoritos aún no inicializada")
            return
        
        try:
            # Limpiar la lista actual
            self.lista_favoritos.delete(0, tk.END)
            
            # Obtener favoritos
            favoritos = self.gestor_favoritos.obtener_favoritos()
            
            # Verificar si hay favoritos
            if not favoritos:
                print("No hay favoritos para cargar")
                return
            
            # Agregar a la lista
            for fav in favoritos:
                # Determinar tipo
                tipo = ""
                if "parametros" in fav and "tipo" in fav["parametros"]:
                    if fav["parametros"]["tipo"] == "sistema":
                        tipo = "[Sistema] "
                    elif fav["parametros"]["tipo"] == "raiz":
                        tipo = "[Raíz] "
                
                # Añadir a la lista con el prefijo de tipo
                self.lista_favoritos.insert(tk.END, f"{tipo}{fav['nombre']}")
            
            print(f"Cargados {len(favoritos)} favoritos")
            
        except Exception as e:
            print(f"Error al cargar lista de favoritos: {e}")

    def mostrar_detalles_favorito(self, event):
        """Muestra los detalles del favorito seleccionado"""
        # Obtener índice seleccionado
        try:
            index = self.lista_favoritos.curselection()[0]
            # Habilitar botones
            self.btn_cargar_fav.config(state="normal")
            self.btn_eliminar_fav.config(state="normal")
        except:
            # Si no hay selección, limpiar y deshabilitar
            self.limpiar_detalles_favorito()
            return
        
        # Obtener favorito
        favoritos = self.gestor_favoritos.obtener_favoritos()
        if index < len(favoritos):
            fav = favoritos[index]
            
            # Mostrar detalles
            self.lbl_nombre_fav.config(text=fav["nombre"])
            self.lbl_expresion_fav.config(text=fav["expresion"])
            self.lbl_descripcion_fav.config(text=fav.get("descripcion", ""))
            self.lbl_fecha_fav.config(text=fav.get("fecha_creacion", ""))

    def limpiar_detalles_favorito(self):
        """Limpia los detalles mostrados"""
        self.lbl_nombre_fav.config(text="")
        self.lbl_expresion_fav.config(text="")
        self.lbl_descripcion_fav.config(text="")
        self.lbl_fecha_fav.config(text="")
        self.btn_cargar_fav.config(state="disabled")
        self.btn_eliminar_fav.config(state="disabled")

    def eliminar_favorito(self):
        """Elimina el favorito seleccionado"""
        try:
            index = self.lista_favoritos.curselection()[0]
            nombre = self.lista_favoritos.get(index)
            
            # Confirmar eliminación
            if messagebox.askyesno("Confirmar eliminación", 
                                f"¿Está seguro de eliminar '{nombre}' de sus favoritos?"):
                # Eliminar favorito
                self.gestor_favoritos.eliminar_favorito(nombre)
                # Actualizar lista
                self.cargar_lista_favoritos()
                # Limpiar detalles
                self.limpiar_detalles_favorito()
                # Actualizar barra de estado
                self.status_bar.config(text=f"Favorito '{nombre}' eliminado correctamente")
        except:
            messagebox.showerror("Error", "No se pudo eliminar el favorito")

    def cargar_favorito_seleccionado(self):
        """Carga el favorito seleccionado en la calculadora correspondiente"""
        try:
            index = self.lista_favoritos.curselection()[0]
            favoritos = self.gestor_favoritos.obtener_favoritos()
            if index < len(favoritos):
                fav = favoritos[index]
                
                # Determinar si es un sistema o una función
                es_sistema = False
                if "parametros" in fav and "tipo" in fav["parametros"]:
                    es_sistema = fav["parametros"]["tipo"] == "sistema"
                else:
                    # Método antiguo (para compatibilidad)
                    es_sistema = fav["expresion"].startswith("Sistema:")
                
                print(f"Cargando favorito: {fav['nombre']}, tipo: {'sistema' if es_sistema else 'raíz'}")
                
                if es_sistema:
                    # Cargar sistema de ecuaciones
                    self.notebook.select(self.tab_sistemas)  # Cambiar a la pestaña de sistemas
                    
                    if "parametros" in fav:
                        # Cargar matriz A
                        if "matriz_a" in fav["parametros"]:
                            self.txt_matriz_a.delete("1.0", tk.END)
                            self.txt_matriz_a.insert("1.0", fav["parametros"]["matriz_a"])
                        
                        # Cargar vector b
                        if "vector_b" in fav["parametros"]:
                            self.txt_vector_b.delete(0, tk.END)
                            self.txt_vector_b.insert(0, fav["parametros"]["vector_b"])
                        
                        # Cargar vector x0 si existe
                        if "x0" in fav["parametros"]:
                            self.txt_vector_x0.delete(0, tk.END)
                            self.txt_vector_x0.insert(0, fav["parametros"]["x0"])
                        
                        # Establecer método
                        if "metodo" in fav["parametros"]:
                            self.metodo_var.set(fav["parametros"]["metodo"])
                    
                else:
                    # Cargar función de búsqueda de raíces
                    self.notebook.select(self.tab_raices)  # Cambiar a la pestaña de raíces
                    
                    # Cargar expresión
                    self.entry_funcion.delete(0, tk.END)
                    self.entry_funcion.insert(0, fav["expresion"])
                    
                    # Cargar parámetros si existen
                    if "parametros" in fav:
                        if "a" in fav["parametros"]:
                            self.entry_a.delete(0, tk.END)
                            self.entry_a.insert(0, str(fav["parametros"]["a"]))
                        if "b" in fav["parametros"]:
                            self.entry_b.delete(0, tk.END)
                            self.entry_b.insert(0, str(fav["parametros"]["b"]))
                
                # Actualizar barra de estado
                self.status_bar.config(text=f"Favorito '{fav['nombre']}' cargado correctamente")
                
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el favorito: {str(e)}")
            print(f"Error al cargar favorito: {e}")  # Para depuración
    def guardar_favorito_raices(self):
                """Guarda la función actual como favorito"""
                # Obtener datos actuales
                funcion = self.entry_funcion.get()
                if not funcion:
                    messagebox.showerror("Error", "La función no puede estar vacía")
                    return
                
                # Obtener parámetros
                parametros = {
                    "tipo": "raiz"  # Añadir indicador de tipo
                }
                
                try:
                    a = float(self.entry_a.get())
                    parametros["a"] = a
                    
                    # Solo agregar b si está habilitado
                    if self.entry_b.cget("state") != "disabled":
                        b = float(self.entry_b.get())
                        parametros["b"] = b
                except ValueError:
                    # Si hay error de conversión, continuar con advertencia
                    messagebox.showwarning("Advertencia", "No se pudieron convertir algunos parámetros a números. Se guardarán como texto.")
                    parametros["a"] = self.entry_a.get()
                    if self.entry_b.cget("state") != "disabled":
                        parametros["b"] = self.entry_b.get()
                
                # Solicitar nombre y descripción
                nombre = simpledialog.askstring("Guardar como favorito", 
                                            "Ingrese un nombre para este favorito:",
                                            parent=self.master)
                if not nombre:
                    return  # Cancelado por el usuario
                
                descripcion = simpledialog.askstring("Descripción (opcional)", 
                                                "Ingrese una descripción (opcional):",
                                                parent=self.master)
                
                # Guardar favorito
                try:
                    self.gestor_favoritos.agregar_favorito(nombre, funcion, descripcion, parametros)
                    
                    # Agregar también al historial
                    metodo = self.metodo_raices_var.get()
                    self.gestor_favoritos.agregar_al_historial(funcion, metodo, parametros)
                    
                    # Forzar la recarga de la lista de favoritos independientemente de la pestaña actual
                    self.cargar_lista_favoritos()
                    
                    # Actualizar barra de estado
                    self.status_bar.config(text=f"Función guardada como favorito: '{nombre}'")
                    
                    # Mostrar mensaje de éxito
                    messagebox.showinfo("Éxito", f"La función '{nombre}' ha sido guardada como favorito")
                    
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo guardar el favorito: {str(e)}")
                    print(f"Error al guardar favorito: {e}")  # Para depuración
                
    def guardar_favorito_sistemas(self):
        """Guarda el sistema actual como favorito"""
        # Obtener matriz A y vector b
        matriz_a_text = self.txt_matriz_a.get("1.0", tk.END).strip()
        vector_b_text = self.txt_vector_b.get().strip()
        
        if not matriz_a_text or not vector_b_text:
            messagebox.showerror("Error", "La matriz A y el vector b no pueden estar vacíos")
            return
        
        # Validar el formato de la matriz y vector
        try:
            # Usar Validar_txt para verificar formato
            valido_a, _ = vt.validar_matriz_texto(matriz_a_text)
            if not valido_a:
                messagebox.showerror("Error", "El formato de la matriz A no es válido")
                return
                
            valido_b, _ = vt.validar_vector_texto(vector_b_text)
            if not valido_b:
                messagebox.showerror("Error", "El formato del vector b no es válido")
                return
        except Exception as e:
            messagebox.showerror("Error de validación", f"Error al validar los datos: {str(e)}")
            return
        
        # Crear una expresión representativa
        expresion = f"Sistema: {matriz_a_text} | {vector_b_text}"
        
        # Obtener parámetros
        parametros = {
            "matriz_a": matriz_a_text,
            "vector_b": vector_b_text,
            "metodo": self.metodo_var.get(),
            "tipo": "sistema"  # Añadir indicador de tipo
        }
        
        # Intentar agregar x0 si existe
        x0_text = self.txt_vector_x0.get().strip()
        if x0_text:
            try:
                valido_x0, _ = vt.validar_vector_texto(x0_text)
                if valido_x0:
                    parametros["x0"] = x0_text
                else:
                    if messagebox.askyesno("Advertencia", 
                                        "El formato del vector x0 no es válido. ¿Desea continuar sin incluirlo?"):
                        pass  # Continuar sin x0
                    else:
                        return  # Cancelar la operación
            except:
                # Ignorar x0 si hay error
                pass
        
        # Solicitar nombre y descripción
        nombre = simpledialog.askstring("Guardar como favorito", 
                                    "Ingrese un nombre para este sistema:",
                                    parent=self.master)
        if not nombre:
            return  # Cancelado por el usuario
        
        descripcion = simpledialog.askstring("Descripción (opcional)", 
                                        "Ingrese una descripción (opcional):",
                                        parent=self.master)
        
        # Guardar favorito
        try:
            self.gestor_favoritos.agregar_favorito(nombre, expresion, descripcion, parametros)
            
            # Agregar también al historial
            metodo = self.metodo_var.get()
            self.gestor_favoritos.agregar_al_historial(expresion, metodo, parametros)
            
            # Forzar la recarga de la lista de favoritos independientemente de la pestaña actual
            self.cargar_lista_favoritos()
            
            # Actualizar barra de estado
            self.status_bar.config(text=f"Sistema guardado como favorito: '{nombre}'")
            
            # Mostrar mensaje de éxito
            messagebox.showinfo("Éxito", f"El sistema '{nombre}' ha sido guardado como favorito")
            
        except Exception as e:
            # Mostrar el error específico
            messagebox.showerror("Error", f"No se pudo guardar el favorito: {str(e)}")
            print(f"Error al guardar favorito: {e}")  # Para depuración
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
