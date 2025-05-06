"""
MathWorks 2025 - Aplicación de Métodos Numéricos
Módulo principal para ejecutar la aplicación
"""

import tkinter as tk
import sys
import os
import json

# Asegurar que favoritos.py y gui_desktop.py estén accesibles
from gui_desktop_corregido import AplicacionMetodosNumericos
from favoritos import GestorFavoritos

def verificar_archivos_requeridos():
    """Verifica que los archivos necesarios existan"""
    archivos_requeridos = [
        "favoritos.py", 
        "gui_desktop.py",
        "metodos_raices.py",
        "metodos_sistemas.py",
        "Validar_txt.py"
    ]
    
    archivos_faltantes = []
    for archivo in archivos_requeridos:
        if not os.path.exists(archivo):
            archivos_faltantes.append(archivo)
    
    if archivos_faltantes:
        print(f"Error: No se encontraron los siguientes archivos requeridos:")
        for archivo in archivos_faltantes:
            print(f"- {archivo}")
        print("La aplicación no puede iniciarse.")
        return False
    
    return True

def main():
    """Función principal para iniciar la aplicación"""
    # Verificar archivos requeridos
    if not verificar_archivos_requeridos():
        sys.exit(1)
    
    # Crear instancia del gestor de favoritos para asegurar que existan los archivos JSON
    gestor_favoritos = GestorFavoritos()
    
    # Iniciar aplicación
    root = tk.Tk()
    app = AplicacionMetodosNumericos(root)
    root.mainloop()

if __name__ == "__main__":
    main()