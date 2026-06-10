from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from flask_login import current_user, login_required
from utils.email import enviar_correo_seguimiento
from models.user import User
from models.pedido import Pedido
from models.viaje import Viaje
from models.estacion import Estacion
from forms import PedidoForm
import secrets
import MySQLdb
from threading import Lock


main = Blueprint('main', __name__)


# Bloqueo en memoria para evitar varios POST simultáneos del mismo formulario
reservas_en_proceso = set()
reservas_usadas = set()
reservas_lock = Lock()


@main.route('/')
def index():
    if current_user.is_authenticated:
        if current_user.role == "admin":
            return redirect(url_for('admin.dashboard'))
        else:
            return redirect(url_for('main.home'))

    return redirect(url_for('main.home'))


@main.route('/home')
def home():
    if current_user.is_authenticated:
        if current_user.role == "admin":
            return redirect(url_for('admin.dashboard'))

    return render_template('home.html')


@main.route('/profile', methods=['GET', 'POST'])
def profile():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        name = request.form.get('name')

        if not name:
            flash('El nombre no puede estar vacío.', 'danger')
            return render_template('profile.html')

        User.update_name(current_user.id, name)

        flash('Nombre actualizado correctamente.', 'success')
        return redirect(url_for('main.profile'))

    return render_template('profile.html')


@main.route('/reservar')
def reservar():
    Viaje.actualizar_estados_automaticos()

    origen_id = request.args.get('origen_id', type=int)
    destino_id = request.args.get('destino_id', type=int)

    viajes = Viaje.get_disponibles(
        origen_id=origen_id,
        destino_id=destino_id
    )

    estaciones = Estacion.get_all()

    return render_template(
        'reservar.html',
        viajes=viajes,
        estaciones=estaciones,
        origen_id=origen_id,
        destino_id=destino_id
    )


@main.route('/reservar/<int:viaje_id>', methods=['GET', 'POST'])
def reservar_viaje(viaje_id):
    reserva_token_form = None
    token_bloqueado = False

    # Protección temprana: si llegan varios POST a la vez,
    # solo el primero pasa. Los demás se cortan antes de tocar MySQL.
    if request.method == 'POST':
        reserva_token_form = request.form.get('reserva_token')
        reserva_token_session = session.get('reserva_token')

        if not reserva_token_form or reserva_token_form != reserva_token_session:
            flash('La reserva ya se está procesando o el formulario ha caducado.', 'warning')
            return redirect(url_for('main.reservar'))

        with reservas_lock:
            if reserva_token_form in reservas_en_proceso or reserva_token_form in reservas_usadas:
                flash('Esta reserva ya se está procesando. Evita pulsar varias veces el botón.', 'warning')
                return redirect(url_for('main.reservar'))

            reservas_en_proceso.add(reserva_token_form)
            token_bloqueado = True

    try:
        Viaje.actualizar_estados_automaticos()
        viaje = Viaje.get_by_id(viaje_id)

        if not viaje:
            flash('El viaje no existe.', 'danger')
            return redirect(url_for('main.reservar'))

        if viaje.estado_viaje != 'programado':
            flash('Este viaje no está disponible para reservas.', 'danger')
            return redirect(url_for('main.reservar'))

        capacidad_total = Viaje.get_capacidad_total(viaje_id)
        espacio_reservado = Viaje.get_espacio_reservado(viaje_id)
        espacio_disponible = capacidad_total - espacio_reservado

        if espacio_disponible < 0:
            espacio_disponible = 0

        form = PedidoForm()

        if request.method == 'GET':
            session['reserva_token'] = secrets.token_urlsafe(32)

            if current_user.is_authenticated:
                form.nombre_cliente.data = current_user.name
                form.email_cliente.data = current_user.email

        if form.validate_on_submit():
            nombre_cliente = form.nombre_cliente.data
            email_cliente = form.email_cliente.data
            descripcion = form.descripcion.data
            espacios_solicitados = form.espacios_solicitados.data

            if espacios_solicitados > espacio_disponible:
                flash('No hay suficiente espacio disponible para este viaje.', 'danger')

                session['reserva_token'] = secrets.token_urlsafe(32)

                return render_template(
                    'reservar_viaje.html',
                    form=form,
                    viaje=viaje,
                    capacidad_total=capacidad_total,
                    espacio_reservado=espacio_reservado,
                    espacio_disponible=espacio_disponible,
                    reserva_token=session['reserva_token']
                )

            user_id = current_user.id if current_user.is_authenticated else None

            try:
                codigo_seguimiento = Pedido.create(
                    user_id,
                    viaje_id,
                    nombre_cliente,
                    email_cliente,
                    descripcion,
                    espacios_solicitados,
                    reserva_token_form
                )

                # Se elimina el token de la sesión y se marca como usado en memoria
                session.pop('reserva_token', None)

                with reservas_lock:
                    reservas_usadas.add(reserva_token_form)

            except MySQLdb.IntegrityError as e:
                # 1062 = entrada duplicada por índice UNIQUE
                if e.args[0] == 1062:
                    flash('Esta reserva ya se ha procesado. Evita pulsar varias veces el botón.', 'warning')

                    if current_user.is_authenticated:
                        return redirect(url_for('main.mis_pedidos'))

                    return redirect(url_for('main.reservar'))

                raise

            pedido = Pedido.get_by_codigo_email(codigo_seguimiento, email_cliente)

            try:
                if pedido:
                    enviar_correo_seguimiento(pedido)

                flash('Reserva creada correctamente. Hemos enviado el código de seguimiento a tu correo.', 'success')

            except Exception as e:
                print("Error al enviar correo:", e)

                flash(
                    'Reserva creada correctamente, pero no se pudo enviar el correo de seguimiento. Contacta con administración si necesitas el código.',
                    'warning'
                )

            if current_user.is_authenticated:
                return redirect(url_for('main.mis_pedidos'))

            return redirect(url_for('main.reservar'))

        return render_template(
            'reservar_viaje.html',
            form=form,
            viaje=viaje,
            capacidad_total=capacidad_total,
            espacio_reservado=espacio_reservado,
            espacio_disponible=espacio_disponible,
            reserva_token=session.get('reserva_token')
        )

    finally:
        if token_bloqueado and reserva_token_form:
            with reservas_lock:
                reservas_en_proceso.discard(reserva_token_form)


@main.route('/mis-pedidos')
@login_required
def mis_pedidos():
    pedidos = Pedido.get_by_user(current_user.id)
    return render_template('mis_pedidos.html', pedidos=pedidos)


@main.route('/seguimiento', methods=['GET', 'POST'])
def seguimiento_pedido():
    pedido = None

    if request.method == 'POST':
        codigo_seguimiento = request.form.get('codigo_seguimiento')
        email_cliente = request.form.get('email_cliente')

        if not codigo_seguimiento or not email_cliente:
            flash('Debes introducir el código de seguimiento y el email.', 'danger')
            return render_template('seguimiento_pedido.html', pedido=pedido)

        codigo_seguimiento = codigo_seguimiento.strip().upper()
        email_cliente = email_cliente.strip().lower()

        pedido = Pedido.get_by_codigo_email(codigo_seguimiento, email_cliente)

        if pedido:
            session['pedido_seguimiento'] = pedido.id

        if not pedido:
            flash('No se ha encontrado ningún pedido con esos datos.', 'danger')
            return render_template('seguimiento_pedido.html', pedido=None)

    return render_template('seguimiento_pedido.html', pedido=pedido)



