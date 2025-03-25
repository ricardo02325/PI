import sys
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import style

# Variable global para la animación
ani = None

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
            WHERE LOWER(s.tipo_sensor) IN ('ph', 'conductividad eléctrica', 'temperatura')
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
    """Crea y actualiza las gráficas en la interfaz."""
    ctk.set_appearance_mode("light")  
    ctk.set_default_color_theme("blue")  
    style.use('ggplot')

    frame.configure(fg_color="#f0f0f0")  # Fondo del frame
    
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
    sensores = {'pH': 'pH', 'Conductividad eléctrica': 'Conductividad eléctrica', 'Temperatura': 'Temperatura'}

    for etiqueta_sensor, sensor_db in sensores.items():
        cuadro = ctk.CTkFrame(
            lecturas_frame, 
            fg_color="#E3F2FD",  # Azul claro
            corner_radius=8, 
            border_color="#0D47A1",  # Azul fuerte
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

    def actualizar_graficas(_):
        df = obtener_datos()
        if df is None or df.empty:
            for ax in axes:
                ax.clear()
                ax.set_facecolor('#f0f0f0')
                ax.text(0.5, 0.5, "No hay datos", fontsize=14, ha='center', va='center', transform=ax.transAxes)
            for etiqueta in etiquetas_lectura.values():
                etiqueta.configure(text=f"{etiqueta.cget('text').split('\n')[0]}\nSin datos")
            canvas.draw()
            return
        
        # Convertir valores a tipo numérico si es necesario
        df['valor'] = pd.to_numeric(df['valor'], errors='coerce')  # Asegura que los valores sean numéricos
        
        # Asegurar que los datos están ordenados cronológicamente
        df = df.sort_values(by='fecha_hora')
        
        colores = {'pH': '#0D47A1', 'Conductividad eléctrica': '#388E3C', 'Temperatura': '#D32F2F'}
        
        # Filtrar los datos por tipo de sensor y graficarlos en sus respectivos subgráficos
        for i, (tipo, ax) in enumerate(zip(colores.keys(), axes)):
            ax.clear()
            df_tipo = df[df['tipo_sensor'].str.lower() == tipo.lower()]
            if not df_tipo.empty:
                ax.plot(df_tipo['fecha_hora'], df_tipo['valor'], color=colores[tipo], linewidth=2, marker='o', markersize=6)
                ax.set_title(tipo, fontsize=12, fontweight='bold', color="#333333")
                ax.set_facecolor('#ffffff')
                ax.grid(True, linestyle='--', alpha=0.5, color="gray")
                
                # Actualizar valores
                valor_actual = df_tipo['valor'].iloc[-1]
                etiquetas_lectura[tipo].configure(text=f"{tipo}\n\n{valor_actual}")
            else:
                etiquetas_lectura[tipo].configure(text=f"{tipo}\n\nSin datos")
    
        canvas.draw()

    global ani
    if ani is None:
        ani = animation.FuncAnimation(fig, actualizar_graficas, interval=5000, cache_frame_data=False)

    # Botones
    boton_frame = ctk.CTkFrame(frame, fg_color="transparent")
    boton_frame.pack(side="top", fill="x", pady=10)

    botones_textos = ["Bomba 1", "Bomba 2", "Bomba 3", "Sensor PH", "Sensor Temp", "Sensor CE"]
    botones = []
    
    for i, texto in enumerate(botones_textos):
        btn = ctk.CTkButton(
            boton_frame,
            text=texto,  
            fg_color="#E3F2FD",  # Azul claro
            border_color="#0D47A1",
            border_width=2,
            text_color="#333333",
            hover_color="#BBDEFB",  # Azul más claro al pasar el mouse
            command=lambda b=i: cambiar_color(b, botones)
        )
        btn.pack(side="left", padx=10, pady=5, expand=True)
        botones.append(btn)

    def cambiar_color(indice, botones):
        if botones[indice].cget("border_color") == "#0D47A1":
            botones[indice].configure(border_color="#388E3C")  # Verde
        else:
            botones[indice].configure(border_color="#0D47A1")  # Azul