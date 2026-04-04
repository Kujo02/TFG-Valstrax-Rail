from flask import Flask, render_template, request
import os
from config import config


from routes.main import main



app = Flask(__name__)

app.config.from_object(config['development'])

app.register_blueprint(main)

if __name__ == '__main__':
    app.run(debug=True)