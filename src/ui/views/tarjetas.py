import sys
import customtkinter as ctk
import mysql.connector

sys.path.append('C:\\Users\\Colibecas\\Desktop\\PI')
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

        return datos if datos else [["No hay datos disponibles.", "", "", "", ""]]

    except mysql.connector.Error as err:
        print(f"Error al conectar con la base de datos: {err}")
        return [["Error al conectar con la base de datos.", "", "", "", ""]]

def crear_tarjetas_alertas(contenedor):
    """Crea tarjetas para mostrar las alertas en la ventana dada."""
    datos = obtener_datos_db()
    
    for widget in contenedor.winfo_children():
        widget.destroy()
    
    for i, (id_alerta, tipo_alerta, descripcion, fecha_hora, estado) in enumerate(datos):
        tarjeta = ctk.CTkFrame(contenedor, fg_color="lightgray", corner_radius=10)
        tarjeta.grid(row=i // 2, column=i % 2, padx=10, pady=10, sticky="nsew")
        
        ctk.CTkLabel(tarjeta, text=f"ID: {id_alerta}", font=("Arial", 14, "bold")).pack(pady=2)
        ctk.CTkLabel(tarjeta, text=f"Tipo: {tipo_alerta}", font=("Arial", 12)).pack(pady=2)
        ctk.CTkLabel(tarjeta, text=f"Descripción: {descripcion}", font=("Arial", 12), wraplength=250).pack(pady=2)
        ctk.CTkLabel(tarjeta, text=f"Fecha: {fecha_hora}", font=("Arial", 12)).pack(pady=2)
        ctk.CTkLabel(tarjeta, text=f"Estado: {estado}", font=("Arial", 12)).pack(pady=2)

def cambiar_contenido(nombre):
    if nombre == "alertas":
        crear_tarjetas_alertas(contenedor_principal)
    else:
        for widget in contenedor_principal.winfo_children():
            widget.destroy()
        ctk.CTkLabel(contenedor_principal, text=f"Vista: {nombre}", font=("Arial", 18, "bold")).pack(pady=20)

root = ctk.CTk()
root.title("Sistema Hidropónico - Alertas")
root.geometry("900x600")

barra_nav = ctk.CTkFrame(root, fg_color="#2C3E50", width=200)
barra_nav.pack(side="left", fill="y")

botones = ["alertas", "configuración", "sensores", "reportes"]
for boton in botones:
    btn = ctk.CTkButton(barra_nav, text=boton.capitalize(), command=lambda b=boton: cambiar_contenido(b))
    btn.pack(pady=10, padx=10, fill="x")

contenedor_principal = ctk.CTkFrame(root)
contenedor_principal.pack(side="right", fill="both", expand=True, padx=20, pady=20)

cambiar_contenido("alertas")
root.mainloop()