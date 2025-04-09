import customtkinter as ctk
import mysql.connector
from mysql.connector import Error
from datetime import date
from tkinter import ttk, messagebox

class MantenimientoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Mantenimiento Hidropónico")
        self.root.geometry("1000x700")
        self.root.configure(bg="white")
        
        # Configuración de estilo
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        # Conectar a la base de datos
        self.connection = self.connect_to_database()
        
        # Crear widgets
        self.create_widgets()
        
        # Cargar datos iniciales
        self.load_mantenimientos()
        self.load_usuarios()
    
    def connect_to_database(self):
        try:
            connection = mysql.connector.connect(
                host='localhost',
                database='sistema_hidroponico',
                user='root',
                password=''  # Agrega tu contraseña si es necesaria
            )
            return connection
        except Error as e:
            messagebox.showerror("Error", f"No se pudo conectar a la base de datos: {e}")
            return None
    
    def create_widgets(self):
        # Frame principal
        self.main_frame = ctk.CTkFrame(self.root, fg_color="white")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        self.title_label = ctk.CTkLabel(
            self.main_frame, 
            text="Gestión de Mantenimientos",
            font=("Helvetica", 20, "bold"),
            text_color="#2A8C55"
        )
        self.title_label.pack(pady=(0, 20))
        
        # Frame de formulario
        self.form_frame = ctk.CTkFrame(
            self.main_frame, 
            fg_color="#F5F5F5",
            border_width=1,
            border_color="#E0E0E0",
            corner_radius=10
        )
        self.form_frame.pack(fill="x", padx=10, pady=(0, 20), ipady=10)
        
        # Campos del formulario
        self.create_form_fields()
        
        # Frame de la tabla
        self.table_frame = ctk.CTkFrame(
            self.main_frame, 
            fg_color="white",
            border_width=1,
            border_color="#E0E0E0",
            corner_radius=10
        )
        self.table_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Tabla de mantenimientos
        self.create_mantenimientos_table()
    
    def create_form_fields(self):
        # Usuario
        self.usuario_label = ctk.CTkLabel(
            self.form_frame, 
            text="Usuario:",
            font=("Helvetica", 12)
        )
        self.usuario_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        self.usuario_combobox = ctk.CTkComboBox(
            self.form_frame,
            values=[],
            font=("Helvetica", 12),
            dropdown_font=("Helvetica", 12),
            state="readonly"
        )
        self.usuario_combobox.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        
        # Fecha
        self.fecha_label = ctk.CTkLabel(
            self.form_frame, 
            text="Fecha:",
            font=("Helvetica", 12)
        )
        self.fecha_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        
        today = date.today().strftime("%Y-%m-%d")
        self.fecha_entry = ctk.CTkEntry(
            self.form_frame,
            font=("Helvetica", 12),
            placeholder_text=today
        )
        self.fecha_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        
        # Descripción
        self.descripcion_label = ctk.CTkLabel(
            self.form_frame, 
            text="Descripción:",
            font=("Helvetica", 12)
        )
        self.descripcion_label.grid(row=2, column=0, padx=10, pady=5, sticky="nw")
        
        self.descripcion_text = ctk.CTkTextbox(
            self.form_frame,
            font=("Helvetica", 12),
            height=80,
            wrap="word"
        )
        self.descripcion_text.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        
        # Estado
        self.estado_label = ctk.CTkLabel(
            self.form_frame, 
            text="Estado:",
            font=("Helvetica", 12)
        )
        self.estado_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        
        self.estado_combobox = ctk.CTkComboBox(
            self.form_frame,
            values=["Pendiente", "En progreso", "Completado", "Cancelado"],
            font=("Helvetica", 12),
            dropdown_font=("Helvetica", 12)
        )
        self.estado_combobox.grid(row=3, column=1, padx=10, pady=5, sticky="ew")
        
        # Botón de guardar
        self.guardar_button = ctk.CTkButton(
            self.form_frame,
            text="Guardar Mantenimiento",
            command=self.save_mantenimiento,
            font=("Helvetica", 12, "bold"),
            fg_color="#2A8C55",
            hover_color="#207244"
        )
        self.guardar_button.grid(row=4, column=0, columnspan=2, pady=10, sticky="ew")
        
        # Configurar grid
        self.form_frame.grid_columnconfigure(1, weight=1)
    
    def create_mantenimientos_table(self):
        # Crear Treeview con estilo
        style = ttk.Style()
        style.theme_use("default")
        
        # Configurar estilo
        style.configure("Treeview", 
                       background="#FFFFFF",
                       foreground="black",
                       rowheight=25,
                       fieldbackground="#FFFFFF",
                       bordercolor="#E0E0E0",
                       borderwidth=1)
        style.map('Treeview', background=[('selected', '#2A8C55')])
        
        style.configure("Treeview.Heading", 
                        background="#2A8C55",
                        foreground="white",
                        font=('Helvetica', 12, 'bold'))
        
        # Crear el Treeview
        self.tree = ttk.Treeview(
            self.table_frame,
            columns=("id", "usuario", "fecha", "descripcion", "estado"),
            show="headings",
            style="Treeview"
        )
        
        # Configurar columnas
        self.tree.heading("id", text="ID")
        self.tree.heading("usuario", text="Usuario")
        self.tree.heading("fecha", text="Fecha")
        self.tree.heading("descripcion", text="Descripción")
        self.tree.heading("estado", text="Estado")
        
        self.tree.column("id", width=50, anchor="center")
        self.tree.column("usuario", width=150, anchor="w")
        self.tree.column("fecha", width=100, anchor="center")
        self.tree.column("descripcion", width=400, anchor="w")
        self.tree.column("estado", width=100, anchor="center")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Empaquetar
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Doble click para editar
        self.tree.bind("<Double-1>", self.edit_mantenimiento)
    
    def load_usuarios(self):
        if not self.connection:
            return
            
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT id_usuario, nombre FROM usuarios")
            usuarios = cursor.fetchall()
            
            # Formatear como "ID - Nombre"
            usuarios_formatted = [f"{u[0]} - {u[1]}" for u in usuarios]
            self.usuario_combobox.configure(values=usuarios_formatted)
            
            if usuarios_formatted:
                self.usuario_combobox.set(usuarios_formatted[0])
            
        except Error as e:
            messagebox.showerror("Error", f"Error al cargar usuarios: {e}")
    
    def load_mantenimientos(self):
        if not self.connection:
            return
            
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = """
            SELECT m.id_mantenimiento, m.fecha_mantenimiento, m.descripcion, m.estado_tarea, 
                   u.id_usuario, u.nombre
            FROM mantenimiento m
            JOIN usuarios u ON m.id_usuario = u.id_usuario
            ORDER BY m.fecha_mantenimiento DESC
            """
            cursor.execute(query)
            mantenimientos = cursor.fetchall()
            
            # Limpiar tabla
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Insertar datos
            for m in mantenimientos:
                self.tree.insert("", "end", 
                                values=(m["id_mantenimiento"],
                                       f"{m['id_usuario']} - {m['nombre']}",
                                       m["fecha_mantenimiento"],
                                       m["descripcion"],
                                       m["estado_tarea"]))
            
        except Error as e:
            messagebox.showerror("Error", f"Error al cargar mantenimientos: {e}")
    
    def save_mantenimiento(self):
        if not self.connection:
            return
            
        # Obtener datos del formulario
        usuario = self.usuario_combobox.get().split(" - ")[0]
        fecha = self.fecha_entry.get() or date.today().strftime("%Y-%m-%d")
        descripcion = self.descripcion_text.get("1.0", "end-1c")
        estado = self.estado_combobox.get()
        
        if not descripcion:
            messagebox.showwarning("Advertencia", "Por favor ingrese una descripción")
            return
            
        try:
            cursor = self.connection.cursor()
            query = """
            INSERT INTO mantenimiento (id_usuario, fecha_mantenimiento, descripcion, estado_tarea)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (usuario, fecha, descripcion, estado))
            self.connection.commit()
            
            messagebox.showinfo("Éxito", "Mantenimiento guardado correctamente")
            
            # Limpiar formulario
            self.descripcion_text.delete("1.0", "end")
            self.estado_combobox.set("Pendiente")
            
            # Recargar datos
            self.load_mantenimientos()
            
        except Error as e:
            messagebox.showerror("Error", f"Error al guardar mantenimiento: {e}")
    
    def edit_mantenimiento(self, event):
        # Obtener item seleccionado
        selected_item = self.tree.selection()
        if not selected_item:
            return
            
        item_data = self.tree.item(selected_item)
        values = item_data["values"]
        
        # Crear ventana de edición
        edit_window = ctk.CTkToplevel(self.root)
        edit_window.title("Editar Mantenimiento")
        edit_window.geometry("500x400")
        edit_window.grab_set()
        
        # ID (no editable)
        ctk.CTkLabel(edit_window, text="ID:").pack(pady=(10, 0))
        id_entry = ctk.CTkEntry(edit_window, state="readonly")
        id_entry.pack(fill="x", padx=20)
        id_entry.configure(state="normal")
        id_entry.insert(0, values[0])
        id_entry.configure(state="readonly")
        
        # Usuario (no editable)
        ctk.CTkLabel(edit_window, text="Usuario:").pack(pady=(10, 0))
        usuario_entry = ctk.CTkEntry(edit_window, state="readonly")
        usuario_entry.pack(fill="x", padx=20)
        usuario_entry.insert(0, values[1])
        
        # Fecha
        ctk.CTkLabel(edit_window, text="Fecha:").pack(pady=(10, 0))
        fecha_entry = ctk.CTkEntry(edit_window)
        fecha_entry.pack(fill="x", padx=20)
        fecha_entry.insert(0, values[2])
        
        # Descripción
        ctk.CTkLabel(edit_window, text="Descripción:").pack(pady=(10, 0))
        descripcion_text = ctk.CTkTextbox(edit_window, height=100)
        descripcion_text.pack(fill="x", padx=20, pady=(0, 10))
        descripcion_text.insert("1.0", values[3])
        
        # Estado
        ctk.CTkLabel(edit_window, text="Estado:").pack(pady=(10, 0))
        estado_combobox = ctk.CTkComboBox(
            edit_window,
            values=["Pendiente", "En progreso", "Completado", "Cancelado"]
        )
        estado_combobox.pack(fill="x", padx=20, pady=(0, 10))
        estado_combobox.set(values[4])
        
        # Botón de guardar
        def update_mantenimiento():
            try:
                cursor = self.connection.cursor()
                query = """
                UPDATE mantenimiento 
                SET fecha_mantenimiento = %s, 
                    descripcion = %s, 
                    estado_tarea = %s
                WHERE id_mantenimiento = %s
                """
                cursor.execute(query, (
                    fecha_entry.get(),
                    descripcion_text.get("1.0", "end-1c"),
                    estado_combobox.get(),
                    values[0]
                ))
                self.connection.commit()
                
                messagebox.showinfo("Éxito", "Mantenimiento actualizado correctamente")
                edit_window.destroy()
                self.load_mantenimientos()
                
            except Error as e:
                messagebox.showerror("Error", f"Error al actualizar mantenimiento: {e}")
        
        save_button = ctk.CTkButton(
            edit_window,
            text="Guardar Cambios",
            command=update_mantenimiento,
            fg_color="#2A8C55",
            hover_color="#207244"
        )
        save_button.pack(pady=10)
    
    def __del__(self):
        if hasattr(self, 'connection') and self.connection:
            self.connection.close()

if __name__ == "__main__":
    root = ctk.CTk()
    app = MantenimientoApp(root)
    root.mainloop()