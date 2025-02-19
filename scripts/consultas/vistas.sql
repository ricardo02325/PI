SELECT 
    sensores.id_sensor, 
    sensores.tipo_sensor, 
    sensores.estado, 
    sensores.fecha_instalacion, 
    lecturas_sensores.valor, 
    lecturas_sensores.fecha_hora
FROM sensores
INNER JOIN lecturas_sensores ON sensores.id_sensor = lecturas_sensores.id_sensor;