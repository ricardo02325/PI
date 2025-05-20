import customtkinter
from datetime import datetime

def crear_interfaz_notificaciones(frame):
    # Limpiar frame antes de mostrar notificaciones
    for widget in frame.winfo_children():
        widget.destroy()

    # Ejemplo de notificaciones
    notificaciones = [
        "Sensor de humedad bajo",
        "Bomba 1 apagada",
        "Nivel de agua bajo",
        "PH bajo",
        "Temperatura alta",
        "Conductividad electrica alta",
        "Temperatura muy alta",
        "PH alto"
    ]

    titulo = customtkinter.CTkLabel(
        frame, text="Notificaciones", font=customtkinter.CTkFont(size=20, weight="bold")
    )
    titulo.pack(pady=10)

    container = customtkinter.CTkScrollableFrame(frame, height=400)
    container.pack(fill="both", expand=True, padx=10, pady=10)

    for notif in notificaciones:
        # Fecha y hora actual para cada notificación
        fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Frame para cada notificación
        notif_frame = customtkinter.CTkFrame(
            container,
            corner_radius=8,
            fg_color="#e0f7fa",
            border_width=1,
            border_color="#4dd0e1"
        )
        notif_frame.pack(fill="x", pady=4, padx=6)

        # Texto de la falla
        falla_label = customtkinter.CTkLabel(
            notif_frame,
            text=f"Falla: {notif}",
            font=customtkinter.CTkFont(size=14, weight="bold"),
            anchor="w"
        )
        falla_label.pack(anchor="w", padx=8, pady=(6, 0))

        # Fecha y hora
        fecha_label = customtkinter.CTkLabel(
            notif_frame,
            text=f"Fecha y hora: {fecha_hora}",
            font=customtkinter.CTkFont(size=12),
            anchor="w"
        )
        fecha_label.pack(anchor="w", padx=8, pady=(0, 6))
