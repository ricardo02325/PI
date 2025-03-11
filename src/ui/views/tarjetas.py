import customtkinter as ctk
import mysql.connector

def obtener_datos_sistema():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="sistema_hidroponico"
        )

        cursor = conexion.cursor()
        cursor.execute("""
            SELECT tipo_sensor, valor FROM inf_sensores 
            WHERE id_lectura = ( 
                SELECT MAX(id_lectura) 
                FROM inf_sensores AS sub 
                WHERE sub.id_sensor = inf_sensores.id_sensor
            );
        """)

        resultados = cursor.fetchall()
        conexion.close()

        if resultados:
            return [(sensor, f"{valor}") for sensor, valor in resultados]
        else:
            return [("No hay datos", "N/A")]

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return [("Error de conexión", "N/A")]

def crear_tarjetas(parent):
    # Frame principal con fondo blanco
    frame_principal = ctk.CTkFrame(parent, fg_color="white")
    frame_principal.pack(pady=1, padx=1, fill="both", expand=True)

    # Obtener datos
    datos = obtener_datos_sistema()

    # Configurar el grid para expansión proporcional
    total_columnas = len(datos)
    for i in range(total_columnas):
        frame_principal.columnconfigure(i, weight=1)

    for i, (titulo, valor) in enumerate(datos):
        tarjeta = ctk.CTkFrame(
            frame_principal, fg_color="#D3D3D3", border_color="#00A3A3",
            border_width=3, corner_radius=12
        )
        tarjeta.grid(row=0, column=i, padx=8, pady=8, ipadx=10, ipady=25, sticky="nsew")  # Tamaño ajustado

        titulo_label = ctk.CTkLabel(tarjeta, text=titulo, font=("Arial", 16, "bold"), text_color="#00A3A3")
        titulo_label.pack(pady=(5, 2))

        valor_label = ctk.CTkLabel(tarjeta, text=valor, font=("Arial", 18, "bold"), text_color="black")
        valor_label.pack(pady=(2, 5))

    return frame_principal