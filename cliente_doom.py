import cv2
import numpy as np
import base64
import paho.mqtt.client as mqtt
import time
import pygame
import json


class doom_exe:
    
    def __init__(self):
        self.topic_transmitir = "transmitir_doom"
        self.topic_teclas = "imputs_teclas"
        self.broker = "broker.emqx.io"
        self.port = 1883

        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(self.broker, 1883, 60)
        self.ultimo_frame = None
        
        # Inicializar pygame
        pygame.init()
        self.ventana = pygame.display.set_mode((640, 480))
        pygame.display.set_caption("DOOM - Receptor")
        
        
    # mensajes doom
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Conexión exitosa al broker MQTT")
            # Suscribirse a los temas
            self.client.subscribe(self.topic_transmitir)
            self.client.subscribe(self.topic_teclas)
            print(f"Suscrito al tema '{self.topic_transmitir}'")
        else:
            print(f"Error de conexión, código: {rc}")
            
    # recibir mensajes
    def on_message(self, client, userdata, msg):

        if msg.topic == 'transmitir_doom':
            print(f"Frame recibido en '{self.topic_transmitir}'")
            try:
                # Decodificar base64 a bytes
                frame_bytes = base64.b64decode(msg.payload.decode("utf-8"))
                
                # Convertir bytes a array NumPy
                array = np.frombuffer(frame_bytes, np.uint8)
                
                # Decodificar JPEG a imagen OpenCV
                img = cv2.imdecode(array, cv2.IMREAD_COLOR)

                # Convertir de BGR (OpenCV) a RGB (Pygame)
                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                
                # Guardar el frame
                self.ultimo_frame = img_rgb
                
                # Mostrar la imagen
                #cv2.imshow('DOOM - Ventana Completa', img)
                #cv2.waitKey(1) 
            except Exception as e:
                print("Error decodificando frame:", e)

    def detectar_imputs(self):
        last_input = None
        
        while True:
            for event in pygame.event.get():
                pass
            
            # Actualizar pantalla
            if self.ultimo_frame is not None:
                surf = pygame.surfarray.make_surface(np.transpose(self.ultimo_frame, (1, 0, 2)))
                self.ventana.blit(surf, (0, 0))
            else:
                self.ventana.fill((0, 0, 0))
            
            pygame.display.flip()
            
            # Detectar teclas
            tecla = pygame.key.get_pressed()
            imput = None
            
            if tecla[pygame.K_w]:
                imput = 'w'
            elif tecla[pygame.K_a]:
                imput = 'a'
            elif tecla[pygame.K_s]:
                imput = 's'
            elif tecla[pygame.K_d]:
                imput = 'd'
            elif tecla[pygame.K_e]:
                imput = 'espacio'
            elif tecla[pygame.K_SPACE]:
                imput = 'click_izquierdo'
            
            # SIEMPRE enviar si hay tecla presionada 
            if imput is not None:
                # Solo imprimir cuando cambia
                if imput != last_input:
                    print(f"{imput.upper()} presionada")
                self.client.publish(self.topic_teclas, imput, qos=0)
                last_input = imput
            else:
                # Si no hay tecla, enviar "release" una vez
                if last_input is not None:
                    print(f"{last_input.upper()} soltada")
                    self.client.publish(self.topic_teclas, "release", qos=0)
                    last_input = None
            
            time.sleep(0.2)  
""""""""""" 
    def detectar_imputs(self):
        imput = None
        last_pos= None
        while True:
            # Procesar eventos
            for event in pygame.event.get():
                # Actualizar la pantalla SIEMPRE, no solo cuando hay eventos
                if self.ultimo_frame is not None:
                    surf = pygame.surfarray.make_surface(np.transpose(self.ultimo_frame, (1, 0, 2)))
                    self.ventana.blit(surf, (0, 0))
                else:
                    self.ventana.fill((0, 0, 0))
                
                pygame.display.flip()
            
                tecla = pygame.key.get_pressed
                if tecla[pygame.K_w]:
                    imput = 'w'
                    print("W presionada")
                elif tecla[pygame.K_a]:
                    imput = 'a'
                    print("A presionada")
                elif tecla[pygame.K_s]:
                    imput = 's'
                    print("S presionada")
                elif tecla[pygame.K_d]:
                    imput = 'd'
                    print("D presionada")
                elif tecla[pygame.K_SPACE]:
                    imput = 'espacio' 
                    print("espacio presionada")
                elif pygame.mouse.get_pressed()[0]:
                    imput = 'click_izquierdo'
                    print("click izquierdo presionado")

                mx,my = pygame.mouse.get_pos()
                print(f"Posición mouse: {mx},{my}")
                pos = {"mx": mx, "my": my}
                

                if pos != last_pos:
                    mensaje = json.dumps(pos)
                    # retain=False: no guardar mensaje
                    # qos=0: enviar sin garantía (más rápido, descarta si hay congestión)
                    self.client.publish(self.topic_raton, mensaje, qos=0, retain=False)
                    last_pos = pos

                if imput is not None:
                    self.client.publish(self.topic_teclas, imput, qos=0, retain=False)

                time.sleep(0.2)
"""""""""""
                
def main():
    doom = doom_exe()
    doom.client.loop_start()
    doom.detectar_imputs()

if __name__ == "__main__":
    main()