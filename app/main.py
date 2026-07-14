from fastapi import FastAPI, Form, Request
import secrets
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.database import (
    crear_base_datos,
    crear_tabla_regalos,
    eliminar_reserva,
    guardar_regalo,
    guardar_reserva,
    insertar_regalos_iniciales,
    obtener_ids_reservados,
    obtener_regalos,
    obtener_reserva_por_codigo,
    obtener_reservas,
    regalo_esta_reservado,
)

app = FastAPI()

app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static",
)

templates = Jinja2Templates(directory="app/templates")


# Crear las tablas e insertar los regalos iniciales al iniciar la aplicación.
crear_base_datos()
crear_tabla_regalos()
insertar_regalos_iniciales()


@app.get("/")
def inicio(request: Request):
    regalos = obtener_regalos()
    ids_reservados = obtener_ids_reservados()

    regalos_disponibles = []

    for regalo in regalos:
        if regalo["id"] not in ids_reservados:
            regalos_disponibles.append(regalo)

    total_regalos = len(regalos)
    total_reservados = len(ids_reservados)
    total_disponibles = len(regalos_disponibles)

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "titulo": "Baby Shower",
            "bebe": "Thianna Amira Gutiérrez Ibáñez",
            "regalos": regalos_disponibles,
            "total_regalos": total_regalos,
            "total_reservados": total_reservados,
            "total_disponibles": total_disponibles,
        },
    )


@app.post("/reservar")
def reservar(
    regalo_id: int = Form(...),
    nombre: str = Form(...),
    apellido: str = Form(...),
    telefono: str = Form(...),
):
    if regalo_esta_reservado(regalo_id):
        return {
            "ok": False,
            "mensaje": "Lo sentimos, este regalo ya fue reservado.",
        }

    codigo_cancelacion = secrets.token_hex(3).upper()

    guardar_reserva(
        regalo_id=regalo_id,
        nombre=nombre.strip(),
        apellido=apellido.strip(),
        telefono=telefono.strip(),
        codigo_cancelacion=codigo_cancelacion,
    )

    return {
        "ok": True,
        "mensaje": "Reserva guardada correctamente 💖",
        "codigo_cancelacion": codigo_cancelacion,
    }


@app.post("/admin/regalos")
def crear_regalo(
    emoji: str = Form("🎁"),
    nombre: str = Form(...),
    descripcion: str = Form(""),
    categoria: str = Form(""),
    precio: int = Form(0),
    imagen: str = Form(""),
    enlace: str = Form(""),
):
    nombre_limpio = nombre.strip()

    if not nombre_limpio:
        return RedirectResponse(
            url="/admin?error=nombre",
            status_code=303,
        )

    guardar_regalo(
        emoji=emoji.strip() or "🎁",
        nombre=nombre_limpio,
        descripcion=descripcion.strip(),
        imagen=imagen.strip(),
        categoria=categoria.strip(),
        precio=max(precio, 0),
        enlace=enlace.strip(),
    )

    return RedirectResponse(
        url="/admin?guardado=1",
        status_code=303,
    )


@app.get("/admin/reservas")
def ver_reservas():
    reservas = obtener_reservas()

    return {
        "reservas": reservas,
    }

@app.post("/admin/reservas/{id_reserva}/liberar")
def liberar_reserva(id_reserva: int):
    eliminar_reserva(id_reserva)

    return RedirectResponse(
        url="/admin?liberada=1",
        status_code=303,
    )

@app.get("/cancelar")
def mostrar_cancelacion(
    request: Request,
    cancelada: int = 0,
    error: str = "",
):
    return templates.TemplateResponse(
        request=request,
        name="cancelar.html",
        context={
            "cancelada": cancelada,
            "error": error,
        },
    )


@app.post("/cancelar")
def cancelar_reserva(codigo: str = Form(...)):
    codigo_limpio = codigo.strip().upper()

    reserva = obtener_reserva_por_codigo(codigo_limpio)

    if reserva is None:
        return RedirectResponse(
            url="/cancelar?error=codigo",
            status_code=303,
        )

    eliminar_reserva(reserva["id"])

    return RedirectResponse(
        url="/cancelar?cancelada=1",
        status_code=303,
    )

@app.get("/admin")
def admin(
    request: Request,
    guardado: int = 0,
    liberada: int = 0,
    error: str = "",
):
    reservas = obtener_reservas()
    regalos = obtener_regalos()

    reservas_detalle = []

    for reserva in reservas:
        id_reserva = reserva[0]
        regalo_id = reserva[1]
        nombre = reserva[2]
        apellido = reserva[3]
        telefono = reserva[4]

        nombre_regalo = "Regalo no encontrado"

        for regalo in regalos:
            if regalo["id"] == regalo_id:
                nombre_regalo = regalo["nombre"]
                break

        reservas_detalle.append(
            {
                "id": id_reserva,
                "regalo_id": regalo_id,
                "regalo": nombre_regalo,
                "nombre": nombre,
                "apellido": apellido,
                "telefono": telefono,
            }
        )

    return templates.TemplateResponse(
        request=request,
        name="admin.html",
        context={
            "titulo": "Panel de Administración",
            "reservas": reservas_detalle,
            "guardado": guardado,
            "liberada": liberada,
            "error": error,
        },
    )