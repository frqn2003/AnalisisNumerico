import json
import os

class GestorIdiomas:
    """
    Clase para gestionar los idiomas y traducciones de la aplicación.
    Proporciona un mecanismo para cambiar dinámicamente entre español e inglés.
    """
    def __init__(self, idioma_inicial="es"):
        """
        Inicializa el gestor de idiomas.
        
        Args:
            idioma_inicial (str): Código de idioma inicial (es=español, en=inglés)
        """
        self.idioma_actual = idioma_inicial
        self.traducciones = {}
        self._cargar_traducciones()
    
    def _cargar_traducciones(self):
        """Carga los archivos de traducciones"""
        # Definir nombres de archivos
        archivos_idiomas = {
            "es": "traducciones_es.json",
            "en": "traducciones_en.json"
        }
        
        # Crear archivos de traducciones si no existen
        self._crear_archivos_traducciones(archivos_idiomas)
        
        # Cargar traducciones desde archivos
        for codigo, archivo in archivos_idiomas.items():
            if os.path.exists(archivo):
                try:
                    with open(archivo, 'r', encoding='utf-8') as f:
                        self.traducciones[codigo] = json.load(f)
                except Exception as e:
                    print(f"Error al cargar traducciones {codigo}: {e}")
                    # Cargar traducciones por defecto en caso de error
                    self.traducciones[codigo] = self._obtener_traducciones_predeterminadas(codigo)
            else:
                self.traducciones[codigo] = self._obtener_traducciones_predeterminadas(codigo)
    
    def _crear_archivos_traducciones(self, archivos_idiomas):
        """Crea los archivos de traducciones si no existen"""
        for codigo, archivo in archivos_idiomas.items():
            if not os.path.exists(archivo):
                traducciones = self._obtener_traducciones_predeterminadas(codigo)
                try:
                    with open(archivo, 'w', encoding='utf-8') as f:
                        json.dump(traducciones, f, indent=4, ensure_ascii=False)
                    print(f"Archivo de traducciones {archivo} creado correctamente")
                except Exception as e:
                    print(f"Error al crear archivo de traducciones {archivo}: {e}")
    
    def _obtener_traducciones_predeterminadas(self, codigo):
        """Obtiene las traducciones predeterminadas para un idioma"""
        # Español (idioma base)
        if codigo == "es":
            return {
                # Textos generales
                "app_title": "MathWorks 2025 - Métodos Numéricos",
                "app_subtitle": "Sistemas de ecuaciones y búsqueda de raíces",
                "ready_status": "Listo",
                
                # Pestañas
                "tab_roots": "Búsqueda de Raíces",
                "tab_systems": "Sistemas de Ecuaciones",
                "tab_info": "Información",
                "tab_favorites": "Favoritos",
                
                # Búsqueda de raíces
                "method": "Método",
                "select_method": "Seleccionar método:",
                "function": "Función",
                "function_fx": "Función f(x):",
                "parameters": "Parámetros",
                "a_left": "a (extremo izquierdo):",
                "b_right": "b (extremo derecho):",
                "x0_approx": "x0 (aproximación inicial):",
                "not_used": "No se usa:",
                "x0_first": "x0 (primera aproximación):",
                "x1_second": "x1 (segunda aproximación):",
                "tolerance": "Tolerancia:",
                "max_iterations": "Máx. iteraciones:",
                "calculate_root": "Calcular Raíz",
                "examples": "Ejemplos",
                "polynomial_function": "Función Polinómica",
                "trigonometric_function": "Función Trigonométrica",
                "save_as_favorite": "Guardar como Favorito",
                "results": "Resultados",
                "graph": "Gráfico",
                
                # Sistemas de ecuaciones
                "data_input": "Entrada de datos",
                "matrix_A": "Matriz A (filas separadas por ; y elementos por espacios o comas):",
                "vector_b": "Vector b (elementos separados por espacios o comas):",
                "vector_x0": "Vector inicial x0 (opcional):",
                "solve_system": "Resolver Sistema",
                "example_1": "Ejemplo 1: Sistema 3x3",
                "example_2": "Ejemplo 2: Para Métodos Iterativos",
                
                # Favoritos
                "my_favorites": "Mis Favoritos",
                "details": "Detalles",
                "name": "Nombre:",
                "expression": "Expresión:",
                "description": "Descripción:",
                "creation_date": "Fecha de creación:",
                "load_calculator": "Cargar en Calculadora",
                "delete": "Eliminar",
                
                # Diálogos
                "save_favorite_title": "Guardar como favorito",
                "enter_name": "Ingrese un nombre para este favorito:",
                "enter_name_system": "Ingrese un nombre para este sistema:",
                "enter_description": "Ingrese una descripción (opcional):",
                "confirm_delete": "Confirmar eliminación",
                "confirm_delete_message": "¿Está seguro de eliminar '{0}' de sus favoritos?",
                "error": "Error",
                "success": "Éxito",
                "warning": "Advertencia",
                "function_empty": "La función no puede estar vacía",
                "matrix_vector_empty": "La matriz A y el vector b no pueden estar vacíos",
                "invalid_matrix": "El formato de la matriz A no es válido",
                "invalid_vector": "El formato del vector b no es válido",
                "invalid_x0": "El formato del vector x0 no es válido. ¿Desea continuar sin incluirlo?",
                "favorite_error": "No se pudo guardar el favorito: {0}",
                "favorite_saved": "{0} guardado como favorito: '{1}'",
                "favorite_loaded": "Favorito '{0}' cargado correctamente",
                "favorite_deleted": "Favorito '{0}' eliminado correctamente",
                "cannot_delete_favorite": "No se pudo eliminar el favorito",
                "cannot_load_favorite": "No se pudo cargar el favorito: {0}",
                
                # Información
                "app_name": "MathWorks 2025",
                "app_description": """
Esta aplicación implementa diversos métodos numéricos para la resolución de problemas matemáticos:

• Búsqueda de raíces de funciones: Bisección, Regula Falsi, Newton y Secante
• Resolución de sistemas de ecuaciones lineales: Gauss-Jordan, Gauss-Seidel y Jacobi

Cada método posee características particulares que los hacen más adecuados para distintos tipos de problemas.""",
                "footer_text": "Desarrollado para el curso de Análisis Numérico",
                
                # Métodos
                "root_methods": "Métodos para búsqueda de raíces",
                "system_methods": "Métodos para sistemas de ecuaciones",
                "bisection_name": "Bisección",
                "bisection_desc": "Divide repetidamente el intervalo a la mitad y selecciona el subintervalo donde la función cambia de signo.",
                "regula_falsi_name": "Regula Falsi",
                "regula_falsi_desc": "Similar a bisección, pero usa interpolación lineal para estimar la raíz.",
                "newton_name": "Newton",
                "newton_desc": "Utiliza la derivada de la función para aproximarse rápidamente a la raíz.",
                "secant_name": "Secante",
                "secant_desc": "Similar a Newton, pero aproxima la derivada usando dos puntos anteriores.",
                "gauss_jordan_name": "Gauss-Jordan",
                "gauss_jordan_desc": "Método directo que transforma la matriz aumentada en una forma escalonada reducida.",
                "gauss_seidel_name": "Gauss-Seidel",
                "gauss_seidel_desc": "Método iterativo que actualiza cada componente usando los valores más recientes.",
                "jacobi_name": "Jacobi",
                "jacobi_desc": "Método iterativo que calcula nuevos valores basados en los valores de la iteración anterior.",
                
                # Idioma
                "language": "Idioma",
                "language_spanish": "Español",
                "language_english": "Inglés",
                "change_language": "Cambiar idioma"
            }
        # Inglés
        elif codigo == "en":
            return {
                # General texts
                "app_title": "MathWorks 2025 - Numerical Methods",
                "app_subtitle": "Equation systems and root finding",
                "ready_status": "Ready",
                
                # Tabs
                "tab_roots": "Root Finding",
                "tab_systems": "Equation Systems",
                "tab_info": "Information",
                "tab_favorites": "Favorites",
                
                # Root finding
                "method": "Method",
                "select_method": "Select method:",
                "function": "Function",
                "function_fx": "Function f(x):",
                "parameters": "Parameters",
                "a_left": "a (left endpoint):",
                "b_right": "b (right endpoint):",
                "x0_approx": "x0 (initial approximation):",
                "not_used": "Not used:",
                "x0_first": "x0 (first approximation):",
                "x1_second": "x1 (second approximation):",
                "tolerance": "Tolerance:",
                "max_iterations": "Max. iterations:",
                "calculate_root": "Calculate Root",
                "examples": "Examples",
                "polynomial_function": "Polynomial Function",
                "trigonometric_function": "Trigonometric Function",
                "save_as_favorite": "Save as Favorite",
                "results": "Results",
                "graph": "Graph",
                
                # Equation systems
                "data_input": "Data Input",
                "matrix_A": "Matrix A (rows separated by ; and elements by spaces or commas):",
                "vector_b": "Vector b (elements separated by spaces or commas):",
                "vector_x0": "Initial vector x0 (optional):",
                "solve_system": "Solve System",
                "example_1": "Example 1: 3x3 System",
                "example_2": "Example 2: For Iterative Methods",
                
                # Favorites
                "my_favorites": "My Favorites",
                "details": "Details",
                "name": "Name:",
                "expression": "Expression:",
                "description": "Description:",
                "creation_date": "Creation date:",
                "load_calculator": "Load in Calculator",
                "delete": "Delete",
                
                # Dialogs
                "save_favorite_title": "Save as favorite",
                "enter_name": "Enter a name for this favorite:",
                "enter_name_system": "Enter a name for this system:",
                "enter_description": "Enter a description (optional):",
                "confirm_delete": "Confirm deletion",
                "confirm_delete_message": "Are you sure you want to delete '{0}' from your favorites?",
                "error": "Error",
                "success": "Success",
                "warning": "Warning",
                "function_empty": "The function cannot be empty",
                "matrix_vector_empty": "Matrix A and vector b cannot be empty",
                "invalid_matrix": "The format of matrix A is invalid",
                "invalid_vector": "The format of vector b is invalid",
                "invalid_x0": "The format of vector x0 is invalid. Do you want to continue without it?",
                "favorite_error": "Could not save favorite: {0}",
                "favorite_saved": "{0} saved as favorite: '{1}'",
                "favorite_loaded": "Favorite '{0}' loaded successfully",
                "favorite_deleted": "Favorite '{0}' deleted successfully",
                "cannot_delete_favorite": "Could not delete favorite",
                "cannot_load_favorite": "Could not load favorite: {0}",
                
                # Information
                "app_name": "MathWorks 2025",
                "app_description": """
This application implements various numerical methods for solving mathematical problems:

• Function root finding: Bisection, Regula Falsi, Newton and Secant
• Linear equation systems: Gauss-Jordan, Gauss-Seidel and Jacobi

Each method has particular characteristics that make them more suitable for different types of problems.""",
                "footer_text": "Developed for the Numerical Analysis course",
                
                # Methods
                "root_methods": "Methods for root finding",
                "system_methods": "Methods for equation systems",
                "bisection_name": "Bisection",
                "bisection_desc": "Repeatedly divides the interval in half and selects the subinterval where the function changes sign.",
                "regula_falsi_name": "Regula Falsi",
                "regula_falsi_desc": "Similar to bisection, but uses linear interpolation to estimate the root.",
                "newton_name": "Newton",
                "newton_desc": "Uses the derivative of the function to quickly approach the root.",
                "secant_name": "Secant",
                "secant_desc": "Similar to Newton, but approximates the derivative using two previous points.",
                "gauss_jordan_name": "Gauss-Jordan",
                "gauss_jordan_desc": "Direct method that transforms the augmented matrix into a reduced echelon form.",
                "gauss_seidel_name": "Gauss-Seidel",
                "gauss_seidel_desc": "Iterative method that updates each component using the most recent values.",
                "jacobi_name": "Jacobi",
                "jacobi_desc": "Iterative method that calculates new values based on the values of the previous iteration.",
                
                # Language
                "language": "Language",
                "language_spanish": "Spanish",
                "language_english": "English",
                "change_language": "Change language"
            }
        else:
            # Devuelve un diccionario vacío para idiomas no soportados
            return {}
    
    def cambiar_idioma(self, nuevo_idioma):
        """
        Cambia el idioma actual
        
        Args:
            nuevo_idioma (str): Código del nuevo idioma (es/en)
            
        Returns:
            bool: True si el cambio fue exitoso, False en caso contrario
        """
        if nuevo_idioma in self.traducciones:
            self.idioma_actual = nuevo_idioma
            return True
        return False
    
    def obtener_texto(self, clave, *args):
        """
        Obtiene el texto traducido para una clave específica
        
        Args:
            clave (str): Clave del texto a traducir
            *args: Parámetros para formatear el texto
            
        Returns:
            str: Texto traducido o la clave si no se encuentra traducción
        """
        if self.idioma_actual in self.traducciones and clave in self.traducciones[self.idioma_actual]:
            texto = self.traducciones[self.idioma_actual][clave]
            # Si hay argumentos, formatear el texto
            if args:
                try:
                    return texto.format(*args)
                except:
                    return texto
            return texto
        else:
            # Si no se encuentra la clave, devolver la clave misma
            return clave