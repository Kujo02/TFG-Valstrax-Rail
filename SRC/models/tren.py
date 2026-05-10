from DB.db import mysql

class Tren:
    def __init__(self, id=None, nombre=None, codigo=None, estado_tren=None, created_at=None, updated_at=None):
        self.id = id
        self.nombre = nombre
        self.codigo = codigo
        self.estado_tren = estado_tren
        self.created_at = created_at
        self.updated_at = updated_at

    @classmethod
    def get_all(cls):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT id, nombre, codigo, estado_tren, created_at, updated_at FROM trenes")
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
                updated_at=row[5]
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
            SELECT id, nombre, codigo, estado_tren, created_at, updated_at
            FROM trenes
            WHERE id = %s
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
                updated_at=row[5]
            )

        return None
    
    @classmethod
    def create(cls, nombre, codigo, estado_tren):
        cursor = mysql.connection.cursor()

        cursor.execute("""
            INSERT INTO trenes (nombre, codigo, estado_tren)
            VALUES (%s, %s, %s)
        """, (nombre, codigo, estado_tren))

        mysql.connection.commit()
        cursor.close()


    @classmethod
    def get_by_codigo(cls, codigo):
        cursor = mysql.connection.cursor()
        cursor.execute("""
            SELECT id, nombre, codigo, estado_tren, created_at, updated_at
            FROM trenes
            WHERE codigo = %s
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
                updated_at=row[5]
            )

        return None
    

    @classmethod
    def update(cls, tren_id, nombre, codigo, estado_tren):
        cursor = mysql.connection.cursor()

        cursor.execute("""
            UPDATE trenes
            SET nombre = %s,
                codigo = %s,
                estado_tren = %s
            WHERE id = %s
        """, (nombre, codigo, estado_tren, tren_id))

        mysql.connection.commit()
        cursor.close()