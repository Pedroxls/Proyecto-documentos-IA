# app.py (Versión Final del Proyecto)
import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS
from db_utils import insertar_alumno, consultar_historial_alumno

app = Flask(__name__)
CORS(app)

# --- (Rutas existentes: /ping, /api/alumno, /api/historial, /api/login, /api/definicion_proyecto) ---
# ... (El código de las rutas anteriores se mantiene igual) ...
# Ruta de prueba para verificar que Flask está corriendo
@app.route("/ping")
def ping():
    return jsonify({"message": "Flask está funcionando correctamente "})

# Ruta para insertar un alumno (POST)
@app.route("/api/alumno", methods=["POST"])
def api_insertar_alumno():
    data = request.get_json()
    nombre = data.get("nombre")
    correo = data.get("correo")
    matricula = data.get("matricula")
    contraseña = data.get("contraseña")

    if not all([nombre, correo, matricula, contraseña]):
        return jsonify({"error": "Faltan datos del alumno"}), 400

    insertar_alumno(nombre, correo, matricula, contraseña)
    return jsonify({"message": "Alumno insertado correctamente ✅"})

# Ruta para consultar historial de reportes por alumno_id
@app.route("/api/historial/<int:alumno_id>", methods=["GET"])
def api_historial_alumno(alumno_id):
    historial = consultar_historial_alumno(alumno_id)
    resultado = [
        {"semana": h[0], "fecha_envio": h[1], "actividades_realizadas": h[2]}
        for h in historial
    ]
    return jsonify(resultado)

# === RUTA DE LOGIN ACTUALIZADA (AHORA INCLUYE ALUMNOS) ===
@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    correo = data.get("correo")
    contraseña = data.get("contraseña")

    conn = sqlite3.connect("seguimiento_estancias.db")
    cur = conn.cursor()

    # 1. Buscar en profesores
    cur.execute("SELECT id, contraseña FROM profesores WHERE correo = ?", (correo,))
    usuario = cur.fetchone()
    if usuario and usuario[1] == contraseña:
        conn.close()
        return jsonify({"id": usuario[0], "rol": "profesor"})

    # 2. Buscar en administradores
    cur.execute("SELECT id, contraseña FROM administradores WHERE correo = ?", (correo,))
    usuario = cur.fetchone()
    if usuario and usuario[1] == contraseña:
        conn.close()
        return jsonify({"id": usuario[0], "rol": "admin"})

    # 3. Buscar en alumnos
    cur.execute("SELECT id, contraseña FROM alumnos WHERE correo = ?", (correo,))
    usuario = cur.fetchone()
    if usuario and usuario[1] == contraseña:
        conn.close()
        return jsonify({"id": usuario[0], "rol": "alumno"})

    conn.close()
    return jsonify({"error": "Credenciales inválidas"}), 401


