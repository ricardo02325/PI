-- Disparador para sensor de ph
DELIMITER //

CREATE TRIGGER insertar_alerta_valor_fuera_de_rango_ph
AFTER INSERT ON lecturas_sensores
FOR EACH ROW
BEGIN
    DECLARE umbral_bajo FLOAT;
    DECLARE umbral_alto FLOAT;
    DECLARE estado_sensor VARCHAR(50);

    -- Definir los umbrales para el sensor PH
    SET umbral_bajo = 5.0;
    SET umbral_alto = 9.0;

    -- Obtener el estado del sensor PH desde la tabla 'sensores'
    SELECT estado INTO estado_sensor
    FROM sensores
    WHERE id_sensor = NEW.id_sensor;

    -- Verificar si el valor del sensor PH está fuera del rango
    IF NEW.id_sensor = 1 AND (NEW.valor < umbral_bajo OR NEW.valor > umbral_alto) THEN
        -- Insertar una alerta en la tabla 'alertas' con el estado del sensor
        INSERT INTO alertas (tipo_alerta, descripcion, fecha_hora, estado)
        VALUES ('Valor fuera de rango', 'Valor fuera de rango del sensor PH', NOW(), estado_sensor);
    END IF;
END //

DELIMITER ;

-- Ejemplo de Insert para que se dispare el disparador
INSERT INTO lecturas_sensores (id_sensor, valor, fecha_hora)
VALUES (1, 4.5, NOW());  -- En este caso, el valor es 4.5, que está fuera del rango para el sensor PH