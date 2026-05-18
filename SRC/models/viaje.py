from DB.db import mysql


class Viaje:
    def __init__(self,id=None,tren_id=None,origen_id=None,destino_id=None,origen=None,destino=None,fecha_salida=None,
        fecha_llegada=None,estado_viaje=None,created_at=None,updated_at=None,tren_nombre=None,tren_codigo=None):

        self.id = id
        self.tren_id = tren_id
        self.origen_id = origen_id
        self.destino_id = destino_id
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
                v.origen_id,
                v.destino_id,
                eo.nombre AS origen_nombre,
                ed.nombre AS destino_nombre,
                v.fecha_salida,
                v.fecha_llegada,
                v.estado_viaje,
                v.created_at,
                v.updated_at,
                t.nombre,
                t.codigo
            FROM viajes v
            JOIN trenes t ON v.tren_id = t.id
            LEFT JOIN estaciones eo ON v.origen_id = eo.id
            LEFT JOIN estaciones ed ON v.destino_id = ed.id
            ORDER BY v.fecha_salida DESC
        """)

        rows = cursor.fetchall()
        cursor.close()

        viajes = []

        for row in rows:
            viajes.append(cls(
                id=row[0],
                tren_id=row[1],
                origen_id=row[2],
                destino_id=row[3],
                origen=row[4],
                destino=row[5],
                fecha_salida=row[6],
                fecha_llegada=row[7],
                estado_viaje=row[8],
                created_at=row[9],
                updated_at=row[10],
                tren_nombre=row[11],
                tren_codigo=row[12]
            ))

        return viajes

    @classmethod
    def get_by_id(cls, viaje_id):
        cursor = mysql.connection.cursor()

        cursor.execute("""
            SELECT 
                v.id,
                v.tren_id,
                v.origen_id,
                v.destino_id,
                eo.nombre AS origen_nombre,
                ed.nombre AS destino_nombre,
                v.fecha_salida,
                v.fecha_llegada,
                v.estado_viaje,
                v.created_at,
                v.updated_at,
                t.nombre,
                t.codigo
            FROM viajes v
            JOIN trenes t ON v.tren_id = t.id
            LEFT JOIN estaciones eo ON v.origen_id = eo.id
            LEFT JOIN estaciones ed ON v.destino_id = ed.id
            WHERE v.id = %s
        """, (viaje_id,))

        row = cursor.fetchone()
        cursor.close()

        if row:
            return cls(
                id=row[0],
                tren_id=row[1],
                origen_id=row[2],
                destino_id=row[3],
                origen=row[4],
                destino=row[5],
                fecha_salida=row[6],
                fecha_llegada=row[7],
                estado_viaje=row[8],
                created_at=row[9],
                updated_at=row[10],
                tren_nombre=row[11],
                tren_codigo=row[12]
            )

        return None

    @classmethod
    def create(cls, tren_id, origen_id, destino_id, fecha_salida, fecha_llegada, estado_viaje):
        cursor = mysql.connection.cursor()

        cursor.execute("""
            INSERT INTO viajes 
            (tren_id, origen_id, destino_id, fecha_salida, fecha_llegada, estado_viaje)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (tren_id, origen_id, destino_id, fecha_salida, fecha_llegada, estado_viaje))

        mysql.connection.commit()
        cursor.close()

    @classmethod
    def update(cls, viaje_id, tren_id, origen_id, destino_id, fecha_salida, fecha_llegada, estado_viaje):
        cursor = mysql.connection.cursor()

        cursor.execute("""
            UPDATE viajes
            SET tren_id = %s,
                origen_id = %s,
                destino_id = %s,
                fecha_salida = %s,
                fecha_llegada = %s,
                estado_viaje = %s
            WHERE id = %s
        """, (tren_id, origen_id, destino_id, fecha_salida, fecha_llegada, estado_viaje, viaje_id))

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



        if estado_viaje == 'finalizado':
            Viaje.finalizar_viaje(viaje_id)

        else:
            Viaje.update_estado(viaje_id, estado_viaje)

        mysql.connection.commit()
        cursor.close()

    @classmethod
    def get_disponibles(cls):
        cursor = mysql.connection.cursor()

        cursor.execute("""
            SELECT 
                v.id,
                v.tren_id,
                v.origen_id,
                v.destino_id,
                eo.nombre AS origen_nombre,
                ed.nombre AS destino_nombre,
                v.fecha_salida,
                v.fecha_llegada,
                v.estado_viaje,
                v.created_at,
                v.updated_at,
                t.nombre,
                t.codigo
            FROM viajes v
            JOIN trenes t ON v.tren_id = t.id
            LEFT JOIN estaciones eo ON v.origen_id = eo.id
            LEFT JOIN estaciones ed ON v.destino_id = ed.id
            WHERE v.estado_viaje = 'programado'
            ORDER BY v.fecha_salida ASC
        """)

        rows = cursor.fetchall()
        cursor.close()

        viajes = []

        for row in rows:
            viaje = cls(
                id=row[0],
                tren_id=row[1],
                origen_id=row[2],
                destino_id=row[3],
                origen=row[4],
                destino=row[5],
                fecha_salida=row[6],
                fecha_llegada=row[7],
                estado_viaje=row[8],
                created_at=row[9],
                updated_at=row[10],
                tren_nombre=row[11],
                tren_codigo=row[12]
            )

            viaje.capacidad_total = cls.get_capacidad_total(viaje.id)
            viaje.espacio_reservado = cls.get_espacio_reservado(viaje.id)
            viaje.espacio_disponible = cls.get_espacio_disponible(viaje.id)

            viajes.append(viaje)

        return viajes

    @classmethod
    def get_capacidad_total(cls, viaje_id):
        cursor = mysql.connection.cursor()

        cursor.execute("""
            SELECT COALESCE(SUM(vg.capacidad_m2), 0)
            FROM viajes vi
            JOIN vagones vg ON vi.tren_id = vg.tren_id
            WHERE vi.id = %s
            AND vg.estado_vagon = 'activo'
        """, (viaje_id,))

        capacidad = cursor.fetchone()[0]
        cursor.close()

        return capacidad

    @classmethod
    def get_espacio_reservado(cls, viaje_id):
        cursor = mysql.connection.cursor()

        cursor.execute("""
            SELECT COALESCE(SUM(espacios_solicitados), 0)
            FROM pedidos
            WHERE viaje_id = %s
            AND estado_pedido IN ('pendiente', 'aceptado', 'en_transito')
        """, (viaje_id,))

        reservado = cursor.fetchone()[0]
        cursor.close()

        return reservado

    @classmethod
    def get_espacio_disponible(cls, viaje_id):
        capacidad_total = cls.get_capacidad_total(viaje_id)
        espacio_reservado = cls.get_espacio_reservado(viaje_id)

        disponible = capacidad_total - espacio_reservado

        if disponible < 0:
            return 0

        return disponible

    @classmethod
    def count_programados(cls):
        cursor = mysql.connection.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM viajes
            WHERE estado_viaje = 'programado'
        """)

        total = cursor.fetchone()[0]
        cursor.close()

        return total


    @classmethod
    def actualizar_estados_automaticos(cls):
        cursor = mysql.connection.cursor()

        # Pasar a en_transito los viajes cuya salida ya ha llegado
        # pero cuya llegada todavía no ha pasado
        cursor.execute("""
            UPDATE viajes
            SET estado_viaje = 'en_transito'
            WHERE estado_viaje = 'programado'
            AND fecha_salida <= NOW()
            AND fecha_llegada IS NOT NULL
            AND fecha_llegada > NOW()
        """)

        # Obtener viajes que deben finalizar
        cursor.execute("""
            SELECT id, tren_id, destino_id
            FROM viajes
            WHERE estado_viaje IN ('programado', 'en_transito')
            AND fecha_llegada IS NOT NULL
            AND fecha_llegada <= NOW()
        """)

        viajes_finalizados = cursor.fetchall()

        # Finalizar viajes
        cursor.execute("""
            UPDATE viajes
            SET estado_viaje = 'finalizado'
            WHERE estado_viaje IN ('programado', 'en_transito')
            AND fecha_llegada IS NOT NULL
            AND fecha_llegada <= NOW()
        """)

        # Mover el tren a la estación destino
        for viaje in viajes_finalizados:
            tren_id = viaje[1]
            destino_id = viaje[2]

            cursor.execute("""
                UPDATE trenes
                SET estacion_actual_id = %s
                WHERE id = %s
            """, (destino_id, tren_id))

        mysql.connection.commit()
        cursor.close()

    @classmethod
    def finalizar_viaje(cls, viaje_id):
        cursor = mysql.connection.cursor()

        cursor.execute("""
            SELECT tren_id, destino_id
            FROM viajes
            WHERE id = %s
        """, (viaje_id,))

        viaje = cursor.fetchone()

        if viaje:
            tren_id = viaje[0]
            destino_id = viaje[1]

            cursor.execute("""
                UPDATE viajes
                SET estado_viaje = 'finalizado'
                WHERE id = %s
            """, (viaje_id,))

            cursor.execute("""
                UPDATE trenes
                SET estacion_actual_id = %s
                WHERE id = %s
            """, (destino_id, tren_id))

        mysql.connection.commit()
        cursor.close()