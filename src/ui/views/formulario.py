import sys
import os
import customtkinter

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from src.models.models import obtener_sensores
from src.models.models import actualizar_trigger

class Formulario(customtkinter.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.sensores = obtener_sensores()
        self.sensor_ids = [str(sensor['id_sensor']) for sensor in self.sensores]
        self.sensor_names = [f"ID: {sensor['id_sensor']} - {sensor['tipo_sensor']}" for sensor in self.sensores]

        # Selección de Sensor
        self.sensor_label = customtkinter.CTkLabel(self, text="Selecciona un Sensor:", anchor="w")
        self.sensor_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.sensor_menu = customtkinter.CTkOptionMenu(self, values=self.sensor_names)
        self.sensor_menu.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        # Campo Rango Mínimo
        self.rango_min_label = customtkinter.CTkLabel(self, text="Rango Mínimo:", anchor="w")
        self.rango_min_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.rango_min_entry = customtkinter.CTkEntry(self, height=30)
        self.rango_min_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        # Campo Rango Máximo
        self.rango_max_label = customtkinter.CTkLabel(self, text="Rango Máximo:", anchor="w")
        self.rango_max_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.rango_max_entry = customtkinter.CTkEntry(self, height=30)
        self.rango_max_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        # Botón para actualizar el trigger
        self.submit_button = customtkinter.CTkButton(self, text="Actualizar Trigger", height=35, command=self.submit_form)
        self.submit_button.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

    def submit_form(self):
        """Obtiene los valores ingresados y actualiza el trigger en la base de datos."""
        try:
            sensor_name = self.sensor_menu.get()
            sensor_id = self.sensor_ids[self.sensor_names.index(sensor_name)]
            rango_min = float(self.rango_min_entry.get())
            rango_max = float(self.rango_max_entry.get())

            actualizar_trigger(sensor_id, rango_min, rango_max)
            print(f"Trigger actualizado para el sensor {sensor_id} con rango {rango_min}-{rango_max}")

        except ValueError:
            print("Error: Ingresa valores numéricos para los rangos.")