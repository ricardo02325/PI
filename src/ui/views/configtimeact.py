import sys
import mysql.connector
import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime

# Añadir el path al proyecto si es necesario
sys.path.append('C:\\Users\\Colibecas\\Desktop\\PI')

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class ConfiguracionSistema(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Configuración del Sistema Hidropónico")
        self.geometry("1200x700")

        # Frame principal
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Título principal centrado con emoji de engranaje
        self.titulo_principal = ctk.CTkLabel(
            self.main_frame,
            text="⚙ CONFIGURACION GENERAL",
            font=("Arial", 24, "bold"),
            anchor="center"
        )
        self.titulo_principal.pack(fill="x", pady=(0, 20))

        # Contenedor para menú y contenido
        self.content_container = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.content_container.pack(fill="both", expand=True)

        # Menú lateral izquierdo mejorado
        self.menu_frame = ctk.CTkFrame(
            self.content_container, 
            width=280, 
            corner_radius=12,
            border_width=1
        )
        self.menu_frame.pack(side="left", fill="y", padx=(0, 20))
        
        # Título del menú
        self.menu_label = ctk.CTkLabel(
            self.menu_frame, 
            text="Configuración de Tiempos", 
            font=("Arial", 18, "bold"),
            pady=15
        )
        self.menu_label.pack(fill="x", padx=15)

        # Frame de opciones con mejor diseño
        self.opciones_frame = ctk.CTkFrame(
            self.menu_frame, 
            fg_color="transparent",
            border_width=0
        )
        self.opciones_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        # Opciones de configuración con mejor diseño
        self.opciones = {"Bomba 1": 0, "Bomba 2": 0, "Bomba 3": 0}
        for bomba in self.opciones:
            frame_opcion = ctk.CTkFrame(
                self.opciones_frame, 
                fg_color=("gray90", "gray20"),
                corner_radius=8
            )
            frame_opcion.pack(fill="x", pady=6)

            label = ctk.CTkLabel(
                frame_opcion, 
                text=bomba, 
                width=100, 
                anchor="w",
                font=("Arial", 14)
            )
            label.pack(side="left", padx=10, pady=8)
            
            entry = ctk.CTkEntry(
                frame_opcion, 
                width=100,
                placeholder_text="Segundos",
                justify="right"
            )
            entry.pack(side="right", padx=10, pady=8)
            self.opciones[bomba] = entry

        # Botón de guardar con mejor diseño
        save_button = ctk.CTkButton(
            self.opciones_frame, 
            text="Guardar Configuración", 
            command=self.guardar_cambios,
            corner_radius=8,
            height=40,
            font=("Arial", 14),
            fg_color=("#3A7EBF", "#1F538D"),
            hover_color=("#2D5F8B", "#14375F")
        )
        save_button.pack(pady=(10, 0), fill="x")

        # Sección de últimos datos ingresados
        self.ultimos_datos_frame = ctk.CTkFrame(
            self.menu_frame,
            fg_color="transparent",
            border_width=0
        )
        self.ultimos_datos_frame.pack(fill="x", padx=15, pady=(20, 15))

        # Título para la sección de últimos datos
        ctk.CTkLabel(
            self.ultimos_datos_frame,
            text="Últimos Tiempos Configurados",
            font=("Arial", 14, "bold")
        ).pack(anchor="w", pady=(0, 10))

        # Frame para los recuadros de últimos datos
        self.recuadros_frame = ctk.CTkFrame(
            self.ultimos_datos_frame,
            fg_color="transparent"
        )
        self.recuadros_frame.pack(fill="x")

        # Recuadros de últimos datos (inicialmente vacíos)
        self.recuadros_ultimos_datos = {}
        for i, bomba in enumerate(self.opciones.keys()):
            frame = ctk.CTkFrame(
                self.recuadros_frame,
                border_width=2,
                border_color="red",
                corner_radius=20,  # Bordes más ovalados
                fg_color="white"
            )
            frame.grid(row=0, column=i, padx=5, pady=5, sticky="nsew")
            self.recuadros_frame.grid_columnconfigure(i, weight=1)
            
            # Título de la bomba
            ctk.CTkLabel(
                frame,
                text=bomba,
                text_color="black",
                font=("Arial", 12, "bold")
            ).pack(pady=(8, 0))
            
            # Valor (inicialmente vacío)
            valor_label = ctk.CTkLabel(
                frame,
                text="N/A",
                text_color="black",
                font=("Arial", 14)
            )
            valor_label.pack(pady=(0, 8))
            
            self.recuadros_ultimos_datos[bomba] = valor_label

        # Contenedor derecho con scroll
        self.right_content = ctk.CTkFrame(
            self.content_container,
            fg_color="transparent"
        )
        self.right_content.pack(side="right", fill="both", expand=True)

        # Título "Bombas en uso"
        self.bombas_titulo = ctk.CTkLabel(
            self.right_content,
            text="BOMBA EXISTENTES: ",
            font=("Arial", 18, "bold"),
            anchor="w"
        )
        self.bombas_titulo.pack(fill="x", pady=(0, 15))

        # Frame scrollable para las bombas
        self.bombas_frame = ctk.CTkScrollableFrame(
            self.right_content, 
            fg_color="transparent"
        )
        self.bombas_frame.pack(fill="both", expand=True)

        # Cargar los actuadores desde la base de datos
        self.cargar_actuadores()
        # Cargar últimos tiempos configurados
        self.cargar_ultimos_tiempos()

    def cargar_ultimos_tiempos(self):
        """Carga los últimos tiempos configurados desde la base de datos"""
        db = self.conectar_db()
        if db:
            cursor = db.cursor(dictionary=True)
            try:
                for bomba in self.opciones.keys():
                    query = f"SELECT valor FROM configuracion_sistema WHERE parametro = '{bomba}' ORDER BY fecha_actualizacion DESC LIMIT 1"
                    cursor.execute(query)
                    resultado = cursor.fetchone()
                    if resultado:
                        self.recuadros_ultimos_datos[bomba].configure(text=f"{resultado['valor']} seg")
            except mysql.connector.Error as err:
                messagebox.showwarning("Advertencia", f"No se pudieron cargar los últimos tiempos: {err}")
            finally:
                db.close()

    def crear_recuadro_bomba(self, actuador):
        # Frame principal para cada bomba
        frame_bomba = ctk.CTkFrame(
            self.bombas_frame, 
            border_width=0, 
            corner_radius=10,
            fg_color=("gray95", "gray10"),
            height=80
        )
        frame_bomba.pack(pady=6, padx=5, fill="x")

        # Grid layout para organizar los elementos
        frame_bomba.grid_columnconfigure(0, weight=3)
        frame_bomba.grid_columnconfigure(1, weight=2)
        frame_bomba.grid_columnconfigure(2, weight=1)
        frame_bomba.grid_rowconfigure(0, weight=1)

        # Nombre de la bomba
        nombre_label = ctk.CTkLabel(
            frame_bomba, 
            text=actuador['tipo_actuador'],
            font=("Arial", 14, "bold"),
            anchor="w"
        )
        nombre_label.grid(row=0, column=0, padx=20, sticky="w")

        # Estado de la bomba
        estado_color = "#2ECC71" if actuador['estado'].lower() == "activo" else "#E74C3C"
        estado_text = f"Estado: {actuador['estado']}"
        estado_label = ctk.CTkLabel(
            frame_bomba, 
            text=estado_text,
            text_color=estado_color,
            font=("Arial", 12),
            anchor="w"
        )
        estado_label.grid(row=0, column=1, padx=15, sticky="w")

        # Botón de detalles en color azul
        toggle_button = ctk.CTkButton(
            frame_bomba, 
            text="Detalles", 
            width=90,
            height=30,
            corner_radius=6,
            font=("Arial", 12),
            fg_color=("#3A7EBF", "#1F538D"),
            hover_color=("#2D5F8B", "#14375F"),
            text_color="white"
        )
        toggle_button.grid(row=0, column=2, padx=15, sticky="e")
        toggle_button.configure(command=lambda a=actuador: self.toggle_info(a))

    def guardar_cambios(self):
        db = self.conectar_db()
        if db:
            cursor = db.cursor()
            try:
                for bomba, entry in self.opciones.items():
                    try:
                        valor = float(entry.get())
                        query = f"UPDATE configuracion_sistema SET valor = {valor}, fecha_actualizacion = NOW() WHERE parametro = '{bomba}'"
                        cursor.execute(query)
                        db.commit()
                        # Actualizar el recuadro correspondiente
                        self.recuadros_ultimos_datos[bomba].configure(text=f"{valor} seg")
                    except ValueError:
                        messagebox.showerror("Error", f"Valor inválido para {bomba}")
                        return
                
                messagebox.showinfo("Guardado", "Configuración actualizada correctamente.")
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"No se pudo guardar: {err}")
            finally:
                db.close()

    # Resto de los métodos se mantienen igual...
    def conectar_db(self):
        try:
            db = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="",
                database="sistema_hidroponico"
            )
            return db
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"No se pudo conectar a la base de datos: {err}")
            return None

    def cargar_actuadores(self):
        db = self.conectar_db()
        if db:
            cursor = db.cursor(dictionary=True)
            query = "SELECT * FROM actuadores"
            cursor.execute(query)
            actuadores = cursor.fetchall()
            db.close()
            for actuador in actuadores:
                self.crear_recuadro_bomba(actuador)

    def toggle_info(self, actuador):
        detalles = (
            f"Tipo: {actuador['tipo_actuador']}\n"
            f"Ubicación: {actuador['ubicacion']}\n"
            f"Fecha instalación: {actuador['fecha_instalacion']}\n"
            f"Estado: {actuador['estado']}"
        )
        messagebox.showinfo("Detalles del Actuador", detalles)

if __name__ == "__main__":
    app = ConfiguracionSistema()
    app.mainloop()