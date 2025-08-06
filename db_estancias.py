
# db_estancias.py ( Actualizado)

import sqlite3

def crear_base_datos_estancias(nombre_db="seguimiento_estancias.db"):
    conn = sqlite3.connect(nombre_db)
    cursor = conn.cursor()

    # --- TABLAS EXISTENTES (SIN CAMBIOS) ---
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS alumnos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        correo TEXT,
        matricula TEXT NOT NULL,
        contraseña TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS profesores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        correo TEXT,
        departamento TEXT,
        contraseña TEXT
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS administradores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        correo TEXT,
        contraseña TEXT
    )
    """)

    # --- TABLA "estancias" ACTUALIZADA CON NUEVOS CAMPOS ---
    # Se eliminó la tabla anterior para volver a crearla con la nueva estructura
    cursor.execute("DROP TABLE IF EXISTS estancias")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS estancias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        
        -- Datos de vinculación principales --
        alumno_id INTEGER NOT NULL,
        profesor_id INTEGER NOT NULL,
        
        -- Campos de "Información General" (Preguntas 1-5) --
        nombre_alumno TEXT,
        nombre_proyecto TEXT,
        lider_proyecto TEXT,
        area_empresarial TEXT,
        fecha_elaboracion DATE,
        
        -- Campos de "Formalización" (Pregunta 6) --
        justificacion_proposito TEXT,
        
        -- Campos de "Descripción" (Preguntas 7-10) --
        antecedentes_desc TEXT,
        descripcion_problema TEXT,
        situacion_problema_actual TEXT,
        expectativas_proyecto TEXT,
        
        -- Campos de "Entregables" y "Alcance" (Preguntas 11-12) --
        productos_entregar TEXT,
        antecedentes_area TEXT,
        
        -- Campos de "Restricciones" (Pregunta 13) --
        restriccion_costos TEXT,
        restriccion_materiales TEXT,
        restriccion_humanos TEXT,
        restriccion_tiempo TEXT,
        restriccion_calidad TEXT,
        restriccion_alcance TEXT,
        restriccion_riesgos TEXT,
        
        -- Campo de "Impacto" (Pregunta 51) --
        impacto_actividades TEXT,
        
        -- Campo para el archivo del cronograma (Pregunta 52) --
        diagrama_path TEXT,

        FOREIGN KEY (alumno_id) REFERENCES alumnos(id),
        FOREIGN KEY (profesor_id) REFERENCES profesores(id)
    )
    """)

    # --- NUEVA TABLA: fases_proyecto ---
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS fases_proyecto (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        estancia_id INTEGER NOT NULL,
        nombre_fase TEXT,
        descripcion TEXT,
        duracion TEXT,
        entregable TEXT,
        criterio_exito TEXT,
        recomendacion_nps INTEGER,
        FOREIGN KEY (estancia_id) REFERENCES estancias(id)
    )
    """)

    # --- NUEVA TABLA: tareas_proyecto ---
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tareas_proyecto (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        estancia_id INTEGER NOT NULL,
        fase_correspondiente TEXT,
        nombre_tarea TEXT,
        entregable_tarea TEXT,
        criterio_exito_tarea TEXT,
        fecha_inicio DATE,
        fecha_fin DATE,
        responsable_tarea TEXT,
        FOREIGN KEY (estancia_id) REFERENCES estancias(id)
    )
    """)

    # --- TABLAS RESTANTES (SIN CAMBIOS) ---
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
    print(f"✅ Base de datos '{nombre_db}' actualizada correctamente con la nueva estructura.")

if __name__ == "__main__":
    crear_base_datos_estancias()