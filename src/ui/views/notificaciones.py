import customtkinter as ctk
from datetime import datetime
from PIL import Image


class Notificador:
    def __init__(self, parent_frame):
        self.parent = parent_frame
        self.nuevas_alertas = []
        self.panel_visible = False

        # Imagen de campanita reducida
        self.img_campana = ctk.CTkImage(
            light_image=Image.open(r"C:\Users\Colibecas\Desktop\PI\src\ui\views\test_images\campana.png"),
            size=(22, 22)
        )

        # Botón rectangular con campanita
        self.btn_campana = ctk.CTkButton(
            self.parent,
            image=self.img_campana,
            text="",
            width=40,
            height=30,
            fg_color="#FFDB6F",
            hover_color="#FFCA28",
            corner_radius=5,
            border_width=0,
            command=self.toggle_panel
        )

        # Posicionar en la esquina superior derecha
        self.btn_campana.place(relx=1.0, rely=0.0, anchor="ne", x=-30, y=30)

        # Panel de notificaciones
        self.panel = ctk.CTkFrame(
            self.parent,
            width=350,
            height=250,
            corner_radius=15,
            fg_color="#FFFFFF",
            border_width=1,
            border_color="#BDBDBD"
        )

        # Contenido scrollable dentro del panel
        self.contenido_panel = ctk.CTkScrollableFrame(self.panel, fg_color="transparent")
        self.contenido_panel.pack(fill="both", expand=True, padx=10, pady=10)

    def toggle_panel(self):
        if self.panel_visible:
            self.panel.place_forget()
            self.panel_visible = False
        else:
            self.actualizar_panel()
            self.panel.place(relx=1.0, rely=0.0, anchor="ne", x=-90, y=80)
            self.panel_visible = True

        # Restaurar color normal al abrir/cerrar el panel
        self.btn_campana.configure(fg_color="#FFDB6F")
        self.nuevas_alertas.clear()

    def recibir_alerta(self, mensaje):
        ahora = datetime.now().strftime("%H:%M:%S")
        self.nuevas_alertas.append((mensaje, ahora))
        # Cambiar color del botón a rojo cuando hay alerta
        self.btn_campana.configure(fg_color="#D32F2F")
        self.actualizar_panel()

    def actualizar_panel(self):
        # Limpiar notificaciones previas
        for widget in self.contenido_panel.winfo_children():
            widget.destroy()

        if not self.nuevas_alertas:
            mensaje = ctk.CTkLabel(
                self.contenido_panel,
                text="Sin nuevas notificaciones",
                font=("Arial", 13, "italic"),
                text_color="#757575"
            )
            mensaje.pack(pady=5)
        else:
            for hora, msg in reversed(self.nuevas_alertas):
                item = ctk.CTkFrame(self.contenido_panel, fg_color="#F5F5F5", corner_radius=10)
                item.pack(fill="x", pady=5, padx=2)

                texto = ctk.CTkLabel(
                    item,
                    text=f"{hora} {msg}",
                    font=("Arial", 13),
                    text_color="#212121",
                    anchor="w",
                    justify="left",
                    wraplength=300
                )
                texto.pack(fill="both", padx=10, pady=6)