import customtkinter as ctk
from datetime import datetime

class Notificador:
    def __init__(self, parent_frame):
        self.parent = parent_frame
        self.nuevas_alertas = []
        self.panel_visible = False

        # Contenedor superior derecho
        self.frame_superior = ctk.CTkFrame(self.parent, fg_color="transparent")
        self.frame_superior.place(relx=1.0, rely=0.0, anchor="ne", x=-20, y=20)

        # Botón de campanita con diseño moderno
        self.btn_campana = ctk.CTkButton(
            self.frame_superior,
            text="🔔",
            width=45,
            height=45,
            fg_color="#E0E0E0",
            hover_color="#D32F2F",
            corner_radius=100,
            font=('Arial', 20, 'bold'),
            text_color="black",
            border_width=0,
            command=self.toggle_panel
        )
        self.btn_campana.pack()

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
            self.btn_campana.configure(fg_color="#E0E0E0")
            self.nuevas_alertas.clear()

    def recibir_alerta(self, mensaje):
        ahora = datetime.now().strftime("%H:%M:%S")
        self.nuevas_alertas.append((mensaje, ahora))
        self.btn_campana.configure(fg_color="#D32F2F")  # rojo fuerte
        self.actualizar_panel()

    def actualizar_panel(self):
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
            for msg, hora in reversed(self.nuevas_alertas):
                item = ctk.CTkFrame(self.contenido_panel, fg_color="#F5F5F5", corner_radius=10)
                item.pack(fill="x", pady=5, padx=2)

                texto = ctk.CTkLabel(
                    item,
                    text=f"[{hora}] {msg}",
                    font=("Arial", 13),
                    text_color="#212121",
                    anchor="w",
                    justify="left",
                    wraplength=300
                )
                texto.pack(fill="both", padx=10, pady=6)

# Ejemplo de uso (en tu app principal):
# notificador = Notificador(self)
# notificador.recibir_alerta("Nueva alerta de pH detectada")
