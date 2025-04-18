"""
MathWorks 2025 - Aplicación de Métodos Numéricos
Módulo principal para ejecutar la aplicación
"""

import tkinter as tk
from gui_desktop import AplicacionMetodosNumericos

if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacionMetodosNumericos(root)
    root.mainloop()