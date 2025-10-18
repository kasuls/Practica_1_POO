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

📁 Estructura del Proyecto
text
proyecto/
├── menu.py              # Menú principal y controlador
├── dispositivo.py       # Gestión del dispositivo y datos
├── comunicador.py      # Comunicaciones MQTT mesh
├── recibir_mensajes.py # Procesamiento de mensajes
├── sensores.py         # Monitoreo de sensores externos
├── static/
│   └── variables.json  # Configuración
├── historial_mensajes.csv
├── historial_coordenadas.csv
└── historial_nodos.csv
🎮 Uso
Ejecución del Sistema
bash
python main.py
Menú Principal
text
1. Enviar mensaje
2. Enviar posición
3. Ver historial
4. Ver sensores
5. Ver historial sensores
6. Salir
Funcionalidades
📨 Enviar Mensajes
Mensajes de texto a todos los nodos (broadcast)

Mensajes directos a nodos específicos

Encriptación automática

🗺️ Compartir Ubicación
Coordenadas GPS actuales

Altitud y timestamp

Actualización en tiempo real

📊 Monitoreo de Sensores
SEN55: Calidad del aire, partículas PM2.5/PM10

Gas Sensor: Detección de gases y compuestos

Datos en tiempo real vía MQTT

Almacenamiento automático en JSON

📈 Historiales
Mensajes enviados/recibidos

Ubicaciones compartidas

Datos de sensores históricos

Información de nodos conectados

🔧 Clases Principales
Menu
Controlador principal que coordina todas las funcionalidades.

Dispositivo
Gestiona la identidad del dispositivo y almacena todos los datos.

Comunicador
Maneja la conexión MQTT y envío de mensajes mesh.

RecibirMensajes
Procesa y decodifica mensajes entrantes de la red.

Sensor
Monitoriza y almacena datos de sensores externos.

🔐 Seguridad
Encriptación AES para todos los mensajes

Canales privados con clave compartida

Autenticación MQTT con usuario/contraseña

Conexiones TLS para comunicación segura

📊 Archivos de Salida
historial_mensajes.csv - Todos los mensajes intercambiados

historial_coordenadas.csv - Ubicaciones GPS

historial_nodos.csv - Información de dispositivos

sen55_data.json - Datos del sensor de calidad de aire

gas_sensor_data.json - Datos del sensor de gas

🐛 Solución de Problemas
Conexión MQTT Fallida
Verificar credenciales en variables.json

Confirmar que el broker esté accesible

Revisar configuración de firewall

Mensajes No Recibidos
Confirmar que todos los nodos usen el mismo canal

Verificar la clave de encriptación

Revisir suscripciones MQTT

Sensores Sin Datos
Verificar conexión al broker de sensores

Confirmar topics MQTT correctos

Revisar formato de datos JSON

🤝 Contribución
Fork del proyecto

Crear rama feature (git checkout -b feature/AmazingFeature)

Commit cambios (git commit -m 'Add AmazingFeature')

Push a la rama (git push origin feature/AmazingFeature)

Abrir Pull Request

📄 Licencia
Distribuido bajo la Licencia MIT. Ver LICENSE para más información.

👥 Autores
Manuel - Desarrollo inicial

Alejandro - Colaborador

Aitor - Colaborador

Jaime - Colaborador

📞 Soporte
Para soporte técnico o consultas:

Abrir un issue en el repositorio

Contactar al equipo de desarrollo

