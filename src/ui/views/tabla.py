import tkinter as tk
import mysql.connector

def crear_tabla(ventana, datos):
    fuente = ("Arial", 12)
    color_fondo_celda = "white"
    color_fondo_ventana = "#f0f0f0"
    color_fondo_encabezado = "#40E0D0"
    borde_celda = 1
    color_borde = "white"

    ventana.configure(bg=color_fondo_ventana)

    for i, fila in enumerate(datos):
        for j, valor in enumerate(fila):
            if i == 0:
                fuente_celda = ("Arial", 12, "bold")
                color_fondo_celda = color_fondo_encabezado
            else:
                fuente_celda = fuente
                color_fondo_celda = "white"

            etiqueta = tk.Label(
                ventana,
                text=valor,
                borderwidth=borde_celda,
                relief="solid",
                bg=color_fondo_celda,
                font=fuente_celda,
                anchor="w",
                padx=5,
                pady=2,
                highlightbackground=color_borde,
                highlightcolor=color_borde,
            )
            etiqueta.grid(row=i, column=j, padx=0, pady=0, sticky="ew")

            ventana.grid_columnconfigure(j, weight=1)

    ventana.geometry("600x300")


def obtener_datos_db():
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="sistema_hidroponico",
    )

    cursor = conexion.cursor()
    query = "SELECT id_sensor, tipo_sensor, estado, fecha_instalacion, valor, fecha_hora FROM php"
    cursor.execute(query)
    datos = cursor.fetchall()

    conexion.close()

    return datos


ventana = tk.Tk()
ventana.title("Historial de Sensores")

datos = obtener_datos_db()

encabezados = ["ID Sensor", "Tipo Sensor", "Estado", "Fecha Instalación", "Valor", "Fecha y Hora"]
datos = [encabezados] + datos

crear_tabla(ventana, datos)

ventana.mainloop()