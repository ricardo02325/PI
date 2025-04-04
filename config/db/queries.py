# queries.py

# Consultas SQL
QUERY_SENSORES = """
SELECT id_sensor, tipo_sensor, estado, fecha_instalacion, valor, fecha_hora
FROM php
"""

QUERY_SENSOR_POR_ID = """
SELECT id_sensor, tipo_sensor, estado, fecha_instalacion, valor, fecha_hora
FROM php
WHERE id_sensor = %s
"""


QUERY_LECTURAS_SENSOR = """
SELECT id_lectura, id_sensor, valor, fecha_hora
FROM lecturas_sensores
WHERE id_sensor = %s AND fecha_hora BETWEEN %s AND %s
ORDER BY fecha_hora ASC;
"""


QUERY_ACTUADORES = """
SELECT a.id_actuador, a.tipo_actuador, a.ubicacion, a.fecha_instalacion, a.estado,
       e.accion, e.fecha_hora
FROM actuadores a
LEFT JOIN (
    SELECT id_actuador, accion, fecha_hora
    FROM eventos_actuadores 
    WHERE fecha_hora = (SELECT MAX(fecha_hora) FROM eventos_actuadores WHERE id_actuador = eventos_actuadores.id_actuador)
) e ON a.id_actuador = e.id_actuador;
"""


QUERY_ALERTAS = """
SELECT id_alerta, tipo_alerta, descripcion, fecha_hora, estado
FROM alertas
WHERE fecha_hora BETWEEN %s AND %s
ORDER BY fecha_hora DESC;
"""


QUERY_CONFIGURACION = """
SELECT id_configuracion, parametro, valor, fecha_actualizacion
FROM configuracion_sistema
ORDER BY fecha_actualizacion DESC;
"""


QUERY_USUARIOS = """
SELECT id_usuario, nombre, rol, fecha_registro
FROM usuarios;
"""

QUERY_USUARIO_POR_ID = """
SELECT id_usuario, nombre, rol, fecha_registro
FROM usuarios
WHERE id_usuario = %s;
"""

QUERY_EVENTOS_ACTUADOR = """
SELECT id_evento, id_actuador, accion, fecha_hora
FROM eventos_actuadores
WHERE id_actuador = %s
ORDER BY fecha_hora DESC;
"""