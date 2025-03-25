import sys
import os
import customtkinter as ctk

# Asegúrate de que el directorio que contiene tu módulo se añada al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

# Importar todas las funciones necesarias desde src.models.models
from src.models.models import (
    obtener_alertas,
    actualizar_trigger,
    actualizar_alerta  # Importar la función para actualizar el estado de la alerta
)

COLORES = {
    'pH': '#A8E6CF',  # Verde pastel para pH
    'Temperatura': '#FFABAB',  # Rosa claro para Temperatura
    'Conductividad': '#FFD3B6',  # Amarillo suave para Conductividad
    'boton_pH': '#81C784',  # Verde suave para botones de pH
    'boton_temperatura': '#FF8A80',  # Rosa pastel para botones de temperatura
    'boton_conductividad': '#FFB74D',  # Naranja suave para botones de conductividad
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

def iniciar_alertas(frame):
    alertas = obtener_alertas()  # Llamar a la función importada

    # Frame para el título
    frame_titulo = ctk.CTkFrame(frame)
    frame_titulo.pack(pady=(20, 10))
    label_titulo = ctk.CTkLabel(frame_titulo, text="🚨 Alertas 🚨", font=('Arial', 20, 'bold'), text_color=obtener_color_texto())
    label_titulo.pack()

    # Frame para los recuadros de alertas
    frame_alertas = ctk.CTkFrame(frame)
    frame_alertas.pack(pady=10)

    # Crear recuadros de alerta con colores suaves y armoniosos
    recuadro_1 = ctk.CTkFrame(frame_alertas, width=250, height=120, corner_radius=10, fg_color=COLORES['pH'], border_width=2, border_color="black")
    recuadro_1.grid(row=0, column=0, padx=10, pady=10)

    recuadro_2 = ctk.CTkFrame(frame_alertas, width=250, height=120, corner_radius=10, fg_color=COLORES['Temperatura'], border_width=2, border_color="black")
    recuadro_2.grid(row=0, column=1, padx=10, pady=10)

    recuadro_3 = ctk.CTkFrame(frame_alertas, width=250, height=120, corner_radius=10, fg_color=COLORES['Conductividad'], border_width=2, border_color="black")
    recuadro_3.grid(row=0, column=2, padx=10, pady=10)

    # Etiquetas con íconos y texto dinámico
    label_1 = ctk.CTkLabel(recuadro_1, text="⚠️ ¡Alerta de pH! ⚠️\nSin alertas detectadas.", font=('Arial', 12, 'bold'), text_color=obtener_color_texto())
    label_1.pack(padx=10, pady=10)

    label_2 = ctk.CTkLabel(recuadro_2, text="⚠️ ¡Temperatura Alta! ⚠️\nSin alertas detectadas.", font=('Arial', 12, 'bold'), text_color=obtener_color_texto())
    label_2.pack(padx=10, pady=10)

    label_3 = ctk.CTkLabel(recuadro_3, text="⚠️ ¡Alerta de Conductividad! ⚠️\nSin alertas detectadas.", font=('Arial', 12, 'bold'), text_color=obtener_color_texto())
    label_3.pack(padx=10, pady=10)

    def resolver_pH():
        print("Resolviendo alerta de pH...")
        # Actualizar estado a "resuelta" y mostrar modal
        actualizar_alerta(id_alerta_pH, 'resuelta')
        mostrar_modal(frame_modal, label_modal, "pH", "resuelta")

    def resolver_temperatura():
        print("Resolviendo alerta de Temperatura...")
        # Actualizar estado a "resuelta" y mostrar modal
        actualizar_alerta(id_alerta_temperatura, 'resuelta')
        mostrar_modal(frame_modal, label_modal, "Temperatura", "resuelta")
    
    def resolver_conductividad():
        print("Resolviendo alerta de Conductividad...")
        # Actualizar estado a "resuelta" y mostrar modal
        actualizar_alerta(id_alerta_conductividad, 'resuelta')
        mostrar_modal(frame_modal, label_modal, "Conductividad", "resuelta")
    
    def descartar_alerta(tipo_alerta):
        print(f"Descartando alerta de {tipo_alerta}...")
        # Actualizar estado a "descartada"
        mostrar_modal(frame_modal, label_modal, tipo_alerta, "descartada")


    def editar_alerta(tipo_alerta, id_sensor):
        # Llamar al formulario de edición, que puede ser un modal con un formulario
        print(f"Editando alerta de {tipo_alerta}...")

        # Mostrar formulario de edición con valores máximos y mínimos
        formulario_modal = ctk.CTkFrame(frame, width=400, height=300, corner_radius=10, fg_color="lightgray")
        formulario_modal.place(relx=0.5, rely=0.5, anchor="center")

        label_titulo_formulario = ctk.CTkLabel(formulario_modal, text=f"Editar alerta de {tipo_alerta}", font=('Arial', 14, 'bold'))
        label_titulo_formulario.pack(pady=10)

        # Campos para el valor máximo y mínimo
        label_valor_max = ctk.CTkLabel(formulario_modal, text="Valor máximo:", font=('Arial', 12))
        label_valor_max.pack(pady=5)

        entry_valor_max = ctk.CTkEntry(formulario_modal, font=('Arial', 12))
        entry_valor_max.pack(pady=5)

        label_valor_min = ctk.CTkLabel(formulario_modal, text="Valor mínimo:", font=('Arial', 12))
        label_valor_min.pack(pady=5)

        entry_valor_min = ctk.CTkEntry(formulario_modal, font=('Arial', 12))
        entry_valor_min.pack(pady=5)

        # Botón de enviar para actualizar el trigger
        def enviar_edicion():
            try:
                valor_min = float(entry_valor_min.get())
                valor_max = float(entry_valor_max.get())

                if valor_min is not None and valor_max is not None:
                    # Usar id_sensor que fue pasado como argumento
                    actualizar_trigger(id_sensor, valor_min, valor_max)

                    # Confirmar la actualización del trigger
                    print(f"Trigger de {tipo_alerta} actualizado con valor mínimo: {valor_min}, valor máximo: {valor_max}")
                    formulario_modal.place_forget()  # Cerrar el modal después de actualizar
                else:
                    print("Por favor ingrese valores válidos.")

            except ValueError:
                print("Error: Ingrese valores numéricos válidos.")

        boton_enviar = ctk.CTkButton(formulario_modal, text="✔️ Enviar", command=enviar_edicion, width=230, corner_radius=5, fg_color="green")
        boton_enviar.pack(pady=10)

        # Botón para cerrar el formulario sin realizar cambios
        boton_cerrar = ctk.CTkButton(formulario_modal, text="❌ Cerrar", command=formulario_modal.place_forget, width=230, corner_radius=5, fg_color="red")
        boton_cerrar.pack(pady=5)

    # Botones con íconos para resolver, editar y descartar
    boton_1_resolver = ctk.CTkButton(recuadro_1, text="✔️ Resolver", command=resolver_pH, width=230, corner_radius=5, fg_color=COLORES['boton_pH'])
    boton_1_resolver.pack(pady=5, padx=10)
    
    boton_1_descartar = ctk.CTkButton(recuadro_1, text="❌ Descartar", command=lambda: descartar_alerta("pH"), width=230, corner_radius=5, fg_color="gray")
    boton_1_descartar.pack(pady=5, padx=10)
    
    # Suponiendo que el id del sensor de pH es 'id_sensor_pH'
    id_alerta_pH = 1  # Esta es solo una suposición, reemplázalo con el valor real
    boton_1_editar = ctk.CTkButton(recuadro_1, text="✏️ Editar", command=lambda: editar_alerta("pH", id_alerta_pH), width=230, corner_radius=5, fg_color="#64B5F6")  # Azul suave
    boton_1_editar.pack(pady=5, padx=10)
    
    boton_2_resolver = ctk.CTkButton(recuadro_2, text="✔️ Resolver", command=resolver_temperatura, width=230, corner_radius=5, fg_color=COLORES['boton_temperatura'])
    boton_2_resolver.pack(pady=5, padx=10)
    
    boton_2_descartar = ctk.CTkButton(recuadro_2, text="❌ Descartar", command=lambda: descartar_alerta("Temperatura"), width=230, corner_radius=5, fg_color="gray")
    boton_2_descartar.pack(pady=5, padx=10)
    
    # Suponiendo que el id del sensor de Temperatura es 'id_sensor_temperatura'
    id_alerta_temperatura = 2  # Esta es solo una suposición, reemplázalo con el valor real
    boton_2_editar = ctk.CTkButton(recuadro_2, text="✏️ Editar", command=lambda: editar_alerta("Temperatura", id_alerta_temperatura), width=230, corner_radius=5, fg_color="#81C784")  # Verde suave
    boton_2_editar.pack(pady=5, padx=10)
    
    boton_3_resolver = ctk.CTkButton(recuadro_3, text="✔️ Resolver", command=resolver_conductividad, width=230, corner_radius=5, fg_color=COLORES['boton_conductividad'])
    boton_3_resolver.pack(pady=5, padx=10)
    
    boton_3_descartar = ctk.CTkButton(recuadro_3, text="❌ Descartar", command=lambda: descartar_alerta("Conductividad"), width=230, corner_radius=5, fg_color="gray")
    boton_3_descartar.pack(pady=5, padx=10)
    
    # Suponiendo que el id del sensor de Conductividad es 'id_sensor_conductividad'
    id_alerta_conductividad = 3  # Esta es solo una suposición, reemplázalo con el valor real
    boton_3_editar = ctk.CTkButton(recuadro_3, text="✏️ Editar", command=lambda: editar_alerta("Conductividad", id_alerta_conductividad), width=230, corner_radius=5, fg_color="#FFEB3B")  # Amarillo suave
    boton_3_editar.pack(pady=5, padx=10)
    
    # Modal de resolución de alerta
    frame_modal = ctk.CTkFrame(frame, width=300, height=150, corner_radius=10, fg_color='gray')
    label_modal = ctk.CTkLabel(frame_modal, text="Resolviendo...", font=('Arial', 14))
    label_modal.pack(padx=10, pady=40)
    
    # Actualizar etiquetas con alertas si existen
    if len(alertas) > 0:
        # Asignar alerta de pH al recuadro 1
        label_1.configure(text=f"⚠️ ¡Alerta de pH! ⚠️\n{alertas[0]['descripcion']}")

    if len(alertas) > 1:
        # Asignar alerta de Temperatura al recuadro 2
        label_2.configure(text=f"⚠️ ¡Temperatura Alta! ⚠️\n{alertas[1]['descripcion']}")

    if len(alertas) > 2:
        # Asignar alerta de Conductividad al recuadro 3
        label_3.configure(text=f"⚠️ ¡Alerta de Conductividad! ⚠️\n{alertas[2]['descripcion']}")