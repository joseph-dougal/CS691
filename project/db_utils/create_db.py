from project.db_utils.login_model import User
from project import db


def db_setup():
    # db.drop_all()
    db.create_all()
    db.session.commit()


# def db_insert():
#
#     new_obj = User('jd.com', b'123')
#     db.session.add(new_obj)
#     db.session.commit()


if __name__ == '__main__':
    db_setup()
    # db_insert()
