import sys
import os
import customtkinter as ctk
from tkinter import ttk
from datetime import datetime
import threading
import cv2
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from src.models.models import (
    obtener_alertas,
    actualizar_trigger,
    actualizar_alerta,
    obtener_alertas_completas
)

COLORES = {
    'pH': '#B0E0E6',            # Sensor ID 1
    'Profundidad': '#FFA07A',   # Sensor ID 2 
    'Temperatura': '#98FB98',   # Sensor ID 3
    'Conductividad': '#FFFACD',  # Sensor ID 4
    'border': '#4682B4',
    'header_bg': '#4F94CD',
    'row_selected': '#B0E0E6'
}

SENSOR_NAMES = {
    1: 'pH',
    2: 'Profundidad',
    3: 'Temperatura',
    4: 'Conductividad'
}

class AlertasApp:
    def __init__(self, frame_principal):
        self.frame = frame_principal
        self.alertas = []
        self.inicializar_ui()
        self.iniciar_actualizaciones_periodicas()
        
         # Añadir botón de ayuda en el frame principal
        self.agregar_boton_ayuda()

    def agregar_boton_ayuda(self):
        # Frame para contener los botones de ayuda y notificaciones
        botones_frame = ctk.CTkFrame(self.frame_titulo, fg_color="transparent")
        botones_frame.pack(side="right", padx=10)
        
        # Botón de ayuda
        btn_ayuda = ctk.CTkButton(
            botones_frame,
            text="?",
            width=30,
            height=30,
            font=("Arial", 14, "bold"),
            fg_color="#3498db",
            hover_color="#2980b9",
            command=self.mostrar_ayuda_alertas
        )
        btn_ayuda.pack(side="left", padx=5)

    def mostrar_ayuda_alertas(self):
        """Muestra el video de ayuda para el módulo de alertas"""
        # Construir la ruta absoluta al video
        video_path = os.path.join("C:\\", "Users", "Colibecas", "Escritorio", "PI", "src", "ui", "views", "test_images", "Alertas.mp4")
        
        # Verificar si el archivo existe
        if not os.path.exists(video_path):
            tk.messagebox.showerror("Error", f"El archivo de ayuda no se encontró en:\n{video_path}")
            return
        
        # Crear ventana modal
        modal = ctk.CTkToplevel(self.frame)
        modal.title("Ayuda - Manejo de Alertas")
        modal.geometry("800x600")
        modal.resizable(True, True)
        modal.grab_set()  # Hace que sea modal
        
        # Centrar el modal en la pantalla
        window_width = 800
        window_height = 600
        screen_width = modal.winfo_screenwidth()
        screen_height = modal.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        modal.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        
        # Frame principal del modal
        main_frame = ctk.CTkFrame(modal, fg_color="white")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Etiqueta para el video
        video_label = ctk.CTkLabel(main_frame, text="")
        video_label.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Botones de control
        controls_frame = ctk.CTkFrame(main_frame, fg_color="white")
        controls_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        btn_play = ctk.CTkButton(
            controls_frame,
            text="▶ Reproducir",
            command=lambda: self.play_video(),
            width=100
        )
        btn_play.pack(side="left", padx=5)
        
        btn_pause = ctk.CTkButton(
            controls_frame,
            text="⏸ Pausar",
            command=lambda: self.pause_video(),
            width=100
        )
        btn_pause.pack(side="left", padx=5)
        
        btn_stop = ctk.CTkButton(
            controls_frame,
            text="⏹ Detener",
            command=lambda: self.stop_video(),
            width=100
        )
        btn_stop.pack(side="left", padx=5)
        
        # Variables de control del video
        self.cap = None
        self.video_running = False
        self.current_frame = 0
        self.video_path = video_path
        self.video_modal = modal
        self.video_label = video_label
        
        # Mostrar el primer frame
        self.stop_video()
        
        # Configurar el cierre del modal
        modal.protocol("WM_DELETE_WINDOW", self.on_video_closing)

    def play_video(self):
        if self.cap is None:
            self.cap = cv2.VideoCapture(self.video_path)
            self.current_frame = 0
        
        self.video_running = True
        self.update_video()

    def pause_video(self):
        self.video_running = False

    def stop_video(self):
        self.video_running = False
        self.current_frame = 0
        if self.cap is not None:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = self.cap.read()
            if ret:
                self.show_frame(frame)

    def update_video(self):
        if self.video_running and self.cap is not None:
            ret, frame = self.cap.read()
            self.current_frame += 1
            
            if ret:
                self.show_frame(frame)
                self.video_modal.after(30, self.update_video)
            else:
                # Si llegamos al final, reiniciamos
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                self.current_frame = 0
                self.video_modal.after(30, self.update_video)

    def show_frame(self, frame):
        # Convertir el frame de OpenCV a formato compatible con tkinter
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        
        # Redimensionar manteniendo el aspect ratio
        max_width = self.video_label.winfo_width() - 20
        max_height = self.video_label.winfo_height() - 20
        
        if max_width <= 0 or max_height <= 0:
            return
            
        ratio = min(max_width/img.width, max_height/img.height)
        new_size = (int(img.width*ratio), int(img.height*ratio))
        img = img.resize(new_size, Image.LANCZOS)
        
        imgtk = ImageTk.PhotoImage(image=img)
        self.video_label.configure(image=imgtk)
        self.video_label.image = imgtk  # Mantener referencia

    def on_video_closing(self):
        if self.cap is not None:
            self.cap.release()
            self.cap = None
        self.video_modal.destroy()

    def inicializar_ui(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        self.configurar_estructura_principal()
        self.alertas = obtener_alertas_completas()
        self.actualizar_recuadros_alertas()
        self.crear_tabla_historial()

    def configurar_estructura_principal(self):
        self.frame_titulo = ctk.CTkFrame(self.frame, fg_color="#E3F2FD")
        self.frame_titulo.pack(pady=(20, 10), fill="x")
        self.label_titulo = ctk.CTkLabel(
            self.frame_titulo, 
            text="🚨 Alertas 🚨", 
            font=('Arial', 20, 'bold'), 
            text_color=self.obtener_color_texto()
        )
        self.label_titulo.pack()

        self.frame_alertas = ctk.CTkFrame(self.frame, fg_color="transparent")
        self.frame_alertas.pack(pady=10, fill="x", padx=20)
        
        for i in range(4):
            self.frame_alertas.grid_columnconfigure(i, weight=1)

        self.frame_modal = ctk.CTkFrame(
            self.frame, 
            width=300, 
            height=150, 
            corner_radius=10, 
            fg_color='gray'
        )
        self.label_modal = ctk.CTkLabel(
            self.frame_modal, 
            text="Resolviendo...", 
            font=('Arial', 14)
        )
        self.label_modal.pack(padx=10, pady=40)

    def crear_tabla_historial(self):
        self.frame_tabla = ctk.CTkFrame(self.frame, fg_color="transparent")
        self.frame_tabla.pack(pady=(10, 20), padx=20, fill="both", expand=True)
        
        self.frame_filtros = ctk.CTkFrame(self.frame_tabla, fg_color="transparent")
        self.frame_filtros.pack(fill="x", pady=(0, 10))
        
        self.frame_centro_filtros = ctk.CTkFrame(self.frame_filtros, fg_color="transparent")
        self.frame_centro_filtros.pack(expand=True)
        
        self.btn_todos = ctk.CTkButton(
            self.frame_centro_filtros, 
            text="Todas",
            command=lambda: self.actualizar_filtro(None),
            width=100,
            fg_color="#4F94CD"
        )
        self.btn_todos.pack(side="left", padx=5)
        
        self.btn_resueltas = ctk.CTkButton(
            self.frame_centro_filtros, 
            text="Resueltas",
            command=lambda: self.actualizar_filtro("Resuelta"),
            width=100,
            fg_color="#4CAF50"
        )
        self.btn_resueltas.pack(side="left", padx=5)
        
        self.btn_descartadas = ctk.CTkButton(
            self.frame_centro_filtros, 
            text="Descartadas",
            command=lambda: self.actualizar_filtro("Descartada"),
            width=100,
            fg_color="#F44336"
        )
        self.btn_descartadas.pack(side="left", padx=5)
        
        self.btn_revision = ctk.CTkButton(
            self.frame_centro_filtros, 
            text="En revisión",
            command=lambda: self.actualizar_filtro("En revision"),
            width=100,
            fg_color="#FFC107",
            text_color="black"
        )
        self.btn_revision.pack(side="left", padx=5)
        
        self.frame_encabezados = ctk.CTkFrame(
            self.frame_tabla, 
            fg_color=COLORES['header_bg']
        )
        self.frame_encabezados.pack(fill="x", pady=(0, 5))
        
        encabezados = ['🔍 ID', '⚠️ Tipo', '📜 Descripción', '📅 Fecha', '🟢 Estado', '⚙️ Acciones']
        for i, texto in enumerate(encabezados):
            label = ctk.CTkLabel(
                self.frame_encabezados,
                text=texto,
                font=('Arial', 14, 'bold'),
                text_color="white"
            )
            label.grid(row=0, column=i, padx=5, pady=5, sticky="nsew")
            self.frame_encabezados.grid_columnconfigure(i, weight=1)
        
        self.frame_scroll = ctk.CTkScrollableFrame(
            self.frame_tabla, 
            fg_color="transparent"
        )
        self.frame_scroll.pack(fill="both", expand=True)
        
        for i in range(6):
            self.frame_scroll.grid_columnconfigure(i, weight=1)

        self.filtro_actual = None
        self.actualizar_filas()

    def actualizar_filtro(self, estado):
        self.filtro_actual = estado
        self.actualizar_filas()

    def actualizar_filas(self):
        for widget in self.frame_scroll.winfo_children():
            widget.destroy()
        
        alertas_filtradas = self.alertas if self.filtro_actual is None else [
            a for a in self.alertas if a.get('estado', '').lower() == self.filtro_actual.lower()
        ]
        
        for i, alerta in enumerate(alertas_filtradas):
            self.crear_fila_alerta(alerta, i)

    def crear_fila_alerta(self, alerta, index):
        sensor_id = None
        descripcion = alerta.get('descripcion', '')
        
        if 'Valor del sensor' in descripcion:
            try:
                sensor_id = int(descripcion.split('Valor del sensor ')[1].split(' ')[0])
            except (IndexError, ValueError):
                pass
        
        if sensor_id in SENSOR_NAMES:
            color = COLORES[SENSOR_NAMES[sensor_id]]
        else:
            color = COLORES[list(COLORES.keys())[index % 4]]
        
        frame_fila = ctk.CTkFrame(self.frame_scroll, fg_color=color)
        frame_fila.pack(fill="x", pady=2)
        frame_fila.alerta_id = alerta.get('id_alerta', '')
        
        for col in range(6):
            frame_fila.grid_columnconfigure(col, weight=1)
        
        datos = [
            str(alerta.get('id_alerta', '')),
            alerta.get('tipo_alerta', ''),
            descripcion,
            alerta.get('fecha_hora', '').strftime('%Y-%m-%d %H:%M:%S') if isinstance(alerta.get('fecha_hora'), datetime) else str(alerta.get('fecha_hora', '')),
            alerta.get('estado', 'Por atender').capitalize()
        ]
        
        for col, valor in enumerate(datos):
            label = ctk.CTkLabel(
                frame_fila,
                text=valor,
                font=('Arial', 12),
                text_color="black"
            )
            label.grid(row=0, column=col, padx=5, pady=5, sticky="nsew")
        
        # Frame para botones (como atributo accesible)
        frame_fila.frame_botones = ctk.CTkFrame(frame_fila, fg_color="transparent")
        frame_fila.frame_botones.grid(row=0, column=5, padx=5, pady=5, sticky="nsew")
        
        estado = alerta.get('estado', '').lower()
        if estado in ('por atender', 'en revision'):
            btn_resolver = ctk.CTkButton(
                frame_fila.frame_botones,
                text="✔️ Resolver",
                width=80,
                height=30,
                command=lambda id=alerta['id_alerta']: self.resolver_alerta(id),
                fg_color="#4CAF50",
                font=('Arial', 10)
            )
            btn_resolver.pack(side="left", padx=2)
            
            btn_descartar = ctk.CTkButton(
                frame_fila.frame_botones,
                text="❌ Descartar",
                width=80,
                height=30,
                command=lambda id=alerta['id_alerta']: self.descartar_alerta(id),
                fg_color="gray",
                font=('Arial', 10)
            )
            btn_descartar.pack(side="left", padx=2)
            
            if sensor_id is not None:
                btn_editar = ctk.CTkButton(
                    frame_fila.frame_botones,
                    text="✏️ Editar",
                    width=80,
                    height=30,
                    command=lambda id=sensor_id, tipo=SENSOR_NAMES.get(sensor_id, 'Sensor'): self.editar_alerta_callback(tipo, id),
                    fg_color="#1976D2",
                    font=('Arial', 10)
                )
                btn_editar.pack(side="left", padx=2)
        else:
            # Si la alerta no requiere botones, eliminamos el frame
            frame_fila.frame_botones.destroy()

    def actualizar_recuadros_alertas(self):
        contador_alertas = {
            'pH': 0,
            'Profundidad': 0,
            'Temperatura': 0,
            'Conductividad': 0
        }
        
        for alerta in self.alertas:
            id_sensor = alerta.get('id_sensor')
            
            if id_sensor in SENSOR_NAMES:
                contador_alertas[SENSOR_NAMES[id_sensor]] += 1
            else:
                descripcion = alerta.get('descripcion', '')
                if 'pH' in descripcion:
                    contador_alertas['pH'] += 1
                elif 'Profundidad' in descripcion:
                    contador_alertas['Profundidad'] += 1
                elif 'Temperatura' in descripcion:
                    contador_alertas['Temperatura'] += 1
                elif 'Conductividad' in descripcion:
                    contador_alertas['Conductividad'] += 1
        
        for widget in self.frame_alertas.winfo_children():
            widget.destroy()
        
        recuadros = [
            ('pH', COLORES['pH'], f"⚠️ Alertas de pH\n{contador_alertas['pH']} alertas"),
            ('Profundidad', COLORES['Profundidad'], f"📏 Alertas de Profundidad\n{contador_alertas['Profundidad']} alertas"),
            ('Temperatura', COLORES['Temperatura'], f"🌡️ Alertas de Temp.\n{contador_alertas['Temperatura']} alertas"),
            ('Conductividad', COLORES['Conductividad'], f"⚡ Alertas de Condu.\n{contador_alertas['Conductividad']} alertas")
        ]
        
        for i, (nombre, color, texto) in enumerate(recuadros):
            recuadro = ctk.CTkFrame(
                self.frame_alertas, 
                width=200, 
                height=100, 
                corner_radius=10, 
                fg_color=color, 
                border_width=2, 
                border_color="black"
            )
            recuadro.grid(row=0, column=i, padx=10, pady=5, sticky="nsew")
            
            label = ctk.CTkLabel(
                recuadro, 
                text=texto, 
                font=('Arial', 14, 'bold'), 
                text_color="black",
                wraplength=180
            )
            label.pack(padx=10, pady=10, expand=True)

    def resolver_alerta(self, id_alerta):
        for alerta in self.alertas:
            if alerta['id_alerta'] == id_alerta:
                alerta['estado'] = 'Resuelta'
                break
        
        self.ocultar_botones_fila(id_alerta)
        
        tipo = next((a['tipo_alerta'] for a in self.alertas if a['id_alerta'] == id_alerta), "Alerta")
        actualizar_alerta(id_alerta, 'Resuelta')
        self.mostrar_modal(tipo, "resuelta")
        self.actualizar_datos()

    def descartar_alerta(self, id_alerta):
        for alerta in self.alertas:
            if alerta['id_alerta'] == id_alerta:
                alerta['estado'] = 'Descartada'
                break
        
        self.ocultar_botones_fila(id_alerta)
        
        tipo = next((a['tipo_alerta'] for a in self.alertas if a['id_alerta'] == id_alerta), "Alerta")
        actualizar_alerta(id_alerta, 'Descartada')
        self.mostrar_modal(tipo, "descartada")
        self.actualizar_datos()

    def ocultar_botones_fila(self, id_alerta):
        for child in self.frame_scroll.winfo_children():
            if hasattr(child, 'alerta_id') and child.alerta_id == id_alerta:
                if hasattr(child, 'frame_botones'):
                    child.frame_botones.destroy()
                break

    def editar_alerta_callback(self, tipo_alerta, id_sensor=None):
        self.editar_alerta(tipo_alerta, id_sensor)

    def editar_alerta(self, tipo_alerta, id_sensor=None):
        formulario_modal = ctk.CTkFrame(
            self.frame, 
            width=400, 
            height=300, 
            corner_radius=10, 
            fg_color="lightgray"
        )
        formulario_modal.place(relx=0.5, rely=0.5, anchor="center")

        label_titulo_formulario = ctk.CTkLabel(
            formulario_modal, 
            text=f"Editar alerta de {tipo_alerta}", 
            font=('Arial', 14, 'bold')
        )
        label_titulo_formulario.pack(pady=10)

        label_valor_max = ctk.CTkLabel(
            formulario_modal, 
            text="Valor máximo:", 
            font=('Arial', 12)
        )
        label_valor_max.pack(pady=5)

        entry_valor_max = ctk.CTkEntry(formulario_modal, font=('Arial', 12))
        entry_valor_max.pack(pady=5)

        label_valor_min = ctk.CTkLabel(
            formulario_modal, 
            text="Valor mínimo:", 
            font=('Arial', 12)
        )
        label_valor_min.pack(pady=5)

        entry_valor_min = ctk.CTkEntry(formulario_modal, font=('Arial', 12))
        entry_valor_min.pack(pady=5)
        
        def enviar_edicion():
            try:
                valor_min = float(entry_valor_min.get())
                valor_max = float(entry_valor_max.get())

                if valor_min is not None and valor_max is not None:
                    if id_sensor:
                        actualizar_trigger(id_sensor, valor_min, valor_max)
                    print(f"Trigger de {tipo_alerta} actualizado con valor mínimo: {valor_min}, valor máximo: {valor_max}")
                    formulario_modal.place_forget()
                    self.actualizar_datos()
                else:
                    print("Por favor ingrese valores válidos.")
            except ValueError:
                print("Error: Ingrese valores numéricos válidos.")

        boton_enviar = ctk.CTkButton(
            formulario_modal, 
            text="✔️ Enviar", 
            command=enviar_edicion, 
            width=230, 
            corner_radius=5, 
            fg_color="green"
        )
        boton_enviar.pack(pady=10)
        
        boton_cerrar = ctk.CTkButton(
            formulario_modal, 
            text="❌ Cerrar", 
            command=formulario_modal.place_forget, 
            width=230, 
            corner_radius=5, 
            fg_color="red"
        )
        boton_cerrar.pack(pady=5)

    def mostrar_modal(self, tipo_alerta, estado_alerta):
        self.frame_modal.place(relx=0.5, rely=0.5, anchor="center")
        self.label_modal.configure(text=f"Resolviendo alerta de {tipo_alerta}...")
        self.frame_modal.update()
        self.frame_modal.after(2000, lambda: self.actualizar_modal(tipo_alerta, estado_alerta))

    def actualizar_modal(self, tipo_alerta, estado_alerta):
        self.label_modal.configure(text=f"¡Alerta de {tipo_alerta} {estado_alerta}! ✅")
        self.frame_modal.after(1500, self.frame_modal.place_forget)

    def obtener_color_texto(self):
        return "white" if ctk.get_appearance_mode() == "dark" else "black"

    def actualizar_datos(self):
        self.alertas = obtener_alertas_completas()
        self.actualizar_recuadros_alertas()
        self.actualizar_filas()

    def iniciar_actualizaciones_periodicas(self, intervalo=30):
        def actualizar_periodicamente():
            try:
                self.actualizar_datos()
            finally:
                self.frame.after(intervalo*1000, actualizar_periodicamente)
        
        self.frame.after(intervalo*1000, actualizar_periodicamente)

def iniciar_alertas(frame):
    app = AlertasApp(frame)
    return app