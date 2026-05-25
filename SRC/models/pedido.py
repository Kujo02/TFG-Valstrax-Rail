import secrets
import string
from DB.db import mysql


class Pedido:
    def __init__(self,id=None,user_id=None,viaje_id=None,nombre_cliente=None,email_cliente=None,descripcion=None,
        espacios_solicitados=None,estado_pedido=None,codigo_seguimiento=None,created_at=None,updated_at=None,
        user_nombre=None,user_email=None,origen=None,destino=None,fecha_salida=None,fecha_llegada=None,tren_nombre=None,
        tren_codigo=None,precio_total=0,estado_pago='pendiente',stripe_session_id=None,stripe_payment_intent_id=None
    ):
        self.id = id
        self.user_id = user_id
        self.viaje_id = viaje_id
        self.nombre_cliente = nombre_cliente
        self.email_cliente = email_cliente
        self.descripcion = descripcion
        self.espacios_solicitados = espacios_solicitados
        self.estado_pedido = estado_pedido
        self.codigo_seguimiento = codigo_seguimiento
        self.created_at = created_at
        self.updated_at = updated_at

        self.user_nombre = user_nombre
        self.user_email = user_email

        self.origen = origen
        self.destino = destino
        self.fecha_salida = fecha_salida
        self.fecha_llegada = fecha_llegada

        self.tren_nombre = tren_nombre
        self.tren_codigo = tren_codigo

        self.precio_total = precio_total
        self.estado_pago = estado_pago
        self.stripe_session_id = stripe_session_id
        self.stripe_payment_intent_id = stripe_payment_intent_id

    @classmethod
    def create(cls, user_id, viaje_id, nombre_cliente, email_cliente, descripcion, espacios_solicitados, reserva_token=None):
        cursor = mysql.connection.cursor()

        try:
            codigo_seguimiento = cls.generar_codigo_seguimiento()
            precio_total = float(espacios_solicitados) * 10

            cursor.execute("""
                INSERT INTO pedidos 
                (
                    user_id, 
                    viaje_id, 
                    nombre_cliente, 
                    email_cliente, 
                    descripcion, 
                    espacios_solicitados, 
                    codigo_seguimiento,
                    precio_total,
                    estado_pago,
                    reserva_token
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'pendiente', %s)
            """, (
                user_id,
                viaje_id,
                nombre_cliente,
                email_cliente,
                descripcion,
                espacios_solicitados,
                codigo_seguimiento,
                precio_total,
                reserva_token
            ))

            mysql.connection.commit()
            return codigo_seguimiento

        except Exception:
            mysql.connection.rollback()
            raise

        finally:
            cursor.close()
    
    @classmethod
    def get_all(cls):
        cursor = mysql.connection.cursor()

        cursor.execute("""
            SELECT 
                p.id,
                p.user_id,
                p.viaje_id,
                p.nombre_cliente,
                p.email_cliente,
                p.descripcion,
                p.espacios_solicitados,
                p.estado_pedido,
                p.codigo_seguimiento,
                p.created_at,
                p.updated_at,
                u.name,
                u.email,
                eo.nombre AS origen,
                ed.nombre AS destino,
                v.fecha_salida,
                v.fecha_llegada,
                t.nombre,
                t.codigo,
                p.precio_total,
                p.estado_pago,
                p.stripe_session_id,
                p.stripe_payment_intent_id
            FROM pedidos p
            LEFT JOIN users u ON p.user_id = u.id
            JOIN viajes v ON p.viaje_id = v.id
            LEFT JOIN estaciones eo ON v.origen_id = eo.id
            LEFT JOIN estaciones ed ON v.destino_id = ed.id
            JOIN trenes t ON v.tren_id = t.id
            ORDER BY p.created_at DESC
        """)

        rows = cursor.fetchall()
        cursor.close()

        pedidos = []

        for row in rows:
            pedidos.append(cls(
                id=row[0],
                user_id=row[1],
                viaje_id=row[2],
                nombre_cliente=row[3],
                email_cliente=row[4],
                descripcion=row[5],
                espacios_solicitados=row[6],
                estado_pedido=row[7],
                codigo_seguimiento=row[8],
                created_at=row[9],
                updated_at=row[10],
                user_nombre=row[11],
                user_email=row[12],
                origen=row[13],
                destino=row[14],
                fecha_salida=row[15],
                fecha_llegada=row[16],
                tren_nombre=row[17],
                tren_codigo=row[18],
                precio_total=row[19],
                estado_pago=row[20],
                stripe_session_id=row[21],
                stripe_payment_intent_id=row[22]
            ))

        return pedidos

    @classmethod
    def get_by_user(cls, user_id):
        cursor = mysql.connection.cursor()

        cursor.execute("""
            SELECT 
                p.id,
                p.user_id,
                p.viaje_id,
                p.nombre_cliente,
                p.email_cliente,
                p.descripcion,
                p.espacios_solicitados,
                p.estado_pedido,
                p.codigo_seguimiento,
                p.created_at,
                p.updated_at,
                eo.nombre AS origen,
                ed.nombre AS destino,
                v.fecha_salida,
                v.fecha_llegada,
                t.nombre,
                t.codigo,
                p.precio_total,
                p.estado_pago,
                p.stripe_session_id,
                p.stripe_payment_intent_id
            FROM pedidos p
            JOIN viajes v ON p.viaje_id = v.id
            LEFT JOIN estaciones eo ON v.origen_id = eo.id
            LEFT JOIN estaciones ed ON v.destino_id = ed.id
            JOIN trenes t ON v.tren_id = t.id
            WHERE p.user_id = %s
            ORDER BY p.created_at DESC
        """, (user_id,))

        rows = cursor.fetchall()
        cursor.close()

        pedidos = []

        for row in rows:
            pedidos.append(cls(
                id=row[0],
                user_id=row[1],
                viaje_id=row[2],
                nombre_cliente=row[3],
                email_cliente=row[4],
                descripcion=row[5],
                espacios_solicitados=row[6],
                estado_pedido=row[7],
                codigo_seguimiento=row[8],
                created_at=row[9],
                updated_at=row[10],
                origen=row[11],
                destino=row[12],
                fecha_salida=row[13],
                fecha_llegada=row[14],
                tren_nombre=row[15],
                tren_codigo=row[16],
                precio_total=row[17],
                estado_pago=row[18],
                stripe_session_id=row[19],
                stripe_payment_intent_id=row[20]
            ))

        return pedidos

    @classmethod
    def get_by_id(cls, pedido_id):
        cursor = mysql.connection.cursor()

        cursor.execute("""
            SELECT 
                p.id,
                p.user_id,
                p.viaje_id,
                p.nombre_cliente,
                p.email_cliente,
                p.descripcion,
                p.espacios_solicitados,
                p.estado_pedido,
                p.codigo_seguimiento,
                p.created_at,
                p.updated_at,
                u.name,
                u.email,
                eo.nombre AS origen,
                ed.nombre AS destino,
                v.fecha_salida,
                v.fecha_llegada,
                t.nombre,
                t.codigo,
                p.precio_total,
                p.estado_pago,
                p.stripe_session_id,
                p.stripe_payment_intent_id
            FROM pedidos p
            LEFT JOIN users u ON p.user_id = u.id
            JOIN viajes v ON p.viaje_id = v.id
            LEFT JOIN estaciones eo ON v.origen_id = eo.id
            LEFT JOIN estaciones ed ON v.destino_id = ed.id
            JOIN trenes t ON v.tren_id = t.id
            WHERE p.id = %s
        """, (pedido_id,))

        row = cursor.fetchone()
        cursor.close()

        if row:
            return cls(
                id=row[0],
                user_id=row[1],
                viaje_id=row[2],
                nombre_cliente=row[3],
                email_cliente=row[4],
                descripcion=row[5],
                espacios_solicitados=row[6],
                estado_pedido=row[7],
                codigo_seguimiento=row[8],
                created_at=row[9],
                updated_at=row[10],
                user_nombre=row[11],
                user_email=row[12],
                origen=row[13],
                destino=row[14],
                fecha_salida=row[15],
                fecha_llegada=row[16],
                tren_nombre=row[17],
                tren_codigo=row[18],
                precio_total=row[19],
                estado_pago=row[20],
                stripe_session_id=row[21],
                stripe_payment_intent_id=row[22]
            )

        return None

    @classmethod
    def get_by_codigo_email(cls, codigo_seguimiento, email_cliente):
        cursor = mysql.connection.cursor()

        cursor.execute("""
            SELECT 
                p.id,
                p.user_id,
                p.viaje_id,
                p.nombre_cliente,
                p.email_cliente,
                p.descripcion,
                p.espacios_solicitados,
                p.estado_pedido,
                p.codigo_seguimiento,
                p.created_at,
                p.updated_at,
                u.name,
                u.email,
                eo.nombre AS origen,
                ed.nombre AS destino,
                v.fecha_salida,
                v.fecha_llegada,
                t.nombre,
                t.codigo,
                p.precio_total,
                p.estado_pago,
                p.stripe_session_id,
                p.stripe_payment_intent_id
            FROM pedidos p
            LEFT JOIN users u ON p.user_id = u.id
            JOIN viajes v ON p.viaje_id = v.id
            LEFT JOIN estaciones eo ON v.origen_id = eo.id
            LEFT JOIN estaciones ed ON v.destino_id = ed.id
            JOIN trenes t ON v.tren_id = t.id
            WHERE p.codigo_seguimiento = %s
            AND p.email_cliente = %s
        """, (codigo_seguimiento, email_cliente))

        row = cursor.fetchone()
        cursor.close()

        if row:
            return cls(
                id=row[0],
                user_id=row[1],
                viaje_id=row[2],
                nombre_cliente=row[3],
                email_cliente=row[4],
                descripcion=row[5],
                espacios_solicitados=row[6],
                estado_pedido=row[7],
                codigo_seguimiento=row[8],
                created_at=row[9],
                updated_at=row[10],
                user_nombre=row[11],
                user_email=row[12],
                origen=row[13],
                destino=row[14],
                fecha_salida=row[15],
                fecha_llegada=row[16],
                tren_nombre=row[17],
                tren_codigo=row[18],
                precio_total=row[19],
                estado_pago=row[20],
                stripe_session_id=row[21],
                stripe_payment_intent_id=row[22]
            )

        return None

    @classmethod
    def update_estado(cls, pedido_id, estado_pedido):
        cursor = mysql.connection.cursor()

        cursor.execute("""
            UPDATE pedidos
            SET estado_pedido = %s
            WHERE id = %s
        """, (estado_pedido, pedido_id))

        mysql.connection.commit()
        cursor.close()

    @classmethod
    def update_precio_total(cls, pedido_id, precio_total):
        cursor = mysql.connection.cursor()

        cursor.execute("""
            UPDATE pedidos
            SET precio_total = %s
            WHERE id = %s
        """, (precio_total, pedido_id))

        mysql.connection.commit()
        cursor.close()

    @classmethod
    def update_stripe_session(cls, pedido_id, stripe_session_id):
        cursor = mysql.connection.cursor()

        cursor.execute("""
            UPDATE pedidos
            SET stripe_session_id = %s
            WHERE id = %s
        """, (stripe_session_id, pedido_id))

        mysql.connection.commit()

        print("Stripe session guardada")
        print("Pedido ID:", pedido_id)
        print("Stripe session:", stripe_session_id)
        print("Filas actualizadas:", cursor.rowcount)

        cursor.close()

    @classmethod
    def marcar_pagado(cls, pedido_id, stripe_session_id, payment_intent_id):
        cursor = mysql.connection.cursor()

        cursor.execute("""
            UPDATE pedidos
            SET estado_pago = 'pagado',
                stripe_session_id = %s,
                stripe_payment_intent_id = %s
            WHERE id = %s
        """, (stripe_session_id, payment_intent_id, pedido_id))

        mysql.connection.commit()

        print("Pedido marcado como pagado")
        print("Pedido ID:", pedido_id)
        print("Stripe session:", stripe_session_id)
        print("Payment intent:", payment_intent_id)
        print("Filas actualizadas:", cursor.rowcount)

        cursor.close()

    @classmethod
    def marcar_pagado_por_session(cls, stripe_session_id, payment_intent_id):
        cursor = mysql.connection.cursor()

        cursor.execute("""
            UPDATE pedidos
            SET estado_pago = 'pagado',
                stripe_payment_intent_id = %s
            WHERE stripe_session_id = %s
        """, (payment_intent_id, stripe_session_id))

        mysql.connection.commit()

        print("Pedido marcado como pagado por session")
        print("Stripe session:", stripe_session_id)
        print("Payment intent:", payment_intent_id)
        print("Filas actualizadas:", cursor.rowcount)

        cursor.close()

    @classmethod
    def marcar_cancelado_por_session(cls, stripe_session_id):
        cursor = mysql.connection.cursor()

        cursor.execute("""
            UPDATE pedidos
            SET estado_pago = 'cancelado'
            WHERE stripe_session_id = %s
            AND estado_pago = 'pendiente'
        """, (stripe_session_id,))

        mysql.connection.commit()
        cursor.close()

    @classmethod
    def count_pendientes(cls):
        cursor = mysql.connection.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM pedidos
            WHERE estado_pedido = 'pendiente'
        """)

        total = cursor.fetchone()[0]
        cursor.close()

        return total

    @classmethod
    def generar_codigo_seguimiento(cls):
        caracteres = string.ascii_uppercase + string.digits

        while True:
            codigo = 'VR-' + ''.join(secrets.choice(caracteres) for _ in range(6))

            cursor = mysql.connection.cursor()

            cursor.execute("""
                SELECT id
                FROM pedidos
                WHERE codigo_seguimiento = %s
            """, (codigo,))

            existe = cursor.fetchone()
            cursor.close()

            if not existe:
                return codigo