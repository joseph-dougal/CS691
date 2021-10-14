"""Flask configuration."""

DEBUG = True
FLASK_ENV = 'development'
SECRET_KEY = 'JD_12345'
SQLALCHEMY_DATABASE_URI = "sqlite:///sqlite-db.db"
SQLALCHEMY_TRACK_MODIFICATIONS = False