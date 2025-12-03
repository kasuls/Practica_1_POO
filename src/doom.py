import subprocess
import time
import pygetwindow as gw
import pyautogui
import cv2
import numpy as np
import base64
import paho.mqtt.client as mqtt

class doom_exe:
    
    def __init__(self):
        self.wad = "C:\\Users\\manuel\\Desktop\\Practica_1_POO\\DOOM.WAD"
        self.exe = "C:\\Users\\manuel\\Desktop\\crispy-doom-7.1.0-win64\\crispy-doom.exe"
        self.captura = None
        self.topic_transmitir = "transmitir_doom"
        self.topic_teclas = "imputs_teclas"
        self.broker = "broker.emqx.io"
        self.port = 1883

        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(self.broker, 1883, 60)
        self.client.loop_start()
        
    def correr_doom(self):
        command = [self.exe, self.wad]
        subprocess.Popen(command)
        print("Doom lanzado")
        
    def transmitir_ventana(self):
        print("Transmitiendo ventana de DOOM... Presiona 'q' para salir")
        
        while True:
            try:
                # Buscar ventana de DOOM
                ventana = gw.getWindowsWithTitle("The Ultimate DOOM - Crispy Doom")[0]
                # Capturar toda la ventana
                self.captura = pyautogui.screenshot(region=(
                    ventana.left,
                    ventana.top, 
                    ventana.width,
                    ventana.height
                ))
                
                # Convertir para mostrar
                img = np.array(self.captura) 
                img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
                img = cv2.resize(img, (640, 480))

                encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 20]  # ajustar compresión
                _, buffer = cv2.imencode('.jpg', img, encode_param)
                frame = base64.b64encode(buffer).decode('utf-8')
                self.client.publish(self.topic_transmitir, frame)
                

                # Salir con 'q'
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                  
            except:
                print("Esperando ventana de DOOM...")
                time.sleep(1)

        
        cv2.destroyAllWindows()

    # mensajes doom
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Conexión exitosa al broker MQTT")
            # Suscribirse a los temas
            self.client.subscribe(self.topic_teclas)
        else:
            print(f"Error de conexión, código: {rc}")

    def on_message(self, client, userdata, msg):
        if msg.topic == self.topic_teclas:
            imput = msg.payload.decode("utf-8")
            print(f"Input recibido: {imput}")
            
            if imput == "release":
                # Soltar todas las teclas
                pyautogui.keyUp('up')
                pyautogui.keyUp('down')
                pyautogui.keyUp('left')
                pyautogui.keyUp('right')
                pyautogui.keyUp('space')
            elif imput == "w":
                pyautogui.keyDown('up')  # Mantener presionada
            elif imput == "s":
                pyautogui.keyDown('down')
            elif imput == "a":
                pyautogui.keyDown('left')
            elif imput == "d":
                pyautogui.keyDown('right')
            elif imput == "espacio":
                pyautogui.keyDown('space')
            elif imput == "click_izquierdo":
                pyautogui.keyDown('ctrl')
        
