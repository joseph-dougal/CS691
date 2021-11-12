from datetime import datetime
from project import db


class MathTest(db.Model):

    __tablename__ = 'math_test'
    __table_args__ = {'extend_existing': True}
    question_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=True)
    question = db.Column(db.String(250), nullable=True)
    expression = db.Column(db.String(250), nullable=True)
    create_date = db.Column(db.Date, nullable=True)
    update_time = db.Column(db.DateTime, nullable=True)

    def __init__(self, user_id, question, expression=None, create_date=None, update_time=None):
        # format the timestamp and cast the string into a datetime object
        current_date = datetime.now().strftime('%Y-%m-%d')
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        self.user_id = user_id
        self.question = question
        self.expression = expression
        if create_date is None:
            self.create_date = datetime.strptime(current_date, '%Y-%m-%d')
        else:
            self.create_date = create_date
        if update_time is None:
            self.update_time = datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S')
        else:
            self.update_time = update_time


class MathAnswer(db.Model):

    __tablename__ = 'math_answer'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question_id = db.Column(db.Integer, nullable=True)
    user_id = db.Column(db.Integer, nullable=True)
    question = db.Column(db.String(250), nullable=True)
    answer = db.Column(db.String(250), nullable=True)
    update_time = db.Column(db.DateTime, nullable=True)

    def __init__(self, question_id, user_id, question, answer, update_time=None):
        # format the timestamp and cast the string into a datetime object
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        self.question_id = question_id
        self.user_id = user_id
        self.question = question
        self.answer = answer
        if update_time is None:
            self.update_time = datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S')
        else:
            self.update_time = update_time


db.create_all()
db.session.commit()