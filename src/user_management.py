import flask
from flask import Blueprint, render_template, flash, redirect, url_for, request, current_app
from flask_login import LoginManager, current_user, login_user, login_required

from database import db
from forms import NewInstructorForm, LoginForm
from models import Instructor, AccessToken
from security import is_safe_url

user_management = Blueprint('user_management', __name__, template_folder='../templates', )


def initiate_user_functionality(app):
    app.logger.info('initializing user management')
    app.register_blueprint(user_management)


@user_management.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    print("Attempting log in")
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        with current_app.app_context():
            instructor = Instructor.query.filter_by(email=email).first()
            print(instructor)
            if instructor is not None and instructor.verify_password(password):
                login_user(instructor, remember=True)
                next = flask.request.args.get("next")
                if not is_safe_url(next):
                    return flask.abort(400)

                return redirect(next or url_for("index"))
            else:
                print("Not a valid login")
                flash("Email or password is invalid")
    else:
        flash("form invalid")
        for error in form.errors:
            flash(error)
    return render_template("login.html", form=form)


@user_management.route('/register', methods=["GET", "POST"])
def register():
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
        flash("form invalid")
    for error in form.errors:
        flash(error)

    return render_template("register.html", form=form)


@user_management.route('/tokens', methods=["GET", "POST"])
@login_required
def tokens():
    tokens = AccessToken.query.filter_by(owner_id=current_user.owner_id).all()
    if tokens is None:
        return flask.abort(400)
    return render_template("tokens.html", tokens=tokens)