import sqlite3

def insertar_admin():
    conn = sqlite3.connect("seguimiento_estancias.db")
    cur = conn.cursor()
    
    cur.execute("""
        INSERT INTO administradores (nombre, correo, contraseña)
        VALUES (?, ?, ?)
    """, ("Iván Admin", "admin@tec.mx", "1234"))
    
    conn.commit()
    conn.close()
    print("✅ Admin insertado con éxito.")

insertar_admin()