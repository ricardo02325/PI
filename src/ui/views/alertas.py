import sys
import os
import customtkinter as ctk
from tkinter import ttk
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from src.models.models import (
    obtener_alertas,
    actualizar_trigger,
    actualizar_alerta,
    obtener_alertas_completas
)

COLORES = {
    'pH': '#B0E0E6',            # Sensor ID 1
    'Profundidad': '#FFA07A',   # Sensor ID 2 
    'Temperatura': '#98FB98',   # Sensor ID 3
    'Conductividad': '#FFFACD',  # Sensor ID 4
    'border': '#4682B4',
    'header_bg': '#4F94CD',
    'row_selected': '#B0E0E6'
}

# Mapeo de IDs de sensor a nombres
SENSOR_NAMES = {
    1: 'pH',
    2: 'Profundidad',
    3: 'Temperatura',
    4: 'Conductividad'
}

def mostrar_modal(frame_modal, label_modal, tipo_alerta, estado_alerta):
    frame_modal.place(relx=0.5, rely=0.5, anchor="center")
    label_modal.configure(text=f"Resolviendo alerta de {tipo_alerta}...")
    frame_modal.update()
    frame_modal.after(2000, lambda: actualizar_modal(frame_modal, label_modal, tipo_alerta, estado_alerta))

def actualizar_modal(frame_modal, label_modal, tipo_alerta, estado_alerta):
    label_modal.configure(text=f"¡Alerta de {tipo_alerta} {estado_alerta}! ✅")
    frame_modal.after(1500, frame_modal.place_forget)

def obtener_color_texto():
    return "white" if ctk.get_appearance_mode() == "dark" else "black"

