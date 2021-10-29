from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import flask

app = flask.Flask(__name__)
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login_routes.login'

# We need to import the routes after the DB is instantiated
from project.views.utility_routes import utility_routes
from project.views.teacher_routes import teacher_routes
from project.views.student_routes import student_routes
from project.views.login_routes import login_routes
from project.db_utils.login_model import User
app.register_blueprint(utility_routes)
app.register_blueprint(teacher_routes)
app.register_blueprint(student_routes)
app.register_blueprint(login_routes)


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.user_id == int(user_id)).first()


@app.errorhandler(404)
def handle_404(e):
    return flask.render_template('pages/404.html')


@app.errorhandler(401)
def handle_401(e):
    return flask.render_template('pages/401.html')
