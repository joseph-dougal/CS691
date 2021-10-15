from flask import render_template, Blueprint

utility_routes = Blueprint('utility_routes', __name__)

@utility_routes.route('/', methods=["GET"])
def index():
    return render_template('index.html')

@utility_routes.route('/home', methods=["GET"])
def home():
    return render_template('pages/home.html')

@utility_routes.route('/blank', methods=["GET"])
def blank():
    return render_template('pages/blank.html')

@utility_routes.route('/error', methods=["GET"])
def error():
    return render_template('pages/404.html')

@utility_routes.route('/unauthorized', methods=["GET"])
def unauthorized():
    return render_template('pages/401.html')
