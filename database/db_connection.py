import mysql.connector

def conectar_bd():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root", 
            password="",
            database="sistema_hidroponico"
        )
        return conexion
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def imprimir_usuarios():
    conexion = conectar_bd()
    if not conexion:
        return
    
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM usuarios")
        usuarios = cursor.fetchall()
        
        print("ID | Nombre | Correo | Fecha de registro")
        print("-" * 50)
        for usuario in usuarios:
            print(f"{usuario[0]} | {usuario[1]} | {usuario[2]} | {usuario[3]}")
    
    except mysql.connector.Error as err:
        print(f"Error al obtener usuarios: {err}")
    finally:
        cursor.close()
        conexion.close()

if __name__ == "__main__":
    imprimir_usuarios()