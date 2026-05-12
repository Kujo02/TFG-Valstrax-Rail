from DB.db import mysql


class Vagon:
    def __init__(self,id=None,tren_id=None,nombre=None,filas=None,columnas=None,capacidad_m2=None,estado_vagon=None,
        created_at=None,updated_at=None,tren_nombre=None):
        self.id = id
        self.tren_id = tren_id
        self.nombre = nombre
        self.filas = filas
        self.columnas = columnas
        self.capacidad_m2 = capacidad_m2
        self.estado_vagon = estado_vagon
        self.created_at = created_at
        self.updated_at = updated_at
        self.tren_nombre = tren_nombre

    @classmethod
    def get_all(cls):
        cursor = mysql.connection.cursor()

        cursor.execute("""
            SELECT 
                v.id,
                v.tren_id,
                v.nombre,
                v.filas,
                v.columnas,
                v.capacidad_m2,
                v.estado_vagon,
                v.created_at,
                v.updated_at,
                t.nombre
            FROM vagones v
            JOIN trenes t ON v.tren_id = t.id
            ORDER BY v.id DESC
        """)

        rows = cursor.fetchall()
        cursor.close()

        vagones = []

        for row in rows:
            vagones.append(cls(
                id=row[0],
                tren_id=row[1],
                nombre=row[2],
                filas=row[3],
                columnas=row[4],
                capacidad_m2=row[5],
                estado_vagon=row[6],
                created_at=row[7],
                updated_at=row[8],
                tren_nombre=row[9]
            ))

        return vagones

    @classmethod
    def get_by_tren_id(cls, tren_id):
        cursor = mysql.connection.cursor()

        cursor.execute("""
            SELECT 
                id,
                tren_id,
                nombre,
                filas,
                columnas,
                capacidad_m2,
                estado_vagon,
                created_at,
                updated_at
            FROM vagones
            WHERE tren_id = %s
            ORDER BY id DESC
        """, (tren_id,))

        rows = cursor.fetchall()
        cursor.close()

        vagones = []

        for row in rows:
            vagones.append(cls(
                id=row[0],
                tren_id=row[1],
                nombre=row[2],
                filas=row[3],
                columnas=row[4],
                capacidad_m2=row[5],
                estado_vagon=row[6],
                created_at=row[7],
                updated_at=row[8]
            ))

        return vagones

    @classmethod
    def get_by_id(cls, vagon_id):
        cursor = mysql.connection.cursor()

        cursor.execute("""
            SELECT 
                id,
                tren_id,
                nombre,
                filas,
                columnas,
                capacidad_m2,
                estado_vagon,
                created_at,
                updated_at
            FROM vagones
            WHERE id = %s
        """, (vagon_id,))

        row = cursor.fetchone()
        cursor.close()

        if row:
            return cls(
                id=row[0],
                tren_id=row[1],
                nombre=row[2],
                filas=row[3],
                columnas=row[4],
                capacidad_m2=row[5],
                estado_vagon=row[6],
                created_at=row[7],
                updated_at=row[8]
            )

        return None

    @classmethod
    def get_by_nombre_and_tren(cls, nombre, tren_id):
        cursor = mysql.connection.cursor()

        cursor.execute("""
            SELECT 
                id,
                tren_id,
                nombre,
                filas,
                columnas,
                capacidad_m2,
                estado_vagon,
                created_at,
                updated_at
            FROM vagones
            WHERE nombre = %s AND tren_id = %s
        """, (nombre, tren_id))

        row = cursor.fetchone()
        cursor.close()

        if row:
            return cls(
                id=row[0],
                tren_id=row[1],
                nombre=row[2],
                filas=row[3],
                columnas=row[4],
                capacidad_m2=row[5],
                estado_vagon=row[6],
                created_at=row[7],
                updated_at=row[8]
            )

        return None

    @classmethod
    def create(cls, tren_id, nombre, filas, columnas, estado_vagon):
        capacidad_m2 = int(filas) * int(columnas)

        cursor = mysql.connection.cursor()

        cursor.execute("""
            INSERT INTO vagones (tren_id, nombre, filas, columnas, capacidad_m2, estado_vagon)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (tren_id, nombre, filas, columnas, capacidad_m2, estado_vagon))

        mysql.connection.commit()
        cursor.close()

    @classmethod
    def update(cls, vagon_id, nombre, filas, columnas, estado_vagon):
        capacidad_m2 = int(filas) * int(columnas)

        cursor = mysql.connection.cursor()

        cursor.execute("""
            UPDATE vagones
            SET nombre = %s,
                filas = %s,
                columnas = %s,
                capacidad_m2 = %s,
                estado_vagon = %s
            WHERE id = %s
        """, (nombre, filas, columnas, capacidad_m2, estado_vagon, vagon_id))

        mysql.connection.commit()
        cursor.close()

    @classmethod
    def toggle_estado(cls, vagon_id):
        cursor = mysql.connection.cursor()

        cursor.execute("""
            UPDATE vagones
            SET estado_vagon = CASE
                WHEN estado_vagon = 'activo' THEN 'inactivo'
                ELSE 'activo'
            END
            WHERE id = %s
        """, (vagon_id,))

        mysql.connection.commit()
        cursor.close()