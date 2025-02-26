-- Crear vista de Sensores.
SELECT 
    sensores.id_sensor, 
    sensores.tipo_sensor, 
    sensores.estado, 
    lecturas_sensores.id_lectura, 
    lecturas_sensores.valor, 
    lecturas_sensores.fecha_hora
FROM sensores
INNER JOIN lecturas_sensores ON sensores.id_sensor = lecturas_sensores.id_sensor;

-- Creacion de la vista de Actuadores.
CREATE VIEW inf_actuadores AS 
SELECT 
    a.id_actuador, 
    a.tipo_actuador, 
    a.ubicacion, 
    a.fecha_instalacion, 
    a.estado, 
    e.id_evento, 
    e.accion, 
    e.fecha_hora
FROM actuadores a
INNER JOIN eventos_actuadores e ON a.id_actuador = e.id_actuador;

-- Creación de configuración de sistemas.
CREATE VIEWS conf_sistema AS
SELECT id_configuracion, parametro, valor, fecha_actualizacion
FROM configuracion_sistema
