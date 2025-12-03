
from meshtastic import BROADCAST_NUM
import time
import threading

class menu:
    def __init__(self, dispositivo, comunicador, recibir_mensajes, sensor,doom_exe):
        self.dispositivo = dispositivo
        self.comunicador = comunicador
        self.recibir_mensajes = recibir_mensajes
        self.sensor = sensor
        self.doom = doom_exe

    
    def funcionamiento(self):   
        # Configurar handlers
        self.comunicador.client.on_message = self.recibir_mensajes.on_message
        self.comunicador.connect_mqtt()
        time.sleep(3)  # Esperar a que se establezca la conexión

        if self.comunicador.client.is_connected():
            print("Conectado")
            
            while True:
                print('menu')
                print("1. Enviar mensaje")
                print("2. Enviar posición") 
                print("3. Ver historial")
                print("4. Ver sensores")  
                print("5. Ver historial sensores")
                print("6.doom")
                print("7. Salir")
                
                opcion = input("elija una opcion")
                
                if opcion == "1":
                    mensaje = input("Mensaje: ")
                    if mensaje:
                        self.comunicador.message_text = mensaje
                        self.comunicador.send_message(BROADCAST_NUM)
                    
                elif opcion == "2":
                    self.comunicador.send_position(BROADCAST_NUM)
                    
                elif opcion == "3":
                    self.dispositivo.mostrar_historial()
                        
                elif opcion == "4":  

                    self.sensor.client.connect(self.sensor.BROKER, self.sensor.PORT, 60)
                    print("presiona Ctrl+C para salir")
                    try:
                        self.sensor.client.loop_forever()  
                    except KeyboardInterrupt:
                        self.sensor.client.disconnect()

                elif opcion == "5":
                    self.sensor.historial_sensores()  # Mostrar historial de sensores
                
                elif opcion == "6":
                    self.doom.client.loop_start()   
                    print("Cliente DOOM esperando conexión...")
                    time.sleep(1)
                    self.doom.correr_doom()
                    self.doom.transmitir_ventana()
                    
                elif opcion == "7":
                    print("Saliendo...")
                    break
                    
                else:
                    print("Opción no válida")
        
        self.comunicador.disconnect_mqtt()
        print("Programa terminado")
