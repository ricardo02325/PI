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
from datetime import datetime, timedelta
import webbrowser
from tkinter import filedialog

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

# Configuración de sensores (definida a nivel global)
sensores_config = {
    'ph': {
        'nombre': 'pH', 
        'color': '#3498db', 
        'unidad': '', 
        'rango': (0, 14), 
        'icon': '🧪'
    },
    'conductividad_elec': {
        'nombre': 'Conductividad', 
        'color': '#2ecc71', 
        'unidad': 'µS/cm', 
        'rango': (0, 2000), 
        'icon': '⚡'
    },
    'temperatura': {
        'nombre': 'Temperatura', 
        'color': '#e74c3c', 
        'unidad': '°C', 
        'rango': (10, 40), 
        'icon': '🌡️'
    },
    'profundidad': {
        'nombre': 'Profundidad', 
        'color': '#9b59b6', 
        'unidad': 'cm', 
        'rango': (0, 100), 
        'icon': '📏'
    }
}

# Variables globales para mantener referencia a los elementos gráficos
global canvas, axes, fig, graphs_container
canvas = None
axes = None
fig = None
graphs_container = None

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

def mostrar_graficas(frame_destino):
    """Muestra las gráficas en el frame especificado"""
    global canvas, axes, fig, graphs_container
    
    # Limpiar el frame de destino
    for widget in frame_destino.winfo_children():
        widget.destroy()
    
    # Crear contenedor para gráficas
    graphs_container = ctk.CTkFrame(frame_destino, fg_color="white", corner_radius=12)
    graphs_container.pack(fill="both", expand=True, padx=0, pady=0)
    
    # Configuración de figura para gráficas
    fig = plt.figure(figsize=(4.5, 7), facecolor='white', dpi=100)
    gs = fig.add_gridspec(4, 1, hspace=0.5)
    axes = [fig.add_subplot(gs[i]) for i in range(4)]
    
    canvas = FigureCanvasTkAgg(fig, master=graphs_container)
    canvas.get_tk_widget().pack(fill="both", expand=True, padx=8, pady=8)
    
    # Actualizar gráficas inmediatamente
    actualizar_graficas()

def actualizar_graficas():
    """Actualiza las gráficas con los datos más recientes"""
    global canvas, axes, fig
    
    if canvas is None or axes is None or fig is None:
        return
    
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
        
        canvas.draw()
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
        else:
            ax.text(0.5, 0.5, "Datos no disponibles", fontsize=9,
                   ha='center', va='center', color='#95a5a6', transform=ax.transAxes)
    
    fig.tight_layout(pad=2.0)
    canvas.draw()

