import os

from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager

import database
from contents import access_granted
from database import initialize_db
from models import Instructor
from user_management import initiate_user_functionality
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__, template_folder='../templates')

app.config["SECRET_KEY"] = "oEHYBreJ2QSefBdUhD19PkxC"
appdir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
# configure app’s database access
app.config["SQLALCHEMY_DATABASE_URI"] = \
    f"sqlite:///{os.path.join(appdir, 'library.db')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
login_manager = LoginManager()
login_manager.init_app(app)


csrf = CSRFProtect(app)

#logging.basicConfig(filename='access.log', level=logging.DEBUG)


@login_manager.user_loader
def instructor_loader(email):
    return Instructor.query.filter_by(email=email).first()


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/toc", methods=["GET"])
def table_of_contents():
    return render_template("table_of_contents.html")


@app.route("/reset_database", methods=["GET"])
def reset_database():
    database.reset_database(app)
    return redirect(url_for('index'))


@app.route("/protected", methods=["GET"])
@access_granted()
def protected():
    path = request.args.get('path')
    return render_template(path)


@app.route('/content', methods=["GET"])
def get_content():
    path = request.args.get('path')
    return render_template(path)



initiate_user_functionality(app)
initialize_db(app)


def main():
    app.run()


if __name__ == '__main__':
    main()
