"""
Contains function related to content control
"""

from functools import wraps

from flask import Blueprint, request, current_app, redirect, url_for, make_response

from models import AccessToken

contents = Blueprint('contents', __name__, template_folder='../templates', )


def initialize_contents(app):
    """
    Initializes the contents sections
    :param app: The flask application
    """
    app.register_blueprint(contents)


def access_granted(func):
    """
    This is a decorator function that when applied to another function forces a user to have a valid access token.

    An access granted function returns the user to the path they intended to visit after a successful log in.
    :param func: the input function
    :return: the decorated function
    """
    def decorated(*args, **kwargs):
        # Checks whether a user has a valid access token active
        # The cookies don't have to exist for this to work
        access_code = request.cookies.get('code')
        email = request.cookies.get('email')

        with current_app.app_context():
            if not AccessToken.can_access(access_code, email):
                response = make_response(redirect(url_for("user_management.student_login")))
                response.set_cookie('last_page', request.full_path)

                return response
            return func(*args, **kwargs)
    decorated.__name__ = func.__name__
    return decorated
