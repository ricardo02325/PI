import json
import os
from notifypy import Notify

# Ruta al archivo JSON (relativa a este archivo)
base_path = os.path.dirname(__file__)
json_file = os.path.join(base_path, "notificados.json")

# Función para resetear alertas
def reset_alerta(numero=None):
    if os.path.exists(json_file):
        with open(json_file, "r") as file:
            data = json.load(file)
    else:
        print("⚠️ El archivo JSON no existe.")
        return

    if numero is None:
        for key in data:
            data[key] = False
        print("🔁 Todas las alertas han sido reiniciadas.")
    else:
        if str(numero) in data:
            data[str(numero)] = False
            print(f"🔁 Alerta {numero} reiniciada.")
        else:
            print(f"⚠️ Alerta {numero} no encontrada en el archivo.")

    with open(json_file, "w") as file:
        json.dump(data, file, indent=4)

# -------------------------------------
# MAIN - Verificar notificaciones
# -------------------------------------

# Cargar archivo JSON
if os.path.exists(json_file):
    with open(json_file, "r") as file:
        notificados = json.load(file)
else:
    # Crear archivo si no existe (puedes personalizar los números)
    notificados = {
        "8": False,
        "9": False,
        "10": False
    }
    with open(json_file, "w") as file:
        json.dump(notificados, file, indent=4)

# Mostrar contenido actual del archivo
print("📄 Contenido de notificados.json:")
print(json.dumps(notificados, indent=4))

# Configurar notificación
notification = Notify()
notification.title = "Alerta"
notification.audio = os.path.join(base_path, "sonido_alertas.wav")
notification.icon = os.path.join(base_path, "test_images", "noti.png")

# Evaluar y notificar todos los que están en false
alguna_noti = False
for numero, fue_notificado in notificados.items():
    print(f"🔎 Revisando número {numero} - notificado: {fue_notificado}")

    if not fue_notificado:
        print(f"🔔 Enviando notificación para número {numero}")
        notification.message = f"La conductividad eléctrica para número {numero} está muy alta"
        notification.send()
        alguna_noti = True

        # Marcar como notificado
        notificados[numero] = True

# Guardar todos los cambios una sola vez
if alguna_noti:
    with open(json_file, "w") as file:
        json.dump(notificados, file, indent=4)