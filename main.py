from comunicador import comunicador
from dispositivo import Dispositivo
from meshtastic import BROADCAST_NUM
from recibir_mensajes import recibir_mensajes
from sensores import Sensor  # ✅ Añadir import del sensor
import time

def menu():
    print('menu')
    print("1. Enviar mensaje")
    print("2. Enviar posición") 
    print("3. Ver historial")
    print("4. Ver nodos")
    print("5. Ver sensores")  
    print("6. Ver historial sensores")
    print("7. Salir")
    print("="*40)

def main():
    # INICIALIZACIÓN SIMPLIFICADA
    dispositivo = Dispositivo()
    c = comunicador(dispositivo)
    r = recibir_mensajes(dispositivo, c)
    s = Sensor()

    # Configurar handlers
    c.client.on_message = r.on_message
    
    print("Conectando a Meshtastic MQTT...")
    c.connect_mqtt()
    time.sleep(3)
    
    if c.client.is_connected():
        print("Conectado - Sistema listo")
        
        while True:
            menu()
            opcion = input("Opción: ").strip()
            
            if opcion == "1":
                mensaje = input("Mensaje: ")
                if mensaje:
                    c.message_text = mensaje
                    c.send_message(BROADCAST_NUM)
                
            elif opcion == "2":
                c.send_position(BROADCAST_NUM)
                
            elif opcion == "3":
                dispositivo.mostrar_historial()
                
            elif opcion == "4":
                if dispositivo.nodos_conectados:
                    for nodo_id, info in dispositivo.nodos_conectados.items():
                        nombre = info.get('nombre_largo', nodo_id)
                        print(f"  👤 {nodo_id}: {nombre}")
                else:
                    print(" No hay nodos conectados")
                    
            elif opcion == "5":  
                # Conectar al broker MQTT
                s.client.connect(s.BROKER, s.PORT, 60)

                # Bucle principal para mantener la conexión y escuchar mensajes
                print("Esperando mensajes... Presiona Ctrl+C para salir")
                try:
                    s.client.loop_forever()  # Mantener el cliente en ejecución
                except KeyboardInterrupt:
                    print("Desconectando del broker...")
                    s.client.disconnect()

            elif opcion == "6":
                s.historial_sensores()  # Mostrar historial de sensores

            elif opcion == "7":
                print("Saliendo...")
                break
                
            else:
                print("Opción no válida")
    
    c.disconnect_mqtt()
    print("Programa terminado")

if __name__ == "__main__":
    main()