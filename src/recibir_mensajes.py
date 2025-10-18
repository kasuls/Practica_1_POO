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


class recibir_mensajes:
    def __init__(self, dispositivo, comunicador):
        self.dispositivo = dispositivo
        self.comunicador = comunicador
        # Copiar atributos del comunicador
        self.print_service_envelope = comunicador.print_service_envelope
        self.print_message_packet = comunicador.print_message_packet
        self.debug = comunicador.debug
        self.key = comunicador.key  # ✅ Añadir esta línea

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

    def guardar_datos(self, dispositivo, msq):
        
        remitente_id = str(getattr(msq, 'from', 'Desconocido'))
        if remitente_id in dispositivo.nombres:
            remitente = dispositivo.nombres[remitente_id]
        else:
            remitente = remitente_id
 
        if msq.HasField("decoded"):
            payload_str = msq.decoded.payload.decode('utf-8', errors='ignore')
            
            if msq.decoded.portnum == portnums_pb2.TEXT_MESSAGE_APP:
                tipo = "Texto"
                contenido = payload_str
                nombre_largo = remitente # Por defecto
                print(f"Mensaje de {nombre_largo}: {contenido}")
                with open('historial_mensajes.csv', 'a', encoding='utf-8') as archivo:
                    archivo.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')},{nombre_largo}:{contenido}\n")
                
            elif msq.decoded.portnum == portnums_pb2.POSITION_APP:
                tipo = "Posición"
                try:
                    position = mesh_pb2.Position()
                    position.ParseFromString(msq.decoded.payload)
                    
                    lat = position.latitude_i  
                    lon = position.longitude_i
                    alt = position.altitude
                    
                    contenido = {'x': lat, 'y': lon, 'z': alt} 
                    print(f"Posición de {remitente}: {contenido}")
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

    #def guardar_csv(self, dispositivo):
       # with open('historial_mensajes.csv', 'a', encoding='utf-8') as archivo:
        #    for mensaje in dispositivo.historial_mensajes:
               # archivo.write(f"{mensaje['fecha_hora']},{mensaje['remitente']},{mensaje['tipo']},{mensaje['contenido']}\n")
       # print("Historial guardado en historial_mensajes.csv")
        