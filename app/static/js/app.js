let regaloSeleccionado = null;

function abrirModalDesdeBoton(boton) {
    regaloSeleccionado = boton.dataset.id;
    const nombre = boton.dataset.nombre;

    const modalReserva = document.getElementById("modalReserva");
    const nombreSeleccionado = document.getElementById(
        "nombreRegaloSeleccionado"
    );
    const campoRegaloId = document.getElementById("regalo_id");

    campoRegaloId.value = regaloSeleccionado;
    nombreSeleccionado.textContent = nombre;
    modalReserva.style.display = "flex";

    document.body.style.overflow = "hidden";

    const primerCampo = document.querySelector(
        '#formReserva input[name="nombre"]'
    );

    if (primerCampo) {
        setTimeout(() => primerCampo.focus(), 100);
    }
}


function cerrarModal() {
    const modalReserva = document.getElementById("modalReserva");

    modalReserva.style.display = "none";
    document.body.style.overflow = "";
}


function mostrarGracias() {
    const modalGracias = document.getElementById("modalGracias");

    modalGracias.style.display = "flex";
    document.body.style.overflow = "hidden";
}


function cerrarGracias() {
    const modalGracias = document.getElementById("modalGracias");

    modalGracias.style.display = "none";
    document.body.style.overflow = "";

    location.reload();
}


function mostrarMensajeError(mensaje) {
    window.alert(mensaje);
}


document.addEventListener("DOMContentLoaded", () => {
    const formulario = document.getElementById("formReserva");
    const modalReserva = document.getElementById("modalReserva");
    const modalGracias = document.getElementById("modalGracias");

    if (!formulario) {
        return;
    }

    formulario.addEventListener("submit", async (evento) => {
        evento.preventDefault();

        const botonConfirmar = formulario.querySelector(
            'button[type="submit"]'
        );

        const textoOriginal = botonConfirmar.textContent;

        botonConfirmar.disabled = true;
        botonConfirmar.textContent = "Guardando...";

        try {
            const datos = new FormData(formulario);

            const respuesta = await fetch("/reservar", {
                method: "POST",
                body: datos,
            });

            if (!respuesta.ok) {
                throw new Error(
                    "No fue posible comunicarse correctamente con el servidor."
                );
            }

            const resultado = await respuesta.json();

            if (resultado.ok) {

    const mensaje = document.querySelector("#modalGracias .mensaje");

    mensaje.innerHTML = `
        Tu regalo quedó reservado correctamente para Thianna Amira.<br><br>

        <strong>Código de cancelación:</strong><br>

        <span style="font-size:24px;color:#be185d;">
            ${resultado.codigo_cancelacion}
        </span>

        <br><br>

        Guarda este código.
        Lo necesitarás si deseas cancelar tu reserva.
    `;

    cerrarModal();
    formulario.reset();
    regaloSeleccionado = null;
    mostrarGracias();
}

        } catch (error) {
            console.error("Error al guardar la reserva:", error);

            mostrarMensajeError(
                "Ocurrió un problema al guardar la reserva. " +
                "Por favor, inténtalo nuevamente."
            );

        } finally {
            botonConfirmar.disabled = false;
            botonConfirmar.textContent = textoOriginal;
        }
    });

    if (modalReserva) {
        modalReserva.addEventListener("click", (evento) => {
            if (evento.target === modalReserva) {
                cerrarModal();
            }
        });
    }

    if (modalGracias) {
        modalGracias.addEventListener("click", (evento) => {
            if (evento.target === modalGracias) {
                cerrarGracias();
            }
        });
    }

    document.addEventListener("keydown", (evento) => {
        if (evento.key !== "Escape") {
            return;
        }

        if (
            modalReserva &&
            modalReserva.style.display === "flex"
        ) {
            cerrarModal();
        }

        if (
            modalGracias &&
            modalGracias.style.display === "flex"
        ) {
            cerrarGracias();
        }
    });
});