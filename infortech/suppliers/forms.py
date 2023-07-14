from wtforms import Form, BooleanField, StringField, PasswordField, validators


class SupplierAccountRegistrationForm(Form):
    username = StringField('Utilizador', [validators.Length(min=4, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repetir password')


class LoginForm(Form):
    username = StringField('Utilizador', [validators.Length(min=4, max=50)])
    password = PasswordField('Password', [validators.DataRequired()])
