from DB.db import mysql


class Estacion:
    def __init__(self,id=None,nombre=None,ciudad=None,codigo=None,estado_estacion=None,created_at=None,updated_at=None):
        self.id = id
        self.nombre = nombre
        self.ciudad = ciudad
        self.codigo = codigo
        self.estado_estacion = estado_estacion
        self.created_at = created_at
        self.updated_at = updated_at

    @classmethod
    def get_all(cls):
        cursor = mysql.connection.cursor()

        cursor.execute("""
            SELECT id, nombre, ciudad, codigo, estado_estacion, created_at, updated_at
            FROM estaciones
            ORDER BY id DESC
        """)

        rows = cursor.fetchall()
        cursor.close()

        estaciones = []

        for row in rows:
            estaciones.append(cls(
                id=row[0],
                nombre=row[1],
                ciudad=row[2],
                codigo=row[3],
                estado_estacion=row[4],
                created_at=row[5],
                updated_at=row[6]
            ))

        return estaciones

    @classmethod
    def get_activas(cls):
        cursor = mysql.connection.cursor()

        cursor.execute("""
            SELECT id, nombre, ciudad, codigo, estado_estacion, created_at, updated_at
            FROM estaciones
            WHERE estado_estacion = 'activa'
            ORDER BY ciudad ASC, nombre ASC
        """)

        rows = cursor.fetchall()
        cursor.close()

        estaciones = []

        for row in rows:
            estaciones.append(cls(
                id=row[0],
                nombre=row[1],
                ciudad=row[2],
                codigo=row[3],
                estado_estacion=row[4],
                created_at=row[5],
                updated_at=row[6]
            ))

        return estaciones

    @classmethod
    def get_by_id(cls, estacion_id):
        cursor = mysql.connection.cursor()

        cursor.execute("""
            SELECT id, nombre, ciudad, codigo, estado_estacion, created_at, updated_at
            FROM estaciones
            WHERE id = %s
        """, (estacion_id,))

        row = cursor.fetchone()
        cursor.close()

        if row:
            return cls(
                id=row[0],
                nombre=row[1],
                ciudad=row[2],
                codigo=row[3],
                estado_estacion=row[4],
                created_at=row[5],
                updated_at=row[6]
            )

        return None

    @classmethod
    def get_by_codigo(cls, codigo):
        cursor = mysql.connection.cursor()

        cursor.execute("""
            SELECT id, nombre, ciudad, codigo, estado_estacion, created_at, updated_at
            FROM estaciones
            WHERE codigo = %s
        """, (codigo,))

        row = cursor.fetchone()
        cursor.close()

        if row:
            return cls(
                id=row[0],
                nombre=row[1],
                ciudad=row[2],
                codigo=row[3],
                estado_estacion=row[4],
                created_at=row[5],
                updated_at=row[6]
            )

        return None

    @classmethod
    def create(cls, nombre, ciudad, codigo, estado_estacion):
        cursor = mysql.connection.cursor()

        cursor.execute("""
            INSERT INTO estaciones (nombre, ciudad, codigo, estado_estacion)
            VALUES (%s, %s, %s, %s)
        """, (nombre, ciudad, codigo, estado_estacion))

        mysql.connection.commit()
        cursor.close()

    @classmethod
    def update(cls, estacion_id, nombre, ciudad, codigo, estado_estacion):
        cursor = mysql.connection.cursor()

        cursor.execute("""
            UPDATE estaciones
            SET nombre = %s,
                ciudad = %s,
                codigo = %s,
                estado_estacion = %s
            WHERE id = %s
        """, (nombre, ciudad, codigo, estado_estacion, estacion_id))

        mysql.connection.commit()
        cursor.close()

    @classmethod
    def toggle_estado(cls, estacion_id):
        cursor = mysql.connection.cursor()

        cursor.execute("""
            UPDATE estaciones
            SET estado_estacion = CASE
                WHEN estado_estacion = 'activa' THEN 'inactiva'
                ELSE 'activa'
            END
            WHERE id = %s
        """, (estacion_id,))

        mysql.connection.commit()
        cursor.close()

    @classmethod
    def count_activas(cls):
        cursor = mysql.connection.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM estaciones
            WHERE estado_estacion = 'activa'
        """)

        total = cursor.fetchone()[0]
        cursor.close()

        return total