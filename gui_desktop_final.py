# Este archivo contiene solo los métodos que necesitas agregar al archivo gui_desktop_corregido.py

# AGREGAR ESTAS IMPORTACIONES AL INICIO DEL ARCHIVO:
# from metodos_integracion import regla_trapecios, simpson_1_3, simpson_3_8
# from metodos_ecuaciones_diferenciales import runge_kutta_1er_orden, runge_kutta_4to_orden, calcular_k_values, mostrar_k_values_detallado

# AGREGAR ESTAS PESTAÑAS EN EL __init__ DESPUÉS DE tab_sistemas:
# self.tab_integracion = tk.Frame(self.notebook, bg="#f5f5f5")
# self.notebook.add(self.tab_integracion, text="Integración")
# 
# self.tab_ecuaciones_diff = tk.Frame(self.notebook, bg="#f5f5f5")
# self.notebook.add(self.tab_ecuaciones_diff, text="Ecuaciones Diferenciales")

# AGREGAR ESTAS LLAMADAS EN EL __init__ DESPUÉS DE setup_tab_sistemas():
# self.setup_tab_integracion()
# self.setup_tab_ecuaciones_diff()

# MÉTODOS PARA AGREGAR AL FINAL DE LA CLASE:

def setup_tab_integracion(self):
    """Configura la pestaña de integración numérica"""
    # Panel principal dividido en dos
    panel_frame = tk.Frame(self.tab_integracion, bg="#f5f5f5")
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
        text="Método de Integración",
        bg="#f5f5f5",
        fg="#2c3e50",
        font=("Arial", 11, "bold"),
        padx=10,
        pady=10
    )
    metodo_frame.pack(fill='x', pady=(0, 10))
    
    self.metodo_integracion_var = tk.StringVar()
    metodos_int = ["Regla de los Trapecios", "Simpson 1/3", "Simpson 3/8"]
    
    self.combo_metodo_integracion = ttk.Combobox(
        metodo_frame,
        textvariable=self.metodo_integracion_var,
        values=metodos_int,
        state="readonly",
        width=20,
        font=("Arial", 10)
    )
    self.combo_metodo_integracion.pack(pady=5)
    self.combo_metodo_integracion.current(0)
    
    # Frame para entrada de función
    funcion_int_frame = tk.LabelFrame(
        panel_izquierdo,
        text="Función a Integrar",
        bg="#f5f5f5",
        fg="#2c3e50",
        font=("Arial", 11, "bold"),
        padx=10,
        pady=10
    )
    funcion_int_frame.pack(fill='x', pady=10)
    
    tk.Label(
        funcion_int_frame,
        text="f(x) =",
        bg="#f5f5f5",
        fg="#2c3e50",
        font=("Arial", 10)
    ).pack(anchor="w", pady=(0, 5))
    
    self.entry_funcion_int = tk.Entry(
        funcion_int_frame,
        font=("Courier New", 10),
        bg="white",
        fg="#2c3e50",
        relief="solid",
        bd=1
    )
    self.entry_funcion_int.pack(fill='x', pady=(0, 10))
    self.entry_funcion_int.insert(0, "x**2")  # Función de ejemplo
    
    # Frame para límites de integración
    limites_frame = tk.LabelFrame(
        panel_izquierdo,
        text="Límites de Integración",
        bg="#f5f5f5",
        fg="#2c3e50",
        font=("Arial", 11, "bold"),
        padx=10,
        pady=10
    )
    limites_frame.pack(fill='x', pady=10)
    
    # Límite inferior
    tk.Label(
        limites_frame,
        text="Límite inferior (a):",
        bg="#f5f5f5",
        fg="#2c3e50",
        font=("Arial", 10)
    ).pack(anchor="w")
    
    self.entry_a_int = tk.Entry(
        limites_frame,
        font=("Courier New", 10),
        bg="white",
        fg="#2c3e50",
        relief="solid",
        bd=1
    )
    self.entry_a_int.pack(fill='x', pady=(0, 10))
    self.entry_a_int.insert(0, "0")
    
    # Límite superior
    tk.Label(
        limites_frame,
        text="Límite superior (b):",
        bg="#f5f5f5",
        fg="#2c3e50",
        font=("Arial", 10)
    ).pack(anchor="w")
    
    self.entry_b_int = tk.Entry(
        limites_frame,
        font=("Courier New", 10),
        bg="white",
        fg="#2c3e50",
        relief="solid",
        bd=1
    )
    self.entry_b_int.pack(fill='x', pady=(0, 10))
    self.entry_b_int.insert(0, "1")
    
    # Número de intervalos
    tk.Label(
        limites_frame,
        text="Número de intervalos (n):",
        bg="#f5f5f5",
        fg="#2c3e50",
        font=("Arial", 10)
    ).pack(anchor="w")
    
    self.entry_n_int = tk.Entry(
        limites_frame,
        font=("Courier New", 10),
        bg="white",
        fg="#2c3e50",
        relief="solid",
        bd=1
    )
    self.entry_n_int.pack(fill='x', pady=(0, 10))
    self.entry_n_int.insert(0, "100")
    
    # Botón para calcular
    btn_frame_int = tk.Frame(panel_izquierdo, bg="#f5f5f5")
    btn_frame_int.pack(fill='x', pady=10)
    
    self.btn_calcular_integral = tk.Button(
        btn_frame_int,
        text="Calcular Integral",
        command=self.calcular_integral,
        bg="#3498db",
        fg="white",
        font=("Arial", 10, "bold"),
        relief="flat",
        padx=10,
        pady=5,
        cursor="hand2"
    )
    self.btn_calcular_integral.pack(side=tk.RIGHT)
    
    # ===== PANEL DERECHO =====
    # Frame para resultados
    resultados_int_frame = tk.LabelFrame(
        panel_derecho,
        text="Resultados",
        bg="#f5f5f5",
        fg="#2c3e50",
        font=("Arial", 11, "bold"),
        padx=10,
        pady=10
    )
    resultados_int_frame.pack(fill='both', expand=True)
    
    # Área de texto para mostrar resultados
    self.txt_resultados_int = scrolledtext.ScrolledText(
        resultados_int_frame,
        width=45,
        height=25,
        font=("Courier New", 10),
        bg="white",
        fg="#2c3e50"
    )
    self.txt_resultados_int.pack(fill='both', expand=True, pady=5)

