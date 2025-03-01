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
    current_x = navbar.winfo_x()
    target_x = -200 if current_x >= 0 else 0
    animate_navbar(current_x, target_x)

# Función para animar la barra de navegación
def animate_navbar(current_x, target_x):
    global is_animating
    step = -10 if target_x < current_x else 10
    new_x = current_x + step
    if (step > 0 and new_x > target_x) or (step < 0 and new_x < target_x):
        new_x = target_x
    navbar.place(x=new_x, y=0, relheight=1)
    content.place(x=new_x + 200, y=0, relwidth=1, relheight=1)
    if new_x != target_x:
        is_animating = True
        root.after(10, animate_navbar, new_x, target_x)
    else:
        is_animating = False

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
root = ctk.CTk()
root.title("Sistema Hidropónico")
root.geometry("1000x600")

# Crear un frame para la barra de navegación
navbar = ctk.CTkFrame(root, width=200, fg_color="sky blue", corner_radius=0)
navbar.place(x=0, y=0, relheight=1)

# Frame para el título
title_frame = ctk.CTkFrame(navbar, fg_color="sky blue", corner_radius=0)
title_frame.pack(fill="x", pady=20, padx=10)

# Título de la barra de navegación
title_label = ctk.CTkLabel(title_frame, text="Sistema Hidropónico", font=("Arial", 16, "bold"), 
                           text_color="white", fg_color="sky blue")
title_label.pack(side="left", padx=20)

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
show_navbar_button.place(x=10, y=10)

root.mainloop()