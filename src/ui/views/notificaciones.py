import customtkinter as ctk
from datetime import datetime

class Notificador:
    def __init__(self, root):
        self.parent = root
        self.nuevas_alertas = []
        self.panel_visible = False

        # Botón de notificación usando CTkLabel (más control visual)
        self.btn_campana = ctk.CTkLabel(
            master=self.parent,
            text="🔔",
            width=45,
            height=45,
            font=("Arial", 20),
            fg_color="#FFFFFF",       # Fondo blanco
            text_color="#212121",     # Color del texto (icono)
            corner_radius=100,        # Hacemos el label completamente redondo
            cursor="hand2"           # Cambia el cursor al pasar por encima
        )
        self.btn_campana.place(relx=1.0, rely=0.0, x=-20, y=20, anchor="ne")
        
        # Configuramos los eventos para simular un botón
        self.btn_campana.bind("<Button-1>", lambda e: self.toggle_panel())
        self.btn_campana.bind("<Enter>", lambda e: self.btn_campana.configure(fg_color="#E0E0E0"))  # Gris claro al pasar el mouse
        self.btn_campana.bind("<Leave>", lambda e: self.btn_campana.configure(fg_color="#FFFFFF"))  # Vuelve a blanco al salir

        # Panel de notificaciones
        self.panel = ctk.CTkFrame(
            master=self.parent,
            width=350,
            height=250,
            corner_radius=15,
            fg_color="#ffffff",
            border_width=1,
            border_color="#BDBDBD"
        )
        self.contenido_panel = ctk.CTkScrollableFrame(self.panel, fg_color="transparent")
        self.contenido_panel.pack(fill="both", expand=True, padx=10, pady=10)

    def toggle_panel(self, event=None):
        if self.panel_visible:
            self.panel.place_forget()
            self.panel_visible = False
        else:
            self.actualizar_panel()
            self.panel.place(relx=1.0, rely=0.0, x=-20, y=75, anchor="ne")
            self.panel_visible = True
            self.btn_campana.configure(fg_color="#FFFFFF")  # Restablecer fondo blanco
            self.nuevas_alertas.clear()

    def recibir_alerta(self, mensaje):
        ahora = datetime.now().strftime("%H:%M:%S")
        self.nuevas_alertas.append((mensaje, ahora))
        self.btn_campana.configure(fg_color="#FFEB3B")  # Amarillo al recibir alerta
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

# Ejemplo de uso
if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("800x600")
    
    notificador = Notificador(root)
    
    # Ejemplo: agregar una notificación después de 2 segundos
    root.after(2000, lambda: notificador.recibir_alerta("Esta es una notificación de prueba"))
    
    root.mainloop()