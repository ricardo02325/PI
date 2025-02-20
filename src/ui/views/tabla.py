import tkinter as tk
from tkinter import ttk

def crear_ventana():
    ventana = tk.Tk()
    ventana.title("Tabla en una Ventana")
    ventana.geometry("500x300")
    
    # Crear un Treeview (tabla)
    columnas = ("ID", "Nombre", "Edad")
    tabla = ttk.Treeview(ventana, columns=columnas, show="headings")
    
    # Configurar encabezados
    tabla.heading("ID", text="ID")
    tabla.heading("Nombre", text="Nombre")
    tabla.heading("Edad", text="Edad")
    
    # Insertar datos de ejemplo
    datos = [(1, "Ana", 25), (2, "Luis", 30), (3, "María", 22)]
    for fila in datos:
        tabla.insert("", tk.END, values=fila)
    
    tabla.pack(expand=True, fill="both")
    
    ventana.mainloop()

crear_ventana()