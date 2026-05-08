from flask import Blueprint, render_template,redirect, url_for, request, flash
from flask_login import current_user
from models.user import User

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