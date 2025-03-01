import sys
import customtkinter as ctk
import mysql.connector
from tkcalendar import DateEntry
import tkinter as tk

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
        query = "SELECT id_alerta, tipo_alerta, descripcion, fecha_hora, estado FROM alertas"
        cursor.execute(query)
        datos = cursor.fetchall()
        conexion.close()

        return datos if datos else [["No hay datos disponibles."]]

    except mysql.connector.Error as err:
        print(f"Error al conectar con la base de datos: {err}")
        return [["Error al conectar con la base de datos."]]

def crear_formulario(ventana):
    """Crea un formulario en la ventana dada con los campos proporcionados."""
    ventana.configure(fg_color="white")  # Color de fondo del contenido

    marco_formulario = ctk.CTkFrame(ventana, fg_color="transparent")
    marco_formulario.pack(padx=10, pady=10, fill="both", expand=True)

    # Campos del formulario
    etiquetas = ["ID Alerta", "Tipo de Alerta", "Descripción", "Fecha y Hora", "Estado"]
    entradas = {}
    
    for i, etiqueta in enumerate(etiquetas):
        # Crear etiqueta y campo de entrada
        ctk.CTkLabel(marco_formulario, text=etiqueta, font=("Arial", 12)).grid(row=i, column=0, padx=10, pady=5, sticky="e")
        
        if etiqueta == "Fecha y Hora":
            # Crear selector de fecha
            fecha_entry = DateEntry(marco_formulario, font=("Arial", 12), width=20)
            fecha_entry.grid(row=i, column=1, padx=10, pady=5, sticky="w")
            entradas["Fecha y Hora"] = fecha_entry  # Guardamos el campo de fecha
        else:
            campo = ctk.CTkEntry(marco_formulario, font=("Arial", 12))
            campo.grid(row=i, column=1, padx=10, pady=5, sticky="w")
            entradas[etiqueta] = campo  # Guardamos los campos de entrada en un diccionario

    # Crear campo de hora
    ctk.CTkLabel(marco_formulario, text="Hora", font=("Arial", 12)).grid(row=5, column=0, padx=10, pady=5, sticky="e")
    hora_entry = ctk.CTkEntry(marco_formulario, font=("Arial", 12), placeholder_text="HH:MM")
    hora_entry.grid(row=5, column=1, padx=10, pady=5, sticky="w")
    entradas["Hora"] = hora_entry  # Guardamos el campo de hora

    # Botón para enviar el formulario
    boton_guardar = ctk.CTkButton(marco_formulario, text="Guardar", font=("Arial", 12), command=lambda: guardar_alerta(entradas))
    boton_guardar.grid(row=6, column=0, columnspan=2, pady=10)

def guardar_alerta(entradas):
    """Guarda los datos del formulario en la base de datos."""
    id_alerta = entradas["ID Alerta"].get()
    tipo_alerta = entradas["Tipo de Alerta"].get()
    descripcion = entradas["Descripción"].get()
    fecha = entradas["Fecha y Hora"].get()  # Obtener fecha del selector
    hora = entradas["Hora"].get()  # Obtener hora del campo de texto
    estado = entradas["Estado"].get()

    # Concatenar fecha y hora
    fecha_hora = f"{fecha} {hora}"

    try:
        # Conexión a la base de datos
        conexion = mysql.connector.connect(
            host=DB_CONFIG["host"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            database=DB_CONFIG["database"],
        )
        cursor = conexion.cursor()

        # Consulta SQL para insertar los datos en la base de datos
        query = """
            INSERT INTO alertas (id_alerta, tipo_alerta, descripcion, fecha_hora, estado)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (id_alerta, tipo_alerta, descripcion, fecha_hora, estado))
        conexion.commit()  # Confirmar los cambios en la base de datos
        conexion.close()

        # Confirmación
        print("Datos insertados correctamente.")
    except mysql.connector.Error as err:
        print(f"Error al insertar los datos: {err}")

def mostrar_formulario():
    """Muestra el formulario al hacer click en 'Formulario de Alertas'."""
    for widget in content.winfo_children():
        widget.destroy()  # Elimina todos los widgets dentro del contenedor

    content.place(x=200, y=0, relwidth=1, relheight=1)  # Coloca el formulario correctamente
    crear_formulario(content)

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
options = ["Estado del sistema", "Sensores", "Control de actuadores", "Formulario de Alertas", "Configuración"]
for option in options:
    button = ctk.CTkButton(navbar, text=option, fg_color="sky blue", hover_color="deep sky blue", 
                           font=("Arial", 14), corner_radius=5, width=180, height=40, anchor="w") 
    if option == "Formulario de Alertas":
        button.configure(command=mostrar_formulario)  # Asociar la función para mostrar el formulario
    button.pack(pady=8, padx=10)

# Obtener los datos de la base de datos
datos = obtener_datos_db()

# Crear el área de contenido principal (inicialmente oculta)
content = ctk.CTkFrame(root, fg_color="white")

# Iniciar el bucle principal de la aplicación
root.mainloop()