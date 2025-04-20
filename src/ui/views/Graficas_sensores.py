import sys
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates
from matplotlib.ticker import MaxNLocator

# Añadir el path al proyecto si es necesario
sys.path.append('C:\\Users\\Colibecas\\Desktop\\PI')

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
            DATE_FORMAT(l.fecha_hora, '%d-%m-%Y') AS fecha
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
        
        # Normalizar nombres de sensores para evitar errores
        df['tipo_sensor'] = df['tipo_sensor'].str.lower().str.strip()
        df['fecha_hora'] = pd.to_datetime(df['fecha_hora'])
        df['valor'] = pd.to_numeric(df['valor'], errors='coerce')  

        print("✅ Datos obtenidos de MySQL:")
        print(df.head())  

        return df
    except mysql.connector.Error as err:
        print(f"❌ Error de conexión: {err}")
        return None

def iniciar_graficas(frame):
    """Crea y actualiza las gráficas en la interfaz."""
    # Configuración de estilo general
    ctk.set_appearance_mode("light")  
    ctk.set_default_color_theme("dark-blue")  
    
    # Configuración de estilo para matplotlib
    plt.style.use('seaborn-v0_8')
    
    # Configurar fondo del frame principal
    frame.configure(fg_color="#f8f9fa")  
    
    # Encabezado moderno
    encabezado_frame = ctk.CTkFrame(frame, fg_color="transparent")
    encabezado_frame.pack(side="top", fill="x", pady=(20, 10))
    
    bienvenido_label = ctk.CTkLabel(
        encabezado_frame, 
        text="Panel de Monitoreo Hidropónico",  
        font=("Arial", 24, "bold"),  
        text_color="#2c3e50"
    )
    bienvenido_label.pack(side="top", padx=10, pady=0)
    
    # Frame de lecturas actuales (tarjetas modernas)
    lecturas_frame = ctk.CTkFrame(frame, fg_color="transparent")
    lecturas_frame.pack(side="top", fill="x", pady=(0, 15), padx=20)
    
    # Configuración de colores para cada sensor
    sensores_config = {
        'ph': {'nombre': 'pH', 'color': '#3498db', 'unidad': '', 'rango': (0, 14)},
        'conductividad_elec': {'nombre': 'Conductividad', 'color': '#2ecc71', 'unidad': 'µS/cm', 'rango': (0, 2000)},
        'temperatura': {'nombre': 'Temperatura', 'color': '#e74c3c', 'unidad': '°C', 'rango': (10, 40)}
    }
    
    etiquetas_lectura = {}
    
    for sensor_db, config in sensores_config.items():
        # Tarjeta para cada sensor
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
        
        # Título de la tarjeta
        titulo = ctk.CTkLabel(
            cuadro, 
            text=config['nombre'],  
            font=("Arial", 14, "bold"), 
            text_color=config['color'],
            justify="center"
        )
        titulo.pack(pady=(10, 0))
        
        # Valor actual
        valor = ctk.CTkLabel(
            cuadro, 
            text="--",  
            font=("Arial", 24, "bold"), 
            text_color="#2c3e50",
            justify="center"
        )
        valor.pack(expand=True)
        
        # Unidad de medida
        unidad = ctk.CTkLabel(
            cuadro, 
            text=config['unidad'],  
            font=("Arial", 12), 
            text_color="#7f8c8d",
            justify="center"
        )
        unidad.pack(pady=(0, 10))
        
        etiquetas_lectura[sensor_db] = valor

    # Configuración de la figura con dimensiones ajustadas
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
        
        # Asegurar que los datos están ordenados cronológicamente
        df = df.sort_values(by='fecha_hora')

        for i, (sensor_db, ax) in enumerate(zip(sensores_config.keys(), axes)):
            df_tipo = df[df['tipo_sensor'] == sensor_db]
            config = sensores_config[sensor_db]
            
            ax.clear()
            
            if not df_tipo.empty:
                # Gráfico de línea con estilo moderno
                ax.plot(df_tipo['fecha_hora'], df_tipo['valor'], 
                       color=config['color'], 
                       linewidth=2.5, 
                       marker='o', 
                       markersize=6,
                       markerfacecolor='white',
                       markeredgecolor=config['color'],
                       markeredgewidth=2)
                
                # Relleno bajo la curva
                ax.fill_between(df_tipo['fecha_hora'], df_tipo['valor'], 
                               alpha=0.1, color=config['color'])
                
                # Configuración del eje Y
                ax.set_ylim(config['rango'])
                ax.yaxis.set_major_locator(MaxNLocator(5))
                
                # Configuración del eje X (fechas completas)
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y %H:%M'))  # Formato día/mes/año hora:minuto
                
                # Rotación de etiquetas para mejor legibilidad
                plt.setp(ax.get_xticklabels(), rotation=30, ha='right', fontsize=8)
                
                # Título y etiquetas
                ax.set_title(config['nombre'], fontsize=13, pad=10, 
                             fontweight='bold', color=config['color'])
                ax.set_xlabel('Fecha y Hora', fontsize=9, labelpad=8, color='#7f8c8d')
                ax.set_ylabel(config['unidad'], fontsize=9, labelpad=8, color='#7f8c8d')
                
                # Estilo del grid
                ax.grid(True, linestyle=':', alpha=0.5, color='#e0e0e0')
                
                # Color de fondo y bordes
                ax.set_facecolor('#ffffff')
                for spine in ax.spines.values():
                    spine.set_edgecolor('#e0e0e0')
                    spine.set_linewidth(0.8)
                
                # Actualizar valor en la tarjeta
                valor_actual = df_tipo['valor'].iloc[-1]
                etiquetas_lectura[sensor_db].configure(text=f"{valor_actual:.1f}")
            else:
                ax.text(0.5, 0.5, f"No hay datos de {config['nombre']}", 
                       fontsize=12, ha='center', va='center', 
                       color='#7f8c8d', transform=ax.transAxes)
                ax.set_frame_on(False)
                etiquetas_lectura[sensor_db].configure(text="--")
        
        # Ajustar diseño para mejor visualización
        fig.tight_layout(pad=2.0)
        canvas.draw_idle()
        
        # Programar próxima actualización
        frame.after(10000, actualizar_graficas)

    # Primera actualización
    actualizar_graficas()