def crear_tabla_historial(frame, alertas, resolver_callback, descartar_callback, editar_callback, filtro_estado=None):
    """Crea una tabla con el historial de alertas usando solo CTk widgets"""
    
    # Frame contenedor principal
    frame_principal = ctk.CTkFrame(frame, fg_color="transparent")
    frame_principal.pack(pady=(10, 20), padx=20, fill="both", expand=True)
    
    # Frame para los filtros
    frame_filtros = ctk.CTkFrame(frame_principal, fg_color="transparent")
    frame_filtros.pack(fill="x", pady=(0, 10))
    
    # Frame interno para centrar los botones
    frame_centro_filtros = ctk.CTkFrame(frame_filtros, fg_color="transparent")
    frame_centro_filtros.pack(expand=True)  # Esto centrará el frame
    
    # Botones de filtrado
    btn_todos = ctk.CTkButton(
        frame_centro_filtros, 
        text="Todas",
        command=lambda: actualizar_filtro(None),
        width=100,
        fg_color="#4F94CD"
    )
    btn_todos.pack(side="left", padx=5)
    
    btn_resueltas = ctk.CTkButton(
        frame_centro_filtros, 
        text="Resueltas",
        command=lambda: actualizar_filtro("Resuelta"),
        width=100,
        fg_color="#4CAF50"
    )
    btn_resueltas.pack(side="left", padx=5)
    
    btn_descartadas = ctk.CTkButton(
        frame_centro_filtros, 
        text="Descartadas",
        command=lambda: actualizar_filtro("Descartada"),
        width=100,
        fg_color="#F44336"
    )
    btn_descartadas.pack(side="left", padx=5)
    
    btn_revision = ctk.CTkButton(
        frame_centro_filtros, 
        text="En revisión",
        command=lambda: actualizar_filtro("En revision"),
        width=100,
        fg_color="#FFC107",
        text_color="black"
    )
    btn_revision.pack(side="left", padx=5)
    
    def actualizar_filtro(estado):
        nonlocal filtro_estado
        filtro_estado = estado
        # Limpiar y recrear la tabla con el nuevo filtro
        for widget in frame_principal.winfo_children():
            if widget != frame_filtros:  # Mantener los filtros
                widget.destroy()
        crear_tabla_contenido()
    
    def crear_tabla_contenido():
        # Frame para los encabezados
        frame_encabezados = ctk.CTkFrame(frame_principal, fg_color=COLORES['header_bg'])
        frame_encabezados.pack(fill="x", pady=(0, 5))
        
        # Crear encabezados centrados
        encabezados = ['🔍 ID', '⚠️ Tipo', '📜 Descripción', '📅 Fecha', '🟢 Estado', '⚙️ Acciones']
        for i, texto in enumerate(encabezados):
            label = ctk.CTkLabel(
                frame_encabezados,
                text=texto,
                font=('Arial', 14, 'bold'),
                text_color="white"
            )
            label.grid(row=0, column=i, padx=5, pady=5, sticky="nsew")
            frame_encabezados.grid_columnconfigure(i, weight=1)
        
        # Frame para el scrollable
        frame_scroll = ctk.CTkScrollableFrame(frame_principal, fg_color="transparent")
        frame_scroll.pack(fill="both", expand=True)
        
        # Configurar pesos de columnas
        for i in range(6):
            frame_scroll.grid_columnconfigure(i, weight=1)
        
        # Filtrar alertas si hay un filtro aplicado
        alertas_filtradas = alertas if filtro_estado is None else [
            a for a in alertas if a.get('estado', '').lower() == filtro_estado.lower()
        ]
        
        # Crear filas
        for i, alerta in enumerate(alertas_filtradas):
            # Determinar el color basado en el tipo de sensor
            sensor_id = None
            descripcion = alerta.get('descripcion', '')
            
            # Extraer ID del sensor de la descripción si es una alerta de rango
            if 'Valor del sensor' in descripcion:
                try:
                    sensor_id = int(descripcion.split('Valor del sensor ')[1].split(' ')[0])
                except (IndexError, ValueError):
                    pass
            
            # Asignar color basado en el sensor o tipo de alerta
            if sensor_id in SENSOR_NAMES:
                color = COLORES[SENSOR_NAMES[sensor_id]]
            else:
                # Asignar colores alternativos para otros tipos de alerta
                color = COLORES['pH'] if i % 4 == 0 else \
                        COLORES['Profundidad'] if i % 4 == 1 else \
                        COLORES['Temperatura'] if i % 4 == 2 else \
                        COLORES['Conductividad']
            
            frame_fila = ctk.CTkFrame(frame_scroll, fg_color=color)
            frame_fila.pack(fill="x", pady=2)
            
            # Configurar pesos de columnas para la fila
            for col in range(6):
                frame_fila.grid_columnconfigure(col, weight=1)
            
            # Mostrar datos de la alerta (centrados)
            datos = [
                str(alerta.get('id_alerta', '')),
                alerta.get('tipo_alerta', ''),
                descripcion,
                alerta.get('fecha_hora', '').strftime('%Y-%m-%d %H:%M:%S') if isinstance(alerta.get('fecha_hora'), datetime) else str(alerta.get('fecha_hora', '')),
                alerta.get('estado', 'Por atender').capitalize()
            ]
            
            for col, valor in enumerate(datos):
                label = ctk.CTkLabel(
                    frame_fila,
                    text=valor,
                    font=('Arial', 12),
                    text_color="black"
                )
                # Texto centrado en cada celda
                label.grid(row=0, column=col, padx=5, pady=5, sticky="nsew")
            
            # Frame para botones
            frame_botones = ctk.CTkFrame(frame_fila, fg_color="transparent")
            frame_botones.grid(row=0, column=5, padx=5, pady=5, sticky="nsew")
            
            # Determinar si los botones deben estar habilitados
            estado = alerta.get('estado', '').lower()
            botones_habilitados = estado in ('por atender', 'en revision')
            
            # Botones de acción
            btn_resolver = ctk.CTkButton(
                frame_botones,
                text="✔️ Resolver",
                width=80,
                height=30,
                command=lambda id=alerta['id_alerta']: resolver_callback(id),
                fg_color="#4CAF50",
                font=('Arial', 10),
                state="normal" if botones_habilitados else "disabled"
            )
            btn_resolver.pack(side="left", padx=2)
            
            btn_descartar = ctk.CTkButton(
                frame_botones,
                text="❌ Descartar",
                width=80,
                height=30,
                command=lambda id=alerta['id_alerta']: descartar_callback(id),
                fg_color="gray",
                font=('Arial', 10),
                state="normal" if botones_habilitados else "disabled"
            )
            btn_descartar.pack(side="left", padx=2)
            
            # Mostrar botón editar solo para alertas de rango con sensor identificado
            if sensor_id is not None:
                btn_editar = ctk.CTkButton(
                    frame_botones,
                    text="✏️ Editar",
                    width=80,
                    height=30,
                    command=lambda id=sensor_id, tipo=SENSOR_NAMES.get(sensor_id, 'Sensor'): editar_callback(tipo, id),
                    fg_color="#1976D2",
                    font=('Arial', 10),
                    state="normal" if botones_habilitados else "disabled"
                )
                btn_editar.pack(side="left", padx=2)
    
    # Crear el contenido inicial de la tabla
    crear_tabla_contenido()
    
    return frame_principal

def editar_alerta(frame, tipo_alerta, id_sensor=None):
    """Muestra un formulario modal para editar los triggers de una alerta."""
    formulario_modal = ctk.CTkFrame(frame, width=400, height=300, corner_radius=10, fg_color="lightgray")
    formulario_modal.place(relx=0.5, rely=0.5, anchor="center")

    label_titulo_formulario = ctk.CTkLabel(formulario_modal, text=f"Editar alerta de {tipo_alerta}", font=('Arial', 14, 'bold'))
    label_titulo_formulario.pack(pady=10)

    label_valor_max = ctk.CTkLabel(formulario_modal, text="Valor máximo:", font=('Arial', 12))
    label_valor_max.pack(pady=5)

    entry_valor_max = ctk.CTkEntry(formulario_modal, font=('Arial', 12))
    entry_valor_max.pack(pady=5)

    label_valor_min = ctk.CTkLabel(formulario_modal, text="Valor mínimo:", font=('Arial', 12))
    label_valor_min.pack(pady=5)

    entry_valor_min = ctk.CTkEntry(formulario_modal, font=('Arial', 12))
    entry_valor_min.pack(pady=5)
    
    def enviar_edicion():
        try:
            valor_min = float(entry_valor_min.get())
            valor_max = float(entry_valor_max.get())

            if valor_min is not None and valor_max is not None:
                if id_sensor:
                    actualizar_trigger(id_sensor, valor_min, valor_max)
                print(f"Trigger de {tipo_alerta} actualizado con valor mínimo: {valor_min}, valor máximo: {valor_max}")
                formulario_modal.place_forget()
            else:
                print("Por favor ingrese valores válidos.")
        except ValueError:
            print("Error: Ingrese valores numéricos válidos.")

    boton_enviar = ctk.CTkButton(formulario_modal, text="✔️ Enviar", command=enviar_edicion, width=230, corner_radius=5, fg_color="green")
    boton_enviar.pack(pady=10)
    
    boton_cerrar = ctk.CTkButton(formulario_modal, text="❌ Cerrar", command=formulario_modal.place_forget, width=230, corner_radius=5, fg_color="red")
    boton_cerrar.pack(pady=5)

