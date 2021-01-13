import datetime
from random import randint

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug import security

db = SQLAlchemy()


class Instructor(db.Model, UserMixin):
    __tablename__ = "Instructor"
    owner_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    # owner_domain = db.Column(db.UnicodeText(), nullable=False)
    owner_first = db.Column(db.UnicodeText(), nullable=False)
    owner_last = db.Column(db.UnicodeText(), nullable=False)
    email = db.Column(db.Unicode(256), nullable=False, unique=True)
    password_hash = db.Column(db.String(128))

    def access_tokens(self):
        return AccessToken.query.filter(owner_id=self.owner_id)

    @property
    def password(self):
        raise AttributeError("password is write only")

    @password.setter
    def password(self, password):
        self.password_hash = security.generate_password_hash(password)

    def verify_password(self, password):
        return security.check_password_hash(self.password_hash, password)

    @classmethod
    def get(cls, user_id):
        return cls.query.filter_by(owner_id=user_id).first()


class AccessToken(db.Model):
    __tablename__ = "AccessToken"
    code = db.Column(db.String(), primary_key=True)
    owner_id = db.Column(db.Integer(), db.ForeignKey("Instructor.owner_id"))
    time_start = db.Column(db.DateTime(), nullable=False, default=datetime.datetime.utcnow)
    time_end = db.Column(db.DateTime())

    # determines if an access token has expired
    def is_expired(self):
        now = datetime.datetime.utcnow()
        return now > self.time_end

    # determines if an access token is valid yet
    def is_valid(self):
        now = datetime.datetime.utcnow()
        return now < self.time_start


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


