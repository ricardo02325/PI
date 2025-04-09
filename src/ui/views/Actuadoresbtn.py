import customtkinter as ctk
import mysql.connector

def crear_interfaz_actuadores(root):
    DB_HOST = "127.0.0.1"
    DB_USER = "root"
    DB_PASSWORD = ""
    DB_NAME = "sistema_hidroponico"

    bomba_nombres = ["Bomba 1", "Bomba 2", "Bomba 3", "Bomba 4"]

    def obtener_estados():
        """Obtiene los estados de los actuadores desde la base de datos."""
        try:
            db = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME
            )
            cursor = db.cursor()
            query = "SELECT estado FROM actuadores ORDER BY id_actuador ASC LIMIT 4"
            cursor.execute(query)
            estados = [fila[0] for fila in cursor.fetchall()]
            cursor.close()
            db.close()
            return estados
        except mysql.connector.Error as err:
            print(f"Error de conexión a la base de datos: {err}")
            return ["Inactivo"] * 4  

    def actualizar_estados():
        """Actualiza la interfaz con los estados actuales de los actuadores."""
        estados = obtener_estados()
        
        for i, estado in enumerate(estados):
            color = "#E74C3C" if estado == "Inactivo" else "#2ECC71"  # Rojo o Verde moderno
            boton_text = "Encender" if estado == "Inactivo" else "Apagar"
            boton_color = "#3498DB" if estado == "Inactivo" else "#E74C3C"  # Azul o Rojo moderno

            indicadores[i].configure(fg_color=color, border_color="white" if estado == "Activo" else "#ccc", border_width=3)
            botones[i].configure(text=boton_text, fg_color=boton_color, hover_color="#2980B9" if estado == "Inactivo" else "#C0392B")

        root.after(5000, actualizar_estados)

    def cambiar_estado(indice):
        """Cambia el estado de un actuador en la base de datos."""
        try:
            db = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME
            )
            cursor = db.cursor()
            cursor.execute("SELECT estado FROM actuadores WHERE id_actuador = %s", (indice + 1,))
            estado_actual = cursor.fetchone()
            
            if estado_actual:
                nuevo_estado = "Activo" if estado_actual[0] == "Inactivo" else "Inactivo"
                cursor.execute("UPDATE actuadores SET estado = %s WHERE id_actuador = %s", (nuevo_estado, indice + 1))
                db.commit()
            
            cursor.close()
            db.close()
            actualizar_estados()
        except mysql.connector.Error as err:
            print(f"Error al actualizar el estado: {err}")

    # Configuración de la interfaz
    root.grid_rowconfigure((0, 1, 2), weight=1)
    root.grid_columnconfigure((0, 1), weight=1)

    # Título centrado con icono
    titulo = ctk.CTkLabel(root, text=" CONTROL DE ACTUADORES ", font=("Arial", 32, "bold"))
    titulo.grid(row=0, column=0, columnspan=2, pady=20)

    # Creación de los recuadros con estilo moderno
    global indicadores, botones
    indicadores = []
    botones = []

    for i in range(4):
        frame = ctk.CTkFrame(root, width=250, height=150, fg_color="#f8f9fa", 
                             corner_radius=15, border_width=2, border_color="#BDC3C7")
        frame.grid(row=(i // 2) + 1, column=i % 2, padx=15, pady=15, sticky="nsew")
        
        # Etiqueta de nombre
        nombre_label = ctk.CTkLabel(frame, text=bomba_nombres[i], font=("Arial", 18, "bold"), text_color="#2C3E50")
        nombre_label.pack(pady=10, anchor="center")
        
        # Indicador de estado con borde blanco brillante si está activo
        indicador = ctk.CTkFrame(frame, width=50, height=50, fg_color="#E74C3C", corner_radius=25, border_width=3, border_color="#ccc")
        indicador.pack(pady=10, anchor="center")
        
        # Botón moderno con hover y sombra ligera
        boton = ctk.CTkButton(frame, text="Cargando...", command=lambda i=i: cambiar_estado(i), 
                              fg_color="#3498DB", hover_color="#2980B9", font=("Arial", 20, "bold"), 
                              text_color="white", corner_radius=8, width=160, height=50)
        boton.pack(pady=10, anchor="center")
        
        indicadores.append(indicador)
        botones.append(boton)

    # Cargar estados iniciales
    actualizar_estados()
    