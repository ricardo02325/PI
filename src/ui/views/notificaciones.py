import json
import os
from notifypy import Notify
import threading

base_path = os.path.dirname(__file__)
json_file = os.path.join(base_path, "notificados.json")


def verificar_notificaciones():
    if os.path.exists(json_file):
        with open(json_file, "r") as file:
            notificados = json.load(file)
    else:
        notificados = {"8": False, "9": False, "10": False}
        with open(json_file, "w") as file:
            json.dump(notificados, file, indent=4)

    notification = Notify()
    notification.title = "Alerta"
    notification.audio = os.path.join(base_path, "sonido_alertas.wav")
    notification.icon = os.path.join(base_path, "test_images", "noti.png")

    alguna_noti = False
    for numero, fue_notificado in notificados.items():
        if not fue_notificado:
            print(f"🔔 Enviando notificación para número {numero}")
            notification.message = f"La conductividad eléctrica para número {numero} está muy alta"
            notification.send()
            notificados[numero] = True
            alguna_noti = True

    if alguna_noti:
        with open(json_file, "w") as file:
            json.dump(notificados, file, indent=4)


def reiniciar_notificaciones():
    """Pone todos los valores en False cada 5 segundos."""
    if os.path.exists(json_file):
        with open(json_file, "r") as file:
            notificados = json.load(file)
    else:
        notificados = {"8": False, "9": False, "10": False}

    reiniciado = False
    for numero in notificados:
        if notificados[numero] is not False:
            notificados[numero] = False
            reiniciado = True

    if reiniciado:
        with open(json_file, "w") as file:
            json.dump(notificados, file, indent=4)
        print("♻️ Notificaciones reiniciadas a False")

    # Ejecutar esta función de nuevo en 5 segundos
    threading.Timer(5.0, reiniciar_notificaciones).start()


# Iniciar el reinicio periódico (una sola vez al arrancar)
reiniciar_notificaciones()