def setup_tab_ecuaciones_diff(self):
    """Configura la pestaña de ecuaciones diferenciales"""
    # Panel principal dividido en dos
    panel_frame = tk.Frame(self.tab_ecuaciones_diff, bg="#f5f5f5")
    panel_frame.pack(fill='both', expand=True, padx=10, pady=10)
    
    # Panel izquierdo para entrada de datos
    panel_izquierdo = tk.Frame(panel_frame, bg="#f5f5f5")
    panel_izquierdo.pack(side=tk.LEFT, fill='both', expand=True, padx=(0, 5))
    
    # Panel derecho para resultados
    panel_derecho = tk.Frame(panel_frame, bg="#f5f5f5")
    panel_derecho.pack(side=tk.RIGHT, fill='both', expand=True, padx=(5, 0))
    
    # ===== PANEL IZQUIERDO =====
    # Frame para selección de método
    metodo_edo_frame = tk.LabelFrame(
        panel_izquierdo,
        text="Método de Resolución",
        bg="#f5f5f5",
        fg="#2c3e50",
        font=("Arial", 11, "bold"),
        padx=10,
        pady=10
    )
    metodo_edo_frame.pack(fill='x', pady=(0, 10))
    
    self.metodo_edo_var = tk.StringVar()
    metodos_edo = ["Runge-Kutta 1er Orden (Euler)", "Runge-Kutta 4to Orden"]
    
    self.combo_metodo_edo = ttk.Combobox(
        metodo_edo_frame,
        textvariable=self.metodo_edo_var,
        values=metodos_edo,
        state="readonly",
        width=25,
        font=("Arial", 10)
    )
    self.combo_metodo_edo.pack(pady=5)
    self.combo_metodo_edo.current(0)
    
    # Frame para ecuación diferencial
    ecuacion_frame = tk.LabelFrame(
        panel_izquierdo,
        text="Ecuación Diferencial",
        bg="#f5f5f5",
        fg="#2c3e50",
        font=("Arial", 11, "bold"),
        padx=10,
        pady=10
    )
    ecuacion_frame.pack(fill='x', pady=10)
    
    tk.Label(
        ecuacion_frame,
        text="dy/dx = f(x,y) =",
        bg="#f5f5f5",
        fg="#2c3e50",
        font=("Arial", 10)
    ).pack(anchor="w", pady=(0, 5))
    
    self.entry_ecuacion_diff = tk.Entry(
        ecuacion_frame,
        font=("Courier New", 10),
        bg="white",
        fg="#2c3e50",
        relief="solid",
        bd=1
    )
    self.entry_ecuacion_diff.pack(fill='x', pady=(0, 10))
    self.entry_ecuacion_diff.insert(0, "x + y")  # Ecuación de ejemplo
    
    # Frame para condiciones iniciales
    condiciones_frame = tk.LabelFrame(
        panel_izquierdo,
        text="Condiciones Iniciales y Parámetros",
        bg="#f5f5f5",
        fg="#2c3e50",
        font=("Arial", 11, "bold"),
        padx=10,
        pady=10
    )
    condiciones_frame.pack(fill='x', pady=10)
    
    # x0
    tk.Label(
        condiciones_frame,
        text="x₀ (valor inicial de x):",
        bg="#f5f5f5",
        fg="#2c3e50",
        font=("Arial", 10)
    ).pack(anchor="w")
    
    self.entry_x0_edo = tk.Entry(
        condiciones_frame,
        font=("Courier New", 10),
        bg="white",
        fg="#2c3e50",
        relief="solid",
        bd=1
    )
    self.entry_x0_edo.pack(fill='x', pady=(0, 10))
    self.entry_x0_edo.insert(0, "0")
    
    # y0
    tk.Label(
        condiciones_frame,
        text="y₀ (valor inicial de y):",
        bg="#f5f5f5",
        fg="#2c3e50",
        font=("Arial", 10)
    ).pack(anchor="w")
    
    self.entry_y0_edo = tk.Entry(
        condiciones_frame,
        font=("Courier New", 10),
        bg="white",
        fg="#2c3e50",
        relief="solid",
        bd=1
    )
    self.entry_y0_edo.pack(fill='x', pady=(0, 10))
    self.entry_y0_edo.insert(0, "1")
    
    # h (tamaño del paso)
    tk.Label(
        condiciones_frame,
        text="h (tamaño del paso):",
        bg="#f5f5f5",
        fg="#2c3e50",
        font=("Arial", 10)
    ).pack(anchor="w")
    
    self.entry_h_edo = tk.Entry(
        condiciones_frame,
        font=("Courier New", 10),
        bg="white",
        fg="#2c3e50",
        relief="solid",
        bd=1
    )
    self.entry_h_edo.pack(fill='x', pady=(0, 10))
    self.entry_h_edo.insert(0, "0.1")
    
    # x_final
    tk.Label(
        condiciones_frame,
        text="x_final (valor final de x):",
        bg="#f5f5f5",
        fg="#2c3e50",
        font=("Arial", 10)
    ).pack(anchor="w")
    
    self.entry_x_final_edo = tk.Entry(
        condiciones_frame,
        font=("Courier New", 10),
        bg="white",
        fg="#2c3e50",
        relief="solid",
        bd=1
    )
    self.entry_x_final_edo.pack(fill='x', pady=(0, 10))
    self.entry_x_final_edo.insert(0, "1")
    
    # Botones
    btn_frame_edo = tk.Frame(panel_izquierdo, bg="#f5f5f5")
    btn_frame_edo.pack(fill='x', pady=10)
    
    self.btn_resolver_edo = tk.Button(
        btn_frame_edo,
        text="Resolver EDO",
        command=self.resolver_ecuacion_diferencial,
        bg="#3498db",
        fg="white",
        font=("Arial", 10, "bold"),
        relief="flat",
        padx=10,
        pady=5,
        cursor="hand2"
    )
    self.btn_resolver_edo.pack(side=tk.RIGHT, padx=(5, 0))
    
    self.btn_mostrar_k_values = tk.Button(
        btn_frame_edo,
        text="Mostrar cálculo de k",
        command=self.mostrar_calculo_k,
        bg="#2ecc71",
        fg="white",
        font=("Arial", 10, "bold"),
        relief="flat",
        padx=10,
        pady=5,
        cursor="hand2"
    )
    self.btn_mostrar_k_values.pack(side=tk.RIGHT)
    
    # ===== PANEL DERECHO =====
    # Frame para resultados
    resultados_edo_frame = tk.LabelFrame(
        panel_derecho,
        text="Resultados",
        bg="#f5f5f5",
        fg="#2c3e50",
        font=("Arial", 11, "bold"),
        padx=10,
        pady=10
    )
    resultados_edo_frame.pack(fill='both', expand=True)
    
    # Área de texto para mostrar resultados
    self.txt_resultados_edo = scrolledtext.ScrolledText(
        resultados_edo_frame,
        width=45,
        height=25,
        font=("Courier New", 10),
        bg="white",
        fg="#2c3e50"
    )
    self.txt_resultados_edo.pack(fill='both', expand=True, pady=5)

