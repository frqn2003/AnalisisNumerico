
import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.uix.togglebutton import ToggleButton
from kivy.graphics import Color, Rectangle, Line, Ellipse
from kivy.core.window import Window
from kivy.clock import Clock
import math
import sys
import io
import os

try:
    import matplotlib.pyplot as plt
    from matplotlib import rc
    from kivy.core.image import Image as CoreImage
    import numpy as np
    MATPLOTLIB = True
except ImportError:
    MATPLOTLIB = False

try:
    import imageio
    from PIL import Image as PILImage
    IMAGEIO = True
except ImportError:
    IMAGEIO = False

Window.clearcolor = (0, 0, 0, 1)

def safe_eval(expr, x):
    allowed_names = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}
    allowed_names["x"] = x
    return eval(expr, {"__builtins__": {}}, allowed_names)

class IOSDarkBackground(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            Color(0, 0, 0, 1)
            self.bg = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_bg, size=self.update_bg)
    def update_bg(self, *a):
        self.bg.pos = self.pos
        self.bg.size = self.size

class IOSDarkLabel(Label):
    def __init__(self, **kwargs):
        kwargs.setdefault("color", (1, 1, 1, 1))
        kwargs.setdefault("font_size", 18)
        kwargs.setdefault("halign", "left")
        kwargs.setdefault("valign", "middle")
        kwargs.setdefault("text_size", (None, None))
        super().__init__(**kwargs)

class IOSDarkInput(TextInput):
    def __init__(self, **kwargs):
        kwargs.setdefault("background_color", (0, 0, 0, 1))
        kwargs.setdefault("foreground_color", (1, 1, 1, 1))
        kwargs.setdefault("cursor_color", (1, 1, 1, 1))
        kwargs.setdefault("hint_text_color", (1, 1, 1, 1))
        kwargs.setdefault("font_size", 18)
        kwargs.setdefault("padding", [12, 12, 12, 12])
        kwargs.setdefault("size_hint_y", None)
        kwargs.setdefault("height", 48)
        super().__init__(**kwargs)
        with self.canvas.after:
            Color(1, 1, 1, 0.25)
            self.rect = Line(rectangle=(self.x, self.y, self.width, self.height), width=1.5)
        self.bind(pos=self.update_rect, size=self.update_rect)
    def update_rect(self, *a):
        self.rect.rectangle = (self.x, self.y, self.width, self.height)

class IOSDarkButton(Button):
    def __init__(self, **kwargs):
        kwargs.setdefault("background_color", (0.1, 0.4, 1, 1))
        kwargs.setdefault("color", (1, 1, 1, 1))
        kwargs.setdefault("font_size", 18)
        kwargs.setdefault("size_hint_y", None)
        kwargs.setdefault("height", 48)
        kwargs.setdefault("background_normal", "")
        kwargs.setdefault("background_down", "")
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(0.1, 0.4, 1, 1)
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)
    def update_rect(self, *a):
        self.rect.pos = self.pos
        self.rect.size = self.size

class MathKeyboard(BoxLayout):
    def __init__(self, target_input, **kwargs):
        super().__init__(orientation="horizontal", size_hint_y=None, height=48, spacing=4, **kwargs)
        self.target_input = target_input
        keys = [
            "(", ")", "^", "√", "π", "e", "sin", "cos", "tan", "log", "ln", "+", "-", "*", "/", "x"
        ]
        for k in keys:
            b = Button(text=k, font_size=18, background_color=(0.12,0.12,0.12,1), color=(1,1,1,1), size_hint_x=None, width=48)
            b.bind(on_release=self.insert_key)
            self.add_widget(b)
    def insert_key(self, instance):
        k = instance.text
        if k == "^":
            k = "**"
        elif k == "√":
            k = "sqrt("
        elif k == "π":
            k = "pi"
        elif k == "e":
            k = "e"
        elif k == "ln":
            k = "log("
        self.target_input.insert_text(k)

