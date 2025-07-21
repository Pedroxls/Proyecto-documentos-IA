// ========== CONFIG ==========
const API_BASE = "http://127.0.0.1:5000";

// ========== INICIO DE SESIÓN ==========
function iniciarSesion() {
  const correo = document.getElementById("correo").value;
  const password = document.getElementById("password").value;

  if (!correo || !password) {
    alert("Por favor completa ambos campos.");
    return;
  }

  fetch(`${API_BASE}/api/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ correo, contraseña: password })
  })
    .then(res => {
      if (!res.ok) throw new Error("Credenciales incorrectas");
      return res.json();
    })
    .then(data => {
      localStorage.setItem("usuario_id", data.id);
      localStorage.setItem("rol", data.rol);
      window.location.href = "dashboard.html"; // o resumen.html si prefieres
    })
    .catch(err => {
      alert("Error de autenticación: " + err.message);
    });
}

// ========== GENERAR RESUMEN ==========
function generarResumen() {
  const id = localStorage.getItem("usuario_id");
  if (!id) return window.location.href = "index.html";

  fetch(`${API_BASE}/api/resumen/${id}`)
    .then(res => res.json())
    .then(data => {
      const salida = document.getElementById("salida");
      if (salida) salida.innerText = data.resumen;
    })
    .catch(err => {
      console.error("Error al generar resumen:", err);
      alert("No se pudo generar el resumen");
    });
}

// ========== CARGAR HISTORIAL ==========
function cargarHistorial() {
  const id = localStorage.getItem("usuario_id");
  if (!id) return window.location.href = "index.html";

  const contenedor = document.getElementById("historial");
  fetch(`${API_BASE}/api/historial/${id}`)
    .then(res => res.json())
    .then(historial => {
      if (contenedor && historial.length > 0) {
        historial.reverse().forEach(item => {
          const li = document.createElement('li');
          li.innerHTML = `<strong>Semana ${item.semana} - ${item.fecha_envio}</strong><br>${item.actividades_realizadas}`;
          contenedor.appendChild(li);
        });
      } else if (contenedor) {
        contenedor.innerHTML = "<p>No hay resúmenes registrados todavía.</p>";
      }
    })
    .catch(err => {
      console.error("Error al cargar historial:", err);
    });
}

// ========== EJECUCIÓN AUTOMÁTICA SEGÚN PÁGINA ==========
window.addEventListener("DOMContentLoaded", () => {
  const path = window.location.pathname;

  if (path.includes("resumen.html")) {
    const boton = document.querySelector("button");
    if (boton) boton.onclick = generarResumen;
  }

  if (path.includes("historial.html")) {
    cargarHistorial();
  }

  if (path.includes("index.html")) {
    const boton = document.querySelector("button");
    if (boton) boton.onclick = iniciarSesion;
  }
});