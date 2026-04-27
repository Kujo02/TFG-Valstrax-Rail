from flask import Blueprint, render_template, request,redirect, url_for
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    pass



@auth.route('/login', methods=['GET', 'POST'])
def login():
    pass


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))