class FunctionPlot(FloatLayout):
    def __init__(self, func_expr, a, b, pasos=None, paso_idx=None, raiz=None, latex_img=None, **kwargs):
        super().__init__(**kwargs)
        self.func_expr = func_expr
        self.a = a
        self.b = b
        self.pasos = pasos or []
        self.paso_idx = paso_idx
        self.raiz = raiz
        self.latex_img = latex_img
        self.bind(pos=self.redraw, size=self.redraw)
        Clock.schedule_once(lambda dt: self.redraw())
    def redraw(self, *a):
        self.canvas.clear()
        with self.canvas:
            Color(1,1,1,1)
            w, h = self.width, self.height
            x0, y0 = self.x, self.y
            if self.latex_img:
                img = CoreImage(self.latex_img, ext="png")
                Rectangle(texture=img.texture, pos=(x0+10, y0+h-60), size=(min(w-20, 200), 40))
            Color(0.5,0.5,0.5,1)
            Line(points=[x0+20, y0+h/2, x0+w-20, y0+h/2], width=1)
            Line(points=[x0+w/2, y0+20, x0+w/2, y0+h-20], width=1)
            Color(0.1,0.7,1,1)
            N = 200
            X = [self.a + (self.b-self.a)*i/(N-1) for i in range(N)]
            Y = []
            ymin, ymax = 0, 0
            for x in X:
                try:
                    y = safe_eval(self.func_expr, x)
                except:
                    y = 0
                Y.append(y)
                ymin = min(ymin, y)
                ymax = max(ymax, y)
            if ymax==ymin: ymax=ymin+1
            scale_x = (w-40)/(self.b-self.a)
            scale_y = (h-40)/(ymax-ymin)
            pts = []
            for i in range(N):
                px = x0+20 + (X[i]-self.a)*scale_x
                py = y0+20 + (Y[i]-ymin)*scale_y
                pts += [px, py]
            Line(points=pts, width=2)
            if self.pasos and self.paso_idx is not None:
                p = self.pasos[self.paso_idx]
                if "a" in p and "b" in p:
                    Color(1,1,0,0.2)
                    ax = x0+20 + (p["a"]-self.a)*scale_x
                    bx = x0+20 + (p["b"]-self.a)*scale_x
                    Rectangle(pos=(min(ax,bx), y0+20), size=(abs(bx-ax), h-40))
                if "c" in p:
                    Color(1,0,0,1)
                    cx = x0+20 + (p["c"]-self.a)*scale_x
                    cy = y0+20 + (safe_eval(self.func_expr, p["c"])-ymin)*scale_y
                    Ellipse(pos=(cx-6, cy-6), size=(12,12))
            if self.raiz is not None:
                Color(0,1,0,1)
                rx = x0+20 + (self.raiz-self.a)*scale_x
                ry = y0+20 + (safe_eval(self.func_expr, self.raiz)-ymin)*scale_y
                Ellipse(pos=(rx-7, ry-7), size=(14,14))

