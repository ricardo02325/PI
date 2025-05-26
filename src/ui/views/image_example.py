import customtkinter
import os
from PIL import Image, ImageTk
import hashlib
import mysql.connector
from tkinter import messagebox
import threading
import time
import uuid
from Graficas_sensores import iniciar_graficas
from alertas import iniciar_alertas
from Actuadoresbtn import crear_interfaz_actuadores
from configtimeact import crear_configuracion_sistema
from notificaciones import Notificador
from src.models.models import obtener_alertas_completas

class LoadingAnimation(customtkinter.CTkFrame):
    def __init__(self, parent, message):
        super().__init__(parent, fg_color="transparent")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Frame de carga centrado
        self.loading_frame = customtkinter.CTkFrame(self, corner_radius=10)
        self.loading_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        
        # Mensaje
        self.message_label = customtkinter.CTkLabel(
            self.loading_frame, 
            text=message,
            font=customtkinter.CTkFont(size=16, weight="bold")
        )
        self.message_label.pack(pady=(20, 10), padx=20)
        
        # Cargar GIF de loading con tamaño aumentado
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images", "loading.gif")
        try:
            self.gif = Image.open(image_path)
            
            # Tamaño del GIF (ajustar según necesidad)
            self.gif_size = (300, 200)
            
            # Preparar los frames del GIF
            self.frames = []
            try:
                for i in range(0, self.gif.n_frames):
                    self.gif.seek(i)
                    frame = self.gif.copy()
                    frame = frame.resize(self.gif_size, Image.LANCZOS)
                    frame = customtkinter.CTkImage(
                        light_image=frame,
                        dark_image=frame,
                        size=self.gif_size
                    )
                    self.frames.append(frame)
            except EOFError:
                pass
            
            # Label para mostrar el GIF
            self.gif_label = customtkinter.CTkLabel(self.loading_frame, text="", image=self.frames[0])
            self.gif_label.pack(pady=(0, 20))
            
            # Iniciar animación
            self.current_frame = 0
            self.animate()
            
        except FileNotFoundError:
            # Si no hay GIF, mostrar un spinner simple
            self.fallback_loading()

    def fallback_loading(self):
        """Mostrar un spinner simple si no se encuentra el GIF"""
        self.loading_label = customtkinter.CTkLabel(
            self.loading_frame, 
            text="Cargando...", 
            font=customtkinter.CTkFont(size=14)
        )
        self.loading_label.pack(pady=20)
    
    def animate(self):
        """Anima el GIF"""
        if hasattr(self, 'frames') and self.frames:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.gif_label.configure(image=self.frames[self.current_frame])
            self.after(50, self.animate)

