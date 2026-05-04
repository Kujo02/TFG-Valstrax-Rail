from flask import Blueprint, render_template, request,redirect, url_for, flash
from flask_login import login_user, logout_user, login_required,current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User
from forms import RegisterForm, LoginForm


auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():

    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    form = RegisterForm()

    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data

        #Comrpobar si el email ya existe.
        if User.get_by_email(form.email.data):
            flash('Email already registered', 'danger')
            return redirect(url_for('auth.register'))

        password_hash = generate_password_hash(password)

        User.create(name, email, password_hash)

        return redirect(url_for('auth.login'))
    
    



    return render_template('register.html', form=form)




@auth.route('/login', methods=['GET', 'POST'])
def login():
    

    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.get_by_email(email)

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('main.home'))
        else:
            flash('Invalid email or password', 'danger')
            return render_template('login.html', form=form, error='Invalid email or password')

    return render_template('login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    
    return redirect(url_for('main.home'))