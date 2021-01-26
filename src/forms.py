from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators, SubmitField, DateTimeField, DateField


class NewInstructorForm(FlaskForm):
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
    start_time = DateField("Start Date", [validators.DataRequired()])
    end_time = DateField("End Date", [validators.DataRequired()])
    valid_domain = StringField("Valid Domain", [validators.DataRequired()])
    submit = SubmitField("Request Token")


class LoginForm(FlaskForm):
    email = StringField("Email", [validators.DataRequired(), validators.Email()])
    password = PasswordField("Password *", [
        validators.DataRequired(),
        validators.Length(min=8),
    ])
    submit = SubmitField("Log in")


class GetAccessForm(FlaskForm):
    email = StringField("Email", [validators.DataRequired(), validators.Email()])
    access_code = StringField("Access Code",  [validators.DataRequired()])
    submit = SubmitField("Log in")


