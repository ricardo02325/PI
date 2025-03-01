import sys
import customtkinter as ctk
import mysql.connector

sys.path.append('C:\\Users\\Colibecas\\Desktop\\PI')

# Importa la configuración de la base de datos
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
        query = "SELECT id_actuador, tipo_actuador, estado, fecha_instalacion, valor, fecha_hora FROM inf_actuadores"
        cursor.execute(query)
        datos = cursor.fetchall()
        conexion.close()

        return datos if datos else [["No hay datos disponibles."]]

    except mysql.connector.Error as err:
        print(f"Error al conectar con la base de datos: {err}")
        return [["Error al conectar con la base de datos."]]

def crear_tabla(ventana, datos):
    """Crea una tabla en una ventana dada con los datos proporcionados."""
    fuente = ("Arial", 12)
    color_fondo_encabezado = "#40E0D0"
    color_borde = "#000000"
    borde_ancho = 2

    ventana.configure(fg_color="white")  # Color de fondo del contenido

    marco_tabla = ctk.CTkFrame(ventana, fg_color="transparent")
    marco_tabla.pack(padx=10, pady=10, fill="both", expand=True)

    for i, fila in enumerate(datos):
        for j, valor in enumerate(fila):
            fuente_celda = ("Arial", 12, "bold") if i == 0 else fuente
            color_fondo_celda = color_fondo_encabezado if i == 0 else "white"

            # Crear marco de celda con borde
            celda_marco = ctk.CTkFrame(marco_tabla, border_width=borde_ancho, border_color=color_borde)
            celda_marco.grid(row=i, column=j, sticky="nsew")

            etiqueta = ctk.CTkLabel(
                celda_marco,
                text=str(valor),  # Convertir a string para evitar errores
                fg_color=color_fondo_celda,
                font=fuente_celda,
                corner_radius=0,
                padx=5,
                pady=2
            )
            etiqueta.pack(fill="both", expand=True)

            # Permitir que las columnas se expandan
            marco_tabla.grid_columnconfigure(j, weight=1)

def mostrar_historial():
    """Muestra la tabla al hacer click en 'Historial de datos', eliminando la anterior si existe."""
    for widget in content.winfo_children():
        widget.destroy()  # Elimina todos los widgets dentro del contenedor

    content.place(x=200, y=0, relwidth=1, relheight=1)  # Coloca la tabla correctamente
    crear_tabla(content, datos)

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
options = ["Estado del sistema", "Sensores", "Control de actuadores", "Historial de datos", "Configuración"]
for option in options:
    button = ctk.CTkButton(navbar, text=option, fg_color="sky blue", hover_color="deep sky blue", 
                           font=("Arial", 14), corner_radius=5, width=180, height=40, anchor="w") 
    if option == "Historial de datos":
        button.configure(command=mostrar_historial)  # Asociar la función para mostrar la tabla
    button.pack(pady=8, padx=10)

# Obtener los datos de la base de datos
datos = obtener_datos_db()
encabezados = ["ID Sensor", "Tipo Sensor", "Estado", "Fecha Instalación", "Valor", "Fecha y Hora"]
datos = [encabezados] + datos

# Crear el área de contenido principal (inicialmente oculta)
content = ctk.CTkFrame(root, fg_color="white")

# Iniciar el bucle principal de la aplicación
root.mainloop()