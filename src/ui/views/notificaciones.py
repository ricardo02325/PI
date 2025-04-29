import sqlite3
from notifypy import Notify

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
