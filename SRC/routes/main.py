from flask import Blueprint, render_template,redirect, url_for
from flask_login import current_user

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