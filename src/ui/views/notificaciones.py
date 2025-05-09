import json
import os
import time
from notifypy import Notify

# Ruta al archivo JSON
base_path = os.path.dirname(__file__)
json_file = os.path.join(base_path, "notificados.json")

# Guardar última hora de modificación conocida
ultima_modificacion = None

def verificar_notificaciones():
    with open(json_file, "r") as file:
        notificados = json.load(file)

    notification = Notify()
    notification.title = "Alerta"
    notification.audio = os.path.join(base_path, "sonido_alertas.wav")
    # Línea eliminada: icono personalizado

    alguna_noti = False

    for grupo_id, alertas in notificados.items():
        for alerta_id, registro in alertas.items():
            if not registro.get("notify", False):
                print(f"🔔 Enviando notificación del grupo {grupo_id} para ID {registro['id']}")
                notification.message = f"{registro['message']} - {registro['date']}"
                notification.send()
                registro["notify"] = True
                alguna_noti = True

    if alguna_noti:
        with open(json_file, "w") as file:
            json.dump(notificados, file, indent=4)

# Bucle de monitoreo
if __name__ == "__main__":
    if not os.path.exists(json_file):
        print("❌ El archivo JSON no existe.")
        exit()

    ultima_modificacion = os.path.getmtime(json_file)
    print("⏳ Monitoreando cambios en notificados.json...")

    try:
        while True:
            time.sleep(1)
            nueva_modificacion = os.path.getmtime(json_file)
            if nueva_modificacion != ultima_modificacion:
                print("🔄 Cambio detectado en notificados.json.")
                ultima_modificacion = nueva_modificacion
                verificar_notificaciones()
    except KeyboardInterrupt:
        print("\n🛑 Monitoreo detenido por el usuario.")