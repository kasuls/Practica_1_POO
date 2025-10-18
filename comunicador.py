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
import json

class comunicador:
    def __init__(self,dispositivo):

        self.debug = True
        self.auto_reconnect = True
        self.auto_reconnect_delay = 1
        self.print_service_envelope = False
        self.print_message_packet = False

        self.dispositivo = dispositivo
        self.mqtt_broker = "mqtt.meshtastic.org"
        self.mqtt_port = 1883
        self.mqtt_username = "meshdev"
        self.mqtt_password = "large4cats"

        self.root_topic = "msh/EU_868/ES/2/e/"
        self.channel = "TestMQTT"
        self.key = "ymACgCy9Tdb8jHbLxUxZ/4ADX+BWLOGVihmKHcHTVyo="
        
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="", clean_session=True, userdata=None)
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.message_text = "message_text"

        
        self.subscribe_topic = ""
        self.publish_topic = ""

    
    # configuración no tocar
    def set_topic(self):
        self.dispositivo.node_name = '!' + hex(self.dispositivo.node_number)[2:]
        self.subscribe_topic = self.root_topic + self.channel + "/#"
        self.publish_topic = self.root_topic + self.channel + "/" + self.dispositivo.node_name

    def xor_hash(self,data):
        result = 0
        for char in data:
            result ^= char
        return result

    def generate_hash(self, name, key):
        replaced_key = key.replace('-', '+').replace('_', '/')
        key_bytes = base64.b64decode(replaced_key.encode('utf-8'))
        h_name = self.xor_hash(bytes(name, 'utf-8'))
        h_key = self.xor_hash(key_bytes)
        return h_name ^ h_key
        
    #coneccion
    def connect_mqtt(self):
        if not hasattr(self, "tls_configured"):
            self.tls_configured = False

        if self.debug:
            print("connect_mqtt")
        if not hasattr(self, "client") or self.client is None:
            raise RuntimeError("El cliente MQTT (self.client) no está inicializado")

        if not self.client.is_connected():
            try:
                if ':' in self.mqtt_broker:
                    self.mqtt_broker, self.mqtt_port = self.mqtt_broker.split(':')
                    self.mqtt_port = int(self.mqtt_port)
                if self.key == "AQ==":
                    if self.debug:
                        print("key is default, expanding to AES128")
                    self.key = "1PG7OiApB1nwvP+rz05pAQ=="
                padded_key = self.key.ljust(len(self.key) + ((4 - (len(self.key) % 4)) % 4), '=')
                replaced_key = padded_key.replace('-', '+').replace('_', '/')
                self.key = replaced_key
                self.client.username_pw_set(self.mqtt_username, self.mqtt_password)
                if self.mqtt_port == 8883 and not self.tls_configured:
                    self.client.tls_set(ca_certs="cacert.pem", tls_version=ssl.PROTOCOL_TLSv1_2)
                    self.client.tls_insecure_set(False)
                    self.tls_configured = True
                self.client.connect(self.mqtt_broker, self.mqtt_port, 60)
                self.client.loop_start()

            except Exception as e:
                print(e)

    def disconnect_mqtt(self):
        if self.debug:
            print("disconnect_mqtt")
        if self.client.is_connected():
            self.client.disconnect()

    def on_connect(self, client, userdata, flags, reason_code, properties=None):
        self.set_topic()
        if self.client.is_connected():
            print("client is connected")
        if reason_code == 0:
            if self.debug:
                print(f"Connected to server: {self.mqtt_broker}")
                print(f"Subscribe Topic is: {self.subscribe_topic}")
                print(f"Publish Topic is: {self.publish_topic}\n")
            client.subscribe(self.subscribe_topic)

    def on_disconnect(self, client, userdata, reason_code, properties=None):
        if self.debug:
            print("on_disconnect")
        if reason_code != 0:
            if self.auto_reconnect:
                print(f"Attempting to reconnect in {self.auto_reconnect_delay} second(s)")
                time.sleep(self.auto_reconnect_delay)
                self.connect_mqtt()
    
    #mandar mensajes
    def direct_message(self, destination_id):
        if self.debug:
            print("direct_message")
        if destination_id:
            try:
                destination_id = int(destination_id[1:], 16)
                self.send_message(destination_id, self.message_text)
            except Exception as e:
                if self.debug:
                    print(f"Error converting destination_id: {e}")

    def send_message(self, destination_id):
        if not self.client.is_connected():
            self.connect_mqtt()

        if self.message_text:
            encoded_message = mesh_pb2.Data()
            encoded_message.portnum = portnums_pb2.TEXT_MESSAGE_APP 
            encoded_message.payload = self.message_text.encode("utf-8")
            self.generate_mesh_packet(destination_id, encoded_message)
        else:
            return

    def send_traceroute(self, destination_id):
        if not self.client.is_connected():
            self.connect_mqtt()
        if self.debug:
            print(f"Sending Traceroute Packet to {str(destination_id)}")

        encoded_message = mesh_pb2.Data()
        encoded_message.portnum = portnums_pb2.TRACEROUTE_APP
        encoded_message.want_response = True

        destination_id = int(destination_id[1:], 16)
        self.generate_mesh_packet(destination_id, encoded_message)

    def send_node_info(self, destination_id, want_response):
        if self.client.is_connected():
            try:
                user_payload = mesh_pb2.User()
                setattr(user_payload, "id", self.dispositivo.node_name)
                setattr(user_payload, "long_name", self.dispositivo.long_name)
                setattr(user_payload, "short_name", self.dispositivo.short_name)
                setattr(user_payload, "hw_model", 0)  
                
                user_payload = user_payload.SerializeToString()

                encoded_message = mesh_pb2.Data()
                encoded_message.portnum = portnums_pb2.NODEINFO_APP
                encoded_message.payload = user_payload
                encoded_message.want_response = want_response
                self.generate_mesh_packet(destination_id, encoded_message)
                
            except Exception as e:
                print(f"Error enviando info de nodo: {e}")

    def send_position(self, destination_id):
        if self.client.is_connected():
            pos_time = int(time.time())
            latitude = int(float(self.dispositivo.lat) * 1e7)
            longitude = int(float(self.dispositivo.lon) * 1e7)
            altitude_units = 1 / 3.28084 if 'ft' in str(self.dispositivo.alt) else 1.0
            altitude = int(altitude_units * float(re.sub('[^0-9.]', '', str(self.dispositivo.alt))))

            position_payload = mesh_pb2.Position()
            setattr(position_payload, "latitude_i", latitude)
            setattr(position_payload, "longitude_i", longitude)
            setattr(position_payload, "altitude", altitude)
            setattr(position_payload, "time", pos_time)

            position_payload = position_payload.SerializeToString()

            encoded_message = mesh_pb2.Data()
            encoded_message.portnum = portnums_pb2.POSITION_APP
            encoded_message.payload = position_payload
            encoded_message.want_response = True

            self.generate_mesh_packet(destination_id, encoded_message)

    def generate_mesh_packet(self, destination_id, encoded_message):
        mesh_packet = mesh_pb2.MeshPacket()

        # Usar el ID global del dispositivo
        mesh_packet.id = self.dispositivo.global_message_id
        self.dispositivo.global_message_id += 1

        setattr(mesh_packet, "from", self.dispositivo.node_number)
        mesh_packet.to = destination_id
        mesh_packet.want_ack = False
        mesh_packet.channel = self.generate_hash(self.channel, self.key)
        mesh_packet.hop_limit = 3

        if self.key == "":
            mesh_packet.decoded.CopyFrom(encoded_message)
        else:
            mesh_packet.encrypted = self.encrypt_message(mesh_packet, encoded_message)

        service_envelope = mqtt_pb2.ServiceEnvelope()
        service_envelope.packet.CopyFrom(mesh_packet)
        service_envelope.channel_id = self.channel
        service_envelope.gateway_id = self.dispositivo.node_name

        payload = service_envelope.SerializeToString()
        self.client.publish(self.publish_topic, payload)

    def encrypt_message(self, mesh_packet, encoded_message):
        mesh_packet.channel = self.generate_hash(self.channel, self.key)
        key_bytes = base64.b64decode(self.key.encode('ascii'))
        nonce_packet_id = mesh_packet.id.to_bytes(8, "little")
        nonce_from_node = self.dispositivo.node_number.to_bytes(8, "little")
        nonce = nonce_packet_id + nonce_from_node
        cipher = Cipher(algorithms.AES(key_bytes), modes.CTR(nonce), backend=default_backend())
        encryptor = cipher.encryptor()
        encrypted_bytes = encryptor.update(encoded_message.SerializeToString()) + encryptor.finalize()
        return encrypted_bytes

    def send_ack(self, destination_id, message_id):
        if self.debug:
            print("Sending ACK")
        encoded_message = mesh_pb2.Data()
        encoded_message.portnum = portnums_pb2.ROUTING_APP
        encoded_message.request_id = message_id
        encoded_message.payload = b"\030\000"
        self.generate_mesh_packet(destination_id, encoded_message)
    

    