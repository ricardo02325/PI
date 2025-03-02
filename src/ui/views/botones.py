import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
from Graficas_sensores import iniciar_graficas  # Asegúrate de importar la función desde el archivo adecuado

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Interfaz con CustomTkinter")
        self.geometry("800x500")

        ctk.set_appearance_mode("light")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = ctk.CTkFrame(self, width=200)
        self.sidebar.grid(row=0, column=0, sticky="ns")

        self.btn_page1 = ctk.CTkButton(self.sidebar, text="Página 1", command=lambda: self.show_page("page1"))
        self.btn_page1.pack(pady=10, padx=10)

        self.btn_page2 = ctk.CTkButton(self.sidebar, text="Página 2", command=lambda: self.show_page("page2"))
        self.btn_page2.pack(pady=10, padx=10)

        self.btn_graph = ctk.CTkButton(self.sidebar, text="Gráfica", command=lambda: self.show_page("graph"))
        self.btn_graph.pack(pady=10, padx=10)

        self.btn_menu = ctk.CTkButton(self.sidebar, text="Menú Horizontal", command=lambda: self.show_page("menu"))
        self.btn_menu.pack(pady=10, padx=10)

        self.btn_graficas = ctk.CTkButton(self.sidebar, text="Mostrar Gráficas", command=lambda: self.show_page("graficas"))
        self.btn_graficas.pack(pady=10, padx=10)

        self.container = ctk.CTkFrame(self)
        self.container.grid(row=0, column=1, sticky="nsew")
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_rowconfigure(0, weight=1)

        self.pages = {}
        self.create_pages()

    def create_pages(self):
        """Crear y almacenar las páginas"""
        self.pages["page1"] = self.create_page("Hola Mundo - Página 1")
        self.pages["page2"] = self.create_page("Hola Mundo - Página 2")
        self.pages["graph"] = self.create_graph_page()
        self.pages["menu"] = self.create_menu_page()
        self.pages["graficas"] = self.create_graphs_page()

    def create_page(self, text):
        frame = ctk.CTkFrame(self.container)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)
        label = ctk.CTkLabel(frame, text=text, font=("Arial", 20))
        label.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        return frame

    def create_graph_page(self):
        frame = ctk.CTkFrame(self.container)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)

        fig, ax = plt.subplots(figsize=(5, 3))
        x = list(range(10))
        y = [random.randint(1, 100) for _ in range(10)]
        ax.plot(x, y, marker='o', linestyle='-', color='blue')
        ax.set_title("Gráfica de Datos Aleatorios")
        ax.set_xlabel("Tiempo")
        ax.set_ylabel("Valor")

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        canvas.draw()

        return frame

    def create_menu_page(self):
        frame = ctk.CTkFrame(self.container)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)

        menu_frame = ctk.CTkFrame(frame, fg_color="#e0e0e0", corner_radius=10)
        menu_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        labels = ["Inicio", "Servicios", "Nosotros", "Contacto", "Ayuda"]
        for text in labels:
            label = ctk.CTkLabel(menu_frame, text=text, font=("Arial", 14, "bold"), fg_color="#a0a0a0", width=80, height=30, corner_radius=5)
            label.pack(side="left", padx=5, pady=5)

        return frame

    def create_graphs_page(self):
        frame = ctk.CTkFrame(self.container)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)

        # Llamar a la función iniciar_graficas para mostrar las gráficas
        iniciar_graficas(frame)

        return frame

    def show_page(self, page_name):
        for page in self.pages.values():
            page.grid_forget()

        self.pages[page_name].grid(row=0, column=0, sticky="nsew")

if __name__ == "__main__":
    app = App()
    app.mainloop()
