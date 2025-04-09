from notifypy import Notify

notification = Notify()
notification.title = "Alerta"
notification.message = "La conductividad electrica esta muy alta"
notification.audio = "C:\\Users\\Colibecas\\Desktop\\PI\\src\\ui\\views\\sonido_alertas.wav"
notification.icon = "C:\\Users\\Colibecas\\Desktop\\PI\\src\\ui\\views\\test_images\\noti.png"


notification.send()