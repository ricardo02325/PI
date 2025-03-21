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

def mostrar_modal(frame_modal, label_modal, tipo_alerta):
    frame_modal.place(relx=0.5, rely=0.5, anchor="center")
    label_modal.configure(text=f"Resolviendo alerta de {tipo_alerta}...")

    frame_modal.update()
    frame_modal.after(2000, lambda: actualizar_modal(frame_modal, label_modal, tipo_alerta))

def actualizar_modal(frame_modal, label_modal, tipo_alerta):
    label_modal.configure(text=f"¡Alerta de {tipo_alerta} resuelta! ✅")
    frame_modal.after(1500, frame_modal.place_forget)

def obtener_color_texto():
    # Obtener el modo de apariencia actual
    if ctk.get_appearance_mode() == "dark":
        return "white"  # Color blanco para texto en modo oscuro
    else:
        return "black"  # Color negro para texto en modo claro

def iniciar_alertas(frame):
    alertas = obtener_alertas()

    # Frame para el título con texto y símbolo de alerta
    frame_titulo = ctk.CTkFrame(frame)
    frame_titulo.pack(pady=(20, 10))

    # Agregar el texto y el símbolo de alerta
    label_titulo = ctk.CTkLabel(frame_titulo, text="🚨 Alertas 🚨", font=('Arial', 20, 'bold'), text_color=obtener_color_texto())
    label_titulo.pack()

    # Frame para los recuadros de alertas, centrados en la ventana
    frame_alertas = ctk.CTkFrame(frame)
    frame_alertas.pack(pady=10)

    # Crear recuadros con fondo blanco y contorno rojo
    recuadro_1 = ctk.CTkFrame(frame_alertas, width=250, height=120, corner_radius=10, fg_color="white", border_width=2, border_color="red")
    recuadro_1.grid(row=0, column=0, padx=10, pady=10)
    
    recuadro_2 = ctk.CTkFrame(frame_alertas, width=250, height=120, corner_radius=10, fg_color="white", border_width=2, border_color="red")
    recuadro_2.grid(row=0, column=1, padx=10, pady=10)

    recuadro_3 = ctk.CTkFrame(frame_alertas, width=250, height=120, corner_radius=10, fg_color="white", border_width=2, border_color="red")
    recuadro_3.grid(row=0, column=2, padx=10, pady=10)

    # Crear etiquetas con texto dinámico según el modo de apariencia
    label_1 = ctk.CTkLabel(recuadro_1, text='**¡Alerta de pH!**\nSin alertas detectadas.', font=('Arial', 12), text_color=obtener_color_texto())
    label_1.pack(padx=10, pady=10)

    label_2 = ctk.CTkLabel(recuadro_2, text='**¡Temperatura Alta!**\nSin alertas detectadas.', font=('Arial', 12), text_color=obtener_color_texto())
    label_2.pack(padx=10, pady=10)

    label_3 = ctk.CTkLabel(recuadro_3, text='**¡Alerta de Conductividad!**\nSin alertas detectadas.', font=('Arial', 12), text_color=obtener_color_texto())
    label_3.pack(padx=10, pady=10)

    # Crear botones con tamaño reducido
    def resolver_pH():
        mostrar_modal(frame_modal, label_modal, "pH")
    def resolver_temperatura():
        mostrar_modal(frame_modal, label_modal, "Temperatura")
    def resolver_conductividad():
        mostrar_modal(frame_modal, label_modal, "Conductividad")

    # Ajustar botones al ancho de los recuadros y agregar separación
    boton_1 = ctk.CTkButton(recuadro_1, text="Resolver", command=resolver_pH, width=230)
    boton_1.pack(pady=5, padx=10)

    boton_2 = ctk.CTkButton(recuadro_2, text="Resolver", command=resolver_temperatura, width=230)
    boton_2.pack(pady=5, padx=10)

    boton_3 = ctk.CTkButton(recuadro_3, text="Resolver", command=resolver_conductividad, width=230)
    boton_3.pack(pady=5, padx=10)

    # Crear el modal (ventana emergente dentro de la misma ventana)
    frame_modal = ctk.CTkFrame(frame, width=300, height=150, corner_radius=10, fg_color='gray')
    label_modal = ctk.CTkLabel(frame_modal, text="Resolviendo...", font=('Arial', 14))
    label_modal.pack(padx=10, pady=40)

    # Actualizar etiquetas con alertas si existen
    if len(alertas) > 0:
        label_1.configure(text=f"**¡Alerta de pH!**\n{alertas[0]['descripcion']}")
    if len(alertas) > 1:
        label_2.configure(text=f"**¡Temperatura Alta!**\n{alertas[1]['descripcion']}")
    if len(alertas) > 2:
        label_3.configure(text=f"**¡Alerta de Conductividad!**\n{alertas[2]['descripcion']}")
