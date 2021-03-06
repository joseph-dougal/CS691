from flask import render_template, Blueprint
from project import app
from os import listdir
import os

utility_routes = Blueprint('utility_routes', __name__)


@utility_routes.route('/', methods=["GET"])
def index():
    carousel = [f for f in listdir(f'{os.path.join(app.root_path)}/static/img/carousel')]
    return render_template('index.html', carousel=carousel)


@utility_routes.route('/educators_h', methods=["GET"])
def index_ed():
    return render_template('index-educators.html')


@utility_routes.route('/blank', methods=["GET"])
def blank():
    return render_template('pages/blank.html')


@utility_routes.route('/error', methods=["GET"])
def error():
    return render_template('pages/404.html')


@utility_routes.route('/unauthorized', methods=["GET"])
def unauthorized():
    return render_template('pages/401.html')

