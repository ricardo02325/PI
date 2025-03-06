import sys
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))
    fig.tight_layout(pad=5.0)
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.get_tk_widget().pack(fill="both", expand=True)

    def actualizar_graficas(frame):
        ax1.clear()
        ax2.clear()
        ax3.clear()

        ax1.set_title('Nivel de pH')
        ax1.set_xlabel('Fecha y Hora')
        ax1.set_ylabel('Valor de pH')
        ax1.grid(True, linestyle='--', alpha=0.6)

        ax2.set_title('Conductividad Eléctrica')
        ax2.set_xlabel('Fecha y Hora')
        ax2.set_ylabel('Valor (mS/cm)')
        ax2.grid(True, linestyle='--', alpha=0.6)

        ax3.set_title('Temperatura')
        ax3.set_xlabel('Fecha y Hora')
        ax3.set_ylabel('Temperatura (°C)')
        ax3.grid(True, linestyle='--', alpha=0.6)

        df = obtener_datos()
        if df is None:
            for ax in [ax1, ax2, ax3]:
                ax.text(0.5, 0.5, "No hay datos disponibles", fontsize=14, ha='center', va='center', transform=ax.transAxes)
                ax.set_xlim(0, 1)
                ax.set_ylim(0, 1)
            canvas.draw()
            return
        
        # Graficar pH
        df_ph = df[df['tipo_sensor'] == 'pH']
        if not df_ph.empty:
            ax1.plot(df_ph['fecha_hora'], df_ph['valor'], label="pH", color='dodgerblue', linewidth=2)
            ax1.scatter(df_ph['fecha_hora'], df_ph['valor'], color='blue', edgecolors='black', s=50)
            ax1.legend()

        # Graficar Conductividad Eléctrica
        df_ce = df[df['tipo_sensor'] == 'Conductividad eléctrica']
        if not df_ce.empty:
            ax2.plot(df_ce['fecha_hora'], df_ce['valor'], label="Conductividad Eléctrica", color='limegreen', linewidth=2)
            ax2.scatter(df_ce['fecha_hora'], df_ce['valor'], color='green', edgecolors='black', s=50)
            ax2.legend()

        # Graficar Temperatura
        df_temp = df[df['tipo_sensor'] == 'Temperatura']
        if not df_temp.empty:
            ax3.plot(df_temp['fecha_hora'], df_temp['valor'], label="Temperatura", color='tomato', linewidth=2)
            ax3.scatter(df_temp['fecha_hora'], df_temp['valor'], color='red', edgecolors='black', s=50)
            ax3.legend()
        
        canvas.draw()
<<<<<<< HEAD

    ani = animation.FuncAnimation(fig, actualizar_graficas, interval=5000)
=======
    
    ani = animation.FuncAnimation(fig, actualizar_graficas, interval=5000)
>>>>>>> 32a6936cef92d92c2d2f7ff7f472316f6f551129
