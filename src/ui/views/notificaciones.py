from notifypy import Notify

notification = Notify()
notification.title = "Cool Title"
notification.message = "Even cooler message."
notification.audio = "C:\\Users\\Colibecas\\Desktop\\PI\\src\\ui\\views\\sonido_alertas.wav"

notification.send()