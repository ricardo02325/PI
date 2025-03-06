<<<<<<< HEAD
import sys
import customtkinter as ctk

# Variables globales para controlar la animación
is_animating = False
target_x = 0

# Función para ocultar/mostrar la barra de navegación con animación
def toggle_navbar():
    global target_x, is_animating
    if is_animating:
        return
=======
import customtkinter as ctk
from Graficas_sensores import iniciar_graficas
import sys
import mysql.connector

sys.path.append('C:\\Users\\Colibecas\\Desktop\\PI')

# Configuración de conexión a la base de datos
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",  # Agregar contraseña si es necesario
    "database": "sistema_hidroponico"
}

def conectar_db():
    try:
        conexion = mysql.connector.connect(**DB_CONFIG)
        if conexion.is_connected():
            print("Conexión exitosa a la base de datos")
        return conexion
    except mysql.connector.Error as error:
        print(f"Error al conectar a la base de datos: {error}")
        return None

def obtener_datos_sensores():
    conexion = conectar_db()
    if conexion:
        try:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("SELECT * FROM lecturas_sensores")
            lecturas = cursor.fetchall()
            return lecturas
        except mysql.connector.Error as error:
            print(f"Error en la consulta: {error}")
            return []
        finally:
            cursor.close()
            conexion.close()
    return []

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

is_animating = False  
target_x = 0  

def toggle_navbar():
    global target_x, is_animating
    if is_animating:
        return 
>>>>>>> 32a6936cef92d92c2d2f7ff7f472316f6f551129
    current_x = navbar.winfo_x()
    target_x = -200 if current_x >= 0 else 0
    animate_navbar(current_x, target_x)

<<<<<<< HEAD
# Función para animar la barra de navegación
def animate_navbar(current_x, target_x):
    global is_animating
    step = -10 if target_x < current_x else 10
=======
def animate_navbar(current_x, target_x):
    global is_animating
    step = -10 if target_x < current_x else 10 
>>>>>>> 32a6936cef92d92c2d2f7ff7f472316f6f551129
    new_x = current_x + step
    if (step > 0 and new_x > target_x) or (step < 0 and new_x < target_x):
        new_x = target_x
    navbar.place(x=new_x, y=0, relheight=1)
<<<<<<< HEAD
    content.place(x=new_x + 200, y=0, relwidth=1, relheight=1)
=======
    content.place(x=new_x + 200, y=0, relwidth=1, relheight=1) 
>>>>>>> 32a6936cef92d92c2d2f7ff7f472316f6f551129
    if new_x != target_x:
        is_animating = True
        root.after(10, animate_navbar, new_x, target_x)
    else:
        is_animating = False

<<<<<<< HEAD
# Simulación de datos de sensores
def obtener_datos_db():
    return [
        [1, "Sensor de temperatura", "Activo", "2025-01-01", "25.3", "2025-01-01 12:30"],
        [2, "Sensor de pH", "Inactivo", "2025-02-01", "6.5", "2025-02-01 14:00"],
        [3, "Sensor de conductividad", "Activo", "2025-03-01", "1.2", "2025-03-01 10:15"]
    ]

# Función para inicializar la tabla de historial de sensores en el contenido principal
def mostrar_historial_sensores():
    try:
        datos = obtener_datos_db()
    except Exception as e:
        print(f"Error al obtener datos de la base de datos: {e}")
        datos = []

    encabezados = ["ID Sensor", "Tipo Sensor", "Estado", "Fecha Instalación", "Valor", "Fecha y Hora"]
    datos = [encabezados] + datos

    if datos:
        crear_tabla(content, datos)
    else:
        ctk.CTkLabel(content, text="No se han encontrado datos.", font=("Arial", 14)).place(x=50, y=50)

# Función para manejar el clic en los botones de la barra de navegación
def handle_navbar_option(option):
    if option == "Historial de datos":
        mostrar_historial_sensores()

# Función para crear una tabla dentro del contenido
def crear_tabla(ventana, datos):
    for i, row in enumerate(datos):
        for j, item in enumerate(row):
            cell = ctk.CTkLabel(ventana, text=item, font=("Arial", 12), width=150, height=40, anchor="w", fg_color="lightgray" if i % 2 == 0 else "white")
            cell.grid(row=i, column=j, padx=5, pady=5)

# Crear la ventana principal
=======
>>>>>>> 32a6936cef92d92c2d2f7ff7f472316f6f551129
root = ctk.CTk()
root.title("Sistema Hidropónico")
root.geometry("1000x600")

<<<<<<< HEAD
# Crear un frame para la barra de navegación
navbar = ctk.CTkFrame(root, width=200, fg_color="sky blue", corner_radius=0)
navbar.place(x=0, y=0, relheight=1)

# Frame para el título
=======
navbar = ctk.CTkFrame(root, width=200, fg_color="sky blue", corner_radius=0)
navbar.place(x=0, y=0, relheight=1)  

>>>>>>> 32a6936cef92d92c2d2f7ff7f472316f6f551129
title_frame = ctk.CTkFrame(navbar, fg_color="sky blue", corner_radius=0)
title_frame.pack(fill="x", pady=20, padx=10)

# Título de la barra de navegación
title_label = ctk.CTkLabel(title_frame, text="Sistema Hidropónico", font=("Arial", 16, "bold"), 
                           text_color="white", fg_color="sky blue")
title_label.pack(side="left", padx=20)

<<<<<<< HEAD
# Opciones de la barra de navegación
options = ["Estado del sistema", "Sensores", "Control de actuadores", "Historial de datos", "Configuración"]
for option in options:
    button = ctk.CTkButton(navbar, text=option, fg_color="sky blue", hover_color="deep sky blue", 
                           font=("Arial", 14), corner_radius=5, width=180, height=40, anchor="w", 
                           command=lambda option=option: handle_navbar_option(option)) 
    button.pack(pady=8, padx=10)

# Frame para el contenido principal
content = ctk.CTkFrame(root, fg_color="white")
content.place(x=200, y=0, relwidth=1, relheight=1)

# Botón para desocultar la barra
=======
options = ["Estado del sistema", "Sensores", "Control de actuadores", "Historial de datos", "Configuración"]
for option in options:
    button = ctk.CTkButton(navbar, text=option, fg_color="sky blue", hover_color="deep sky blue", 
                           font=("Arial", 14), corner_radius=5, width=180, height=40, anchor="w")  
    button.pack(pady=8, padx=10)  

content = ctk.CTkFrame(root, fg_color="white")
content.place(x=200, y=0, relwidth=1, relheight=1) 

>>>>>>> 32a6936cef92d92c2d2f7ff7f472316f6f551129
show_navbar_button = ctk.CTkButton(
    root, 
    text="☰",  
    command=toggle_navbar, 
    width=30, 
    height=30, 
    fg_color="white",  
    hover_color="#f0f0f0",  
    text_color="black",  
    font=("Arial", 16),  
    corner_radius=5
)
<<<<<<< HEAD
show_navbar_button.place(x=10, y=10)
=======
show_navbar_button.place(x=10, y=10) 

iniciar_graficas(content)
>>>>>>> 32a6936cef92d92c2d2f7ff7f472316f6f551129

root.mainloop()