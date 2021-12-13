# test db setup
import os
project_dir = os.path.dirname(os.path.abspath(__file__))
SQLALCHEMY_DATABASE_URI = "sqlite:///{}".format(os.path.join(project_dir, "sqlite-db.db"))


DEBUG = True
FLASK_ENV = 'development'
SECRET_KEY = 'JD_12345'
# SQLALCHEMY_DATABASE_URI = 'postgresql://ubuntu:cs#691@ec2-54-145-120-193.compute-1.amazonaws.com/postgres'
SQLALCHEMY_TRACK_MODIFICATIONS = False
