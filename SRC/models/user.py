from DB.db import mysql
from flask_login import UserMixin

class User(UserMixin):
    
    def __init__(self, id=None, name=None, email=None, password=None, role=None,estado=None, role_id=None):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.role = role
        self.estado = estado
        self.role_id = role_id
        
    @classmethod
    def get_by_email(cls, email):
        cursor = mysql.connection.cursor()
        cursor.execute("""
            SELECT u.id, u.name, u.email, u.password, r.name, u.estado_user
            FROM users u
            JOIN roles r ON u.role_id = r.id
            WHERE u.email = %s
        """, (email,))

        row = cursor.fetchone()
        cursor.close()

        if row:
            return cls(
                id=row[0],
                name=row[1],
                email=row[2],
                password=row[3],
                role=row[4],
                estado=row[5]
            )
        return None

    @classmethod
    def create(cls, username, email, password):
        cursor = mysql.connection.cursor()

        cursor.execute("""
            INSERT INTO users (name, email, password, role_id)
            VALUES (%s, %s, %s, %s)
        """, (username, email, password, 1))

        mysql.connection.commit()
        cursor.close()
    
    @classmethod
    def get_by_id(cls, user_id):
        cursor = mysql.connection.cursor()
        cursor.execute("""
        SELECT u.id, u.name, u.email, u.password, r.name, u.estado_user, u.role_id
        FROM users u
        JOIN roles r ON u.role_id = r.id
        WHERE u.id = %s
    """, (user_id,))
        row = cursor.fetchone()
        cursor.close()

        if row:
            return cls(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
        return None
    

    
    @classmethod
    def get_all(cls):
        cursor = mysql.connection.cursor()
        cursor.execute("""
            SELECT u.id, u.name, u.email, u.password, r.name, u.estado_user
            FROM users u
            JOIN roles r ON u.role_id = r.id
            ORDER BY u.id DESC
        """)
        rows = cursor.fetchall()
        cursor.close()

        users = []

        for row in rows:
            users.append(cls(
                id=row[0],
                name=row[1],
                email=row[2],
                password=row[3],
                role=row[4],
                estado=row[5]
            ))

        return users
    

    @classmethod
    def get_all_roles(cls):
        cursor = mysql.connection.cursor()
        cursor.execute("""
            SELECT id, name
            FROM roles
            ORDER BY id ASC
        """)

        rows = cursor.fetchall()
        cursor.close()

        roles = []

        for row in rows:
            roles.append({
                "id": row[0],
                "name": row[1]
            })

        return roles
    


    @classmethod
    def update_user(cls, user_id, name, email, role_id, estado_user):
        cursor = mysql.connection.cursor()

        cursor.execute("""
            UPDATE users
            SET name = %s,
                email = %s,
                role_id = %s,
                estado_user = %s
            WHERE id = %s
        """, (name, email, role_id, estado_user, user_id))

        mysql.connection.commit()
        cursor.close()


    @classmethod
    def toggle_estado(cls, user_id):
        cursor = mysql.connection.cursor()

        cursor.execute("""
            UPDATE users
            SET estado_user = CASE
                WHEN estado_user = 'activo' THEN 'deshabilitado'
                ELSE 'activo'
            END
            WHERE id = %s
        """, (user_id,))

        mysql.connection.commit()
        cursor.close()



    @classmethod
    def update_name(cls, user_id, name):
        cursor = mysql.connection.cursor()

        cursor.execute("""
            UPDATE users
            SET name = %s
            WHERE id = %s
        """, (name, user_id))

        mysql.connection.commit()
        cursor.close()