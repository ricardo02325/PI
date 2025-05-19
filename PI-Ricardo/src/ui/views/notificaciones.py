import json
import os
import time
import subprocess
import platform

# Detectar sistema operativo
SO = platform.system()

# Establecer rutas según plataforma
if SO == "Windows":
    base_path = r"C:\Users\Colibecas\Desktop\PI\src\ui\assets"
else:
    base_path = "/home/pi/proyecto/assets"

json_file = os.path.join(base_path, "notificados.json")
audio_file = os.path.join(base_path, "sonido_alertas.wav")
icon_file = os.path.join(base_path, "alertx.png")  # Asegúrate de tenerlo

def reproducir_sonido():
    try:
        if SO == "Windows":
            subprocess.run(["powershell", "-c", f'(New-Object Media.SoundPlayer "{audio_file}").PlaySync();'])
        else:
            subprocess.run(["aplay", audio_file])
    except Exception as e:
        print(f"⚠️ Error al reproducir sonido: {e}")

def mostrar_notificacion(titulo, mensaje):
    try:
        if SO == "Windows":
            from notifypy import Notify
            notification = Notify()
            notification.title = titulo
            notification.message = mensaje
            notification.icon = icon_file  # Ícono personalizado
            notification.audio = audio_file
            notification.send()
        else:
            # notify-send en Linux (Raspberry Pi)
            subprocess.run([
                "notify-send", titulo, mensaje,
                "--icon", icon_file,
                "--urgency=normal"
            ])
    except Exception as e:
        print(f"⚠️ Error al mostrar notificación: {e}")

def verificar_notificaciones():
    if not os.path.exists(json_file):
        print(f"❌ El archivo JSON no existe en: {json_file}")
        return

    with open(json_file, "r") as file:
        notificados = json.load(file)

    alguna_noti = False

    for grupo_id, alertas in notificados.items():
        for alerta_id, registro in alertas.items():
            if not registro.get("notify", False):
                mensaje = f"{registro['message']} - {registro['date']}"
                print(f"🔔 ALERTA del grupo {grupo_id}: {mensaje}")
                mostrar_notificacion("Alerta del sistema", mensaje)
                reproducir_sonido()
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