class DemoInnovadorLayout(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bg = IOSDarkBackground(size_hint=(1,1), pos_hint={'x':0,'y':0})
        self.add_widget(self.bg)
        self.historial = []
        self.modo = "Raíces"
        self.metodos_raices = ["Bisección", "Newton-Raphson", "Secante", "Regula Falsi"]
        self.metodos_sistemas = ["Gauss-Jordan", "Jacobi", "Gauss-Seidel"]
        self.metodo = self.metodos_raices[0]
        self.pasos = []
        self.paso_idx = 0
        self.latex_img = None
        self.latex_expr = ""
        self.raiz = None
        self.solucion_sistema = None
        self.pasos_sistema = []
        self.paso_idx_sistema = 0

        scroll = ScrollView(size_hint=(1, 1))
        self.main_box = BoxLayout(orientation="vertical", spacing=18, padding=[24, 32, 24, 32], size_hint_y=None)
        self.main_box.bind(minimum_height=self.main_box.setter('height'))
        scroll.add_widget(self.main_box)
        self.add_widget(scroll)

        switch_box = BoxLayout(orientation="horizontal", size_hint_y=None, height=40, spacing=8)
        self.btn_raices = ToggleButton(text="Raíces", group="modo", state="down", background_color=(0.2,0.2,0.2,1), color=(1,1,1,1))
        self.btn_sistemas = ToggleButton(text="Sistemas", group="modo", background_color=(0.2,0.2,0.2,1), color=(1,1,1,1))
        self.btn_raices.bind(on_release=lambda x:self.cambiar_modo("Raíces"))
        self.btn_sistemas.bind(on_release=lambda x:self.cambiar_modo("Sistemas"))
        switch_box.add_widget(self.btn_raices)
        switch_box.add_widget(self.btn_sistemas)
        self.main_box.add_widget(switch_box)

        self.spinner = Spinner(text=self.metodo, values=self.metodos_raices, size_hint_y=None, height=44, background_color=(0.1,0.4,1,1), color=(1,1,1,1))
        self.spinner.bind(text=self.cambiar_metodo)
        self.main_box.add_widget(self.spinner)

        self.input_func = IOSDarkInput(hint_text="Ingresa la función, ej: x**3-x-2", multiline=False)
        self.main_box.add_widget(self.input_func)
        self.keyboard = MathKeyboard(self.input_func)
        # El teclado solo se agrega en modo raíces, no aquí

        self.input_deriv = IOSDarkInput(hint_text="Ingresa la derivada, ej: 3*x**2-1 (solo Newton)", multiline=False)
        self.main_box.add_widget(self.input_deriv)
        self.input_intervalo = IOSDarkInput(hint_text="Intervalo [a,b] o x0,x1, ej: 1,2 o 1.5,1.7", multiline=False)
        self.main_box.add_widget(self.input_intervalo)
        self.input_tol = IOSDarkInput(hint_text="Tolerancia, ej: 1e-5", multiline=False)
        self.main_box.add_widget(self.input_tol)

        self.input_matriz = IOSDarkInput(
            hint_text="Matriz A: filas separadas por ';', elementos por ','. Ej: 2,1;1,3",
            multiline=False
        )
        self.input_vector = IOSDarkInput(
            hint_text="Vector b: elementos separados por ','. Ej: 5,7",
            multiline=False
        )
        self.main_box.add_widget(self.input_matriz)
        self.main_box.add_widget(self.input_vector)

        self.btn_resolver = IOSDarkButton(text="Resolver")
        self.btn_resolver.bind(on_release=self.resolver)
        self.main_box.add_widget(self.btn_resolver)
        self.btn_paso_visual = IOSDarkButton(text="Paso a paso visual")
        self.btn_paso_visual.bind(on_release=self.paso_visual)
        self.main_box.add_widget(self.btn_paso_visual)
        self.btn_exportar_img = IOSDarkButton(text="Exportar imagen")
        self.btn_exportar_img.bind(on_release=self.exportar_img)
        self.main_box.add_widget(self.btn_exportar_img)
        self.btn_exportar_gif = IOSDarkButton(text="Exportar GIF")
        self.btn_exportar_gif.bind(on_release=self.exportar_gif)
        self.main_box.add_widget(self.btn_exportar_gif)
        self.btn_teoria = IOSDarkButton(text="Teoría")
        self.btn_teoria.bind(on_release=self.mostrar_teoria)
        self.main_box.add_widget(self.btn_teoria)

        self.result_label = IOSDarkLabel(text="", size_hint_y=None, height=32)
        self.main_box.add_widget(self.result_label)
        self.pasos_scroll = ScrollView(size_hint_y=None, height=120)
        self.pasos_label = IOSDarkLabel(text="", size_hint_y=None)
        self.pasos_scroll.add_widget(self.pasos_label)
        self.main_box.add_widget(self.pasos_scroll)
        self.historial_label = IOSDarkLabel(text="Historial:", size_hint_y=None, height=28)
        self.main_box.add_widget(self.historial_label)
        self.historial_scroll = ScrollView(size_hint_y=None, height=80)
        self.historial_box = BoxLayout(orientation="vertical", size_hint_y=None)
        self.historial_box.bind(minimum_height=self.historial_box.setter('height'))
        self.historial_scroll.add_widget(self.historial_box)
        self.main_box.add_widget(self.historial_scroll)
        self.plot = FunctionPlot("x**2-2", 0, 2, size_hint_y=None, height=180)
        self.main_box.add_widget(self.plot)

        self.cambiar_modo("Raíces")

    def cambiar_modo(self, modo):
        self.modo = modo
        if modo == "Raíces":
            self.spinner.values = self.metodos_raices
            self.spinner.text = self.metodos_raices[0]
            self.input_func.opacity = 1
            self.input_deriv.opacity = 1
            self.input_intervalo.opacity = 1
            self.input_tol.opacity = 1
            self.input_matriz.opacity = 0
            self.input_vector.opacity = 0
            self.input_func.disabled = False
            self.input_deriv.disabled = False
            self.input_intervalo.disabled = False
            self.input_tol.disabled = False
            self.input_matriz.disabled = True
            self.input_vector.disabled = True
            self.btn_paso_visual.opacity = 1
            self.btn_paso_visual.disabled = False
            self.btn_exportar_gif.opacity = 1
            self.btn_exportar_gif.disabled = False
            self.btn_exportar_img.opacity = 1
            self.btn_exportar_img.disabled = False
            if self.keyboard.parent is not None:
                self.keyboard.parent.remove_widget(self.keyboard)
            widgets = list(self.main_box.children)[::-1]
            idx = None
            for i, widget in enumerate(widgets):
                if widget is self.input_func:
                    idx = i + 1
                    break
            if idx is not None:
                self.main_box.add_widget(self.keyboard, index=idx)
        else:
            self.spinner.values = self.metodos_sistemas
            self.spinner.text = self.metodos_sistemas[0]
            self.input_func.opacity = 0
            self.input_deriv.opacity = 0
            self.input_intervalo.opacity = 0
            self.input_func.disabled = True
            self.input_deriv.disabled = True
            self.input_intervalo.disabled = True
            self.input_tol.opacity = 1
            self.input_tol.disabled = False
            self.input_matriz.opacity = 1
            self.input_vector.opacity = 1
            self.input_matriz.disabled = False
            self.input_vector.disabled = False
            self.btn_paso_visual.opacity = 0
            self.btn_paso_visual.disabled = True
            self.btn_exportar_gif.opacity = 0
            self.btn_exportar_gif.disabled = True
            self.btn_exportar_img.opacity = 0
            self.btn_exportar_img.disabled = True
            if self.keyboard.parent is not None:
                self.keyboard.parent.remove_widget(self.keyboard)

    def cambiar_metodo(self, spinner, text):
        self.metodo = text

    def resolver(self, instance):
        if self.modo == "Raíces":
            expr = self.input_func.text.strip()
            tol = float(self.input_tol.text.strip() or "1e-5")
            pasos = []
            raiz = None
            resultado = ""
            intervalo = self.input_intervalo.text.strip()
            try:
                if self.metodo == "Bisección":
                    a, b = [float(x) for x in intervalo.split(",")]
                    raiz, pasos = self.biseccion(expr, a, b, tol)
                    resultado = f"Raíz ≈ {raiz:.6f}"
                elif self.metodo == "Newton-Raphson":
                    x0 = float(intervalo.split(",")[0])
                    deriv = self.input_deriv.text.strip()
                    raiz, pasos = self.newton(expr, deriv, x0, tol)
                    resultado = f"Raíz ≈ {raiz:.6f}"
                elif self.metodo == "Secante":
                    x0, x1 = [float(x) for x in intervalo.split(",")]
                    raiz, pasos = self.secante(expr, x0, x1, tol)
                    resultado = f"Raíz ≈ {raiz:.6f}"
                elif self.metodo == "Regula Falsi":
                    a, b = [float(x) for x in intervalo.split(",")]
                    raiz, pasos = self.regula_falsi(expr, a, b, tol)
                    resultado = f"Raíz ≈ {raiz:.6f}"
            except Exception as e:
                resultado = f"Error: {e}"
            self.result_label.text = resultado
            self.pasos = pasos
            self.paso_idx = len(pasos)-1
            self.pasos_label.text = "\n".join([self.formato_paso(p) for p in pasos])
            self.raiz = raiz
            self.latex_img = self.render_latex(expr)
            self.plot.func_expr = expr
            self.plot.a = float(intervalo.split(",")[0]) if "," in intervalo else 0
            self.plot.b = float(intervalo.split(",")[1]) if "," in intervalo else 2
            self.plot.pasos = pasos
            self.plot.paso_idx = self.paso_idx
            self.plot.raiz = raiz
            self.plot.latex_img = self.latex_img
            self.plot.redraw()
            self.historial.append({"modo":self.modo,"metodo":self.metodo,"expr":expr,"resultado":resultado})
            self.actualizar_historial()
        else:
            try:
                matriz_txt = self.input_matriz.text.strip()
                vector_txt = self.input_vector.text.strip()
                if not matriz_txt or not vector_txt:
                    raise Exception("Debes ingresar la matriz y el vector.")
                A = []
                for row in matriz_txt.split(";"):
                    A.append([float(x) for x in row.strip().split(",")])
                b = [float(x) for x in vector_txt.split(",")]
                n = len(A)
                if any(len(row) != n for row in A):
                    raise Exception("La matriz debe ser cuadrada")
                if len(b) != n:
                    raise Exception("El vector b debe tener la misma dimensión que la matriz")
                tol = float(self.input_tol.text.strip() or "1e-5")
                pasos = []
                resultado = ""
                if self.metodo == "Gauss-Jordan":
                    x, pasos = self.gauss_jordan(A, b)
                elif self.metodo == "Jacobi":
                    x, pasos = self.jacobi(A, b, tol)
                elif self.metodo == "Gauss-Seidel":
                    x, pasos = self.gauss_seidel(A, b, tol)
                resultado = "Solución: " + ", ".join([f"x{i+1} ≈ {xi:.6f}" for i,xi in enumerate(x)])
            except Exception as e:
                resultado = f"Error: {e}"
                x = None
                pasos = []
            self.result_label.text = resultado
            self.pasos_label.text = "\n".join([str(p) for p in pasos])
            self.solucion_sistema = x
            self.pasos_sistema = pasos
            self.paso_idx_sistema = len(pasos)-1
            self.historial.append({"modo":self.modo,"metodo":self.metodo,"matriz":A if 'A' in locals() else '',"vector":b if 'b' in locals() else '',"resultado":resultado})
            self.actualizar_historial()

    def formato_paso(self, p):
        if "a" in p and "b" in p and "c" in p:
            return f"Iter {p['iter']}: a={p['a']:.6f}, b={p['b']:.6f}, c={p['c']:.6f}, f(c)={p['fc']:.2e}"
        elif "x" in p and "fx" in p:
            return f"Iter {p['iter']}: x={p['x']:.6f}, f(x)={p['fx']:.2e}"
        return str(p)

    def paso_visual(self, instance):
        if self.modo == "Raíces" and self.pasos:
            self.paso_idx = 0
            self.popup_paso = Popup(title="Paso a paso visual", size_hint=(0.95,0.8))
            layout = BoxLayout(orientation="vertical", spacing=8, padding=8)
            plot = FunctionPlot(self.plot.func_expr, self.plot.a, self.plot.b, pasos=self.pasos, paso_idx=self.paso_idx, raiz=self.raiz, latex_img=self.latex_img, size_hint_y=0.7)
            label = IOSDarkLabel(text=self.formato_paso(self.pasos[self.paso_idx]), size_hint_y=0.1)
            btns = BoxLayout(orientation="horizontal", size_hint_y=0.2, spacing=8)
            btn_prev = IOSDarkButton(text="Anterior")
            btn_next = IOSDarkButton(text="Siguiente")
            def update(idx):
                plot.paso_idx = idx
                plot.redraw()
                label.text = self.formato_paso(self.pasos[idx])
            def prev(_):
                if self.paso_idx>0:
                    self.paso_idx-=1
                    update(self.paso_idx)
            def next(_):
                if self.paso_idx<len(self.pasos)-1:
                    self.paso_idx+=1
                    update(self.paso_idx)
            btn_prev.bind(on_release=prev)
            btn_next.bind(on_release=next)
            btns.add_widget(btn_prev)
            btns.add_widget(btn_next)
            layout.add_widget(plot)
            layout.add_widget(label)
            layout.add_widget(btns)
            self.popup_paso.content = layout
            self.popup_paso.open()

    def exportar_img(self, instance):
        if not self.plot:
            return
        fname = "grafico.png"
        self.plot.export_to_png(fname)
        self.popup_info(f"Imagen guardada como {fname}")

    def exportar_gif(self, instance):
        if not IMAGEIO:
            self.popup_info("Instala imageio y pillow para exportar GIF.")
            return
        if self.modo == "Raíces" and self.pasos:
            frames = []
            for idx in range(len(self.pasos)):
                self.plot.paso_idx = idx
                self.plot.redraw()
                fname = f"frame_{idx}.png"
                self.plot.export_to_png(fname)
                frames.append(PILImage.open(fname))
            gifname = "paso_a_paso.gif"
            frames[0].save(gifname, save_all=True, append_images=frames[1:], duration=800, loop=0)
            for idx in range(len(self.pasos)):
                os.remove(f"frame_{idx}.png")
            self.popup_info(f"GIF guardado como {gifname}")

    def mostrar_teoria(self, instance):
        teoria = {
            "Bisección": (
                "Método de Bisección:\n\n"
                "Busca una raíz de f(x)=0 en [a,b] donde f(a)·f(b)<0. "
                "Divide el intervalo a la mitad en cada paso. "
                "Converge siempre si la función es continua y cambia de signo.\n\n"
                "Ventajas: Siempre converge si la función es continua y cambia de signo.\n"
                "Desventajas: Convergencia lenta."
            ),
            "Newton-Raphson": (
                "Método de Newton-Raphson:\n\n"
                "Aproxima una raíz usando la fórmula x_{n+1} = x_n - f(x_n)/f'(x_n).\n"
                "Rápido si la derivada no es cero y la aproximación inicial es buena.\n\n"
                "Ventajas: Convergencia rápida (cuadrática) cerca de la raíz.\n"
                "Desventajas: Puede divergir si la derivada es cero o la aproximación inicial es mala."
            ),
            "Secante": (
                "Método de la Secante:\n\n"
                "Similar a Newton pero usa una aproximación numérica de la derivada.\n"
                "x_{n+1} = x_n - f(x_n)*(x_n-x_{n-1})/(f(x_n)-f(x_{n-1})).\n\n"
                "Ventajas: No requiere derivada analítica.\n"
                "Desventajas: Puede ser menos estable que Newton."
            ),
            "Regula Falsi": (
                "Método de Regula Falsi:\n\n"
                "Variante de bisección que usa una recta secante para aproximar la raíz.\n"
                "Más rápido que bisección en algunos casos.\n\n"
                "Ventajas: Mejor convergencia que bisección en algunos casos.\n"
                "Desventajas: Puede estancarse si la función es muy asimétrica."
            ),
            "Gauss-Jordan": (
                "Método de Gauss-Jordan:\n\n"
                "Resuelve sistemas lineales Ax=b llevando la matriz aumentada a forma escalonada reducida por filas.\n"
                "Permite encontrar la solución única (si existe) y la inversa de la matriz.\n\n"
                "Ventajas: Método directo, da la solución exacta (en aritmética exacta).\n"
                "Desventajas: Costoso para matrices grandes, sensible a errores de redondeo."
            ),
            "Jacobi": (
                "Método de Jacobi:\n\n"
                "Iterativo para sistemas Ax=b. x^{(k+1)} = D^{-1}(b - (L+U)x^{(k)}).\n"
                "Requiere matriz diagonal dominante para garantizar convergencia.\n\n"
                "Ventajas: Fácil de paralelizar, útil para matrices dispersas.\n"
                "Desventajas: Convergencia lenta, requiere buenas condiciones en la matriz."
            ),
            "Gauss-Seidel": (
                "Método de Gauss-Seidel:\n\n"
                "Similar a Jacobi pero usa los valores más recientes en cada iteración.\n"
                "Suele converger más rápido que Jacobi.\n\n"
                "Ventajas: Mejor convergencia que Jacobi.\n"
                "Desventajas: Puede no converger si la matriz no es diagonal dominante."
            )
        }
        txt = teoria.get(self.metodo, "Selecciona un método para ver la teoría.")
        content = BoxLayout(orientation="vertical", padding=16, spacing=8)
        label = IOSDarkLabel(text=txt, size_hint_y=None)
        label.text_size = (400, None)
        label.bind(texture_size=lambda inst, val: setattr(label, 'height', val[1]))
        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(label)
        content.add_widget(scroll)
        btn_close = IOSDarkButton(text="Cerrar", size_hint_y=None, height=48)
        content.add_widget(btn_close)
        popup = Popup(title="Teoría", content=content, size_hint=(0.95, 0.7))
        btn_close.bind(on_release=popup.dismiss)
        popup.open()

    def actualizar_historial(self):
        self.historial_box.clear_widgets()
        for h in self.historial[-5:][::-1]:
            txt = f"{h['modo']} - {h['metodo']}: {h.get('expr',h.get('matriz',''))} => {h['resultado']}"
            self.historial_box.add_widget(IOSDarkLabel(text=txt, size_hint_y=None, height=24))

    def render_latex(self, expr):
        if not MATPLOTLIB:
            return None
        plt.figure(figsize=(3,0.6))
        plt.axis("off")
        rc('text', usetex=True)
        plt.text(0.5,0.5, f"${expr}$", fontsize=18, ha='center', va='center')
        buf = io.BytesIO()
        plt.savefig(buf, format="png", bbox_inches='tight', pad_inches=0.1, transparent=True)
        plt.close()
        buf.seek(0)
        return buf

    def biseccion(self, expr, a, b, tol):
        pasos = []
        fa = safe_eval(expr, a)
        fb = safe_eval(expr, b)
        if fa*fb > 0:
            raise Exception("f(a) y f(b) deben tener signos opuestos")
        iter = 0
        while abs(b-a) > tol and iter < 100:
            c = (a+b)/2
            fc = safe_eval(expr, c)
            pasos.append({"iter":iter+1, "a":a, "b":b, "c":c, "fc":fc})
            if fa*fc < 0:
                b = c
                fb = fc
            else:
                a = c
                fa = fc
            iter += 1
        return c, pasos

    def newton(self, expr, deriv, x0, tol):
        pasos = []
        x = x0
        for i in range(20):
            fx = safe_eval(expr, x)
            dfx = safe_eval(deriv, x)
            if abs(dfx)<1e-12:
                raise Exception("Derivada cero")
            pasos.append({"iter":i+1, "x":x, "fx":fx})
            x1 = x - fx/dfx
            if abs(x1-x)<tol:
                return x1, pasos
            x = x1
        return x, pasos

    def secante(self, expr, x0, x1, tol):
        pasos = []
        for i in range(20):
            fx0 = safe_eval(expr, x0)
            fx1 = safe_eval(expr, x1)
            if abs(fx1-fx0)<1e-12:
                raise Exception("División por cero")
            x2 = x1 - fx1*(x1-x0)/(fx1-fx0)
            pasos.append({"iter":i+1, "x":x2, "fx":safe_eval(expr, x2)})
            if abs(x2-x1)<tol:
                return x2, pasos
            x0, x1 = x1, x2
        return x2, pasos

    def regula_falsi(self, expr, a, b, tol):
        pasos = []
        fa = safe_eval(expr, a)
        fb = safe_eval(expr, b)
        if fa*fb > 0:
            raise Exception("f(a) y f(b) deben tener signos opuestos")
        for i in range(30):
            c = b - fb*(b-a)/(fb-fa)
            fc = safe_eval(expr, c)
            pasos.append({"iter":i+1, "a":a, "b":b, "c":c, "fc":fc})
            if abs(fc)<tol:
                return c, pasos
            if fa*fc < 0:
                b = c
                fb = fc
            else:
                a = c
                fa = fc
        return c, pasos

    def gauss_jordan(self, A, b):
        n = len(A)
        M = [row[:] + [b[i]] for i, row in enumerate(A)]
        pasos = []
        for i in range(n):
            if abs(M[i][i])<1e-12:
                for j in range(i+1,n):
                    if abs(M[j][i])>1e-12:
                        M[i], M[j] = M[j], M[i]
                        break
            piv = M[i][i]
            for k in range(i,n+1):
                M[i][k] /= piv
            for j in range(n):
                if j!=i:
                    f = M[j][i]
                    for k in range(i,n+1):
                        M[j][k] -= f*M[i][k]
            pasos.append([row[:] for row in M])
        x = [M[i][n] for i in range(n)]
        return x, pasos

    def jacobi(self, A, b, tol):
        n = len(A)
        x = [0 for _ in range(n)]
        pasos = []
        for it in range(25):
            x_new = x[:]
            for i in range(n):
                s = sum(A[i][j]*x[j] for j in range(n) if j!=i)
                x_new[i] = (b[i]-s)/A[i][i]
            pasos.append(x_new[:])
            if all(abs(x_new[i]-x[i])<tol for i in range(n)):
                return x_new, pasos
            x = x_new
        return x, pasos

    def gauss_seidel(self, A, b, tol):
        n = len(A)
        x = [0 for _ in range(n)]
        pasos = []
        for it in range(25):
            x_old = x[:]
            for i in range(n):
                s1 = sum(A[i][j]*x[j] for j in range(i))
                s2 = sum(A[i][j]*x_old[j] for j in range(i+1,n))
                x[i] = (b[i]-s1-s2)/A[i][i]
            pasos.append(x[:])
            if all(abs(x[i]-x_old[i])<tol for i in range(n)):
                return x, pasos
        return x, pasos

    def popup_info(self, msg):
        popup = Popup(title="Info", content=IOSDarkLabel(text=msg), size_hint=(0.7,0.3))
        popup.open()

class DemoInnovadorApp(App):
    def build(self):
        Window.clearcolor = (0,0,0,1)
        return DemoInnovadorLayout()

if __name__ == "__apk__":
    DemoInnovadorApp().run()
