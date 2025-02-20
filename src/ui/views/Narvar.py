import customtkinter as ctk
# Comentario
# Configuración inicial de CustomTkinter
ctk.set_appearance_mode("light")  # Modo claro
ctk.set_default_color_theme("blue")  # Tema azul

# Variables globales para controlar la animación
is_animating = False  # Evita que se solapen múltiples animaciones
target_x = 0  # Posición objetivo de la barra

# Función para ocultar/mostrar la barra de navegación con animación
def toggle_navbar():
    global target_x, is_animating

    if is_animating:
        return  # Evita que se inicie una nueva animación si ya hay una en curso

    current_x = navbar.winfo_x()
    target_x = -200 if current_x >= 0 else 0  # Alternar entre -200 (oculto) y 0 (visible)
    animate_navbar(current_x, target_x)

# Función para animar la barra de navegación
def animate_navbar(current_x, target_x):
    global is_animating

    step = -10 if target_x < current_x else 10  # Paso de animación
    new_x = current_x + step

    # Limita la posición para que no exceda el objetivo
    if (step > 0 and new_x > target_x) or (step < 0 and new_x < target_x):
        new_x = target_x

    navbar.place(x=new_x, y=0, relheight=1)  # Mueve la barra a la nueva posición
    content.place(x=new_x + 200, y=0, relwidth=1, relheight=1)  # Ajusta el contenido principal

    # Si no hemos alcanzado la posición objetivo, continuar la animación
    if new_x != target_x:
        is_animating = True
        root.after(10, animate_navbar, new_x, target_x)
    else:
        is_animating = False  # La animación ha terminado

# Crear la ventana principal
root = ctk.CTk()
root.title("Sistema Hidropónico")
root.geometry("1000x600")

# Crear un frame para la barra de navegación
navbar = ctk.CTkFrame(root, width=200, fg_color="sky blue", corner_radius=0)
navbar.place(x=0, y=0, relheight=1)  # Posición inicial de la barra

# Frame para el título
title_frame = ctk.CTkFrame(navbar, fg_color="sky blue", corner_radius=0)
title_frame.pack(fill="x", pady=20, padx=10)  # Aumentamos el padding superior

# Título de la barra de navegación
title_label = ctk.CTkLabel(title_frame, text="Sistema Hidropónico", font=("Arial", 16, "bold"), 
                           text_color="white", fg_color="sky blue")
title_label.pack(side="left", padx=20)

# Opciones de la barra de navegación
options = ["Estado del sistema", "Sensores", "Control de actuadores", "Historial de datos", "Configuración"]
for option in options:
    button = ctk.CTkButton(navbar, text=option, fg_color="sky blue", hover_color="deep sky blue", 
                           font=("Arial", 14), corner_radius=5, width=180, height=40, anchor="w")  # Botones más grandes y alineados a la izquierda
    button.pack(pady=8, padx=10)  # Más espacio entre botones

# Frame para el contenido principal
content = ctk.CTkFrame(root, fg_color="white")
content.place(x=200, y=0, relwidth=1, relheight=1)  # Ajuste para el contenido

# Botón para desocultar la barra (siempre visible)
show_navbar_button = ctk.CTkButton(
    root, 
    text="☰",  # Ícono de tres líneas horizontales
    command=toggle_navbar, 
    width=30, 
    height=30, 
    fg_color="white",  # Fondo blanco
    hover_color="#f0f0f0",  # Color de hover gris claro
    text_color="black",  # Ícono en negro
    font=("Arial", 16),  # Tamaño del ícono
    corner_radius=5
)
show_navbar_button.place(x=10, y=10)  # Posición en la esquina superior izquierda

# Iniciar el bucle principal de la aplicación
root.mainloop()