def calcular_integral(self):
    """Calcula la integral usando el método seleccionado"""
    try:
        # Obtener datos de entrada
        f_str = self.entry_funcion_int.get().strip()
        if not f_str:
            messagebox.showerror("Error", "La función no puede estar vacía")
            return
        
        a = float(self.entry_a_int.get())
        b = float(self.entry_b_int.get())
        n = int(self.entry_n_int.get())
        
        # Convertir función a expresión simbólica
        from sympy import Symbol, sympify
        x = Symbol('x')
        f = sympify(f_str)
        
        # Obtener método seleccionado
        metodo = self.metodo_integracion_var.get()
        
        # Limpiar resultados anteriores
        self.txt_resultados_int.delete("1.0", tk.END)
        
        # Calcular según el método
        if metodo == "Regla de los Trapecios":
            resultado, pasos = regla_trapecios(f, a, b, n)
        elif metodo == "Simpson 1/3":
            resultado, pasos = simpson_1_3(f, a, b, n)
        elif metodo == "Simpson 3/8":
            resultado, pasos = simpson_3_8(f, a, b, n)
        
        if resultado is not None:
            self.mostrar_resultados_integracion(resultado, pasos)
            self.status_bar.config(text=f"Integral calculada: {resultado:.8f}")
        
    except Exception as e:
        messagebox.showerror("Error", f"Error al calcular la integral: {e}")
        self.status_bar.config(text=f"Error: {str(e)}")