def generar_reporte_semanal(frame_reporte):
    """Genera un reporte semanal en formato HTML con gráficas y estadísticas"""
    try:
        # Limpiar el frame de reporte
        for widget in frame_reporte.winfo_children():
            widget.destroy()
            
        # Frame para controles
        controles_frame = ctk.CTkFrame(frame_reporte, fg_color="transparent")
        controles_frame.pack(fill="x", padx=10, pady=10)
        
        # Botón para regresar a gráficas
        btn_regresar = ctk.CTkButton(
            controles_frame,
            text="← Regresar a Gráficas",
            width=150,
            height=30,
            font=("Montserrat", 12, "bold"),
            fg_color="#95a5a6",
            hover_color="#7f8c8d",
            command=lambda: mostrar_graficas(frame_reporte)
        )
        btn_regresar.pack(side="left", padx=5)
        
        # Mostrar mensaje de generación
        label_generando = ctk.CTkLabel(
            frame_reporte, 
            text="Generando reporte...", 
            font=("Montserrat", 14)
        )
        label_generando.pack(pady=20)
        frame_reporte.update()
        
        # Obtener fecha de inicio (hace 7 días) y fin (hoy)
        fecha_fin = datetime.now()
        fecha_inicio = fecha_fin - timedelta(days=7)
        
        db = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="",
            database="sistema_hidroponico"
        )
        
        query = f"""
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
            AND l.fecha_hora BETWEEN '{fecha_inicio.strftime('%Y-%m-%d')}' AND '{fecha_fin.strftime('%Y-%m-%d 23:59:59')}'
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
            label_generando.configure(text="⚠ No se encontraron datos para generar el reporte.")
            return
        
        df['tipo_sensor'] = df['tipo_sensor'].str.lower().str.strip()
        df['fecha_hora'] = pd.to_datetime(df['fecha_hora'])
        df['valor'] = pd.to_numeric(df['valor'], errors='coerce')
        
        # Crear gráficas para el reporte
        fig_reporte, axes_reporte = plt.subplots(4, 1, figsize=(10, 12))
        stats_html = ""
        
        for i, (sensor_db, config) in enumerate(sensores_config.items()):
            df_sensor = df[df['tipo_sensor'] == sensor_db]
            
            if not df_sensor.empty:
                ax = axes_reporte[i]
                x = df_sensor['fecha_hora']
                y = df_sensor['valor']
                
                ax.plot(x, y, color=config['color'], linewidth=2)
                ax.set_title(f"{config['nombre']} - Semana {fecha_inicio.strftime('%d/%m')} al {fecha_fin.strftime('%d/%m')}")
                ax.set_ylabel(f"{config['nombre']} ({config['unidad']})")
                ax.grid(True, alpha=0.3)
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m %H:%M'))
                
                # Calcular estadísticas
                stats = {
                    'Mínimo': y.min(),
                    'Máximo': y.max(),
                    'Promedio': y.mean(),
                    'Mediana': y.median(),
                    'Último valor': y.iloc[-1]
                }
                
                stats_html += f"""
                <div style="background-color: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 5px;">
                    <h3 style="color: {config['color']}; margin-top: 0;">{config['nombre']}</h3>
                    <ul style="list-style-type: none; padding-left: 0;">
                        <li>📉 <strong>Mínimo:</strong> {stats['Mínimo']:.2f} {config['unidad']}</li>
                        <li>📈 <strong>Máximo:</strong> {stats['Máximo']:.2f} {config['unidad']}</li>
                        <li>📊 <strong>Promedio:</strong> {stats['Promedio']:.2f} {config['unidad']}</li>
                        <li>🔍 <strong>Mediana:</strong> {stats['Mediana']:.2f} {config['unidad']}</li>
                        <li>🔄 <strong>Último valor:</strong> {stats['Último valor']:.2f} {config['unidad']}</li>
                    </ul>
                </div>
                """
        
        # Guardar gráficas como imagen
        fig_reporte.tight_layout()
        img_path = os.path.join(os.path.dirname(__file__), "reporte_semanal.png")
        fig_reporte.savefig(img_path, dpi=100)
        plt.close(fig_reporte)
        
        # Crear HTML del reporte
        reporte_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Reporte Semanal Hidropónico</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ background-color: #2c3e50; color: white; padding: 20px; text-align: center; border-radius: 5px; }}
                .content {{ margin-top: 20px; }}
                .graph {{ text-align: center; margin: 20px 0; }}
                .stats {{ display: flex; flex-wrap: wrap; justify-content: space-between; }}
                .footer {{ margin-top: 20px; text-align: center; font-size: 12px; color: #7f8c8d; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>📊 Reporte Semanal Hidropónico</h1>
                <p>Período: {fecha_inicio.strftime('%d/%m/%Y')} al {fecha_fin.strftime('%d/%m/%Y')}</p>
            </div>
            
            <div class="content">
                <div class="graph">
                    <img src="reporte_semanal.png" style="max-width: 100%;">
                </div>
                
                <h2>📋 Estadísticas Resumidas</h2>
                <div class="stats">
                    {stats_html}
                </div>
            </div>
            
            <div class="footer">
                <p>Generado automáticamente el {datetime.now().strftime('%d/%m/%Y a las %H:%M')}</p>
            </div>
        </body>
        </html>
        """
        
        # Guardar el reporte HTML
        reporte_path = os.path.join(os.path.dirname(__file__), "reporte_semanal.html")
        with open(reporte_path, 'w', encoding='utf-8') as f:
            f.write(reporte_html)
        
        # Mostrar botones en el frame de reporte
        label_generando.destroy()
        
        # Frame para botones de acción
        botones_accion = ctk.CTkFrame(frame_reporte, fg_color="transparent")
        botones_accion.pack(fill="x", padx=20, pady=10)
        
        # Botón para abrir reporte
        btn_abrir_reporte = ctk.CTkButton(
            botones_accion,
            text="Abrir Reporte en Navegador",
            command=lambda: webbrowser.open(reporte_path),
            fg_color="#3498db",
            hover_color="#2980b9",
            font=("Montserrat", 12, "bold")
        )
        btn_abrir_reporte.pack(side="left", padx=5, pady=5, fill='x', expand=True)
        
        # Botón para generar nuevo reporte
        btn_nuevo_reporte = ctk.CTkButton(
            botones_accion,
            text="Generar Nuevo Reporte",
            command=lambda: generar_reporte_semanal(frame_reporte),
            fg_color="#2ecc71",
            hover_color="#27ae60",
            font=("Montserrat", 12, "bold")
        )
        btn_nuevo_reporte.pack(side="left", padx=5, pady=5, fill='x', expand=True)
        
    except Exception as e:
        for widget in frame_reporte.winfo_children():
            widget.destroy()
            
        ctk.CTkLabel(
            frame_reporte, 
            text=f"❌ Error al generar reporte: {str(e)}",
            font=("Montserrat", 12)
        ).pack(pady=20)

