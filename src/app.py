"""
Contains all of the base functionality for the flask application
"""

import os

from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager

import database
from contents import access_granted
from database import initialize_db
from models import Instructor
from user_management import initiate_user_functionality
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__, template_folder='../templates', static_folder='../static')

app.config["SECRET_KEY"] = "oEHYBreJ2QSefBdUhD19PkxC"
appdir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
# configure app’s database access
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(appdir, 'library.db')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
login_manager = LoginManager()
login_manager.init_app(app)


csrf = CSRFProtect(app)

# logging.basicConfig(filename='access.log', level=logging.DEBUG)


@login_manager.user_loader
def instructor_loader(email):
    """
    Loads the instructor based on the email used at log in
    :param email: The email
    :return: An Instructor instance
    """
    return Instructor.query.filter_by(email=email).first()


@app.route('/')
def index():
    """
    The home page of the website
    """
    return render_template('index.html')


@app.route("/toc", methods=["GET"])
@access_granted
def table_of_contents():
    """
    The table of contents.

    This is a protected page
    """
    return render_template("table_of_contents.html")


@app.route("/reset_database", methods=["GET"])
def reset_database():
    """
    Allows the user to reset the database, dropping all tables and recreating them
    :return: A redirect back to the home page
    """
    database.reset_database(app)
    return redirect(url_for('index'))


@app.route("/protected", methods=["GET"])
@access_granted
def protected():
    """
    Provides protection for a file by required a valid access token
    """
    path = request.args.get('path')
    return render_template(path)


"""
@app.route('/content', methods=["GET"])
def get_content():
    path = request.args.get('path')
    return render_template(path)
"""

initiate_user_functionality(app)
initialize_db(app)


def main():
    """
    Allows for the flask application to be ran if the file itself is being run without the flask shell
    :return:
    """
    app.run()


if __name__ == '__main__':
    main()
