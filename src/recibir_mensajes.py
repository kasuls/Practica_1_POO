from meshtastic.protobuf import mesh_pb2, mqtt_pb2, portnums_pb2
from meshtastic import BROADCAST_NUM, protocols
import paho.mqtt.client as mqtt
import time
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64
import re

from abc import ABC, abstractmethod

class plantilla(ABC):
    def __init__(self):
        pass
    @abstractmethod
    def procesar(self, dispositivo, msq, remitente):
        pass

class guardar_texto(plantilla):
    def __init__(self,interfaz):
        self.interfaz = interfaz
        self.mensaje = ""   
    def procesar(self, dispositivo, msq, remitente):
        try:
            payload_str = msq.decoded.payload.decode('utf-8', errors='ignore')
            nombre_largo = remitente

            self.mensaje = f"{nombre_largo}: {payload_str}"
            print(f"Mensaje de {nombre_largo}: {payload_str}")

            with open('historial_mensajes.csv', 'a', encoding='utf-8') as archivo:
                archivo.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')},{self.mensaje}\n")

            dispositivo.agregar_mensaje("Texto", payload_str, remitente)
        except Exception as e:
            return None

class guardar_posicion(plantilla):
    def __init__(self,interfaz):
        self.interfaz = interfaz
        self.mensaje = ""
    def procesar(self, dispositivo, msq, remitente):
        try:
            position = mesh_pb2.Position()
            position.ParseFromString(msq.decoded.payload)

            lat = position.latitude_i
            lon = position.longitude_i
            alt = position.altitude

            contenido = {'x': lat, 'y': lon, 'z': alt}
            self.mensaje = f"{remitente}: {contenido}"

            with open('historial_coordenadas.csv', 'a', encoding='utf-8') as archivo:
                archivo.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')},{remitente}:{contenido}\n")

            dispositivo.agregar_mensaje("Posición", contenido, remitente)

        except Exception:
            return None

class guardar_nodo(plantilla):
    def __init__(self,interfaz):
        self.interfaz = interfaz
        self.mensaje = ""
    def procesar(self, dispositivo, msq, remitente):
        try:
            usuario_info = mesh_pb2.User()
            usuario_info.ParseFromString(msq.decoded.payload)

            contenido = {
                'id': usuario_info.id,
                'nombre_largo': usuario_info.long_name
            }

            self.mensaje = f"{usuario_info.long_name}: {contenido}"
            print(f"Info Nodo de {contenido}")

            with open('historial_nodos.csv', 'a', encoding='utf-8') as archivo:
                archivo.write(f"{contenido}\n")

            dispositivo.agregar_mensaje("Info Nodo", contenido, remitente)

        except Exception:
            return None



