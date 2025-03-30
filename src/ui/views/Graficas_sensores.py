import sys
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import style

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
            SELECT s.tipo_sensor, l.valor, l.fecha_hora
            FROM lecturas_sensores l
            JOIN sensores s ON l.id_sensor = s.id_sensor
            WHERE LOWER(s.tipo_sensor) IN ('ph', 'conductividad_elec', 'temperatura')
            ORDER BY l.fecha_hora
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
    ctk.set_appearance_mode("light")  
    ctk.set_default_color_theme("blue")  
    style.use('ggplot')

    frame.configure(fg_color="#f0f0f0")  
    
    # Encabezado
    encabezado_frame = ctk.CTkFrame(frame, fg_color="transparent")
    encabezado_frame.pack(side="top", fill="x", pady=20)
    
    bienvenido_label = ctk.CTkLabel(
        encabezado_frame, 
        text="BIENVENIDO 🏡",  
        font=("Arial", 30, "bold"),  
        text_color="#333333"
    )
    bienvenido_label.pack(side="top", padx=10, pady=0)

    # Figura de las gráficas
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    fig.patch.set_facecolor('#f0f0f0')  
    fig.tight_layout(pad=4.0)
    
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.get_tk_widget().pack(side="bottom", fill="both", expand=True)

    # Frame de lecturas
    lecturas_frame = ctk.CTkFrame(frame, fg_color="transparent")
    lecturas_frame.pack(side="top", fill="x", pady=10)

    etiquetas_lectura = {}
    sensores = {'ph': 'pH', 'conductividad_elec': 'Conductividad eléctrica', 'temperatura': 'Temperatura'}

    for sensor_db, etiqueta_sensor in sensores.items():
        cuadro = ctk.CTkFrame(
            lecturas_frame, 
            fg_color="#E3F2FD",
            corner_radius=8, 
            border_color="#0D47A1",
            border_width=2, 
            width=200, 
            height=100
        )
        cuadro.pack_propagate(False)  
        cuadro.pack(side="left", padx=10, pady=5, expand=True)

        etiqueta = ctk.CTkLabel(
            cuadro, 
            text=f"{etiqueta_sensor}\n-",  
            font=("Arial", 14, "bold"), 
            text_color="#333333",  
            justify="center"
        )
        etiqueta.pack(expand=True)
        etiquetas_lectura[sensor_db] = etiqueta

    def actualizar_graficas():
        df = obtener_datos()
        if df is None or df.empty:
            for ax in axes:
                ax.clear()
                ax.set_facecolor('#f0f0f0')
                ax.text(0.5, 0.5, "No hay datos", fontsize=14, ha='center', va='center', transform=ax.transAxes)
            for etiqueta in etiquetas_lectura.values():
                etiqueta.configure(text=f"{etiqueta.cget('text').split('\n')[0]}\nSin datos")
            canvas.draw_idle()
            return
        
        # Asegurar que los datos están ordenados cronológicamente
        df = df.sort_values(by='fecha_hora')

        colores = {'ph': '#0D47A1', 'conductividad_elec': '#388E3C', 'temperatura': '#D32F2F'}

        # Verificación de datos filtrados
        print("\n📊 Datos filtrados por tipo de sensor:")
        for i, (tipo, ax) in enumerate(zip(colores.keys(), axes)):
            df_tipo = df[df['tipo_sensor'] == tipo]
            print(f"\n{tipo}: {len(df_tipo)} registros")

            ax.clear()
            if not df_tipo.empty:
                ax.plot(df_tipo['fecha_hora'], df_tipo['valor'], color=colores[tipo], linewidth=2, marker='o', markersize=6)
                ax.set_title(tipo.capitalize(), fontsize=12, fontweight='bold', color="#333333")
                ax.set_facecolor('#ffffff')
                ax.grid(True, linestyle='--', alpha=0.5, color="gray")
                
                # Actualizar valores en la UI
                valor_actual = df_tipo['valor'].iloc[-1]
                etiquetas_lectura[tipo].configure(text=f"{sensores[tipo]}\n\n{valor_actual:.2f}")
            else:
                etiquetas_lectura[tipo].configure(text=f"{sensores[tipo]}\n\nSin datos")
    
        canvas.draw_idle()  # Actualizar UI inmediatamente

        # Actualizar cada 10 segundos
        frame.after(10000, actualizar_graficas)

    # Botón para actualizar manualmente
    boton_actualizar = ctk.CTkButton(
        frame,
        text="Actualizar Gráficas",
        fg_color="#E3F2FD",
        border_color="#0D47A1",
        border_width=2,
        text_color="#333333",
        hover_color="#BBDEFB",
        command=actualizar_graficas
    )
    boton_actualizar.pack(side="top", pady=10)

    actualizar_graficas()  # Primera actualización al cargar la UI 