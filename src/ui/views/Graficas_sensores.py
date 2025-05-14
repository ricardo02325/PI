import sys
import os
import cv2
import tkinter as tk
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import customtkinter as ctk
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates
from matplotlib.ticker import MaxNLocator

# Añadir el path al proyecto si es necesario
sys.path.append('C:\\Users\\Colibecas\\Desktop\\PI')

VIDEO_PATH = os.path.join(os.path.dirname(__file__), "video.mp4")

def obtener_datos():
    """Obtiene los datos desde MySQL y los devuelve en un DataFrame."""
    try:
        db = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="",
            database="sistema_hidroponico"
        )
        
        query = """
        SELECT 
            s.tipo_sensor, 
            l.valor, 
            l.fecha_hora
        FROM 
            lecturas_sensores l
        JOIN 
            sensores s ON l.id_sensor = s.id_sensor
        WHERE 
            LOWER(s.tipo_sensor) IN ('ph', 'conductividad_elec', 'temperatura')
        ORDER BY 
            l.fecha_hora;
        """
        cursor = db.cursor(dictionary=True)
        cursor.execute(query)
        datos = cursor.fetchall()
        cursor.close()
        db.close()
        
        df = pd.DataFrame(datos)
        if df.empty:
            print("⚠ No se encontraron datos en la base de datos.")
            return None
        
        df['tipo_sensor'] = df['tipo_sensor'].str.lower().str.strip()
        df['fecha_hora'] = pd.to_datetime(df['fecha_hora'])
        df['valor'] = pd.to_numeric(df['valor'], errors='coerce')

        return df
    except mysql.connector.Error as err:
        print(f"❌ Error de conexión: {err}")
        return None

def abrir_ayuda():
    """Abre una ventana emergente que reproduce un video de ayuda."""
    ayuda = tk.Toplevel()
    ayuda.title("Ayuda en Video")
    ayuda.geometry("700x500")
    ayuda.resizable(False, False)

    label_video = tk.Label(ayuda)
    label_video.pack()

    cap = cv2.VideoCapture(VIDEO_PATH)

    def reproducir():
        ret, frame = cap.read()
        if ret:
            frame = cv2.resize(frame, (700, 500))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            imagen = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=imagen)
            label_video.imgtk = imgtk
            label_video.configure(image=imgtk)
            ayuda.after(33, reproducir)
        else:
            cap.release()
            ayuda.destroy()

    reproducir()

