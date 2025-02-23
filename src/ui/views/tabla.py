import sys
import customtkinter as ctk
import mysql.connector

# Agregar la ruta al directorio raíz del proyecto (donde está 'config')
sys.path.append('C:\\Users\\Colibecas\\Desktop\\PI')  # Ajusta la ruta a la raíz del proyecto

# Ahora importa la configuración de la base de datos
from config.db.config import DB_CONFIG

def crear_tabla(ventana, datos):
    fuente = ("Arial", 12)
    color_fondo_ventana = "#f0f0f0"
    color_fondo_encabezado = "#40E0D0"
    color_borde = "#000000"  # Color del borde
    borde_ancho = 2  # Grosor del borde

    ventana.configure(bg=color_fondo_ventana)

    marco_tabla = ctk.CTkFrame(ventana, fg_color="transparent")
    marco_tabla.pack(padx=10, pady=10, fill="both", expand=True)

    for i, fila in enumerate(datos):
        for j, valor in enumerate(fila):
            if i == 0:
                fuente_celda = ("Arial", 12, "bold")
                color_fondo_celda = color_fondo_encabezado
            else:
                fuente_celda = fuente
                color_fondo_celda = "white"

            # Crear marco de celda con borde
            celda_marco = ctk.CTkFrame(marco_tabla, border_width=borde_ancho, border_color=color_borde)
            celda_marco.grid(row=i, column=j, sticky="nsew")

            etiqueta = ctk.CTkLabel(
                celda_marco,
                text=valor,
                fg_color=color_fondo_celda,
                font=fuente_celda,
                corner_radius=0,
                padx=5,
                pady=2
            )
            etiqueta.pack(fill="both", expand=True)

            # Permitir que las columnas se expandan
            marco_tabla.grid_columnconfigure(j, weight=1)

    ventana.geometry("700x400")


def obtener_datos_db():
    # Usar la configuración de la base de datos desde DB_CONFIG
    conexion = mysql.connector.connect(
        host=DB_CONFIG["host"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        database=DB_CONFIG["database"],
    )

    cursor = conexion.cursor()
    query = "SELECT id_sensor, tipo_sensor, estado, fecha_instalacion, valor, fecha_hora FROM php"
    cursor.execute(query)
    datos = cursor.fetchall()

    conexion.close()

    return datos


ctk.set_appearance_mode("light")  # "dark" para modo oscuro
ctk.set_default_color_theme("blue")

ventana = ctk.CTk()
ventana.title("Historial de Sensores")

datos = obtener_datos_db()

encabezados = ["ID Sensor", "Tipo Sensor", "Estado", "Fecha Instalación", "Valor", "Fecha y Hora"]
datos = [encabezados] + datos

crear_tabla(ventana, datos)

ventana.mainloop()