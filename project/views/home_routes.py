from flask import render_template, Blueprint, redirect, url_for, flash
from flask_login import login_required, current_user
from project.db_utils.models import MathAnswer, MathTest
from project import db
import pandas as pd
from project.math_logic.equation_builder import MathExpression


home_routes = Blueprint('home_routes', __name__)


@home_routes.route('/home', methods=["GET"])
@login_required
def home():
    if current_user.is_authenticated:

        df = pd.read_sql(db.session.query(MathTest).statement, db.engine, parse_dates=True)
        print(df)
        return render_template('pages/home.html', data=df)
    else:
        return redirect(url_for('utility_routes.index'))
