from flask import Flask, render_template, request
import os
from config import config

app = Flask(__name__)

app.config.from_object(config['development'])



if __name__ == '__main__':
    app.run(debug=True)