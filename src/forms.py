"""
Contains all of the forms used by the application
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators, SubmitField, DateField


class NewInstructorForm(FlaskForm):
    """
    The instructor registration form.

    The Email must be unique.
    """
    first_name = StringField("First Name *", [validators.DataRequired()])
    last_name = StringField("Last Name *", [validators.DataRequired()])
    email = StringField("Email *", [validators.DataRequired(), validators.Email()])
    password = PasswordField("Password *", [
        validators.DataRequired(),
        validators.Length(min=8),
    ])
    confirm_password = PasswordField("Confirm Password *", [
        validators.DataRequired(),
        validators.Length(min=8),
        validators.equal_to("password", message="Passwords must match")
    ])
    submit = SubmitField("Register")


class NewTokenForm(FlaskForm):
    """
    The new token form
    """
    start_time = DateField("Start Date", [validators.DataRequired()])
    end_time = DateField("End Date", [validators.DataRequired()])
    valid_domain = StringField("Valid Domain", [validators.DataRequired()])
    submit = SubmitField("Request Token")


class LoginForm(FlaskForm):
    """
    The instructor login form
    """
    email = StringField("Email", [validators.DataRequired(), validators.Email()])
    password = PasswordField("Password *", [
        validators.DataRequired(),
        validators.Length(min=8),
    ])
    submit = SubmitField("Log in")


class GetAccessForm(FlaskForm):
    """
    The form that must be completed to gain access to protected areas
    """
    email = StringField("Email", [validators.DataRequired(), validators.Email()])
    access_code = StringField("Access Code",  [validators.DataRequired()])
    submit = SubmitField("Log in")


