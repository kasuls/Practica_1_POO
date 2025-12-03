import random
import time
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List

T = TypeVar('T')

class plantilla_dispositivo(Generic[T]):
    def __init__(self):
        self.client_short_name = ""
        self.client_long_name = ""
        self.historial_mensajes: List[T] = []  
        self.nodos_conectados = {}
        self.nombres = {}
        self.lat = ''
        self.lon = ''
        self.alt = ''
        self.protocolo = ''

    @abstractmethod
    def agregar_mensaje(self, tipo, contenido: T, remitente, timestamp=None):
        pass

    @abstractmethod
    def mostrar_historial(self):
        pass

    @abstractmethod
    def mostrar_nodos_conectados(self):
        pass

    @abstractmethod
    def mostrar_posicion(self):
        pass

class Dispositivo(plantilla_dispositivo[dict]):
    def __init__(self):
        super().__init__()
        # Genera cosas no tocar
        random_hex_chars = '6d61'
        node_name = '!abcd' + random_hex_chars
        node_number = int(node_name.replace("!", ""), 16)
        global_message_id = random.getrandbits(32)

        # Información 
        client_short_name = "Man"
        client_long_name = "Manuel"

        # historial de mensajes
        self.historial_mensajes = []  # Lista para guardar todos los mensajes
        self.nodos_conectados = {}    # Diccionario para info de nodos conocidos

        # Guardar las variable en atributos
        self.node_name = node_name
        self.node_number = node_number
        self.global_message_id = global_message_id
        self.short_name = client_short_name  
        self.long_name = client_long_name
        self.conectado = False
        self.lat = '42.6860'
        self.lon = '-2.9490'
        self.alt = '471'
        self.protocolo = 'MTTQ'

        #nombres para saber quien es quien
        self.nombres = {
            '2882366817': 'Manuel',
            '2882381985': 'Alejandro',
            '2882347680': 'Aitor', 
            '719928777': 'Jaime1',
            '2925567208': 'jaime2',
            '2882363145': 'esther',
            '2882380738': 'isabel'
        }
    
    # Añadir mensaje al historial
    def agregar_mensaje(self, tipo, contenido, remitente, timestamp=None):

        if timestamp is None:
            timestamp = time.time()
            
        mensaje = {
            'tipo': tipo,
            'contenido': contenido,
            'remitente': remitente,
            'timestamp': timestamp,
            'fecha_hora': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))
        }
        
        self.historial_mensajes.append(mensaje)

    #enseñar el historial
    def mostrar_historial(self):       
        print(f"Historial de mensajes:")
        for i, msg in enumerate(self.historial_mensajes, 1):
            print(f"{i}. {msg['tipo']} de {msg['remitente']}: {msg['contenido']}")