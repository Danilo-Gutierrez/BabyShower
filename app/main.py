from app.database import crear_base_datos, guardar_reserva, obtener_ids_reservados, obtener_reservas, regalo_esta_reservado, crear_tabla_regalos, insertar_regalos_iniciales, obtener_regalos

from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

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
            "total_disponibles": total_disponibles
        }
    )


@app.post("/reservar")
def reservar(
    regalo_id: int = Form(...),
    nombre: str = Form(...),
    apellido: str = Form(...),
    telefono: str = Form(...)
):
    if regalo_esta_reservado(regalo_id):
        return {
            "ok": False,
            "mensaje": "Lo sentimos, este regalo ya fue reservado."
        }

    guardar_reserva(regalo_id, nombre, apellido, telefono)

    print("========== NUEVA RESERVA GUARDADA ==========")
    print("Regalo ID:", regalo_id)
    print("Nombre:", nombre)
    print("Apellido:", apellido)
    print("Teléfono:", telefono)

    return {
        "ok": True,
        "mensaje": "Reserva guardada correctamente 💖"
    }

@app.get("/admin/reservas")
def ver_reservas():
    import sqlite3

    conexion = sqlite3.connect("babyshower.db")
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM reservas")
    reservas = cursor.fetchall()

    conexion.close()

    return {
        "reservas": reservas
    }

@app.get("/admin")
def admin(request: Request):
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

        reservas_detalle.append({
            "id": id_reserva,
            "regalo_id": regalo_id,
            "regalo": nombre_regalo,
            "nombre": nombre,
            "apellido": apellido,
            "telefono": telefono
        })

    return templates.TemplateResponse(
        request=request,
        name="admin.html",
        context={
            "titulo": "Panel de Administración",
            "reservas": reservas_detalle
        }
    )