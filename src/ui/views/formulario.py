import customtkinter

class Formulario(customtkinter.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.form_label = customtkinter.CTkLabel(self, text="Formulario", font=customtkinter.CTkFont(size=16, weight="bold"))
        self.form_label.grid(row=0, column=0, padx=20, pady=10)

        # Form fields
        self.name_label = customtkinter.CTkLabel(self, text="Nombre:")
        self.name_label.grid(row=1, column=0, padx=20, pady=5)
        self.name_entry = customtkinter.CTkEntry(self)
        self.name_entry.grid(row=1, column=1, padx=20, pady=5)

        self.email_label = customtkinter.CTkLabel(self, text="Correo electrónico:")
        self.email_label.grid(row=2, column=0, padx=20, pady=5)
        self.email_entry = customtkinter.CTkEntry(self)
        self.email_entry.grid(row=2, column=1, padx=20, pady=5)

        self.phone_label = customtkinter.CTkLabel(self, text="Teléfono:")
        self.phone_label.grid(row=3, column=0, padx=20, pady=5)
        self.phone_entry = customtkinter.CTkEntry(self)
        self.phone_entry.grid(row=3, column=1, padx=20, pady=5)

        self.submit_button = customtkinter.CTkButton(self, text="Enviar", command=self.submit_form)
        self.submit_button.grid(row=4, column=0, columnspan=2, padx=20, pady=10)

    def submit_form(self):
        name = self.name_entry.get()
        email = self.email_entry.get()
        phone = self.phone_entry.get()
        print(f"Nombre: {name}, Correo electrónico: {email}, Teléfono: {phone}")
        # Add form submission logic here