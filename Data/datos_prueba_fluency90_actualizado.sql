Archivo de inserción de datos - Fluency90

-- Inserción de datos en la tabla idiomas (con código ISO)
INSERT INTO idiomas (nombre, codigo_iso) VALUES
('Inglés', 'en'),
('Francés', 'fr'),
('Alemán', 'de');

-- Inserción de usuarios
INSERT INTO usuarios (nombre, correo, idioma_id) VALUES
('Juan Pérez', 'juan@example.com', 1),
('Marie Curie', 'marie@example.com', 2),
('Hans Müller', 'hans@example.com', 3);

-- Inserción de lecciones
INSERT INTO lecciones (titulo, descripcion, idioma_id) VALUES
('Saludos básicos', 'Aprende a saludar en inglés', 1),
('Saludos en francés', 'Aprende a saludar en francés', 2);

-- Inserción de ejercicios
INSERT INTO ejercicios (leccion_id, tipo, contenido) VALUES
(1, 'seleccion_multiple', '¿Cómo se dice "Hola" en inglés?'),
(2, 'seleccion_multiple', '¿Cómo se dice "Buenos días" en francés?');

-- Inserción de opciones para ejercicios
INSERT INTO opciones (ejercicio_id, texto, es_correcta) VALUES
(1, 'Hello', true),
(1, 'Goodbye', false),
(2, 'Bonjour', true),
(2, 'Bonsoir', false);

-- Inserción de progreso del usuario
INSERT INTO progreso (usuario_id, leccion_id, completado) VALUES
(1, 1, true),
(2, 2, true),
(3, 1, false);

