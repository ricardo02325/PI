import customtkinter

class Formulario(customtkinter.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        # Expandir la columna de los campos de entrada
        self.grid_columnconfigure(0, weight=0)  # Label sin expansión
        self.grid_columnconfigure(1, weight=1)  # Entry ocupa el ancho disponible

        # Nombre
        self.name_label = customtkinter.CTkLabel(self, text="Nombre:", anchor="w")
        self.name_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.name_entry = customtkinter.CTkEntry(self, height=30)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        # Correo
        self.email_label = customtkinter.CTkLabel(self, text="Correo:", anchor="w")
        self.email_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.email_entry = customtkinter.CTkEntry(self, height=30)
        self.email_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        # Teléfono
        self.phone_label = customtkinter.CTkLabel(self, text="Teléfono:", anchor="w")
        self.phone_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.phone_entry = customtkinter.CTkEntry(self, height=30)
        self.phone_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        # Botón más alineado
        self.submit_button = customtkinter.CTkButton(self, text="Enviar", height=35, command=self.submit_form)
        self.submit_button.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

    def submit_form(self):
        name = self.name_entry.get()
        email = self.email_entry.get()
        phone = self.phone_entry.get()
        print(f"Nombre: {name}, Correo: {email}, Teléfono: {phone}")