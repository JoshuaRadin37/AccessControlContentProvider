import os

import flask
from flask import Flask, render_template, redirect, flash, url_for, request
from flask_login import login_user, current_user, LoginManager

from database import AccessToken, Instructor, db
from forms import NewInstructorForm
from user_management import user_management

app = Flask(__name__, template_folder='../templates')
app.register_blueprint(user_management)
app.config["SECRET_KEY"] = "oEHYBreJ2QSefBdUhD19PkxC"
appdir = os.path.abspath(os.path.dirname(os.path.dirname("app.py")))
# configure app’s database access
app.config["SQLALCHEMY_DATABASE_URI"] = \
    f"sqlite:///{os.path.join(appdir, 'library.db')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def instructor_loader(email):
    return Instructor.query.get(email=email)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/example/<string:example_name>', methods=["GET"])
def get_content(example_name):
    return 'Getting content ' + example_name


@app.route('/register', methods=["GET", "POST"])
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
            return redirect(url_for("index"))
        else:
            flash("User with this email already exists")

    return render_template("register.html", form=form)


@app.route('/tokens', methods=["GET", "POST"])
def tokens():
    tokens = AccessToken.query.filter_by(owner_id=current_user.owner_id).first()
    if tokens is None:
        return flask.abort(400)
    return render_template("tokens.html", tokens=tokens)


@app.route("/toc", methods=["GET"])
def table_of_contents():
    return render_template("table_of_contents.html")


@app.route('/login', methods=["GET", "POST"])
def login():
    return "OOps not implemented yet lol", 200


if __name__ == '__main__':
    app.run()
