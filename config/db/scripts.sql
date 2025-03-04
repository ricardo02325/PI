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

-- Temperatura, tigger disparador.
CREATE TRIGGER `Temperatura_AI` AFTER INSERT ON `lecturas_sensores`
 FOR EACH ROW BEGIN
    IF NEW.id_sensor = 3 THEN
        IF NEW.valor < 10 THEN
            INSERT INTO alertas(tipo_alerta, descripcion, fecha_hora, estado)
            VALUES ('Valor fuera de rango', 'Valor de la Temperatura baja', NOW(),
                    (SELECT estado FROM sensores WHERE id_sensor = NEW.id_sensor));
        ELSEIF NEW.valor > 25 THEN
            INSERT INTO alertas(tipo_alerta, descripcion, fecha_hora, estado)
            VALUES ('Valor fuera de rango', 'Valor de la Temperatura alta', NOW(),
                    (SELECT estado FROM sensores WHERE id_sensor = NEW.id_sensor));
        END IF;
    END IF;
END




CREATE TABLE mantenimiento (
  id_mantenimiento INT NOT NULL AUTO_INCREMENT,
  id_usuario INT NOT NULL,
  id_configuracion INT NULL,  -- Permitir NULL para que ON DELETE SET NULL funcione correctamente
  descripcion TEXT NOT NULL,
  fecha_mantenimiento DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id_mantenimiento),
  FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
  FOREIGN KEY (id_configuracion) REFERENCES configuracion_sistema(id_configuracion) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Conductividad Electrica, tigger de Phoo
CREATE TRIGGER `Conductividad_Elec` AFTER INSERT ON `lecturas_sensores`
 FOR EACH ROW BEGIN
    IF NEW.id_sensor = 4 THEN
        IF NEW.valor < 50 THEN
            INSERT INTO alertas(tipo_alerta, descripcion, fecha_hora, estado)
            VALUES ('Valor fuera de rango', 'Valor de la Conductividad Electrica baja', NOW(),
                    (SELECT estado FROM sensores WHERE id_sensor = NEW.id_sensor));
        ELSEIF NEW.valor > 2000 THEN
            INSERT INTO alertas(tipo_alerta, descripcion, fecha_hora, estado)
            VALUES ('Valor fuera de rango', 'Valor de la Conductividad Electrica alta', NOW(),
                    (SELECT estado FROM sensores WHERE id_sensor = NEW.id_sensor));
        END IF;
    END IF;
END