def mostrar_resultados_integracion(self, resultado, pasos):
    """Muestra los resultados de la integración"""
    self.txt_resultados_int.insert(tk.END, f"MÉTODO: {pasos['metodo']}\n")
    self.txt_resultados_int.insert(tk.END, "="*50 + "\n\n")
    self.txt_resultados_int.insert(tk.END, f"Función: f(x) = {pasos['funcion']}\n")
    self.txt_resultados_int.insert(tk.END, f"Límites: [{pasos['limites'][0]}, {pasos['limites'][1]}]\n")
    self.txt_resultados_int.insert(tk.END, f"Número de intervalos: {pasos['n_intervalos']}\n")
    self.txt_resultados_int.insert(tk.END, f"Tamaño del paso (h): {pasos['h']:.6f}\n\n")
    
    self.txt_resultados_int.insert(tk.END, f"RESULTADO:\n")
    self.txt_resultados_int.insert(tk.END, f"∫ f(x) dx ≈ {resultado:.8f}\n\n")
    
    # Mostrar algunos puntos de evaluación
    self.txt_resultados_int.insert(tk.END, "PUNTOS DE EVALUACIÓN (primeros 10):\n")
    for i in range(min(10, len(pasos['puntos_x']))):
        x_val = pasos['puntos_x'][i]
        y_val = pasos['puntos_y'][i]
        self.txt_resultados_int.insert(tk.END, f"f({x_val:.4f}) = {y_val:.6f}\n")
    
    if len(pasos['puntos_x']) > 10:
        self.txt_resultados_int.insert(tk.END, f"... y {len(pasos['puntos_x']) - 10} puntos más\n")

def resolver_ecuacion_diferencial(self):
    """Resuelve la ecuación diferencial usando el método seleccionado"""
    try:
        # Obtener datos de entrada
        f_str = self.entry_ecuacion_diff.get().strip()
        if not f_str:
            messagebox.showerror("Error", "La ecuación diferencial no puede estar vacía")
            return
        
        x0 = float(self.entry_x0_edo.get())
        y0 = float(self.entry_y0_edo.get())
        h = float(self.entry_h_edo.get())
        x_final = float(self.entry_x_final_edo.get())
        
        # Convertir función a expresión simbólica
        from sympy import Symbol, sympify
        x, y = Symbol('x'), Symbol('y')
        f = sympify(f_str)
        
        # Obtener método seleccionado
        metodo = self.metodo_edo_var.get()
        
        # Limpiar resultados anteriores
        self.txt_resultados_edo.delete("1.0", tk.END)
        
        # Resolver según el método
        if "1er Orden" in metodo:
            solucion, pasos = runge_kutta_1er_orden(f, x0, y0, h, x_final)
        elif "4to Orden" in metodo:
            solucion, pasos = runge_kutta_4to_orden(f, x0, y0, h, x_final)
        
        if solucion is not None:
            self.mostrar_resultados_edo(solucion, pasos)
            self.status_bar.config(text=f"EDO resuelta con {pasos['n_pasos']} pasos")
        
    except Exception as e:
        messagebox.showerror("Error", f"Error al resolver la EDO: {e}")
        self.status_bar.config(text=f"Error: {str(e)}")

