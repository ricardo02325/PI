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
