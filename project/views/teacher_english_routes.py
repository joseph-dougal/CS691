from flask import render_template, Blueprint, request, redirect, url_for, flash
from project.db_utils.models import MathTest, EnglishTest
from flask_login import login_required, current_user
from project.db_utils.login_model import User
from datetime import datetime
from sqlalchemy import exc
from project import db
import pandas as pd

from project.math_logic.equation_builder import MathExpression

teacher_english_routes = Blueprint('teacher_english_routes', __name__)


@teacher_english_routes.route('/teacher-english-question', methods=['GET', 'POST'])
@login_required
def home():

    """
    The /teacher-math-question route is used as a home page for the teacher to edit questions
    :return:
    """

    if request.method == 'POST':
        user_id = current_user.user_id
        question = request.form['question']
        new_object = EnglishTest(user_id, question)
        db.session.add(new_object)
        db.session.commit()
        flash('New Question Added', 'success')
        return redirect(url_for('teacher_english_routes.home'))
    else:
        df = pd.read_sql(db.session.query(EnglishTest).statement, db.engine, parse_dates=True)
        df = df.rename(columns={'question_id': 'Number', 'user_id': 'User ID', 'question': 'Question',
                                'create_date': 'Create Date', 'update_time': 'Update Time'})
        df = df[['Number', 'User ID', 'Create Date', 'Update Time', 'Question']]

        text = open('project/nlp_logic/input_text.txt', 'r')
        text = text.read()
        user = User.query.filter_by(user_id=current_user.user_id).first()
        return render_template('pages/teacher-english.html', data=df, text=text, account=user.account)


@teacher_english_routes.route('/teacher-english-edit', methods=['GET', 'POST'])
@login_required
def edit():

    """
    The /edit route is used to create equation details
    :return:
    """

    if request.method == 'POST':

        # default (need to get this from user login details)
        question_id = request.form['question_id']
        user_id = request.form['user_id']
        question = request.form['question']
        print(question_id, user_id, question)
        try:
            # check if the user submitted an answer and update if they did
            obj = db.session.query(EnglishTest).filter_by(question_id=question_id, user_id=user_id).first()

            # commit the string value to the DB
            obj.question = question
            db.session.commit()

            flash('Question Updated', 'success')
            return redirect(url_for('teacher_english_routes.home'))
        except exc.SQLAlchemyError as err:
            print(err)
            message = 'Error Updating Question \n' + str(err)
            flash(message, 'danger')
            return redirect(url_for('teacher_english_routes.home'))


@teacher_english_routes.route('/delete-english-question', methods=['GET', 'POST'])
@login_required
def delete():

    """
    The /delete route is used to manually delete records from the DB
    :return:
    """

    if request.method == 'POST':

        question_id = request.form['question_id']
        try:
            obj = EnglishTest.query.filter_by(question_id=question_id).one()
            db.session.delete(obj)
            db.session.commit()
            message = 'Question ID {} Deleted'.format(question_id)
            flash(message, 'success')
            return redirect(url_for('teacher_english_routes.home'))
        except exc.SQLAlchemyError as err:
            message = 'Error Deleting Question ID \n' + str(err)
            flash(message, 'danger')
            return redirect(url_for('teacher_english_routes.home'))

