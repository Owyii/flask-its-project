from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, EmailField, PasswordField, SubmitField, BooleanField
from wtforms.validators import Length, DataRequired, Email, EqualTo, ValidationError
from moviecollector.models import User

from flask_login import current_user

'''
Registrazione:
username
email
password
confirm_password

Login:
email
password
remembre_me
'''

class RegistrationForm(FlaskForm):

    username = StringField('Username', validators=[
                           Length(min=2, max=30), DataRequired()])
#    email = EmailField('email', validators=[Length(2, 100)])
    email = StringField('Email', validators=[
                        Length(min=2, max=100), Email(), DataRequired()])
    password = PasswordField('Password', validators=[
                             Length(min=8, max=100), DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[Length(min=8, max=100),
                                                 DataRequired(),
                                                 EqualTo('password')])
    submit = SubmitField('Register Now!')

    # def validate_field(self, field):
    #     if True:
    #         raise ValdationError('Validation Message')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already registered')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
                        Length(min=2, max=100), Email(), DataRequired()])
    password = PasswordField('Password', validators=[
                             Length(min=8, max=100), DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')

class UpdateUserForm(FlaskForm):
    # Campo per l'username con lunghezza minima e massima, non può essere vuoto
    username = StringField('Username', validators=[
        Length(min=2, max=30), DataRequired()])
    # Campo per l'email con lunghezza minima e massima, deve essere una email valida, non può essere vuoto
    email = StringField('Email', validators=[
        Length(min=2, max=100), Email(), DataRequired()])
    # Campo per caricare l'immagine dell'utente con estensioni ammesse
    image_file = FileField('Update your Avatar', validators=[
        FileAllowed(['jpg', 'png'])])
    # Bottone per aggiornare il profilo utente
    submit = SubmitField('Update Your Profile!')

    # Validazione email unica
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email already registered')

    # Validazione username unico
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username already registered')