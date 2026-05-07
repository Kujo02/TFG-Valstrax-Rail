from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from functools import wraps
from models.user import User

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