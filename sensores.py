import json
import paho.mqtt.client as mqtt

class Sensor:
    def __init__(self):
        self.BROKER = "broker.emqx.io"  # Cambia esto por tu broker MQTT
        self.PORT = 1883  # Puerto del broker MQTT
        self.TOPICS = ["sensor/data/sen55", "sensor/data/gas_sensor"]  # Temas a los que se suscribirá el cliente

        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        
        self.historial = {
            "sen55": [],
            "gas_sensor": []
        }
    
    # Callback cuando se establece la conexión con el broker
    def on_connect(self,client, userdata, flags, rc):
        if rc == 0:
            print("Conexión exitosa al broker MQTT")
            # Suscribirse a los temas
            for topic in self.TOPICS:
                client.subscribe(topic)
                print(f"Suscrito al tema '{topic}'")
        else:
            print(f"Error de conexión, código: {rc}")

    # Callback cuando se recibe un mensaje en los temas suscritos
    def on_message(self,client, userdata, msg):
        print(f"Mensaje recibido en el tema '{msg.topic}':")
        print(msg.payload.decode("utf-8"))

        try:
            # Decodificar y convertir el mensaje de JSON a diccionario
            payload = json.loads(msg.payload.decode("utf-8"))
            print(json.dumps(payload, indent=4))  # Mostrar el mensaje formateado
            if msg.topic == "sensor/data/sen55":
                self.historial["sen55"].append(payload)
                with open("sen55_data.json", "a") as f:
                    json.dump(payload, f)
                    f.write("\n")  # Añadir una nueva línea después de cada entrada
            elif msg.topic == "sensor/data/gas_sensor":
                self.historial["gas_sensor"].append(payload)
                with open("gas_sensor_data.json", "a") as f:
                    json.dump(payload, f)
                    f.write("\n")  # Añadir una nueva línea después de cada entrada

        except json.JSONDecodeError as e:
            print(f"Error decodificando JSON: {e}")
    
    def historial_sensores(self):
        print("Historial de datos del sensor SEN55:")
        for entry in self.historial["sen55"]:
            print(json.dumps(entry, indent=4))
        
        print("\nHistorial de datos del sensor de gas:")
        for entry in self.historial["gas_sensor"]:
            print(json.dumps(entry, indent=4))



    """""""""
    BROKER = "broker.emqx.io"  # Cambia esto por tu broker MQTT
    PORT = 1883  # Puerto del broker MQTT
    TOPICS = ["sensor/data/sen55", "sensor/data/gas_sensor"]  # Temas a los que se suscribirá el cliente
    # Crear un cliente MQTT
    client = mqtt.Client()

    # Asignar las funciones de callback
    client.on_connect = on_connect
    client.on_message = on_message

    # Conectar al broker MQTT
    client.connect(BROKER, PORT, 60)

    # Bucle principal para mantener la conexión y escuchar mensajes
    print("Esperando mensajes... Presiona Ctrl+C para salir")
    try:
        client.loop_forever()  # Mantener el cliente en ejecución
    except KeyboardInterrupt:
        print("Desconectando del broker...")
        client.disconnect()"""""