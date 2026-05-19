from flask import Blueprint, render_template,redirect, url_for, request, flash
from flask_login import current_user,login_required
from utils.email import enviar_correo_seguimiento
from models.user import User
from models.pedido import Pedido
from models.viaje import Viaje   
from forms import PedidoForm

main = Blueprint('main', __name__)

@main.route('/')
def index():

    if current_user.is_authenticated:

        if current_user.role == "admin":
            return redirect(url_for('admin.dashboard'))
        
        else:
            return redirect(url_for('main.home'))

    return redirect(url_for('main.home')) #TODO cambiar a render 


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
    viajes = Viaje.get_disponibles()
    return render_template('reservar.html', viajes=viajes)




@main.route('/reservar/<int:viaje_id>', methods=['GET', 'POST'])
def reservar_viaje(viaje_id):
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
    espacio_disponible = Viaje.get_espacio_disponible(viaje_id)

    form = PedidoForm()

    if current_user.is_authenticated and request.method == 'GET':
        form.nombre_cliente.data = current_user.name
        form.email_cliente.data = current_user.email

    if form.validate_on_submit():
        nombre_cliente = form.nombre_cliente.data
        email_cliente = form.email_cliente.data
        descripcion = form.descripcion.data
        espacios_solicitados = form.espacios_solicitados.data

        if espacios_solicitados > espacio_disponible:
            flash('No hay suficiente espacio disponible para este viaje.', 'danger')
            return render_template(
                'reservar_viaje.html',
                form=form,
                viaje=viaje,
                capacidad_total=capacidad_total,
                espacio_reservado=espacio_reservado,
                espacio_disponible=espacio_disponible
            )

        user_id = current_user.id if current_user.is_authenticated else None

        codigo_seguimiento = Pedido.create(
            user_id,
            viaje_id,
            nombre_cliente,
            email_cliente,
            descripcion,
            espacios_solicitados
        )

        pedido = Pedido.get_by_codigo_email(codigo_seguimiento, email_cliente)

        if  pedido:
            
            enviar_correo_seguimiento(pedido)


        flash('Reserva creada correctamente. Hemos enviado el código de seguimiento a tu correo.', 'success')

        if current_user.is_authenticated:
            return redirect(url_for('main.mis_pedidos'))

        return redirect(url_for('main.reservar'))

    return render_template(
        'reservar_viaje.html',
        form=form,
        viaje=viaje,
        capacidad_total=capacidad_total,
        espacio_reservado=espacio_reservado,
        espacio_disponible=espacio_disponible
    )



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

        if not pedido:
            flash('No se ha encontrado ningún pedido con esos datos.', 'danger')
            return render_template('seguimiento_pedido.html', pedido=None)

    return render_template('seguimiento_pedido.html', pedido=pedido)