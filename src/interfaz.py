import tkinter as tk
import threading
from tkinter import scrolledtext, messagebox
from meshtastic import BROADCAST_NUM
import json

class MenuRetro:
    def __init__(self, root, dispositivo, comunicador, recibir_mensajes, sensores, doom,Mapa):
        self.root = root
        self.dispositivo = dispositivo
        self.comunicador = comunicador
        self.recibir_mensajes = recibir_mensajes
        self.sensor = sensores
        self.doom = doom
        self.mapa = Mapa

        # Configurar handlers de mensajes
        self.comunicador.client.on_message = self.recibir_mensajes.on_message
        self.comunicador.connect_mqtt()

        # Configuración ventana - MEJORADA
        self.root.title("⚡ Terminal Retro Mesh Network ⚡")
        self.root.configure(bg="black")
        self.root.geometry("1100x750")

        # Crear estructura visual mejorada
        self.crear_estructura()
        
        # Mensaje inicial
        self.mostrar_en_interfaz("═" * 80 + "\n")
        self.mostrar_en_interfaz("           SISTEMA MESH NETWORK INICIADO           \n")
        self.mostrar_en_interfaz("═" * 80 + "\n")
        self.mostrar_en_interfaz("Conectando a la red Mesh...\n\n")

        # Verificar conexión
        self.root.after(3000, self.verificar_conexion)

    def crear_estructura(self):
        """Estructura visual mejorada con menú lateral"""
        # Frame contenedor principal
        self.container = tk.Frame(self.root, bg="black")
        self.container.pack(fill=tk.BOTH, expand=True)

        # ========== MENÚ LATERAL ==========
        self.menu_frame = tk.Frame(self.container, bg="#001100", width=220, borderwidth=2, relief="raised")
        self.menu_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        self.menu_frame.pack_propagate(False)

        # Título del menú
        titulo = tk.Label(self.menu_frame, text="⚡ MESH NET ⚡", bg="#001100", fg="#00FF55",
                         font=("Courier", 16, "bold"), pady=15)
        titulo.pack(fill=tk.X)

        # Separador
        tk.Frame(self.menu_frame, height=2, bg="#00FF55").pack(fill=tk.X, padx=10)

        # Subtítulo
        subtitulo = tk.Label(self.menu_frame, text="ACCIONES", bg="#001100", fg="#00AA33",
                            font=("Courier", 10, "bold"), pady=8)
        subtitulo.pack(fill=tk.X)

        # Crear botones del menú
        self.crear_botones()

        # Indicador de estado en tiempo real
        tk.Frame(self.menu_frame, height=2, bg="#00FF55").pack(fill=tk.X, padx=10, pady=15, side=tk.BOTTOM)
        
        self.estado_label = tk.Label(self.menu_frame, text="", bg="#001100", fg="#00AA33",
                                     font=("Courier", 8), wraplength=180, justify=tk.LEFT)
        self.estado_label.pack(side=tk.BOTTOM, pady=5, padx=5)

        # Botón salir mejorado
        salir_btn = tk.Button(self.menu_frame, text="🚪 SALIR", command=self.confirmar_salida,
                             bg="#220000", fg="#FF5555", activebackground="#330000",
                             activeforeground="#FF8888", font=("Courier", 11, "bold"),
                             width=22, height=2, borderwidth=2, relief="raised")
        salir_btn.pack(side=tk.BOTTOM, pady=5, padx=5)

        # ========== ÁREA DE CONTENIDO ==========
        contenido_frame = tk.Frame(self.container, bg="black")
        contenido_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Header superior
        header_frame = tk.Frame(contenido_frame, bg="#001100", borderwidth=2, relief="raised")
        header_frame.pack(fill=tk.X, pady=(0, 10))

        tk.Label(header_frame, text="📨 CONSOLA PRINCIPAL", bg="#001100", fg="#00FF55",
                font=("Courier", 20, "bold"), pady=12).pack()
        
        tk.Label(header_frame, text="Mensajes y eventos del sistema en tiempo real", bg="#001100", fg="#00AA33",
                font=("Courier", 10), pady=5).pack()

        # Pantalla de salida mejorada
        self.screen = scrolledtext.ScrolledText(
            contenido_frame, bg="#001100", fg="#00FF55",
            insertbackground="green", font=("Courier", 11), borderwidth=2, relief="sunken", wrap=tk.WORD
        )
        self.screen.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Actualizar estado cada 3 segundos
        self.actualizar_estado()

    def actualizar_estado(self):
        """Actualiza el indicador de estado"""
        mesh = "🟢" if self.comunicador.client.is_connected() else "🔴"
        sens = "🟢" if self.sensor.escuchando else "⚪"
        msgs = len(self.dispositivo.historial_mensajes)
        
        estado_texto = f"Mesh: {mesh}\nSensores: {sens}\nMensajes: {msgs}"
        self.estado_label.config(text=estado_texto)
        
        self.root.after(3000, self.actualizar_estado)

    def crear_botones(self):
        """Crea los botones del menú lateral con diseño mejorado"""
        botones = [
            ("📨 Enviar mensaje", self.enviar_mensaje),
            ("📍 Enviar posición", self.enviar_posicion),
            ("📊 Ver sensores", self.ver_sensores),
            ("🛑 Detener sensores", self.detener_sensores),
            ("🗺️ Ver mapa", self.mapa.crear_mapa),
            ("🎮 DOOM", self.lanzar_doom),
            ("📋 Historial mensajes", self.ver_historial),
            ("📈 Historial sensores", self.historial_sensor),
            ("🖥️ Transmitir DOOM", self.transmitir_doom),
            ("⚙️ Info sistema", self.info_sistema)
        ]

        for texto, comando in botones:
            btn = tk.Button(self.menu_frame, text=texto, command=comando,
                          bg="#002200", fg="#00FF55", activebackground="#003300",
                          activeforeground="#00FF55", font=("Courier", 10, "bold"),
                          width=22, height=2, relief="flat", borderwidth=1,
                          highlightthickness=0, anchor="w", padx=10)
            btn.pack(pady=2, padx=5)

    def mostrar_en_interfaz(self, msg):
        """Muestra mensajes en la consola"""
        self.screen.insert(tk.END, msg)
        self.screen.see(tk.END)
        self.root.update()

    def verificar_conexion(self):
        """Verifica la conexión a la red"""
        estado = "✅ Conectado" if self.comunicador.client.is_connected() else "❌ Desconectado"
        self.mostrar_en_interfaz(f"{estado} a la red Mesh\n")
        self.mostrar_en_interfaz(f"Dispositivo: {self.dispositivo.short_name}\n")
        self.mostrar_en_interfaz(f"ID: {self.dispositivo.node_name}\n\n")

    def enviar_mensaje(self):
        """Ventana modal mejorada para enviar mensaje"""
        win = tk.Toplevel(self.root)
        win.title("📤 Enviar Mensaje")
        win.configure(bg="black")
        win.geometry("450x220")
        win.resizable(False, False)

        # Header de la ventana
        header = tk.Frame(win, bg="#001100", borderwidth=2, relief="raised")
        header.pack(fill=tk.X, pady=(0, 10))
        tk.Label(header, text="ENVIAR MENSAJE A LA RED", bg="#001100", fg="#00FF55",
                font=("Courier", 12, "bold"), pady=10).pack()

        # Frame principal
        main_frame = tk.Frame(win, bg="black")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10)

        tk.Label(main_frame, text="Mensaje:", bg="black", fg="#00FF55",
                font=("Courier", 11, "bold")).pack(pady=(10, 5), anchor="w")

        entry = tk.Entry(main_frame, bg="#002200", fg="#00FF55", insertbackground="green",
                        width=45, font=("Courier", 11), borderwidth=2, relief="sunken")
        entry.pack(padx=5, pady=5)
        entry.focus()

        def send():
            msg = entry.get().strip()
            if msg:
                try:
                    self.comunicador.message_text = msg
                    self.comunicador.send_message(BROADCAST_NUM)
                    self.mostrar_en_interfaz(f"📤 [MENSAJE ENVIADO] {msg}\n")
                except Exception as e:
                    self.mostrar_en_interfaz(f"❌ [ERROR] {e}\n")
            win.destroy()

        btn_frame = tk.Frame(main_frame, bg="black")
        btn_frame.pack(pady=15)

        tk.Button(btn_frame, text="📤 Enviar", command=send, bg="#002200", fg="#00FF55",
                 width=12, height=2, font=("Courier", 10, "bold"),
                 relief="raised", borderwidth=2).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="❌ Cancelar", command=win.destroy, bg="#220000",
                 fg="#FF5555", width=12, height=2, font=("Courier", 10, "bold"),
                 relief="raised", borderwidth=2).pack(side=tk.LEFT, padx=5)

        win.bind('<Return>', lambda e: send())
        win.bind('<Escape>', lambda e: win.destroy())

    def enviar_posicion(self):
        """Envía la posición actual"""
        try:
            self.comunicador.send_position(BROADCAST_NUM)
            self.mostrar_en_interfaz(f"📍 [POSICIÓN ENVIADA] Lat: {self.dispositivo.lat}, Lon: {self.dispositivo.lon}\n")
        except Exception as e:
            self.mostrar_en_interfaz(f"❌ Error al enviar posición: {e}\n")

    def ver_historial(self):
        """Muestra el historial de mensajes con formato mejorado"""
        self.mostrar_en_interfaz("\n" + "═" * 80 + "\n")
        self.mostrar_en_interfaz("                    HISTORIAL DE MENSAJES\n")
        self.mostrar_en_interfaz("═" * 80 + "\n\n")
        
        if self.dispositivo.historial_mensajes:
            for i, msg in enumerate(self.dispositivo.historial_mensajes, 1):
                self.mostrar_en_interfaz(f"[{i:03d}] ─────────────────────────────────\n")
                self.mostrar_en_interfaz(f"📅 {msg['fecha_hora']}\n")
                self.mostrar_en_interfaz(f"👤 {msg['remitente']}\n")
                self.mostrar_en_interfaz(f"💬 {msg['contenido']}\n")
                self.mostrar_en_interfaz("─" * 80 + "\n\n")
        else:
            self.mostrar_en_interfaz("⚠️ No hay mensajes en el historial\n\n")

    def ver_sensores(self):
        """Inicia la escucha de sensores"""
        if not self.sensor.escuchando:
            if self.sensor.iniciar_escucha():
                self.mostrar_en_interfaz("\n" + "═" * 80 + "\n")
                self.mostrar_en_interfaz("📡 [ESCUCHANDO DATOS DE SENSORES...]\n")
                self.mostrar_en_interfaz("═" * 80 + "\n")
                self.mostrar_en_interfaz("✅ Conexión establecida con sensores\n")
                self.mostrar_en_interfaz(f"🔗 Broker: {self.sensor.BROKER}:{self.sensor.PORT}\n")
                self.mostrar_en_interfaz(f"📋 Topics: {', '.join(self.sensor.TOPICS)}\n\n")
            else:
                self.mostrar_en_interfaz("❌ Error al conectar con los sensores\n")
        else:
            self.mostrar_en_interfaz("⚠️ Ya estás escuchando sensores\n")

    def detener_sensores(self):
        """Detiene la escucha de sensores"""
        if self.sensor.escuchando:
            if self.sensor.detener_escucha():
                self.mostrar_en_interfaz("\n🛑 [ESCUCHA DE SENSORES DETENIDA]\n")
                self.mostrar_en_interfaz("✅ Desconectado de sensores\n\n")
            else:
                self.mostrar_en_interfaz("❌ Error al detener sensores\n")
        else:
            self.mostrar_en_interfaz("⚠️ No hay escucha activa de sensores\n")

    def historial_sensor(self):
        """Muestra el historial de sensores con formato mejorado"""
        self.mostrar_en_interfaz("\n" + "═" * 80 + "\n")
        self.mostrar_en_interfaz("                    HISTORIAL DE SENSORES\n")
        self.mostrar_en_interfaz("═" * 80 + "\n\n")

        if self.sensor.historial["sen55"]:
            self.mostrar_en_interfaz("📊 SENSOR SEN55\n")
            self.mostrar_en_interfaz("─" * 80 + "\n")
            for i, datos in enumerate(self.sensor.historial["sen55"], 1):
                self.mostrar_en_interfaz(f"[{i:03d}] {json.dumps(datos, indent=2)}\n")
                self.mostrar_en_interfaz("─" * 80 + "\n")
        else:
            self.mostrar_en_interfaz("⚠️ No hay datos del sensor SEN55\n\n")

        if self.sensor.historial["gas_sensor"]:
            self.mostrar_en_interfaz("\n💨 SENSOR DE GAS\n")
            self.mostrar_en_interfaz("─" * 80 + "\n")
            for i, datos in enumerate(self.sensor.historial["gas_sensor"], 1):
                self.mostrar_en_interfaz(f"[{i:03d}] {json.dumps(datos, indent=2)}\n")
                self.mostrar_en_interfaz("─" * 80 + "\n")
        else:
            self.mostrar_en_interfaz("⚠️ No hay datos del sensor de Gas\n\n")

    def crear_mapa(self):
        """Muestra el mapa con las coordenadas recibidas"""
        self.mostrar_en_interfaz("\n" + "═" * 80 + "\n")
        self.mostrar_en_interfaz("🗺️ [ABRIENDO MAPA CON COORDENADAS RECIBIDAS...]\n")
        self.mostrar_en_interfaz("═" * 80 + "\n\n")
        self.mapa.crear_mapa()

    def lanzar_doom(self):
        """Inicia DOOM"""
        self.mostrar_en_interfaz("\n" + "═" * 80 + "\n")
        self.mostrar_en_interfaz("🎮 [LANZANDO DOOM...]\n")
        self.mostrar_en_interfaz("═" * 80 + "\n\n")
        threading.Thread(target=self.doom.correr_doom, daemon=True).start()

    def transmitir_doom(self):
        """Inicia la transmisión de DOOM"""
        self.mostrar_en_interfaz("\n" + "═" * 80 + "\n")
        self.mostrar_en_interfaz("📡 [INICIANDO TRANSMISIÓN DOOM...]\n")
        self.mostrar_en_interfaz("═" * 80 + "\n")
        threading.Thread(target=self.doom.transmitir_ventana, daemon=True).start()
        self.mostrar_en_interfaz("✅ [TRANSMISIÓN DOOM INICIADA]\n\n")

    def info_sistema(self):
        """Muestra información del sistema con formato mejorado"""
        self.mostrar_en_interfaz("\n" + "╔" + "═" * 78 + "╗\n")
        self.mostrar_en_interfaz("║" + " " * 20 + "INFORMACIÓN DEL SISTEMA" + " " * 35 + "║\n")
        self.mostrar_en_interfaz("╚" + "═" * 78 + "╝\n\n")

        info = f"""📱 DISPOSITIVO
   ├─ Nombre largo: {self.dispositivo.long_name}
   ├─ Nombre corto: {self.dispositivo.short_name}
   ├─ ID de nodo: {self.dispositivo.node_name}
   └─ Protocolo: {self.dispositivo.protocolo}

📍 UBICACIÓN
   ├─ Latitud: {self.dispositivo.lat}
   └─ Longitud: {self.dispositivo.lon}

📡 CONEXIÓN MESH
   ├─ Estado: {'✅ Conectado' if self.comunicador.client.is_connected() else '❌ Desconectado'}
   └─ Broker: Configurado

📊 SENSORES
   ├─ Estado: {'✅ Escuchando' if self.sensor.escuchando else '⚠️ Detenidos'}
   ├─ Broker: {self.sensor.BROKER}:{self.sensor.PORT}
   ├─ Datos SEN55: {len(self.sensor.historial["sen55"])} registros
   └─ Datos Gas: {len(self.sensor.historial["gas_sensor"])} registros

📨 MENSAJES
   └─ Total en historial: {len(self.dispositivo.historial_mensajes)}

"""
        self.mostrar_en_interfaz(info)
        self.mostrar_en_interfaz("─" * 80 + "\n\n")

    def confirmar_salida(self):
        """Confirma antes de salir"""
        if messagebox.askyesno("Salir del Sistema", "¿Deseas salir del sistema Mesh Network?"):
            if self.sensor.escuchando:
                self.sensor.detener_escucha()
            self.root.quit()