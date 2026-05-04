from flask import Blueprint, render_template, request,redirect, url_for

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return redirect(url_for('main.home'))

@main.route('/home')
def home():
    
    return render_template('home.html')