import customtkinter as ctk
from PIL import Image, ImageTk
import mysql.connector
import cv2
import os
import tkinter as tk

# Global variables for video player
cap = None
video_running = False
current_frame = 0
video_modal = None
video_label = None

def crear_interfaz_actuadores(root):
    global cap, video_running, current_frame, video_modal, video_label
    
    DB_HOST = "127.0.0.1"
    DB_USER = "root"
    DB_PASSWORD = ""
    DB_NAME = "sistema_hidroponico"

    bomba_nombres = ["Bomba 1", "Bomba 2", "Bomba 3", "Bomba 4", "Bomba 5"]
    num_bombas = len(bomba_nombres)
    estados_locales = ["Inactivo"] * num_bombas
    bombas_labels = []
    bomba_animaciones = [None] * num_bombas

    # Cargar imágenes
    bomba_on_img = ctk.CTkImage(light_image=Image.open(r"C:\Users\Colibecas\Escritorio\PI\src\ui\views\test_images\bomba_off.png"),
                                dark_image=Image.open(r"C:\Users\Colibecas\Escritorio\PI\src\ui\views\test_images\bomba_off.png"),
                                size=(100, 100))
    bomba_off_img = ctk.CTkImage(light_image=Image.open(r"C:\Users\Colibecas\Escritorio\PI\src\ui\views\test_images\bomba_on.png"),
                                 dark_image=Image.open(r"C:\Users\Colibecas\Escritorio\PI\src\ui\views\test_images\bomba_on.png"),
                                 size=(100, 100))

    def mostrar_ayuda_actuadores():
        """Muestra el video de ayuda para el módulo de actuadores"""
        global cap, video_running, current_frame, video_modal, video_label
        
        video_path = os.path.join("C:\\", "Users", "Colibecas", "Escritorio", "PI", "src", "ui", "views", "test_images", "Actuadores.mp4")
        
        if not os.path.exists(video_path):
            tk.messagebox.showerror("Error", f"El archivo de ayuda no se encontró en:\n{video_path}")
            return
        
        # Crear ventana modal
        video_modal = ctk.CTkToplevel(root)
        video_modal.title("Ayuda - Manejo de Actuadores")
        video_modal.geometry("800x600")
        video_modal.resizable(True, True)
        video_modal.grab_set()
        
        # Centrar el modal
        window_width = 800
        window_height = 600
        screen_width = video_modal.winfo_screenwidth()
        screen_height = video_modal.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        video_modal.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        
        # Frame principal
        main_frame = ctk.CTkFrame(video_modal, fg_color="white")
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
            command=play_video,
            width=100
        )
        btn_play.pack(side="left", padx=5)
        
        btn_pause = ctk.CTkButton(
            controls_frame,
            text="⏸ Pausar",
            command=pause_video,
            width=100
        )
        btn_pause.pack(side="left", padx=5)
        
        btn_stop = ctk.CTkButton(
            controls_frame,
            text="⏹ Detener",
            command=stop_video,
            width=100
        )
        btn_stop.pack(side="left", padx=5)
        
        # Inicializar video
        cap = cv2.VideoCapture(video_path)
        stop_video()
        
        # Configurar cierre
        video_modal.protocol("WM_DELETE_WINDOW", on_video_closing)

    def play_video():
        global video_running, cap
        if cap is None:
            return
        
        video_running = True
        update_video()

    def pause_video():
        global video_running
        video_running = False

    def stop_video():
        global video_running, current_frame
        video_running = False
        current_frame = 0
        if cap is not None:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = cap.read()
            if ret:
                show_frame(frame)

    def update_video():
        global current_frame, video_running, cap
        
        if video_running and cap is not None:
            ret, frame = cap.read()
            current_frame += 1
            
            if ret:
                show_frame(frame)
                video_modal.after(30, update_video)
            else:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                current_frame = 0
                video_modal.after(30, update_video)

    def show_frame(frame):
        global video_label
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        
        max_width = video_label.winfo_width() - 20
        max_height = video_label.winfo_height() - 20
        
        if max_width <= 0 or max_height <= 0:
            return
            
        ratio = min(max_width/img.width, max_height/img.height)
        new_size = (int(img.width*ratio), int(img.height*ratio))
        img = img.resize(new_size, Image.LANCZOS)
        
        imgtk = ImageTk.PhotoImage(image=img)
        video_label.configure(image=imgtk)
        video_label.image = imgtk

    def on_video_closing():
        global cap, video_modal
        if cap is not None:
            cap.release()
            cap = None
        video_modal.destroy()
        video_modal = None

    def obtener_estados():
        try:
            db = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME
            )
            cursor = db.cursor()
            cursor.execute(f"SELECT estado FROM actuadores ORDER BY id_actuador ASC LIMIT {num_bombas}")
            estados = [fila[0] for fila in cursor.fetchall()]
            cursor.close()
            db.close()
            return estados
        except mysql.connector.Error as err:
            print(f"Error de conexión a la base de datos: {err}")
            return ["Inactivo"] * num_bombas

    def actualizar_visual(indice):
        estado = estados_locales[indice]
        color = "#2ECC71" if estado == "Inactivo" else "#E74C3C"
        boton_text = "Apagar ⛔" if estado == "Inactivo" else "Encender 💡"
        boton_color = "#E74C3C" if estado == "Inactivo" else "#3498DB"
        hover_color = "#C0392B" if estado == "Inactivo" else "#2980B9"

        indicadores[indice].configure(
            fg_color=color,
            border_color="white" if estado == "Activo" else "#ccc",
            border_width=3
        )
        botones[indice].configure(
            text=boton_text,
            fg_color=boton_color,
            hover_color=hover_color
        )

        if estado == "Activo":
            if bomba_animaciones[indice] is None:
                animar_bomba(indice)
        else:
            if bomba_animaciones[indice] is not None:
                root.after_cancel(bomba_animaciones[indice])
                bomba_animaciones[indice] = None
            bombas_labels[indice].configure(image=bomba_off_img)

    def cambiar_estado(indice):
        estado_actual = estados_locales[indice]
        nuevo_estado = "Inactivo" if estado_actual == "Activo" else "Activo"
        estados_locales[indice] = nuevo_estado
        actualizar_visual(indice)

        try:
            db = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME
            )
            cursor = db.cursor()
            cursor.execute("UPDATE actuadores SET estado = %s WHERE id_actuador = %s", (nuevo_estado, indice + 1))
            db.commit()
            cursor.close()
            db.close()
        except mysql.connector.Error as err:
            print(f"Error al actualizar el estado: {err}")

    def animar_bomba(indice):
        estados_icono = [bomba_on_img] * 4
        def ciclo(frame_index=0):
            if estados_locales[indice] != "Activo":
                bombas_labels[indice].configure(image=bomba_off_img)
                return
            bombas_labels[indice].configure(image=estados_icono[frame_index])
            anim_id = root.after(300, lambda: ciclo((frame_index + 1) % len(estados_icono)))
            bomba_animaciones[indice] = anim_id
        ciclo()

    # INTERFAZ PRINCIPAL
    root.configure(fg_color="#F4F6F7")
    root.grid_rowconfigure((0, 1, 2, 3), weight=1)
    root.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

    # Frame para el título y botones de ayuda/notificaciones
    header_frame = ctk.CTkFrame(root, fg_color="transparent")
    header_frame.grid(row=0, column=0, columnspan=5, padx=10, pady=(30, 10), sticky="nsew")
    header_frame.grid_columnconfigure(0, weight=1)
    
    # Título centrado
    titulo = ctk.CTkLabel(
        header_frame,
        text="🌱 CONTROL DE ACTUADORES 🌿",
        font=("Segoe UI", 34, "bold"),
        text_color="#1A5276"
    )
    titulo.grid(row=0, column=0, padx=10, pady=10)

    # Frame para botones de ayuda y notificaciones (a la derecha)
    buttons_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
    buttons_frame.grid(row=0, column=1, sticky="e")

    # Botón de ayuda
    btn_ayuda = ctk.CTkButton(
        buttons_frame,
        text="?",
        width=30,
        height=30,
        font=("Arial", 14, "bold"),
        fg_color="#3498db",
        hover_color="#2980b9",
        command=mostrar_ayuda_actuadores
    )
    btn_ayuda.pack(side="left", padx=5)

    # Botón de notificaciones
    btn_notificaciones = ctk.CTkButton(
        buttons_frame,
        text="🔔",
        width=30,
        height=30,
        font=("Arial", 14),
        fg_color="transparent",
        hover_color="#f0f0f0",
        command=lambda: print("Mostrar notificaciones")
    )
    btn_notificaciones.pack(side="left", padx=5)

    global indicadores, botones
    indicadores = []
    botones = []

    # Posiciones relativas para cada bomba
    posiciones = [
        (0.18, 0.36),  # Bomba 1
        (0.5, 0.36),    # Bomba 2
        (0.83, 0.36),   # Bomba 3
        (0.335, 0.77),  # Bomba 4
        (0.665, 0.77)   # Bomba 5
    ]

    for i in range(num_bombas):
        frame = ctk.CTkFrame(
            root,
            width=360,
            height=280,
            fg_color="#FDFEFE",
            corner_radius=25,
            border_width=1,
            border_color="#BDC3C7"
        )
        frame.place(relx=posiciones[i][0], rely=posiciones[i][1], anchor="center")
        frame.pack_propagate(False)

        nombre_label = ctk.CTkLabel(
            frame, text=bomba_nombres[i], font=("Segoe UI", 24, "bold"), text_color="#154360"
        )
        nombre_label.pack(pady=(20, 12))

        # Indicador de estado
        indicador = ctk.CTkFrame(
            frame,
            width=50,
            height=50,
            fg_color="#E74C3C",
            corner_radius=25,
            border_width=3,
            border_color="#ABB2B9"
        )
        indicador.pack(pady=(0, 15))
        indicadores.append(indicador)

        # Botón de encendido
        boton = ctk.CTkButton(
            frame,
            text="Cargando...",
            command=lambda i=i: cambiar_estado(i),
            fg_color="#3498DB",
            hover_color="#2980B9",
            font=("Segoe UI", 17, "bold"),
            text_color="white",
            corner_radius=10,
            width=200,
            height=50
        )
        boton.pack(pady=(0, 10))
        botones.append(boton)

        # Imagen de bomba
        bomba_label = ctk.CTkLabel(frame, image=bomba_off_img, text="")
        bomba_label.pack(pady=(10, 5))
        bombas_labels.append(bomba_label)

    # Cargar estados iniciales
    estados_db = obtener_estados()
    for i in range(min(num_bombas, len(estados_db))):
        estados_locales[i] = estados_db[i]
        actualizar_visual(i)

# Ventana principal
if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
    app = ctk.CTk()
    app.title("Sistema Hidropónico - Actuadores")
    app.geometry("1080x800")
    crear_interfaz_actuadores(app)
    app.mainloop()