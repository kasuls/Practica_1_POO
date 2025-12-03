# Sistema de Comunicación Mesh con Sensores

Sistema de comunicación en red mesh que permite el intercambio de mensajes, ubicaciones y datos de sensores entre múltiples dispositivos usando el protocolo Meshtastic. Incluye funcionalidades avanzadas como transmisión de videojuegos, visualización de mapas y interfaz gráfica.

## Tabla de Contenidos

- [Características](#características)
- [Requisitos del Sistema](#requisitos-del-sistema)
- [Instalación](#instalación)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Configuración](#configuración)
- [Uso](#uso)
- [Arquitectura del Sistema](#arquitectura-del-sistema)
- [Módulos Principales](#módulos-principales)
- [Archivos de Datos](#archivos-de-datos)
- [Tecnologías Utilizadas](#tecnologías-utilizadas)

## Características

### Comunicación Mesh

- Envío y recepción de mensajes de texto entre nodos de la red
- Compartir ubicación GPS en tiempo real
- Información de nodos y usuarios conectados
- Comunicación encriptada mediante AES-CTR para mayor seguridad
- Soporte para broadcast y mensajes directos

### Monitoreo de Sensores

- Integración con sensor SEN55 para calidad del aire (PM1.0, PM2.5, PM10, temperatura, humedad)
- Lectura de sensores de gas mediante protocolo MQTT
- Almacenamiento histórico de todas las mediciones
- Visualización en tiempo real de datos de sensores
- Control de inicio y detención de escucha de sensores

### Gestión de Datos

- Historial completo de mensajes intercambiados
- Registro de ubicaciones GPS compartidas
- Base de datos de nodos conocidos en la red
- Exportación automática a CSV y JSON
- Persistencia de datos entre sesiones

### Funcionalidades Avanzadas

- **Visualización de Mapas**: Muestra las coordenadas GPS recibidas en un mapa interactivo
- **Transmisión de Videojuegos**: Sistema para transmitir y controlar DOOM remotamente via MQTT
- **Interfaz Gráfica**: GUI con diseño retro usando Tkinter
- **Arquitectura Modular**: Diseño basado en patrones de diseño (Abstract Factory, Template Method)

## Requisitos del Sistema

- Python 3.7 o superior
- Sistema operativo: Windows, Linux o macOS
- Conexión a Internet para broker MQTT
- (Opcional) Dispositivo compatible con Meshtastic para comunicación real
- (Opcional) DOOM ejecutable para funcionalidad de transmisión de juegos

## Instalación

### Paso 1: Clonar el Repositorio

```bash
git clone https://github.com/kasuls/Practica_1_POO.git
cd Practica_1_POO
git checkout practica-2-completa
```

### Paso 2: Instalar Dependencias

```bash
pip install meshtastic
pip install cryptography
pip install paho-mqtt
pip install tkintermapview
pip install opencv-python
pip install numpy
pip install pygetwindow
pip install pyautogui
pip install pygame
```

O usando un archivo requirements.txt:

```bash
pip install -r requirements.txt
```

### Paso 3: Configuración de Archivos

Asegúrate de que la estructura de carpetas sea la siguiente:

```
Practica_1_POO/
├── main.py
├── src/
│   ├── comunicador.py
│   ├── dispositivo.py
│   ├── recibir_mensajes.py
│   ├── sensores.py
│   ├── doom.py
│   ├── interfaz.py
│   └── Mapa.py
├── static/
│   └── variables.json
├── historial_mensajes.csv
├── historial_coordenadas.csv
├── historial_nodos.csv
├── sen55_data.json
└── gas_sensor_data.json
```

### Paso 4: Configurar variables.json

Crea un archivo `static/variables.json` con la siguiente estructura:

```json
{
  "debug": false,
  "auto_reconnect": true,
  "auto_reconnect_delay": 5,
  "print_service_envelope": false,
  "print_message_packet": false,
  "mqtt_broker": "mqtt.meshtastic.org",
  "mqtt_port": 1883,
  "mqtt_username": "meshdev",
  "mqtt_password": "large4cats",
  "root_topic": "msh/EU_868/2/e/",
  "channel": "LongFast",
  "key": "AQ==",
  "chanel_doom": "doom_channel",
  "key_doom": "AQ==",
  "BROKER": "broker.emqx.io",
  "PORT": 1883,
  "TOPICS": ["sensor/data/sen55", "sensor/data/gas_sensor"]
}
```

## Estructura del Proyecto

### Directorio src/

**comunicador.py**
Maneja toda la comunicación MQTT y el protocolo Meshtastic. Gestiona conexión, desconexión, encriptación y envío de diferentes tipos de mensajes.

**dispositivo.py**
Define la identidad del dispositivo local y almacena el historial de mensajes. Implementa el patrón Template Method mediante la clase abstracta `plantilla_dispositivo`.

**recibir_mensajes.py**
Procesa los mensajes entrantes de la red mesh. Utiliza el patrón Strategy con clases especializadas para cada tipo de mensaje (texto, posición, nodo).

**sensores.py**
Gestiona la conexión con sensores externos via MQTT. Almacena datos del SEN55 y sensores de gas en formato JSON.

**doom.py**
Implementa la funcionalidad de transmisión de videojuegos. Captura la pantalla del juego y la transmite via MQTT.

**interfaz.py**
Interfaz gráfica de usuario con diseño retro. Proporciona acceso visual a todas las funcionalidades del sistema.

**Mapa.py**
Visualiza las coordenadas GPS recibidas en un mapa interactivo usando TkinterMapView.

### Directorio static/

**variables.json**
Archivo de configuración centralizado con todos los parámetros del sistema (brokers, credenciales, topics, claves de encriptación).

### Archivos de Datos

Los archivos CSV y JSON se generan automáticamente al recibir datos:

- `historial_mensajes.csv`: Registro de todos los mensajes de texto
- `historial_coordenadas.csv`: Coordenadas GPS compartidas
- `historial_nodos.csv`: Información de dispositivos detectados
- `sen55_data.json`: Datos del sensor de calidad del aire
- `gas_sensor_data.json`: Lecturas del sensor de gas

## Configuración

### Configuración de la Red Mesh

Edita los siguientes parámetros en `static/variables.json`:

- **mqtt_broker**: Dirección del broker MQTT (por defecto: mqtt.meshtastic.org)
- **mqtt_port**: Puerto del broker (1883 para no-TLS, 8883 para TLS)
- **channel**: Canal de comunicación mesh (ej: "LongFast")
- **key**: Clave de encriptación en base64 (por defecto: "AQ==" que se expande a AES128)

### Configuración de Sensores

Los sensores se configuran con:

- **BROKER**: Broker MQTT para sensores (por defecto: broker.emqx.io)
- **PORT**: Puerto del broker de sensores (por defecto: 1883)
- **TOPICS**: Lista de topics MQTT a los que suscribirse

### Configuración del Dispositivo

En `dispositivo.py`, modifica:

```python
client_short_name = "Man"
client_long_name = "Manuel"
self.lat = '42.6860'
self.lon = '-2.9490'
self.alt = '471'
```

## Uso

### Ejecución del Programa

```bash
python main.py
```

Esto iniciará la interfaz gráfica con todas las funcionalidades disponibles.

### Interfaz Gráfica

La ventana principal muestra:

- **Panel lateral izquierdo**: Menú con botones de acciones
- **Consola central**: Visualización de mensajes y eventos en tiempo real
- **Indicador de estado**: Muestra conexión mesh, sensores y cantidad de mensajes

### Funcionalidades Disponibles

**Enviar mensaje**
Abre una ventana modal para escribir y enviar un mensaje de texto a la red mesh.

**Enviar posición**
Transmite las coordenadas GPS configuradas en el dispositivo.

**Ver sensores**
Inicia la escucha de datos de sensores MQTT. Los datos se muestran en tiempo real en la consola.

**Detener sensores**
Detiene la recepción de datos de sensores.

**Ver mapa**
Abre una ventana con un mapa interactivo mostrando todas las coordenadas GPS recibidas.

**DOOM**
Lanza el ejecutable de DOOM (requiere configurar la ruta del ejecutable en doom.py).

**Transmitir DOOM**
Inicia la transmisión de la ventana de DOOM via MQTT para visualización remota.

**Historial mensajes**
Muestra todos los mensajes recibidos con formato estructurado.

**Historial sensores**
Visualiza todos los datos históricos de los sensores SEN55 y de gas.

**Info sistema**
Muestra información completa del dispositivo, conexiones y estado del sistema.

### Cliente DOOM (Opcional)

Para recibir la transmisión de DOOM en otro dispositivo:

```bash
python src/cliente_doom.py
```

Controles del cliente:
- W, A, S, D: Movimiento
- E: Abrir puertas
- Espacio: Disparar

## Arquitectura del Sistema

### Patrones de Diseño Implementados

**Template Method**
La clase `plantilla_dispositivo` define la estructura base que debe implementar cualquier dispositivo, permitiendo diferentes implementaciones concretas.

**Strategy**
Las clases `guardar_texto`, `guardar_posicion` y `guardar_nodo` implementan diferentes estrategias para procesar distintos tipos de mensajes.

**Observer**
El sistema MQTT implementa un patrón observer donde los clientes se suscriben a topics y reaccionan a eventos.

### Flujo de Comunicación

1. **Envío de mensaje**:
   - Usuario escribe mensaje en interfaz
   - Comunicador codifica el mensaje en formato Meshtastic
   - Mensaje se encripta con AES-CTR
   - Se publica en el topic MQTT correspondiente

2. **Recepción de mensaje**:
   - Cliente MQTT recibe payload del broker
   - Se deserializa el ServiceEnvelope
   - Se desencripta el mensaje si está cifrado
   - Se identifica el tipo de mensaje (texto, posición, nodo)
   - Se procesa según el tipo y se guarda en historial
   - Se actualiza la interfaz gráfica

### Encriptación

El sistema utiliza AES en modo CTR (Counter) para encriptación:

- **Clave**: Base64 codificada, configurable en variables.json
- **Nonce**: Combinación de ID del paquete y nodo origen (16 bytes)
- **Algoritmo**: AES-128 o AES-256 dependiendo de la longitud de la clave

## Módulos Principales

### comunicador.py

**Responsabilidades**:
- Gestionar conexión MQTT con el broker
- Enviar mensajes de texto, posiciones y información de nodos
- Encriptar y desencriptar mensajes
- Generar paquetes Meshtastic válidos
- Manejar reconexión automática

**Métodos principales**:
- `connect_mqtt()`: Establece conexión con el broker
- `send_message(destination_id)`: Envía mensaje de texto
- `send_position(destination_id)`: Envía coordenadas GPS
- `send_node_info(destination_id, want_response)`: Envía información del nodo
- `encrypt_message(mesh_packet, encoded_message)`: Encripta payload
- `generate_mesh_packet(destination_id, encoded_message)`: Crea paquete mesh

### recibir_mensajes.py

**Responsabilidades**:
- Recibir y procesar mensajes MQTT
- Desencriptar mensajes cifrados
- Clasificar mensajes por tipo
- Guardar mensajes en historial y archivos CSV/JSON
- Actualizar interfaz gráfica

**Clases principales**:
- `plantilla`: Clase abstracta para procesamiento de mensajes
- `guardar_texto`: Procesa mensajes de texto
- `guardar_posicion`: Procesa datos de ubicación GPS
- `guardar_nodo`: Procesa información de nodos

**Métodos principales**:
- `on_message(client, userdata, msg)`: Callback para mensajes MQTT
- `decode_encrypted(mp)`: Desencripta mensajes
- `guardar_datos(dispositivo, msq)`: Clasifica y guarda mensajes

### dispositivo.py

**Responsabilidades**:
- Almacenar identidad del dispositivo
- Mantener historial de mensajes
- Gestionar lista de nodos conocidos
- Proporcionar interfaz para consultar datos

**Atributos principales**:
- `node_name`: Identificador único del nodo
- `node_number`: Número del nodo en formato entero
- `historial_mensajes`: Lista de todos los mensajes recibidos
- `nombres`: Diccionario de IDs a nombres de usuario
- `lat`, `lon`, `alt`: Coordenadas GPS del dispositivo

**Métodos principales**:
- `agregar_mensaje(tipo, contenido, remitente, timestamp)`: Añade mensaje al historial
- `mostrar_historial()`: Imprime el historial de mensajes

### sensores.py

**Responsabilidades**:
- Conectar con broker MQTT de sensores
- Suscribirse a topics de sensores
- Procesar datos JSON de sensores
- Almacenar historial de mediciones
- Guardar datos en archivos JSON

**Métodos principales**:
- `on_connect(client, userdata, flags, rc)`: Callback de conexión
- `on_message(client, userdata, msg)`: Procesa datos de sensores
- `historial_sensores()`: Muestra el historial completo
- `iniciar_escucha()`: Inicia conexión con sensores
- `detener_escucha()`: Detiene conexión

### interfaz.py

**Responsabilidades**:
- Proporcionar interfaz gráfica con Tkinter
- Mostrar mensajes y eventos en tiempo real
- Gestionar interacciones del usuario
- Coordinar acciones entre módulos

**Componentes principales**:
- Panel de menú lateral con botones de acción
- Consola de texto scrollable para mensajes
- Indicador de estado del sistema
- Ventanas modales para entrada de datos

**Métodos principales**:
- `crear_estructura()`: Construye la interfaz visual
- `mostrar_en_interfaz(msg)`: Añade texto a la consola
- `enviar_mensaje()`: Ventana modal para envío de mensajes
- `ver_historial()`: Muestra historial con formato
- `ver_sensores()`: Inicia escucha de sensores
- `info_sistema()`: Muestra información del dispositivo

### Mapa.py

**Responsabilidades**:
- Leer coordenadas del archivo CSV
- Convertir coordenadas Meshtastic a formato GPS estándar
- Visualizar ubicaciones en mapa interactivo
- Trazar rutas entre coordenadas

**Métodos principales**:
- `leer_coordenadas()`: Lee y convierte coordenadas del CSV
- `crear_mapa()`: Abre ventana con mapa interactivo

### doom.py

**Responsabilidades**:
- Lanzar el ejecutable de DOOM
- Capturar la ventana del juego
- Comprimir y codificar frames en base64
- Transmitir video via MQTT
- Recibir comandos de control remoto

**Métodos principales**:
- `correr_doom()`: Ejecuta el juego
- `transmitir_ventana()`: Captura y transmite frames
- `on_message(client, userdata, msg)`: Procesa comandos de teclado

### cliente_doom.py

**Responsabilidades**:
- Recibir stream de video de DOOM
- Decodificar frames base64
- Mostrar video en ventana Pygame
- Capturar inputs del usuario
- Enviar comandos al servidor

**Métodos principales**:
- `on_message(client, userdata, msg)`: Recibe y decodifica frames
- `detectar_imputs()`: Captura teclado y ratón

## Archivos de Datos

### historial_mensajes.csv

Formato:
```csv
timestamp,remitente:mensaje
2024-01-15 10:30:45,Manuel: Hola desde la red mesh
```

### historial_coordenadas.csv

Formato:
```csv
timestamp,remitente:{'x': latitud_i, 'y': longitud_i, 'z': altitud}
2024-01-15 10:30:45,Manuel:{'x': 426860000, 'y': -29490000, 'z': 471}
```

### historial_nodos.csv

Formato:
```csv
{'id': '!abcd6d61', 'nombre_largo': 'Manuel'}
```

### sen55_data.json

Ejemplo de estructura:
```json
{
  "pm1": 5.2,
  "pm2_5": 8.1,
  "pm10": 12.3,
  "temperature": 22.5,
  "humidity": 45.2,
  "timestamp": "2024-01-15T10:30:45"
}
```

### gas_sensor_data.json

Ejemplo de estructura:
```json
{
  "gas_concentration": 150,
  "sensor_type": "CO2",
  "timestamp": "2024-01-15T10:30:45"
}
```

## Tecnologías Utilizadas

### Comunicación y Redes

- **Meshtastic**: Protocolo de comunicación mesh de largo alcance
- **MQTT**: Protocol de mensajería ligero para IoT
- **Paho-MQTT**: Cliente MQTT para Python

### Seguridad

- **Cryptography**: Biblioteca de criptografía para encriptación AES
- **Base64**: Codificación de claves y datos binarios

### Interfaz Gráfica

- **Tkinter**: Framework GUI nativo de Python
- **TkinterMapView**: Widget de mapas interactivos para Tkinter

### Procesamiento de Video

- **OpenCV**: Procesamiento y codificación de imágenes
- **NumPy**: Manipulación de arrays para imágenes
- **PyAutoGUI**: Captura de pantalla
- **PyGetWindow**: Gestión de ventanas del sistema
- **Pygame**: Renderizado de video y captura de inputs

### Datos

- **JSON**: Almacenamiento de configuración y datos de sensores
- **CSV**: Persistencia de historial de mensajes y coordenadas

## Solución de Problemas

### Error de conexión MQTT

Si no puedes conectar al broker:
- Verifica las credenciales en `variables.json`
- Comprueba la conectividad a Internet
- Asegúrate de que el broker está accesible (ping al servidor)

### Mensajes no se descifran

Si recibes mensajes cifrados que no puedes leer:
- Verifica que la clave (`key`) en `variables.json` coincida con la del canal
- Asegúrate de estar suscrito al canal correcto

### Sensores no se conectan

Si los sensores no responden:
- Verifica el broker y topics en `variables.json`
- Comprueba que los sensores están publicando datos
- Revisa la conexión de red

### DOOM no se transmite

Si la transmisión de DOOM falla:
- Verifica que la ruta al ejecutable en `doom.py` es correcta
- Asegúrate de que el archivo DOOM.WAD existe
- Comprueba que la ventana de DOOM se detecta correctamente

## Licencia

Este proyecto es parte de una práctica académica de Programación Orientada a Objetos.

## Autores

- Manuel - [@kasuls](https://github.com/kasuls)

## Contacto

Para preguntas o sugerencias sobre el proyecto, abre un issue en el repositorio de GitHub.
