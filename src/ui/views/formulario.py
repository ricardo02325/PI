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

def crear_formulario(parent):
    # Frame principal con fondo blanco
    frame_principal = ctk.CTkFrame(parent, fg_color="white")
    frame_principal.pack(pady=10, padx=10, fill="both", expand=True)

    # Obtener datos
    datos = obtener_datos_sistema()

    # Etiqueta de encabezado
    titulo_label = ctk.CTkLabel(frame_principal, text="Datos de Sensores", font=("Arial", 20, "bold"), text_color="#00A3A3")
    titulo_label.pack(pady=(10, 20))

    # Crear formulario con los datos obtenidos
    entradas = {}
    for i, (sensor, valor) in enumerate(datos):
        frame_fila = ctk.CTkFrame(frame_principal, fg_color="transparent")
        frame_fila.pack(pady=5, padx=10, fill="x")
        
        etiqueta = ctk.CTkLabel(frame_fila, text=sensor, font=("Arial", 14), width=20, anchor="w")
        etiqueta.pack(side="left", padx=(10, 5))
        
        entrada = ctk.CTkEntry(frame_fila, font=("Arial", 14), width=150)
        entrada.insert(0, valor)
        entrada.pack(side="left", padx=5)
        
        entradas[sensor] = entrada

    # Botón de enviar
    boton_enviar = ctk.CTkButton(frame_principal, text="Guardar Datos", font=("Arial", 14, "bold"), fg_color="#00A3A3", text_color="white")
    boton_enviar.pack(pady=20)

    return frame_principal