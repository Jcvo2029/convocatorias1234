
CREATE DATABASE IF NOT EXISTS convocatorias_culturales;
USE convocatorias_culturales;

CREATE TABLE IF NOT EXISTS api_convocatorias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    no_convocatoria INT,
    año YEAR,
    nombre_convocatoria VARCHAR(255),
    nombre_ganador VARCHAR(255),
    area VARCHAR(100),
    modalidad VARCHAR(100),
    nombre_proyecto VARCHAR(255),
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS convocatorias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    cupos INT NOT NULL,
    nombre_proyecto VARCHAR(255),
    estado ENUM('abierta', 'cerrada') DEFAULT 'abierta',
    area VARCHAR(100) NOT NULL,
    modalidad VARCHAR(100) NOT NULL,
    CHECK (fecha_fin > fecha_inicio)
);

CREATE TABLE IF NOT EXISTS participantes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cedula VARCHAR(20) NOT NULL UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    edad INT NOT NULL,
    id_convocatoria INT NOT NULL,
    estado_convocatoria ENUM('abierta', 'cerrada'),
    fecha_inscripcion DATE NOT NULL,
    FOREIGN KEY (id_convocatoria) REFERENCES convocatorias(id),
    CHECK (edad >= 18),
    CHECK (fecha_inscripcion < (SELECT fecha_inicio FROM convocatorias WHERE id = id_convocatoria))
);

CREATE TABLE IF NOT EXISTS ganadores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_participante INT NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    id_convocatoria INT NOT NULL,
    FOREIGN KEY (id_participante) REFERENCES participantes(id),
    FOREIGN KEY (id_convocatoria) REFERENCES convocatorias(id)
);

CREATE INDEX idx_area ON convocatorias(area);
CREATE INDEX idx_modalidad ON convocatorias(modalidad);
CREATE INDEX idx_estado ON convocatorias(estado);
CREATE INDEX idx_convocatoria_participante ON participantes(id_convocatoria);