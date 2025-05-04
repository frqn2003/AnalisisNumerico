import json
import os
from datetime import datetime

class GestorFavoritos:
    """
    Clase para gestionar funciones favoritas y el historial de uso
    """
    def __init__(self, archivo_favoritos="favoritos.json", archivo_historial="historial.json"):
        self.archivo_favoritos = archivo_favoritos
        self.archivo_historial = archivo_historial
        self.favoritos = self._cargar_favoritos()
        self.historial = self._cargar_historial()
        
        # Crear ejemplos predeterminados si no hay favoritos
        if not self.favoritos:
            self._crear_ejemplos_predeterminados()
    
    def _cargar_favoritos(self):
        """Carga las funciones favoritas desde el archivo JSON"""
        if os.path.exists(self.archivo_favoritos):
            try:
                with open(self.archivo_favoritos, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def _cargar_historial(self):
        """Carga el historial de funciones desde el archivo JSON"""
        if os.path.exists(self.archivo_historial):
            try:
                with open(self.archivo_historial, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def _guardar_favoritos(self):
        """Guarda las funciones favoritas en el archivo JSON"""
        with open(self.archivo_favoritos, 'w') as f:
            json.dump(self.favoritos, f, indent=4)
    
    def _guardar_historial(self):
        """Guarda el historial de funciones en el archivo JSON"""
        with open(self.archivo_historial, 'w') as f:
            json.dump(self.historial, f, indent=4)
    
    def _crear_ejemplos_predeterminados(self):
        """Crea ejemplos predeterminados de funciones favoritas"""
        ejemplos = [
            {
                "nombre": "Función Polinómica Cúbica",
                "expresion": "x**3 - x - 2",
                "descripcion": "Polinomio de tercer grado con una raíz real",
                "parametros": {"a": 1, "b": 2},
                "fecha_creacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            {
                "nombre": "Función Trigonométrica",
                "expresion": "sin(x) - x/2",
                "descripcion": "Función trigonométrica con m��ltiples raíces",
                "parametros": {"a": 0, "b": 2},
                "fecha_creacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            {
                "nombre": "Función Exponencial",
                "expresion": "exp(-x) - x",
                "descripcion": "Función exponencial con una raíz positiva",
                "parametros": {"a": 0, "b": 1},
                "fecha_creacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        ]
        
        for ejemplo in ejemplos:
            self.favoritos.append(ejemplo)
        
        self._guardar_favoritos()
    
    def agregar_favorito(self, nombre, expresion, descripcion="", parametros=None):
        """
        Agrega una función a favoritos
        
        Args:
            nombre (str): Nombre descriptivo de la función
            expresion (str): Expresión matemática de la función
            descripcion (str): Descripción opcional de la función
            parametros (dict): Parámetros asociados a la función (a, b, etc.)
        """
        if parametros is None:
            parametros = {}
        
        # Verificar si ya existe un favorito con el mismo nombre
        for i, fav in enumerate(self.favoritos):
            if fav["nombre"] == nombre:
                # Actualizar el favorito existente
                self.favoritos[i] = {
                    "nombre": nombre,
                    "expresion": expresion,
                    "descripcion": descripcion,
                    "parametros": parametros,
                    "fecha_creacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                self._guardar_favoritos()
                return
        
        # Agregar nuevo favorito
        nuevo_favorito = {
            "nombre": nombre,
            "expresion": expresion,
            "descripcion": descripcion,
            "parametros": parametros,
            "fecha_creacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.favoritos.append(nuevo_favorito)
        self._guardar_favoritos()
    
    def eliminar_favorito(self, nombre):
        """Elimina una función de favoritos por su nombre"""
        self.favoritos = [fav for fav in self.favoritos if fav["nombre"] != nombre]
        self._guardar_favoritos()
    
    def obtener_favoritos(self):
        """Retorna la lista de funciones favoritas"""
        return self.favoritos
    
    def agregar_al_historial(self, expresion, metodo, parametros=None):
        """
        Agrega una función al historial de uso
        
        Args:
            expresion (str): Expresión matemática de la función
            metodo (str): Método numérico utilizado
            parametros (dict): Parámetros utilizados
        """
        if parametros is None:
            parametros = {}
        
        nuevo_historial = {
            "expresion": expresion,
            "metodo": metodo,
            "parametros": parametros,
            "fecha_uso": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Agregar al inicio del historial
        self.historial.insert(0, nuevo_historial)
        
        # Limitar el historial a las últimas 20 entradas
        if len(self.historial) > 20:
            self.historial = self.historial[:20]
        
        self._guardar_historial()
    
    def obtener_historial(self, limite=10):
        """Retorna las últimas entradas del historial"""
        return self.historial[:limite]