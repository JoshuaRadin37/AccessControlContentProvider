import datetime
from random import randint

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug import security


db = SQLAlchemy()


def initialize_db(app):
    global db
    db.init_app(app)
    with app.app_context():
        db.create_all()


def __generate_access_code(length):
    code = ""
    for _ in range(0, length):
        initial = randint(0, 26 + 10 - 1)  # A-Z and 0-9
        if initial < 26:
            next = str('A' + initial)
        else:
            next = str(initial - 26)
        code += next

    return code


# Generates an access control token, and returns the string
def generate_token(app, owner_id, expiration_date, start_date=None, length=16):
    from models import AccessToken
    with app.app_context():
        while True:
            access_code = __generate_access_code(length)
            if AccessToken.query.filter_by(code=access_code).first() is None:
                break

        if start_date is None:
            token = AccessToken(access_code, owner_id, time_end=expiration_date)
        else:
            token = AccessToken(access_code, owner_id, time_start=start_date, time_end=expiration_date)
        db.session.add(token)
        return access_code


