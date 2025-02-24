import customtkinter as ctk
from Narvar import Navbar
from Graficas_sensores import GraficasSensores

# Configuración global
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Crear ventana principal
root = ctk.CTk()
root.title("Sistema Hidropónico")
root.geometry("1400x600")

# Agregar la barra de navegación
navbar = Navbar(root)

# Crear un frame para las gráficas y agregarlas
frame_graficas = ctk.CTkFrame(root)
frame_graficas.pack(fill="both", expand=True, padx=20, pady=20)

graficas = GraficasSensores(frame_graficas)

root.mainloop()
