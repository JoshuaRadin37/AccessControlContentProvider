from functools import wraps

from flask import Blueprint, request, current_app, abort, redirect, url_for, make_response

from models import AccessToken

contents = Blueprint('contents', __name__, template_folder='../templates', )


def initialize_contents(app):
    app.register_blueprint(contents)


def access_granted():
    def decorator(func):

        @wraps(func)
        def decorated(*args, **kwargs):
            access_code = request.cookies.get('code')
            email = request.cookies.get('email')

            with current_app.app_context():
                if not AccessToken.can_access(access_code, email):
                    response = make_response(redirect(url_for("user_management.student_login")))
                    response.set_cookie('last_page', request.full_path)

                    return response
                return func(*args, **kwargs)

        return decorated

    return decorator