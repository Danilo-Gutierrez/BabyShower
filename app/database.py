import sqlite3
from typing import Any

DB_NAME = "babyshower.db"


def conectar() -> sqlite3.Connection:
    conexion = sqlite3.connect(DB_NAME)
    conexion.row_factory = sqlite3.Row
    return conexion


def crear_base_datos() -> None:
    with conectar() as conexion:
        conexion.execute("""
            CREATE TABLE IF NOT EXISTS reservas(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                regalo_id INTEGER NOT NULL,
                nombre TEXT NOT NULL,
                apellido TEXT NOT NULL,
                telefono TEXT NOT NULL,
                FOREIGN KEY(regalo_id) REFERENCES regalos(id)
            )
        """)

        columnas_reservas = {
            fila["name"]
            for fila in conexion.execute(
                "PRAGMA table_info(reservas)"
            ).fetchall()
        }

        if "codigo_cancelacion" not in columnas_reservas:
            conexion.execute(
                "ALTER TABLE reservas "
                "ADD COLUMN codigo_cancelacion TEXT DEFAULT ''"
            )

def crear_tabla_regalos() -> None:
    with conectar() as conexion:
        conexion.execute("""
            CREATE TABLE IF NOT EXISTS regalos(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                emoji TEXT DEFAULT '🎁',
                nombre TEXT NOT NULL,
                descripcion TEXT DEFAULT '',
                imagen TEXT DEFAULT '',
                categoria TEXT DEFAULT '',
                precio INTEGER DEFAULT 0,
                enlace TEXT DEFAULT ''
            )
        """)

        columnas = {
            fila["name"]
            for fila in conexion.execute(
                "PRAGMA table_info(regalos)"
            ).fetchall()
        }

        columnas_nuevas = {
            "imagen": "TEXT DEFAULT ''",
            "categoria": "TEXT DEFAULT ''",
            "precio": "INTEGER DEFAULT 0",
            "enlace": "TEXT DEFAULT ''",
        }

        for nombre_columna, definicion in columnas_nuevas.items():
            if nombre_columna not in columnas:
                conexion.execute(
                    f"ALTER TABLE regalos "
                    f"ADD COLUMN {nombre_columna} {definicion}"
                )


def insertar_regalos_iniciales() -> None:
    with conectar() as conexion:
        cantidad = conexion.execute(
            "SELECT COUNT(*) AS cantidad FROM regalos"
        ).fetchone()["cantidad"]

        if cantidad > 0:
            return

        regalos_iniciales = [
            (
                "🍼",
                "Pañales recién nacido",
                "Pack talla RN o P",
                "panales.jpg",
                "Higiene",
                18990,
                "",
            ),
            (
                "🛁",
                "Bañera para bebé",
                "Color neutro o rosado suave",
                "banera.jpg",
                "Baño",
                29990,
                "",
            ),
            (
                "🧸",
                "Manta o cobertor",
                "Suave, abrigado y delicado",
                "manta.jpg",
                "Dormitorio",
                19990,
                "",
            ),
            (
                "🧦",
                "Calcetines de bebé",
                "Pack de calcetines suaves",
                "calcetines.jpg",
                "Ropa",
                9990,
                "",
            ),
            (
                "🧴",
                "Set de aseo",
                "Shampoo, colonia y crema",
                "set-aseo.jpg",
                "Higiene",
                24990,
                "",
            ),
        ]

        conexion.executemany("""
            INSERT INTO regalos(
                emoji,
                nombre,
                descripcion,
                imagen,
                categoria,
                precio,
                enlace
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, regalos_iniciales)


def guardar_regalo(
    emoji: str,
    nombre: str,
    descripcion: str,
    imagen: str,
    categoria: str,
    precio: int,
    enlace: str,
) -> int:
    with conectar() as conexion:
        cursor = conexion.execute("""
            INSERT INTO regalos(
                emoji,
                nombre,
                descripcion,
                imagen,
                categoria,
                precio,
                enlace
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            emoji,
            nombre,
            descripcion,
            imagen,
            categoria,
            precio,
            enlace,
        ))

        return int(cursor.lastrowid)


def obtener_regalos() -> list[dict[str, Any]]:
    with conectar() as conexion:
        filas = conexion.execute("""
            SELECT
                id,
                emoji,
                nombre,
                descripcion,
                imagen,
                categoria,
                precio,
                enlace
            FROM regalos
            ORDER BY id
        """).fetchall()

    return [dict(fila) for fila in filas]


def guardar_reserva(
    regalo_id: int,
    nombre: str,
    apellido: str,
    telefono: str,
    codigo_cancelacion: str,
) -> int:
    with conectar() as conexion:
        cursor = conexion.execute("""
            INSERT INTO reservas(
                regalo_id,
                nombre,
                apellido,
                telefono,
                codigo_cancelacion
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            regalo_id,
            nombre,
            apellido,
            telefono,
            codigo_cancelacion,
        ))

        return int(cursor.lastrowid)


def obtener_ids_reservados() -> list[int]:
    with conectar() as conexion:
        filas = conexion.execute("""
            SELECT regalo_id
            FROM reservas
        """).fetchall()

    return [int(fila["regalo_id"]) for fila in filas]


def obtener_reservas() -> list[tuple]:
    with conectar() as conexion:
        filas = conexion.execute("""
            SELECT
                id,
                regalo_id,
                nombre,
                apellido,
                telefono
            FROM reservas
            ORDER BY id DESC
        """).fetchall()

    return [
        (
            fila["id"],
            fila["regalo_id"],
            fila["nombre"],
            fila["apellido"],
            fila["telefono"],
        )
        for fila in filas
    ]


def regalo_esta_reservado(regalo_id: int) -> bool:
    with conectar() as conexion:
        reserva = conexion.execute("""
            SELECT id
            FROM reservas
            WHERE regalo_id = ?
            LIMIT 1
        """, (regalo_id,)).fetchone()

    return reserva is not None

def eliminar_reserva(id_reserva):
    conexion = conectar()

    cursor = conexion.cursor()

    cursor.execute("""
        DELETE FROM reservas
        WHERE id = ?
    """, (id_reserva,))

    conexion.commit()
    conexion.close()

def obtener_reserva_por_codigo(codigo_cancelacion: str):
    with conectar() as conexion:
        reserva = conexion.execute("""
            SELECT
                id,
                regalo_id,
                nombre,
                apellido,
                telefono,
                codigo_cancelacion
            FROM reservas
            WHERE codigo_cancelacion = ?
            LIMIT 1
        """, (codigo_cancelacion,)).fetchone()

    if reserva is None:
        return None

    return dict(reserva)