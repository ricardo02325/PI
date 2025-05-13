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
    'pH': '#B0E0E6',  # Azul pastel suave (similar al tono de la vestimenta de Loid)
    'Temperatura': '#98FB98',  # Verde claro elegante
    'Conductividad': '#FFFACD',  # Amarillo oscuro suave
    'border': '#4682B4',  # Azul medianoche suave para bordes
    'header_bg': '#4F94CD',  # Azul claro para los encabezados
    'row_selected': '#B0E0E6'  # Color suave para la fila seleccionada
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
    """Crea una tabla moderna con el historial de alertas dentro del frame dado."""

    # Frame contenedor
    frame_tabla = ctk.CTkFrame(frame, fg_color="transparent")
    frame_tabla.pack(pady=(20, 10), padx=20, fill="both", expand=True)

    # Estilo de la tabla
    estilo = ttk.Style()
    estilo.theme_use('clam')

    # Colores según el modo oscuro o claro
    modo = ctk.get_appearance_mode()
    colores = {
        "dark": {"bg": "#212121", "fg": "white", "heading_bg": "#1A237E", "alt_row": "#90CAF9", "border": "#01579B"},
        "light": {"bg": "white", "fg": "black", "heading_bg": "#66bb6a", "alt_row": "#f1f8e9", "border": "#43a047"}
    }

    colores_actuales = colores["dark"] if modo == "dark" else colores["light"]

    # Configurar el estilo del Treeview
    estilo.configure(
        "Treeview",
        background=colores_actuales["bg"],
        foreground=colores_actuales["fg"],
        rowheight=40,
        fieldbackground=colores_actuales["bg"],
        font=('Arial', 12),
        borderwidth=1,
        relief="flat",
        highlightthickness=1  # Bordes visibles al seleccionar
    )

    # Estilo de encabezado
    estilo.configure(
        "Treeview.Heading",
        background=colores_actuales["heading_bg"],
        foreground="white",
        font=('Arial', 14, 'bold'),
        relief="flat",
        anchor="center"
    )

    # Resaltar fila seleccionada
    estilo.map("Treeview", background=[("selected", "#039BE5")])

    # Crear la tabla con columnas
    tabla = ttk.Treeview(
        frame_tabla,
        columns=('id_alerta', 'tipo_alerta', 'descripcion', 'fecha_hora', 'estado'),
        show='headings',
        style="Treeview"
    )

    # Configurar columnas con bordes redondeados y mejor alineación
    tabla.column('id_alerta', width=80, anchor='center')
    tabla.column('tipo_alerta', width=180, anchor='center')
    tabla.column('descripcion', width=300, anchor='w')
    tabla.column('fecha_hora', width=220, anchor='center')
    tabla.column('estado', width=150, anchor='center')

    # Encabezados con iconos y diseño atractivo
    tabla.heading('id_alerta', text='🔍 ID')
    tabla.heading('tipo_alerta', text='⚠️ Tipo')
    tabla.heading('descripcion', text='📜 Descripción')
    tabla.heading('fecha_hora', text='📅 Fecha')
    tabla.heading('estado', text='🟢 Estado')

    # Scrollbar
    scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=tabla.yview)
    scrollbar.pack(side="right", fill="y")
    tabla.configure(yscrollcommand=scrollbar.set)

    # Insertar datos con colores alternos
    for i, alerta in enumerate(alertas):
        estado = alerta.get('estado', 'activa').lower()
        color_fila = colores_actuales["alt_row"] if i % 2 == 0 else colores_actuales["bg"]

        tabla.insert(
            '',
            'end',
            values=( 
                alerta.get('id_alerta', ''),
                alerta.get('tipo_alerta', ''),
                alerta.get('descripcion', ''),
                alerta.get('fecha_hora', ''),
                estado.capitalize()
            ),
            tags=(estado, "alterno" if i % 2 == 0 else "normal")
        )

    # Configurar colores para los estados
    tabla.tag_configure("alterno", background=colores_actuales["alt_row"])
    tabla.tag_configure("normal", background=colores_actuales["bg"])
    tabla.tag_configure("resuelta", foreground="#388E3C", font=("Arial", 12, "bold"))  # Verde
    tabla.tag_configure("activa", foreground="#D32F2F", font=("Arial", 12, "bold"))  # Rojo
    tabla.tag_configure("descartada", foreground="#757575", font=("Arial", 12, "bold"))  # Gris

    tabla.pack(fill="both", expand=True, padx=10, pady=10)

    return frame_tabla



