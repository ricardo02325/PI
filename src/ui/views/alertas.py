import mysql.connector
import customtkinter as ctk

COLORES = {
    'pH': '#FFD700',  # Amarillo
    'Temperatura': '#FF6347',  # Rojo
    'Conductividad': '#1E90FF'  # Azul
}

def obtener_alertas():
    try:
        db = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='',
            database='sistema_hidroponico'
        )
        query = """
            SELECT * FROM alertas 
            WHERE tipo_alerta IN ('Valor fuera de rango') 
            AND estado = 'inactivo'
        """
        cursor = db.cursor(dictionary=True)
        cursor.execute(query)
        alertas = cursor.fetchall()
        cursor.close()
        db.close()
        return alertas
    except mysql.connector.Error as err:
        print(f"Error de conexión: {err}")
        return []

def iniciar_alertas(frame):
    alertas = obtener_alertas()

    # Crear recuadros
    recuadro_1 = ctk.CTkFrame(frame, width=250, height=120, corner_radius=10, fg_color=COLORES['pH'])
    recuadro_1.grid(row=0, column=0, padx=10, pady=10)
    
    recuadro_2 = ctk.CTkFrame(frame, width=250, height=120, corner_radius=10, fg_color=COLORES['Temperatura'])
    recuadro_2.grid(row=0, column=1, padx=10, pady=10)

    recuadro_3 = ctk.CTkFrame(frame, width=250, height=120, corner_radius=10, fg_color=COLORES['Conductividad'])
    recuadro_3.grid(row=0, column=2, padx=10, pady=10)

    # Crear etiquetas
    label_1 = ctk.CTkLabel(recuadro_1, text='**¡Alerta de pH!**\nSin alertas detectadas.', font=('Arial', 12))
    label_1.pack(padx=10, pady=10)

    label_2 = ctk.CTkLabel(recuadro_2, text='**¡Temperatura Alta!**\nSin alertas detectadas.', font=('Arial', 12))
    label_2.pack(padx=10, pady=10)

    label_3 = ctk.CTkLabel(recuadro_3, text='**¡Alerta de Conductividad!**\nSin alertas detectadas.', font=('Arial', 12))
    label_3.pack(padx=10, pady=10)

    # Actualizar etiquetas con alertas
    if len(alertas) > 0:
        label_1.configure(text=f"**¡Alerta de pH!**\n{alertas[0]['descripcion']}")
    if len(alertas) > 1:
        label_2.configure(text=f"**¡Temperatura Alta!**\n{alertas[1]['descripcion']}")
    if len(alertas) > 2:
        label_3.configure(text=f"**¡Alerta de Conductividad!**\n{alertas[2]['descripcion']}")