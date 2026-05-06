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

app = Flask(__name__)

app.config.from_object(config['development'])

mysql.init_app(app)

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

if __name__ == '__main__':
    app.run(debug=True)