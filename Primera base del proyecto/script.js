//  Función de login
function iniciarSesion() {
  const inputs = document.querySelectorAll('input');
  const usuario = inputs[0].value.trim();
  const contrasena = inputs[1].value.trim();

  if (!usuario || !contrasena) {
    alert("Por favor, completa ambos campos.");
    return;
  }

  localStorage.setItem('usuario', usuario);
  window.location.href = "resumen.html";
}

//  Función para generar resumen
function generarResumen() {
  const usuario = localStorage.getItem('usuario') || "Alumno";
  const fecha = new Date().toLocaleDateString();

  const resumen = `📄 Resumen generado para ${usuario} el ${fecha}.\n\nEste es un resumen ficticio del proyecto.`;

  const salida = document.getElementById('salida');
  if (salida) salida.innerText = resumen;

  // Guardar en historial
  let historial = JSON.parse(localStorage.getItem('historial')) || [];
  historial.push({ resumen, fecha });
  localStorage.setItem('historial', JSON.stringify(historial));
}

//  Función para mostrar historial
function cargarHistorial() {
  const historial = JSON.parse(localStorage.getItem('historial')) || [];
  const contenedor = document.getElementById('historial');

  if (contenedor && historial.length > 0) {
    historial.reverse().forEach(item => {
      const li = document.createElement('li');
      li.innerHTML = `<strong>${item.fecha}</strong><br>${item.resumen}`;
      contenedor.appendChild(li);
    });
  } else if (contenedor) {
    contenedor.innerHTML = "<p>No hay resúmenes generados todavía.</p>";
  }
}

//  Ejecución automática según la pantalla
window.addEventListener("DOMContentLoaded", () => {
  const path = window.location.pathname;

  if (path.includes("resumen.html")) {
    // Está en pantalla de resumen
    const boton = document.querySelector("button");
    if (boton) boton.onclick = generarResumen;
  }

  if (path.includes("historial.html")) {
    // Está en pantalla de historial
    cargarHistorial();
  }
});