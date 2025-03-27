import sys
import os
import customtkinter as ctk
from tkinter import ttk

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from src.models.models import (
    obtener_alertas,
    actualizar_trigger,
    actualizar_alerta,
    obtener_alertas_completas
)

COLORES = {
    'pH': '#A8E6CF',  
    'Temperatura': '#FFABAB',  
    'Conductividad': '#FFD3B6',
    'boton_pH': '#81C784',  
    'boton_temperatura': '#FF8A80',  
    'boton_conductividad': '#FFB74D',
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
    if ctk.get_appearance_mode() == "dark":
        return "white"
    else:
        return "black"

def crear_tabla_historial(frame, alertas):
    """Crea una tabla con el historial de alertas dentro del frame dado."""
    
    # Frame contenedor
    frame_tabla = ctk.CTkFrame(frame)
    frame_tabla.pack(pady=(30, 20), padx=20, fill="both", expand=True)

    # Título
    label_titulo_tabla = ctk.CTkLabel(
        frame_tabla, 
        text="📜 Historial Completo de Alertas", 
        font=('Arial', 16, 'bold'), 
        text_color=obtener_color_texto()
    )
    label_titulo_tabla.pack(pady=(0, 10))

    # Estilo de la tabla
    estilo = ttk.Style()
    estilo.theme_use('default')

    # Configurar colores según el modo (claro/oscuro)
    modo = ctk.get_appearance_mode()
    colores = {
        "dark": {"bg": "#2b2b2b", "fg": "white", "heading_bg": "#3b3b3b"},
        "light": {"bg": "white", "fg": "black", "heading_bg": "#f0f0f0"}
    }
    colores_actuales = colores["dark"] if modo == "dark" else colores["light"]

    estilo.configure(
        "Treeview",
        background=colores_actuales["bg"],
        foreground=colores_actuales["fg"],
        rowheight=25,
        fieldbackground=colores_actuales["bg"],
        bordercolor=colores_actuales["heading_bg"],
        borderwidth=0,
        font=('Arial', 10)
    )
    
    estilo.configure(
        "Treeview.Heading",
        background=colores_actuales["heading_bg"],
        foreground=colores_actuales["fg"],
        relief="flat",
        font=('Arial', 10, 'bold')
    )

    estilo.map(
        "Treeview",
        background=[('selected', '#0078d7' if modo == "dark" else '#1f6aa5')],
        foreground=[('selected', 'white')]
    )

    # Crear la tabla con columnas basadas en la consulta SQL
    tabla = ttk.Treeview(
        frame_tabla,
        columns=('id_alerta', 'tipo_alerta', 'descripcion', 'fecha_hora', 'estado'),
        show='headings',
        style="Treeview"
    )

    # Configurar columnas
    tabla.column('id_alerta', width=50, anchor='center')
    tabla.column('tipo_alerta', width=120, anchor='center')
    tabla.column('descripcion', width=250, anchor='w')
    tabla.column('fecha_hora', width=150, anchor='center')
    tabla.column('estado', width=100, anchor='center')

    # Encabezados
    tabla.heading('id_alerta', text='ID')
    tabla.heading('tipo_alerta', text='Tipo de Alerta')
    tabla.heading('descripcion', text='Descripción')
    tabla.heading('fecha_hora', text='Fecha')
    tabla.heading('estado', text='Estado')

    # Scrollbar
    scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=tabla.yview)
    scrollbar.pack(side="right", fill="y")
    tabla.configure(yscrollcommand=scrollbar.set)

    # Insertar datos
    for alerta in alertas:
        estado = alerta.get('estado', 'activa').lower()  # Convertimos a minúsculas para evitar errores
        
        # Definir color según el estado
        colores_estado = {
            "resuelta": "green",
            "activa": "red",
            "descartada": "gray"
        }

        # Insertar alerta en la tabla
        tabla.insert(
            '', 
            'end', 
            values=(
                alerta.get('id_alerta', ''),
                alerta.get('tipo_alerta', ''),
                alerta.get('descripcion', ''),
                alerta.get('fecha_hora', ''),
                estado
            ),
            tags=(estado,)
        )

    # Configurar colores para los estados
    for estado, color in colores_estado.items():
        tabla.tag_configure(estado, foreground=color)

    tabla.pack(fill="both", expand=True, padx=10, pady=10)

    return frame_tabla

