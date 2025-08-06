// login.js (Versión actualizada con redirección por rol)

function iniciarSesion() {
  const correo = document.getElementById("correo").value;
  const password = document.getElementById("password").value;

  if (!correo || !password) {
    alert("Por favor completa ambos campos.");
    return;
  }

  fetch("http://127.0.0.1:5000/api/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ correo, contraseña: password })
  })
  .then(res => {
    if (!res.ok) {
      throw new Error("Credenciales incorrectas");
    }
    return res.json();
  })
  .then(data => {
    // Guardamos los datos de sesión
    localStorage.setItem("usuario_id", data.id);
    localStorage.setItem("rol", data.rol);

    // === LÓGICA DE REDIRECCIÓN POR ROL ===
    // Aquí está la magia. Revisamos el rol y decidimos a dónde enviar al usuario.

    if (data.rol === 'alumno') {
      // Si es un alumno, lo mandamos a su panel personal
      window.location.href = "panel_alumno.html";
    } else if (data.rol === 'profesor' || data.rol === 'admin') {
      // Si es profesor o admin, lo mandamos al dashboard principal
      window.location.href = "dashboard.html";
    } else {
      // Si por alguna razón el rol no es reconocido, mostramos un error.
      alert("Rol de usuario no reconocido.");
    }
  })
  .catch(err => {
    alert("Error de autenticación: " + err.message);
  });
}