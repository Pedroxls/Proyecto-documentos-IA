import sqlite3

DB_NAME = "seguimiento_estancias.db"

def insertar_alumno(nombre, correo, matricula, contraseña):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO alumnos (nombre, correo, matricula, contraseña)
        VALUES (?, ?, ?, ?)""", (nombre, correo, matricula, contraseña))
    conn.commit()
    conn.close()

def insertar_profesor(nombre, correo, departamento, contraseña):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO profesores (nombre, correo, departamento, contraseña)
        VALUES (?, ?, ?, ?)""", (nombre, correo, departamento, contraseña))
    conn.commit()
    conn.close()

def insertar_estancia(alumno_id, profesor_id, empresa, nombre_proyecto, descripcion, fecha_inicio, fecha_fin):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO estancias (alumno_id, profesor_id, empresa, nombre_proyecto, descripcion, fecha_inicio, fecha_fin)
        VALUES (?, ?, ?, ?, ?, ?, ?)""", (alumno_id, profesor_id, empresa, nombre_proyecto, descripcion, fecha_inicio, fecha_fin))
    conn.commit()
    conn.close()

def guardar_reporte(estancia_id, semana, actividades_planeadas, actividades_realizadas, fecha_envio, pdf_generado):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO reportes_semanales (estancia_id, semana, actividades_planeadas, actividades_realizadas, fecha_envio, pdf_generado)
        VALUES (?, ?, ?, ?, ?, ?)""", (estancia_id, semana, actividades_planeadas, actividades_realizadas, fecha_envio, pdf_generado))
    conn.commit()
    conn.close()

def consultar_historial_alumno(alumno_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        SELECT r.semana, r.fecha_envio, r.actividades_realizadas
        FROM reportes_semanales r
        JOIN estancias e ON r.estancia_id = e.id
        WHERE e.alumno_id = ?
        ORDER BY r.semana ASC
    """, (alumno_id,))
    historial = cur.fetchall()
    conn.close()
    return historial