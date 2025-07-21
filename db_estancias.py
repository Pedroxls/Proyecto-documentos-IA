
import sqlite3

def crear_base_datos_estancias(nombre_db="seguimiento_estancias.db"):
    conn = sqlite3.connect(nombre_db)
    cursor = conn.cursor()

    # Tabla: alumnos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS alumnos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        correo TEXT,
        matricula TEXT NOT NULL,
        contraseña TEXT
    )
    """)

    # Tabla: profesores
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS profesores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        correo TEXT,
        departamento TEXT,
        contraseña TEXT
    )
    """)

    # Tabla: administradores
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS administradores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        correo TEXT,
        contraseña TEXT
    )
    """)

    # Tabla: estancias
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS estancias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        alumno_id INTEGER NOT NULL,
        profesor_id INTEGER NOT NULL,
        empresa TEXT,
        nombre_proyecto TEXT,
        descripcion TEXT,
        fecha_inicio DATE,
        fecha_fin DATE,
        FOREIGN KEY (alumno_id) REFERENCES alumnos(id),
        FOREIGN KEY (profesor_id) REFERENCES profesores(id)
    )
    """)

    # Tabla: reportes_semanales
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reportes_semanales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        estancia_id INTEGER NOT NULL,
        semana INTEGER,
        actividades_planeadas TEXT,
        actividades_realizadas TEXT,
        fecha_envio DATE,
        pdf_generado TEXT,
        FOREIGN KEY (estancia_id) REFERENCES estancias(id)
    )
    """)

    # Tabla: checklist_profesor
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS checklist_profesor (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        reporte_id INTEGER NOT NULL,
        comentarios TEXT,
        retro_ia TEXT,
        calificacion INTEGER,
        fecha_revision DATE,
        FOREIGN KEY (reporte_id) REFERENCES reportes_semanales(id)
    )
    """)

    # Tabla: memorandums
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS memorandums (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        estancia_id INTEGER NOT NULL,
        fecha_generacion DATE,
        archivo_pdf TEXT,
        observaciones TEXT,
        FOREIGN KEY (estancia_id) REFERENCES estancias(id)
    )
    """)

    conn.commit()
    conn.close()
    print(f"Base de datos '{nombre_db}' creada correctamente con todas las tablas.")

if __name__ == "__main__":
    crear_base_datos_estancias()