def ver_historico_semanal(frame_historico):
    """Muestra datos históricos de semanas pasadas en el frame proporcionado"""
    # Limpiar frame de histórico
    for widget in frame_historico.winfo_children():
        widget.destroy()
    
    # Frame para controles
    controles_frame = ctk.CTkFrame(frame_historico, fg_color="transparent")
    controles_frame.pack(fill="x", padx=10, pady=10)
    
    # Botón para regresar a gráficas
    btn_regresar = ctk.CTkButton(
        controles_frame,
        text="← Regresar a Gráficas",
        width=150,
        height=30,
        font=("Montserrat", 12, "bold"),
        fg_color="#95a5a6",
        hover_color="#7f8c8d",
        command=lambda: mostrar_graficas(frame_historico)
    )
    btn_regresar.pack(side="left", padx=5)
    
    # Selector de semanas atrás
    ctk.CTkLabel(controles_frame, text="Semanas atrás:").pack(side="left", padx=5)
    semanas_var = tk.IntVar(value=1)
    semanas_spin = ctk.CTkOptionMenu(controles_frame, variable=semanas_var, values=[str(i) for i in range(1, 13)])
    semanas_spin.pack(side="left", padx=5)
    
    # Botón para cargar datos
    btn_cargar = ctk.CTkButton(
        controles_frame,
        text="Cargar Datos",
        command=lambda: cargar_datos_historicos(semanas_var.get(), graficas_frame),
        fg_color="#3498db",
        hover_color="#2980b9",
        font=("Montserrat", 12, "bold")
    )
    btn_cargar.pack(side="left", padx=5)
    
    # Frame para gráficas
    graficas_frame = ctk.CTkFrame(frame_historico)
    graficas_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

