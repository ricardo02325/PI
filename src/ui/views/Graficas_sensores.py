import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    

def iniciar_graficas(frame):
    ctk.set_appearance_mode("dark")  
    ctk.set_default_color_theme("blue")  
    style.use('ggplot')

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))
    fig.tight_layout(pad=5.0)
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.get_tk_widget().pack(fill="both", expand=True)

    def obtener_datos():
        """Obtiene los datos desde MySQL y los devuelve como un DataFrame."""
        db = mysql.connector.connect(**DB_CONFIG)

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
        db.close()

        df = pd.DataFrame(datos)
        if df.empty:
            return None
        
        df['fecha_hora'] = pd.to_datetime(df['fecha_hora'])
        return df

    def actualizar_graficas(frame):
        """Actualiza las tres gráficas en tiempo real."""
        ax1.clear()
        ax2.clear()
        ax3.clear()

        ax1.set_title('Nivel de pH', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Fecha y Hora', fontsize=12)
        ax1.set_ylabel('Valor de pH', fontsize=12)
        ax1.grid(True, linestyle='--', alpha=0.6)

        ax2.set_title('Conductividad Eléctrica', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Fecha y Hora', fontsize=12)
        ax2.set_ylabel('Valor (mS/cm)', fontsize=12)
        ax2.grid(True, linestyle='--', alpha=0.6)

        ax3.set_title('Temperatura', fontsize=14, fontweight='bold')
        ax3.set_xlabel('Fecha y Hora', fontsize=12)
        ax3.set_ylabel('Temperatura (°C)', fontsize=12)
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
            df_ph = df_ph.sort_values(by='fecha_hora')
            ax1.plot(df_ph['fecha_hora'], df_ph['valor'], label="pH", color='dodgerblue', linewidth=2)
            ax1.scatter(df_ph['fecha_hora'], df_ph['valor'], color='blue', edgecolors='black', s=50)
            ax1.legend()
        else:
            ax1.set_ylim(0, 14) 

        # Graficar Conductividad Eléctrica
        df_ce = df[df['tipo_sensor'] == 'Conductividad eléctrica']
        if not df_ce.empty:
            df_ce = df_ce.sort_values(by='fecha_hora')
            ax2.plot(df_ce['fecha_hora'], df_ce['valor'], label="Conductividad Eléctrica", color='limegreen', linewidth=2)
            ax2.scatter(df_ce['fecha_hora'], df_ce['valor'], color='green', edgecolors='black', s=50)
            ax2.legend()
        else:
            ax2.set_ylim(0, 10) 

        # Graficar Temperatura
        df_temp = df[df['tipo_sensor'] == 'Temperatura']
        if not df_temp.empty:
            df_temp = df_temp.sort_values(by='fecha_hora')
            ax3.plot(df_temp['fecha_hora'], df_temp['valor'], label="Temperatura", color='tomato', linewidth=2)
            ax3.scatter(df_temp['fecha_hora'], df_temp['valor'], color='red', edgecolors='black', s=50)
            ax3.legend()
        else:
            ax3.set_ylim(0, 50)  

        canvas.draw()

    ani = animation.FuncAnimation(fig, actualizar_graficas, interval=5000)