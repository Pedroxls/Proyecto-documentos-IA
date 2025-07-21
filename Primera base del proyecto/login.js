// login.js
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
    // Guardamos el rol y ID en localStorage
    localStorage.setItem("usuario_id", data.id);
    localStorage.setItem("rol", data.rol); // "profesor" o "admin"
    window.location.href = "dashboard.html";
  })
  .catch(err => {
    alert("Error de autenticación: " + err.message);
  });
}