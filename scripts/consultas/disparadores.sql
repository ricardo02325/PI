DELIMITER $$
CREATE TRIGGER FUERA_RANGO_AI
AFTER INSERT ON lecturas_sensores 
FOR EACH ROW
BEGIN
    IF NEW.id_sensor = 1 THEN
        IF NEW.valor < 5.0 THEN
            INSERT INTO alertas(tipo_alerta, descripcion, fecha_hora, estado)
            VALUES ('Valor fuera de rango', 'Valor del sensor muy bajo', NOW(),
                    (SELECT estado FROM sensores WHERE id_sensor = NEW.id_sensor));
        ELSEIF NEW.valor > 9.0 THEN
            INSERT INTO alertas(tipo_alerta, descripcion, fecha_hora, estado)
            VALUES ('Valor fuera de rango', 'Valor del sensor muy alto', NOW(),
                    (SELECT estado FROM sensores WHERE id_sensor = NEW.id_sensor));
        END IF;
    END IF;
END$$
DELIMITER ; 