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
    'pH': '#B0E0E6',
    'Temperatura': '#98FB98',
    'Conductividad': '#FFFACD',
    'border': '#4682B4',
    'header_bg': '#4F94CD',
    'row_selected': '#B0E0E6'
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

def crear_tabla_historial(frame, alertas, resolver_callback, descartar_callback, editar_callback):
    """Crea una tabla con el historial de alertas usando solo CTk widgets"""
    
    # Frame contenedor principal
    frame_principal = ctk.CTkFrame(frame, fg_color="transparent")
    frame_principal.pack(pady=(20, 10), padx=20, fill="both", expand=True)
    
    # Frame para los encabezados
    frame_encabezados = ctk.CTkFrame(frame_principal, fg_color=COLORES['header_bg'])
    frame_encabezados.pack(fill="x")
    
    # Crear encabezados
    encabezados = ['🔍 ID', '⚠️ Tipo', '📜 Descripción', '📅 Fecha', '🟢 Estado', '⚙️ Acciones']
    for i, texto in enumerate(encabezados):
        label = ctk.CTkLabel(
            frame_encabezados,
            text=texto,
            font=('Arial', 14, 'bold'),
            text_color="white"
        )
        label.grid(row=0, column=i, padx=5, pady=5, sticky="ew")
        frame_encabezados.grid_columnconfigure(i, weight=1)
    
    # Frame para el scrollable
    frame_scroll = ctk.CTkScrollableFrame(frame_principal, fg_color="transparent")
    frame_scroll.pack(fill="both", expand=True)
    
    # Configurar pesos de columnas
    for i in range(6):
        frame_scroll.grid_columnconfigure(i, weight=1)
    
    # Crear filas
    for i, alerta in enumerate(alertas):
        frame_fila = ctk.CTkFrame(frame_scroll, fg_color=COLORES['pH'] if i % 3 == 0 else COLORES['Temperatura'] if i % 3 == 1 else COLORES['Conductividad'])
        frame_fila.pack(fill="x", pady=2)
        
        # Configurar pesos de columnas para la fila
        for col in range(6):
            frame_fila.grid_columnconfigure(col, weight=1)
        
        # En la función crear_tabla_historial, modificar la línea que muestra el estado:
        datos = [
            str(alerta.get('id_alerta', '')),
            alerta.get('tipo_alerta', ''),
            alerta.get('descripcion', ''),
            alerta.get('fecha_hora', '').strftime('%Y-%m-%d %H:%M:%S') if isinstance(alerta.get('fecha_hora'), datetime) else str(alerta.get('fecha_hora', '')),
            alerta.get('estado', 'En revision').capitalize()  # Cambiado para usar el valor por defecto
        ]
        
        for col, valor in enumerate(datos):
            label = ctk.CTkLabel(
                frame_fila,
                text=valor,
                font=('Arial', 12),
                text_color="black"
            )
            label.grid(row=0, column=col, padx=5, pady=5, sticky="w")
        
        # Frame para botones
        frame_botones = ctk.CTkFrame(frame_fila, fg_color="transparent")
        frame_botones.grid(row=0, column=5, padx=5, pady=5, sticky="e")
        
        # Botones de acción
        btn_resolver = ctk.CTkButton(
            frame_botones,
            text="✔️ Resolver",
            width=80,
            height=30,
            command=lambda id=alerta['id_alerta']: resolver_callback(id),
            fg_color="#4CAF50",
            font=('Arial', 10)
        )
        btn_resolver.pack(side="left", padx=2)
        
        btn_descartar = ctk.CTkButton(
            frame_botones,
            text="❌ Descartar",
            width=80,
            height=30,
            command=lambda id=alerta['id_alerta']: descartar_callback(id),
            fg_color="gray",
            font=('Arial', 10)
        )
        btn_descartar.pack(side="left", padx=2)
        
        # Solo mostrar botón editar si hay id_sensor en los datos
        if 'id_sensor' in alerta:
            btn_editar = ctk.CTkButton(
                frame_botones,
                text="✏️ Editar",
                width=80,
                height=30,
                command=lambda id=alerta['id_sensor'], tipo=alerta['tipo_alerta']: editar_callback(tipo, id),
                fg_color="#1976D2",
                font=('Arial', 10)
            )
            btn_editar.pack(side="left", padx=2)
    
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
    
    # Contar alertas por tipo
    contador_alertas = {
        'pH': 0,
        'Temperatura': 0,
        'Conductividad': 0,
        'Valor fuera de rango': 0
    }
    
    for alerta in alertas:
        tipo = alerta.get('tipo_alerta', 'Valor fuera de rango')
        if tipo in contador_alertas:
            contador_alertas[tipo] += 1
        else:
            contador_alertas['Valor fuera de rango'] += 1
    
    # Frame para el título
    frame_titulo = ctk.CTkFrame(frame, fg_color="#E3F2FD")
    frame_titulo.pack(pady=(20, 10))
    label_titulo = ctk.CTkLabel(frame_titulo, text="🚨 Alertas 🚨", font=('Arial', 20, 'bold'), text_color=obtener_color_texto())
    label_titulo.pack()
    
    # Frame para las alertas actuales
    frame_alertas = ctk.CTkFrame(frame, fg_color="#E3F2FD")
    frame_alertas.pack(pady=10)
    
    # Recuadros de alertas (solo muestran conteo)
    recuadro_1 = ctk.CTkFrame(frame_alertas, width=250, height=120, corner_radius=10, fg_color=COLORES['pH'], border_width=2, border_color="black")
    recuadro_1.grid(row=0, column=0, padx=10, pady=10)

    recuadro_2 = ctk.CTkFrame(frame_alertas, width=250, height=120, corner_radius=10, fg_color=COLORES['Temperatura'], border_width=2, border_color="black")
    recuadro_2.grid(row=0, column=1, padx=10, pady=10)

    recuadro_3 = ctk.CTkFrame(frame_alertas, width=250, height=120, corner_radius=10, fg_color=COLORES['Conductividad'], border_width=2, border_color="black")
    recuadro_3.grid(row=0, column=2, padx=10, pady=10)
    
    # Labels para las alertas (solo conteo)
    label_1 = ctk.CTkLabel(recuadro_1, text=f"⚠️ Alertas de pH\n{contador_alertas['pH']} alertas", font=('Arial', 16, 'bold'), text_color=obtener_color_texto())
    label_1.pack(padx=10, pady=10)

    label_2 = ctk.CTkLabel(recuadro_2, text=f"🌡️ Alertas de Temp.\n{contador_alertas['Temperatura']} alertas", font=('Arial', 16, 'bold'), text_color=obtener_color_texto())
    label_2.pack(padx=10, pady=10)

    label_3 = ctk.CTkLabel(recuadro_3, text=f"⚡ Alertas de Condu.\n{contador_alertas['Valor fuera de rango']} alertas", font=('Arial', 16, 'bold'), text_color=obtener_color_texto())
    label_3.pack(padx=10, pady=10)

    # Modal para mensajes
    frame_modal = ctk.CTkFrame(frame, width=300, height=150, corner_radius=10, fg_color='gray')
    label_modal = ctk.CTkLabel(frame_modal, text="Resolviendo...", font=('Arial', 14))
    label_modal.pack(padx=10, pady=40)
    
    def resolver_alerta(id_alerta):
        tipo = next((a['tipo_alerta'] for a in alertas if a['id_alerta'] == id_alerta), "Alerta")
        actualizar_alerta(id_alerta, 'Resuelta')  # Capitalizado para consistencia
        mostrar_modal(frame_modal, label_modal, tipo, "resuelta")
        actualizar_vista(frame)
            
    def descartar_alerta(id_alerta):
        tipo = next((a['tipo_alerta'] for a in alertas if a['id_alerta'] == id_alerta), "Alerta")
        actualizar_alerta(id_alerta, 'Descartada')  # Capitalizado para consistencia
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