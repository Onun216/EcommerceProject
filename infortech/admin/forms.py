from wtforms import Form, BooleanField, StringField, PasswordField, validators


class RegistrationForm(Form):
    username = StringField('Utilizador', [validators.Length(min=4, max=25)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repetir password')


class LoginForm(Form):
    username = StringField('Utilizador', [validators.Length(min=4, max=5)])
    password = PasswordField('Password', [validators.DataRequired()])