def iniciar_alertas(frame):
    alertas = obtener_alertas_completas()
    
    # Contar alertas por sensor
    contador_alertas = {
        'pH': 0,
        'Profundidad': 0,
        'Temperatura': 0,
        'Conductividad': 0,
        'Otras': 0
    }
    
    for alerta in alertas:
        # Obtener el id_sensor directamente de la alerta (si está disponible)
        id_sensor = alerta.get('id_sensor')
        
        if id_sensor in SENSOR_NAMES:
            contador_alertas[SENSOR_NAMES[id_sensor]] += 1
        else:
            # Si no hay id_sensor, intentar determinar el tipo por el tipo_alerta
            tipo = alerta.get('tipo_alerta', '')
            if tipo in contador_alertas:
                contador_alertas[tipo] += 1
            else:
                contador_alertas['Otras'] += 1
    
    frame_titulo = ctk.CTkFrame(frame, fg_color="#E3F2FD")
    frame_titulo.pack(pady=(20, 10))
    label_titulo = ctk.CTkLabel(frame_titulo, text="🚨 Alertas 🚨", font=('Arial', 20, 'bold'), text_color=obtener_color_texto())
    label_titulo.pack()
    
    # Frame para las alertas actuales (ahora con 4 recuadros)
    frame_alertas = ctk.CTkFrame(frame, fg_color="#E3F2FD")
    frame_alertas.pack(pady=10)
    
    # Recuadros de alertas para cada sensor
    recuadros = [
        ('pH', COLORES['pH'], f"⚠️ Alertas de pH\n{contador_alertas['pH']} alertas"),
        ('Profundidad', COLORES['Profundidad'], f"📏 Alertas de Profundidad\n{contador_alertas['Profundidad']} alertas"),
        ('Temperatura', COLORES['Temperatura'], f"🌡️ Alertas de Temp.\n{contador_alertas['Temperatura']} alertas"),
        ('Conductividad', COLORES['Conductividad'], f"⚡ Alertas de Condu.\n{contador_alertas['Conductividad']} alertas")
    ]
    
    for i, (nombre, color, texto) in enumerate(recuadros):
        recuadro = ctk.CTkFrame(
            frame_alertas, 
            width=200, 
            height=100, 
            corner_radius=10, 
            fg_color=color, 
            border_width=2, 
            border_color="black"
        )
        recuadro.grid(row=0, column=i, padx=5, pady=5)
        
        label = ctk.CTkLabel(
            recuadro, 
            text=texto, 
            font=('Arial', 14, 'bold'), 
            text_color=obtener_color_texto()
        )
        label.pack(padx=10, pady=10)

    # Modal para mensajes
    frame_modal = ctk.CTkFrame(frame, width=300, height=150, corner_radius=10, fg_color='gray')
    label_modal = ctk.CTkLabel(frame_modal, text="Resolviendo...", font=('Arial', 14))
    label_modal.pack(padx=10, pady=40)
    
    def resolver_alerta(id_alerta):
        tipo = next((a['tipo_alerta'] for a in alertas if a['id_alerta'] == id_alerta), "Alerta")
        actualizar_alerta(id_alerta, 'Resuelta')
        mostrar_modal(frame_modal, label_modal, tipo, "resuelta")
        actualizar_vista(frame)
            
    def descartar_alerta(id_alerta):
        tipo = next((a['tipo_alerta'] for a in alertas if a['id_alerta'] == id_alerta), "Alerta")
        actualizar_alerta(id_alerta, 'Descartada')
        mostrar_modal(frame_modal, label_modal, tipo, "descartada")
        actualizar_vista(frame)
        
    def editar_alerta_callback(tipo_alerta, id_sensor=None):
        editar_alerta(frame, tipo_alerta, id_sensor)
        
    def actualizar_vista(frame):
        # Limpiar el frame y volver a cargar todo
        for widget in frame.winfo_children():
            widget.destroy()
        iniciar_alertas(frame)
    
    # Crear tabla de historial con los botones de acción
    frame_tabla_historial = crear_tabla_historial(
        frame, 
        alertas, 
        resolver_alerta, 
        descartar_alerta, 
        editar_alerta_callback
    )