# preparar_demo.py
import sqlite3

def preparar_base_para_demo():
        DB_NAME = "seguimiento_estancias.db"
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        print("Conectado a la base de datos...")

        try:
            # --- Crear Administrador ---
            cur.execute("SELECT id FROM administradores WHERE correo = ?", ('admin.demo@tec.mx',))
            if cur.fetchone() is None:
                cur.execute("INSERT INTO administradores (nombre, correo, contraseña) VALUES (?, ?, ?)",
                            ("Admin Demo", "admin.demo@tec.mx", "admin123"))
                print("✅ Usuario 'admin.demo@tec.mx' (admin) creado.")
            
            # --- Crear Profesor ---
            cur.execute("SELECT id FROM profesores WHERE correo = ?", ('profesor.demo@tec.mx',))
            if cur.fetchone() is None:
                cur.execute("INSERT INTO profesores (nombre, correo, departamento, contraseña) VALUES (?, ?, ?, ?)",
                            ("Profesor Demo", "profesor.demo@tec.mx", "Computación", "profe123"))
                print("✅ Usuario 'profesor.demo@tec.mx' (profesor) creado.")

            # --- Crear Alumno ---
            cur.execute("SELECT id FROM alumnos WHERE correo = ?", ('alumno.demo@tec.mx',))
            if cur.fetchone() is None:
                cur.execute("INSERT INTO alumnos (nombre, correo, matricula, contraseña) VALUES (?, ?, ?, ?)",
                            ("Alumno Demo", "alumno.demo@tec.mx", "A00987654", "alumno123"))
                print("✅ Usuario 'alumno.demo@tec.mx' (alumno) creado.")

            conn.commit()
            print("\nBase de datos lista para la demostración.")

        except Exception as e:
            print(f"\n❌ Ocurrió un error: {e}")
            conn.rollback()
        finally:
            conn.close()

if __name__ == "__main__":
        preparar_base_para_demo()
    