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