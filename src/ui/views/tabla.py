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
    color_fondo_ventana = "#f0f0f0"
    color_fondo_encabezado = "#40E0D0"
    color_borde = "#000000"
    borde_ancho = 2

    ventana.configure(bg=color_fondo_ventana)

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

    # Establecer un tamaño de ventana adecuado si no se pasa de parámetros
    ventana.geometry("700x400")

# Crear la ventana principal
root = ctk.CTk()
root.title("Sistema Hidropónico")
root.geometry("700x400")

# Obtener los datos de la base de datos
datos = obtener_datos_db()
encabezados = ["ID Sensor", "Tipo Sensor", "Estado", "Fecha Instalación", "Valor", "Fecha y Hora"]
datos = [encabezados] + datos

# Crear la tabla en la ventana principal
crear_tabla(root, datos)

# Iniciar el bucle principal de la aplicación
root.mainloop()