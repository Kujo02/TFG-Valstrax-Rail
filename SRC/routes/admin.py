from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from functools import wraps
from models.user import User
from models.tren import Tren
from models.vagon import Vagon
from models.viaje import Viaje
from models.pedido import Pedido
from models.estacion import Estacion
from forms import TrenForm, VagonForm, ViajeForm, EstacionForm 
from datetime import datetime, timedelta


admin = Blueprint('admin', __name__, url_prefix='/admin')


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        

        if current_user.role != "admin":
            abort(403)

        return f(*args, **kwargs)

    return decorated_function


@admin.route('/dashboard')
@login_required
@admin_required
def dashboard():
    total_usuarios = User.count_all()
    trenes_activos = Tren.count_activos()
    vagones_activos = Vagon.count_activos()
    viajes_programados = Viaje.count_programados()
    pedidos_pendientes = Pedido.count_pendientes()

    return render_template(
        'admin/dashboard.html',
        total_usuarios=total_usuarios,
        trenes_activos=trenes_activos,
        vagones_activos=vagones_activos,
        viajes_programados=viajes_programados,
        pedidos_pendientes=pedidos_pendientes
    )


@admin.route('/users')
@login_required
@admin_required
def users():
    users = User.get_all()

    return render_template('admin/users.html', users=users)



