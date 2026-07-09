import sqlite3

DB_NAME = "babyshower.db"


def crear_base_datos():
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reservas(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        regalo_id INTEGER,
        nombre TEXT,
        apellido TEXT,
        telefono TEXT
    )
    """)

    conexion.commit()
    conexion.close()


def guardar_reserva(regalo_id, nombre, apellido, telefono):
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()

    cursor.execute("""
    INSERT INTO reservas(regalo_id, nombre, apellido, telefono)
    VALUES (?, ?, ?, ?)
    """, (regalo_id, nombre, apellido, telefono))

    conexion.commit()
    conexion.close()

def obtener_ids_reservados():
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()

    cursor.execute("SELECT regalo_id FROM reservas")
    filas = cursor.fetchall()

    conexion.close()

    return [fila[0] for fila in filas]

def obtener_reservas():
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()

    cursor.execute("""
    SELECT id, regalo_id, nombre, apellido, telefono
    FROM reservas
    ORDER BY id DESC
    """)

    filas = cursor.fetchall()

    conexion.close()

    return filas

def regalo_esta_reservado(regalo_id):
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()

    cursor.execute("""
    SELECT id FROM reservas
    WHERE regalo_id = ?
    """, (regalo_id,))

    reserva = cursor.fetchone()

    conexion.close()

    return reserva is not None

def regalo_esta_reservado(regalo_id):
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()

    cursor.execute("""
    SELECT id FROM reservas
    WHERE regalo_id = ?
    """, (regalo_id,))

    reserva = cursor.fetchone()

    conexion.close()

    return reserva is not None

def crear_tabla_regalos():
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS regalos(
        id INTEGER PRIMARY KEY,
        emoji TEXT,
        nombre TEXT,
        descripcion TEXT
    )
    """)

    conexion.commit()
    conexion.close()


def insertar_regalos_iniciales():
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()

    cursor.execute("SELECT COUNT(*) FROM regalos")
    cantidad = cursor.fetchone()[0]

    if cantidad == 0:
        regalos_iniciales = [
            (1, "🍼", "Pañales recién nacido", "Pack talla RN o P"),
            (2, "🛁", "Bañera para bebé", "Color neutro o rosado suave"),
            (3, "🧸", "Manta o cobertor", "Suave, abrigado y delicado"),
            (4, "🧦", "Calcetines de bebé", "Pack de calcetines suaves"),
            (5, "🧴", "Set de aseo", "Shampoo, colonia y crema")
        ]

        cursor.executemany("""
        INSERT INTO regalos(id, emoji, nombre, descripcion)
        VALUES (?, ?, ?, ?)
        """, regalos_iniciales)

    conexion.commit()
    conexion.close()


def obtener_regalos():
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()

    cursor.execute("""
    SELECT id, emoji, nombre, descripcion
    FROM regalos
    ORDER BY id
    """)

    filas = cursor.fetchall()
    conexion.close()

    regalos = []

    for fila in filas:
        regalos.append({
            "id": fila[0],
            "emoji": fila[1],
            "nombre": fila[2],
            "descripcion": fila[3]
        })

    return regalos