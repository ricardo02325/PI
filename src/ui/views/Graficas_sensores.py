import sys
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Aseguramos que ani se mantenga en memoria
ani = None

sys.path.append('C:\\Users\\Colibecas\\Desktop\\PI')

def obtener_datos():
    """Establece la conexión manualmente y obtiene los datos desde MySQL."""
    try:
        db = mysql.connector.connect(
            host="127.0.0.1",
            user="root",  # Cambia por tu usuario de MySQL
            password="",  # Cambia por tu contraseña si tienes
            database="sistema_hidroponico"
        )
        
        query = """
            SELECT s.tipo_sensor, l.valor, l.fecha_hora
            FROM lecturas_sensores l
            JOIN sensores s ON l.id_sensor = s.id_sensor
            WHERE s.tipo_sensor IN ('pH', 'Conductividad eléctrica', 'Temperatura')
            ORDER BY l.fecha_hora
        """
        
        cursor = db.cursor(dictionary=True)
        cursor.execute(query)
        datos = cursor.fetchall()
        cursor.close()
        db.close()
        
        df = pd.DataFrame(datos)
        if df.empty:
            return None
        
        df['fecha_hora'] = pd.to_datetime(df['fecha_hora'])
        return df
    except mysql.connector.Error as err:
        print(f"Error de conexión: {err}")
        return None

def iniciar_graficas(frame):
    ctk.set_appearance_mode("dark")  
    ctk.set_default_color_theme("blue")  
    style.use('ggplot')

    # Crear la figura y los ejes una sola vez
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(30, 5))
    fig.tight_layout(pad=5.0)
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.get_tk_widget().pack(fill="both", expand=True)

    def actualizar_graficas(_):
        df = obtener_datos()
        if df is None or df.empty:
            # Si no hay datos, mostrar mensaje en los tres gráficos
            for ax in [ax1, ax2, ax3]:
                ax.cla()  # Limpia solo los datos, manteniendo títulos y etiquetas
                ax.text(0.5, 0.5, "No hay datos disponibles", fontsize=14, ha='center', va='center', transform=ax.transAxes)
            canvas.draw()
            return

        # Limpia los gráficos anteriores
        for ax in [ax1, ax2, ax3]:
            ax.cla()

        # Graficar los datos para cada tipo de sensor
        for tipo, ax, color in [('pH', ax1, 'blue'), ('Conductividad eléctrica', ax2, 'green'), ('Temperatura', ax3, 'red')]:
            df_tipo = df[df['tipo_sensor'] == tipo]
            if not df_tipo.empty:
                ax.plot(df_tipo['fecha_hora'], df_tipo['valor'], color=color, linewidth=2, label=tipo)
                ax.scatter(df_tipo['fecha_hora'], df_tipo['valor'], color=color, s=50)
                ax.legend()

        canvas.draw()

    global ani  # Necesario para que la variable no sea eliminada
    if ani is None:  # Solo crear la animación si aún no existe
        ani = animation.FuncAnimation(fig, actualizar_graficas, interval=5000, cache_frame_data=False)