def mostrar_resultados_edo(self, solucion, pasos):
    """Muestra los resultados de la ecuación diferencial"""
    self.txt_resultados_edo.insert(tk.END, f"MÉTODO: {pasos['metodo']}\n")
    self.txt_resultados_edo.insert(tk.END, "="*50 + "\n\n")
    self.txt_resultados_edo.insert(tk.END, f"Ecuación: dy/dx = {pasos['ecuacion']}\n")
    self.txt_resultados_edo.insert(tk.END, f"Condiciones iniciales: (x₀, y₀) = {pasos['condiciones_iniciales']}\n")
    self.txt_resultados_edo.insert(tk.END, f"Tamaño del paso: h = {pasos['h']}\n")
    self.txt_resultados_edo.insert(tk.END, f"Valor final de x: {pasos['x_final']}\n")
    self.txt_resultados_edo.insert(tk.END, f"Número de pasos: {pasos['n_pasos']}\n\n")
    
    self.txt_resultados_edo.insert(tk.END, "SOLUCIÓN:\n")
    self.txt_resultados_edo.insert(tk.END, f"{'i':<3} {'x':<10} {'y':<12}\n")
    self.txt_resultados_edo.insert(tk.END, "-"*25 + "\n")
    
    for i, (x_val, y_val) in enumerate(solucion):
        self.txt_resultados_edo.insert(tk.END, f"{i:<3} {x_val:<10.4f} {y_val:<12.6f}\n")
    
    # Mostrar algunos pasos detallados si es Runge-Kutta 4to orden
    if "4to Orden" in pasos['metodo'] and len(pasos['pasos_detallados']) > 0:
        self.txt_resultados_edo.insert(tk.END, f"\nPRIMEROS 3 PASOS DETALLADOS:\n")
        for i, paso in enumerate(pasos['pasos_detallados'][:3]):
            self.txt_resultados_edo.insert(tk.END, f"\nPaso {paso['iteracion']}:\n")
            self.txt_resultados_edo.insert(tk.END, f"  k1 = {paso['k1']:.6f}\n")
            self.txt_resultados_edo.insert(tk.END, f"  k2 = {paso['k2']:.6f}\n")
            self.txt_resultados_edo.insert(tk.END, f"  k3 = {paso['k3']:.6f}\n")
            self.txt_resultados_edo.insert(tk.END, f"  k4 = {paso['k4']:.6f}\n")
            self.txt_resultados_edo.insert(tk.END, f"  y_{paso['iteracion']} = {paso['y_next']:.6f}\n")

def mostrar_calculo_k(self):
    """Muestra el cálculo detallado de los valores k para un paso"""
    try:
        # Obtener datos de entrada
        f_str = self.entry_ecuacion_diff.get().strip()
        if not f_str:
            messagebox.showerror("Error", "La ecuación diferencial no puede estar vacía")
            return
        
        x0 = float(self.entry_x0_edo.get())
        y0 = float(self.entry_y0_edo.get())
        h = float(self.entry_h_edo.get())
        
        # Convertir función a expresión simbólica
        from sympy import Symbol, sympify
        f = sympify(f_str)
        
        # Mostrar cálculo detallado
        descripcion = mostrar_k_values_detallado(f, x0, y0, h)
        
        # Crear ventana emergente para mostrar el cálculo
        ventana_k = tk.Toplevel(self.master)
        ventana_k.title("Cálculo detallado de valores k")
        ventana_k.geometry("600x500")
        ventana_k.configure(bg="#f5f5f5")
        
        # Área de texto con scroll
        frame_k = tk.Frame(ventana_k, bg="#f5f5f5")
        frame_k.pack(fill='both', expand=True, padx=10, pady=10)
        
        txt_k = scrolledtext.ScrolledText(
            frame_k,
            width=70,
            height=25,
            font=("Courier New", 10),
            bg="white",
            fg="#2c3e50"
        )
        txt_k.pack(fill='both', expand=True)
        txt_k.insert(tk.END, descripcion)
        txt_k.config(state='disabled')
        
    except Exception as e:
        messagebox.showerror("Error", f"Error al calcular valores k: {e}")