def cargar_datos_historicos(semanas, frame_destino):
    """Carga los datos históricos y los muestra en el frame especificado"""
    fecha_fin = datetime.now() - timedelta(weeks=semanas-1)
    fecha_inicio = fecha_fin - timedelta(weeks=1)
    
    try:
        db = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="",
            database="sistema_hidroponico"
        )
        
        query = f"""
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
            AND l.fecha_hora BETWEEN '{fecha_inicio.strftime('%Y-%m-%d')}' AND '{fecha_fin.strftime('%Y-%m-%d 23:59:59')}'
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
            # Limpiar frame de gráficas
            for widget in frame_destino.winfo_children():
                widget.destroy()
            ctk.CTkLabel(frame_destino, text="No hay datos para el período seleccionado").pack()
            return
        
        df['tipo_sensor'] = df['tipo_sensor'].str.lower().str.strip()
        df['fecha_hora'] = pd.to_datetime(df['fecha_hora'])
        df['valor'] = pd.to_numeric(df['valor'], errors='coerce')
        
        # Limpiar frame de gráficas
        for widget in frame_destino.winfo_children():
            widget.destroy()
        
        # Crear figura
        fig = plt.figure(figsize=(8, 10))
        for i, (sensor_db, config) in enumerate(sensores_config.items()):
            df_sensor = df[df['tipo_sensor'] == sensor_db]
            
            if not df_sensor.empty:
                ax = fig.add_subplot(4, 1, i+1)
                x = df_sensor['fecha_hora']
                y = df_sensor['valor']
                
                ax.plot(x, y, color=config['color'])
                ax.set_title(f"{config['nombre']} - Semana del {fecha_inicio.strftime('%d/%m')} al {fecha_fin.strftime('%d/%m')}")
                ax.grid(True)
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m %H:%M'))
        
        fig.tight_layout()
        
        # Mostrar gráfica en el frame
        canvas = FigureCanvasTkAgg(fig, master=frame_destino)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        
    except Exception as e:
        # Limpiar frame de gráficas
        for widget in frame_destino.winfo_children():
            widget.destroy()
        ctk.CTkLabel(frame_destino, text=f"Error al cargar datos: {str(e)}").pack()

def iniciar_graficas(frame):
    # Configuración del frame principal
    frame.configure(fg_color="#f5f7fa")
    frame.grid_rowconfigure(1, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    
    # --- ENCABEZADO ---
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
    
    # --- CONTENEDOR PRINCIPAL ---
    main_container = ctk.CTkFrame(frame, fg_color="transparent")
    main_container.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
    main_container.grid_rowconfigure(0, weight=1)
    main_container.grid_columnconfigure(0, weight=1)
    main_container.grid_columnconfigure(1, weight=1)
    
    # --- PANEL IZQUIERDO (LECTURAS Y BOTONES) ---
    left_panel = ctk.CTkFrame(main_container, fg_color="transparent", width=280)
    left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 15))
    left_panel.grid_rowconfigure(0, weight=1)
    
    # --- CONTENEDOR DE TARJETAS ---
    card_container = ctk.CTkFrame(left_panel, fg_color="transparent")
    card_container.pack(expand=True, fill="both", pady=15)
    
    # --- TARJETAS DE VALORES ACTUALES ---
    valores_frame = ctk.CTkFrame(card_container, fg_color="transparent")
    valores_frame.pack(expand=True, fill="both", anchor="center")

    etiquetas_lectura = {}
    iconos = {}
    
    for sensor_db, config in sensores_config.items():
        cuadro = ctk.CTkFrame(
            valores_frame, 
            fg_color="white",
            border_width=1,
            border_color="#e0e0e0",
            corner_radius=12
        )
        cuadro.pack(fill="x", pady=(0, 12), ipady=8, ipadx=8)
        
        content_frame = ctk.CTkFrame(cuadro, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=12, pady=12)
        
        top_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        top_frame.pack(fill="x")
        
        # Mostrar icono
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
            iconos[sensor_db] = config['icon']
        
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
            pady=4
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
    
    # --- BOTONES DE ACCIÓN ---
    botones_frame = ctk.CTkFrame(card_container, fg_color="transparent")
    botones_frame.pack(fill="x", pady=(10, 0))
    
    # Botón de histórico
    boton_historico = ctk.CTkButton(
        botones_frame,
        text="Ver Histórico",
        width=120,
        height=35,
        font=("Montserrat", 12, "bold"),
        fg_color="#2ecc71",
        hover_color="#27ae60",
        command=lambda: ver_historico_semanal(right_panel)
    )
    boton_historico.pack(side="left", padx=5, pady=5, fill='x', expand=True)
    
    # Botón de reporte
    boton_reporte = ctk.CTkButton(
        botones_frame,
        text="Generar Reporte",
        width=120,
        height=35,
        font=("Montserrat", 12, "bold"),
        fg_color="#e74c3c",
        hover_color="#c0392b",
        command=lambda: generar_reporte_semanal(right_panel)
    )
    boton_reporte.pack(side="left", padx=5, pady=5, fill='x', expand=True)
    
    # --- PANEL DERECHO (GRÁFICAS O CONTENIDO DINÁMICO) ---
    right_panel = ctk.CTkFrame(main_container, fg_color="transparent")
    right_panel.grid(row=0, column=1, sticky="nsew")
    right_panel.grid_rowconfigure(0, weight=1)
    right_panel.grid_columnconfigure(0, weight=1)
    
    # Mostrar gráficas por defecto
    mostrar_graficas(right_panel)
    
    # Función para actualizar valores en las tarjetas
    def actualizar_valores():
        df = obtener_datos()
        if df is not None and not df.empty:
            df['fecha_hora'] = pd.to_datetime(df['fecha_hora'])
            df = df.sort_values(by='fecha_hora')
            
            for sensor_db in sensores_config:
                df_sensor = df[df['tipo_sensor'] == sensor_db]
                if not df_sensor.empty:
                    last_val = df_sensor['valor'].iloc[-1]
                    etiquetas_lectura[sensor_db].configure(text=f"{last_val:.1f}")
        
        frame.after(10000, actualizar_valores)
    
    # Iniciar la actualización de valores
    actualizar_valores()