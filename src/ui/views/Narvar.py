import tkinter as tk
from tkinter import ttk

class SidebarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Interfaz con Barra de Navegación")
        self.root.geometry("600x400")
        
        # Colores y estilos
        self.bg_color = "#2c3e50"
        self.fg_color = "#ecf0f1"
        self.btn_color = "#34495e"
        self.hover_color = "#1abc9c"
        
        # Frame de la barra lateral
        self.sidebar_width = 200
        self.sidebar = tk.Frame(root, bg=self.bg_color, width=self.sidebar_width, height=400)
        self.sidebar.place(x=-self.sidebar_width, y=0)
        
        # Botón para mostrar/ocultar barra lateral
        self.toggle_btn = tk.Button(root, text="☰", font=("Arial", 14), bg=self.btn_color, fg=self.fg_color, 
                                    command=self.toggle_sidebar, relief="flat")
        self.toggle_btn.place(x=10, y=10)
        
        # Botones de navegación
        self.create_nav_buttons()
        
        self.sidebar_visible = False
        
    def create_nav_buttons(self):
        buttons = ["Inicio", "Perfil", "Configuración", "Salir"]
        for i, text in enumerate(buttons):
            btn = tk.Button(self.sidebar, text=text, font=("Arial", 12), bg=self.btn_color, fg=self.fg_color,
                            activebackground=self.hover_color, relief="flat", width=20, command=lambda t=text: self.on_nav_click(t))
            btn.pack(pady=10)
    
    def on_nav_click(self, text):
        print(f"Navegando a {text}")
    
    def toggle_sidebar(self):
        if self.sidebar_visible:
            self.hide_sidebar()
        else:
            self.show_sidebar()
    
    def show_sidebar(self):
        for x in range(-self.sidebar_width, 0, 20):
            self.sidebar.place(x=x, y=0)
            self.root.update()
        self.sidebar_visible = True
    
    def hide_sidebar(self):
        for x in range(0, -self.sidebar_width, -20):
            self.sidebar.place(x=x, y=0)
            self.root.update()
        self.sidebar_visible = False

if __name__ == "__main__":
    root = tk.Tk()
    app = SidebarApp(root)
    root.mainloop()
