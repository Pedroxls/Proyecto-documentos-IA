# app.py
import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS  # <- AÑADE ESTO
from db_utils import insertar_alumno, consultar_historial_alumno

app = Flask(__name__)
CORS(app)  # <- AÑADE ESTO


# Ruta de prueba para verificar que Flask está corriendo
@app.route("/ping")
def ping():
    return jsonify({"message": "Flask está funcionando correctamente 🔥"})

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

@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    correo = data.get("correo")
    contraseña = data.get("contraseña")

    conn = sqlite3.connect("seguimiento_estancias.db")
    cur = conn.cursor()

    # Buscar en profesores
    cur.execute("SELECT id, contraseña FROM profesores WHERE correo = ?", (correo,))
    profesor = cur.fetchone()

    if profesor and profesor[1] == contraseña:
        return jsonify({"id": profesor[0], "rol": "profesor"})

    # Buscar en administradores
    cur.execute("SELECT id, contraseña FROM administradores WHERE correo = ?", (correo,))
    admin = cur.fetchone()

    if admin and admin[1] == contraseña:
        return jsonify({"id": admin[0], "rol": "admin"})

    return jsonify({"error": "Credenciales inválidas"}), 401

if __name__ == "__main__":
    app.run(debug=True)
