
import tkinter as tk
from src.comunicador import comunicador
from src.dispositivo import Dispositivo
from src.recibir_mensajes import recibir_mensajes
from src.sensores import Sensor
from src.doom import doom_exe
from src.interfaz import MenuRetro
from src.Mapa import mapa
from meshtastic import BROADCAST_NUM

def main():
    dispositivo = Dispositivo()
    doom = doom_exe()
    
    sensores = Sensor(interfaz=None)
    Comunicador = comunicador(dispositivo, doom)
    Recibir_mensajes = recibir_mensajes(dispositivo, Comunicador, interfaz=None)

    # Asignar callback de MQTT
    Comunicador.client.on_message = Recibir_mensajes.on_message

    # Crear ventana Tkinter
    root = tk.Tk()
    mapa_clase = mapa(root)
    # Crear la interfaz
    Interfaz = MenuRetro(root, dispositivo, Comunicador, Recibir_mensajes, sensores, doom,mapa_clase)

    # Asignar la interfaz al recibir_mensajes
    Recibir_mensajes.interfaz = Interfaz
    sensores.interfaz = Interfaz

    # Ejecutar GUI
    root.mainloop()

if __name__ == "__main__":
    main()

""""""""""
def main():
    # Crear instancias de los módulos necesarios
    dispositivo = Dispositivo()
    doom = doom_exe()
    Comunicador = comunicador(dispositivo,doom) 
    Recibir_mensajes = recibir_mensajes(dispositivo, Comunicador)
    sensor= Sensor()
    

    # Crear la interfaz del menú pasando los objetos
    interfaz = menu(dispositivo, Comunicador, Recibir_mensajes, sensor,doom)

    # Iniciar el funcionamiento del menú
    interfaz.funcionamiento()

if __name__ == "__main__":
    main()
"""""""""