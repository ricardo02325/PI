import json
from notifypy import Notify
import os

def verificar_notificaciones():
    # Ruta del archivo JSON
    base_path = os.path.dirname(__file__)
    json_file = os.path.join(base_path, "notificados.json")

    # Verificar si el archivo existe
    if not os.path.exists(json_file):
        print("El archivo JSON no existe.")
        return

    with open(json_file, "r") as file:
        notificados = json.load(file)

    # Configurar notificación
    notification = Notify()
    notification.title = "Alerta"
    notification.audio = os.path.join(base_path, "sonido_alertas.wav")
    notification.icon = os.path.join(base_path, "test_images", "noti.png")

    alguna_noti = False

    # Iterar sobre grupos y registros dentro de cada grupo
    for grupo_id, alertas in notificados.items():
        for alerta_id, registro in alertas.items():
            if not registro.get("notify", False):  # Si no ha sido notificado
                print(f"🔔 Enviando notificación del grupo {grupo_id} para ID {registro['id']}")
                notification.message = f"{registro['message']} - {registro['date']}"
                notification.send()
                registro["notify"] = True
                alguna_noti = True

    # Guardar los cambios en el archivo JSON solo si hubo notificaciones
    if alguna_noti:
        with open(json_file, "w") as file:
            json.dump(notificados, file, indent=4)