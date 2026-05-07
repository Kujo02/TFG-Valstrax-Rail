from DB.db import mysql
from flask_login import UserMixin

class User(UserMixin):
    
    def __init__(self, id=None, name=None, email=None, password=None, role=None,estado=None):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.role = role
        self.estado = estado
        
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
        SELECT u.id, u.name, u.email, u.password, r.name, u.estado_user
        FROM users u
        JOIN roles r ON u.role_id = r.id
        WHERE u.id = %s
    """, (user_id,))
        row = cursor.fetchone()
        cursor.close()

        if row:
            return cls(row[0], row[1], row[2], row[3], row[4], row[5])
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