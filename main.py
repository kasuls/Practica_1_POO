
from meshtastic import BROADCAST_NUM
from src.menu import menu
from src.comunicador import comunicador
from src.dispositivo import Dispositivo
from src.recibir_mensajes import recibir_mensajes
from src.sensores import Sensor
import time

def main():
    # Crear instancias de los módulos necesarios
    dispositivo = Dispositivo()
    Comunicador = comunicador(dispositivo)
    Recibir_mensajes = recibir_mensajes(dispositivo, Comunicador)
    sensor= Sensor()

    # Crear la interfaz del menú pasando los objetos
    interfaz = menu(dispositivo, Comunicador, Recibir_mensajes, sensor)

    # Iniciar el funcionamiento del menú
    interfaz.funcionamiento()

if __name__ == "__main__":
    main()
