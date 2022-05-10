from flask import render_template, Blueprint, redirect, url_for, flash, request, make_response
# from project.nlp_logic.question_parser import gen_answer_list, print_answers, grade_response
from project.db_utils.models import MathAnswer, MathTest, EnglishTest, EnglishAnswer
from flask_login import login_required, current_user
# from transformers import BertForQuestionAnswering
from project.db_utils.login_model import User
# from transformers import BertTokenizer
# import spacy
from project import db
import pandas as pd


home_routes = Blueprint('home_routes', __name__)


def get_user_info(account):

    """
    gets test & answer results from the db for teachers and students
    """
    df_test = pd.read_sql(db.session.query(MathTest).statement, db.engine, parse_dates=True)
    # display all answers
    if account == 'teacher':
        df_answer = pd.read_sql(db.session.query(MathAnswer).statement, db.engine, parse_dates=True)
    # display students answers
    else:
        df_answer = pd.read_sql(db.session.query(MathAnswer).filter_by(user_id=current_user.user_id).statement,
                                db.engine, parse_dates=True)
    df = df_test.merge(df_answer, how='left', on='question_id')
    try:
        # check if answers are correct
        df.loc[df['correct_answer'] == df['answer'], 'correct'] = True
        df.loc[df['correct_answer'] != df['answer'], 'correct'] = False

        # calculate grade
        # df['grade'] = df['correct'].count(True) / df['correct'].count(False)
        # df['grade'] = df['grade'] * 100
    except ValueError:
        df['correct'] = None
    df = clean_df(df)
    return df


def clean_df(df):
    """
    utility to clean results before displaying in UI
    """
    # fill na's with empty string
    df = df.fillna('')
    # filter only columns we want to see in the UI
    df = df[['question_id', 'user_id_x', 'question_x', 'expression', 'correct_answer', 'answer', 'correct']]
    # update naming convention to be UI friendly
    df = df.rename(columns={'question_id': 'Number', 'user_id_x': 'User ID', 'question_x': 'Question',
                            'expression': 'Expression', 'correct_answer': 'Correct Answer', 'answer': 'Answer',
                            'correct': 'Correct'})
    return df


def get_english_results(account):
    """
    gets test & answer results from the db for teachers and students
    """
    df_test = pd.read_sql(db.session.query(EnglishTest).statement, db.engine, parse_dates=True)
    # display all answers
    if account == 'teacher':
        df_answer = pd.read_sql(db.session.query(EnglishAnswer).statement, db.engine, parse_dates=True)
    # display students answers
    else:
        df_answer = pd.read_sql(db.session.query(EnglishAnswer).filter_by(user_id=current_user.user_id).statement,
                                db.engine, parse_dates=True)

    df = df_test.merge(df_answer, how='left', on='question_id')
    # df = check_answers(df)
    df = clean_english_df(df)
    return df


# def check_answers(df):
#
#     df[['answer']] = df[['answer']].fillna('not answered yet')
#
#     for i, row in df.iterrows():
#         question = row['question_x']
#         user_answer = row['answer']
#         text = open('project/nlp_logic/input_text.txt', 'r')
#         text = text.read()
#         nlp = spacy.load('en_core_web_sm')
#         answer_list = gen_answer_list(text, question, nlp, par_len=9)
#         df['correct_answer'] = str(answer_list).strip('[]')
#         x = grade_response(user_answer, answer_list, nlp, limit=10)
#         df['Correct'] = x
#
#     return df


def clean_english_df(df):
    df['Correct'] = ' '
    df = df.rename(columns={'question_id': 'Number', 'id': 'User ID', 'question_x': 'Question',
                            'correct_answer': 'Correct Answer', 'answer': 'Answer'})
    df = df[['Number', 'User ID', 'Question', 'Correct Answer', 'Answer', 'Correct']]
    return df


@home_routes.route('/home', methods=["GET"])
@login_required
def home():

    """
    Home route gets users info from the DB based on Flask login's current_user ID
    """
    if current_user.is_authenticated:
        user = User.query.filter_by(user_id=current_user.user_id).first()
        df = get_user_info(user.account)
        return render_template('pages/home.html', data=df, account=user.account)
    else:
        return redirect(url_for('utility_routes.index'))


@home_routes.route('/report', methods=["GET"])
@login_required
def report():

    """
    Home route gets users info from the DB based on Flask login's current_user ID
    """
    if current_user.is_authenticated:
        user = User.query.filter_by(user_id=current_user.user_id).first()
        df_math = get_user_info(user.account)
        df_english = get_english_results(user.account)
        return render_template('pages/report.html', math_data=df_math, english_data=df_english, account=user.account)
    else:
        return redirect(url_for('utility_routes.index'))


@home_routes.route('/billing', methods=["GET"])
@login_required
def billing():

    """
    Home route gets users info from the DB based on Flask login's current_user ID
    """
    if current_user.is_authenticated:
        user = User.query.filter_by(user_id=current_user.user_id).first()
        df = get_user_info(user.account)
        return render_template('pages/billing.html', data=df, account=user.account)
    else:
        return redirect(url_for('utility_routes.index'))


@home_routes.route('/support', methods=["GET"])
@login_required
def support():

    """
    Home route gets users info from the DB based on Flask login's current_user ID
    """
    if current_user.is_authenticated:
        user = User.query.filter_by(user_id=current_user.user_id).first()
        df = get_user_info(user.account)
        return render_template('pages/support.html', data=df, account=user.account)
    else:
        return redirect(url_for('utility_routes.index'))


@home_routes.route('/download', methods=['POST'])
@login_required
def download():

    """
    The /download route is used to create a DB export
    :return:
    """
    export_type = request.form['export_type']

    try:
        if request.method == 'POST' and export_type == 'export_data':
            user = User.query.filter_by(user_id=current_user.user_id).first()
            df = get_user_info(user.account)
            output = make_response(df.to_csv(index=False))
            output.headers["Content-Disposition"] = f'attachment; filename={"test_results"}.csv'
            output.headers["Content-type"] = "text/csv"
            return output
    except Exception as err:
        message = 'Error exporting data \n' + str(err)
        flash(message, 'danger')
        return render_template('home_routes.home')
