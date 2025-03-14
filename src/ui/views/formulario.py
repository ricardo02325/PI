import customtkinter as ctk
import mysql.connector

def obtener_sensores():
    """Función para obtener los sensores disponibles de la base de datos."""
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="sistema_hidroponico"
        )

        cursor = conexion.cursor()
        cursor.execute("SELECT id_sensor, tipo_sensor FROM sensores")
        sensores = cursor.fetchall()
        conexion.close()

        return sensores
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return []

def actualizar_trigger(temp_min, temp_max, id_sensor):
    """Actualizar el trigger en la base de datos con los valores del formulario."""
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="sistema_hidroponico"
        )
        cursor = conexion.cursor()

        # Borrar el trigger existente
        cursor.execute("DROP TRIGGER IF EXISTS Temperatura_AI")

        # Crear el nuevo trigger con los valores proporcionados
        trigger_sql = f"""
        CREATE TRIGGER `Temperatura_AI` AFTER INSERT ON `lecturas_sensores`
        FOR EACH ROW BEGIN
            IF NEW.id_sensor = {id_sensor} THEN
                IF NEW.valor < {temp_min} THEN
                    INSERT INTO alertas(tipo_alerta, descripcion, fecha_hora, estado)
                    VALUES ('Valor fuera de rango', 'Valor de la Temperatura baja', NOW(),
                            (SELECT estado FROM sensores WHERE id_sensor = NEW.id_sensor));
                ELSEIF NEW.valor > {temp_max} THEN
                    INSERT INTO alertas(tipo_alerta, descripcion, fecha_hora, estado)
                    VALUES ('Valor fuera de rango', 'Valor de la Temperatura alta', NOW(),
                            (SELECT estado FROM sensores WHERE id_sensor = NEW.id_sensor));
                END IF;
            END IF;
        END
        """

        cursor.execute(trigger_sql)
        conexion.commit()
        conexion.close()
        print("Trigger actualizado correctamente.")
    except mysql.connector.Error as err:
        print(f"Error al actualizar el trigger: {err}")

def crear_formulario(parent):
    """Crear el formulario para configurar las temperaturas mínimas y máximas."""
    frame_principal = ctk.CTkFrame(parent, fg_color="white")
    frame_principal.grid(pady=10, padx=10, sticky="nsew")

    # Obtener los sensores desde la base de datos
    sensores = obtener_sensores()

    # Etiqueta de encabezado
    titulo_label = ctk.CTkLabel(frame_principal, text="📊 Configuración de Sensores", font=("Arial", 20, "bold"), text_color="#00A3A3")
    titulo_label.grid(row=0, column=0, pady=(10, 20), columnspan=2)

    # Etiqueta de selección de sensor
    sensor_label = ctk.CTkLabel(frame_principal, text="Seleccionar Sensor:", font=("Arial", 14))
    sensor_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

    # Desplegable para seleccionar el sensor
    sensor_variable = ctk.StringVar()
    sensor_menu = ctk.CTkOptionMenu(frame_principal, variable=sensor_variable, values=[f"{sensor[1]} (ID: {sensor[0]})" for sensor in sensores])
    sensor_menu.grid(row=1, column=1, padx=10, pady=5, sticky="w")

    # Etiqueta de temperatura mínima
    temp_min_label = ctk.CTkLabel(frame_principal, text="Temperatura Mínima (°C):", font=("Arial", 14))
    temp_min_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")

    # Entrada para la temperatura mínima
    temp_min_entry = ctk.CTkEntry(frame_principal, font=("Arial", 14), width=150)
    temp_min_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

    # Etiqueta de temperatura máxima
    temp_max_label = ctk.CTkLabel(frame_principal, text="Temperatura Máxima (°C):", font=("Arial", 14))
    temp_max_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")

    # Entrada para la temperatura máxima
    temp_max_entry = ctk.CTkEntry(frame_principal, font=("Arial", 14), width=150)
    temp_max_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")

    # Función de guardar cuando el usuario presiona el botón
    def guardar():
        try:
            # Obtener el ID del sensor seleccionado
            sensor_seleccionado = sensor_variable.get()
            sensor_id = int(sensor_seleccionado.split("ID: ")[1].split(")")[0])

            # Obtener las temperaturas mínima y máxima
            temp_min = float(temp_min_entry.get())
            temp_max = float(temp_max_entry.get())

            # Actualizar el trigger con los nuevos valores
            actualizar_trigger(temp_min, temp_max, sensor_id)
        except ValueError:
            print("Por favor, ingrese valores válidos para la temperatura.")

    # Botón para guardar la configuración
    boton_guardar = ctk.CTkButton(frame_principal, text="💾 Guardar Configuración", font=("Arial", 14, "bold"), fg_color="#007bff", text_color="white", command=guardar)
    boton_guardar.grid(row=4, column=0, columnspan=2, pady=20)

    return frame_principal