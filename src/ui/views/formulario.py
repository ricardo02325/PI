import sys
import customtkinter as ctk
import mysql.connector

sys.path.append('C:\\Users\\Colibecas\\Desktop\\PI')
from config.db.config import DB_CONFIG

def obtener_datos_db():
    """Obtiene los datos de la base de datos y los devuelve en una lista."""
    try:
        conexion = mysql.connector.connect(
            host=DB_CONFIG["host"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            database=DB_CONFIG["database"],
        )
        cursor = conexion.cursor()
        query = "SELECT id_alerta, tipo_alerta, descripcion, fecha_hora, estado FROM alertas"
        cursor.execute(query)
        datos = cursor.fetchall()
        conexion.close()
        return datos if datos else [["No hay datos disponibles."]]
    except mysql.connector.Error as err:
        print(f"Error al conectar con la base de datos: {err}")
        return [["Error al conectar con la base de datos."]]

def toggle_navbar():
    """Muestra u oculta la barra de navegación."""
    global navbar_visible
    if navbar_visible:
        navbar.place_forget()
    else:
        navbar.place(x=0, y=0, relheight=1)
    navbar_visible = not navbar_visible

# Crear la ventana principal
root = ctk.CTk()
root.title("Sistema Hidropónico")
root.geometry("1000x600")  # Ajustar el tamaño de la ventana principal

# Estado inicial de la barra de navegación
navbar_visible = True

# Crear barra de navegación (inicialmente visible)
navbar = ctk.CTkFrame(root, width=200, fg_color="sky blue", corner_radius=0)
navbar.place(x=0, y=0, relheight=1)

# Botón de 3 líneas horizontales en la esquina superior izquierda
toggle_button = ctk.CTkButton(root, text="☰", font=("Arial", 18), fg_color="sky blue", 
                              hover_color="deep sky blue", corner_radius=5, width=40, height=40, 
                              command=toggle_navbar)
toggle_button.place(x=10, y=10)  # Coloca el botón en la esquina superior izquierda

# Opciones de la barra de navegación
options = ["Estado del sistema", "Sensores", "Control de actuadores", "Configuración"]
for option in options:
    button = ctk.CTkButton(navbar, text=option, fg_color="sky blue", hover_color="deep sky blue", 
                           font=("Arial", 14), corner_radius=5, width=180, height=40, anchor="w") 
    button.pack(pady=8, padx=10)

# Frame para la tarjeta de alertas
card = ctk.CTkFrame(root, width=750, height=200, fg_color="white", corner_radius=10)
card.place(x=220, y=50)

# Título de la tarjeta
card_title = ctk.CTkLabel(card, text="Alertas del Sistema", font=("Arial", 16, "bold"), text_color="black")
card_title.pack(pady=10)

# Contenedor para mostrar las alertas
alert_container = ctk.CTkFrame(card, width=700, height=150, fg_color="light gray", corner_radius=5)
alert_container.pack(pady=5, padx=10, fill="both", expand=True)

# Obtener y mostrar los datos de la base de datos
datos = obtener_datos_db()

for alerta in datos[:5]:  # Mostrar solo las primeras 5 alertas
    texto_alerta = f"ID: {alerta[0]} | Tipo: {alerta[1]} | {alerta[2]} | {alerta[3]} | Estado: {alerta[4]}"
    alerta_label = ctk.CTkLabel(alert_container, text=texto_alerta, font=("Arial", 12), text_color="black", anchor="w")
    alerta_label.pack(fill="x", padx=5, pady=2)

# Iniciar el bucle principal de la aplicación
root.mainloop()