import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style


style.use('ggplot')


fig, ax = plt.subplots(figsize=(12, 7))

def obtener_datos():
    """Obtiene los datos desde MySQL y los devuelve como un DataFrame."""
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
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
    db.close()

    df = pd.DataFrame(datos)

    if df.empty:
        print("No hay datos para graficar.")
        return None

    df['fecha_hora'] = pd.to_datetime(df['fecha_hora'])
    return df

def actualizar_grafica(frame):
    """Actualiza la gráfica en tiempo real."""
    ax.clear()  

    df = obtener_datos()
    if df is None:
        return  

    colores = {'pH': 'blue', 'Conductividad eléctrica': 'green', 'Temperatura': 'red'}

    for sensor in colores.keys():
        sensor_data = df[df['tipo_sensor'] == sensor]

        if not sensor_data.empty:
            
            sensor_data = sensor_data.sort_values(by='fecha_hora')
            dif = sensor_data['valor'].diff()  

      
            colores_puntos = ['green' if d > 0 else 'red' for d in dif.fillna(0)]

           
            ax.plot(sensor_data['fecha_hora'], sensor_data['valor'], label=sensor, color=colores[sensor], linewidth=2)

           
            ax.scatter(sensor_data['fecha_hora'], sensor_data['valor'], c=colores_puntos, edgecolors='black', s=50, zorder=3)

    ax.set_title('Lecturas de Sensores en Sistema Hidropónico', fontsize=16, fontweight='bold')
    ax.set_xlabel('Fecha y Hora', fontsize=14)
    ax.set_ylabel('Valor de la Lectura', fontsize=14)
    ax.legend(title='Sensores', title_fontsize='13', fontsize='12', loc='upper left')
    ax.tick_params(axis='x', rotation=45, labelsize=12)
    ax.tick_params(axis='y', labelsize=12)
    ax.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()


ani = animation.FuncAnimation(fig, actualizar_grafica, interval=5000)


plt.show()
