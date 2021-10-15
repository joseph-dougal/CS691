from flask import render_template, Blueprint, session, request, redirect, url_for, flash
from project.db_utils.models import MathAnswer, MathTest
from flask_login import login_required
from sqlalchemy import exc
from project import db
import pandas as pd


student_routes = Blueprint('student_routes', __name__)


@student_routes.route('/student-math-question', methods=['GET', 'POST'])
def home():

    if request.method == 'POST':
        question_id = request.form['question_id']
        user_id = 10
        question = request.form['question']
        answer = request.form['answer']
        print(question_id, question, answer)
        # new_object = MathAnswer(question_id, user_id, question, answer)
        # db.session.add(new_object)
        # db.session.commit()
        flash('Answer Submitted', 'success')
        return redirect(url_for('student_routes.home'))
    else:
        df = pd.read_sql(db.session.query(MathTest).statement, db.engine, parse_dates=True)
        df = df[['question_id', 'question']]
        df = df.rename(columns={'question_id': 'Number', 'question': 'Question'})
        return render_template('pages/student-math.html', data=df)


# @student_routes.route('/answer-update', methods=['GET', 'POST'])
# def delete():
#
#     """
#     The /answer-update route is used to add student answers to the DB
#     :return:
#     """
#
#     if request.method == 'POST':
#
#         user_id = 10
#         question_id = request.form['question_id']
#         question = request.form['question']
#         answer = request.form['answer']
#
#         try:
#             obj = MathTest.query.filter_by(question_id=question_id).one()
#             db.session.delete(obj)
#             db.session.commit()
#             message = 'Question ID {} Deleted'.format(question_id)
#             flash(message, 'success')
#             return redirect(url_for('teacher_routes.home'))
#         except exc.SQLAlchemyError as err:
#             message = 'Error Deleting Question ID \n' + str(err)
#             flash(message, 'danger')
#             return redirect(url_for('teacher_routes.home'))
