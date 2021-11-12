from flask import render_template, Blueprint, session, request, redirect, url_for, flash
from project.db_utils.models import MathTest
from flask_login import login_required
from sqlalchemy import exc
from project import db
import pandas as pd

from project.math_logic.equation_builder import MathExpression

teacher_routes = Blueprint('teacher_routes', __name__)


@login_required
@teacher_routes.route('/teacher-math-question', methods=['GET', 'POST'])
def home():

    """
    The /teacher-math-question route is used as a home page for the teacher to edit questions
    :return:
    """

    if request.method == 'POST':
        user_id = 5
        question = request.form['question']
        question = MathExpression(question)
        question = question.expression_string

        new_object = MathTest(user_id, question)

        db.session.add(new_object)
        db.session.commit()
        flash('New Question Added', 'success')
        return redirect(url_for('teacher_routes.home'))
    else:
        df = pd.read_sql(db.session.query(MathTest).statement, db.engine, parse_dates=True)
        df = df.rename(columns={'question_id': 'Number', 'user_id': 'User ID', 'question': 'Question',
                                'create_date': 'Create Date', 'update_time': 'Update Time',
                                'expression': 'Expression (Ex: 1, None, 2.3)'})
        df = df[['Number', 'User ID', 'Question', 'Create Date', 'Update Time', 'Expression (Ex: 1, None, 2.3)']]
        return render_template('pages/teacher-math.html', data=df)


@login_required
@teacher_routes.route('/teacher-math-edit', methods=['GET', 'POST'])
def edit():

    """
    The /edit route is used to create equation details
    :return:
    """

    if request.method == 'POST':

        # default (need to get this from user login details)
        question_id = request.form['question_id']
        user_id = request.form['user_id']
        expression = request.form['expression']

        try:
            # check if the user submitted an answer and update if they did
            obj = db.session.query(MathTest).filter_by(question_id=question_id, user_id=user_id).first()

            # call the MathExpression class with the question created by the user
            question = obj.question
            question = MathExpression(question)

            # convert string to list of int, float, or None type
            new_expression = []
            result = [x.strip() for x in expression.split(',')]
            for x in result:
                if x.isnumeric():
                    new_expression.append(int(x))
                elif x.replace('.', '', 1).isdigit():
                    new_expression.append(float(x))
                else:
                    new_expression.append(None)

            # call the replace_variables() function to generate the expression
            question.replace_variables(new_expression)

            # commit the string value to the DB
            obj.expression = question.expression_string
            db.session.commit()

            flash('Expression Updated', 'success')
            return redirect(url_for('teacher_routes.home'))
        except exc.SQLAlchemyError as err:
            message = 'Error Updating Expression \n' + str(err)
            flash(message, 'danger')
            return redirect(url_for('teacher_routes.home'))


@login_required
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

