DROP TABLE IF EXISTS directorio;
CREATE TABLE directorio(
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    area NOT NULL,
    dependencia NOT NULL,
    telefono NOT NULL,
    ubicacion NOT NULL,
    correo NOT NULL,
    extension NOT NULL,
    adicionales DEFAULT NULL
);

DROP TABLE IF EXISTS academic_calendar;
CREATE TABLE academic_calendar(
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    actividad TEXT NOT NULL,
    fecha TEXT(20) NOT NULL
);

CREATE TABLE request_calendar(
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    indice INTEGER NOT NULL,
    actividad TEXT NOT NULL,
    fecha TEXT(20) NOT NULL,
    tipo_estudiante TEXT(20) NOT NULL
);

DROP TABLE IF EXISTS grupos;
CREATE TABLE grupos(
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    codigo INTEGER NOT NULL,
    nombre NOT NULL,
    enlace NOT NULL
);