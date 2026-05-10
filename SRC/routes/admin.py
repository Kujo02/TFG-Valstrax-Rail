from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from functools import wraps
from models.user import User
from models.tren import Tren
from forms import TrenForm

admin = Blueprint('admin', __name__, url_prefix='/admin')


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        

        if current_user.role != "admin":
            flash('No tienes permisos para acceder a esta página.', 'danger')
            return redirect(url_for('main.home'))

        return f(*args, **kwargs)

    return decorated_function


@admin.route('/dashboard')
@login_required
@admin_required
def dashboard():
    return render_template('admin/dashboard.html')


@admin.route('/users')
@login_required
@admin_required
def users():
    users = User.get_all()

    return render_template('admin/users.html ', users=users)



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

    if form.validate_on_submit():
        nombre = form.nombre.data
        codigo = form.codigo.data
        estado_tren = form.estado_tren.data

        tren_existe = Tren.get_by_codigo(codigo)

        if tren_existe:
            flash('Ya existe un tren con ese código.', 'danger')
            return render_template('admin/tren_insert.html', form=form, title='Nuevo tren')

        Tren.create(nombre, codigo, estado_tren)

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

    if form.validate_on_submit():
        nombre = form.nombre.data
        codigo = form.codigo.data
        estado_tren = form.estado_tren.data

        tren_existe = Tren.get_by_codigo(codigo)

        if tren_existe and tren_existe.id != tren.id:
            flash('Ya existe otro tren con ese código.', 'danger')
            return render_template('admin/tren_edit.html', form=form, tren=tren, title='Editar tren')

        Tren.update(tren_id, nombre, codigo, estado_tren)

        flash('Tren actualizado correctamente.', 'success')
        return redirect(url_for('admin.trenes'))

    return render_template('admin/tren_edit.html', form=form, tren=tren, title='Editar tren')