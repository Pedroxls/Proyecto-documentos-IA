function iniciarSesion() {
  const usuario = document.getElementById('usuario').value;
  if (usuario) {
    localStorage.setItem('usuario', usuario);
    window.location.href = "resumen.html";
  } else {
    alert("Ingresa tu nombre o matrícula.");
  }
}

function generarResumen() {
  const usuario = localStorage.getItem('usuario') || "Alumno";
  const resumen = `Este es un resumen ficticio generado para ${usuario}.`;

  document.getElementById('salida').innerText = resumen;

  // Guardamos en historial simulado
  let historial = JSON.parse(localStorage.getItem('historial')) || [];
  historial.push(resumen);
  localStorage.setItem('historial', JSON.stringify(historial));
}

// Para historial.html
window.onload = function () {
  if (document.getElementById('historial')) {
    const historial = JSON.parse(localStorage.getItem('historial')) || [];
    const ul = document.getElementById('historial');
    historial.forEach(item => {
      const li = document.createElement('li');
      li.textContent = item;
      ul.appendChild(li);
    });
  }
};