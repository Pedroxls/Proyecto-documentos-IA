# insertar_usuarios_prueba.py
import sqlite3

def insertar_datos_demo():
    """
    Inserta un alumno y un profesor de prueba para poder
    demostrar el funcionamiento del sistema.
    """
    DB_NAME = "seguimiento_estancias.db"
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    print("Conectado a la base de datos...")

    try:
        # --- Insertar Alumno de Prueba ---
        # Verificamos si ya existe para no duplicarlo
        cur.execute("SELECT id FROM alumnos WHERE correo = ?", ('alumno.prueba@tec.mx',))
        if cur.fetchone() is None:
            cur.execute("""
                INSERT INTO alumnos (nombre, correo, matricula, contraseña)
                VALUES (?, ?, ?, ?)
            """, ("Alumno de Prueba", "alumno.prueba@tec.mx", "A01234567", "alumno123"))
            print("✅ Usuario 'alumno.prueba@tec.mx' insertado.")
        else:
            print("ℹ️  El alumno de prueba ya existe.")

        # --- Insertar Profesor de Prueba ---
        # Verificamos si ya existe para no duplicarlo
        cur.execute("SELECT id FROM profesores WHERE correo = ?", ('profesor.prueba@tec.mx',))
        if cur.fetchone() is None:
            cur.execute("""
                INSERT INTO profesores (nombre, correo, departamento, contraseña)
                VALUES (?, ?, ?, ?)
            """, ("Profesor de Prueba", "profesor.prueba@tec.mx", "Computación", "profe123"))
            print("✅ Usuario 'profesor.prueba@tec.mx' insertado.")
        else:
            print("ℹ️  El profesor de prueba ya existe.")
        
        conn.commit()
        print("\nDatos de prueba listos.")

    except Exception as e:
        print(f"\n❌ Ocurrió un error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    insertar_datos_demo()