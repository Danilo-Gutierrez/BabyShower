let regaloSeleccionado = null;

function abrirModalDesdeBoton(boton) {
    regaloSeleccionado = boton.dataset.id;
    let nombre = boton.dataset.nombre;

    document.getElementById("modalReserva").style.display = "flex";
    document.getElementById("nombreRegaloSeleccionado").innerText = nombre;
    document.getElementById("regalo_id").value = regaloSeleccionado;
}

function cerrarModal() {
    document.getElementById("modalReserva").style.display = "none";
}

function mostrarGracias() {
    document.getElementById("modalGracias").style.display = "flex";
}

function cerrarGracias() {
    document.getElementById("modalGracias").style.display = "none";
    location.reload();
}

document.addEventListener("DOMContentLoaded", function () {

    const formulario = document.getElementById("formReserva");

    formulario.addEventListener("submit", async function (e) {

        e.preventDefault();

        const datos = new FormData(formulario);

        const respuesta = await fetch("/reservar", {
            method: "POST",
            body: datos
        });

        const resultado = await respuesta.json();

        if (resultado.ok) {
            cerrarModal();
            formulario.reset();
            mostrarGracias();
        } else {
            alert(resultado.mensaje);
        }

    });

});