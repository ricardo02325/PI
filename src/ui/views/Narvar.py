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
    current_x = navbar.winfo_x()
    target_x = -200 if current_x >= 0 else 0  
    animate_navbar(current_x, target_x)

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

root = ctk.CTk()
root.title("Sistema Hidropónico")
root.geometry("1000x600")

navbar = ctk.CTkFrame(root, width=200, fg_color="sky blue", corner_radius=0)
navbar.place(x=0, y=0, relheight=1)  

title_frame = ctk.CTkFrame(navbar, fg_color="sky blue", corner_radius=0)
title_frame.pack(fill="x", pady=20, padx=10)

title_label = ctk.CTkLabel(title_frame, text="Sistema Hidropónico", font=("Arial", 16, "bold"), 
                           text_color="white", fg_color="sky blue")
title_label.pack(side="left", padx=20)

options = ["Estado del sistema", "Sensores", "Control de actuadores", "Historial de datos", "Configuración"]
for option in options:
    button = ctk.CTkButton(navbar, text=option, fg_color="sky blue", hover_color="deep sky blue", 
                           font=("Arial", 14), corner_radius=5, width=180, height=40, anchor="w")  
    button.pack(pady=8, padx=10)  

content = ctk.CTkFrame(root, fg_color="white")
content.place(x=200, y=0, relwidth=1, relheight=1) 

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
)
show_navbar_button.place(x=10, y=10) 

iniciar_graficas(content)

root.mainloop()