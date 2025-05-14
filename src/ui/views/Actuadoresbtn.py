import customtkinter as ctk
from PIL import Image
import mysql.connector

def crear_interfaz_actuadores(root):
    DB_HOST = "127.0.0.1"
    DB_USER = "root"
    DB_PASSWORD = ""
    DB_NAME = "sistema_hidroponico"

    bomba_nombres = ["Bomba 1", "Bomba 2", "Bomba 3", "Bomba 4"]
    estados_locales = ["Inactivo"] * 4
    bombas_labels = []
    bomba_animaciones = [None] * 4

    # Cargar imágenes
    bomba_on_img = ctk.CTkImage(light_image=Image.open(r"C:\Users\Colibecas\Desktop\PI\src\ui\views\test_images\bomba_on.png"),
                                dark_image=Image.open(r"C:\Users\Colibecas\Desktop\PI\src\ui\views\test_images\bomba_on.png"),
                                size=(100, 100))  # Ajusta el tamaño de la imagen según sea necesario
    bomba_off_img = ctk.CTkImage(light_image=Image.open(r"C:\Users\Colibecas\Desktop\PI\src\ui\views\test_images\bomba_off.png"),
                                 dark_image=Image.open(r"C:\Users\Colibecas\Desktop\PI\src\ui\views\test_images\bomba_off.png"),
                                 size=(100, 100))  # Cambia esta ruta si la imagen para el estado apagado es diferente

    def obtener_estados():
        try:
            db = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME
            )
            cursor = db.cursor()
            cursor.execute("SELECT estado FROM actuadores ORDER BY id_actuador ASC LIMIT 4")
            estados = [fila[0] for fila in cursor.fetchall()]
            cursor.close()
            db.close()
            return estados
        except mysql.connector.Error as err:
            print(f"Error de conexión a la base de datos: {err}")
            return ["Inactivo"] * 4

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

        # Usar imágenes en lugar de texto
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
        estados_icono = [bomba_on_img, bomba_on_img, bomba_on_img, bomba_on_img]
        colores = ["#1ABC9C", "#48C9B0", "#17A589", "#148F77"]

        def ciclo(frame_index=0):
            if estados_locales[indice] != "Activo":
                bombas_labels[indice].configure(image=bomba_off_img)  # Apagado
                return
            bombas_labels[indice].configure(image=estados_icono[frame_index])  # Activado
            anim_id = root.after(300, lambda: ciclo((frame_index + 1) % len(estados_icono)))
            bomba_animaciones[indice] = anim_id

        ciclo()

    # INTERFAZ PRINCIPAL
    root.configure(fg_color="#F4F6F7")
    root.grid_rowconfigure((0, 1, 2), weight=1)
    root.grid_columnconfigure((0, 1), weight=1)

    titulo = ctk.CTkLabel(
        root,
        text="🌱 CONTROL DE ACTUADORES 🌿",
        font=("Segoe UI", 34, "bold"),
        text_color="#1A5276"
    )
    titulo.grid(row=0, column=0, columnspan=2, pady=(30, 10))

    global indicadores, botones
    indicadores = []
    botones = []

    for i in range(4):
        frame = ctk.CTkFrame(
            root,
            width=360,
            height=280,
            fg_color="#FDFEFE",
            corner_radius=25,
            border_width=1,
            border_color="#BDC3C7"
        )
        frame.grid(row=(i // 2) + 1, column=i % 2, padx=25, pady=25, sticky="nsew")

        nombre_label = ctk.CTkLabel(
            frame,
            text=bomba_nombres[i],
            font=("Segoe UI", 24, "bold"),
            text_color="#154360"
        )
        nombre_label.pack(pady=(20, 12))

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

        # Bomba de agua (animación)
        bomba_label = ctk.CTkLabel(frame, image=bomba_off_img, text="")  # Eliminar texto por defecto
        bomba_label.pack(pady=(10, 5))
        bombas_labels.append(bomba_label)

    # Cargar estados iniciales
    estados_db = obtener_estados()
    for i in range(4):
        estados_locales[i] = estados_db[i]
        actualizar_visual(i)

# Ventana principal
if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
    app = ctk.CTk()
    app.title("Sistema Hidropónico - Actuadores")
    app.geometry("820x740")
    crear_interfaz_actuadores(app)
    app.mainloop()