def iniciar_graficas(frame):
    ctk.set_appearance_mode("light")  
    ctk.set_default_color_theme("dark-blue")  
    plt.style.use('seaborn-v0_8')
    frame.configure(fg_color="#f8f9fa")

    encabezado_frame = ctk.CTkFrame(frame, fg_color="transparent")
    encabezado_frame.pack(side="top", fill="x", pady=(20, 10))
    encabezado_frame.grid_columnconfigure(0, weight=1)
    encabezado_frame.grid_columnconfigure(1, weight=0)

    bienvenido_label = ctk.CTkLabel(
        encabezado_frame, 
        text="Panel de Monitoreo Hidropónico",  
        font=("Arial", 24, "bold"),  
        text_color="#2c3e50"
    )
    bienvenido_label.grid(row=0, column=0, sticky="ew")

    boton_ayuda = ctk.CTkButton(
        encabezado_frame, 
        text="?", 
        width=30, 
        font=("Arial", 18, "bold"), 
        command=abrir_ayuda
    )
    boton_ayuda.grid(row=0, column=1, padx=10)

    lecturas_frame = ctk.CTkFrame(frame, fg_color="transparent")
    lecturas_frame.pack(side="top", fill="x", pady=(0, 15), padx=20)

    sensores_config = {
        'ph': {'nombre': 'pH', 'color': '#3498db', 'unidad': '', 'rango': (0, 14)},
        'conductividad_elec': {'nombre': 'Conductividad', 'color': '#2ecc71', 'unidad': 'µS/cm', 'rango': (0, 2000)},
        'temperatura': {'nombre': 'Temperatura', 'color': '#e74c3c', 'unidad': '°C', 'rango': (10, 40)}
    }

    etiquetas_lectura = {}

    for sensor_db, config in sensores_config.items():
        cuadro = ctk.CTkFrame(
            lecturas_frame, 
            fg_color="#ffffff",
            corner_radius=12, 
            border_color="#e0e0e0",
            border_width=1, 
            width=180, 
            height=100
        )
        cuadro.pack_propagate(False)  
        cuadro.pack(side="left", padx=10, pady=5, expand=True)

        titulo = ctk.CTkLabel(
            cuadro, 
            text=config['nombre'],  
            font=("Arial", 14, "bold"), 
            text_color=config['color'],
            justify="center"
        )
        titulo.pack(pady=(10, 0))

        valor = ctk.CTkLabel(
            cuadro, 
            text="--",  
            font=("Arial", 24, "bold"), 
            text_color="#2c3e50",
            justify="center"
        )
        valor.pack(expand=True)

        unidad = ctk.CTkLabel(
            cuadro, 
            text=config['unidad'],  
            font=("Arial", 12), 
            text_color="#7f8c8d",
            justify="center"
        )
        unidad.pack(pady=(0, 10))

        etiquetas_lectura[sensor_db] = valor

    fig = plt.figure(figsize=(20, 4.5), facecolor='#f8f9fa')
    gs = fig.add_gridspec(1, 3, wspace=0.25)
    axes = [fig.add_subplot(gs[0, i]) for i in range(3)]

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.get_tk_widget().pack(side="bottom", fill="both", expand=True, padx=15, pady=(0, 15))

    def actualizar_graficas():
        df = obtener_datos()
        if df is None or df.empty:
            for ax in axes:
                ax.clear()
                ax.set_facecolor('#f8f9fa')
                ax.text(0.5, 0.5, "No hay datos disponibles", 
                        fontsize=14, ha='center', va='center', 
                        color='#7f8c8d', transform=ax.transAxes)
                ax.set_frame_on(False)
            for sensor_db in etiquetas_lectura:
                etiquetas_lectura[sensor_db].configure(text="--")
            canvas.draw_idle()
            frame.after(10000, actualizar_graficas)
            return

        df = df.sort_values(by='fecha_hora')

        for i, (sensor_db, ax) in enumerate(zip(sensores_config.keys(), axes)):
            df_tipo = df[df['tipo_sensor'] == sensor_db]
            config = sensores_config[sensor_db]

            ax.clear()

            if not df_tipo.empty:
                ax.plot(df_tipo['fecha_hora'], df_tipo['valor'], 
                        color=config['color'], linewidth=2.5, 
                        marker='o', markersize=6,
                        markerfacecolor='white',
                        markeredgecolor=config['color'],
                        markeredgewidth=2)

                ax.fill_between(df_tipo['fecha_hora'], df_tipo['valor'], alpha=0.1, color=config['color'])

                ax.set_ylim(config['rango'])
                ax.yaxis.set_major_locator(MaxNLocator(5))
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y %H:%M'))
                plt.setp(ax.get_xticklabels(), rotation=30, ha='right', fontsize=8)

                ax.set_title(config['nombre'], fontsize=13, pad=10, fontweight='bold', color=config['color'])
                ax.set_xlabel('Fecha y Hora', fontsize=9, labelpad=8, color='#7f8c8d')
                ax.set_ylabel(config['unidad'], fontsize=9, labelpad=8, color='#7f8c8d')

                ax.grid(True, linestyle=':', alpha=0.5, color='#e0e0e0')
                ax.set_facecolor('#ffffff')
                for spine in ax.spines.values():
                    spine.set_edgecolor('#e0e0e0')
                    spine.set_linewidth(0.8)

                valor_actual = df_tipo['valor'].iloc[-1]
                etiquetas_lectura[sensor_db].configure(text=f"{valor_actual:.1f}")
            else:
                ax.text(0.5, 0.5, f"No hay datos de {config['nombre']}", 
                        fontsize=12, ha='center', va='center', 
                        color='#7f8c8d', transform=ax.transAxes)
                ax.set_frame_on(False)
                etiquetas_lectura[sensor_db].configure(text="--")

        fig.tight_layout(pad=2.0)
        canvas.draw_idle()
        frame.after(10000, actualizar_graficas)

    actualizar_graficas()
