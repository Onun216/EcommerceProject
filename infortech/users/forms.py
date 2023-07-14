from wtforms import Form, BooleanField, StringField, PasswordField, validators, SubmitField, ValidationError, \
    IntegerField
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired, FileField
from .models import User


class UserRegistrationForm(FlaskForm):
    name = StringField('Nome', [validators.Length(min=4, max=25)])
    address = StringField('Morada', [validators.DataRequired()])
    NIF = IntegerField()
    email = StringField('Email: ', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repetir password: ', [validators.DataRequired()])
    submit = SubmitField('Registar')


def validate_email(self, email):
    if User.query.filter_by(username=email.data):
        raise ValidationError('This email address is already in use!')


class UserLoginForm(FlaskForm):
    email = StringField('Email: ', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Password: ', [validators.DataRequired()])


