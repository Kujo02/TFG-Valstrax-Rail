from flask import Blueprint, render_template,redirect, url_for, request, flash
from flask_login import current_user,login_required
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
    viajes = Viaje.get_disponibles()
    return render_template('reservar.html', viajes=viajes)




@main.route('/reservar/<int:viaje_id>', methods=['GET', 'POST'])
def reservar_viaje(viaje_id):
    viaje = Viaje.get_by_id(viaje_id)

    if not viaje:
        flash('El viaje no existe.', 'danger')
        return redirect(url_for('main.reservar'))

    if viaje.estado_viaje != 'programado':
        flash('Este viaje no está disponible para reservas.', 'danger')
        return redirect(url_for('main.reservar'))

    form = PedidoForm()

    if current_user.is_authenticated and request.method == 'GET':
        form.nombre_cliente.data = current_user.name
        form.email_cliente.data = current_user.email

    if form.validate_on_submit():
        nombre_cliente = form.nombre_cliente.data
        email_cliente = form.email_cliente.data
        descripcion = form.descripcion.data
        espacios_solicitados = form.espacios_solicitados.data

        user_id = current_user.id if current_user.is_authenticated else None

        Pedido.create(
            user_id,
            viaje_id,
            nombre_cliente,
            email_cliente,
            descripcion,
            espacios_solicitados
        )

        flash('Reserva creada correctamente. Queda pendiente de revisión.', 'success')

        if current_user.is_authenticated:
            return redirect(url_for('main.mis_pedidos'))

        return redirect(url_for('main.reservar'))

    return render_template('reservar_viaje.html', form=form, viaje=viaje)




@main.route('/mis-pedidos')
@login_required
def mis_pedidos():
    pedidos = Pedido.get_by_user(current_user.id)
    return render_template('mis_pedidos.html', pedidos=pedidos)