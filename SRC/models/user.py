from DB.db import mysql

class User:
    
    def __init__(self, id=None, name=None, email=None, password=None):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        
    @classmethod
    def get_by_email(cls, email):
        cursor = mysql.connection.cursor()
        cursor.execute("""
            SELECT u.id, u.name, u.email, u.password, r.name
            FROM users u
            JOIN roles r ON u.role_id = r.id
            WHERE u.email = %s
        """, (email,))

        row = cursor.fetchone()
        cursor.close()

        if row:
            return cls(
                id=row[0],
                username=row[1],
                email=row[2],
                password=row[3],
                role=row[4]
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