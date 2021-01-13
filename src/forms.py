from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators, SubmitField, DateTimeField


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
    start_time = DateTimeField("Start Date")
    end_time = DateTimeField("End Date", [validators.DataRequired()])
    submit = SubmitField("Request Token")


class LoginForm(FlaskForm):
    email = StringField("Email", [validators.DataRequired(), validators.Email()])
    password = PasswordField("Password *", [
        validators.DataRequired(),
        validators.Length(min=8),
    ])