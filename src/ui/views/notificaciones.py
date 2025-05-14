import sqlite3
import json
from notifypy import Notify
import os

# 1. Conectar a la base de datos
conn = sqlite3.connect("C:")
cursor = conn.cursor()

# 2. Obtener el último valor de conductividad
cursor.execute("SELECT conductividad FROM mediciones ORDER BY id DESC LIMIT 1")
resultado = cursor.fetchone()

if resultado:
    conductividad = resultado[0]
    print(f"Conductividad actual: {conductividad}")

    # 3. Verificar si supera el límite
    if conductividad > 1000:  # Ajusta este valor al límite que desees
        notification = Notify()
        notification.title = "⚠️ Alerta de Conductividad"
        notification.message = f"La conductividad eléctrica es muy alta: {conductividad}"
        notification.audio = "C:\\Users\\Colibecas\\Desktop\\PI\\src\\ui\\views\\sonido_alertas.wav"
        notification.icon = "C:\\Users\\Colibecas\\Desktop\\PI\\src\\ui\\views\\test_images\\noti.png"
        notification.send()

# 4. Cerrar la conexión
conn.close()

def verificar_notificaciones():
    base_path = os.path.dirname(__file__)
    json_file = os.path.join(base_path, "notificados.json")

    # Verificar si el archivo existe
    if not os.path.exists(json_file):
        print("El archivo JSON no existe.")
        return

    with open(json_file, "r") as file:
        notificados = json.load(file)

    alguna_noti = False

    # Iterar sobre grupos y registros dentro de cada grupo
    for grupo_id, alertas in notificados.items():
        for alerta_id, registro in alertas.items():
            if not registro.get("notify", False):  # Si no ha sido notificado
                print(f"🔔 Enviando notificación del grupo {grupo_id} para ID {registro['id']}")

                # Configurar notificación
                notification = Notify()
                notification.title = f"Alerta {registro.get('priority', 'Sin prioridad')}"
                notification.audio = os.path.join(base_path, "sonido_alertas.wav")

                # Definir ícono según su prioridad
                priority = registro.get("priority", "Baja")

                if priority == "Alta":
                    icon_file = "noti.2.png"
                elif priority == "Media":
                    icon_file = "noti.1.png"
                else:
                    icon_file = "noti.png"

                icon_path = os.path.join(base_path, "ui", "assets", "views", "test_images", icon_file)

                # Verificar si existe el ícono
                if not os.path.exists(icon_path):
                    icon_path = os.path.join(base_path, "ui", "assets", "views", "test_images", "noti.png")

                notification.icon = icon_path

                notification.message = f"{registro['message']} - {registro['datetime']}"
                notification.send()

                # Marcar como notificado
                registro["notify"] = True
                alguna_noti = True

    # Guardar los cambios en el archivo JSON solo si hubo notificaciones
    if alguna_noti:
        with open(json_file, "w") as file:
            json.dump(notificados, file, indent=4)

# Ejecutar la función
verificar_notificaciones()