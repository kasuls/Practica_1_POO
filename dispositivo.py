from meshtastic.protobuf import mesh_pb2, mqtt_pb2, portnums_pb2
from meshtastic import BROADCAST_NUM, protocols
import paho.mqtt.client as mqtt
import random
import time
import ssl
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64
import re

class Dispositivo:
    def __init__(self):

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