class recibir_mensajes():
    def __init__(self, dispositivo, comunicador,interfaz):
        self.dispositivo = dispositivo
        self.comunicador = comunicador
        self.interfaz = interfaz
        self.print_service_envelope = comunicador.print_service_envelope
        self.print_message_packet = comunicador.print_message_packet
        self.debug = comunicador.debug
        self.key = comunicador.key  

        self.guardar_texto = guardar_texto(interfaz)
        self.guardar_posicion = guardar_posicion(interfaz)
        self.guardar_nodo = guardar_nodo(interfaz)
       
    def on_message(self, client, userdata, msg):
        se = mqtt_pb2.ServiceEnvelope()
        try:
            se.ParseFromString(msg.payload)
            
            if self.print_service_envelope:
                print ("")
                print ("Service Envelope:")
                print (se)
            mp = se.packet
            if self.print_message_packet: 
                print ("")
                print ("Message Packet:")
                print(mp)
        except Exception as e:
            print(f"*** ServiceEnvelope: {str(e)}")
            return
        
        if mp.HasField("encrypted") and not mp.HasField("decoded"):
            self.decode_encrypted(mp)

        # Attempt to process the decrypted or encrypted payload
        portNumInt = mp.decoded.portnum if mp.HasField("decoded") else None
        handler = protocols.get(portNumInt) if portNumInt else None

        pb = None
        if handler is not None and handler.protobufFactory is not None:
            pb = handler.protobufFactory()
            pb.ParseFromString(mp.decoded.payload)

        #if pb:
            # Clean and update the payload
            #pb_str = str(pb).replace('\n', ' ').replace('\r', ' ').strip()
            #mp.decoded.payload = pb_str.encode("utf-8")
        #print(mp)
        
        self.guardar_datos(self.dispositivo, mp)
        

    def decode_encrypted(self, mp):
        try:
            key_bytes = base64.b64decode(self.key.encode('ascii'))
            nonce_packet_id = getattr(mp, "id").to_bytes(8, "little")
            nonce_from_node = getattr(mp, "from").to_bytes(8, "little")
            nonce = nonce_packet_id + nonce_from_node
            cipher = Cipher(algorithms.AES(key_bytes), modes.CTR(nonce), backend=default_backend())
            decryptor = cipher.decryptor()
            decrypted_bytes = decryptor.update(getattr(mp, "encrypted")) + decryptor.finalize()
            data = mesh_pb2.Data()
            data.ParseFromString(decrypted_bytes)
            mp.decoded.CopyFrom(data)
        except Exception as e:
            if self.print_message_packet: 
                print(f"failed to decrypt: \n{mp}")
            if self.debug: 
                print(f"*** Decryption failed: {str(e)}")
            return
        
    def mostrar_en_interfaz(self, mensaje):
        if self.interfaz and hasattr(self.interfaz, 'mostrar_en_interfaz'):
            self.interfaz.mostrar_en_interfaz(mensaje)
        else:
            print(mensaje) 
   
    def guardar_datos(self, dispositivo, msq):

        remitente_id = str(getattr(msq, 'from', 'Desconocido'))
        remitente = dispositivo.nombres.get(remitente_id, remitente_id)

        if not msq.HasField("decoded"):
            dispositivo.agregar_mensaje("Cifrado", "No legible", remitente)
            return

        port = msq.decoded.portnum

        if port == portnums_pb2.TEXT_MESSAGE_APP:
            self.guardar_texto.procesar(dispositivo, msq, remitente)
            self.mostrar_en_interfaz(self.guardar_texto.mensaje)
        elif port == portnums_pb2.POSITION_APP:
            self.guardar_posicion.procesar(dispositivo, msq, remitente)
            self.mostrar_en_interfaz(self.guardar_posicion.mensaje)
        elif port == portnums_pb2.NODEINFO_APP:
            self.guardar_nodo.procesar(dispositivo, msq, remitente)
            self.mostrar_en_interfaz(self.guardar_nodo.mensaje)
            
        else:
            payload_str = msq.decoded.payload.decode('utf-8', errors='ignore')
            dispositivo.agregar_mensaje(f"Tipo {port}", payload_str, remitente)

        

        
        """""""""
        if msq.HasField("decoded"):
            payload_str = msq.decoded.payload.decode('utf-8', errors='ignore')
            
            if msq.decoded.portnum == portnums_pb2.TEXT_MESSAGE_APP:
                tipo = "Texto"
                contenido = payload_str
                nombre_largo = remitente # Por defecto
                print(f"Mensaje de {nombre_largo}: {contenido}")
                mensaje = f"{nombre_largo}: {contenido}"
                self.mostrar_en_interfaz(mensaje)
                with open('historial_mensajes.csv', 'a', encoding='utf-8') as archivo:
                    archivo.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')},{nombre_largo}:{contenido}\n")
                
            elif msq.decoded.portnum == portnums_pb2.POSITION_APP:
                tipo = "Posición"
                try:
                    position = mesh_pb2.Position()
                    position.ParseFromString(msq.decoded.payload)
                    
                    lat = position.latitude_i  
                    lon = position.longitude_i
                    alt = position
                    
                    contenido = {'x': lat, 'y': lon, 'z': alt} 
                    print(f"Posición de {remitente}: {contenido}")
                    mensaje_pos = f"{nombre_largo}: {contenido}"
                    self.mostrar_en_interfaz(mensaje_pos)
                    with open('historial_coordenadas.csv', 'a', encoding='utf-8') as archivo:
                        archivo.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')},{remitente}:{contenido}\n")

                except Exception as e:
                    contenido = f"Error: {e}"

            elif msq.decoded.portnum == portnums_pb2.NODEINFO_APP:
                tipo = "Info Nodo" 
                try:
                    usuario_info = mesh_pb2.User()
                    usuario_info.ParseFromString(msq.decoded.payload)
                    id = usuario_info.id
                    nombre_largo = usuario_info.long_name
                    contenido = {'id': id, 'nombre_largo': nombre_largo}
                    print(f"Info Nodo de {contenido}") 
                    mensaje_nodo = f"{nombre_largo}: {contenido}"
                    self.mostrar_en_interfaz(mensaje_nodo)
                    with open('historial_nodos.csv', 'a', encoding='utf-8') as archivo:
                        archivo.write(f"{contenido}\n")
                except Exception as e:
                    contenido = f"Error: {e}"

            else:
                tipo = f"Tipo {msq.decoded.portnum}"
                contenido = payload_str
        else:
            tipo = "Cifrado"
            contenido = "No legible"
        
        dispositivo.agregar_mensaje(tipo, contenido, remitente)
        """""""""
       
    #def guardar_csv(self, dispositivo):
       # with open('historial_mensajes.csv', 'a', encoding='utf-8') as archivo:
        #    for mensaje in dispositivo.historial_mensajes:
               # archivo.write(f"{mensaje['fecha_hora']},{mensaje['remitente']},{mensaje['tipo']},{mensaje['contenido']}\n")
       # print("Historial guardado en historial_mensajes.csv")
        