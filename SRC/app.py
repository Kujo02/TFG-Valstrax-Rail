from flask import Flask, render_template, request
import os
from config import config
from flask_login import LoginManager
from DB.db import mysql
from routes.main import main
from routes.auth import auth
from routes.admin import admin
from models.user import User
from flask_wtf import CSRFProtect
from extensions import mail

app = Flask(__name__)

app.config.from_object(config['development'])



mysql.init_app(app)
mail.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

csrf = CSRFProtect(app)
app.register_blueprint(main)
app.register_blueprint(auth)    
app.register_blueprint(admin)
@login_manager.user_loader
def load_user(user_id):
    
    return User.get_by_id(user_id)


@app.errorhandler(404)
def pagina_no_encontrada(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(403)
def acceso_denegado(error):
    return render_template('errors/403.html'), 403


@app.errorhandler(500)
def error_servidor(error):
    return render_template('errors/500.html'), 500


# @app.route('/probar-500')
# def probar_500():
#     raise Exception('Error de prueba 500')


if __name__ == '__main__':
    app.run(debug=True)