class LoginFrame(customtkinter.CTkFrame):
    def __init__(self, parent, on_login_success):
        super().__init__(parent)
        self.on_login_success = on_login_success
        self.parent = parent
        
        # Configuración de la conexión a la base de datos
        self.db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="sistema_hidroponico"
        )
        
        # Cargar imagen de fondo
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")
        try:
            self.background_image = Image.open(os.path.join(image_path, "fondo.jpg"))
            self.bg_image = customtkinter.CTkImage(
                light_image=self.background_image,
                dark_image=self.background_image,
                size=(self.winfo_screenwidth(), self.winfo_screenheight())
            )
            self.bg_label = customtkinter.CTkLabel(self, image=self.bg_image, text="")
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except FileNotFoundError:
            print("No se encontró la imagen de fondo")
            self.configure(fg_color=("#f5f7fa", "#1a1a1a"))  # Fondo alternativo

        # Configurar fuente moderna
        try:
            self.title_font = customtkinter.CTkFont(family="Montserrat", size=28, weight="bold")
            self.welcome_font = customtkinter.CTkFont(family="Montserrat", size=20, weight="bold")
            self.input_font = customtkinter.CTkFont(family="Montserrat", size=14)
            self.button_font = customtkinter.CTkFont(family="Montserrat", size=16, weight="bold")
        except:
            # Fallback si Montserrat no está instalado
            self.title_font = customtkinter.CTkFont(size=28, weight="bold")
            self.welcome_font = customtkinter.CTkFont(size=20, weight="bold")
            self.input_font = customtkinter.CTkFont(size=14)
            self.button_font = customtkinter.CTkFont(size=16, weight="bold")

        # Frame principal con transparencia
        self.main_frame = customtkinter.CTkFrame(
            self, 
            fg_color=("white", "gray20"),  # Fondo semitransparente
            border_width=0,
            corner_radius=15,
            bg_color="transparent"
        )
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Logo o imagen decorativa
        try:
            self.logo_image = customtkinter.CTkImage(
                light_image=Image.open(os.path.join(image_path, "Arbol.png")),
                dark_image=Image.open(os.path.join(image_path, "Arbol.png")),
                size=(180, 180)
            )
            self.logo_label = customtkinter.CTkLabel(
                self.main_frame, 
                text="", 
                image=self.logo_image,
                compound="top"
            )
            self.logo_label.grid(row=0, column=0, columnspan=2, pady=(30, 10), padx=40)
        except FileNotFoundError:
            pass

        # Texto de bienvenida con estilo moderno
        self.welcome_label = customtkinter.CTkLabel(
            self.main_frame,
            text="BIENVENIDO",
            font=self.welcome_font,
            text_color=("#3a7ebf", "#1f538d"),
            justify="center"
        )
        self.welcome_label.grid(row=1, column=0, columnspan=2, pady=(0, 5), padx=40)
        
        # Subtítulo
        self.subtitle_label = customtkinter.CTkLabel(
            self.main_frame,
            text="Por favor ingrese sus credenciales",
            font=self.input_font,
            text_color=("#6c757d", "#adb5bd"),
            justify="center"
        )
        self.subtitle_label.grid(row=2, column=0, columnspan=2, pady=(0, 30), padx=40)
        
        # Título principal del sistema
        self.title_label = customtkinter.CTkLabel(
            self.main_frame,
            text="SISTEMA HIDROPÓNICO",
            font=self.title_font,
            text_color=("#2b2b2b", "white"),
            justify="center"
        )
        self.title_label.grid(row=3, column=0, columnspan=2, pady=(0, 40), padx=40)
        
        # Notebook (pestañas) con estilo moderno y transparencia
        self.notebook = customtkinter.CTkTabview(
            self.main_frame,
            width=400,
            segmented_button_fg_color=("gray90", "gray20"),
            segmented_button_selected_color=("#3a7ebf", "#1f538d"),
            segmented_button_selected_hover_color=("#3a7ebf", "#1f538d"),
            segmented_button_unselected_hover_color=("gray80", "gray30"),
            text_color=("gray10", "gray90"),
            corner_radius=10,
            fg_color=("white", "gray20")
        )
        self.notebook.grid(row=4, column=0, columnspan=2, pady=(0, 30), padx=40)
        
        # [El resto del código de las pestañas y campos de entrada permanece igual...]
        # Solo asegúrate de usar self.input_font para los CTkEntry y self.button_font para los CTkButton
        
        # Pestaña de Login
        self.login_tab = self.notebook.add("INICIAR SESIÓN")
        self.notebook.set("INICIAR SESIÓN")
        
        # Pestaña de Registro
        self.register_tab = self.notebook.add("REGISTRARSE")
        
        # Configurar grid para las pestañas
        for tab in [self.login_tab, self.register_tab]:
            tab.grid_columnconfigure(0, weight=1)
            tab.grid_rowconfigure((0, 1, 2, 3), weight=1)
        
        # Widgets para Login
        self.email_login = customtkinter.CTkEntry(
            self.login_tab, 
            placeholder_text="Correo electrónico",
            width=300,
            height=40,
            corner_radius=10,
            font=customtkinter.CTkFont(size=14)
        )
        self.email_login.grid(row=0, column=0, padx=20, pady=10)
        
        self.password_login = customtkinter.CTkEntry(
            self.login_tab, 
            placeholder_text="Contraseña", 
            show="*",
            width=300,
            height=40,
            corner_radius=10,
            font=customtkinter.CTkFont(size=14)
        )
        self.password_login.grid(row=1, column=0, padx=20, pady=10)
        
        self.login_button = customtkinter.CTkButton(
            self.login_tab, 
            text="INGRESAR", 
            command=self.login,
            width=300,
            height=40,
            corner_radius=10,
            font=customtkinter.CTkFont(size=14, weight="bold"),
            fg_color=("#3a7ebf", "#1f538d"),
            hover_color=("#2d6ba3", "#184477"),
            text_color=("white", "white")
        )
        self.login_button.grid(row=2, column=0, padx=20, pady=20)
        
        # Widgets para Registro
        self.nombre_registro = customtkinter.CTkEntry(
            self.register_tab, 
            placeholder_text="Nombre completo",
            width=300,
            height=40,
            corner_radius=10,
            font=customtkinter.CTkFont(size=14)
        )
        self.nombre_registro.grid(row=0, column=0, padx=20, pady=10)
        
        self.email_registro = customtkinter.CTkEntry(
            self.register_tab, 
            placeholder_text="Correo electrónico",
            width=300,
            height=40,
            corner_radius=10,
            font=customtkinter.CTkFont(size=14)
        )
        self.email_registro.grid(row=1, column=0, padx=20, pady=10)
        
        self.password_registro = customtkinter.CTkEntry(
            self.register_tab, 
            placeholder_text="Contraseña", 
            show="*",
            width=300,
            height=40,
            corner_radius=10,
            font=customtkinter.CTkFont(size=14)
        )
        self.password_registro.grid(row=2, column=0, padx=20, pady=10)
        
        self.register_button = customtkinter.CTkButton(
            self.register_tab, 
            text="REGISTRARSE", 
            command=self.register,
            width=300,
            height=40,
            corner_radius=10,
            font=customtkinter.CTkFont(size=14, weight="bold"),
            fg_color=("#3a7ebf", "#1f538d"),
            hover_color=("#2d6ba3", "#184477"),
            text_color=("white", "white")
        )
        self.register_button.grid(row=3, column=0, padx=20, pady=20)
        
        # Frame para animación de carga (inicialmente oculto)
        self.loading_frame = None
    
    def show_loading(self, message):
        """Muestra la animación de carga"""
        if self.loading_frame:
            self.loading_frame.destroy()
        
        self.loading_frame = LoadingAnimation(self, message)
        self.loading_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.update()
    
    def hide_loading(self):
        """Oculta la animación de carga"""
        if self.loading_frame:
            self.loading_frame.destroy()
            self.loading_frame = None
        self.update()
    
    def hash_password(self, password):
        """Hashea la contraseña usando SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def generate_session_token(self):
        """Genera un token de sesión único"""
        return str(uuid.uuid4())
    
    def update_session_token(self, user_id, token):
        """Actualiza el token de sesión en la base de datos"""
        try:
            cursor = self.db_connection.cursor()
            query = "UPDATE usuarios SET token_sesion = %s WHERE id_usuario = %s"
            cursor.execute(query, (token, user_id))
            self.db_connection.commit()
        except Exception as e:
            print(f"Error al actualizar token de sesión: {str(e)}")
        finally:
            cursor.close()
    
    def login(self):
        email = self.email_login.get()
        password = self.password_login.get()
        
        if not email or not password:
            messagebox.showerror("Error", "Por favor complete todos los campos")
            return
        
        # Mostrar animación de carga
        self.show_loading("Iniciando Sesión...")
        
        # Ejecutar en un hilo para no bloquear la interfaz
        threading.Thread(target=self._perform_login, args=(email, password), daemon=True).start()
    
    def _perform_login(self, email, password):
        try:
            cursor = self.db_connection.cursor(dictionary=True)
            query = "SELECT * FROM usuarios WHERE email = %s AND contrasena = %s"
            hashed_password = self.hash_password(password)
            cursor.execute(query, (email, hashed_password))
            user = cursor.fetchone()
            
            if user:
                # Generar y guardar token de sesión
                token = self.generate_session_token()
                self.update_session_token(user['id_usuario'], token)
                user['token_sesion'] = token
                
                # Simular tiempo de carga
                time.sleep(2)
                self.after(0, lambda: self.on_login_success(user))
            else:
                self.after(0, lambda: messagebox.showerror("Error", "Credenciales incorrectas"))
        except Exception as e:
            self.after(0, lambda: messagebox.showerror("Error", f"Error al conectar con la base de datos: {str(e)}"))
        finally:
            cursor.close()
            self.after(0, self.hide_loading)
    
    def register(self):
        nombre = self.nombre_registro.get()
        email = self.email_registro.get()
        password = self.password_registro.get()
        
        if not nombre or not email or not password:
            messagebox.showerror("Error", "Por favor complete todos los campos")
            return
        
        # Mostrar animación de carga
        self.show_loading("Registrando usuario...")
        
        # Ejecutar en un hilo para no bloquear la interfaz
        threading.Thread(target=self._perform_register, args=(nombre, email, password), daemon=True).start()
    
    def _perform_register(self, nombre, email, password):
        try:
            cursor = self.db_connection.cursor()
            
            # Verificar si el email ya existe
            cursor.execute("SELECT email FROM usuarios WHERE email = %s", (email,))
            if cursor.fetchone():
                self.after(0, lambda: messagebox.showerror("Error", "El email ya está registrado"))
                return
            
            # Insertar nuevo usuario
            hashed_password = self.hash_password(password)
            insert_query = """
                INSERT INTO usuarios (nombre_completo, email, contrasena, rol, fecha_registro)
                VALUES (%s, %s, %s, 'Usuario', CURDATE())
            """
            cursor.execute(insert_query, (nombre, email, hashed_password))
            self.db_connection.commit()
            
            # Simular tiempo de carga
            time.sleep(2)
            
            self.after(0, lambda: messagebox.showinfo("Éxito", "Registro exitoso. Ahora puede iniciar sesión."))
            self.after(0, lambda: self.notebook.set("INICIAR SESIÓN"))
            self.after(0, lambda: self.email_login.delete(0, 'end'))
            self.after(0, lambda: self.password_login.delete(0, 'end'))
            self.after(0, lambda: self.email_login.focus_set())
            
        except Exception as e:
            self.after(0, lambda: messagebox.showerror("Error", f"Error al registrar usuario: {str(e)}"))
        finally:
            cursor.close()
            self.after(0, self.hide_loading)

class MainFrame(customtkinter.CTkFrame):
    def __init__(self, parent, user, on_logout):
        super().__init__(parent)
        self.user = user
        self.on_logout = on_logout
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # Variables de control
        self.graficas_mostradas = False
        self.alertas_mostradas = False
        self.bombas_config_mostrada = False
        
        # Inicializar interfaz
        self.initialize_interface()
        
        # Iniciar sistema de notificaciones
        self.notificador = Notificador(self)
        self.ids_alertas_vistas = set()
        
        # Iniciar verificación periódica de notificaciones
        self.after(20000, self.comprobar_notificaciones)
    
    def initialize_interface(self):
        """Inicializa la interfaz principal"""
        icon_size = (48, 48)
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")

        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "CustomTkinter_logo_single.png")).resize(icon_size, Image.LANCZOS))
        self.small_logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "CustomTkinter_logo_single.png")).resize((24, 24), Image.LANCZOS))

        self.home_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "home.png")).resize(icon_size, Image.LANCZOS),
            dark_image=Image.open(os.path.join(image_path, "home_light.png")).resize(icon_size, Image.LANCZOS),
            size=icon_size
        )

        self.alerts_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "alert.png")).resize(icon_size, Image.LANCZOS),
            dark_image=Image.open(os.path.join(image_path, "chat_light.png")).resize(icon_size, Image.LANCZOS),
            size=icon_size
        )

        self.actuators_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "actuadores.png")).resize(icon_size, Image.LANCZOS),
            dark_image=Image.open(os.path.join(image_path, "actuadores.png")).resize(icon_size, Image.LANCZOS),
            size=icon_size
        )

        self.settings_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "settings.png")).resize(icon_size, Image.LANCZOS),
            dark_image=Image.open(os.path.join(image_path, "settings.png")).resize(icon_size, Image.LANCZOS),
            size=icon_size
        )

        # Panel lateral
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        
        # Configurar pesos de filas para empujar el usuario hacia abajo
        self.navigation_frame.grid_rowconfigure(0, weight=0)  # Título
        self.navigation_frame.grid_rowconfigure(1, weight=0)  # Botón Inicio
        self.navigation_frame.grid_rowconfigure(2, weight=0)  # Botón Alertas
        self.navigation_frame.grid_rowconfigure(3, weight=0)  # Botón Actuadores
        self.navigation_frame.grid_rowconfigure(4, weight=0)  # Botón Config Bombas
        self.navigation_frame.grid_rowconfigure(5, weight=1)  # Espacio flexible
        self.navigation_frame.grid_rowconfigure(6, weight=0)  # Usuario
        self.navigation_frame.grid_rowconfigure(7, weight=0)  # Botón logout

        # Título "Sistema Hidroponico" con icono
        self.system_title_frame = customtkinter.CTkFrame(self.navigation_frame, fg_color="transparent")
        self.system_title_frame.grid(row=0, column=0, padx=10, pady=(20, 10), sticky="ew")

        self.system_title_icon = customtkinter.CTkLabel(
            self.system_title_frame,
            image=self.small_logo_image,
            text=""
        )
        self.system_title_icon.pack(side="left", padx=(0, 10))

        self.system_title_label = customtkinter.CTkLabel(
            self.system_title_frame, 
            text="Sistema Hidroponico",
            font=customtkinter.CTkFont(size=16, weight="bold"),
            anchor="w"
        )
        self.system_title_label.pack(side="left")

        # Botones del menú
        self.home_button = self.create_nav_button("Inicio", self.home_image, self.home_button_event, 1)
        self.alerts_button = self.create_nav_button("Alertas", self.alerts_image, self.alerts_button_event, 2)
        self.actuators_button = self.create_nav_button("Actuadores", self.actuators_image, self.actuators_button_event, 3)
        self.bombas_button = self.create_nav_button("Configuración Bombas", self.settings_image, self.bombas_button_event, 4)

        # Configuración de filas para empujar el usuario hacia abajo
        self.navigation_frame.grid_rowconfigure(5, weight=1)  # Espacio flexible

        # Frame contenedor para usuario centrado
        self.user_container = customtkinter.CTkFrame(self.navigation_frame, fg_color="transparent")
        self.user_container.grid(row=6, column=0, padx=10, pady=(40, 10), sticky="nsew")
        self.user_container.grid_columnconfigure(0, weight=1)  # Centrar contenido

        # Frame interno para alinear icono y texto
        self.user_frame = customtkinter.CTkFrame(self.user_container, fg_color="transparent")
        self.user_frame.grid(row=0, column=0, sticky="")

        # Icono del usuario centrado
        self.user_icon = customtkinter.CTkLabel(
            self.user_frame,
            image=self.small_logo_image,
            text=""
        )
        self.user_icon.grid(row=0, column=0, pady=(0, 5))

        # Texto del usuario centrado
        user_info = f"{self.user['nombre_completo']}\n({self.user['rol']})"
        self.user_info_label = customtkinter.CTkLabel(
            self.user_frame,
            text=user_info,
            font=customtkinter.CTkFont(size=14, weight="bold"),
            anchor="center",  # Texto centrado
            justify="center"  # Justificación centrada
        )
        self.user_info_label.grid(row=1, column=0)

        # Botón de cerrar sesión centrado
        self.logout_button = customtkinter.CTkButton(
            self.navigation_frame, 
            text="Cerrar Sesión", 
            command=self.on_logout,
            fg_color="#FF0000",
            hover_color="#CC0000",
            text_color="white",
            anchor="center",
            font=customtkinter.CTkFont(size=14, weight="bold"),
            corner_radius=10
        )
        self.logout_button.grid(row=7, column=0, sticky="ew", padx=20, pady=(0, 20))
        

        # Frames principales
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.alerts_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.actuators_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.bombas_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        self.select_frame_by_name("home")
    
    def comprobar_notificaciones(self):
        alertas_actuales = obtener_alertas_completas()
        
        for alerta in alertas_actuales:
            id_alerta = alerta.get("id_alerta")
            if id_alerta not in self.ids_alertas_vistas:
                mensaje = f"⚠️ {alerta.get('tipo_alerta', 'Alerta')} - {alerta.get('descripcion', '')}"
                self.notificador.recibir_alerta(mensaje)
                self.ids_alertas_vistas.add(id_alerta)
        
        self.after(20000, self.comprobar_notificaciones)
    
    def create_nav_button(self, text, image, command, row):
        button = customtkinter.CTkButton(
            self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text=text,
            fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
            image=image, anchor="w", command=command, font=customtkinter.CTkFont(size=18)
        )
        button.grid(row=row, column=0, sticky="ew")
        return button
    
    def select_frame_by_name(self, name):
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.alerts_button.configure(fg_color=("gray75", "gray25") if name == "alerts" else "transparent")
        self.actuators_button.configure(fg_color=("gray75", "gray25") if name == "actuators" else "transparent")
        self.bombas_button.configure(fg_color=("gray75", "gray25") if name == "bombas" else "transparent")
        
        if name == "home":
            self.show_frame(self.home_frame, iniciar_graficas, self.graficas_mostradas)
            self.graficas_mostradas = True
        else:
            self.home_frame.grid_forget()
        
        if name == "alerts":
            self.show_frame(self.alerts_frame, iniciar_alertas, self.alertas_mostradas)
            self.alertas_mostradas = True
        else:
            self.alerts_frame.grid_forget()
        
        if name == "actuators":
            self.show_frame(self.actuators_frame, crear_interfaz_actuadores)
        else:
            self.actuators_frame.grid_forget()
        
        if name == "bombas":
            self.show_frame(self.bombas_frame, crear_configuracion_sistema, self.bombas_config_mostrada)
            self.bombas_config_mostrada = True
        else:
            self.bombas_frame.grid_forget()
    
    def show_frame(self, frame, func=None, flag=None):
        frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        if func and not flag:
            func(frame)
    
    def home_button_event(self):
        self.select_frame_by_name("home")
    
    def alerts_button_event(self):
        self.select_frame_by_name("alerts")
    
    def actuators_button_event(self):
        self.select_frame_by_name("actuators")
    
    def bombas_button_event(self):
        self.select_frame_by_name("bombas")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Sistema Hidropónico")
        self.geometry("900x500")
        customtkinter.set_appearance_mode("light")
        
        # Variables para controlar el estado de maximizado
        self.maximized = False
        self.original_size = "900x500"
        self.original_pos = None
        
        # Configurar evento para detectar cambio de tamaño
        self.bind("<Configure>", self.on_window_configure)
        
        # Contenedor principal
        self.container = customtkinter.CTkFrame(self)
        self.container.pack(fill="both", expand=True)
        
        # Variables de usuario
        self.current_user = None
        
        # Mostrar primero el login
        self.show_login()
    
    def on_window_configure(self, event):
        """Detecta cuando la ventana cambia de tamaño"""
        if not self.maximized and (self.winfo_width() > 1000 or self.winfo_height() > 600):
            self.maximized = True
        elif self.maximized and self.winfo_width() <= 1000 and self.winfo_height() <= 600:
            self.maximized = False
    
    def toggle_maximize(self):
        """Alterna entre tamaño normal y maximizado"""
        if self.maximized:
            self.geometry(self.original_size)
            if self.original_pos:
                self.geometry(f"+{self.original_pos[0]}+{self.original_pos[1]}")
        else:
            self.original_size = f"{self.winfo_width()}x{self.winfo_height()}"
            self.original_pos = (self.winfo_x(), self.winfo_y())
            self.state('zoomed')
        self.maximized = not self.maximized
    
    def show_login(self):
        """Muestra el frame de login"""
        # Limpiar contenedor
        for widget in self.container.winfo_children():
            widget.destroy()
        
        # Configurar tamaño fijo para login
        self.geometry("900x500")
        self.resizable(True, True)
        
        # Crear frame de login
        login_frame = LoginFrame(self.container, self.on_login_success)
        login_frame.pack(fill="both", expand=True)
    
    def show_main_interface(self, user):
        """Muestra la interfaz principal"""
        # Limpiar contenedor
        for widget in self.container.winfo_children():
            widget.destroy()
        
        # Habilitar redimensionamiento para la interfaz principal
        self.resizable(True, True)
        
        # Configurar tamaño inicial más grande
        self.geometry("900x500")
        
        # Crear frame principal
        main_frame = MainFrame(self.container, user, self.on_logout)
        main_frame.pack(fill="both", expand=True)
    
    def on_login_success(self, user):
        """Callback cuando el login es exitoso"""
        self.current_user = user
        self.show_main_interface(user)
    
    def on_logout(self):
        """Callback para cerrar sesión"""
        self.current_user = None
        self.show_login()

if __name__ == "__main__":
    app = App()
    app.mainloop()