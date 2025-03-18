import mysql.connector

def conectar_db():
    """Establece conexión con la base de datos MySQL."""
    try:
        conexion = mysql.connector.connect(
            host="localhost",  # host
            user="root",       # Usuario de MySQL
            password="",       # Contraseña
            database="sistema_hidroponico"  # Nombre de la db
        )
        return conexion
    except mysql.connector.Error as err:
        print(f"Error de conexión: {err}")
        return None

def obtener_sensores():
    """Obtiene la lista de sensores de la base de datos."""
    conexion = conectar_db()
    if conexion:
        cursor = conexion.cursor(dictionary=True)  # Devuelve los resultados como diccionario
        cursor.execute("SELECT id_sensor, tipo_sensor FROM sensores")
        sensores = cursor.fetchall()
        conexion.close()
        return sensores
    return []

def actualizar_trigger(id_sensor, rango_min, rango_max):
    """Elimina el trigger existente y crea uno nuevo con los valores proporcionados."""
    conexion = conectar_db()
    if conexion:
        try:
            cursor = conexion.cursor()

            # Eliminar el trigger si ya existe
            cursor.execute("DROP TRIGGER IF EXISTS Temperatura_AI")

            # Crear el nuevo trigger con los valores dinámicos
            trigger_sql = f"""
            DELIMITER $$

            CREATE TRIGGER Temperatura_AI
            AFTER INSERT ON lecturas_sensores
            FOR EACH ROW
            BEGIN
                -- Verificar si el sensor es el correcto
                IF NEW.id_sensor = {id_sensor} THEN
                    -- Si el valor es menor que el rango mínimo, insertar alerta
                    IF NEW.valor < {rango_min} THEN
                        INSERT INTO alertas(tipo_alerta, descripcion, fecha_hora, estado)
                        VALUES ('Valor fuera de rango', 
                                CONCAT('Valor del sensor ', NEW.id_sensor, ' demasiado bajo'), 
                                NOW(), 
                                (SELECT estado FROM sensores WHERE id_sensor = NEW.id_sensor));
                    -- Si el valor es mayor que el rango máximo, insertar alerta
                    ELSEIF NEW.valor > {rango_max} THEN
                        INSERT INTO alertas(tipo_alerta, descripcion, fecha_hora, estado)
                        VALUES ('Valor fuera de rango', 
                                CONCAT('Valor del sensor ', NEW.id_sensor, ' demasiado alto'), 
                                NOW(), 
                                (SELECT estado FROM sensores WHERE id_sensor = NEW.id_sensor));
                    END IF;
                END IF;
            END$$

            DELIMITER ;
            """

            cursor.execute(trigger_sql)
            conexion.commit()
            print("Trigger actualizado correctamente.")

        except mysql.connector.Error as err:
            print(f"Error al actualizar el trigger: {err}")
        finally:
            cursor.close()
            conexion.close()

# Prueba la función
sensores = obtener_sensores()
for sensor in sensores:
    print(sensor)