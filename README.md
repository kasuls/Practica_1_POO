Sistema de Comunicación Mesh con Sensores

Descripción
Sistema de comunicación en red mesh que permite el intercambio de mensajes, ubicaciones y datos de sensores entre múltiples dispositivos usando el protocolo Meshtastic.

Características Principales
Comunicación Mesh
  -Mensajes de texto entre nodos de la red
  -Compartir ubicación GPS en tiempo real
  -Información de nodos y usuarios conectados
  -Comunicación encriptada para mayor seguridad

Monitoreo de Sensores
  -Datos ambientales del sensor SEN55 (calidad del aire)
  -Lecturas de gas de sensores MQTT
  -Almacenamiento histórico de todas las mediciones
  -Visualización en tiempo real

Gestión de Datos
  -Historial completo de mensajes y ubicaciones
  -Base de datos de nodos conocidos
  -Exportación a CSV para análisis posterior
  -Interfaz de consola intuitiva

Instalación
Prerrequisitos
  -Los csv y json deben estar en la misma carpeta del main 
  -los .py que no son el main deben estar en una carpeta que se llame src
Dependencias Principales
  -meshtastic - Comunicación mesh protocol
  -cryptography - Encriptación de mensajes
  -paho-mqtt - Cliente MQTT para sensores

Clases Principales
Menu: Controlador principal que coordina todas las funcionalidades.
Dispositivo: Gestiona la identidad del dispositivo y almacena todos los datos.
Comunicador: Maneja la conexión MQTT y envío de mensajes mesh.
RecibirMensajes: Procesa y decodifica mensajes entrantes de la red.
Sensor: Monitoriza y almacena datos de sensores externos.

Archivos de Salida
  -historial_mensajes.csv - Todos los mensajes intercambiados
  -historial_coordenadas.csv - Ubicaciones GPS
  -historial_nodos.csv - Información de dispositivos
  -sen55_data.json - Datos del sensor de calidad de aire
  -gas_sensor_data.json - Datos del sensor de gas

