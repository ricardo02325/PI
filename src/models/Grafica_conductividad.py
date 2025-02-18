import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

style.use('ggplot')

fig, ax = plt.subplots(figsize=(12, 5))

def obtener_datos():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="sistema_hidroponico"
    )

    query = """
        SELECT l.valor, l.fecha_hora
        FROM lecturas_sensores l
        JOIN sensores s ON l.id_sensor = s.id_sensor
        WHERE s.tipo_sensor = 'Conductividad eléctrica'
        ORDER BY l.fecha_hora
    """
    
    cursor = db.cursor(dictionary=True)
    cursor.execute(query)
    datos = cursor.fetchall()
    db.close()
    
    df = pd.DataFrame(datos)
    if df.empty:
        print("⚠️ No hay datos para graficar.")
        return None

    df['fecha_hora'] = pd.to_datetime(df['fecha_hora'])
    return df

def actualizar_grafica(frame):
    ax.clear()
    df = obtener_datos()
    if df is None:
        return
    
    df = df.sort_values(by='fecha_hora')
    ax.plot(df['fecha_hora'], df['valor'], label="Conductividad Eléctrica", color='green', linewidth=2)
    
    ax.set_title('📊 Conductividad Eléctrica', fontsize=16, fontweight='bold')
    ax.set_xlabel('Fecha y Hora', fontsize=14)
    ax.set_ylabel('Valor (mS/cm)', fontsize=14)
    ax.legend(fontsize=12, loc='upper left')
    ax.tick_params(axis='x', rotation=45, labelsize=12)
    ax.tick_params(axis='y', labelsize=12)
    ax.grid(True, linestyle='--', alpha=0.7)
    fig.tight_layout()

ani = animation.FuncAnimation(fig, actualizar_grafica, interval=5000)
plt.show()
