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
import matplotlib.patheffects as patheffects
from matplotlib import font_manager

# Configuración inicial
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")
plt.style.use('seaborn-v0_8')

# Configurar fuente compatible con emojis
try:
    font_manager.fontManager.addfont('seguiemj.ttf')
    plt.rcParams['font.family'] = 'Segoe UI Emoji'
except:
    print("No se pudo cargar la fuente Segoe UI Emoji, usando fuente predeterminada")

# Cargar iconos (asegúrate de tener estos archivos en tu directorio)
ICON_PH = "ph_icon.png"
ICON_CE = "conductividad_icon.png"
ICON_TEMP = "temperatura_icon.png"
ICON_PROF = "profundidad_icon.png"

def cargar_icono(ruta, size=(24,24)):
    try:
        img = Image.open(ruta)
        img = img.resize(size, Image.LANCZOS)
        return ImageTk.PhotoImage(img)
    except:
        return None

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
            LOWER(s.tipo_sensor) IN ('ph', 'conductividad_elec', 'temperatura', 'profundidad')
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
    # Configuración del frame principal
    frame.configure(fg_color="#f5f7fa")
    frame.grid_rowconfigure(1, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    
    # --- ENCABEZADO MEJORADO ---
    encabezado_frame = ctk.CTkFrame(frame, fg_color="transparent", height=80)
    encabezado_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=(10, 0))
    
    titulo_frame = ctk.CTkFrame(encabezado_frame, fg_color="transparent")
    titulo_frame.pack(side="left", fill="both", expand=True)
    
    bienvenido_label = ctk.CTkLabel(
        titulo_frame,
        text="MONITOREO HIDROPÓNICO",
        font=("Montserrat", 22, "bold"),
        text_color="#2c3e50"
    )
    bienvenido_label.pack(side="left", padx=(20, 0))
    
    boton_ayuda = ctk.CTkButton(
        encabezado_frame,
        text="Ayuda",
        width=80,
        height=30,
        font=("Montserrat", 12, "bold"),
        fg_color="#3498db",
        hover_color="#2980b9",
        command=abrir_ayuda
    )
    boton_ayuda.pack(side="right", padx=20)

    # --- CONTENEDOR PRINCIPAL ---
    main_container = ctk.CTkFrame(frame, fg_color="transparent")
    main_container.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
    main_container.grid_rowconfigure(0, weight=1)
    main_container.grid_columnconfigure(0, weight=1)
    main_container.grid_columnconfigure(1, weight=1)  # Gráficas menos anchas
    
    # --- PANEL IZQUIERDO (LECTURAS) ---
    left_panel = ctk.CTkFrame(main_container, fg_color="transparent", width=280)  # Ancho reducido
    left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 15))  # Menos padding
    left_panel.grid_rowconfigure(0, weight=1)
    
    # --- CONTENEDOR DE TARJETAS CENTRADO ---
    card_container = ctk.CTkFrame(left_panel, fg_color="transparent")
    card_container.pack(expand=True, fill="both", pady=15)  # Menos espacio vertical
    
    # --- TARJETAS DE VALORES ACTUALES CON ICONOS ---
    valores_frame = ctk.CTkFrame(card_container, fg_color="transparent")
    valores_frame.pack(expand=True, fill="both", anchor="center")
    
    # Configuración de sensores con emojis
    sensores_config = {
        'ph': {
            'nombre': 'pH', 
            'color': '#3498db', 
            'unidad': '', 
            'rango': (0, 14), 
            'icon': '🧪'  # Emoji para pH
        },
        'conductividad_elec': {
            'nombre': 'Conductividad', 
            'color': '#2ecc71', 
            'unidad': 'µS/cm', 
            'rango': (0, 2000), 
            'icon': '⚡'  # Emoji para conductividad
        },
        'temperatura': {
            'nombre': 'Temperatura', 
            'color': '#e74c3c', 
            'unidad': '°C', 
            'rango': (10, 40), 
            'icon': '🌡️'  # Emoji para temperatura
        },
        'profundidad': {
            'nombre': 'Profundidad', 
            'color': '#9b59b6', 
            'unidad': 'cm', 
            'rango': (0, 100), 
            'icon': '📏'  # Emoji para profundidad
        }
    }


    etiquetas_lectura = {}
    iconos = {}  # Para mantener referencia a los iconos
    
    for sensor_db, config in sensores_config.items():
        cuadro = ctk.CTkFrame(
            valores_frame, 
            fg_color="white",
            border_width=1,
            border_color="#e0e0e0",
            corner_radius=12
        )
        cuadro.pack(fill="x", pady=(0, 12), ipady=8, ipadx=8)  # Menos espacio entre tarjetas
        
        content_frame = ctk.CTkFrame(cuadro, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=12, pady=12)  # Padding interno reducido
        
        top_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        top_frame.pack(fill="x")
        
        # Mostrar icono (imagen o texto alternativo)
        if isinstance(config['icon'], str):
            icono = ctk.CTkLabel(
                top_frame, 
                text=config['icon'], 
                font=("Montserrat", 14, "bold"),
                width=30,
                text_color=config['color']
            )
        else:
            icono = ctk.CTkLabel(top_frame, image=config['icon'], text="")
            iconos[sensor_db] = config['icon']  # Mantener referencia
        
        icono.pack(side="left", padx=(0, 8))
        
        nombre = ctk.CTkLabel(
            top_frame, 
            text=config['nombre'], 
            font=("Montserrat", 12, "bold"), 
            text_color="#34495e"
        )
        nombre.pack(side="left")
        
        valor = ctk.CTkLabel(
            content_frame, 
            text="--", 
            font=("Montserrat", 24, "bold"), 
            text_color=config['color'],
            pady=4  # Menos espacio
        )
        valor.pack()
        
        unidad = ctk.CTkLabel(
            content_frame, 
            text=config['unidad'], 
            font=("Montserrat", 18), 
            text_color="#7f8c8d"
        )
        unidad.pack()
        
        etiquetas_lectura[sensor_db] = valor

    # --- PANEL DERECHO (GRÁFICAS MEJORADAS) ---
    right_panel = ctk.CTkFrame(main_container, fg_color="transparent")
    right_panel.grid(row=0, column=1, sticky="nsew")
    right_panel.grid_rowconfigure(0, weight=1)
    right_panel.grid_columnconfigure(0, weight=1)
    
    graphs_container = ctk.CTkFrame(right_panel, fg_color="white", corner_radius=12)
    graphs_container.pack(fill="both", expand=True, padx=0, pady=0)
    
    # Configuración de figura para gráficas más estrechas y altas
    fig = plt.figure(figsize=(4.5, 7), facecolor='white', dpi=100)  # Más estrechas y altas
    gs = fig.add_gridspec(4, 1, hspace=0.5)  # Menos espacio entre gráficas
    axes = [fig.add_subplot(gs[i]) for i in range(4)]
    
    canvas = FigureCanvasTkAgg(fig, master=graphs_container)
    canvas.get_tk_widget().pack(fill="both", expand=True, padx=8, pady=8)  # Menos padding

    def actualizar_graficas():
        """Actualiza las gráficas con los datos más recientes"""
        df = obtener_datos()
        if df is None or df.empty:
            for ax in axes:
                ax.clear()
                ax.set_facecolor('white')
                ax.text(0.5, 0.5, "Sin datos", fontsize=10,
                       ha='center', va='center', color='#95a5a6', transform=ax.transAxes)
                ax.grid(True, color='#f0f0f0', linestyle=':', linewidth=0.7, alpha=0.5)
                for spine in ax.spines.values():
                    spine.set_color('#e0e0e0')
                    spine.set_linewidth(0.7)
            
            for sensor_db in etiquetas_lectura:
                etiquetas_lectura[sensor_db].configure(text="--")
            
            canvas.draw()
            frame.after(10000, actualizar_graficas)
            return
        
        df['fecha_hora'] = pd.to_datetime(df['fecha_hora'])
        df = df.sort_values(by='fecha_hora')
        
        # Configuración de estilo mejorado para mayor claridad
        plt.style.use('seaborn-v0_8')
        plt.rcParams['axes.facecolor'] = 'white'
        plt.rcParams['axes.edgecolor'] = '#e0e0e0'
        plt.rcParams['grid.color'] = '#f0f0f0'
        plt.rcParams['grid.alpha'] = 0.5
        plt.rcParams['grid.linestyle'] = ':'
        
        for i, (sensor_db, ax) in enumerate(zip(sensores_config.keys(), axes)):
            config = sensores_config[sensor_db]
            df_sensor = df[df['tipo_sensor'] == sensor_db]
            
            ax.clear()
            
            if not df_sensor.empty:
                x = df_sensor['fecha_hora']
                y = df_sensor['valor']
                
                # Línea más gruesa para mejor visibilidad
                ax.plot(x, y, color=config['color'], linewidth=2.5, alpha=0.9, zorder=3,
                       path_effects=[patheffects.withStroke(linewidth=4, foreground='white')])
                
                # Relleno más sutil
                ax.fill_between(x, y, color=config['color'], alpha=0.05, zorder=2)
                
                # Destacar el último valor con marcador más visible
                last_x, last_y = x.iloc[-1], y.iloc[-1]
                ax.scatter(last_x, last_y, s=120, color='white', 
                          edgecolor=config['color'], linewidth=2.5, zorder=5)
                ax.scatter(last_x, last_y, s=50, color=config['color'], zorder=6)
                
                # Etiqueta del último valor más clara
                ax.annotate(f'{last_y:.1f}', xy=(last_x, last_y), xytext=(6, 6),
                           textcoords='offset points', color=config['color'],
                           fontsize=10, weight='bold', zorder=10,
                           bbox=dict(boxstyle='round,pad=0.3', fc='white', 
                                   ec=config['color'], lw=0.8, alpha=0.9))
                
                # Configuración del eje con mejor visibilidad
                ax.set_ylim(config['rango'])
                ax.set_title(f"{config['nombre']}", fontsize=11, fontweight='bold',
                           pad=5, color=config['color'], loc='left')
                
                # Formato de fechas más compacto
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M\n%d/%m'))
                ax.tick_params(axis='x', labelsize=8, pad=2)
                ax.tick_params(axis='y', labelsize=9, pad=2)
                
                # Grid más sutil
                ax.grid(True, color='#f0f0f0', linestyle=':', linewidth=0.7, alpha=0.5)
                
                # Bordes más definidos
                for spine in ax.spines.values():
                    spine.set_visible(True)
                    spine.set_color('#e0e0e0')
                    spine.set_linewidth(0.8)
                
                # Actualizar valor en tarjeta
                last_val = y.iloc[-1]
                etiquetas_lectura[sensor_db].configure(text=f"{last_val:.1f}")
                
                # Animación de cambio de valor más notoria
                current_text = etiquetas_lectura[sensor_db].cget("text")
                try:
                    current_val = float(current_text)
                except:
                    current_val = 0
                
                if abs(float(last_val) - current_val) > 0.1:
                    etiquetas_lectura[sensor_db].configure(text_color="#e74c3c")
                    etiquetas_lectura[sensor_db].after(500, lambda s=sensor_db: 
                        etiquetas_lectura[s].configure(text_color=sensores_config[s]['color']))
            else:
                ax.text(0.5, 0.5, "Datos no disponibles", fontsize=9,
                       ha='center', va='center', color='#95a5a6', transform=ax.transAxes)
                etiquetas_lectura[sensor_db].configure(text="--")
        
        fig.tight_layout(pad=2.0)
        canvas.draw()
        frame.after(10000, actualizar_graficas)

    # Iniciar la actualización de gráficas
    actualizar_graficas()