# === ENDPOINT PARA RECIBIR EL FORMULARIO COMPLETO ===
@app.route("/api/definicion_proyecto", methods=["POST"])
def api_definicion_proyecto():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No se recibieron datos"}), 400

    conn = sqlite3.connect("seguimiento_estancias.db")
    cur = conn.cursor()

    try:
        # --- Paso 1: Insertar en la tabla principal 'estancias' ---
        cur.execute("""
            INSERT INTO estancias (
                alumno_id, profesor_id, nombre_alumno, nombre_proyecto, lider_proyecto, area_empresarial, fecha_elaboracion,
                justificacion_proposito, antecedentes_desc, descripcion_problema, situacion_problema_actual,
                expectativas_proyecto, productos_entregar, antecedentes_area, restriccion_costos, restriccion_materiales,
                restriccion_humanos, restriccion_tiempo, restriccion_calidad, restriccion_alcance, restriccion_riesgos,
                impacto_actividades
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data.get("alumno_id"), data.get("profesor_id"), data.get("nombre_alumno"), data.get("nombre_proyecto"),
            data.get("lider_proyecto"), data.get("area_empresarial"), data.get("fecha_elaboracion"),
            data.get("justificacion"), data.get("antecedentes_desc"), data.get("descripcion_problema"),
            data.get("situacion_problema"), data.get("expectativas_proyecto"), data.get("productos_entregar"),
            data.get("antecedentes_area"), data.get("restriccion_costos"), data.get("restriccion_materiales"),
            data.get("restriccion_humanos"), data.get("restriccion_tiempo"), data.get("restriccion_calidad"),
            data.get("restriccion_alcance"), data.get("restriccion_riesgos"), data.get("impacto_actividades")
        ))
        
        estancia_id = cur.lastrowid

        # --- Paso 2: Insertar en la tabla 'fases_proyecto' ---
        for i in range(1, 4):
            if data.get(f"fase{i}_nombre"):
                cur.execute("""
                    INSERT INTO fases_proyecto (estancia_id, nombre_fase, descripcion, duracion, entregable, criterio_exito, recomendacion_nps)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    estancia_id, data.get(f"fase{i}_nombre"), data.get(f"fase{i}_descripcion"), data.get(f"fase{i}_duracion"),
                    data.get(f"fase{i}_entregable"), data.get(f"fase{i}_criterio_exito"), data.get(f"fase{i}_recomendacion")
                ))

        # --- Paso 3: Insertar en la tabla 'tareas_proyecto' ---
        for i in range(1, 4):
            if data.get(f"tarea{i}_nombre"):
                cur.execute("""
                    INSERT INTO tareas_proyecto (estancia_id, fase_correspondiente, nombre_tarea, entregable_tarea, criterio_exito_tarea, fecha_inicio, fecha_fin, responsable_tarea)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    estancia_id, data.get(f"tarea{i}_fase"), data.get(f"tarea{i}_nombre"), data.get(f"tarea{i}_entregable"),
                    data.get(f"tarea{i}_criterio_exito"), data.get(f"tarea{i}_fecha_inicio"), data.get(f"tarea{i}_fecha_fin"), data.get(f"tarea{i}_responsable")
                ))
        
        conn.commit()
        return jsonify({"message": "Definición de proyecto guardada con éxito!", "estancia_id": estancia_id}), 201

    except Exception as e:
        conn.rollback()
        print(f"Error en la base de datos: {e}")
        return jsonify({"error": "Ocurrió un error al guardar los datos en el servidor"}), 500
    finally:
        conn.close()

# === ENDPOINT DEL DASHBOARD ACTUALIZADO Y MEJORADO ===
@app.route("/api/dashboard/data", methods=["GET"])
def get_dashboard_data():
    rol = request.args.get('rol')
    user_id = request.args.get('id')

    conn = sqlite3.connect("seguimiento_estancias.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    try:
        query = "SELECT e.id, e.alumno_id, e.nombre_alumno, e.nombre_proyecto FROM estancias e"
        params = ()
        
        if rol == 'profesor':
            query += " WHERE e.profesor_id = ?"
            params = (user_id,)

        cur.execute(query, params)
        estancias = [dict(row) for row in cur.fetchall()]
        
        total_estancias_activas = len(estancias)
        reportes_pendientes = 0 
        alertas = 0

        dashboard_data = {
            "estadisticas": {"activas": total_estancias_activas, "pendientes": reportes_pendientes, "alertas": alertas},
            "lista_estancias": estancias
        }
        
        conn.close()
        return jsonify(dashboard_data), 200

    except Exception as e:
        if conn: conn.close()
        return jsonify({"error": f"Error al obtener datos para el dashboard: {e}"}), 500

# === ENDPOINTS COMPLETOS PARA GESTIÓN DE PROFESORES (EXCLUSIVO ADMIN) ===
@app.route("/api/profesores", methods=["GET", "POST"])
def gestionar_profesores():
    conn = sqlite3.connect("seguimiento_estancias.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    if request.method == "GET":
        cur.execute("SELECT nombre, correo, departamento FROM profesores")
        profesores = [dict(row) for row in cur.fetchall()]
        conn.close()
        return jsonify(profesores)

    if request.method == "POST":
        data = request.get_json()
        try:
            cur.execute(
                "INSERT INTO profesores (nombre, correo, departamento, contraseña) VALUES (?, ?, ?, ?)",
                (data['nombre'], data['correo'], data['departamento'], data['contraseña'])
            )
            conn.commit()
            conn.close()
            return jsonify({"message": "Profesor añadido con éxito."}), 201
        except Exception as e:
            conn.close()
            return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
