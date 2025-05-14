import sys
import mysql.connector
import customtkinter as ctk
from datetime import datetime

# Añadir el path al proyecto si es necesario
sys.path.append('C:\\Users\\Colibecas\\Desktop\\PI')

class Modal(ctk.CTkToplevel):
    def __init__(self, parent, title, message, width=400, height=200):
        super().__init__(parent)
        self.title(title)
        self.geometry(f"{width}x{height}")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        
        # Centrar el modal respecto a la ventana principal
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (width // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (height // 2)
        self.geometry(f"+{x}+{y}")
        
        # Frame principal
        self.main_frame = ctk.CTkFrame(self, corner_radius=12)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Título
        ctk.CTkLabel(
            self.main_frame, 
            text=title,
            font=("Arial", 18, "bold"),
            anchor="center"
        ).pack(pady=(15, 10), padx=20, fill="x")
        
        # Mensaje
        ctk.CTkLabel(
            self.main_frame, 
            text=message,
            font=("Arial", 14),
            wraplength=width-40,
            justify="left"
        ).pack(pady=(0, 20), padx=20, fill="x")
        
        # Botón de cerrar
        ctk.CTkButton(
            self.main_frame,
            text="Cerrar",
            command=self.destroy,
            font=("Arial", 14),
            height=40,
            fg_color=("#3A7EBF", "#1F538D"),
            hover_color=("#2D5F8B", "#14375F")
        ).pack(pady=(0, 15), padx=20, fill="x")

class ConfiguracionSistema(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Variable para controlar si ya existe un modal abierto
        self.modal_abierto = False

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

        # Inicializar opciones vacías (se llenarán con datos de la BD)
        self.opciones = {}
        self.bombas_data = {}  # Para almacenar datos de las bombas

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

        # Contenedor derecho con scroll
        self.right_content = ctk.CTkFrame(
            self.content_container,
            fg_color="transparent"
        )
        self.right_content.pack(side="right", fill="both", expand=True)

        # Título "Bombas en uso"
        self.bombas_titulo = ctk.CTkLabel(
            self.right_content,
            text="BOMBAS EXISTENTES: ",
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
        # Cargar configuración de tiempos
        self.cargar_configuracion_tiempos()

    def cargar_configuracion_tiempos(self):
        """Carga las bombas existentes y sus tiempos de configuración"""
        db = self.conectar_db()
        if db:
            cursor = db.cursor(dictionary=True)
            try:
                # Limpiar frames existentes
                for widget in self.opciones_frame.winfo_children():
                    widget.destroy()
                
                for widget in self.recuadros_frame.winfo_children():
                    widget.destroy()
                
                self.opciones = {}
                self.recuadros_ultimos_datos = {}
                
                # Obtener todas las bombas de la tabla actuadores
                query = "SELECT * FROM actuadores WHERE tipo_actuador LIKE '%bomba%' OR tipo_actuador LIKE '%Bomba%'"
                cursor.execute(query)
                bombas = cursor.fetchall()
                
                if not bombas:
                    label = ctk.CTkLabel(
                        self.opciones_frame,
                        text="No se encontraron bombas en la base de datos",
                        text_color="gray"
                    )
                    label.pack(pady=20)
                    return
                
        
                for i, bomba in enumerate(bombas):
                    # Guardar datos de la bomba
                    self.bombas_data[bomba['id_actuador']] = bomba
                    
                
                    frame_opcion = ctk.CTkFrame(
                        self.opciones_frame, 
                        fg_color=("gray90", "gray20"),
                        corner_radius=8
                    )
                    frame_opcion.pack(fill="x", pady=6)

                    # Nombre de la bomba
                    label = ctk.CTkLabel(
                        frame_opcion, 
                        text=bomba['tipo_actuador'], 
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
                
                    if bomba['tencendido'] is not None:
                        entry.insert(0, str(bomba['tencendido']))
                    entry.pack(side="right", padx=10, pady=8)
                    self.opciones[bomba['id_actuador']] = entry
                    
                    
                    frame_recuadro = ctk.CTkFrame(
                        self.recuadros_frame,
                        width=200,
                        border_width=2,
                        border_color="#3A7EBF",
                        corner_radius=16,
                        fg_color=("#EAF2FB", "#1C1F26")
                    )


                    frame_recuadro.grid(row=0, column=i, padx=5, pady=5, sticky="nsew")
                    self.recuadros_frame.grid_columnconfigure(i, weight=1)
                    
            
                    ctk.CTkLabel(
                        frame_recuadro,
                        text=bomba['tipo_actuador'],
                        text_color="black",
                        font=("Arial", 8, "bold")
                    ).pack(pady=(8, 0))

                    valor_label = ctk.CTkLabel(
                        frame_recuadro,
                        text=f"{bomba['tencendido']} seg" if bomba['tencendido'] is not None else "N/A",
                        text_color="black",
                        font=("Arial", 12)  # Antes era 14
                    )
                    valor_label.pack(pady=(0, 8))

                    
                    self.recuadros_ultimos_datos[bomba['id_actuador']] = valor_label

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

            except mysql.connector.Error as err:
                if not self.modal_abierto:
                    self.modal_abierto = True
                    Modal(self.parent, "Error", f"No se pudieron cargar los tiempos: {err}")
                    self.modal_abierto = False
            finally:
                db.close()

    def crear_recuadro_bomba(self, actuador):

        frame_bomba = ctk.CTkFrame(
            self.bombas_frame, 
            border_width=0, 
            corner_radius=10,
            fg_color=("gray95", "gray10"),
            height=200000
        )
        frame_bomba.pack(pady=6, padx=5, fill="x")

        
        frame_bomba.grid_columnconfigure(0, weight=3)
        frame_bomba.grid_columnconfigure(1, weight=2)
        frame_bomba.grid_columnconfigure(2, weight=1)
        frame_bomba.grid_rowconfigure(0, weight=1)

        
        nombre_label = ctk.CTkLabel(
            frame_bomba, 
            text=actuador['tipo_actuador'],
            font=("Arial", 14, "bold"),
            anchor="w"
        )
        nombre_label.grid(row=0, column=0, padx=20, sticky="w")

    
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
        toggle_button.configure(command=lambda a=actuador: self.mostrar_detalles_actuador(a))

    def guardar_cambios(self):
        if self.modal_abierto:
            return
            
        db = self.conectar_db()
        if db:
            cursor = db.cursor()
            try:
                for id_actuador, entry in self.opciones.items():
                    try:
                        valor = float(entry.get()) if entry.get() else None
                        query = "UPDATE actuadores SET tencendido = %s WHERE id_actuador = %s"
                        cursor.execute(query, (valor, id_actuador))
                        db.commit()
                        
                        # Actualizar el recuadro corresp
                        if id_actuador in self.recuadros_ultimos_datos:
                            texto = f"{valor} seg" if valor is not None else "N/A"
                            self.recuadros_ultimos_datos[id_actuador].configure(text=texto)
                    except ValueError:
                        if not self.modal_abierto:
                            self.modal_abierto = True
                            Modal(self.parent, "Error", f"Valor inválido para {self.bombas_data[id_actuador]['tipo_actuador']}")
                            self.modal_abierto = False
                        return
                
                self.modal_abierto = True
                Modal(self.parent, "Éxito", "Configuración actualizada correctamente")
                self.modal_abierto = False
                
            except mysql.connector.Error as err:
                if not self.modal_abierto:
                    self.modal_abierto = True
                    Modal(self.parent, "Error", f"No se pudo guardar: {err}")
                    self.modal_abierto = False
            finally:
                db.close()

    def mostrar_detalles_actuador(self, actuador):
        if self.modal_abierto:
            return
            
        detalles = (
            f"Tipo: {actuador['tipo_actuador']}\n"
            f"Ubicación: {actuador['ubicacion']}\n"
            f"Fecha instalación: {actuador['fecha_instalacion']}\n"
            f"Estado: {actuador['estado']}\n"
            f"Tiempo encendido: {actuador['tencendido'] if actuador['tencendido'] is not None else 'N/A'} seg"
        )
        
        self.modal_abierto = True
        modal = Modal(self.parent, f"Detalles: {actuador['tipo_actuador']}", detalles)
        # Configurar para que al cerrar el modal se resetee la variable
        modal.protocol("WM_DELETE_WINDOW", lambda: self.cerrar_modal(modal))

    def cerrar_modal(self, modal):
        modal.destroy()
        self.modal_abierto = False

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
            if not self.modal_abierto:
                self.modal_abierto = True
                Modal(self.parent, "Error", f"No se pudo conectar a la base de datos: {err}")
                self.modal_abierto = False
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

def crear_configuracion_sistema(parent):
    """Función para crear e integrar el módulo de configuración del sistema en la interfaz principal"""
    config_frame = ConfiguracionSistema(parent)
    config_frame.pack(fill="both", expand=True)
    return config_frame