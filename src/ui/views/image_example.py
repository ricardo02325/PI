import customtkinter
import os
from PIL import Image
from Graficas_sensores import iniciar_graficas
from alertas import iniciar_alertas
from Actuadoresbtn import crear_interfaz_actuadores
from configtimeact import crear_configuracion_sistema
from mantenimiento import MantenimientoFrame  # Importamos la clase MantenimientoFrame

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sistema Hidropónico")
        self.geometry("900x500")
        customtkinter.set_appearance_mode("light")

        self.grid_rowconfigure(0, weight=1) 
        self.grid_columnconfigure(1, weight=1)

        icon_size = (32, 32)
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")

        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "CustomTkinter_logo_single.png")).resize(icon_size, Image.LANCZOS))

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

        self.maintenance_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "mantenimiento.png")).resize(icon_size, Image.LANCZOS),
            dark_image=Image.open(os.path.join(image_path, "mantenimiento.png")).resize(icon_size, Image.LANCZOS),
            size=icon_size
        )

        # Panel lateral
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(6, weight=1)  

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="  Sistema Hidropónico", image=self.logo_image,
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        # Botones del menú
        self.home_button = self.create_nav_button("Inicio", self.home_image, self.home_button_event, 1)
        self.alerts_button = self.create_nav_button("Alertas", self.alerts_image, self.alerts_button_event, 2)
        self.actuators_button = self.create_nav_button("Actuadores", self.actuators_image, self.actuators_button_event, 3)
        self.bombas_button = self.create_nav_button("Configuración Bombas", self.settings_image, self.bombas_button_event, 4)
        self.maintenance_button = self.create_nav_button("Mantenimiento", self.maintenance_image, self.mantenimiento_button_event, 5)

        # Frames de contenido
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")  
        self.alerts_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.actuators_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.bombas_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")  
        self.maintenance_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        self.graficas_mostradas = False  
        self.alertas_mostradas = False 
        self.bombas_config_mostrada = False
        self.mantenimiento_mostrado = False

        self.select_frame_by_name("home")

    def create_nav_button(self, text, image, command, row):
        button = customtkinter.CTkButton(
            self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text=text,
            fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
            image=image, anchor="w", command=command
        )
        button.grid(row=row, column=0, sticky="ew")
        return button

    def select_frame_by_name(self, name):
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.alerts_button.configure(fg_color=("gray75", "gray25") if name == "alerts" else "transparent")
        self.actuators_button.configure(fg_color=("gray75", "gray25") if name == "actuators" else "transparent")
        self.bombas_button.configure(fg_color=("gray75", "gray25") if name == "bombas" else "transparent")
        self.maintenance_button.configure(fg_color=("gray75", "gray25") if name == "mantenimiento" else "transparent")

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

        if name == "mantenimiento":
            self.show_mantenimiento_frame()
        else:
            self.maintenance_frame.grid_forget()

    def show_frame(self, frame, func=None, flag=None):
        frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        if func and not flag:
            func(frame)

    def show_mantenimiento_frame(self):
        # Limpiamos el frame de mantenimiento si ya tiene widgets
        for widget in self.maintenance_frame.winfo_children():
            widget.destroy()
        
        # Creamos y mostramos el frame de mantenimiento
        self.maintenance_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        
        # Configuramos el grid para que el frame de mantenimiento se expanda
        self.maintenance_frame.grid_rowconfigure(0, weight=1)
        self.maintenance_frame.grid_columnconfigure(0, weight=1)
        ''
        # Creamos el módulo de mantenimiento dentro del frame
        mantenimiento = MantenimientoFrame(self.maintenance_frame)
        mantenimiento.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        self.mantenimiento_mostrado = True

    def home_button_event(self):
        self.select_frame_by_name("home")

    def alerts_button_event(self):
        self.select_frame_by_name("alerts")
    
    def actuators_button_event(self):
        self.select_frame_by_name("actuators")
        
    def bombas_button_event(self):
        self.select_frame_by_name("bombas")

    def mantenimiento_button_event(self):
        self.select_frame_by_name("mantenimiento")

if __name__ == "__main__":
    app = App()
    app.mainloop()