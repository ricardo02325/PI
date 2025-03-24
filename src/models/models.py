import mysql.connector

def conectar_db():
    """Establece la conexión con la base de datos MySQL."""
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="sistema_hidroponico"
        )
        return conexion
    except mysql.connector.Error as err:
        print(f"Error al conectar a la base de datos: {err}")
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

def actualizar_alerta(id_alerta, nuevo_estado):
    """Actualizar el estado de una alerta en la base de datos."""
    conexion = conectar_db()
    if conexion:
        try:
            cursor = conexion.cursor()
            query = """
            UPDATE alertas
            SET estado = %s
            WHERE id_alerta = %s
            """
            cursor.execute(query, (nuevo_estado, id_alerta))
            conexion.commit()
            print(f"Alerta {id_alerta} actualizada a estado {nuevo_estado}.")
        except mysql.connector.Error as err:
            print(f"Error al actualizar la alerta: {err}")
        finally:
            cursor.close()
            conexion.close()

def obtener_alertas():
    """Obtiene todas las alertas inactivas con tipo 'Valor fuera de rango'."""
    conexion = conectar_db()
    if conexion:
        try:
            cursor = conexion.cursor(dictionary=True)  # Retorna resultados como diccionarios
            consulta_sql = """
                SELECT * FROM alertas 
                WHERE tipo_alerta = 'Valor fuera de rango' 
                AND estado = 'inactivo'
            """
            cursor.execute(consulta_sql)
            alertas = cursor.fetchall()  # Obtiene todas las filas de la consulta
            return alertas
        except mysql.connector.Error as err:
            print(f"Error al obtener alertas inactivas: {err}")
            return []
        finally:
            cursor.close()
            conexion.close()

def actualizar_trigger(id_sensor, valor_min, valor_max):
    """Elimina el trigger existente y crea uno nuevo con los valores proporcionados."""
    conexion = conectar_db()
    if conexion:
        try:
            cursor = conexion.cursor()
            # Eliminar el trigger si ya existe
            cursor.execute(f"DROP TRIGGER IF EXISTS Trigger_{id_sensor}_AI")

            # Crear el nuevo trigger con los valores dinámicos
            trigger_sql = f"""
            DELIMITER $$

            CREATE TRIGGER Trigger_{id_sensor}_AI
            AFTER INSERT ON lecturas_sensores
            FOR EACH ROW
            BEGIN
                IF NEW.id_sensor = {id_sensor} THEN
                    IF NEW.valor < {valor_min} THEN
                        INSERT INTO alertas(tipo_alerta, descripcion, fecha_hora, estado)
                        VALUES ('Valor fuera de rango', 
                                CONCAT('Valor del sensor {id_sensor} demasiado bajo: ', NEW.valor), 
                                NOW(), 
                                (SELECT estado FROM sensores WHERE id_sensor = NEW.id_sensor));
                    ELSEIF NEW.valor > {valor_max} THEN
                        INSERT INTO alertas(tipo_alerta, descripcion, fecha_hora, estado)
                        VALUES ('Valor fuera de rango', 
                                CONCAT('Valor del sensor {id_sensor} demasiado alto: ', NEW.valor), 
                                NOW(), 
                                (SELECT estado FROM sensores WHERE id_sensor = NEW.id_sensor));
                    END IF;
                END IF;
            END$$

            DELIMITER ;
            """
            cursor.execute(trigger_sql)
            conexion.commit()
            print(f"Trigger para el sensor {id_sensor} actualizado correctamente.")
        except mysql.connector.Error as err:
            print(f"Error al actualizar el trigger para el sensor {id_sensor}: {err}")
        finally:
            cursor.close()
            conexion.close()

def actualizar_alerta(id_alerta, nuevo_estado):
    """Actualizar el estado de una alerta en la base de datos."""
    conexion = conectar_db()
    if conexion:
        try:
            cursor = conexion.cursor()
            query = """
            UPDATE alertas
            SET estado = %s
            WHERE id_alerta = %s
            """
            cursor.execute(query, (nuevo_estado, id_alerta))
            conexion.commit()
            print(f"Alerta {id_alerta} actualizada a estado {nuevo_estado}.")
        except mysql.connector.Error as err:
            print(f"Error al actualizar la alerta: {err}")
        finally:
            cursor.close()
            conexion.close()