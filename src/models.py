import datetime

from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug import security

from database import db


class Instructor(db.Model, UserMixin):
    __tablename__ = "Instructor"
    owner_id = db.Column(db.Integer(), autoincrement=True, primary_key=True)
    # owner_domain = db.Column(db.UnicodeText(), nullable=False)
    owner_first = db.Column(db.UnicodeText(), nullable=False)
    owner_last = db.Column(db.UnicodeText(), nullable=False)
    email = db.Column(db.Unicode(256), nullable=False)
    password_hash = db.Column(db.String(128))
    active = db.Column(db.Boolean(), default=False)

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

    def get_id(self):
        return self.email

    @property
    def is_active(self):
        return self.active

    def activate(self):
        self.active = True

    def __repr__(self):
        return str(self.owner_first) + " " + str(self.owner_last)


class AccessToken(db.Model):
    __tablename__ = "AccessToken"
    code = db.Column(db.String(), primary_key=True)
    owner_id = db.Column(db.Integer(), db.ForeignKey("Instructor.owner_id"))
    time_start = db.Column(db.DateTime(), nullable=False, default=datetime.datetime.utcnow)
    time_end = db.Column(db.DateTime())
    valid_domain = db.Column(db.String(), nullable=False)

    # determines if an access token has expired
    @hybrid_property
    def is_expired(self):
        now = datetime.datetime.utcnow()
        return now > self.time_end

    # determines if an access token is valid yet
    @hybrid_property
    def is_valid(self):
        now = datetime.datetime.utcnow()
        return now < self.time_start

    @classmethod
    def can_access(cls, code: str, email: str):
        if code is None or email is None:
            print("Either code or email is None")
            return False
        token = AccessToken.query.filter_by(code=code).first()
        if token is None:
            print("Token doesn't exist")
            return False
        email_domain = email.split('@')[1]
        return token.valid_domain == email_domain
