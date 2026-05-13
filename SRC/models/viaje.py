from DB.db import mysql


class Viaje:
    def __init__(self,id=None,tren_id=None,origen=None,destino=None,fecha_salida=None,fecha_llegada=None,estado_viaje=None,
        created_at=None,updated_at=None,tren_nombre=None,tren_codigo=None
    ):
        self.id = id
        self.tren_id = tren_id
        self.origen = origen
        self.destino = destino
        self.fecha_salida = fecha_salida
        self.fecha_llegada = fecha_llegada
        self.estado_viaje = estado_viaje
        self.created_at = created_at
        self.updated_at = updated_at
        self.tren_nombre = tren_nombre
        self.tren_codigo = tren_codigo

    @classmethod
    def get_all(cls):
        cursor = mysql.connection.cursor()

        cursor.execute("""
            SELECT 
                v.id,
                v.tren_id,
                v.origen,
                v.destino,
                v.fecha_salida,
                v.fecha_llegada,
                v.estado_viaje,
                v.created_at,
                v.updated_at,
                t.nombre,
                t.codigo
            FROM viajes v
            JOIN trenes t ON v.tren_id = t.id
            ORDER BY v.fecha_salida DESC
        """)

        rows = cursor.fetchall()
        cursor.close()

        viajes = []

        for row in rows:
            viajes.append(cls(
                id=row[0],
                tren_id=row[1],
                origen=row[2],
                destino=row[3],
                fecha_salida=row[4],
                fecha_llegada=row[5],
                estado_viaje=row[6],
                created_at=row[7],
                updated_at=row[8],
                tren_nombre=row[9],
                tren_codigo=row[10]
            ))

        return viajes

    @classmethod
    def get_by_id(cls, viaje_id):
        cursor = mysql.connection.cursor()

        cursor.execute("""
            SELECT 
                v.id,
                v.tren_id,
                v.origen,
                v.destino,
                v.fecha_salida,
                v.fecha_llegada,
                v.estado_viaje,
                v.created_at,
                v.updated_at,
                t.nombre,
                t.codigo
            FROM viajes v
            JOIN trenes t ON v.tren_id = t.id
            WHERE v.id = %s
        """, (viaje_id,))

        row = cursor.fetchone()
        cursor.close()

        if row:
            return cls(
                id=row[0],
                tren_id=row[1],
                origen=row[2],
                destino=row[3],
                fecha_salida=row[4],
                fecha_llegada=row[5],
                estado_viaje=row[6],
                created_at=row[7],
                updated_at=row[8],
                tren_nombre=row[9],
                tren_codigo=row[10]
            )

        return None

    @classmethod
    def create(cls, tren_id, origen, destino, fecha_salida, fecha_llegada, estado_viaje):
        cursor = mysql.connection.cursor()

        cursor.execute("""
            INSERT INTO viajes 
            (tren_id, origen, destino, fecha_salida, fecha_llegada, estado_viaje)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (tren_id, origen, destino, fecha_salida, fecha_llegada, estado_viaje))

        mysql.connection.commit()
        cursor.close()

    @classmethod
    def update(cls, viaje_id, tren_id, origen, destino, fecha_salida, fecha_llegada, estado_viaje):
        cursor = mysql.connection.cursor()

        cursor.execute("""
            UPDATE viajes
            SET tren_id = %s,
                origen = %s,
                destino = %s,
                fecha_salida = %s,
                fecha_llegada = %s,
                estado_viaje = %s
            WHERE id = %s
        """, (tren_id, origen, destino, fecha_salida, fecha_llegada, estado_viaje, viaje_id))

        mysql.connection.commit()
        cursor.close()

    @classmethod
    def update_estado(cls, viaje_id, estado_viaje):
        cursor = mysql.connection.cursor()

        cursor.execute("""
            UPDATE viajes
            SET estado_viaje = %s
            WHERE id = %s
        """, (estado_viaje, viaje_id))

        mysql.connection.commit()
        cursor.close()