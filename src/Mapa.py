import tkinter as tk
from tkintermapview import TkinterMapView
import re

class mapa:
    def __init__(self, TopLevel = None):
        self.level = TopLevel
        self.coordenadas = []
        self.ventana_mapa = None
        
    def leer_coordenadas(self):
        with open('historial_coordenadas.csv', 'r') as archivo:
            for linea in archivo:
                linea = linea.strip()
                try:
                    # Extraer todos los números (incluyendo negativos)
                    numeros = re.findall(r'-?\d+', linea)
                    x = int(numeros[-3])  # x
                    y = int(numeros[-2])  # y
                    
                    # Conversión a GPS Miranda de Ebro
                    lon = -2.9444 + (x - 426864633) / 1000000.0
                    lat = 42.6861 + (y + 29429133) / 1000000.0

                    self.coordenadas.append((lat, lon))
                    
                except Exception as e:
                    print(f"Error: {e}")

        return self.coordenadas

    def crear_mapa(self):
        if self.ventana_mapa is None:
            # Crear una nueva ventana independiente
            self.ventana_mapa = tk.Toplevel()
            self.ventana_mapa.title("Mapa de Coordenadas")
            self.ventana_mapa.geometry("1000x700")

            # Crear widget del mapa en esa ventana
            map_widget = TkinterMapView(self.ventana_mapa, width=1000, height=700, corner_radius=0)
            map_widget.pack(fill="both", expand=True)

            # Centrar en Miranda de Ebro
            map_widget.set_position(42.6861, -2.9444)
            map_widget.set_zoom(16)

            self.leer_coordenadas()

            for (lat, lon) in self.coordenadas:
                map_widget.set_marker(lat, lon)

            if len(self.coordenadas) > 1:
                map_widget.set_path(self.coordenadas, width=2)

            return self.ventana_mapa