def iniciar_alertas(frame):
    alertas = obtener_alertas_completas()
    
    # Frame para el título
    frame_titulo = ctk.CTkFrame(frame)
    frame_titulo.pack(pady=(20, 10))
    label_titulo = ctk.CTkLabel(frame_titulo, text="🚨 Alertas 🚨", font=('Arial', 20, 'bold'), text_color=obtener_color_texto())
    label_titulo.pack()
    
    # Frame para las alertas actuales
    frame_alertas = ctk.CTkFrame(frame)
    frame_alertas.pack(pady=10)
    
    # Recuadros de alertas
    recuadro_1 = ctk.CTkFrame(frame_alertas, width=250, height=120, corner_radius=10, fg_color=COLORES['pH'], border_width=2, border_color="black")
    recuadro_1.grid(row=0, column=0, padx=10, pady=10)

    recuadro_2 = ctk.CTkFrame(frame_alertas, width=250, height=120, corner_radius=10, fg_color=COLORES['Temperatura'], border_width=2, border_color="black")
    recuadro_2.grid(row=0, column=1, padx=10, pady=10)

    recuadro_3 = ctk.CTkFrame(frame_alertas, width=250, height=120, corner_radius=10, fg_color=COLORES['Conductividad'], border_width=2, border_color="black")
    recuadro_3.grid(row=0, column=2, padx=10, pady=10)
    
    # Labels para las alertas
    label_1 = ctk.CTkLabel(recuadro_1, text="⚠️ ¡Alerta de pH! ⚠️\nSin alertas detectadas.", font=('Arial', 12, 'bold'), text_color=obtener_color_texto())
    label_1.pack(padx=10, pady=10)

    label_2 = ctk.CTkLabel(recuadro_2, text="⚠️ ¡Temperatura Alta! ⚠️\nSin alertas detectadas.", font=('Arial', 12, 'bold'), text_color=obtener_color_texto())
    label_2.pack(padx=10, pady=10)

    label_3 = ctk.CTkLabel(recuadro_3, text="⚠️ ¡Alerta de Conductividad! ⚠️\nSin alertas detectadas.", font=('Arial', 12, 'bold'), text_color=obtener_color_texto())
    label_3.pack(padx=10, pady=10)

    # Modal para mensajes
    frame_modal = ctk.CTkFrame(frame, width=300, height=150, corner_radius=10, fg_color='gray')
    label_modal = ctk.CTkLabel(frame_modal, text="Resolviendo...", font=('Arial', 14))
    label_modal.pack(padx=10, pady=40)
    
    # Crear tabla de historial (debe crearse antes de las funciones que la usan)
    frame_tabla_historial = crear_tabla_historial(frame, alertas)
    
    # Funciones para resolver alertas
    def resolver_pH():
        print("Resolviendo alerta de pH...")
        actualizar_alerta(id_alerta_pH, 'resuelta')
        mostrar_modal(frame_modal, label_modal, "pH", "resuelta")
        # Actualizar la tabla después de resolver
        nonlocal frame_tabla_historial
        frame_tabla_historial.pack_forget()
        frame_tabla_historial = crear_tabla_historial(frame, obtener_alertas())

    def resolver_temperatura():
        print("Resolviendo alerta de Temperatura...")
        actualizar_alerta(id_alerta_temperatura, 'resuelta')
        mostrar_modal(frame_modal, label_modal, "Temperatura", "resuelta")
        # Actualizar la tabla después de resolver
        nonlocal frame_tabla_historial
        frame_tabla_historial.pack_forget()
        frame_tabla_historial = crear_tabla_historial(frame, obtener_alertas())
    
    def resolver_conductividad():
        print("Resolviendo alerta de Conductividad...")
        actualizar_alerta(id_alerta_conductividad, 'resuelta')
        mostrar_modal(frame_modal, label_modal, "Conductividad", "resuelta")
        # Actualizar la tabla después de resolver
        nonlocal frame_tabla_historial
        frame_tabla_historial.pack_forget()
        frame_tabla_historial = crear_tabla_historial(frame, obtener_alertas())
    
    def descartar_alerta(tipo_alerta):
        print(f"Descartando alerta de {tipo_alerta}...")
        mostrar_modal(frame_modal, label_modal, tipo_alerta, "descartada")
        # Actualizar la tabla después de descartar
        nonlocal frame_tabla_historial
        frame_tabla_historial.pack_forget()
        frame_tabla_historial = crear_tabla_historial(frame, obtener_alertas())

    def editar_alerta(tipo_alerta, id_sensor):
        print(f"Editando alerta de {tipo_alerta}...")
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

    # Botones para cada alerta
    boton_1_resolver = ctk.CTkButton(recuadro_1, text="✔️ Resolver", command=resolver_pH, width=230, corner_radius=5, fg_color=COLORES['boton_pH'])
    boton_1_resolver.pack(pady=5, padx=10)
    
    boton_1_descartar = ctk.CTkButton(recuadro_1, text="❌ Descartar", command=lambda: descartar_alerta("pH"), width=230, corner_radius=5, fg_color="gray")
    boton_1_descartar.pack(pady=5, padx=10)
    
    id_alerta_pH = 1
    boton_1_editar = ctk.CTkButton(recuadro_1, text="✏️ Editar", command=lambda: editar_alerta("pH", id_alerta_pH), width=230, corner_radius=5, fg_color="#64B5F6")
    boton_1_editar.pack(pady=5, padx=10)
    
    boton_2_resolver = ctk.CTkButton(recuadro_2, text="✔️ Resolver", command=resolver_temperatura, width=230, corner_radius=5, fg_color=COLORES['boton_temperatura'])
    boton_2_resolver.pack(pady=5, padx=10)
    
    boton_2_descartar = ctk.CTkButton(recuadro_2, text="❌ Descartar", command=lambda: descartar_alerta("Temperatura"), width=230, corner_radius=5, fg_color="gray")
    boton_2_descartar.pack(pady=5, padx=10)
    
    id_alerta_temperatura = 2
    boton_2_editar = ctk.CTkButton(recuadro_2, text="✏️ Editar", command=lambda: editar_alerta("Temperatura", id_alerta_temperatura), width=230, corner_radius=5, fg_color="#81C784")
    boton_2_editar.pack(pady=5, padx=10)
    
    boton_3_resolver = ctk.CTkButton(recuadro_3, text="✔️ Resolver", command=resolver_conductividad, width=230, corner_radius=5, fg_color=COLORES['boton_conductividad'])
    boton_3_resolver.pack(pady=5, padx=10)
    
    boton_3_descartar = ctk.CTkButton(recuadro_3, text="❌ Descartar", command=lambda: descartar_alerta("Conductividad"), width=230, corner_radius=5, fg_color="gray")
    boton_3_descartar.pack(pady=5, padx=10)
    
    id_alerta_conductividad = 3
    boton_3_editar = ctk.CTkButton(recuadro_3, text="✏️ Editar", command=lambda: editar_alerta("Conductividad", id_alerta_conductividad), width=230, corner_radius=5, fg_color="#1976D2")
    boton_3_editar.pack(pady=5, padx=10)
    
    # Actualizar alertas si existen
    if len(alertas) > 0:
        label_1.configure(text=f"⚠️ ¡Alerta de pH! ⚠️\n{alertas[0]['descripcion']}")

    if len(alertas) > 1:
        label_2.configure(text=f"⚠️ ¡Temperatura Alta! ⚠️\n{alertas[1]['descripcion']}")

    if len(alertas) > 2:
        label_3.configure(text=f"⚠️ ¡Alerta de Conductividad! ⚠️\n{alertas[2]['descripcion']}")