import datetime
from functools import wraps

import flask
from flask import Blueprint, render_template, flash, redirect, url_for, request, current_app, abort, make_response
from flask_login import LoginManager, current_user, login_user, login_required, logout_user

from database import db, generate_token
from forms import NewInstructorForm, LoginForm, NewTokenForm, GetAccessForm
from models import Instructor, AccessToken
from security import is_safe_url

user_management = Blueprint('user_management', __name__, template_folder='../templates', )


def initiate_user_functionality(app):
    """
    Initializes the user routes
    :param app: The flask application
    """
    app.register_blueprint(user_management)


@user_management.route('/logout', methods=["GET", "POST"])
@login_required
def logout():
    """
    Logs out the user.
    Must be logged in to access this page, enforced by flask-login.
    :return: A redirect back to the index page
    """
    logout_user()
    return redirect(url_for("index"))


@user_management.route('/login', methods=["GET", "POST"])
def login():
    """
    The login page
    :return: A HTTPS request
    """
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        with current_app.app_context():
            instructor = Instructor.query.filter_by(email=email).first()

            if instructor is not None and instructor.verify_password(password):
                print("logging in", instructor)
                if not login_user(instructor, remember=True, force=True):
                    print("Failed to log in user")

                next = flask.request.args.get("next")
                if not is_safe_url(next):
                    return flask.abort(400)

                return redirect(next or url_for("index"))
            else:
                print("Not a valid login")
                flash("Email or password is invalid")
    else:
        for error in form.errors:
            flash(error)
    return render_template("login.html", form=form)


@user_management.route('/register', methods=["GET", "POST"])
def register():
    """
    The user registration page
    :return: A HTTPS request
    """
    form = NewInstructorForm(request.form)
    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        password = form.password.data
        if Instructor.query.filter_by(email=email).first() is None:
            instructor = Instructor(owner_first=first_name, owner_last=last_name, email=email, password=password)
            db.session.add(instructor)
            db.session.commit()
            login_user(instructor, remember=False)
            next = flask.request.args.get("next")
            if not is_safe_url(next):
                return flask.abort(400)

            return redirect(next or url_for("index"))
        else:
            flash("User with this email already exists")
    else:
        for error in form.errors:
            flash(error)

    return render_template("register.html", form=form)


@user_management.route('/tokens', methods=["GET", "POST"])
@login_required
def profile():
    """
    The page where instructors can see their profile
    :return: A HTTPS request
    """
    tokens = AccessToken.query.filter(AccessToken.is_valid).all()
    if tokens is None:
        return flask.abort(400)
    form = NewTokenForm()
    if form.validate_on_submit():
        start_time = form.start_time.data
        end_time = form.end_time.data
        valid_domain = form.valid_domain.data

        code = generate_token(current_app, current_user.get_id(), valid_domain, start_time, end_time)
        return redirect(url_for('user_management.profile'))
    else:
        for error in form.errors:
            flash(error)

    return render_template("profile.html", active_tokens=tokens, form=form)


@user_management.route('/student_login', methods=["GET", "POST"])
def student_login():
    """
    The page where students must input their access codes
    :return: A HTTPS request
    """
    access_code = request.cookies.get('code')
    email = request.cookies.get('email')

    last_page = request.cookies.get('last_page')

    if AccessToken.can_access(access_code, email):
        return redirect(last_page or url_for("table_of_contents"))

    form = GetAccessForm()
    if form.validate_on_submit():
        email = form.email.data
        code = form.access_code.data

        if AccessToken.can_access(code, email):

            resp = make_response(redirect(last_page or url_for("table_of_contents")))
            #expire_date = datetime.datetime.now()
            #expire_date = expire_date + datetime.timedelta(hours=1)
            resp.set_cookie('code', code, max_age=60 * 60 * 3)
            resp.set_cookie('email', email, max_age=60 * 60 * 3)

            return resp
        else:
            flash("Not a valid access code or email for access code")
    else:
        # flash("form invalid")
        for error in form.errors:
            flash(error)

    return render_template("get_access.html", form=form)


# Checks if the current user has this permission
def permission_required(permission):
    return permissions_required(permission)


# Checks if the current user has all required permissions
def permissions_required(*permissions):
    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            for permission in permissions:
                if not current_user.has_permission(permission):
                    abort(403)

            return func(*args, **kwargs)

        return decorated_function

    return decorator