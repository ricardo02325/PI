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

# Prueba la función
sensores = obtener_sensores()
for sensor in sensores:
    print(sensor)