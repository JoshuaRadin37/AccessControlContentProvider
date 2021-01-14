import datetime

from flask_login import UserMixin
from werkzeug import security

from database import db


class Instructor(db.Model, UserMixin):
    __tablename__ = "Instructor"
    owner_id = db.Column(db.Integer(), autoincrement=True)
    # owner_domain = db.Column(db.UnicodeText(), nullable=False)
    owner_first = db.Column(db.UnicodeText(), nullable=False)
    owner_last = db.Column(db.UnicodeText(), nullable=False)
    email = db.Column(db.Unicode(256), nullable=False, primary_key=True)
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

    def get_id(self):
        return self.owner_id


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