@admin.route('/users/<int:user_id>/edit_users', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(user_id):
    user = User.get_by_id(user_id)
    roles = User.get_all_roles()

    if not user:
        flash('El usuario no existe.', 'danger')
        return redirect(url_for('admin.users'))

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        role_id = request.form.get('role_id')
        estado_user = request.form.get('estado_user')

        User.update_user(user_id, name, email, role_id, estado_user)

        flash('Usuario actualizado correctamente.', 'success')
        return redirect(url_for('admin.users'))

    return render_template('admin/edit_user.html', user=user, roles=roles)





@admin.route('/users/<int:user_id>/toggle_estado', methods=['POST'])
@login_required
@admin_required
def toggle_user_estado(user_id):
    if user_id == int(current_user.id):
        flash('No puedes deshabilitar tu propio usuario.', 'danger')
        return redirect(url_for('admin.users'))

    User.toggle_estado(user_id)

    flash('Estado del usuario actualizado correctamente.', 'success')
    return redirect(url_for('admin.users'))


@admin.route('/trenes')
@login_required 
@admin_required
def trenes():
    trenes = Tren.get_all()
    return render_template('admin/trenes.html', trenes=trenes)




@admin.route('/trenes/<int:tren_id>/toggle_estado', methods=['GET', 'POST'])
@login_required
@admin_required
def toggle_tren_estado(tren_id):
    Tren.toggle_estado(tren_id)

    flash('Estado del tren actualizado correctamente.', 'success')
    return redirect(url_for('admin.trenes'))




@admin.route('/trenes/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_tren():
    form = TrenForm()

    estaciones_activas = Estacion.get_activas()

    form.estacion_actual_id.choices = [
        (estacion.id, f'{estacion.nombre} - {estacion.ciudad}')
        for estacion in estaciones_activas
    ]

    if form.validate_on_submit():
        nombre = form.nombre.data
        codigo = form.codigo.data
        estado_tren = form.estado_tren.data
        estacion_actual_id = form.estacion_actual_id.data

        tren_existe = Tren.get_by_codigo(codigo)

        if tren_existe:
            flash('Ya existe un tren con ese código.', 'danger')
            return render_template('admin/tren_insert.html', form=form, title='Nuevo tren')

        Tren.create(nombre, codigo, estado_tren, estacion_actual_id)

        flash('Tren creado correctamente.', 'success')
        return redirect(url_for('admin.trenes'))

    return render_template('admin/tren_insert.html', form=form, title='Nuevo tren')



@admin.route('/trenes/<int:tren_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_tren(tren_id):
    tren = Tren.get_by_id(tren_id)

    if not tren:
        flash('El tren no existe.', 'danger')
        return redirect(url_for('admin.trenes'))

    form = TrenForm(obj=tren)

    estaciones_activas = Estacion.get_activas()

    choices = [
        (estacion.id, f'{estacion.nombre} - {estacion.ciudad}')
        for estacion in estaciones_activas
    ]

    # Por si el tren tiene una estación inactiva asignada, la mantenemos en el select
    if tren.estacion_actual_id and tren.estacion_actual_id not in [estacion.id for estacion in estaciones_activas]:
        choices.append(
            (
                tren.estacion_actual_id,
                f'{tren.estacion_actual_nombre} - {tren.estacion_actual_ciudad}'
            )
        )

    form.estacion_actual_id.choices = choices

    if form.validate_on_submit():
        nombre = form.nombre.data
        codigo = form.codigo.data
        estado_tren = form.estado_tren.data
        estacion_actual_id = form.estacion_actual_id.data

        tren_existe = Tren.get_by_codigo(codigo)

        if tren_existe and tren_existe.id != tren.id:
            flash('Ya existe otro tren con ese código.', 'danger')
            return render_template(
                'admin/tren_edit.html',
                form=form,
                tren=tren,
                title='Editar tren'
            )

        Tren.update(tren_id, nombre, codigo, estado_tren, estacion_actual_id)

        flash('Tren actualizado correctamente.', 'success')
        return redirect(url_for('admin.trenes'))

    return render_template(
        'admin/tren_edit.html',
        form=form,
        tren=tren,
        title='Editar tren'
    )






@admin.route('/vagones')
@login_required
@admin_required
def vagones():
    vagones = Vagon.get_all()
    return render_template('admin/vagones.html', vagones=vagones)




@admin.route('/trenes/<int:tren_id>/vagones')
@login_required
@admin_required
def vagones_tren(tren_id):
    tren = Tren.get_by_id(tren_id)

    if not tren:
        flash('El tren no existe.', 'danger')
        return redirect(url_for('admin.trenes'))

    vagones = Vagon.get_by_tren_id(tren_id)

    return render_template('admin/vagones_tren.html', tren=tren, vagones=vagones)




@admin.route('/trenes/<int:tren_id>/vagones/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_vagon(tren_id):
    tren = Tren.get_by_id(tren_id)

    if not tren:
        flash('El tren no existe.', 'danger')
        return redirect(url_for('admin.trenes'))

    form = VagonForm()

    if form.validate_on_submit():
        nombre = form.nombre.data
        filas = form.filas.data
        columnas = form.columnas.data
        estado_vagon = form.estado_vagon.data

        vagon_existe = Vagon.get_by_nombre_and_tren(nombre, tren_id)

        if vagon_existe:
            flash('Ya existe un vagón con ese nombre en este tren.', 'danger')
            return render_template('admin/vagon_insert.html', form=form, tren=tren, title='Nuevo vagón')

        Vagon.create(tren_id, nombre, filas, columnas, estado_vagon)

        flash('Vagón creado correctamente.', 'success')
        return redirect(url_for('admin.vagones_tren', tren_id=tren_id))

    return render_template('admin/vagon_insert.html', form=form, tren=tren, title='Nuevo vagón')


@admin.route('/vagones/<int:vagon_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_vagon(vagon_id):
    vagon = Vagon.get_by_id(vagon_id)

    if not vagon:
        flash('El vagón no existe.', 'danger')
        return redirect(url_for('admin.vagones'))

    tren = Tren.get_by_id(vagon.tren_id)

    form = VagonForm(obj=vagon)

    if form.validate_on_submit():
        nombre = form.nombre.data
        filas = form.filas.data
        columnas = form.columnas.data
        estado_vagon = form.estado_vagon.data

        vagon_existe = Vagon.get_by_nombre_and_tren(nombre, vagon.tren_id)

        if vagon_existe and vagon_existe.id != vagon.id:
            flash('Ya existe otro vagón con ese nombre en este tren.', 'danger')
            return render_template('admin/vagon_edit.html', form=form, vagon=vagon, tren=tren, title='Editar vagón')

        Vagon.update(vagon_id, nombre, filas, columnas, estado_vagon)

        flash('Vagón actualizado correctamente.', 'success')
        return redirect(url_for('admin.vagones_tren', tren_id=vagon.tren_id))

    return render_template('admin/vagon_edit.html', form=form, vagon=vagon, tren=tren, title='Editar vagón')


@admin.route('/vagones/<int:vagon_id>/toggle_estado', methods=['POST'])
@login_required
@admin_required
def toggle_vagon_estado(vagon_id):
    vagon = Vagon.get_by_id(vagon_id)

    if not vagon:
        flash('El vagón no existe.', 'danger')
        return redirect(url_for('admin.vagones'))

    Vagon.toggle_estado(vagon_id)

    flash('Estado del vagón actualizado correctamente.', 'success')
    return redirect(url_for('admin.vagones_tren', tren_id=vagon.tren_id))


@admin.route('/viajes')
@login_required
@admin_required
def viajes():
    Viaje.actualizar_estados_automaticos()
    viajes = Viaje.get_all()
    return render_template('admin/viajes.html', viajes=viajes)

@admin.route('/viajes/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_viaje():
    form = ViajeForm()

    trenes_activos = Tren.get_activos()
    estaciones_activas = Estacion.get_activas()

    form.tren_id.choices = [
    (
        tren.id,
        f'{tren.nombre} - {tren.codigo} | Estación: {tren.estacion_actual_nombre or "Sin asignar"}'
    )
    for tren in trenes_activos
    ]

    form.origen_id.choices = [
        (estacion.id, estacion.nombre)
        for estacion in estaciones_activas
    ]

    form.destino_id.choices = [
        (estacion.id, estacion.nombre)
        for estacion in estaciones_activas
    ]

    if form.validate_on_submit():
        tren_id = form.tren_id.data
        origen_id = form.origen_id.data
        destino_id = form.destino_id.data
        fecha_salida = form.fecha_salida.data
        fecha_llegada = form.fecha_llegada.data
        estado_viaje = form.estado_viaje.data

        tren = Tren.get_by_id(tren_id)

        ahora = datetime.now()


        limite_maximo = ahora + timedelta(days=90)

        if fecha_salida < ahora:
            flash('No se puede crear un viaje con fecha de salida en el pasado.', 'danger')
            return render_template('admin/viaje_insert.html', form=form, title='Nuevo viaje')

        if fecha_salida > limite_maximo:
            flash('No se puede crear un viaje con más de 3 meses de antelación.', 'danger')
            return render_template('admin/viaje_insert.html', form=form, title='Nuevo viaje')

        if tren.estacion_actual_id != origen_id:
            flash('El tren seleccionado no se encuentra en la estación de origen.', 'danger')
            return render_template('admin/viaje_insert.html', form=form, title='Nuevo viaje')

        if origen_id == destino_id:
            flash('La estación de origen y destino no pueden ser la misma.', 'danger')
            return render_template('admin/viaje_insert.html', form=form, title='Nuevo viaje')

        if fecha_llegada and fecha_llegada <= fecha_salida:
            flash('La fecha de llegada debe ser posterior a la fecha de salida.', 'danger')
            return render_template('admin/viaje_insert.html', form=form, title='Nuevo viaje')

        Viaje.create(
            tren_id,
            origen_id,
            destino_id,
            fecha_salida,
            fecha_llegada,
            estado_viaje
        )

        flash('Viaje creado correctamente.', 'success')
        return redirect(url_for('admin.viajes'))

    return render_template('admin/viaje_insert.html', form=form, title='Nuevo viaje')

@admin.route('/viajes/<int:viaje_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_viaje(viaje_id):
    viaje = Viaje.get_by_id(viaje_id)

    if not viaje:
        flash('El viaje no existe.', 'danger')
        return redirect(url_for('admin.viajes'))

    form = ViajeForm(obj=viaje)

    trenes_activos = Tren.get_activos()
    tren_actual = Tren.get_by_id(viaje.tren_id)
    estaciones_activas = Estacion.get_activas()

    form.tren_id.choices = [
    (
        tren.id,
        f'{tren.nombre} - {tren.codigo} | Estación: {tren.estacion_actual_nombre or "Sin asignar"}'
    )
    for tren in trenes_activos

]

    if tren_actual and tren_actual.id not in [tren.id for tren in trenes_activos]:
        form.tren_id.choices.append(
            (tren_actual.id, f'{tren_actual.nombre} - {tren_actual.codigo}')
        )

    form.origen_id.choices = [
        (estacion.id, estacion.nombre)
        for estacion in estaciones_activas
    ]

    form.destino_id.choices = [
        (estacion.id, estacion.nombre)
        for estacion in estaciones_activas
    ]

    if form.validate_on_submit():
        tren_id = form.tren_id.data
        origen_id = form.origen_id.data
        destino_id = form.destino_id.data
        fecha_salida = form.fecha_salida.data
        fecha_llegada = form.fecha_llegada.data
        estado_viaje = form.estado_viaje.data

        tren = Tren.get_by_id(tren_id)

        ahora = datetime.now()
        limite_maximo = ahora + timedelta(days=90)

        if estado_viaje == 'programado':

            if fecha_salida < ahora:
                flash('No se puede programar un viaje con fecha de salida en el pasado.', 'danger')
                return render_template('admin/viaje_edit.html', form=form, viaje=viaje, title='Editar viaje')

            if fecha_salida > limite_maximo:
                flash('No se puede programar un viaje con más de 3 meses de antelación.', 'danger')
                return render_template('admin/viaje_edit.html', form=form, viaje=viaje, title='Editar viaje')
            
        if tren.estacion_actual_id != origen_id:
            flash('El tren seleccionado no se encuentra en la estación de origen.', 'danger')
            return render_template('admin/viaje_edit.html', form=form, title='Nuevo viaje')

        if origen_id == destino_id:
            flash('La estación de origen y destino no pueden ser la misma.', 'danger')
            return render_template('admin/viaje_edit.html', form=form, viaje=viaje, title='Editar viaje')

        if fecha_llegada and fecha_llegada <= fecha_salida:
            flash('La fecha de llegada debe ser posterior a la fecha de salida.', 'danger')
            return render_template('admin/viaje_edit.html', form=form, viaje=viaje, title='Editar viaje')

        Viaje.update(
            viaje_id,
            tren_id,
            origen_id,
            destino_id,
            fecha_salida,
            fecha_llegada,
            estado_viaje
        )

        flash('Viaje actualizado correctamente.', 'success')
        return redirect(url_for('admin.viajes'))

    return render_template(
        'admin/viaje_edit.html',
        form=form,
        viaje=viaje,
        title='Editar viaje'
    )

@admin.route('/viajes/<int:viaje_id>/estado', methods=['POST'])
@login_required
@admin_required
def update_estado_viaje(viaje_id):
    estado_viaje = request.form.get('estado_viaje')

    estados_validos = ['programado', 'en_transito', 'finalizado', 'cancelado']

    if estado_viaje not in estados_validos:
        flash('Estado de viaje no válido.', 'danger')
        return redirect(url_for('admin.viajes'))

    Viaje.update_estado(viaje_id, estado_viaje)

    flash('Estado del viaje actualizado correctamente.', 'success')
    return redirect(url_for('admin.viajes'))


@admin.route('/pedidos')
@login_required
@admin_required
def pedidos():
    pedidos = Pedido.get_all()
    return render_template('admin/pedidos.html', pedidos=pedidos)




@admin.route('/pedidos/<int:pedido_id>/estado', methods=['POST'])
@login_required
@admin_required
def update_estado_pedido(pedido_id):
    estado_pedido = request.form.get('estado_pedido')

    estados_validos = [
        'pendiente',
        'aceptado',
        'rechazado',
        'en_transito',
        'entregado',
        'cancelado'
    ]

    if estado_pedido not in estados_validos:
        flash('Estado de pedido no válido.', 'danger')
        return redirect(url_for('admin.pedidos'))

    Pedido.update_estado(pedido_id, estado_pedido)

    flash('Estado del pedido actualizado correctamente.', 'success')
    return redirect(url_for('admin.pedidos'))



@admin.route('/estaciones')
@login_required
@admin_required
def estaciones():
    estaciones = Estacion.get_all()
    return render_template('admin/estaciones.html', estaciones=estaciones)


@admin.route('/estaciones/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_estacion():
    form = EstacionForm()

    if form.validate_on_submit():
        nombre = form.nombre.data
        ciudad = form.ciudad.data
        codigo = form.codigo.data
        estado_estacion = form.estado_estacion.data

        estacion_existe = Estacion.get_by_codigo(codigo)

        if estacion_existe:
            flash('Ya existe una estación con ese código.', 'danger')
            return render_template('admin/estacion_insert.html', form=form, title='Nueva estación')

        Estacion.create(nombre, ciudad, codigo, estado_estacion)

        flash('Estación creada correctamente.', 'success')
        return redirect(url_for('admin.estaciones'))

    return render_template('admin/estacion_insert.html', form=form, title='Nueva estación')


@admin.route('/estaciones/<int:estacion_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_estacion(estacion_id):
    estacion = Estacion.get_by_id(estacion_id)

    if not estacion:
        flash('La estación no existe.', 'danger')
        return redirect(url_for('admin.estaciones'))

    form = EstacionForm(obj=estacion)

    if form.validate_on_submit():
        nombre = form.nombre.data
        ciudad = form.ciudad.data
        codigo = form.codigo.data
        estado_estacion = form.estado_estacion.data

        estacion_existe = Estacion.get_by_codigo(codigo)

        if estacion_existe and estacion_existe.id != estacion.id:
            flash('Ya existe otra estación con ese código.', 'danger')
            return render_template(
                'admin/estacion_edit.html',
                form=form,
                estacion=estacion,
                title='Editar estación'
            )

        Estacion.update(estacion_id, nombre, ciudad, codigo, estado_estacion)

        flash('Estación actualizada correctamente.', 'success')
        return redirect(url_for('admin.estaciones'))

    return render_template(
        'admin/estacion_edit.html',
        form=form,
        estacion=estacion,
        title='Editar estación'
    )


@admin.route('/estaciones/<int:estacion_id>/toggle_estado', methods=['POST'])
@login_required
@admin_required
def toggle_estacion_estado(estacion_id):
    estacion = Estacion.get_by_id(estacion_id)

    if not estacion:
        flash('La estación no existe.', 'danger')
        return redirect(url_for('admin.estaciones'))

    Estacion.toggle_estado(estacion_id)

    flash('Estado de la estación actualizado correctamente.', 'success')
    return redirect(url_for('admin.estaciones'))