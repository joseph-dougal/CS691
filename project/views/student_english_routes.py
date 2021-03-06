from flask import render_template, Blueprint, session, request, redirect, url_for, flash
from project.db_utils.models import EnglishAnswer, EnglishTest
from flask_login import login_required, current_user
from project.db_utils.login_model import User
from project import db
import pandas as pd


# Display all columns in Pycharm
desired_width = 320
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns', 20)
pd.set_option('display.max_rows', 100000)

student_english_routes = Blueprint('student_english_routes', __name__)


def clean_df(df):
    """
    utility to clean results before displaying in UI
    """
    # fill na's with empty string
    df = df.fillna('')
    # filter only columns we want to see in the UI
    df = df[['question_id', 'question_x', 'create_date', 'answer']]
    # update naming convention to be UI friendly
    df = df.rename(columns={'question_id': 'Number', 'question_x': 'Question', 'create_date': 'Create Date',
                            'answer': 'Answer'})
    return df


@student_english_routes.route('/student-english-question', methods=['GET', 'POST'])
@login_required
def home():

    """
    The /student-english-question route is used as a home page for the student to see questions and submit answers
    """
    if request.method == 'POST':
        # variables submitted by form
        question_id = request.form['question_id']
        user_id = current_user.user_id
        question = request.form['question']
        answer = request.form['answer']

        # check if the user submitted an answer and update if they did
        obj = db.session.query(EnglishAnswer).filter_by(question_id=question_id, user_id=user_id).first()
        if not obj:
            new_object = EnglishAnswer(question_id, user_id, question, answer)
            db.session.add(new_object)
            db.session.commit()
        else:
            obj.answer = answer
            db.session.commit()
        flash('Answer Submitted', 'success')
        return redirect(url_for('student_english_routes.home'))
    else:
        # get math questions & answer df's join to display current answers
        df_test = pd.read_sql(db.session.query(EnglishTest).statement, db.engine, parse_dates=True)
        user_id = current_user.user_id
        df_answer = pd.read_sql(db.session.query(EnglishAnswer).filter_by(user_id=user_id).statement, db.engine,
                                parse_dates=True)
        # left join to get all questions and answers if they exists
        df = df_test.merge(df_answer, how='left', on='question_id')
        df = clean_df(df)
        user = User.query.filter_by(user_id=current_user.user_id).first()
        return render_template('pages/student-english.html', data=df, account=user.account)