def iniciar_alertas(frame):
    alertas = obtener_alertas_completas()
    
    # Frame para el título
    frame_titulo = ctk.CTkFrame(frame, fg_color="#E3F2FD")
    frame_titulo.pack(pady=(20, 10))
    label_titulo = ctk.CTkLabel(frame_titulo, text="🚨 Alertas 🚨", font=('Arial', 20, 'bold'), text_color=obtener_color_texto())
    label_titulo.pack()
    
    # Frame para las alertas actuales
    frame_alertas = ctk.CTkFrame(frame, fg_color="#E3F2FD")
    frame_alertas.pack(pady=10)
    
    # Recuadros de alertas
    recuadro_1 = ctk.CTkFrame(frame_alertas, width=250, height=120, corner_radius=10, fg_color=COLORES['pH'], border_width=2, border_color="black")
    recuadro_1.grid(row=0, column=0, padx=10, pady=10)

    recuadro_2 = ctk.CTkFrame(frame_alertas, width=250, height=120, corner_radius=10, fg_color=COLORES['Temperatura'], border_width=2, border_color="black")
    recuadro_2.grid(row=0, column=1, padx=10, pady=10)

    recuadro_3 = ctk.CTkFrame(frame_alertas, width=250, height=120, corner_radius=10, fg_color=COLORES['Conductividad'], border_width=2, border_color="black")
    recuadro_3.grid(row=0, column=2, padx=10, pady=10)
    
    # Labels para las alertas
    label_1 = ctk.CTkLabel(recuadro_1, text="⚠️ ¡Alerta de pH! ⚠️\nSin alertas detectadas.", font=('Arial', 19, 'bold'), text_color=obtener_color_texto())
    label_1.pack(padx=10, pady=10)

    label_2 = ctk.CTkLabel(recuadro_2, text="⚠️ ¡Temperatura Alta! ⚠️\nSin alertas detectadas.", font=('Arial', 19, 'bold'), text_color=obtener_color_texto())
    label_2.pack(padx=10, pady=10)

    label_3 = ctk.CTkLabel(recuadro_3, text="⚠️ ¡Alerta de Conductividad! ⚠️\nSin alertas detectadas.", font=('Arial', 19, 'bold'), text_color=obtener_color_texto())
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
    boton_1_resolver = ctk.CTkButton(recuadro_1, text="✔️ Resolver", command=resolver_pH, width=230, corner_radius=5, fg_color="#4CAF50")
    boton_1_resolver.pack(pady=5, padx=10)

    
    boton_1_descartar = ctk.CTkButton(recuadro_1, text="❌ Descartar", command=lambda: descartar_alerta("pH"), width=230, corner_radius=5, fg_color="gray")
    boton_1_descartar.pack(pady=5, padx=10)
    
    id_alerta_pH = 1
    boton_1_editar = ctk.CTkButton(recuadro_1, text="✏️ Editar", command=lambda: editar_alerta("pH", id_alerta_pH), width=230, corner_radius=5, fg_color="#1976D2")
    boton_1_editar.pack(pady=5, padx=10)
    
    boton_2_resolver = ctk.CTkButton(recuadro_2, text="✔️ Resolver", command=resolver_temperatura, width=230, corner_radius=5, fg_color="#4CAF50")
    boton_2_resolver.pack(pady=5, padx=10)
    
    boton_2_descartar = ctk.CTkButton(recuadro_2, text="❌ Descartar", command=lambda: descartar_alerta("Temperatura"), width=230, corner_radius=5, fg_color="gray")
    boton_2_descartar.pack(pady=5, padx=10)
    
    id_alerta_temperatura = 2
    boton_2_editar = ctk.CTkButton(recuadro_2, text="✏️ Editar", command=lambda: editar_alerta("Temperatura", id_alerta_temperatura), width=230, corner_radius=5, fg_color="#1976D2")
    boton_2_editar.pack(pady=5, padx=10)

    
    boton_3_resolver = ctk.CTkButton(recuadro_3, text="✔️ Resolver", command=resolver_conductividad, width=230, corner_radius=5, fg_color="#4CAF50")
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
        label_2.configure(text=f"⚠️ ¡Alerta de Conductividad! ⚠️\n{alertas[1]['descripcion']}")

    if len(alertas) > 2:
        label_3.configure(text=f"⚠️ ¡Temperatura Alta! ⚠️\n{alertas[2]['descripcion']}")