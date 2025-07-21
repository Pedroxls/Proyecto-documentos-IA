from db_utils import *

# 1. Insertar un alumno
insertar_alumno(
    nombre="Iván Pérez",
    correo="ivan.perez@ejemplo.com",
    matricula="A00837473",
    contraseña="1234"
)

# 2. Insertar un profesor
insertar_profesor(
    nombre="Dra. López",
    correo="lopez@tec.mx",
    departamento="IA",
    contraseña="abcd"
)

# 3. Insertar una estancia
insertar_estancia(
    alumno_id=1,
    profesor_id=1,
    empresa="Google México",
    nombre_proyecto="Desarrollo de IA aplicada a documentos",
    descripcion="El alumno participa en un proyecto de clasificación de archivos usando IA.",
    fecha_inicio="2025-07-10",
    fecha_fin="2025-08-30"
)

# 4. Registrar un reporte semanal
guardar_reporte(
    estancia_id=1,
    semana=1,
    actividades_planeadas="Revisión de archivos y preparación de datos.",
    actividades_realizadas="Clasificó 20 documentos y preparó el entorno de entrenamiento IA.",
    fecha_envio="2025-07-15",
    pdf_generado="reporte_semana_1.pdf"
)

# 5. Consultar historial por alumno
historial = consultar_historial_alumno(1)
print("Historial del alumno ID 1:")
for reporte in historial:
    print(f"Semana {reporte[0]} - {reporte[1]} - {reporte[2]}")