# backup in case the current URI doesn't work
# from os import environ, path
# database_uri = f'sqlite:///{path.abspath(path.dirname(__file__))}\\sqlite-db.db'

DEBUG = True
FLASK_ENV = 'development'
SECRET_KEY = 'JD_12345'
SQLALCHEMY_DATABASE_URI = "sqlite:///sqlite-db.db"
SQLALCHEMY_TRACK_MODIFICATIONS = False
