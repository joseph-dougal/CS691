from flask import render_template, Blueprint, session, request, redirect, url_for, flash
from project.db_utils.models import MathTest
from flask_login import login_required
from sqlalchemy import exc
from project import db
import pandas as pd


teacher_routes = Blueprint('teacher_routes', __name__)


@teacher_routes.route('/teacher-math-question', methods=['GET', 'POST'])
def home():

    """
    The /teacher-math-question route is used as a home page for the teacher to edit questions
    :return:
    """

    if request.method == 'POST':
        user_id = 5
        question = request.form['question']
        new_object = MathTest(user_id, question)
        db.session.add(new_object)
        db.session.commit()
        flash('New Question Added', 'success')
        return redirect(url_for('teacher_routes.home'))
    else:
        df = pd.read_sql(db.session.query(MathTest).statement, db.engine, parse_dates=True)
        df = df.rename(columns={'question_id': 'Number', 'user_id': 'User ID', 'question': 'Question',
                                'create_date': 'Create Date', 'update_time': 'Update Time'})
        return render_template('pages/teacher-math.html', data=df)


@teacher_routes.route('/delete', methods=['GET', 'POST'])
def delete():

    """
    The /delete route is used to manually delete records from the DB
    :return:
    """

    if request.method == 'POST':

        question_id = request.form['question_id']
        try:
            obj = MathTest.query.filter_by(question_id=question_id).one()
            db.session.delete(obj)
            db.session.commit()
            message = 'Question ID {} Deleted'.format(question_id)
            flash(message, 'success')
            return redirect(url_for('teacher_routes.home'))
        except exc.SQLAlchemyError as err:
            message = 'Error Deleting Question ID \n' + str(err)
            flash(message, 'danger')
            return redirect(url_for('teacher_routes.home'))

