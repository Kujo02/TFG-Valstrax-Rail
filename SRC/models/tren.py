from DB.db import mysql

class Tren:
    def __init__(self,id=None,nombre=None,codigo=None,estado_tren=None,created_at=None,updated_at=None,
        estacion_actual_id=None,estacion_actual_nombre=None,estacion_actual_ciudad=None
    ):
        self.id = id
        self.nombre = nombre
        self.codigo = codigo
        self.estado_tren = estado_tren
        self.created_at = created_at
        self.updated_at = updated_at
        self.estacion_actual_id = estacion_actual_id
        self.estacion_actual_nombre = estacion_actual_nombre
        self.estacion_actual_ciudad = estacion_actual_ciudad

    @classmethod
    def get_all(cls):
        cursor = mysql.connection.cursor()

        cursor.execute("""
            SELECT 
                t.id,
                t.nombre,
                t.codigo,
                t.estado_tren,
                t.created_at,
                t.updated_at,
                t.estacion_actual_id,
                e.nombre,
                e.ciudad
            FROM trenes t
            LEFT JOIN estaciones e ON t.estacion_actual_id = e.id
            ORDER BY t.id DESC
        """)

        rows = cursor.fetchall()
        cursor.close()

        trenes = []

        for row in rows:
            trenes.append(cls(
                id=row[0],
                nombre=row[1],
                codigo=row[2],
                estado_tren=row[3],
                created_at=row[4],
                updated_at=row[5],
                estacion_actual_id=row[6],
                estacion_actual_nombre=row[7],
                estacion_actual_ciudad=row[8]
            ))

        return trenes
    
    @classmethod
    def toggle_estado(cls, tren_id):
        cursor = mysql.connection.cursor()

        cursor.execute("""
            UPDATE trenes
            SET estado_tren = CASE
                WHEN estado_tren = 'activo' THEN 'inactivo'
                ELSE 'activo'
            END
            WHERE id = %s
        """, (tren_id,))

        mysql.connection.commit()
        cursor.close()

    @classmethod
    def get_by_id(cls, tren_id):
        cursor = mysql.connection.cursor()

        cursor.execute("""
            SELECT 
                t.id,
                t.nombre,
                t.codigo,
                t.estado_tren,
                t.created_at,
                t.updated_at,
                t.estacion_actual_id,
                e.nombre,
                e.ciudad
            FROM trenes t
            LEFT JOIN estaciones e ON t.estacion_actual_id = e.id
            WHERE t.id = %s
        """, (tren_id,))

        row = cursor.fetchone()
        cursor.close()

        if row:
            return cls(
                id=row[0],
                nombre=row[1],
                codigo=row[2],
                estado_tren=row[3],
                created_at=row[4],
                updated_at=row[5],
                estacion_actual_id=row[6],
                estacion_actual_nombre=row[7],
                estacion_actual_ciudad=row[8]
            )

        return None
    
    @classmethod
    def create(cls, nombre, codigo, estado_tren, estacion_actual_id):
        cursor = mysql.connection.cursor()

        cursor.execute("""
            INSERT INTO trenes (nombre, codigo, estado_tren, estacion_actual_id)
            VALUES (%s, %s, %s, %s)
        """, (nombre, codigo, estado_tren, estacion_actual_id))

        mysql.connection.commit()
        cursor.close()

    @classmethod
    def get_by_codigo(cls, codigo):
        cursor = mysql.connection.cursor()

        cursor.execute("""
            SELECT 
                t.id,
                t.nombre,
                t.codigo,
                t.estado_tren,
                t.created_at,
                t.updated_at,
                t.estacion_actual_id,
                e.nombre,
                e.ciudad
            FROM trenes t
            LEFT JOIN estaciones e ON t.estacion_actual_id = e.id
            WHERE t.codigo = %s
        """, (codigo,))

        row = cursor.fetchone()
        cursor.close()

        if row:
            return cls(
                id=row[0],
                nombre=row[1],
                codigo=row[2],
                estado_tren=row[3],
                created_at=row[4],
                updated_at=row[5],
                estacion_actual_id=row[6],
                estacion_actual_nombre=row[7],
                estacion_actual_ciudad=row[8]
            )

        return None
    
    @classmethod
    def update(cls, tren_id, nombre, codigo, estado_tren, estacion_actual_id):
        cursor = mysql.connection.cursor()

        cursor.execute("""
            UPDATE trenes
            SET nombre = %s,
                codigo = %s,
                estado_tren = %s,
                estacion_actual_id = %s
            WHERE id = %s
        """, (nombre, codigo, estado_tren, estacion_actual_id, tren_id))

        mysql.connection.commit()
        cursor.close()

    @classmethod
    def get_activos(cls):
        cursor = mysql.connection.cursor()

        cursor.execute("""
            SELECT 
                t.id,
                t.nombre,
                t.codigo,
                t.estado_tren,
                t.created_at,
                t.updated_at,
                t.estacion_actual_id,
                e.nombre,
                e.ciudad
            FROM trenes t
            LEFT JOIN estaciones e ON t.estacion_actual_id = e.id
            WHERE t.estado_tren = 'activo'
            ORDER BY t.nombre ASC
        """)

        rows = cursor.fetchall()
        cursor.close()

        trenes = []

        for row in rows:
            trenes.append(cls(
                id=row[0],
                nombre=row[1],
                codigo=row[2],
                estado_tren=row[3],
                created_at=row[4],
                updated_at=row[5],
                estacion_actual_id=row[6],
                estacion_actual_nombre=row[7],
                estacion_actual_ciudad=row[8]
            ))

        return trenes
    
    @classmethod
    def count_activos(cls):
        cursor = mysql.connection.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM trenes
            WHERE estado_tren = 'activo'
        """)

        total = cursor.fetchone()[0]
        cursor.close()

        return total