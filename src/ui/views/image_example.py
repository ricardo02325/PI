import customtkinter
import os
from PIL import Image
from Graficas_sensores import iniciar_graficas  # Importa la función para mostrar las gráficas
from alertas import iniciar_alertas  # Importa la función para mostrar alertas

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sistema Hidropónico")
        self.geometry("900x500")
        customtkinter.set_appearance_mode("light")  # Fijar el modo claro

        # Configuración de la cuadrícula
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Cargar imágenes
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "CustomTkinter_logo_single.png")), size=(26, 26))
        self.home_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "home_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "home_light.png")), size=(20, 20))
        self.alerts_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "chat_dark.png")),
                                                   dark_image=Image.open(os.path.join(image_path, "chat_light.png")), size=(20, 20))

        # Crear el panel de navegación
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="  Sistema Hidropónico", image=self.logo_image,
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Inicio",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.alerts_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Alertas",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.alerts_image, anchor="w", command=self.alerts_button_event)
        self.alerts_button.grid(row=2, column=0, sticky="ew")

        # Crear los frames principales
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")  # Eliminé el formulario aquí
        self.alerts_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.graphs_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        self.graficas_mostradas = False  # Control para evitar recargar las gráficas
        self.alertas_mostradas = False  # Control para evitar recargar las alertas
        self.select_frame_by_name("home")

    def select_frame_by_name(self, name):
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.alerts_button.configure(fg_color=("gray75", "gray25") if name == "alerts" else "transparent")

        if name == "home":
            self.home_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
            if not self.graficas_mostradas:
                iniciar_graficas(self.home_frame)  # Mostrar las gráficas en la página de inicio
                self.graficas_mostradas = True
        else:
            self.home_frame.grid_forget()

        if name == "alerts":
            self.alerts_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
            if not self.alertas_mostradas:  # Verifica si las alertas ya han sido mostradas
                iniciar_alertas(self.alerts_frame)
                self.alertas_mostradas = True
        else:
            self.alerts_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def alerts_button_event(self):
        self.select_frame_by_name("alerts")

if __name__ == "__main__":
    app = App()
    app.mainloop()
